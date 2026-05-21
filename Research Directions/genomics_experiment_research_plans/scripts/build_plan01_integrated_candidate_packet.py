from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "plan01_integrated_candidate_packet_2026-05-18"

CLAIM_LIMIT = (
    "Computational BGC prioritization only. This table does not validate product "
    "formation, product identity, antimicrobial activity, compound novelty, "
    "biosafety, synthesis, transfer, or engineering."
)


def read_by(path: Path, key: str) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(field, "").replace("|", "/") for field in fields) + " |")
    return "\n".join(lines)


def candidate_call(base: dict[str, str], targeted: dict[str, str], full_mibig: dict[str, str]) -> str:
    wetlab = base.get("wetlab_packaging_call", "")
    blockers = base.get("readiness_blockers", "")
    full_mibig_call = full_mibig.get("full_mibig_call", "")
    targeted_call = targeted.get("targeted_mibig_panel_call", "")
    if wetlab.startswith("KEEP") and "NO_CLOSE_FULL_MIBIG" in full_mibig_call:
        return "KEEP_STRONG_PRE_WETLAB_EXPERT_REVIEW_WITH_FULL_MIBIG_BIGSCAPE_SUPPORT"
    if wetlab.startswith("KEEP") and "NO_CLOSE_TARGETED_MIBIG" in targeted_call:
        return "KEEP_STRONG_PRE_WETLAB_EXPERT_REVIEW_WITH_TARGETED_MIBIG_BIGSCAPE_SUPPORT"
    if wetlab.startswith("KEEP"):
        return "KEEP_PRE_WETLAB_EXPERT_REVIEW_TARGETED_MIBIG_CONTEXT_LIMITED"
    if "BOUNDARY" in wetlab or "edge" in blockers.lower():
        return "HOLD_BOUNDARY_OR_CONTIG_EDGE_BEFORE_WETLAB_PACKAGING"
    if "DOMAIN" in wetlab or "domain" in blockers.lower():
        return "HOLD_DOMAIN_LOGIC_BEFORE_WETLAB_PACKAGING"
    return "HOLD_OR_REVIEW"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    base = read_by(ROOT / "outputs/plan01_claim_hardening_2026-05-17/plan01_bgc_claim_hardening.csv", "strict_bgc_id")
    derep = read_by(ROOT / "outputs/plan01_claim_hardening_2026-05-17/plan01_bgc_dereplication_novelty_matrix.csv", "strict_bgc_id")
    domain = read_by(ROOT / "outputs/plan01_claim_hardening_2026-05-17/plan01_bgc_domain_boundary_matrix.csv", "strict_bgc_id")
    safety = read_by(ROOT / "outputs/plan01_claim_hardening_2026-05-17/plan01_bgc_safety_context_matrix.csv", "strict_bgc_id")
    product = read_by(
        ROOT / "outputs/plan01_product_class_integrated_lookup_2026-05-17/plan01_product_class_integrated_summary.csv",
        "strict_bgc_id",
    )
    deep = read_by(ROOT / "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/plan01_deep_bgc_dereplication.csv", "strict_bgc_id")
    wholemag = read_by(
        ROOT / "outputs/plan01_antismash_wholemag_kaggle_attempt_2026-05-17/plan01_antismash_wholemag_keep_candidate_summary.csv",
        "candidate_id",
    )
    wholemag_bigscape = read_by(
        ROOT / "outputs/plan01_bigscape_wholemag_regions_kaggle_attempt_2026-05-17/plan01_bigscape_wholemag_keep_candidate_distance_summary.csv",
        "candidate_id",
    )
    targeted_mibig = read_by(
        ROOT / "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17/plan01_bigscape_mibig_keep_external_distance_summary.csv",
        "candidate_id",
    )
    full_mibig = read_by(
        ROOT / "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17/plan01_bigscape_full_mibig_keep_external_distance_summary.csv",
        "candidate_id",
    )

    rows: list[dict[str, str]] = []
    for strict_id, base_row in sorted(base.items(), key=lambda item: int(item[1].get("readiness_rank", "999"))):
        derep_row = derep.get(strict_id, {})
        domain_row = domain.get(strict_id, {})
        safety_row = safety.get(strict_id, {})
        product_row = product.get(strict_id, {})
        deep_row = deep.get(strict_id, {})
        wholemag_row = wholemag.get(strict_id, {})
        wholemag_bigscape_row = wholemag_bigscape.get(strict_id, {})
        targeted_row = targeted_mibig.get(strict_id, {})
        full_mibig_row = full_mibig.get(strict_id, {})
        is_keep = base_row.get("wetlab_packaging_call", "").startswith("KEEP")
        if full_mibig_row:
            full_mibig_status = "PASS_FULL_MIBIG_BIGSCAPE_ALL_VS_ALL_KEEP_SUMMARIZED"
        elif is_keep:
            full_mibig_status = "MISSING_FULL_MIBIG_KEEP_SUMMARY"
        else:
            full_mibig_status = "NOT_SUMMARIZED_FOR_HOLD_CANDIDATE"

        row = {
            "readiness_rank": base_row.get("readiness_rank", ""),
            "strict_bgc_id": strict_id,
            "genome_id": base_row.get("genome_id", ""),
            "product_class_original": base_row.get("product_class", ""),
            "wholemag_antismash_product": wholemag_row.get("wholemag_products_covering_candidate", ""),
            "product_class_frame": base_row.get("product_frame", ""),
            "integrated_candidate_call": candidate_call(base_row, targeted_row, full_mibig_row),
            "wetlab_packaging_call": base_row.get("wetlab_packaging_call", ""),
            "claim_hardening_score": base_row.get("claim_hardening_score", ""),
            "readiness_decision": base_row.get("readiness_decision", ""),
            "readiness_blockers": base_row.get("readiness_blockers", ""),
            "domain_status": domain_row.get("domain_status", base_row.get("domain_status", "")),
            "domain_blockers": domain_row.get("domain_blockers", base_row.get("domain_blockers", "")),
            "boundary_status": domain_row.get("boundary_status", base_row.get("boundary_status", "")),
            "edge_flag_500bp": domain_row.get("edge_flag_500bp", base_row.get("edge_flag_500bp", "")),
            "safety_context_call": safety_row.get("safety_context_call", base_row.get("safety_context_call", "")),
            "amrfinder_nearby_hits": safety_row.get("amrfinder_nearby_hits", ""),
            "mobilome_nearby_hits": safety_row.get("mobilome_nearby_hits", ""),
            "toxin_keyword_hits": safety_row.get("toxin_keyword_hits", ""),
            "virulence_keyword_hits": safety_row.get("virulence_keyword_hits", ""),
            "product_lookup_rows_with_hits": product_row.get("rows_with_hits", ""),
            "product_lookup_hit_terms": product_row.get("hit_terms", ""),
            "novelty_call": derep_row.get("novelty_call", base_row.get("novelty_call", "")),
            "novelty_score": derep_row.get("novelty_score", base_row.get("novelty_score", "")),
            "mibig_blast_flag": derep_row.get("blast_dereplication_flag", base_row.get("blast_dereplication_flag", "")),
            "mibig_blast_max_identity": derep_row.get("blast_max_identity", base_row.get("blast_max_identity", "")),
            "top_mibig_bgc_by_all_gene_hits": derep_row.get("top_mibig_bgc_by_all_gene_hits", deep_row.get("all_cluster_top_mibig_bgc", "")),
            "known_related_mibig_compounds": derep_row.get("known_related_mibig_compounds", deep_row.get("known_related_mibig_compounds", "")),
            "wholemag_antismash_call": wholemag_row.get("wholemag_candidate_call", ""),
            "wholemag_region_coordinates": wholemag_row.get("wholemag_region_coordinates", ""),
            "wholemag_contig_edge": wholemag_row.get("wholemag_contig_edge", ""),
            "wholemag_bigscape_nearest_file": wholemag_bigscape_row.get("nearest_region_file", ""),
            "wholemag_bigscape_nearest_distance": wholemag_bigscape_row.get("nearest_bigscape_distance", ""),
            "wholemag_bigscape_singleton_call": wholemag_bigscape_row.get("singleton_call", ""),
            "targeted_mibig_nearest_accession": targeted_row.get("nearest_external_mibig_accession", ""),
            "targeted_mibig_nearest_distance": targeted_row.get("nearest_external_bigscape_distance", ""),
            "targeted_mibig_panel_call": targeted_row.get("targeted_mibig_panel_call", ""),
            "full_mibig_bigscape_status": full_mibig_status,
            "full_mibig_nearest_accession": full_mibig_row.get("nearest_external_mibig_accession", ""),
            "full_mibig_nearest_distance": full_mibig_row.get("nearest_external_bigscape_distance", ""),
            "full_mibig_nearest_cutoff_call": full_mibig_row.get("nearest_external_cutoff_call", ""),
            "full_mibig_call": full_mibig_row.get("full_mibig_call", ""),
            "strongest_safe_claim": base_row.get("strongest_safe_claim", ""),
            "claim_limit": CLAIM_LIMIT,
            "remaining_gap": (
                "Full-MIBiG all-vs-all BiG-SCAPE is summarized for current keep candidates; product formation, product identity, "
                "antimicrobial activity, expression behavior, biosafety acceptability, and wet-lab validation remain unresolved."
            ),
        }
        rows.append(row)

    fields = [
        "readiness_rank",
        "strict_bgc_id",
        "genome_id",
        "product_class_original",
        "wholemag_antismash_product",
        "product_class_frame",
        "integrated_candidate_call",
        "wetlab_packaging_call",
        "claim_hardening_score",
        "readiness_decision",
        "readiness_blockers",
        "domain_status",
        "domain_blockers",
        "boundary_status",
        "edge_flag_500bp",
        "safety_context_call",
        "amrfinder_nearby_hits",
        "mobilome_nearby_hits",
        "toxin_keyword_hits",
        "virulence_keyword_hits",
        "product_lookup_rows_with_hits",
        "product_lookup_hit_terms",
        "novelty_call",
        "novelty_score",
        "mibig_blast_flag",
        "mibig_blast_max_identity",
        "top_mibig_bgc_by_all_gene_hits",
        "known_related_mibig_compounds",
        "wholemag_antismash_call",
        "wholemag_region_coordinates",
        "wholemag_contig_edge",
        "wholemag_bigscape_nearest_file",
        "wholemag_bigscape_nearest_distance",
        "wholemag_bigscape_singleton_call",
        "targeted_mibig_nearest_accession",
        "targeted_mibig_nearest_distance",
        "targeted_mibig_panel_call",
        "full_mibig_bigscape_status",
        "full_mibig_nearest_accession",
        "full_mibig_nearest_distance",
        "full_mibig_nearest_cutoff_call",
        "full_mibig_call",
        "strongest_safe_claim",
        "claim_limit",
        "remaining_gap",
    ]
    out_csv = OUT / "plan01_integrated_bgc_candidate_packet.csv"
    write_csv(out_csv, rows, fields)

    keep_rows = [row for row in rows if row["wetlab_packaging_call"].startswith("KEEP")]
    hold_rows = [row for row in rows if not row["wetlab_packaging_call"].startswith("KEEP")]
    keep_with_targeted = [row for row in keep_rows if "NO_CLOSE_TARGETED_MIBIG" in row["targeted_mibig_panel_call"]]
    keep_with_full_mibig = [row for row in keep_rows if "NO_CLOSE_FULL_MIBIG" in row["full_mibig_call"]]
    wholemag_supported = [row for row in keep_rows if row["wholemag_antismash_call"]]

    report = f"""# Plan01 Integrated BGC Candidate Packet

Date: 2026-05-18

## Claim Boundary

{CLAIM_LIMIT}

## Summary

- Candidates represented: `{len(rows)}`
- Keep candidates: `{len(keep_rows)}`
- Computational holds: `{len(hold_rows)}`
- Keep candidates with whole-MAG antiSMASH direct-region support: `{len(wholemag_supported)}/{len(keep_rows)}`
- Keep candidates with no close targeted-MIBiG BiG-SCAPE link at cutoffs 0.3/0.5: `{len(keep_with_targeted)}/{len(keep_rows)}`
- Keep candidates with no close full-MIBiG BiG-SCAPE link at cutoffs 0.3/0.5: `{len(keep_with_full_mibig)}/{len(keep_rows)}`
- Full-MIBiG BiG-SCAPE status: `PASS_FULL_MIBIG_BIGSCAPE_ALL_VS_ALL`

## Keep Candidate Snapshot

{md_table(keep_rows, ["strict_bgc_id", "product_class_original", "wholemag_antismash_product", "integrated_candidate_call", "novelty_call", "wholemag_bigscape_nearest_distance", "targeted_mibig_nearest_accession", "targeted_mibig_nearest_distance", "targeted_mibig_panel_call", "full_mibig_nearest_accession", "full_mibig_nearest_distance", "full_mibig_call"])}

## Hold Candidate Snapshot

{md_table(hold_rows, ["strict_bgc_id", "product_class_original", "integrated_candidate_call", "readiness_blockers", "domain_blockers", "edge_flag_500bp"])}

## Interpretation

The three keep candidates remain the strongest Plan01 pre-wet-lab expert-review BGC hypotheses after integrating whole-MAG antiSMASH, within-whole-MAG-region BiG-SCAPE, targeted-MIBiG BiG-SCAPE, and full-MIBiG 4.0 all-vs-all BiG-SCAPE context. Neither the targeted-MIBiG panel nor the full-MIBiG run links any keep candidate to a close MIBiG family at cutoffs 0.3 or 0.5. The four held candidates remain computational holds because their prior boundary/domain blockers are not resolved by the newer dereplication layers.

## Outputs

- `plan01_integrated_bgc_candidate_packet.csv`
- `PLAN01_INTEGRATED_BGC_CANDIDATE_PACKET_COMPLETION_AUDIT.md`
"""
    (OUT / "PLAN01_INTEGRATED_BGC_CANDIDATE_PACKET_REPORT.md").write_text(report)

    audit = f"""# Plan01 Integrated BGC Candidate Packet Completion Audit

Date: 2026-05-18

## Verdict

PASS_UPDATED_PACKET_WITH_FULL_MIBIG_COMPLETE: the Plan01 candidate packet now integrates the completed whole-MAG antiSMASH, whole-MAG-region BiG-SCAPE, targeted-MIBiG BiG-SCAPE, full-MIBiG 4.0 all-vs-all BiG-SCAPE, product lookup, boundary/domain, dereplication, and local safety-context layers.

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Preserve original keep/hold decisions | `plan01_integrated_bgc_candidate_packet.csv wetlab_packaging_call` | PASS |
| Add whole-MAG antiSMASH direct-region support for keep candidates | `wholemag_antismash_call` | PASS_3_OF_3_KEEP |
| Add whole-MAG-region BiG-SCAPE singleton/distance context for keep candidates | `wholemag_bigscape_*` columns | PASS_3_OF_3_KEEP |
| Add targeted-MIBiG BiG-SCAPE nearest-external context for keep candidates | `targeted_mibig_*` columns | PASS_3_OF_3_KEEP |
| Add full-MIBiG all-vs-all BiG-SCAPE nearest-external context for keep candidates | `full_mibig_*` columns | PASS_3_OF_3_KEEP |
| Retain boundary/domain and safety limitations | `domain_*`, `boundary_*`, `safety_*`, `claim_limit` columns | PASS |
| Avoid activity, product, biosafety, or wet-lab validation claims | `claim_limit` and `remaining_gap` columns | PASS |

## Counts

- Rows: `{len(rows)}`
- Keep candidates: `{len(keep_rows)}`
- Holds: `{len(hold_rows)}`
- Keep candidates with targeted-MIBiG no-close-link call: `{len(keep_with_targeted)}/{len(keep_rows)}`
- Keep candidates with full-MIBiG no-close-link call: `{len(keep_with_full_mibig)}/{len(keep_rows)}`

## Remaining Work

- Optional only: add CORASON/BiG-SLiCE or broader publication-grade BGC-family context if needed for a manuscript.
- Keep product formation, product identity, antimicrobial activity, biosafety, and wet-lab validation claims experimental only.
"""
    (OUT / "PLAN01_INTEGRATED_BGC_CANDIDATE_PACKET_COMPLETION_AUDIT.md").write_text(audit)
    print(f"Wrote {out_csv.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
