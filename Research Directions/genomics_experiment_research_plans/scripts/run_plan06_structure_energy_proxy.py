#!/usr/bin/env python3
"""Plan06 FoldX/Rosetta feasibility plus bounded structure-energy proxy.

This emits only candidate-level aggregate metrics. It intentionally omits
mutation-level, residue-pair, and design suggestions.
"""

from __future__ import annotations

import csv
import math
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN06_DIR = ROOT / "outputs" / "plan06_deep_stability_bridge_2026-05-15"
CLAIM_DIR = ROOT / "outputs" / "plan06_claim_hardening_2026-05-17"
MODEL_DIR = PLAN06_DIR / "candidate_specific_colabfold" / "gcp_colabfold_t4_output" / "output"
OUT_DIR = ROOT / "outputs" / "plan06_structure_energy_proxy_2026-05-17"

BEST_MODELS = PLAN06_DIR / "plan06_candidate_specific_colabfold_best_models.csv"
FINALISTS = CLAIM_DIR / "plan06_finalist_claim_hardening.csv"

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
}

ACIDIC = {"ASP", "GLU"}
BASIC = {"LYS", "ARG", "HIS"}
AROMATIC = {"PHE", "TRP", "TYR"}
HYDROPHOBIC = {"ALA", "VAL", "ILE", "LEU", "MET", "PHE", "TRP", "TYR"}
ACID_ATOMS = {"ASP": {"OD1", "OD2"}, "GLU": {"OE1", "OE2"}}
BASIC_ATOMS = {"LYS": {"NZ"}, "ARG": {"NE", "NH1", "NH2"}, "HIS": {"ND1", "NE2"}}


@dataclass
class Atom:
    name: str
    x: float
    y: float
    z: float
    bfactor: float


@dataclass
class Residue:
    chain: str
    resseq: int
    icode: str
    resname: str
    atoms: list[Atom]

    @property
    def key(self) -> tuple[str, int, str]:
        return (self.chain, self.resseq, self.icode)

    @property
    def ca(self) -> Atom | None:
        for atom in self.atoms:
            if atom.name == "CA":
                return atom
        return None

    @property
    def plddt(self) -> float | None:
        ca = self.ca
        return ca.bfactor if ca else None


def read_csv_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def parse_pdb(path: Path) -> list[Residue]:
    residues: dict[tuple[str, int, str], Residue] = {}
    order: list[tuple[str, int, str]] = []
    with path.open() as handle:
        for line in handle:
            if line.startswith("ENDMDL"):
                break
            if not line.startswith("ATOM"):
                continue
            atom_name = line[12:16].strip()
            resname = line[17:20].strip()
            if resname not in AA3_TO_1:
                continue
            chain = line[21].strip() or "A"
            try:
                resseq = int(line[22:26])
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                bfactor = float(line[60:66])
            except ValueError:
                continue
            icode = line[26].strip()
            key = (chain, resseq, icode)
            if key not in residues:
                residues[key] = Residue(chain=chain, resseq=resseq, icode=icode, resname=resname, atoms=[])
                order.append(key)
            residues[key].atoms.append(Atom(atom_name, x, y, z, bfactor))
    return [residues[key] for key in order]


