#!/usr/bin/env python3
"""Integrate Plan01 COCONUT lookups with the product-class derep matrix."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_MATRIX = ROOT / "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/plan01_product_class_lookup_matrix.csv"
COCONUT_LOOKUP = ROOT / "outputs/plan01_coconut_product_lookup_2026-05-17/plan01_coconut_product_lookup.csv"
OUTDIR = ROOT / "outputs/plan01_product_class_integrated_lookup_2026-05-17"
INTEGRATED_MATRIX = OUTDIR / "plan01_product_class_integrated_lookup_matrix.csv"
SUMMARY = OUTDIR / "plan01_product_class_integrated_summary.csv"
REPORT = OUTDIR / "PLAN01_PRODUCT_CLASS_INTEGRATED_LOOKUP_REPORT.md"
AUDIT = OUTDIR / "PLAN01_PRODUCT_CLASS_INTEGRATED_LOOKUP_COMPLETION_AUDIT.md"

CLAIM_LIMIT = (
    "Integrated product-class lookup supports dereplication awareness only; "
    "it does not prove candidate product identity, compound novelty, product formation, "
    "antimicrobial activity, or biosafety."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base_rows = read_csv(BASE_MATRIX)
    coconut_rows = read_csv(COCONUT_LOOKUP)
    coconut_by_key = {
        (row["strict_bgc_id"], row["lookup_term"], row["source"]): row
        for row in coconut_rows
    }

    integrated_rows: list[dict[str, object]] = []
    unmatched_coconut_rows = 0

    for row in base_rows:
        out = dict(row)
        out["integration_status"] = "BASE_MATRIX_RETAINED"
        out["api_url"] = ""
        out["http_status"] = ""
        out["top_result_identifiers"] = ""
        out["top_result_names"] = ""
        out["cache_file"] = ""
        if row["source"] == "coconut":
            hit = coconut_by_key.get((row["strict_bgc_id"], row["lookup_term"], row["source"]))
            if hit:
                out["lookup_status"] = hit["lookup_status"]
                out["hit_count"] = hit["hit_count"]
                out["note"] = (
                    f"{hit['query_status']}; top results: {hit['top_result_names'] or 'none'}"
                )
                out["claim_limit"] = CLAIM_LIMIT
                out["integration_status"] = "COCONUT_API_LOOKUP_INTEGRATED"
                out["api_url"] = hit["api_url"]
                out["http_status"] = hit["http_status"]
                out["top_result_identifiers"] = hit["top_result_identifiers"]
                out["top_result_names"] = hit["top_result_names"]
                out["cache_file"] = hit["cache_file"]
            else:
                unmatched_coconut_rows += 1
                out["integration_status"] = "COCONUT_ROW_UNMATCHED_RETAINS_BASE_STATUS"
                out["claim_limit"] = CLAIM_LIMIT
        integrated_rows.append(out)

    matrix_fields = [
        "strict_bgc_id",
        "product_class",
        "lookup_term",
        "source",
        "lookup_status",
        "hit_count",
        "note",
        "api_url",
        "http_status",
        "top_result_identifiers",
        "top_result_names",
        "cache_file",
        "integration_status",
        "claim_limit",
    ]
    write_csv(INTEGRATED_MATRIX, integrated_rows, matrix_fields)

    by_bgc: dict[str, Counter[str]] = defaultdict(Counter)
    hit_terms: dict[str, list[str]] = defaultdict(list)
    for row in integrated_rows:
        bgc = str(row["strict_bgc_id"])
        status = str(row["lookup_status"])
        source = str(row["source"])
        by_bgc[bgc]["total_rows"] += 1
        by_bgc[bgc][f"{source}_rows"] += 1
        if int(str(row["hit_count"]) or 0) > 0:
            by_bgc[bgc]["rows_with_hits"] += 1
            by_bgc[bgc][f"{source}_hit_rows"] += 1
            hit_terms[bgc].append(f"{source}:{row['lookup_term']}:{row['hit_count']}")
        if status.startswith("COCONUT_API"):
            by_bgc[bgc]["coconut_integrated_rows"] += 1

    summary_rows: list[dict[str, object]] = []
    for bgc, counts in sorted(by_bgc.items()):
        summary_rows.append(
            {
                "strict_bgc_id": bgc,
                "total_lookup_rows": counts["total_rows"],
                "rows_with_hits": counts["rows_with_hits"],
                "coconut_integrated_rows": counts["coconut_integrated_rows"],
                "npatlas_hit_rows": counts["npatlas_hit_rows"],
                "pubchem_hit_rows": counts["pubchem_hit_rows"],
                "chembl_hit_rows": counts["chembl_hit_rows"],
                "coconut_hit_rows": counts["coconut_hit_rows"],
                "hit_terms": "; ".join(hit_terms[bgc][:12]),
                "claim_limit": CLAIM_LIMIT,
            }
        )
    write_csv(
        SUMMARY,
        summary_rows,
        [
            "strict_bgc_id",
            "total_lookup_rows",
            "rows_with_hits",
            "coconut_integrated_rows",
            "npatlas_hit_rows",
            "pubchem_hit_rows",
            "chembl_hit_rows",
            "coconut_hit_rows",
            "hit_terms",
            "claim_limit",
        ],
    )

    total_hits = sum(int(row["rows_with_hits"]) for row in summary_rows)
    coconut_integrated = sum(int(row["coconut_integrated_rows"]) for row in summary_rows)
    coconut_hit_rows = sum(int(row["coconut_hit_rows"]) for row in summary_rows)

    report = f"""# Plan 01 Integrated Product-Class Lookup Report

