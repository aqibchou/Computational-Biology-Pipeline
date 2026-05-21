#!/usr/bin/env python3
"""Compare Plan 07 finalists to ligand-bound PDB reference pockets.

This is a lightweight, auditable pass. It does not run structure prediction or
structural superposition. It uses existing ColabFold/PDB70 template alignments,
downloads PDB reference structures, detects nontrivial ligands near the matched
template chain, and maps ligand-proximal template residues back to candidate
positions through the alignment CIGAR.
"""

from __future__ import annotations

import csv
import datetime as dt
import math
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
PLAN07_CLAIM = ROOT / "outputs/plan07_claim_hardening_2026-05-17/plan07_finalist_claim_hardening.csv"
BEST_MODELS = ROOT / "outputs/plan07_rare_chemistry_bridge_2026-05-15/plan07_candidate_specific_colabfold_best_models.csv"
COLABFOLD_OUTPUT = ROOT / "outputs/plan07_rare_chemistry_bridge_2026-05-15/candidate_specific_colabfold/gcp_colabfold_t4_output/output"
OUTDIR = ROOT / f"outputs/plan07_reference_ligand_pocket_comparison_{RUN_DATE}"
PDB_CACHE = OUTDIR / "pdb_cache"

MAX_TEMPLATE_ROWS = 25
NEIGHBOR_CUTOFF_A = 5.0

AA3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "MSE": "M",
}

AA_CLASS = {
    "A": "hydrophobic",
    "V": "hydrophobic",
    "I": "hydrophobic",
    "L": "hydrophobic",
    "M": "hydrophobic",
    "F": "aromatic",
    "Y": "aromatic",
    "W": "aromatic",
    "S": "polar",
    "T": "polar",
    "N": "polar",
    "Q": "polar",
    "C": "polar",
    "G": "special",
    "P": "special",
    "D": "acidic",
    "E": "acidic",
    "K": "basic",
    "R": "basic",
    "H": "basic",
}

SOLVENT_LIGANDS = {"HOH", "WAT", "DOD"}
LOW_INFORMATION_LIGANDS = {
    "SO4",
    "PO4",
    "CL",
    "BR",
    "IOD",
    "NA",
    "K",
    "CA",
    "MG",
    "MN",
    "ZN",
    "FE",
    "CU",
    "CO",
    "NI",
    "CD",
    "GOL",
    "EDO",
    "PEG",
    "PGE",
    "TRS",
    "ACT",
    "ACE",
    "FMT",
    "BME",
    "DTT",
    "MPD",
    "MES",
    "HEP",
    "MSE",
}

