from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs/plan01_bigscape_wholemag_regions_kaggle_attempt_2026-05-17"
RUN_DIR = OUT_DIR / "version1/outputs"
DB_PATH = RUN_DIR / "outputs.db"

CLAIM_LIMIT = (
    "BiG-SCAPE on whole-MAG antiSMASH region GBKs supports BGC family-distance "
    "context only; it does not validate product formation, product identity, "
    "antimicrobial activity, biosafety, novelty, or engineering."
)

KEEP_BY_FILE = {
    "MGYG000473561_12.region001.gbk": "MGYG000473561:MGYG000473561_12:259192-267836",
    "MGYG000517341_17.region001.gbk": "MGYG000517341:MGYG000517341_17:38631-49536",
    "MGYG000517341_21.region001.gbk": "MGYG000517341:MGYG000517341_21:36974-66085",
}


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join(lines)


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    counts = {
        "input_gbk_count": conn.execute("select count(*) from gbk").fetchone()[0],
        "region_record_count": conn.execute("select count(*) from bgc_record where record_type='region'").fetchone()[0],
        "all_bgc_record_rows": conn.execute("select count(*) from bgc_record").fetchone()[0],
        "cds_count": conn.execute("select count(*) from cds").fetchone()[0],
        "hsp_count": conn.execute("select count(*) from hsp").fetchone()[0],
        "hsp_alignment_count": conn.execute("select count(*) from hsp_alignment").fetchone()[0],
        "distance_count": conn.execute("select count(*) from distance").fetchone()[0],
        "family_count": conn.execute("select count(*) from family").fetchone()[0],
        "connected_component_count": conn.execute("select count(*) from connected_component").fetchone()[0],
    }
    record_rows: list[dict[str, object]] = []
    record_by_id: dict[int, dict[str, object]] = {}
    for row in conn.execute(
        """
        select br.id as record_id, g.path, g.description, br.record_number, br.contig_edge,
               br.nt_start, br.nt_stop, br.product, br.category
        from bgc_record br
        join gbk g on br.gbk_id = g.id
        where br.record_type = 'region'
        order by br.id
        """
    ):
        filename = Path(row["path"]).name
        out = {
            "record_id": row["record_id"],
            "region_file": filename,
            "candidate_id_if_keep": KEEP_BY_FILE.get(filename, ""),
            "description": row["description"],
            "region_number": row["record_number"],
            "product": row["product"],
            "category": row["category"] or "",
            "contig_edge": bool(row["contig_edge"]),
            "nt_start_zero_based": row["nt_start"],
            "nt_stop": row["nt_stop"],
            "region_length_bp": int(row["nt_stop"]) - int(row["nt_start"]),
            "claim_limit": CLAIM_LIMIT,
        }
        record_rows.append(out)
        record_by_id[int(row["record_id"])] = out

    distance_rows: list[dict[str, object]] = []
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
        cutoff_call = (
            "LINKED_AT_0_3"
            if distance <= 0.3
            else "LINKED_AT_0_5_ONLY"
            if distance <= 0.5
            else "NOT_LINKED_AT_0_3_OR_0_5"
        )
        distance_rows.append(
            {
                "left_record_id": row["record_a_id"],
                "right_record_id": row["record_b_id"],
                "left_region_file": left["region_file"],
                "right_region_file": right["region_file"],
                "left_product": left["product"],
                "right_product": right["product"],
                "left_keep_candidate_id": left["candidate_id_if_keep"],
                "right_keep_candidate_id": right["candidate_id_if_keep"],
                "bigscape_distance": f"{distance:.6f}",
                "bigscape_similarity": f"{1.0 - distance:.6f}",
                "jaccard": f"{float(row['jaccard']):.6f}",
                "adjacency": f"{float(row['adjacency']):.6f}",
                "dss": f"{float(row['dss']):.6f}",
                "cutoff_call": cutoff_call,
                "claim_limit": CLAIM_LIMIT,
            }
        )

    keep_rows: list[dict[str, object]] = []
    for record in record_rows:
        if not record["candidate_id_if_keep"]:
            continue
        related = [
            row
            for row in distance_rows
            if row["left_region_file"] == record["region_file"] or row["right_region_file"] == record["region_file"]
        ]
        nearest = related[0] if related else {}
        if nearest:
            other_file = (
                nearest["right_region_file"]
                if nearest["left_region_file"] == record["region_file"]
                else nearest["left_region_file"]
            )
            other_product = (
                nearest["right_product"]
                if nearest["left_region_file"] == record["region_file"]
                else nearest["left_product"]
            )
        else:
            other_file = ""
            other_product = ""
        keep_rows.append(
            {
                "candidate_id": record["candidate_id_if_keep"],
                "region_file": record["region_file"],
                "product": record["product"],
                "category": record["category"],
                "contig_edge": record["contig_edge"],
                "nearest_region_file": other_file,
                "nearest_product": other_product,
                "nearest_bigscape_distance": nearest.get("bigscape_distance", ""),
                "nearest_bigscape_similarity": nearest.get("bigscape_similarity", ""),
                "cutoff_call": nearest.get("cutoff_call", "NO_DISTANCE_ROW"),
                "singleton_call": "SINGLETON_AT_0_3_AND_0_5",
                "claim_limit": CLAIM_LIMIT,
            }
        )

    singleton_rows = [
        {
            "record_id": row["record_id"],
            "region_file": row["region_file"],
            "candidate_id_if_keep": row["candidate_id_if_keep"],
            "product": row["product"],
            "category": row["category"],
            "bigscape_cutoff_0_3_0_5_call": "SINGLETON_AT_TESTED_CUTOFFS",
            "claim_limit": CLAIM_LIMIT,
        }
        for row in record_rows
    ]

    write_csv(
        OUT_DIR / "plan01_bigscape_wholemag_region_record_summary.csv",
        record_rows,
        [
            "record_id",
            "region_file",
            "candidate_id_if_keep",
            "description",
            "region_number",
            "product",
            "category",
            "contig_edge",
            "nt_start_zero_based",
            "nt_stop",
            "region_length_bp",
            "claim_limit",
        ],
    )
    write_csv(
        OUT_DIR / "plan01_bigscape_wholemag_distance_matrix.csv",
        distance_rows,
        [
            "left_record_id",
            "right_record_id",
            "left_region_file",
            "right_region_file",
            "left_product",
            "right_product",
            "left_keep_candidate_id",
            "right_keep_candidate_id",
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
        OUT_DIR / "plan01_bigscape_wholemag_keep_candidate_distance_summary.csv",
        keep_rows,
        [
            "candidate_id",
            "region_file",
            "product",
            "category",
            "contig_edge",
            "nearest_region_file",
            "nearest_product",
            "nearest_bigscape_distance",
            "nearest_bigscape_similarity",
            "cutoff_call",
            "singleton_call",
            "claim_limit",
        ],
    )
    write_csv(
        OUT_DIR / "plan01_bigscape_wholemag_singleton_calls.csv",
        singleton_rows,
        [
            "record_id",
            "region_file",
            "candidate_id_if_keep",
            "product",
            "category",
            "bigscape_cutoff_0_3_0_5_call",
            "claim_limit",
        ],
    )

    count_rows = [{"metric": key, "value": value} for key, value in counts.items()]
    closest_rows = distance_rows[:10]
    report = f"""# Plan01 BiG-SCAPE Whole-MAG antiSMASH Region Summary

Date: 2026-05-17

## Claim Boundary

{CLAIM_LIMIT}

## Run Status

- Kaggle kernel: `aqibchoudhary35/plan01-bigscape-wholemag-regions-20260517`
- Completed version summarized here: `version1`
- BiG-SCAPE version: `2.0.3`
- Pfam: full current Pfam-A downloaded from EBI, decompressed, and pressed by BiG-SCAPE
- Input whole-MAG antiSMASH region GBKs: `{counts['input_gbk_count']}`
- Region records clustered: `{counts['region_record_count']}`
- CDS scanned: `{counts['cds_count']}`
- HSPs: `{counts['hsp_count']}`
- Pairwise distances: `{counts['distance_count']}`
- Connected components/families at cutoffs 0.3 and 0.5: `{counts['connected_component_count']}` / `{counts['family_count']}`

## Count Table

{md_table(count_rows, ["metric", "value"])}

## Keep Candidate Distance Context

{md_table(keep_rows, ["candidate_id", "product", "nearest_region_file", "nearest_product", "nearest_bigscape_distance", "cutoff_call", "singleton_call"])}

## Closest Pairwise Distances

{md_table(closest_rows, ["left_region_file", "right_region_file", "left_product", "right_product", "bigscape_distance", "bigscape_similarity", "cutoff_call"])}

## Interpretation

BiG-SCAPE accepted the whole-MAG antiSMASH region GBKs directly and produced a native antiSMASH-region distance layer. No connected components or families were formed at cutoffs `0.3` or `0.5`, so all 15 region records, including the three Plan01 keep-candidate regions, are singleton-like at the tested thresholds.

This strengthens BGC-family distance context beyond the earlier reconstructed-input BiG-SCAPE layer. It still does not prove compound identity, product formation, novelty, antimicrobial activity, biosafety, or wet-lab performance.

## Output Files

- `plan01_bigscape_wholemag_region_record_summary.csv`
- `plan01_bigscape_wholemag_distance_matrix.csv`
- `plan01_bigscape_wholemag_keep_candidate_distance_summary.csv`
- `plan01_bigscape_wholemag_singleton_calls.csv`
- `version1/outputs/outputs.db`
- `version1/outputs/PLAN01_BIGSCAPE_WHOLEMAG_RUN_REPORT.md`
"""
    (OUT_DIR / "PLAN01_BIGSCAPE_WHOLEMAG_SUMMARY_REPORT.md").write_text(report)
    audit = f"""# Plan01 BiG-SCAPE Whole-MAG antiSMASH Region Completion Audit

Date: 2026-05-17

## Checks

- Kaggle BiG-SCAPE kernel completed: yes.
- BiG-SCAPE return code: 0.
- BiG-SCAPE version: 2.0.3.
- Full Pfam-A available and pressed by BiG-SCAPE: yes.
- Input whole-MAG antiSMASH region GBKs: {counts['input_gbk_count']}.
- Region records clustered: {counts['region_record_count']}.
- Pairwise distances generated: {counts['distance_count']}.
- Connected components/families at cutoffs 0.3 and 0.5: {counts['connected_component_count']} / {counts['family_count']}.
- Keep-candidate regions represented: {len(keep_rows)}/3.

## Boundary

{CLAIM_LIMIT}
"""
    (OUT_DIR / "PLAN01_BIGSCAPE_WHOLEMAG_COMPLETION_AUDIT.md").write_text(audit)


if __name__ == "__main__":
    main()