Run date: 2026-05-17

## Scope

This supplemental layer integrates the completed COCONUT API text-search lookups into the older Plan01 NPAtlas/PubChem/ChEMBL product-class dereplication matrix. It is a database-awareness and analog/class-review layer only.

## Results

- Base product-class rows integrated: {len(base_rows)}
- COCONUT API rows available: {len(coconut_rows)}
- COCONUT rows integrated into the matrix: {coconut_integrated}
- COCONUT rows with one or more text-search hits: {coconut_hit_rows}
- Candidate summary rows written: {len(summary_rows)}
- Total source-term rows with one or more hits across all sources: {total_hits}
- Unmatched base COCONUT rows: {unmatched_coconut_rows}

## Interpretation

- COCONUT results now sit in the same product-class matrix as NPAtlas, PubChem, and ChEMBL cache results.
- Hits for known analog names strengthen dereplication awareness.
- Hits for broad class names are weak evidence and may retrieve unrelated natural products.
- No hit should be treated as candidate product identity, product novelty, antimicrobial activity, or biosafety clearance.

## Files

- `plan01_product_class_integrated_lookup_matrix.csv`
- `plan01_product_class_integrated_summary.csv`
- `PLAN01_PRODUCT_CLASS_INTEGRATED_LOOKUP_COMPLETION_AUDIT.md`
"""
    REPORT.write_text(report)

    audit = f"""# Plan 01 Integrated Product-Class Lookup Completion Audit

Run date: 2026-05-17

## Verdict

PASS_INTEGRATED_PRODUCT_CLASS_DEREP_AWARENESS_WITH_TEXT_SEARCH_LIMITATION: the completed COCONUT API text-search layer is now integrated with the existing NPAtlas/PubChem/ChEMBL product-class matrix. This remains class/query-level dereplication awareness, not product identity or novelty validation.

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Read existing Plan01 product-class matrix | `{BASE_MATRIX.relative_to(ROOT)}` | PASS |
| Read completed COCONUT API lookup table | `{COCONUT_LOOKUP.relative_to(ROOT)}` | PASS |
| Replace stale COCONUT no-cache rows where API evidence exists | `{INTEGRATED_MATRIX.relative_to(ROOT)}` | PASS |
| Write candidate-level integrated summary | `{SUMMARY.relative_to(ROOT)}` | PASS |
| Preserve product-identity and novelty claim boundary | report claim limits | PASS |

## Counts

- Integrated matrix rows: {len(integrated_rows)}
- Candidate summary rows: {len(summary_rows)}
- COCONUT integrated rows: {coconut_integrated}
- COCONUT hit rows: {coconut_hit_rows}
- Unmatched base COCONUT rows: {unmatched_coconut_rows}
"""
    AUDIT.write_text(audit)


if __name__ == "__main__":
    main()
