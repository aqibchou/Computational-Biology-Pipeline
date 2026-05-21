from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17"

CLAIM_LIMIT = (
    "Full-MIBiG BiG-SCAPE supports external BGC family-distance context only; "
    "it does not validate product formation, product identity, antimicrobial "
    "activity, biosafety, novelty, synthesis, transfer, or engineering."
)

KEEP_BY_FILE = {
    "MGYG000473561_12.region001.gbk": "MGYG000473561:MGYG000473561_12:259192-267836",
    "MGYG000517341_17.region001.gbk": "MGYG000517341:MGYG000517341_17:38631-49536",
    "MGYG000517341_21.region001.gbk": "MGYG000517341:MGYG000517341_21:36974-66085",
}


def latest_run_dir() -> Path:
    candidates = sorted(OUT_DIR.glob("version*/outputs/outputs.db"))
    if not candidates:
        raise FileNotFoundError(f"No pulled full-MIBiG outputs.db found under {OUT_DIR}")
    return candidates[-1].parent


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


def source_for_file(filename: str) -> str:
    if filename.startswith("BGC"):
        return "MIBIG_FULL_REFERENCE"
    if filename.startswith("MGYG"):
        return "PLAN01_WHOLEMAG_REGION"
    return "OTHER"


def cutoff_call(distance: float) -> str:
    if distance <= 0.3:
        return "LINKED_AT_0_3"
    if distance <= 0.5:
        return "LINKED_AT_0_5_ONLY"
    return "NOT_LINKED_AT_0_3_OR_0_5"


def distance_row(conn: sqlite3.Connection, record_id: int) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            """
            select record_a_id, record_b_id, distance, jaccard, adjacency, dss
            from distance
            where record_a_id = ? or record_b_id = ?
            order by distance asc
            limit 250
            """,
            (record_id, record_id),
        )
    )


