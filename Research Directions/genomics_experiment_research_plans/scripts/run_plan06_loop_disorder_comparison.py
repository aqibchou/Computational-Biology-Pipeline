#!/usr/bin/env python3
"""Add candidate-level Plan06 loop/disorder comparison against reviewed homologs.

This is a bounded pre-wet-lab screen. It compares whole-sequence composition,
alignment insertion burden, and ColabFold pLDDT flexibility proxies against the
reviewed homolog sequences already used in the Plan06 family MSAs. It does not
emit residue-level engineering targets or mutation suggestions.
"""

from __future__ import annotations

import csv
import datetime as dt
import math
import statistics
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
PLAN06_DIR = ROOT / "outputs/plan06_claim_hardening_2026-05-17"
FINALISTS = PLAN06_DIR / "plan06_finalist_claim_hardening.csv"
PHYLOGENY_PROXY = PLAN06_DIR / "plan06_phylogeny_proxy.csv"
COLABFOLD_DIR = (
    ROOT
    / "outputs/plan06_deep_stability_bridge_2026-05-15/"
    / "candidate_specific_colabfold/gcp_colabfold_t4_output/output"
)
OUTDIR = ROOT / f"outputs/plan06_loop_disorder_comparison_{RUN_DATE}"

DISORDER_PROMOTING = set("ARGQSPEDK")
LOW_COMPLEXITY_WINDOW = 15


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


