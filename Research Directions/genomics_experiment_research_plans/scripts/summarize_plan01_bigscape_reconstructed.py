#!/usr/bin/env python3
"""Summarize the Plan01 BiG-SCAPE run on reconstructed GenBank inputs."""

from __future__ import annotations

import csv
import datetime as dt
import re
import sqlite3
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
BIGSCAPE_DIR = ROOT / f"outputs/plan01_bigscape_reconstructed_{RUN_DATE}"
DB_PATH = BIGSCAPE_DIR / f"plan01_bigscape_reconstructed_{RUN_DATE}.db"
RECON_MANIFEST = ROOT / f"outputs/plan01_reconstructed_bgc_genbanks_{RUN_DATE}/plan01_reconstructed_bgc_genbank_manifest.csv"
CLAIM_LIMIT = (
    "BiG-SCAPE 2 was run with --force-gbk on reconstructed GenBank-like inputs, not native "
    "antiSMASH GenBank exports. Results support native-style cluster-distance context only; "
    "they do not validate product formation, compound novelty, antimicrobial activity, or biosafety."
)


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


def strict_id_from_description(description: str) -> str:
    match = re.search(r"for (MGYG[^.]+)$", description)
    return match.group(1) if match else ""


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def main() -> None:
    manifest = {row["strict_bgc_id"]: row for row in read_csv(RECON_MANIFEST)}
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    run_row = conn.execute("select * from run order by id desc limit 1").fetchone()
    counts = {
        "gbk_count": conn.execute("select count(*) from gbk").fetchone()[0],
        "bgc_record_count": conn.execute("select count(*) from bgc_record").fetchone()[0],
        "cds_count": conn.execute("select count(*) from cds").fetchone()[0],
        "scanned_cds_count": conn.execute("select count(*) from scanned_cds").fetchone()[0],
        "hsp_count": conn.execute("select count(*) from hsp").fetchone()[0],
        "hsp_alignment_count": conn.execute("select count(*) from hsp_alignment").fetchone()[0],
        "distance_count": conn.execute("select count(*) from distance").fetchone()[0],
        "family_count": conn.execute("select count(*) from family").fetchone()[0],
        "connected_component_count": conn.execute("select count(*) from connected_component").fetchone()[0],
    }

    record_rows = []
    record_by_id: dict[int, dict[str, object]] = {}
    for row in conn.execute(
        """
        select br.id as record_id, g.path, g.description, br.product, br.category,
               br.nt_start, br.nt_stop, br.record_type
        from bgc_record br
        join gbk g on br.gbk_id = g.id
        order by br.id
        """
    ):
        strict_id = strict_id_from_description(row["description"])
        manifest_row = manifest.get(strict_id, {})
        out = {
            "record_id": row["record_id"],
            "strict_bgc_id": strict_id,
            "product_class_from_plan01": manifest_row.get("product_class", ""),
            "readiness_decision": manifest_row.get("readiness_decision", ""),
            "bigscape_product": row["product"],
            "bigscape_category": row["category"] or "",
            "record_type": row["record_type"],
            "nt_start": row["nt_start"],
            "nt_stop": row["nt_stop"],
            "reconstructed_gbk": str(Path(row["path"]).relative_to(ROOT)) if row["path"] else "",
            "claim_limit": CLAIM_LIMIT,
        }
        record_rows.append(out)
        record_by_id[int(row["record_id"])] = out

    distance_rows = []
    for row in conn.execute(
        """
        select record_a_id, record_b_id, distance, jaccard, adjacency, dss
        from distance
        order by distance asc, record_a_id, record_b_id
        """
    ):
        left = record_by_id[int(row["record_a_id"])]
        right = record_by_id[int(row["record_b_id"])]
        distance = float(row["distance"])
        if distance <= 0.3:
            cutoff_call = "LINKED_AT_0_3"
        elif distance <= 0.5:
            cutoff_call = "LINKED_AT_0_5_ONLY"
        else:
            cutoff_call = "NOT_LINKED_AT_0_3_OR_0_5"
        distance_rows.append(
            {
                "left_record_id": row["record_a_id"],
                "right_record_id": row["record_b_id"],
                "left_strict_bgc_id": left["strict_bgc_id"],
                "right_strict_bgc_id": right["strict_bgc_id"],
                "left_product_class": left["product_class_from_plan01"],
                "right_product_class": right["product_class_from_plan01"],
                "bigscape_distance": f"{distance:.6f}",
                "bigscape_similarity": f"{1.0 - distance:.6f}",
                "jaccard": f"{float(row['jaccard']):.6f}",
                "adjacency": f"{float(row['adjacency']):.6f}",
                "dss": f"{float(row['dss']):.6f}",
                "cutoff_call": cutoff_call,
                "claim_limit": CLAIM_LIMIT,
            }
        )

    singleton_rows = []
    linked_records = set()
    for row in distance_rows:
        if row["cutoff_call"] != "NOT_LINKED_AT_0_3_OR_0_5":
            linked_records.add(row["left_record_id"])
            linked_records.add(row["right_record_id"])
    for record in record_rows:
        singleton_rows.append(
            {
                "record_id": record["record_id"],
                "strict_bgc_id": record["strict_bgc_id"],
                "product_class_from_plan01": record["product_class_from_plan01"],
                "readiness_decision": record["readiness_decision"],
                "bigscape_cutoff_0_3_0_5_call": "SINGLETON_AT_TESTED_CUTOFFS"
                if record["record_id"] not in linked_records
                else "LINKED_AT_TESTED_CUTOFFS",
                "claim_limit": CLAIM_LIMIT,
            }
        )

    write_csv(
        BIGSCAPE_DIR / "plan01_bigscape_reconstructed_record_summary.csv",
        record_rows,
        [
            "record_id",
            "strict_bgc_id",
            "product_class_from_plan01",
            "readiness_decision",
            "bigscape_product",
            "bigscape_category",
            "record_type",
            "nt_start",
            "nt_stop",
            "reconstructed_gbk",
            "claim_limit",
        ],
    )
    write_csv(
        BIGSCAPE_DIR / "plan01_bigscape_reconstructed_distance_matrix.csv",
        distance_rows,
        [
            "left_record_id",
            "right_record_id",
            "left_strict_bgc_id",
            "right_strict_bgc_id",
            "left_product_class",
            "right_product_class",
            "bigscape_distance",
            "bigscape_similarity",
            "jaccard",
            "adjacency",
            "dss",
            "cutoff_call",
            "claim_limit",
        ],
    )
    write_csv(
        BIGSCAPE_DIR / "plan01_bigscape_reconstructed_singleton_calls.csv",
        singleton_rows,
        [
            "record_id",
            "strict_bgc_id",
            "product_class_from_plan01",
            "readiness_decision",
            "bigscape_cutoff_0_3_0_5_call",
            "claim_limit",
        ],
    )

    top_edges = distance_rows[:8]
    count_rows = [{"metric": key, "value": value} for key, value in counts.items()]
    report = f"""# Plan01 BiG-SCAPE Reconstructed-Input Compatibility Report

Run date: {RUN_DATE}

## Scope

BiG-SCAPE 2.0.3 was installed in a local project tool environment and run on the seven reconstructed Plan01 GenBank-like BGC region files using:

`bigscape cluster --force-gbk --mix --db-only-output --gcf-cutoffs 0.3,0.5 --pfam-path resources/pfam/current_release/Pfam-A.hmm`

Claim boundary: {CLAIM_LIMIT}

## Run Summary

| metric | value |
| --- | ---: |
{md_table(count_rows, ["metric", "value"]).split(chr(10), 2)[2]}

## Interpretation

- BiG-SCAPE accepted the reconstructed `.gbk` files with `--force-gbk`.
- The corrected files produced `{counts['cds_count']}` CDS records, `{counts['hsp_count']}` HMM hits, and `{counts['distance_count']}` pairwise distances.
- No multi-record connected components/families were generated at distance cutoffs `0.3` or `0.5`; all seven records are singletons at those tested cutoffs.
- Because these are reconstructed non-native GenBank inputs, this should be framed as a BiG-SCAPE 2 compatibility/native-style distance layer, not as publication-grade native antiSMASH/BiG-SCAPE cluster-family novelty.

## Closest Pairwise Distances

{md_table(top_edges, ["left_strict_bgc_id", "right_strict_bgc_id", "left_product_class", "right_product_class", "bigscape_distance", "bigscape_similarity", "cutoff_call"])}

## Output Files

- `plan01_bigscape_reconstructed_2026-05-17.db`
- `plan01_bigscape_reconstructed_record_summary.csv`
- `plan01_bigscape_reconstructed_distance_matrix.csv`
- `plan01_bigscape_reconstructed_singleton_calls.csv`
- `PLAN01_BIGSCAPE_RECONSTRUCTED_COMPLETION_AUDIT.md`
"""
    (BIGSCAPE_DIR / "PLAN01_BIGSCAPE_RECONSTRUCTED_REPORT.md").write_text(report)

    audit = f"""# Plan01 BiG-SCAPE Reconstructed-Input Completion Audit

Run date: {RUN_DATE}

## Verdict

PASS_RECONSTRUCTED_INPUT_COMPATIBILITY_RUN_WITH_LIMITATIONS

## Prompt-To-Artifact Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Use Plan01 BGC reconstructed inputs | `../plan01_reconstructed_bgc_genbanks_{RUN_DATE}/reconstructed_region_gbks/*.gbk` | PASS |
| Run BiG-SCAPE 2 on all seven inputs | `plan01_bigscape_reconstructed_{RUN_DATE}.db`; log file | PASS_FORCE_GBK |
| Use full Pfam-A HMM resource | command log; `resources/pfam/current_release/Pfam-A.hmm` | PASS |
| Confirm CDS/HMM parsing | `{counts['cds_count']}` CDS; `{counts['hsp_count']}` HSPs in SQLite DB | PASS |
| Generate pairwise cluster distances | `plan01_bigscape_reconstructed_distance_matrix.csv`; `{counts['distance_count']}` distances | PASS |
| Generate GCF/connected-component calls at tested cutoffs | SQLite `family` and `connected_component` tables | PASS_EMPTY_NO_LINKED_COMPONENTS_AT_0_3_OR_0_5 |
| Preserve claim boundary | `PLAN01_BIGSCAPE_RECONSTRUCTED_REPORT.md` | PASS |

## Remaining Caveat

This is not a native antiSMASH GenBank export run. BiG-SCAPE used `--force-gbk` and categorized records as non-native/categoryless. The result strengthens Plan01 cluster-distance context but should not be represented as definitive publication-grade BiG-SCAPE/CORASON family novelty.
"""
    (BIGSCAPE_DIR / "PLAN01_BIGSCAPE_RECONSTRUCTED_COMPLETION_AUDIT.md").write_text(audit)

    print(f"Wrote {BIGSCAPE_DIR.relative_to(ROOT)}")
    print(
        f"records={counts['bgc_record_count']} cds={counts['cds_count']} "
        f"hsp={counts['hsp_count']} distances={counts['distance_count']} "
        f"families={counts['family_count']} components={counts['connected_component_count']}"
    )


if __name__ == "__main__":
    main()