def main() -> None:
    run_dir = latest_run_dir()
    db_path = run_dir / "outputs.db"
    status_path = run_dir / "plan01_bigscape_full_mibig_status.json"
    discovery_path = run_dir / "plan01_bigscape_full_mibig_input_discovery.json"
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    discovery = json.loads(discovery_path.read_text()) if discovery_path.exists() else {}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
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
            accession = filename[:-4] if source == "MIBIG_FULL_REFERENCE" and filename.endswith(".gbk") else ""
            out = {
                "record_id": row["record_id"],
                "region_file": filename,
                "source": source,
                "candidate_id_if_keep": KEEP_BY_FILE.get(filename, ""),
                "mibig_accession": accession,
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

        keep_records = [row for row in record_rows if row["candidate_id_if_keep"]]
        plan01_ids = {int(row["record_id"]) for row in record_rows if row["source"] == "PLAN01_WHOLEMAG_REGION"}
        mibig_ids = {int(row["record_id"]) for row in record_rows if row["source"] == "MIBIG_FULL_REFERENCE"}

        keep_external_rows: list[dict[str, object]] = []
        for keep in keep_records:
            nearest_external: dict[str, object] | None = None
            nearest_any: dict[str, object] | None = None
            for row in distance_row(conn, int(keep["record_id"])):
                other_id = int(row["record_b_id"]) if int(row["record_a_id"]) == int(keep["record_id"]) else int(row["record_a_id"])
                other = record_by_id.get(other_id)
                if not other:
                    continue
                distance = float(row["distance"])
                candidate = {
                    "candidate_id": keep["candidate_id_if_keep"],
                    "region_file": keep["region_file"],
                    "product": keep["product"],
                    "other_record_id": other_id,
                    "other_file": other["region_file"],
                    "other_source": other["source"],
                    "other_product": other["product"],
                    "other_mibig_accession": other["mibig_accession"],
                    "bigscape_distance": f"{distance:.6f}",
                    "bigscape_similarity": f"{1.0 - distance:.6f}",
                    "jaccard": f"{float(row['jaccard']):.6f}",
                    "adjacency": f"{float(row['adjacency']):.6f}",
                    "dss": f"{float(row['dss']):.6f}",
                    "cutoff_call": cutoff_call(distance),
                    "claim_limit": CLAIM_LIMIT,
                }
                if nearest_any is None:
                    nearest_any = candidate
                if other["source"] == "MIBIG_FULL_REFERENCE" and nearest_external is None:
                    nearest_external = candidate
            external = nearest_external or {}
            any_hit = nearest_any or {}
            keep_external_rows.append(
                {
                    "candidate_id": keep["candidate_id_if_keep"],
                    "region_file": keep["region_file"],
                    "product": keep["product"],
                    "nearest_external_mibig_accession": external.get("other_mibig_accession", ""),
                    "nearest_external_file": external.get("other_file", ""),
                    "nearest_external_product": external.get("other_product", ""),
                    "nearest_external_bigscape_distance": external.get("bigscape_distance", ""),
                    "nearest_external_bigscape_similarity": external.get("bigscape_similarity", ""),
                    "nearest_external_cutoff_call": external.get("cutoff_call", "NO_EXTERNAL_DISTANCE_ROW"),
                    "nearest_any_file": any_hit.get("other_file", ""),
                    "nearest_any_source": any_hit.get("other_source", ""),
                    "nearest_any_distance": any_hit.get("bigscape_distance", ""),
                    "full_mibig_call": (
                        "NO_CLOSE_FULL_MIBIG_BIGSCAPE_LINK_AT_0_3_OR_0_5"
                        if external and external.get("cutoff_call") == "NOT_LINKED_AT_0_3_OR_0_5"
                        else external.get("cutoff_call", "NO_EXTERNAL_DISTANCE_ROW")
                    ),
                    "claim_limit": CLAIM_LIMIT,
                }
            )

        closest_cross_source: list[dict[str, object]] = []
        if plan01_ids and mibig_ids:
            placeholders_plan01 = ",".join("?" for _ in plan01_ids)
            placeholders_mibig = ",".join("?" for _ in mibig_ids)
            query = f"""
                select record_a_id, record_b_id, distance, jaccard, adjacency, dss
                from distance
                where (
                    record_a_id in ({placeholders_plan01}) and record_b_id in ({placeholders_mibig})
                ) or (
                    record_a_id in ({placeholders_mibig}) and record_b_id in ({placeholders_plan01})
                )
                order by distance asc
                limit 100
            """
            params = list(plan01_ids) + list(mibig_ids) + list(mibig_ids) + list(plan01_ids)
            for row in conn.execute(query, params):
                left = record_by_id[int(row["record_a_id"])]
                right = record_by_id[int(row["record_b_id"])]
                distance = float(row["distance"])
                closest_cross_source.append(
                    {
                        "left_region_file": left["region_file"],
                        "right_region_file": right["region_file"],
                        "left_source": left["source"],
                        "right_source": right["source"],
                        "left_keep_candidate_id": left["candidate_id_if_keep"],
                        "right_keep_candidate_id": right["candidate_id_if_keep"],
                        "left_mibig_accession": left["mibig_accession"],
                        "right_mibig_accession": right["mibig_accession"],
                        "left_product": left["product"],
                        "right_product": right["product"],
                        "bigscape_distance": f"{distance:.6f}",
                        "bigscape_similarity": f"{1.0 - distance:.6f}",
                        "cutoff_call": cutoff_call(distance),
                        "claim_limit": CLAIM_LIMIT,
                    }
                )

        family_rows: list[dict[str, object]] = []
        for fam in conn.execute("select id, center_id, cutoff, bin_label from family order by id"):
            members = []
            for row in conn.execute("select record_id from bgc_record_family where family_id = ? order by record_id", (fam["id"],)):
                member = record_by_id.get(int(row["record_id"]))
                if member:
                    members.append(member)
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
                    "mibig_member_count": len(mibig_members),
                    "first_mibig_members": ";".join(mibig_members[:25]),
                    "contains_plan01_keep_candidate": bool(keep_members),
                    "contains_cross_source_members": "PLAN01_WHOLEMAG_REGION" in sources and "MIBIG_FULL_REFERENCE" in sources,
                    "claim_limit": CLAIM_LIMIT,
                }
            )

        count_rows = [{"metric": key, "value": value} for key, value in counts.items()]
        count_rows.extend(
            [
                {"metric": "plan01_region_records", "value": sum(1 for row in record_rows if row["source"] == "PLAN01_WHOLEMAG_REGION")},
                {"metric": "mibig_reference_region_records", "value": sum(1 for row in record_rows if row["source"] == "MIBIG_FULL_REFERENCE")},
                {"metric": "families_containing_plan01_keep_candidate", "value": sum(1 for row in family_rows if row["contains_plan01_keep_candidate"])},
                {"metric": "cross_source_families", "value": sum(1 for row in family_rows if row["contains_cross_source_members"])},
                {"metric": "keep_candidate_external_summaries", "value": len(keep_external_rows)},
            ]
        )

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        write_csv(
            OUT_DIR / "plan01_bigscape_full_mibig_record_summary.csv",
            record_rows,
            [
                "record_id",
                "region_file",
                "source",
                "candidate_id_if_keep",
                "mibig_accession",
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
            OUT_DIR / "plan01_bigscape_full_mibig_keep_external_distance_summary.csv",
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
                "full_mibig_call",
                "claim_limit",
            ],
        )
        write_csv(
            OUT_DIR / "plan01_bigscape_full_mibig_closest_cross_source_pairs.csv",
            closest_cross_source,
            [
                "left_region_file",
                "right_region_file",
                "left_source",
                "right_source",
                "left_keep_candidate_id",
                "right_keep_candidate_id",
                "left_mibig_accession",
                "right_mibig_accession",
                "left_product",
                "right_product",
                "bigscape_distance",
                "bigscape_similarity",
                "cutoff_call",
                "claim_limit",
            ],
        )
        write_csv(
            OUT_DIR / "plan01_bigscape_full_mibig_family_summary.csv",
            family_rows,
            [
                "family_id",
                "cutoff",
                "bin_label",
                "member_count",
                "sources",
                "keep_candidate_members",
                "mibig_member_count",
                "first_mibig_members",
                "contains_plan01_keep_candidate",
                "contains_cross_source_members",
                "claim_limit",
            ],
        )

        run_status = status.get("command", {})
        report = f"""# Plan01 BiG-SCAPE Full-MIBiG Summary

Date: 2026-05-17

## Claim Boundary

{CLAIM_LIMIT}

## Run Status

- Kaggle kernel: `aqibchoudhary35/plan01-big-scape-full-mibig-20260517`
- Pulled output directory summarized: `{run_dir.relative_to(ROOT)}`
- BiG-SCAPE status: `{run_status.get('bigscape_status', '')}`
- BiG-SCAPE return code: `{run_status.get('returncode', '')}`
- BiG-SCAPE version output: `{run_status.get('bigscape_version_output', '')}`
- Full Pfam-A available on Kaggle: `{run_status.get('pfam_hmm_exists', '')}`
- MIBiG archive MD5 passed: `{discovery.get('mibig', {}).get('archive_md5_pass', run_status.get('mibig_archive_md5_pass', ''))}`
- Plan01 whole-MAG antiSMASH region GBKs staged: `{discovery.get('plan01_region_gbks', run_status.get('plan01_region_gbks', ''))}`
- MIBiG 4.0 GBKs staged: `{discovery.get('mibig_reference_gbks', run_status.get('mibig_reference_gbks', ''))}`

## Count Table

{md_table(count_rows, ["metric", "value"])}

## Keep Candidate Full-MIBiG Distance Context

{md_table(keep_external_rows, ["candidate_id", "product", "nearest_external_mibig_accession", "nearest_external_bigscape_distance", "nearest_external_cutoff_call", "nearest_any_file", "nearest_any_source", "nearest_any_distance", "full_mibig_call"])}

## Closest Cross-Source Pairs

{md_table(closest_cross_source[:20], ["left_region_file", "right_region_file", "left_source", "right_source", "left_keep_candidate_id", "right_keep_candidate_id", "left_mibig_accession", "right_mibig_accession", "bigscape_distance", "cutoff_call"])}

## Families Containing Plan01 Keep Candidates

{md_table([row for row in family_rows if row["contains_plan01_keep_candidate"]], ["family_id", "cutoff", "bin_label", "member_count", "sources", "keep_candidate_members", "mibig_member_count", "first_mibig_members", "contains_cross_source_members"])}

## Interpretation

This full-MIBiG layer is the publication-grade external reference expansion that the targeted-panel audit left open. Interpret it only as BGC-family distance and family-link context against the MIBiG 4.0 GenBank archive plus Plan01 whole-MAG antiSMASH regions. It does not establish product identity, product formation, antimicrobial activity, biosafety, or validated novelty.

## Output Files

- `plan01_bigscape_full_mibig_record_summary.csv`
- `plan01_bigscape_full_mibig_keep_external_distance_summary.csv`
- `plan01_bigscape_full_mibig_closest_cross_source_pairs.csv`
- `plan01_bigscape_full_mibig_family_summary.csv`
- `{run_dir.relative_to(ROOT)}/outputs.db`
- `{run_dir.relative_to(ROOT)}/PLAN01_BIGSCAPE_FULL_MIBIG_RUN_REPORT.md`
"""
        (OUT_DIR / "PLAN01_BIGSCAPE_FULL_MIBIG_SUMMARY_REPORT.md").write_text(report)

        audit = f"""# Plan01 BiG-SCAPE Full-MIBiG Completion Audit

Date: 2026-05-17

## Checks

- Kaggle BiG-SCAPE kernel status: `{run_status.get('bigscape_status', '')}`.
- BiG-SCAPE return code: `{run_status.get('returncode', '')}`.
- Full Pfam-A available on Kaggle: `{run_status.get('pfam_hmm_exists', '')}`.
- Plan01 region GBKs staged: `{discovery.get('plan01_region_gbks', run_status.get('plan01_region_gbks', ''))}`.
- MIBiG reference GBKs staged: `{discovery.get('mibig_reference_gbks', run_status.get('mibig_reference_gbks', ''))}`.
- Region records clustered: `{counts['region_record_count']}`.
- Pairwise distances generated: `{counts['distance_count']}`.
- Families at cutoffs 0.3 and 0.5: `{counts['family_count']}`.
- Families containing Plan01 keep candidates: `{sum(1 for row in family_rows if row['contains_plan01_keep_candidate'])}`.
- Cross-source families: `{sum(1 for row in family_rows if row['contains_cross_source_members'])}`.
- Keep-candidate external summaries represented: `{len(keep_external_rows)}/3`.

## Boundary

{CLAIM_LIMIT}
"""
        (OUT_DIR / "PLAN01_BIGSCAPE_FULL_MIBIG_COMPLETION_AUDIT.md").write_text(audit)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
