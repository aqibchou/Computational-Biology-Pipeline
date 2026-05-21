from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
REPORT = OUT / "PRE_WETLAB_HARDENING_ARTIFACT_VERIFICATION_2026-05-17.md"
CSV_OUT = OUT / "pre_wetlab_hardening_artifact_verification_2026-05-17.csv"


CHECKS = [
    {
        "plan": "01",
        "requirement": "MIBiG dereplication and BGC boundary/domain/safety matrix",
        "evidence": [
            "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/plan01_deep_bgc_dereplication.csv",
            "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/plan01_boundary_domain_safety_deepcheck.csv",
            "outputs/plan01_integrated_candidate_packet_2026-05-18/plan01_integrated_bgc_candidate_packet.csv",
            "outputs/plan01_integrated_candidate_packet_2026-05-18/PLAN01_INTEGRATED_BGC_CANDIDATE_PACKET_REPORT.md",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "01",
        "requirement": "Whole-MAG antiSMASH coverage for Plan01 keep candidates",
        "evidence": [
            "outputs/plan01_antismash_wholemag_kaggle_attempt_2026-05-17/plan01_antismash_wholemag_keep_candidate_summary.csv",
            "outputs/plan01_antismash_wholemag_kaggle_attempt_2026-05-17/version3/outputs/antismash_wholemag_outputs/*/*.region*.gbk",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "01",
        "requirement": "Targeted MIBiG reference-panel BiG-SCAPE",
        "evidence": [
            "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_MIBIG_REFERENCE_PANEL_SUMMARY_REPORT.md",
            "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17/plan01_bigscape_mibig_keep_external_distance_summary.csv",
            "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17/version3/outputs/outputs.db",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "01",
        "requirement": "Full-MIBiG/global BiG-SCAPE",
        "evidence": [
            "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_FULL_MIBIG_SUMMARY_REPORT.md",
            "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17/plan01_bigscape_full_mibig_keep_external_distance_summary.csv",
        ],
        "fallback_evidence": [
            "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_FULL_MIBIG_LAUNCH_STATUS.md",
            "outputs/plan01_bigscape_full_mibig_query_kaggle_attempt_2026-05-18/PLAN01_BIGSCAPE_FULL_MIBIG_QUERY_LAUNCH_STATUS.md",
        ],
        "completion_gate": "explicit_remaining_global_gap",
    },
    {
        "plan": "02",
        "requirement": "UniRef/nr dereplication and full Pfam-A HMMER validation for claim-hardening queue",
        "evidence": [
            "outputs/plan02_uniref_pending_recovery_2026-05-17/plan02_uniref_pending_recovery_crosswalk.csv",
            "outputs/plan02_full_pfam_hmmer_validation_2026-05-17/plan02_full_pfam_hmmer_validation.csv",
            "outputs/plan02_claim_hardening_2026-05-17/plan02_commercial_benchmark_matrix.csv",
            "outputs/plan02_claim_hardening_2026-05-17/plan02_cofactor_dependency_matrix.csv",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "04",
        "requirement": "Genome quality, strain/reference gate, ecology, safety, isolate, host, and trait literature package",
        "evidence": [
            "outputs/plan04_claim_hardening_2026-05-17/plan04_finalist_claim_hardening.csv",
            "outputs/plan04_reference_ani_2026-05-17/plan04_reference_ani_results.csv",
            "outputs/plan04_bacteriovorax_reference_ani_2026-05-17/plan04_bacteriovorax_reference_ani_results.csv",
            "outputs/plan04_remaining_mag_reference_gate_2026-05-17/plan04_remaining_mag_reference_gate.csv",
            "outputs/plan04_claim_hardening_2026-05-17/plan04_trait_literature_support.csv",
            "outputs/plan04_claim_hardening_2026-05-17/plan04_isolate_availability_triage.csv",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "06",
        "requirement": "Stability predictors/proxies, loop/disorder, phylogeny, structure confidence, benchmark",
        "evidence": [
            "outputs/plan06_thermompnn_kaggle_attempt_v8_t4_2026-05-17/outputs/plan06_thermompnn_aggregate_summary.csv",
            "outputs/plan06_structure_energy_proxy_2026-05-17/plan06_structure_energy_proxy.csv",
            "outputs/plan06_loop_disorder_comparison_2026-05-17/plan06_loop_disorder_comparison.csv",
            "outputs/plan06_07_iqtree_phylogeny_2026-05-17/plan06_iqtree_phylogeny_summary.csv",
            "outputs/plan06_claim_hardening_2026-05-17/plan06_industrial_benchmark_matrix.csv",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "06",
        "requirement": "FoldX/Rosetta-style estimates",
        "evidence": [
            "outputs/plan06_structure_energy_proxy_2026-05-17/plan06_foldx_rosetta_feasibility.csv",
        ],
        "completion_gate": "tool_unavailable_proxy_only",
    },
    {
        "plan": "07",
        "requirement": "Reaction-family phylogeny, Rhea/EC, catalytic/cofactor, neighborhood, pocket, dependency",
        "evidence": [
            "outputs/plan06_07_iqtree_phylogeny_2026-05-17/plan07_iqtree_phylogeny_summary.csv",
            "outputs/plan07_claim_hardening_2026-05-17/plan07_finalist_claim_hardening.csv",
            "outputs/plan07_claim_hardening_2026-05-17/plan07_cofactor_partner_dependency_matrix.csv",
            "outputs/plan07_reference_ligand_pocket_comparison_2026-05-17/plan07_reference_ligand_pocket_comparison.csv",
            "outputs/plan07_reference_ligand_pocket_comparison_2026-05-17/plan07_reference_ligand_pocket_residue_map.csv",
        ],
        "completion_gate": "required_current_packaging",
    },
    {
        "plan": "09",
        "requirement": "Atlas metadata, family filtering, replication, stability scoring, Plan02/06 overlap",
        "evidence": [
            "outputs/plan09_release_metadata_stability_2026-05-17/plan09_extremophile_metadata_audit.csv",
            "outputs/plan09_claim_hardening_2026-05-17/plan09_filter_funnel.csv",
            "outputs/plan09_release_metadata_stability_2026-05-17/plan09_stability_feature_scores.csv",
            "outputs/plan09_release_metadata_stability_2026-05-17/plan09_stability_track_summary.csv",
            "outputs/plan09_claim_hardening_2026-05-17/plan09_overlap_with_plan02_plan06_winners.csv",
        ],
        "completion_gate": "required_current_packaging",
    },
]


def count_csv_rows(path: Path) -> int | str:
    try:
        with path.open(newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return sum(1 for _ in reader)
    except UnicodeDecodeError:
        return "binary_or_non_utf8"


def count_db_tables(path: Path) -> str:
    try:
        conn = sqlite3.connect(path)
        try:
            parts = []
            for table in ["gbk", "bgc_record", "distance", "family"]:
                try:
                    value = conn.execute(f"select count(*) from {table}").fetchone()[0]
                    parts.append(f"{table}={value}")
                except sqlite3.Error:
                    pass
            return ";".join(parts)
        finally:
            conn.close()
    except sqlite3.Error as exc:
        return f"sqlite_error:{exc}"


def evidence_summary(pattern: str) -> tuple[int, str, str]:
    matches = sorted(ROOT.glob(pattern))
    detail_parts = []
    for path in matches[:25]:
        rel = str(path.relative_to(ROOT))
        if path.suffix == ".csv":
            detail_parts.append(f"{rel}[rows={count_csv_rows(path)}]")
        elif path.suffix == ".db":
            detail_parts.append(f"{rel}[{count_db_tables(path)}]")
        else:
            detail_parts.append(rel)
    if len(matches) > 25:
        detail_parts.append(f"... plus {len(matches) - 25} more")
    return len(matches), "; ".join(detail_parts), str(matches[0].relative_to(ROOT)) if matches else ""


def main() -> None:
    rows: list[dict[str, object]] = []
    for check in CHECKS:
        evidence_patterns = check["evidence"]
        missing = []
        evidence_details = []
        first_hit = []
        total_hits = 0
        for pattern in evidence_patterns:
            count, details, first = evidence_summary(pattern)
            total_hits += count
            if first:
                first_hit.append(first)
            if details:
                evidence_details.append(details)
            if count == 0:
                missing.append(pattern)
        fallback_hits = []
        for pattern in check.get("fallback_evidence", []):
            count, details, first = evidence_summary(pattern)
            if count:
                fallback_hits.append(details or first)

        if not missing:
            status = "PASS_ARTIFACTS_PRESENT"
        elif check["completion_gate"] == "explicit_remaining_global_gap" and fallback_hits:
            status = "IN_PROGRESS_LAUNCH_ARTIFACT_PRESENT_OUTPUTS_PENDING"
        else:
            status = "MISSING_REQUIRED_ARTIFACT"

        rows.append(
            {
                "plan": check["plan"],
                "requirement": check["requirement"],
                "completion_gate": check["completion_gate"],
                "status": status,
                "missing_patterns": "; ".join(missing),
                "matched_evidence_count": total_hits,
                "first_matched_evidence": "; ".join(first_hit[:5]),
                "evidence_details": " | ".join(evidence_details + fallback_hits),
            }
        )

    with CSV_OUT.open("w", newline="") as handle:
        fields = [
            "plan",
            "requirement",
            "completion_gate",
            "status",
            "missing_patterns",
            "matched_evidence_count",
            "first_matched_evidence",
            "evidence_details",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    status_lines = "\n".join(f"- `{key}`: `{value}`" for key, value in sorted(status_counts.items()))
    table_lines = [
        "| Plan | Requirement | Gate | Status | Missing |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        table_lines.append(
            "| {plan} | {requirement} | {completion_gate} | {status} | {missing_patterns} |".format(**row).replace("\n", " ")
        )

    REPORT.write_text(
        "# Pre-Wet-Lab Hardening Artifact Verification\n\n"
        "Date: 2026-05-17\n\n"
        "## Scope\n\n"
        "This verifier checks whether the named evidence files behind the current pre-wet-lab hardening audit exist and, where possible, records CSV row counts or SQLite table counts. It does not treat file existence as biological validation.\n\n"
        "## Status Counts\n\n"
        f"{status_lines}\n\n"
        "## Requirement Table\n\n"
        + "\n".join(table_lines)
        + "\n\n## Output\n\n"
        "- `pre_wetlab_hardening_artifact_verification_2026-05-17.csv`\n"
    )
    print(f"Wrote {CSV_OUT.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
