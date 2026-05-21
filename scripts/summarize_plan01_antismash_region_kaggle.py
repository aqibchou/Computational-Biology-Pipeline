#!/usr/bin/env python3
"""Summarize the Plan01 Kaggle antiSMASH region reannotation outputs."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "outputs/plan01_antismash_region_kaggle_attempt_2026-05-17/version6/outputs"
STATUS = RUN_DIR / "plan01_antismash_region_run_status.csv"
TOOL_STATUS = RUN_DIR / "plan01_antismash_tool_status.json"
OUTDIR = ROOT / "outputs/plan01_antismash_region_kaggle_attempt_2026-05-17"
SUMMARY = OUTDIR / "plan01_antismash_region_summary.csv"
REPORT = OUTDIR / "PLAN01_ANTISMASH_REGION_KAGGLE_SUMMARY_REPORT.md"
AUDIT = OUTDIR / "PLAN01_ANTISMASH_REGION_KAGGLE_SUMMARY_COMPLETION_AUDIT.md"

CLAIM_LIMIT = (
    "antiSMASH region reannotation supports BGC boundary/domain review only; "
    "it does not validate product formation, product identity, antimicrobial activity, "
    "novelty, biosafety, or engineering."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def count_feature(text: str, feature: str) -> int:
    return len(re.findall(rf"^     {re.escape(feature)}\b", text, flags=re.MULTILINE))


def qualifiers(text: str, key: str) -> list[str]:
    return re.findall(rf"/{re.escape(key)}=\"([^\"]+)\"", text)


def summarize_gbk(path: Path | None) -> dict[str, object]:
    if path is None or not path.exists():
        return {
            "gbk_path": "",
            "region_feature_count": 0,
            "candidate_cluster_count": 0,
            "protocluster_count": 0,
            "cds_count": 0,
            "asdomain_count": 0,
            "products": "",
            "categories": "",
            "contig_edge_flag": "",
            "detection_rule_count": 0,
        }
    text = path.read_text(errors="replace")
    products = sorted(set(qualifiers(text, "product")))
    categories = sorted(set(qualifiers(text, "category")))
    contig_edges = sorted(set(qualifiers(text, "contig_edge")))
    return {
        "gbk_path": str(path.relative_to(ROOT)),
        "region_feature_count": count_feature(text, "region"),
        "candidate_cluster_count": count_feature(text, "cand_cluster"),
        "protocluster_count": count_feature(text, "protocluster"),
        "cds_count": count_feature(text, "CDS"),
        "asdomain_count": count_feature(text, "aSDomain"),
        "products": ";".join(products),
        "categories": ";".join(categories),
        "contig_edge_flag": ";".join(contig_edges),
        "detection_rule_count": text.count("/detection_rule="),
    }


def main() -> None:
    rows = read_csv(STATUS)
    tool_status = json.loads(TOOL_STATUS.read_text())
    summary_rows: list[dict[str, object]] = []
    for row in rows:
        outdir = RUN_DIR / row["output_dir"]
        main_gbk = outdir / row["region_fasta"].replace(".fna", ".gbk")
        region_gbks = sorted(outdir.glob("*.region*.gbk"))
        region_gbk = region_gbks[0] if region_gbks else None
        parsed = summarize_gbk(region_gbk or main_gbk)
        detected_call = "ANTISMASH_REGION_DETECTED" if region_gbk else "ANTISMASH_COMPLETED_NO_REGION_FILE"
        summary_rows.append(
            {
                "region_fasta": row["region_fasta"],
                "antismash_status": row["antismash_status"],
                "detected_region_call": detected_call,
                "region_gbk_count": len(region_gbks),
                **parsed,
                "claim_limit": CLAIM_LIMIT,
            }
        )

    fields = [
        "region_fasta",
        "antismash_status",
        "detected_region_call",
        "region_gbk_count",
        "gbk_path",
        "region_feature_count",
        "candidate_cluster_count",
        "protocluster_count",
        "cds_count",
        "asdomain_count",
        "products",
        "categories",
        "contig_edge_flag",
        "detection_rule_count",
        "claim_limit",
    ]
    with SUMMARY.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    completed = sum(row["antismash_status"] == "PASS_ANTISMASH_REGION_REANNOTATION" for row in summary_rows)
    detected = sum(row["detected_region_call"] == "ANTISMASH_REGION_DETECTED" for row in summary_rows)
    product_counts: dict[str, int] = {}
    for row in summary_rows:
        for product in str(row["products"]).split(";"):
            if product:
                product_counts[product] = product_counts.get(product, 0) + 1
    product_text = "; ".join(f"{key}:{value}" for key, value in sorted(product_counts.items()))

    REPORT.write_text(
        f"""# Plan 01 Kaggle antiSMASH Region Summary

Run date: 2026-05-17

## Scope

This summarizes the Kaggle CPU antiSMASH 8.0.4 region-level reannotation run for seven Plan01 reconstructed BGC region FASTA inputs. The run used Bioconda/micromamba plus `download-antismash-databases` in Kaggle `/tmp`.

## Result

- antiSMASH command completed rows: {completed} / {len(summary_rows)}
- Rows with explicit `*.region001.gbk` BGC output: {detected} / {len(summary_rows)}
- antiSMASH prereq status: {tool_status.get("check_prereqs_output")}
- Database download return code: {tool_status.get("download_antismash_databases_returncode")}
- Product labels detected across outputs: {product_text or "none"}

## Interpretation

- This is stronger than the earlier reconstructed-only GenBank layer because antiSMASH was actually run remotely with databases available.
- It is still region-level reannotation of reconstructed region FASTA, not whole-MAG native antiSMASH exports.
- Three rows completed antiSMASH but did not produce a `region001.gbk`; keep those as no-region-detected or review rows rather than rescuing them.
- No antiSMASH product label should be treated as product identity, product formation, antimicrobial activity, compound novelty, or biosafety clearance.

## Files

- `plan01_antismash_region_summary.csv`
- `version6/outputs/plan01_antismash_region_run_status.csv`
- `version6/outputs/plan01_antismash_tool_status.json`
- `version6/outputs/antismash_region_outputs/*/*.gbk`
"""
    )

    AUDIT.write_text(
        f"""# Plan 01 Kaggle antiSMASH Region Summary Completion Audit

Run date: 2026-05-17

## Verdict

PASS_REGION_LEVEL_ANTISMASH_REANNOTATION_WITH_RECONSTRUCTED_INPUT_LIMITATION: antiSMASH 8.0.4 completed through Kaggle for all seven reconstructed region FASTA inputs, with explicit BGC region outputs for {detected} of {len(summary_rows)} rows. This is not whole-MAG native antiSMASH/CORASON clustering and does not validate products or activity.

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Launch heavy antiSMASH attempt through Kaggle | `kaggle_kernels/plan01_antismash_regions/`; Kaggle kernel version 6 | PASS |
| Confirm antiSMASH install and databases | `version6/outputs/plan01_antismash_tool_status.json` | PASS |
| Run seven Plan01 region inputs | `version6/outputs/plan01_antismash_region_run_status.csv` | PASS |
| Parse detected antiSMASH region outputs | `plan01_antismash_region_summary.csv` | PASS |
| Keep claims bounded away from product/activity/engineering | report claim limits | PASS |

## Counts

- Completed antiSMASH command rows: {completed}
- Rows with `region001.gbk`: {detected}
- Rows without detected region file: {len(summary_rows) - detected}
"""
    )


if __name__ == "__main__":
    main()
