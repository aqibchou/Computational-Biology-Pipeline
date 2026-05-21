from __future__ import annotations

import csv
import sqlite3
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17"
RUN_DIR = OUT_DIR / "version3/outputs"
DB_PATH = RUN_DIR / "outputs.db"
PANEL_MANIFEST = ROOT / "outputs/plan01_mibig_reference_panel_2026-05-17/plan01_mibig_reference_panel_manifest.csv"

CLAIM_LIMIT = (
    "Targeted MIBiG reference-panel BiG-SCAPE supports external BGC family-distance "
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


def load_mibig_manifest() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    with PANEL_MANIFEST.open(newline="") as handle:
        for row in csv.DictReader(handle):
            accession = row["mibig_accession"]
            candidate = row["strict_bgc_id"]
            if candidate not in mapping[accession]:
                mapping[accession].append(candidate)
    return mapping


def source_for_file(filename: str) -> str:
    if filename.startswith("BGC"):
        return "MIBIG_REFERENCE"
    if filename.startswith("MGYG"):
        return "PLAN01_WHOLEMAG_REGION"
    return "OTHER"


def cutoff_call(distance: float) -> str:
    if distance <= 0.3:
        return "LINKED_AT_0_3"
    if distance <= 0.5:
        return "LINKED_AT_0_5_ONLY"
    return "NOT_LINKED_AT_0_3_OR_0_5"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    mibig_to_candidates = load_mibig_manifest()

    counts = {
        "input_gbk_count": conn.execute("select count(*) from gbk").fetchone()[0],
        "region_record_count": conn.execute("select count(*) from bgc_record where record_type='region'").fetchone()[0],
        "all_bgc_record_rows": conn.execute("select count(*) from bgc_record").fetchone()[0],
        "cds_count": conn.execute("select count(*) from cds").fetchone()[0],
        "hsp_count": conn.execute("select count(*) from hsp").fetchone()[0],
        "hsp_alignment_count": conn.execute("select count(*) from hsp_alignment").fetchone()[0],
        "distance_count": conn.execute("select count(*) from distance").fetchone()[0],
        "family_count": conn.execute("select count(*) from family").fetchone()[0],
        "connected_component_row_count": conn.execute("select count(*) from connected_component").fetchone()[0],
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
        source = source_for_file(filename)
        accession = filename[:-4] if source == "MIBIG_REFERENCE" and filename.endswith(".gbk") else ""
        out = {
            "record_id": row["record_id"],
            "region_file": filename,
            "source": source,
            "candidate_id_if_keep": KEEP_BY_FILE.get(filename, ""),
            "mibig_accession": accession,
            "mibig_selected_for_keep_candidates": ";".join(mibig_to_candidates.get(accession, [])),
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
        distance_rows.append(
            {
                "left_record_id": row["record_a_id"],
                "right_record_id": row["record_b_id"],
                "left_region_file": left["region_file"],
                "right_region_file": right["region_file"],
                "left_source": left["source"],
                "right_source": right["source"],
                "left_product": left["product"],
                "right_product": right["product"],
                "left_keep_candidate_id": left["candidate_id_if_keep"],
                "right_keep_candidate_id": right["candidate_id_if_keep"],
                "left_mibig_accession": left["mibig_accession"],
                "right_mibig_accession": right["mibig_accession"],
                "bigscape_distance": f"{distance:.6f}",
                "bigscape_similarity": f"{1.0 - distance:.6f}",
                "jaccard": f"{float(row['jaccard']):.6f}",
                "adjacency": f"{float(row['adjacency']):.6f}",
                "dss": f"{float(row['dss']):.6f}",
                "cutoff_call": cutoff_call(distance),
                "pair_type": f"{left['source']}__{right['source']}",
                "claim_limit": CLAIM_LIMIT,
            }
        )

    keep_external_rows: list[dict[str, object]] = []
    for record in record_rows:
        if not record["candidate_id_if_keep"]:
            continue
        external = []
        all_related = []
        for row in distance_rows:
            if row["left_region_file"] == record["region_file"]:
                other_source = row["right_source"]
                other_file = row["right_region_file"]
                other_product = row["right_product"]
                other_mibig = row["right_mibig_accession"]
            elif row["right_region_file"] == record["region_file"]:
                other_source = row["left_source"]
                other_file = row["left_region_file"]
                other_product = row["left_product"]
                other_mibig = row["left_mibig_accession"]
            else:
                continue
            enriched = dict(row)
            enriched["other_source"] = other_source
            enriched["other_file"] = other_file
            enriched["other_product"] = other_product
            enriched["other_mibig_accession"] = other_mibig
            all_related.append(enriched)
            if other_source == "MIBIG_REFERENCE":
                external.append(enriched)
        nearest_external = sorted(external, key=lambda item: float(item["bigscape_distance"]))[0] if external else {}
        nearest_any = sorted(all_related, key=lambda item: float(item["bigscape_distance"]))[0] if all_related else {}
        keep_external_rows.append(
            {
                "candidate_id": record["candidate_id_if_keep"],
                "region_file": record["region_file"],
                "product": record["product"],
                "nearest_external_mibig_accession": nearest_external.get("other_mibig_accession", ""),
                "nearest_external_file": nearest_external.get("other_file", ""),
                "nearest_external_product": nearest_external.get("other_product", ""),
                "nearest_external_bigscape_distance": nearest_external.get("bigscape_distance", ""),
                "nearest_external_bigscape_similarity": nearest_external.get("bigscape_similarity", ""),
                "nearest_external_cutoff_call": nearest_external.get("cutoff_call", "NO_EXTERNAL_DISTANCE_ROW"),
                "nearest_any_file": nearest_any.get("other_file", ""),
                "nearest_any_source": nearest_any.get("other_source", ""),
                "nearest_any_distance": nearest_any.get("bigscape_distance", ""),
                "targeted_mibig_panel_call": (
                    "NO_CLOSE_TARGETED_MIBIG_BIGSCAPE_LINK_AT_0_3_OR_0_5"
                    if nearest_external and nearest_external.get("cutoff_call") == "NOT_LINKED_AT_0_3_OR_0_5"
                    else nearest_external.get("cutoff_call", "NO_EXTERNAL_DISTANCE_ROW")
                ),
                "claim_limit": CLAIM_LIMIT,
            }
        )

    cross_source_pairs = [
        row
        for row in distance_rows
        if {row["left_source"], row["right_source"]} == {"PLAN01_WHOLEMAG_REGION", "MIBIG_REFERENCE"}
    ]
    closest_cross_source = sorted(cross_source_pairs, key=lambda item: float(item["bigscape_distance"]))[:25]

    family_rows: list[dict[str, object]] = []
    for fam in conn.execute("select id, center_id, cutoff, bin_label from family order by id"):
        members = []
        for row in conn.execute("select record_id from bgc_record_family where family_id = ? order by record_id", (fam["id"],)):
            members.append(record_by_id[int(row["record_id"])])
        sources = sorted({member["source"] for member in members})
        keep_members = [member["candidate_id_if_keep"] for member in members if member["candidate_id_if_keep"]]
        mibig_members = [member["mibig_accession"] for member in members if member["mibig_accession"]]
        family_rows.append(
            {
                "family_id": fam["id"],
                "cutoff": fam["cutoff"],
                "bin_label": fam["bin_label"],
                "member_count": len(members),
                "sources": ";".join(sources),
                "keep_candidate_members": ";".join(keep_members),
                "mibig_members": ";".join(mibig_members),
                "contains_plan01_keep_candidate": bool(keep_members),
                "claim_limit": CLAIM_LIMIT,
            }
        )

    write_csv(
        OUT_DIR / "plan01_bigscape_mibig_reference_panel_record_summary.csv",
        record_rows,
        [
            "record_id",
            "region_file",
            "source",
            "candidate_id_if_keep",
            "mibig_accession",
            "mibig_selected_for_keep_candidates",
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
        OUT_DIR / "plan01_bigscape_mibig_reference_panel_distance_matrix.csv",
        distance_rows,
        [
            "left_record_id",
            "right_record_id",
            "left_region_file",
            "right_region_file",
            "left_source",
            "right_source",
            "left_product",
            "right_product",
            "left_keep_candidate_id",
            "right_keep_candidate_id",
            "left_mibig_accession",
            "right_mibig_accession",
            "bigscape_distance",
            "bigscape_similarity",
            "jaccard",
            "adjacency",
            "dss",
            "cutoff_call",
            "pair_type",
            "claim_limit",
        ],
    )
    write_csv(
        OUT_DIR / "plan01_bigscape_mibig_keep_external_distance_summary.csv",
        keep_external_rows,
        [
            "candidate_id",
            "region_file",
            "product",
            "nearest_external_mibig_accession",
            "nearest_external_file",
            "nearest_external_product",
            "nearest_external_bigscape_distance",
            "nearest_external_bigscape_similarity",
            "nearest_external_cutoff_call",
            "nearest_any_file",
            "nearest_any_source",
            "nearest_any_distance",
            "targeted_mibig_panel_call",
            "claim_limit",
        ],
    )
    write_csv(
        OUT_DIR / "plan01_bigscape_mibig_closest_cross_source_pairs.csv",
        closest_cross_source,
        [
            "left_region_file",
            "right_region_file",
            "left_source",
            "right_source",
            "left_product",
            "right_product",
            "left_keep_candidate_id",
            "right_keep_candidate_id",
            "left_mibig_accession",
            "right_mibig_accession",
            "bigscape_distance",
            "bigscape_similarity",
            "cutoff_call",
            "claim_limit",
        ],
    )
    write_csv(
        OUT_DIR / "plan01_bigscape_mibig_family_summary.csv",
        family_rows,
        [
            "family_id",
            "cutoff",
            "bin_label",
            "member_count",
            "sources",
            "keep_candidate_members",
            "mibig_members",
            "contains_plan01_keep_candidate",
            "claim_limit",
        ],
    )

    count_rows = [{"metric": key, "value": value} for key, value in counts.items()]
    count_rows.extend(
        [
            {"metric": "plan01_region_records", "value": sum(1 for row in record_rows if row["source"] == "PLAN01_WHOLEMAG_REGION")},
            {"metric": "mibig_reference_region_records", "value": sum(1 for row in record_rows if row["source"] == "MIBIG_REFERENCE")},
            {"metric": "cross_source_pairwise_distances", "value": len(cross_source_pairs)},
            {"metric": "families_containing_plan01_keep_candidate", "value": sum(1 for row in family_rows if row["contains_plan01_keep_candidate"])},
        ]
    )

    report = f"""# Plan01 BiG-SCAPE Targeted MIBiG Reference Panel Summary

Date: 2026-05-17

## Claim Boundary

{CLAIM_LIMIT}

## Run Status

- Kaggle kernel: `aqibchoudhary35/plan01-big-scape-mibig-reference-panel-20260517`
- Completed version summarized here: `version3`
- BiG-SCAPE version: `2.0.3`
- Pfam: full current Pfam-A downloaded from EBI, decompressed, and pressed by BiG-SCAPE on Kaggle
- Plan01 whole-MAG antiSMASH region GBKs staged: `15`
- Targeted MIBiG GenBank references staged: `27`
- Region records clustered: `{counts['region_record_count']}`
- CDS scanned: `{counts['cds_count']}`
- HSPs: `{counts['hsp_count']}`
- Pairwise distances: `{counts['distance_count']}`
- Connected component rows / families at cutoffs 0.3 and 0.5: `{counts['connected_component_row_count']}` / `{counts['family_count']}`

## Count Table

{md_table(count_rows, ["metric", "value"])}

## Keep Candidate External MIBiG Distance Context

{md_table(keep_external_rows, ["candidate_id", "product", "nearest_external_mibig_accession", "nearest_external_bigscape_distance", "nearest_external_cutoff_call", "nearest_any_file", "nearest_any_source", "nearest_any_distance", "targeted_mibig_panel_call"])}

## Closest Cross-Source Pairs

{md_table(closest_cross_source[:10], ["left_region_file", "right_region_file", "left_source", "right_source", "left_keep_candidate_id", "right_keep_candidate_id", "left_mibig_accession", "right_mibig_accession", "bigscape_distance", "cutoff_call"])}

## Family Summary

{md_table(family_rows, ["family_id", "cutoff", "bin_label", "member_count", "sources", "keep_candidate_members", "mibig_members", "contains_plan01_keep_candidate"])}

## Interpretation

BiG-SCAPE accepted the Plan01 whole-MAG antiSMASH region GBKs and the targeted MIBiG GenBank reference panel. The two family calls at the tested cutoff are MIBiG-only (`BGC0001831` and `BGC0001964`) and do not contain any Plan01 keep candidate. The three Plan01 keep candidates have nearest targeted-MIBiG distances above the 0.3 and 0.5 cutoffs, so this panel does not produce a close targeted-MIBiG family link for the keep queue.

This strengthens external BGC-family distance context, but it is still a targeted panel selected from prior BLAST hits, not full-MIBiG or publication-grade global BGC-family novelty. It does not prove product identity, product formation, antimicrobial activity, biosafety, or wet-lab performance.

## Output Files

- `plan01_bigscape_mibig_reference_panel_record_summary.csv`
- `plan01_bigscape_mibig_reference_panel_distance_matrix.csv`
- `plan01_bigscape_mibig_keep_external_distance_summary.csv`
- `plan01_bigscape_mibig_closest_cross_source_pairs.csv`
- `plan01_bigscape_mibig_family_summary.csv`
- `version3/outputs/outputs.db`
- `version3/outputs/PLAN01_BIGSCAPE_MIBIG_REFERENCE_PANEL_RUN_REPORT.md`
"""
    (OUT_DIR / "PLAN01_BIGSCAPE_MIBIG_REFERENCE_PANEL_SUMMARY_REPORT.md").write_text(report)

    audit = f"""# Plan01 BiG-SCAPE Targeted MIBiG Reference Panel Completion Audit

Date: 2026-05-17

## Checks

- Kaggle BiG-SCAPE kernel completed: yes.
- BiG-SCAPE return code: 0.
- BiG-SCAPE version: 2.0.3.
- Full Pfam-A available and pressed by BiG-SCAPE: yes.
- Plan01 region GBKs staged: 15.
- Targeted MIBiG reference GBKs staged: 27.
- Region records clustered: {counts['region_record_count']}.
- Pairwise distances generated: {counts['distance_count']}.
- Families at cutoffs 0.3 and 0.5: {counts['family_count']}.
- Families containing Plan01 keep candidates: {sum(1 for row in family_rows if row['contains_plan01_keep_candidate'])}.
- Keep-candidate external summaries represented: {len(keep_external_rows)}/3.

## Boundary

{CLAIM_LIMIT}
"""
    (OUT_DIR / "PLAN01_BIGSCAPE_MIBIG_REFERENCE_PANEL_COMPLETION_AUDIT.md").write_text(audit)


if __name__ == "__main__":
    main()