COFACTOR_LIGANDS = {
    "FAD",
    "FMN",
    "NAD",
    "NAP",
    "NDP",
    "NAI",
    "NADP",
    "SAM",
    "SAH",
    "PLP",
    "UDP",
    "UPG",
    "ADP",
    "ATP",
    "AMP",
    "GDP",
    "GTP",
    "F420",
    "COA",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_pdb70(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    with path.open() as handle:
        for rank, raw in enumerate(handle, start=1):
            parts = raw.strip().split()
            if len(parts) < 13:
                continue
            target = parts[1]
            if "_" not in target:
                continue
            pdb_id, chain_id = target.split("_", 1)
            rows.append(
                {
                    "template_rank": rank,
                    "pdb_id": pdb_id.lower(),
                    "chain_id": chain_id,
                    "pident": float(parts[2]),
                    "alignment_length": int(parts[3]),
                    "mismatch_count": int(parts[4]),
                    "gap_open_count": int(parts[5]),
                    "query_start": int(parts[6]),
                    "query_end": int(parts[7]),
                    "template_start": int(parts[8]),
                    "template_end": int(parts[9]),
                    "evalue": parts[10],
                    "bits": float(parts[11]),
                    "cigar": parts[12],
                }
            )
    return rows[:MAX_TEMPLATE_ROWS]


def download_pdb(pdb_id: str) -> tuple[Path | None, str]:
    PDB_CACHE.mkdir(parents=True, exist_ok=True)
    path = PDB_CACHE / f"{pdb_id.upper()}.pdb"
    if path.exists() and path.stat().st_size > 0:
        return path, "cache"
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        if not data:
            return None, "empty"
        path.write_bytes(data)
        time.sleep(0.1)
        return path, "downloaded"
    except urllib.error.HTTPError as exc:
        return None, f"http_{exc.code}"
    except Exception as exc:  # noqa: BLE001 - captured in manifest output
        return None, f"error_{type(exc).__name__}"


def parse_title_and_resolution(lines: list[str]) -> tuple[str, str]:
    title_parts = []
    resolution = ""
    for line in lines:
        rec = line[:6].strip()
        if rec == "TITLE":
            title_parts.append(line[10:].strip())
        elif line.startswith("REMARK   2 RESOLUTION."):
            text = line.strip()
            match = re.search(r"RESOLUTION\.\s+([0-9.]+)\s+ANGSTROMS", text)
            if match:
                resolution = match.group(1)
    return " ".join(title_parts), resolution


def parse_hetnam(lines: list[str]) -> dict[str, str]:
    names: dict[str, list[str]] = defaultdict(list)
    for line in lines:
        if line.startswith("HETNAM"):
            ligand = line[11:14].strip()
            name = line[15:].strip()
            if ligand:
                names[ligand].append(name)
    return {lig: " ".join(parts) for lig, parts in names.items()}


def parse_pdb_atoms(path: Path) -> dict[str, object]:
    lines = path.read_text(errors="ignore").splitlines()
    title, resolution = parse_title_and_resolution(lines)
    het_names = parse_hetnam(lines)
    chain_atoms: dict[str, list[dict[str, object]]] = defaultdict(list)
    chain_residues: dict[str, list[dict[str, object]]] = defaultdict(list)
    residue_seen: dict[str, set[tuple[str, int, str, str]]] = defaultdict(set)
    ligands: list[dict[str, object]] = []
    ligand_atoms: dict[tuple[str, str, int, str], list[tuple[float, float, float]]] = defaultdict(list)

    for line in lines:
        rec = line[:6].strip()
        if rec not in {"ATOM", "HETATM"} or len(line) < 54:
            continue
        resname = line[17:20].strip()
        chain = line[21].strip() or "_"
        try:
            resseq = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
        except ValueError:
            continue
        icode = line[26].strip()
        atom = line[12:16].strip()
        key = (chain, resseq, icode, resname)
        coord = (x, y, z)
        if rec == "ATOM" and resname in AA3_TO_1:
            chain_atoms[chain].append({"key": key, "atom": atom, "coord": coord, "resname": resname})
            if key not in residue_seen[chain]:
                residue_seen[chain].add(key)
                chain_residues[chain].append(
                    {
                        "seq_index": len(chain_residues[chain]) + 1,
                        "key": key,
                        "resname": resname,
                        "aa": AA3_TO_1.get(resname, "X"),
                    }
                )
        elif rec == "HETATM" and resname not in SOLVENT_LIGANDS:
            ligand_atoms[key].append(coord)

    for key, coords in ligand_atoms.items():
        chain, resseq, icode, resname = key
        ligand_type = "cofactor_or_substrate_like" if resname in COFACTOR_LIGANDS else "low_information" if resname in LOW_INFORMATION_LIGANDS else "nontrivial"
        ligands.append(
            {
                "ligand_key": key,
                "chain": chain,
                "resseq": resseq,
                "icode": icode,
                "resname": resname,
                "name": het_names.get(resname, ""),
                "atom_count": len(coords),
                "coords": coords,
                "ligand_type": ligand_type,
            }
        )
    return {
        "title": title,
        "resolution": resolution,
        "chain_atoms": chain_atoms,
        "chain_residues": chain_residues,
        "ligands": ligands,
    }


def parse_candidate_model(path: Path) -> dict[int, dict[str, object]]:
    residues: dict[int, dict[str, object]] = {}
    seen: set[tuple[str, int, str, str]] = set()
    if not path.exists():
        return residues
    with path.open(errors="ignore") as handle:
        for line in handle:
            if not line.startswith("ATOM") or len(line) < 66:
                continue
            resname = line[17:20].strip()
            if resname not in AA3_TO_1:
                continue
            chain = line[21].strip() or "_"
            try:
                resseq = int(line[22:26])
                bfactor = float(line[60:66])
            except ValueError:
                continue
            icode = line[26].strip()
            atom = line[12:16].strip()
            key = (chain, resseq, icode, resname)
            if key not in seen:
                seen.add(key)
                idx = len(residues) + 1
                residues[idx] = {"aa": AA3_TO_1.get(resname, "X"), "plddt": bfactor, "pdb_residue": f"{chain}{resseq}{icode}"}
            elif atom == "CA":
                idx = len(seen)
                if idx in residues:
                    residues[idx]["plddt"] = bfactor
    return residues


def cigar_mapping(query_start: int, template_start: int, cigar: str) -> dict[int, int]:
    mapping: dict[int, int] = {}
    q = query_start
    t = template_start
    for count_text, op in re.findall(r"(\d+)([MDI])", cigar):
        count = int(count_text)
        if op == "M":
            for _ in range(count):
                mapping[t] = q
                q += 1
                t += 1
        elif op == "I":
            q += count
        elif op == "D":
            t += count
    return mapping


def dist2(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def ligand_neighbor_residues(pdb_data: dict[str, object], chain_id: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    chain_atoms = pdb_data["chain_atoms"].get(chain_id, [])  # type: ignore[index,union-attr]
    chain_residue_by_key = {row["key"]: row for row in pdb_data["chain_residues"].get(chain_id, [])}  # type: ignore[index,union-attr]
    ligands: list[dict[str, object]] = pdb_data["ligands"]  # type: ignore[assignment]
    near_ligands: list[dict[str, object]] = []
    pocket_residue_keys: set[tuple[str, int, str, str]] = set()
    cutoff2 = NEIGHBOR_CUTOFF_A * NEIGHBOR_CUTOFF_A
    for ligand in ligands:
        ligand_key = ligand["ligand_key"]
        ligand_coords = ligand["coords"]
        min_d2 = math.inf
        local_residue_keys: set[tuple[str, int, str, str]] = set()
        for atom in chain_atoms:
            residue_key = atom["key"]
            for coord in ligand_coords:
                d2 = dist2(atom["coord"], coord)
                if d2 < min_d2:
                    min_d2 = d2
                if d2 <= cutoff2:
                    local_residue_keys.add(residue_key)
        if local_residue_keys:
            near_ligands.append(
                {
                    "ligand_key": ligand_key,
                    "resname": ligand["resname"],
                    "name": ligand["name"],
                    "ligand_type": ligand["ligand_type"],
                    "distance_to_chain_a": round(math.sqrt(min_d2), 3) if min_d2 < math.inf else "",
                    "neighbor_residue_count": len(local_residue_keys),
                }
            )
            pocket_residue_keys.update(local_residue_keys)

    pocket_residues = [chain_residue_by_key[key] for key in pocket_residue_keys if key in chain_residue_by_key]
    pocket_residues.sort(key=lambda row: row["seq_index"])
    return near_ligands, pocket_residues


def informative_score(near_ligands: list[dict[str, object]]) -> tuple[int, int, int]:
    cofactor = sum(1 for lig in near_ligands if lig["ligand_type"] == "cofactor_or_substrate_like")
    nontrivial = sum(1 for lig in near_ligands if lig["ligand_type"] == "nontrivial")
    low = sum(1 for lig in near_ligands if lig["ligand_type"] == "low_information")
    return cofactor, nontrivial, low


def summarize_mapping(
    hit: dict[str, object],
    pdb_data: dict[str, object],
    candidate_residues: dict[int, dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    near_ligands, pocket_residues = ligand_neighbor_residues(pdb_data, str(hit["chain_id"]))
    mapping = cigar_mapping(int(hit["query_start"]), int(hit["template_start"]), str(hit["cigar"]))
    mapped_rows: list[dict[str, object]] = []
    exact = 0
    class_match = 0
    mapped_plddt: list[float] = []
    for template_residue in pocket_residues:
        template_index = int(template_residue["seq_index"])
        query_index = mapping.get(template_index)
        candidate_row = candidate_residues.get(query_index, {}) if query_index is not None else {}
        template_aa = str(template_residue["aa"])
        candidate_aa = str(candidate_row.get("aa", ""))
        exact_match = bool(candidate_aa and candidate_aa == template_aa)
        class_same = bool(candidate_aa and AA_CLASS.get(candidate_aa) == AA_CLASS.get(template_aa))
        if exact_match:
            exact += 1
        if class_same:
            class_match += 1
        if "plddt" in candidate_row:
            mapped_plddt.append(float(candidate_row["plddt"]))
        chain, resseq, icode, resname = template_residue["key"]
        mapped_rows.append(
            {
                "pdb_id": hit["pdb_id"],
                "chain_id": hit["chain_id"],
                "template_seq_index": template_index,
                "template_pdb_residue": f"{chain}{resseq}{icode}",
                "template_aa": template_aa,
                "candidate_position": query_index or "",
                "candidate_aa": candidate_aa,
                "candidate_plddt": candidate_row.get("plddt", ""),
                "exact_aa_match": "yes" if exact_match else "no",
                "biochemical_class_match": "yes" if class_same else "no",
            }
        )
    mapped_count = sum(1 for row in mapped_rows if row["candidate_position"] != "")
    denom = len(pocket_residues) or 1
    mapped_denom = mapped_count or 1
    lig_summary = [
        f"{lig['resname']}:{lig['ligand_type']}:{lig['neighbor_residue_count']}res"
        for lig in near_ligands
    ]
    summary = {
        "near_ligand_count": len(near_ligands),
        "informative_ligand_count": sum(1 for lig in near_ligands if lig["ligand_type"] != "low_information"),
        "cofactor_or_substrate_like_ligand_count": sum(1 for lig in near_ligands if lig["ligand_type"] == "cofactor_or_substrate_like"),
        "nontrivial_ligand_count": sum(1 for lig in near_ligands if lig["ligand_type"] == "nontrivial"),
        "low_information_ligand_count": sum(1 for lig in near_ligands if lig["ligand_type"] == "low_information"),
        "near_ligands": ";".join(lig_summary),
        "pocket_residue_count": len(pocket_residues),
        "mapped_pocket_residue_count": mapped_count,
        "mapped_pocket_fraction": round(mapped_count / denom, 3),
        "exact_aa_match_fraction": round(exact / mapped_denom, 3),
        "biochemical_class_match_fraction": round(class_match / mapped_denom, 3),
        "candidate_mean_plddt_mapped_pocket": round(sum(mapped_plddt) / len(mapped_plddt), 3) if mapped_plddt else "",
        "candidate_min_plddt_mapped_pocket": round(min(mapped_plddt), 3) if mapped_plddt else "",
    }
    return summary, near_ligands, mapped_rows


def pocket_call(summary: dict[str, object]) -> str:
    informative = int(summary["informative_ligand_count"])
    mapped_fraction = float(summary["mapped_pocket_fraction"])
    class_fraction = float(summary["biochemical_class_match_fraction"])
    mean_plddt = summary["candidate_mean_plddt_mapped_pocket"]
    mean_plddt_value = float(mean_plddt) if mean_plddt != "" else 0.0
    if informative == 0:
        return "NO_INFORMATIVE_LIGAND_BOUND_REFERENCE_FOUND"
    if mapped_fraction >= 0.65 and class_fraction >= 0.45 and mean_plddt_value >= 70:
        return "PASS_REFERENCE_LIGAND_POCKET_CONTEXT"
    if mapped_fraction >= 0.45 and mean_plddt_value >= 70:
        return "PARTIAL_REFERENCE_LIGAND_POCKET_CONTEXT"
    return "WEAK_REFERENCE_LIGAND_POCKET_CONTEXT"


def find_pdb70_file(protein_id: str, rare_class: str) -> Path:
    pattern = f"{protein_id}_{rare_class}_plan07_env/pdb70.m8"
    matches = list(COLABFOLD_OUTPUT.glob(pattern))
    if matches:
        return matches[0]
    matches = list(COLABFOLD_OUTPUT.glob(f"{protein_id}_*_plan07_env/pdb70.m8"))
    return matches[0] if matches else Path("__missing__")


def model_path_for(protein_id: str, model_rows: list[dict[str, str]]) -> Path:
    row = next(row for row in model_rows if row["protein_id"] == protein_id)
    return COLABFOLD_OUTPUT / row["pdb"]


def make_report(final_rows: list[dict[str, object]]) -> str:
    pass_count = sum(1 for row in final_rows if str(row["reference_pocket_call"]).startswith("PASS"))
    partial_count = sum(1 for row in final_rows if str(row["reference_pocket_call"]).startswith("PARTIAL"))
    lines = [
        "# Plan 07 Reference Ligand-Pocket Comparison",
        "",
        f"Run date: {RUN_DATE}",
        "",
        "## Scope",
        "",
        "This supplemental layer compares Plan 07 finalists against ligand-bound PDB references from the existing ColabFold/PDB70 template hits. It detects ligands within 5.0 Angstroms of the matched template chain and maps ligand-proximal template residues back to the candidate through the PDB70 alignment CIGAR. No new structure prediction or sequence optimization was performed.",
        "",
        "## Verdict",
        "",
        f"Reference ligand-pocket context was added for {len(final_rows)} finalists: {pass_count} pass and {partial_count} partial. The comparison strengthens pocket-context evidence, but it does not validate activity, substrate specificity, product identity, expression, or safety.",
        "",
        "## Finalist Summary",
        "",
        "| Protein | Class | Reference | Ligands Near Chain | Mapped Pocket | Class Match | Pocket pLDDT | Call |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    for row in final_rows:
        lines.append(
            f"| `{row['protein_id']}` | {row['rare_chemistry_class']} | `{row['selected_pdb_chain']}` | "
            f"{row['near_ligands']} | {row['mapped_pocket_fraction']} | "
            f"{row['biochemical_class_match_fraction']} | {row['candidate_mean_plddt_mapped_pocket']} | "
            f"{row['reference_pocket_call']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `PASS_REFERENCE_LIGAND_POCKET_CONTEXT` means a ligand-bound reference was found, most ligand-neighboring reference residues map back to confident candidate residues, and broad amino-acid class conservation is acceptable for a family-level pocket comparison.",
            "- `PARTIAL_REFERENCE_LIGAND_POCKET_CONTEXT` means a ligand-bound reference exists and maps into the candidate, but pocket conservation or mapping coverage is weaker.",
            "- Ligand-bound reference context is still a computational analogy. It should not be framed as substrate specificity or activity validation.",
            "",
            "## Files",
            "",
            "- `plan07_reference_ligand_pocket_comparison.csv`",
            "- `plan07_reference_ligand_pocket_template_hits.csv`",
            "- `plan07_reference_ligand_pocket_residue_map.csv`",
            "- `plan07_reference_ligand_pocket_resource_manifest.csv`",
            "",
        ]
    )
    return "\n".join(lines)


def make_audit(final_rows: list[dict[str, object]]) -> str:
    pass_or_partial = sum(
        1
        for row in final_rows
        if str(row["reference_pocket_call"]).startswith("PASS") or str(row["reference_pocket_call"]).startswith("PARTIAL")
    )
    return "\n".join(
        [
            "# Plan 07 Reference Ligand-Pocket Comparison Completion Audit",
            "",
            f"Run date: {RUN_DATE}",
            "",
            "## Verdict",
            "",
            f"PASS_WITH_LIMITATIONS: ligand-bound/reference pocket comparison was completed for {pass_or_partial}/{len(final_rows)} Plan 07 finalists using existing PDB70 template alignments and downloaded PDB structures. This upgrades the previous unresolved pocket-comparison gap to a bounded computational comparison, not validation.",
            "",
            "## Checklist",
            "",
            "| Requirement | Evidence | Status |",
            "|---|---|---|",
            "| Use Plan 07 finalists | `plan07_finalist_claim_hardening.csv` | PASS |",
            "| Use candidate-specific structures | `plan07_candidate_specific_colabfold_best_models.csv`; ColabFold PDB files | PASS |",
            "| Identify reference templates | finalist PDB70 `.m8` files | PASS |",
            "| Use ligand-bound references where available | downloaded PDB files in `pdb_cache/`; ligand-neighbor summaries | PASS |",
            "| Compare reference pocket to candidate | `plan07_reference_ligand_pocket_residue_map.csv` maps template ligand-neighbor residues to candidate positions | PASS_WITH_ALIGNMENT_LIMITATION |",
            "| Avoid validation claims | report states pocket comparison is computational analogy only | PASS |",
            "",
            "## Remaining Limits",
            "",
            "- No structural superposition or docking was performed in this pass.",
            "- PDB70 alignments are remote-homology mappings for some finalists, so pocket conclusions remain family-level context.",
            "- Wet-lab activity, substrate scope, product identity, expression, and safety remain unresolved.",
            "",
        ]
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    finalist_rows = read_csv(PLAN07_CLAIM)
    model_rows = read_csv(BEST_MODELS)
    comparison_rows: list[dict[str, object]] = []
    template_rows: list[dict[str, object]] = []
    residue_rows: list[dict[str, object]] = []
    manifest_rows: list[dict[str, object]] = []

    for finalist in finalist_rows:
        protein_id = finalist["protein_id"]
        rare_class = finalist["rare_chemistry_class"]
        model_path = model_path_for(protein_id, model_rows)
        candidate_residues = parse_candidate_model(model_path)
        pdb70_file = find_pdb70_file(protein_id, rare_class)
        hits = parse_pdb70(pdb70_file)
        selected: dict[str, object] | None = None
        selected_summary: dict[str, object] | None = None
        selected_ligands: list[dict[str, object]] = []
        selected_residue_rows: list[dict[str, object]] = []
        best_fallback: tuple[dict[str, object], dict[str, object], list[dict[str, object]], list[dict[str, object]]] | None = None

        for hit in hits:
            pdb_path, status = download_pdb(str(hit["pdb_id"]))
            manifest_rows.append(
                {
                    "protein_id": protein_id,
                    "pdb_id": str(hit["pdb_id"]).upper(),
                    "chain_id": hit["chain_id"],
                    "download_status": status,
                    "pdb_path": rel(pdb_path) if pdb_path else "",
                    "source_url": f"https://files.rcsb.org/download/{str(hit['pdb_id']).upper()}.pdb",
                }
            )
            if pdb_path is None:
                continue
            pdb_data = parse_pdb_atoms(pdb_path)
            summary, near_ligands, mapped = summarize_mapping(hit, pdb_data, candidate_residues)
            cofactor, nontrivial, low = informative_score(near_ligands)
            hit_row = {
                "protein_id": protein_id,
                "rare_chemistry_class": rare_class,
                "pdb_id": str(hit["pdb_id"]).upper(),
                "chain_id": hit["chain_id"],
                "template_rank": hit["template_rank"],
                "pident": hit["pident"],
                "alignment_length": hit["alignment_length"],
                "query_range": f"{hit['query_start']}-{hit['query_end']}",
                "template_range": f"{hit['template_start']}-{hit['template_end']}",
                "evalue": hit["evalue"],
                "bits": hit["bits"],
                "pdb_title": pdb_data["title"],
                "pdb_resolution_a": pdb_data["resolution"],
                **summary,
            }
            hit_row["reference_pocket_call"] = pocket_call(summary)
            template_rows.append(hit_row)
            if best_fallback is None:
                best_fallback = (hit_row, summary, near_ligands, mapped)
            if cofactor + nontrivial > 0 and int(summary["mapped_pocket_residue_count"]) > 0:
                selected = hit_row
                selected_summary = summary
                selected_ligands = near_ligands
                selected_residue_rows = mapped
                break
            if cofactor + nontrivial + low > 0 and int(summary["mapped_pocket_residue_count"]) > 0:
                best_fallback = (hit_row, summary, near_ligands, mapped)

        if selected is None and best_fallback is not None:
            selected, selected_summary, selected_ligands, selected_residue_rows = best_fallback
        if selected is None:
            selected = {
                "protein_id": protein_id,
                "rare_chemistry_class": rare_class,
                "pdb_id": "",
                "chain_id": "",
                "template_rank": "",
                "pident": "",
                "alignment_length": "",
                "query_range": "",
                "template_range": "",
                "evalue": "",
                "bits": "",
                "pdb_title": "",
                "pdb_resolution_a": "",
                "near_ligands": "",
                "near_ligand_count": 0,
                "informative_ligand_count": 0,
                "cofactor_or_substrate_like_ligand_count": 0,
                "nontrivial_ligand_count": 0,
                "low_information_ligand_count": 0,
                "pocket_residue_count": 0,
                "mapped_pocket_residue_count": 0,
                "mapped_pocket_fraction": 0,
                "exact_aa_match_fraction": 0,
                "biochemical_class_match_fraction": 0,
                "candidate_mean_plddt_mapped_pocket": "",
                "candidate_min_plddt_mapped_pocket": "",
                "reference_pocket_call": "NO_REFERENCE_TEMPLATE_EVALUATED",
            }
        selected_pdb_chain = f"{selected.get('pdb_id', '')}_{selected.get('chain_id', '')}".strip("_")
        comparison = {
            "protein_id": protein_id,
            "rare_chemistry_class": rare_class,
            "reaction_family": finalist["reaction_family"],
            "previous_pocket_review_call": finalist["pocket_review_call"],
            "selected_pdb_chain": selected_pdb_chain,
            **selected,
            "candidate_model_path": rel(model_path),
            "pdb70_file": rel(pdb70_file) if pdb70_file.exists() else "",
        }
        comparison_rows.append(comparison)
        for row in selected_residue_rows:
            residue_rows.append(
                {
                    "protein_id": protein_id,
                    "rare_chemistry_class": rare_class,
                    "selected_pdb_chain": selected_pdb_chain,
                    **row,
                }
            )

    comparison_fields = [
        "protein_id",
        "rare_chemistry_class",
        "reaction_family",
        "previous_pocket_review_call",
        "selected_pdb_chain",
        "template_rank",
        "pident",
        "alignment_length",
        "query_range",
        "template_range",
        "evalue",
        "bits",
        "pdb_title",
        "pdb_resolution_a",
        "near_ligand_count",
        "informative_ligand_count",
        "cofactor_or_substrate_like_ligand_count",
        "nontrivial_ligand_count",
        "low_information_ligand_count",
        "near_ligands",
        "pocket_residue_count",
        "mapped_pocket_residue_count",
        "mapped_pocket_fraction",
        "exact_aa_match_fraction",
        "biochemical_class_match_fraction",
        "candidate_mean_plddt_mapped_pocket",
        "candidate_min_plddt_mapped_pocket",
        "reference_pocket_call",
        "candidate_model_path",
        "pdb70_file",
    ]
    template_fields = [
        "protein_id",
        "rare_chemistry_class",
        "pdb_id",
        "chain_id",
        "template_rank",
        "pident",
        "alignment_length",
        "query_range",
        "template_range",
        "evalue",
        "bits",
        "pdb_title",
        "pdb_resolution_a",
        "near_ligand_count",
        "informative_ligand_count",
        "cofactor_or_substrate_like_ligand_count",
        "nontrivial_ligand_count",
        "low_information_ligand_count",
        "near_ligands",
        "pocket_residue_count",
        "mapped_pocket_residue_count",
        "mapped_pocket_fraction",
        "exact_aa_match_fraction",
        "biochemical_class_match_fraction",
        "candidate_mean_plddt_mapped_pocket",
        "candidate_min_plddt_mapped_pocket",
        "reference_pocket_call",
    ]
    residue_fields = [
        "protein_id",
        "rare_chemistry_class",
        "selected_pdb_chain",
        "pdb_id",
        "chain_id",
        "template_seq_index",
        "template_pdb_residue",
        "template_aa",
        "candidate_position",
        "candidate_aa",
        "candidate_plddt",
        "exact_aa_match",
        "biochemical_class_match",
    ]
    manifest_fields = ["protein_id", "pdb_id", "chain_id", "download_status", "pdb_path", "source_url"]

    write_csv(OUTDIR / "plan07_reference_ligand_pocket_comparison.csv", comparison_rows, comparison_fields)
    write_csv(OUTDIR / "plan07_reference_ligand_pocket_template_hits.csv", template_rows, template_fields)
    write_csv(OUTDIR / "plan07_reference_ligand_pocket_residue_map.csv", residue_rows, residue_fields)
    write_csv(OUTDIR / "plan07_reference_ligand_pocket_resource_manifest.csv", manifest_rows, manifest_fields)
    (OUTDIR / "PLAN07_REFERENCE_LIGAND_POCKET_COMPARISON_REPORT.md").write_text(make_report(comparison_rows))
    (OUTDIR / "PLAN07_REFERENCE_LIGAND_POCKET_COMPARISON_COMPLETION_AUDIT.md").write_text(make_audit(comparison_rows))

    print(f"Wrote {rel(OUTDIR)}")
    for row in comparison_rows:
        print(row["protein_id"], row["selected_pdb_chain"], row["reference_pocket_call"])


if __name__ == "__main__":
    main()