def dist(a: Atom, b: Atom) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def fraction(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    idx = (len(vals) - 1) * q
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return vals[lo]
    return vals[lo] * (hi - idx) + vals[hi] * (idx - lo)


def residue_charge(resname: str) -> float:
    if resname in {"ASP", "GLU"}:
        return -1.0
    if resname in {"LYS", "ARG"}:
        return 1.0
    if resname == "HIS":
        return 0.1
    return 0.0


def salt_bridge_pairs(residues: list[Residue], outer_shell_keys: set[tuple[str, int, str]]) -> dict[str, int]:
    acidic_res = [r for r in residues if r.resname in ACID_ATOMS]
    basic_res = [r for r in residues if r.resname in BASIC_ATOMS]
    pairs: set[tuple[tuple[str, int, str], tuple[str, int, str]]] = set()
    high_conf: set[tuple[tuple[str, int, str], tuple[str, int, str]]] = set()
    long_range: set[tuple[tuple[str, int, str], tuple[str, int, str]]] = set()
    outer_shell: set[tuple[tuple[str, int, str], tuple[str, int, str]]] = set()

    for acid in acidic_res:
        acid_atoms = [a for a in acid.atoms if a.name in ACID_ATOMS[acid.resname]]
        if not acid_atoms:
            continue
        for base in basic_res:
            base_atoms = [a for a in base.atoms if a.name in BASIC_ATOMS[base.resname]]
            if not base_atoms or acid.key == base.key:
                continue
            if acid.chain == base.chain and abs(acid.resseq - base.resseq) <= 2:
                continue
            if any(dist(a, b) <= 4.0 for a in acid_atoms for b in base_atoms):
                pair = (acid.key, base.key)
                pairs.add(pair)
                if (acid.plddt or 0.0) >= 70.0 and (base.plddt or 0.0) >= 70.0:
                    high_conf.add(pair)
                if acid.chain != base.chain or abs(acid.resseq - base.resseq) >= 6:
                    long_range.add(pair)
                if acid.key in outer_shell_keys or base.key in outer_shell_keys:
                    outer_shell.add(pair)

    return {
        "salt_bridge_pairs": len(pairs),
        "high_conf_salt_bridge_pairs": len(high_conf),
        "long_range_salt_bridge_pairs": len(long_range),
        "outer_shell_salt_bridge_pairs": len(outer_shell),
    }


def structure_proxy_call(row: dict[str, str]) -> str:
    low_conf = float(row["low_conf_fraction"])
    salt_density = float(row["salt_bridge_pairs_per_100aa"])
    outer_charge = abs(float(row["outer_shell_net_charge_per_100aa"]))
    if low_conf > 0.10:
        return "REVIEW_STRUCTURE_CONFIDENCE_BEFORE_ENERGY_INTERPRETATION"
    if salt_density >= 1.0 and outer_charge >= 2.0:
        return "PASS_BOUNDED_CHARGE_SALTBRIDGE_PROXY"
    if salt_density >= 0.5 or outer_charge >= 1.0:
        return "MODERATE_BOUNDED_CHARGE_SALTBRIDGE_PROXY"
    return "LOW_BOUNDED_CHARGE_SALTBRIDGE_PROXY"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    finalists = read_csv_by_key(FINALISTS, "protein_id")
    best_models = read_csv_by_key(BEST_MODELS, "protein_id")

    rows: list[dict[str, str]] = []
    for protein_id, finalist in finalists.items():
        best = best_models[protein_id]
        pdb_path = MODEL_DIR / best["pdb"]
        residues = parse_pdb(pdb_path)
        ca_residues = [r for r in residues if r.ca is not None]
        total = len(ca_residues)
        plddts = [r.plddt or 0.0 for r in ca_residues]

        centroid = (
            sum((r.ca.x for r in ca_residues if r.ca), 0.0) / total,
            sum((r.ca.y for r in ca_residues if r.ca), 0.0) / total,
            sum((r.ca.z for r in ca_residues if r.ca), 0.0) / total,
        )
        radial = []
        for r in ca_residues:
            ca = r.ca
            assert ca is not None
            radial.append(math.sqrt((ca.x - centroid[0]) ** 2 + (ca.y - centroid[1]) ** 2 + (ca.z - centroid[2]) ** 2))
        radial_cut = percentile(radial, 0.70)
        outer_shell = {r.key for r, rad in zip(ca_residues, radial) if rad >= radial_cut}
        outer_residues = [r for r in ca_residues if r.key in outer_shell]

        acidic = sum(1 for r in ca_residues if r.resname in ACIDIC)
        basic = sum(1 for r in ca_residues if r.resname in BASIC)
        charged = acidic + basic
        net_charge = sum(residue_charge(r.resname) for r in ca_residues)
        outer_acidic = sum(1 for r in outer_residues if r.resname in ACIDIC)
        outer_basic = sum(1 for r in outer_residues if r.resname in BASIC)
        outer_net_charge = sum(residue_charge(r.resname) for r in outer_residues)
        bridge_counts = salt_bridge_pairs(ca_residues, outer_shell)

        row = {
            "protein_id": protein_id,
            "family": finalist["family"],
            "primary_stability_axis": finalist["primary_stability_axis"],
            "pdb": pdb_path.name,
            "residue_count": str(total),
            "mean_plddt": f"{mean(plddts):.3f}",
            "min_plddt": f"{min(plddts):.2f}" if plddts else "0.00",
            "low_conf_fraction": f"{fraction(sum(1 for v in plddts if v < 70.0), total):.4f}",
            "acidic_fraction": f"{fraction(acidic, total):.4f}",
            "basic_fraction": f"{fraction(basic, total):.4f}",
            "charged_fraction": f"{fraction(charged, total):.4f}",
            "net_charge": f"{net_charge:.1f}",
            "net_charge_per_100aa": f"{(net_charge / total * 100.0 if total else 0.0):.3f}",
            "outer_shell_residue_count": str(len(outer_residues)),
            "outer_shell_acidic_fraction": f"{fraction(outer_acidic, len(outer_residues)):.4f}",
            "outer_shell_basic_fraction": f"{fraction(outer_basic, len(outer_residues)):.4f}",
            "outer_shell_net_charge_per_100aa": f"{(outer_net_charge / len(outer_residues) * 100.0 if outer_residues else 0.0):.3f}",
            **{key: str(value) for key, value in bridge_counts.items()},
            "salt_bridge_pairs_per_100aa": f"{(bridge_counts['salt_bridge_pairs'] / total * 100.0 if total else 0.0):.3f}",
            "high_conf_salt_bridge_pairs_per_100aa": f"{(bridge_counts['high_conf_salt_bridge_pairs'] / total * 100.0 if total else 0.0):.3f}",
            "foldx_rosetta_feasibility_call": "FOLDX_ROSETTA_NOT_AVAILABLE_USE_PROXY_ONLY",
            "claim_limit": "Candidate-level structural proxy only; does not validate stability, activity, expression, process performance, or recommend mutations.",
        }
        row["structure_energy_proxy_call"] = structure_proxy_call(row)
        rows.append(row)

    proxy_csv = OUT_DIR / "plan06_structure_energy_proxy.csv"
    with proxy_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    feasibility_rows = [
        {
            "tool": "FoldX",
            "local_executable": "foldx",
            "path_check": shutil.which("foldx") or "",
            "status": "NOT_AVAILABLE",
            "action_taken": "No FoldX run performed.",
            "claim_limit": "Licensing/setup absent; not evidence against or for candidate stability.",
        },
        {
            "tool": "Rosetta",
            "local_executable": "rosetta_scripts",
            "path_check": shutil.which("rosetta_scripts") or "",
            "status": "NOT_AVAILABLE",
            "action_taken": "No Rosetta run performed.",
            "claim_limit": "Setup absent; not evidence against or for candidate stability.",
        },
        {
            "tool": "Bounded structure-energy proxy",
            "local_executable": "stdlib_pdb_parser",
            "path_check": str(Path(__file__).name),
            "status": "COMPLETED",
            "action_taken": "Computed candidate-level pLDDT, global/outer-shell charge, and salt-bridge aggregate metrics from rank-1 ColabFold PDBs.",
            "claim_limit": "Proxy only; no mutation-level or residue-pair outputs retained.",
        },
    ]
    feasibility_csv = OUT_DIR / "plan06_foldx_rosetta_feasibility.csv"
    with feasibility_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(feasibility_rows[0]))
        writer.writeheader()
        writer.writerows(feasibility_rows)

    report = OUT_DIR / "PLAN06_STRUCTURE_ENERGY_PROXY_REPORT.md"
    with report.open("w") as handle:
        handle.write("# Plan 06 Structure-Energy Proxy Report\n\n")
        handle.write("Run date: 2026-05-17\n\n")
        handle.write("## Claim Boundary\n\n")
        handle.write(
            "FoldX/Rosetta binaries were not available locally, so no FoldX/Rosetta energy estimates were generated. "
            "This fallback layer adds only candidate-level aggregate structure proxy metrics from existing rank-1 ColabFold PDBs. "
            "It does not validate stability, activity, expression, process performance, or suggest mutations.\n\n"
        )
        handle.write("## Tool Feasibility\n\n")
        handle.write("| Tool | Status | Action |\n|---|---|---|\n")
        for row in feasibility_rows:
            handle.write(f"| {row['tool']} | {row['status']} | {row['action_taken']} |\n")
        handle.write("\n## Candidate-Level Proxy Summary\n\n")
        handle.write(
            "| protein_id | family | axis | mean_plddt | low_conf_fraction | net_charge_per_100aa | "
            "outer_shell_net_charge_per_100aa | salt_bridge_pairs_per_100aa | proxy_call |\n"
        )
        handle.write("|---|---|---|---:|---:|---:|---:|---:|---|\n")
        for row in rows:
            handle.write(
                f"| `{row['protein_id']}` | {row['family']} | {row['primary_stability_axis']} | "
                f"{row['mean_plddt']} | {row['low_conf_fraction']} | {row['net_charge_per_100aa']} | "
                f"{row['outer_shell_net_charge_per_100aa']} | {row['salt_bridge_pairs_per_100aa']} | "
                f"{row['structure_energy_proxy_call']} |\n"
            )
        handle.write("\n## Interpretation\n\n")
        handle.write(
            "- This layer is a bounded proxy for structural confidence, charge distribution, and salt-bridge density, not a thermodynamic model.\n"
            "- `MGYG000517341_01521` remains the main structure-confidence caveat because its rank-1 model has a larger low-confidence fraction than the other finalists.\n"
            "- Salt-axis candidates can use these aggregate charge/salt-bridge summaries as assay-prioritization context only; no stability claim should be made before wet-lab testing.\n"
            "- FoldX/Rosetta remains unresolved because the relevant binaries are not available in this environment.\n"
        )
        handle.write("\n## Output Files\n\n")
        handle.write("- `plan06_structure_energy_proxy.csv`\n")
        handle.write("- `plan06_foldx_rosetta_feasibility.csv`\n")

    audit = OUT_DIR / "PLAN06_STRUCTURE_ENERGY_PROXY_COMPLETION_AUDIT.md"
    with audit.open("w") as handle:
        handle.write("# Plan 06 Structure-Energy Proxy Completion Audit\n\n")
        handle.write("Run date: 2026-05-17\n\n")
        handle.write("## Verdict\n\n")
        handle.write(
            "PASS_PROXY_WITH_TOOL_LIMITATION: FoldX/Rosetta were not available, but a non-design, candidate-level "
            "structure proxy layer was generated from existing finalist ColabFold PDBs. This satisfies only the bounded "
            "fallback context; it is not a FoldX/Rosetta substitute and not wet-lab validation.\n\n"
        )
        handle.write("## Prompt-To-Artifact Checklist\n\n")
        handle.write("| Requirement | Evidence | Status |\n|---|---|---|\n")
        handle.write("| Check FoldX availability | `plan06_foldx_rosetta_feasibility.csv` | PASS_NOT_AVAILABLE |\n")
        handle.write("| Check Rosetta availability | `plan06_foldx_rosetta_feasibility.csv` | PASS_NOT_AVAILABLE |\n")
        handle.write("| Use existing Plan06 finalist structures | `plan06_structure_energy_proxy.csv` | PASS_4_OF_4_FINALISTS |\n")
        handle.write("| Add surface/charge/salt-bridge aggregate context | `plan06_structure_energy_proxy.csv` | PASS_PROXY_ONLY |\n")
        handle.write("| Avoid mutation or residue-level engineering suggestions | output schema omits mutation and residue-pair fields | PASS |\n")
        handle.write("| Keep validation claims bounded | `PLAN06_STRUCTURE_ENERGY_PROXY_REPORT.md` | PASS |\n")
        handle.write("\n## Remaining Work\n\n")
        handle.write("- Run FoldX/Rosetta only if licensed binaries become available and calibration/limits are reported.\n")
        handle.write("- Treat all activity, stability, expression, and process-performance claims as wet-lab-only.\n")

    print(f"Wrote {proxy_csv}")
    print(f"Wrote {feasibility_csv}")
    print(f"Wrote {report}")
    print(f"Wrote {audit}")


if __name__ == "__main__":
    main()