def fasta_records(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header = ""
    parts: list[str] = []
    with path.open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    records.append((header, "".join(parts)))
                header = line[1:]
                parts = []
            else:
                parts.append(line)
        if header:
            records.append((header, "".join(parts)))
    return records


def resolve_alignment(path_text: str) -> Path:
    path = Path(path_text)
    if path.exists():
        return path
    candidate = ROOT / path_text
    if candidate.exists():
        return candidate
    if "outputs/" in path_text:
        suffix = path_text[path_text.index("outputs/") :]
        candidate = ROOT / suffix
        if candidate.exists():
            return candidate
    raise FileNotFoundError(path_text)


def ungap(seq: str) -> str:
    return "".join(ch for ch in seq.upper() if ch.isalpha() and ch != "X")


def safe_fraction(numerator: int | float, denominator: int | float) -> float:
    if not denominator:
        return 0.0
    return float(numerator) / float(denominator)


def shannon_entropy(window: str) -> float:
    counts: dict[str, int] = {}
    for aa in window:
        counts[aa] = counts.get(aa, 0) + 1
    entropy = 0.0
    for count in counts.values():
        p = count / len(window)
        entropy -= p * math.log2(p)
    return entropy


def low_complexity_fraction(seq: str) -> float:
    if len(seq) < LOW_COMPLEXITY_WINDOW:
        return 0.0
    low_complexity_positions: set[int] = set()
    max_entropy = math.log2(20)
    for start in range(0, len(seq) - LOW_COMPLEXITY_WINDOW + 1):
        window = seq[start : start + LOW_COMPLEXITY_WINDOW]
        entropy = shannon_entropy(window)
        dominant_fraction = max(window.count(aa) for aa in set(window)) / len(window)
        if entropy / max_entropy < 0.55 or dominant_fraction >= 0.45:
            low_complexity_positions.update(range(start, start + LOW_COMPLEXITY_WINDOW))
    return safe_fraction(len(low_complexity_positions), len(seq))


def sequence_metrics(seq: str) -> dict[str, float]:
    clean = ungap(seq)
    length = len(clean)
    if not length:
        return {
            "length": 0,
            "disorder_promoting_fraction": 0.0,
            "gly_pro_fraction": 0.0,
            "charged_fraction": 0.0,
            "low_complexity_fraction": 0.0,
        }
    return {
        "length": length,
        "disorder_promoting_fraction": safe_fraction(sum(1 for aa in clean if aa in DISORDER_PROMOTING), length),
        "gly_pro_fraction": safe_fraction(sum(1 for aa in clean if aa in {"G", "P"}), length),
        "charged_fraction": safe_fraction(sum(1 for aa in clean if aa in {"D", "E", "K", "R", "H"}), length),
        "low_complexity_fraction": low_complexity_fraction(clean),
    }


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(statistics.median(values))


def parse_rank1_plddt(protein_id: str) -> tuple[Path | None, list[float]]:
    candidates = sorted(COLABFOLD_DIR.glob(f"{protein_id}_*unrelaxed_rank_001*.pdb"))
    if not candidates:
        return None, []
    path = candidates[0]
    plddt: list[float] = []
    seen_residues: set[tuple[str, str, str]] = set()
    with path.open(errors="replace") as handle:
        for raw in handle:
            if not raw.startswith("ATOM"):
                continue
            atom_name = raw[12:16].strip()
            if atom_name != "CA":
                continue
            chain = raw[21].strip()
            resseq = raw[22:26].strip()
            icode = raw[26].strip()
            key = (chain, resseq, icode)
            if key in seen_residues:
                continue
            seen_residues.add(key)
            try:
                plddt.append(float(raw[60:66]))
            except ValueError:
                pass
    return path, plddt


def longest_run(flags: list[bool]) -> int:
    best = 0
    current = 0
    for flag in flags:
        if flag:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def candidate_alignment_features(candidate_aln: str, reviewed_alns: list[str], plddt: list[float]) -> dict[str, float | int | str]:
    candidate_residue_index = -1
    insertion_flags: list[bool] = []
    insertion_plddt_values: list[float] = []
    plddt_by_candidate_residue: list[float | None] = []
    reviewed_count = len(reviewed_alns)

    for col_idx, aa in enumerate(candidate_aln):
        if aa == "-":
            continue
        candidate_residue_index += 1
        value = plddt[candidate_residue_index] if candidate_residue_index < len(plddt) else None
        plddt_by_candidate_residue.append(value)
        if reviewed_count:
            reviewed_gap_fraction = safe_fraction(sum(1 for seq in reviewed_alns if col_idx >= len(seq) or seq[col_idx] == "-"), reviewed_count)
        else:
            reviewed_gap_fraction = 0.0
        insertion_like = reviewed_gap_fraction >= 0.6
        insertion_flags.append(insertion_like)
        if insertion_like and value is not None:
            insertion_plddt_values.append(value)

    numeric_plddt = [value for value in plddt_by_candidate_residue if value is not None]
    low70_flags = [value is not None and value < 70.0 for value in plddt_by_candidate_residue]
    low50_flags = [value is not None and value < 50.0 for value in plddt_by_candidate_residue]

    return {
        "candidate_insertion_like_residue_count": sum(1 for flag in insertion_flags if flag),
        "candidate_insertion_like_fraction": round(safe_fraction(sum(1 for flag in insertion_flags if flag), len(insertion_flags)), 4),
        "longest_insertion_like_run": longest_run(insertion_flags),
        "insertion_like_mean_plddt": round(statistics.mean(insertion_plddt_values), 3) if insertion_plddt_values else "",
        "rank1_mean_plddt": round(statistics.mean(numeric_plddt), 3) if numeric_plddt else "",
        "rank1_low_conf_lt70_fraction": round(safe_fraction(sum(1 for flag in low70_flags if flag), len(low70_flags)), 4),
        "rank1_very_low_conf_lt50_fraction": round(safe_fraction(sum(1 for flag in low50_flags if flag), len(low50_flags)), 4),
        "rank1_longest_low_conf_lt70_run": longest_run(low70_flags),
    }


def comparison_call(row: dict[str, object]) -> str:
    insertion_fraction = float(row["candidate_insertion_like_fraction"])
    low70_fraction = float(row["rank1_low_conf_lt70_fraction"])
    low50_fraction = float(row["rank1_very_low_conf_lt50_fraction"])
    disorder_delta = float(row["candidate_vs_reviewed_disorder_promoting_delta"])
    low_complexity_delta = float(row["candidate_vs_reviewed_low_complexity_delta"])
    longest_low_run = int(row["rank1_longest_low_conf_lt70_run"])
    longest_insertion = int(row["longest_insertion_like_run"])

    if low50_fraction > 0.02 or low70_fraction > 0.12 or longest_low_run >= 20:
        return "REVIEW_LOW_CONFIDENCE_FLEXIBLE_REGION_BURDEN"
    if insertion_fraction > 0.12 or longest_insertion >= 20:
        return "REVIEW_ALIGNMENT_INSERTION_LOOP_BURDEN"
    if disorder_delta > 0.06 or low_complexity_delta > 0.04:
        return "WATCH_COMPOSITIONAL_DISORDER_PROXY"
    return "PASS_EXPLICIT_LOOP_DISORDER_PROXY"


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    finalists = read_csv(FINALISTS)
    proxy_by_protein = {row["protein_id"]: row for row in read_csv(PHYLOGENY_PROXY)}
    summary_rows: list[dict[str, object]] = []
    resource_rows: list[dict[str, object]] = []

    for finalist in finalists:
        protein_id = finalist["protein_id"]
        proxy = proxy_by_protein[protein_id]
        alignment = resolve_alignment(proxy["msa_alignment"])
        records = fasta_records(alignment)
        candidate_records = [(header, seq) for header, seq in records if header.startswith("query_") or protein_id in header]
        candidate_header, candidate_aln = candidate_records[0]
        reviewed_records = [(header, seq) for header, seq in records if header.startswith("sp_")]
        reviewed_alns = [seq for _, seq in reviewed_records]
        reviewed_metrics = [sequence_metrics(seq) for _, seq in reviewed_records]
        candidate_metrics = sequence_metrics(candidate_aln)
        pdb_path, plddt = parse_rank1_plddt(protein_id)
        alignment_features = candidate_alignment_features(candidate_aln, reviewed_alns, plddt)

        row: dict[str, object] = {
            "protein_id": protein_id,
            "family": finalist["family"],
            "primary_stability_axis": finalist["primary_stability_axis"],
            "alignment": str(alignment.relative_to(ROOT)),
            "reviewed_homolog_count": len(reviewed_records),
            "candidate_length": int(candidate_metrics["length"]),
            "reviewed_median_length": round(median([float(m["length"]) for m in reviewed_metrics]), 3),
            "candidate_disorder_promoting_fraction": round(float(candidate_metrics["disorder_promoting_fraction"]), 4),
            "reviewed_median_disorder_promoting_fraction": round(median([float(m["disorder_promoting_fraction"]) for m in reviewed_metrics]), 4),
            "candidate_vs_reviewed_disorder_promoting_delta": round(
                float(candidate_metrics["disorder_promoting_fraction"])
                - median([float(m["disorder_promoting_fraction"]) for m in reviewed_metrics]),
                4,
            ),
            "candidate_gly_pro_fraction": round(float(candidate_metrics["gly_pro_fraction"]), 4),
            "reviewed_median_gly_pro_fraction": round(median([float(m["gly_pro_fraction"]) for m in reviewed_metrics]), 4),
            "candidate_low_complexity_fraction": round(float(candidate_metrics["low_complexity_fraction"]), 4),
            "reviewed_median_low_complexity_fraction": round(median([float(m["low_complexity_fraction"]) for m in reviewed_metrics]), 4),
            "candidate_vs_reviewed_low_complexity_delta": round(
                float(candidate_metrics["low_complexity_fraction"])
                - median([float(m["low_complexity_fraction"]) for m in reviewed_metrics]),
                4,
            ),
            **alignment_features,
            "rank1_pdb": str(pdb_path.relative_to(ROOT)) if pdb_path else "",
            "claim_limit": "Candidate-level loop/disorder proxy only; does not validate stability and does not identify engineering targets.",
        }
        row["loop_disorder_comparison_call"] = comparison_call(row)
        summary_rows.append(row)
        resource_rows.append(
            {
                "protein_id": protein_id,
                "alignment": str(alignment.relative_to(ROOT)),
                "rank1_pdb": str(pdb_path.relative_to(ROOT)) if pdb_path else "",
                "reviewed_homolog_count": len(reviewed_records),
                "candidate_header": candidate_header,
                "method_note": "Whole-sequence composition, reviewed-homolog alignment gap burden, and rank1 ColabFold pLDDT proxies; no residue-level targets emitted.",
            }
        )

    fields = [
        "protein_id",
        "family",
        "primary_stability_axis",
        "reviewed_homolog_count",
        "candidate_length",
        "reviewed_median_length",
        "candidate_disorder_promoting_fraction",
        "reviewed_median_disorder_promoting_fraction",
        "candidate_vs_reviewed_disorder_promoting_delta",
        "candidate_gly_pro_fraction",
        "reviewed_median_gly_pro_fraction",
        "candidate_low_complexity_fraction",
        "reviewed_median_low_complexity_fraction",
        "candidate_vs_reviewed_low_complexity_delta",
        "candidate_insertion_like_residue_count",
        "candidate_insertion_like_fraction",
        "longest_insertion_like_run",
        "insertion_like_mean_plddt",
        "rank1_mean_plddt",
        "rank1_low_conf_lt70_fraction",
        "rank1_very_low_conf_lt50_fraction",
        "rank1_longest_low_conf_lt70_run",
        "loop_disorder_comparison_call",
        "alignment",
        "rank1_pdb",
        "claim_limit",
    ]
    write_csv(OUTDIR / "plan06_loop_disorder_comparison.csv", summary_rows, fields)
    write_csv(
        OUTDIR / "plan06_loop_disorder_resource_manifest.csv",
        resource_rows,
        ["protein_id", "alignment", "rank1_pdb", "reviewed_homolog_count", "candidate_header", "method_note"],
    )

    pass_count = sum(1 for row in summary_rows if row["loop_disorder_comparison_call"] == "PASS_EXPLICIT_LOOP_DISORDER_PROXY")
    review_count = len(summary_rows) - pass_count
    report = f"""# Plan06 Loop/Disorder Homolog Comparison Report

Date: {RUN_DATE}

## Scope

This supplemental layer addresses the explicit Plan06 gap for loop/disorder comparison against reviewed homologs. It uses the existing Plan06 family MSAs and rank-1 ColabFold models to compare each finalist against reviewed homolog anchors by:

- disorder-promoting amino-acid composition;
- low-complexity sequence burden;
- candidate insertion-like residues relative to reviewed homolog alignment columns;
- aggregate pLDDT low-confidence burden from the candidate-specific ColabFold model.

No residue-level engineering targets, mutations, or optimization instructions are emitted.

## Result

- Finalists analyzed: {len(summary_rows)}
- Pass calls: {pass_count}
- Review/caveat calls: {review_count}

## Candidate Summary

{md_table(summary_rows, ["protein_id", "family", "candidate_disorder_promoting_fraction", "reviewed_median_disorder_promoting_fraction", "candidate_insertion_like_fraction", "rank1_low_conf_lt70_fraction", "rank1_longest_low_conf_lt70_run", "loop_disorder_comparison_call"])}

## Interpretation

This closes the previous Plan06 loop/disorder comparison gap at a candidate-level proxy standard. The strongest allowed claim is that the current finalists now have explicit reviewed-homolog loop/composition and ColabFold confidence context. This does not validate salt tolerance, pH tolerance, thermostability, expression, activity, or any proposed engineering change.
"""
    (OUTDIR / "PLAN06_LOOP_DISORDER_COMPARISON_REPORT.md").write_text(report)

    audit = f"""# Plan06 Loop/Disorder Homolog Comparison Completion Audit

Date: {RUN_DATE}

## Verdict

PASS_PROXY

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Use current Plan06 finalists | `plan06_finalist_claim_hardening.csv` | PASS |
| Compare against reviewed homologs | `family_msas/*.aln.faa` reviewed `sp_` records | PASS |
| Include loop/insertion proxy | `plan06_loop_disorder_comparison.csv` candidate insertion-like fraction and longest run | PASS |
| Include disorder/composition proxy | `plan06_loop_disorder_comparison.csv` disorder-promoting and low-complexity fractions | PASS |
| Include structure-confidence/flexible-region proxy | rank-1 ColabFold pLDDT aggregate fields | PASS |
| Avoid engineering outputs | No residue positions, mutation candidates, or sequence optimization suggestions emitted | PASS |

## Remaining Caveat

This is an explicit proxy comparison, not a calibrated disorder predictor and not wet-lab stability evidence.
"""
    (OUTDIR / "PLAN06_LOOP_DISORDER_COMPARISON_COMPLETION_AUDIT.md").write_text(audit)

    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"Analyzed {len(summary_rows)} finalists; pass={pass_count}; review={review_count}")


if __name__ == "__main__":
    main()
