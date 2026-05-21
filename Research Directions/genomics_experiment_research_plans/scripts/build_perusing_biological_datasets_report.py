from __future__ import annotations

import csv
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "Perusing_Biological_Datasets.md"


PLAN_REPORTS = {
    "Plan 01 - Secondary Metabolite / BGC Discovery": [
        "outputs/plan01_integrated_candidate_packet_2026-05-18/PLAN01_INTEGRATED_BGC_CANDIDATE_PACKET_REPORT.md",
        "outputs/plan01_claim_hardening_2026-05-17/PLAN01_CLAIM_HARDENING_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_STRICT_BGC_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_HIGH_PRIORITY_VALIDATION_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_TOP16_DEEP_VALIDATION_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_TOP3_NOVELTY_CHECK_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_FINALISTS_NOVELTY_CHECK_REPORT.md",
        "outputs/plan01_strict_bgc_triage_2026-05-14/PLAN01_GO_CANDIDATE_READINESS_REPORT.md",
        "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/PLAN01_DEEP_BGC_DEREP_BOUNDARY_REPORT.md",
        "outputs/plan01_mibig_reference_panel_2026-05-17/PLAN01_MIBIG_REFERENCE_PANEL_REPORT.md",
        "outputs/plan01_reconstructed_bgc_genbanks_2026-05-17/PLAN01_RECONSTRUCTED_BGC_GENBANK_REPORT.md",
        "outputs/plan01_bigscape_reconstructed_2026-05-17/PLAN01_BIGSCAPE_RECONSTRUCTED_REPORT.md",
        "outputs/plan01_antismash_region_kaggle_attempt_2026-05-17/PLAN01_ANTISMASH_REGION_KAGGLE_SUMMARY_REPORT.md",
        "outputs/plan01_antismash_wholemag_kaggle_attempt_2026-05-17/PLAN01_ANTISMASH_WHOLEMAG_SUMMARY_REPORT.md",
        "outputs/plan01_bigscape_mibig_reference_panel_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_MIBIG_REFERENCE_PANEL_SUMMARY_REPORT.md",
        "outputs/plan01_bigscape_wholemag_regions_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_WHOLEMAG_SUMMARY_REPORT.md",
        "outputs/plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17/PLAN01_BIGSCAPE_FULL_MIBIG_SUMMARY_REPORT.md",
        "outputs/plan01_native_bgc_clustering_feasibility_2026-05-17/PLAN01_NATIVE_BGC_CLUSTERING_FEASIBILITY_REPORT.md",
        "outputs/plan01_product_class_integrated_lookup_2026-05-17/PLAN01_PRODUCT_CLASS_INTEGRATED_LOOKUP_REPORT.md",
        "outputs/plan01_coconut_product_lookup_2026-05-17/PLAN01_COCONUT_PRODUCT_LOOKUP_REPORT.md",
    ],
    "Plan 02 - Industrial Biocatalyst Candidate Discovery": [
        "outputs/plan02_09_deep_strict_2026-05-14/HIGH_PRECISION_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/STAGE2_STRICT_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/expanded_triage_queue_200_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/PLAN02_09_TIGHTENING_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_final_wetlab_bridge/PLAN02_09_FINAL_WETLAB_BRIDGE_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_final_wetlab_bridge/PLAN02_09_T4_COLABFOLD_COMPLETION_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_final_wetlab_bridge/active_site_pocket_inspection/PLAN02_09_ACTIVE_SITE_POCKET_INSPECTION_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_finalist12_dedup_residue/PLAN02_09_FINALIST12_DEDUP_RESIDUE_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_top5_full_derep_structures/PLAN02_09_TOP5_FULL_DEREP_STRUCTURE_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/plan02_09_remaining6_full_derep_structures/PLAN02_09_REMAINING6_FULL_DEREP_STRUCTURE_REPORT.md",
        "outputs/plan02_claim_hardening_2026-05-17/PLAN02_CLAIM_HARDENING_REPORT.md",
        "outputs/plan02_full_pfam_hmmer_validation_2026-05-17/PLAN02_FULL_PFAM_HMMER_VALIDATION_REPORT.md",
        "outputs/plan02_uniref_pending_recovery_2026-05-17/PLAN02_UNIREF_PENDING_RECOVERY_REPORT.md",
    ],
    "Plan 03 - Nitrogen-Cycle Pathway Candidate Discovery": [
        "outputs/plan03_pre_wetlab_screen_2026-05-18/PLAN03_PRE_WETLAB_SCREEN_REPORT.md",
        "outputs/plan03_pre_wetlab_screen_2026-05-18/PLAN03_RESEARCH_STYLE_WRITEUP.md",
        "outputs/plan03_iqtree_kaggle_2026-05-18/PLAN03_IQTREE_KAGGLE_RESULTS_SUMMARY.md",
        "outputs/plan03_iqtree_kaggle_2026-05-18/binary_complete/plan03_iqtree_kaggle_outputs/PLAN03_IQTREE_KAGGLE_REPORT.md",
        "outputs/plan03_iqtree_kaggle_2026-05-18/original_complete/plan03_iqtree_kaggle_outputs/PLAN03_IQTREE_KAGGLE_REPORT.md",
    ],
    "Plan 04 - Plant-Growth-Promotion Genome Candidate Discovery": [
        "outputs/plan04_pgp_bridge_2026-05-17/PLAN04_PGP_BRIDGE_REPORT.md",
        "outputs/plan04_claim_hardening_2026-05-17/PLAN04_CLAIM_HARDENING_REPORT.md",
        "outputs/plan04_claim_hardening_2026-05-17/PLAN04_RESEARCH_STYLE_WRITEUP.md",
        "outputs/plan04_reference_ani_2026-05-17/PLAN04_REFERENCE_ANI_REPORT.md",
        "outputs/plan04_bacteriovorax_reference_ani_2026-05-17/PLAN04_BACTERIOVORAX_REFERENCE_ANI_REPORT.md",
        "outputs/plan04_remaining_mag_reference_gate_2026-05-17/PLAN04_REMAINING_MAG_REFERENCE_GATE_REPORT.md",
        "outputs/plan04_strain_dereplication_2026-05-17/PLAN04_STRAIN_DEREPLICATION_REPORT.md",
    ],
    "Plan 05 - Stability-Focused Enzyme Candidate Discovery": [
        "outputs/plan06_deep_stability_bridge_2026-05-15/PLAN06_DEEP_STABILITY_BRIDGE_REPORT.md",
        "outputs/plan06_deep_stability_bridge_2026-05-15/PLAN06_RESEARCH_STYLE_WRITEUP.md",
        "outputs/plan06_deep_stability_bridge_2026-05-15/PLAN06_CANDIDATE_SPECIFIC_COLABFOLD_REPORT.md",
        "outputs/plan06_claim_hardening_2026-05-17/PLAN06_CLAIM_HARDENING_REPORT.md",
        "outputs/plan06_structure_energy_proxy_2026-05-17/PLAN06_STRUCTURE_ENERGY_PROXY_REPORT.md",
        "outputs/plan06_loop_disorder_comparison_2026-05-17/PLAN06_LOOP_DISORDER_COMPARISON_REPORT.md",
        "outputs/plan06_07_iqtree_phylogeny_2026-05-17/PLAN06_07_IQTREE_PHYLOGENY_REPORT.md",
        "outputs/plan06_thermompnn_kaggle_attempt_v8_t4_2026-05-17/outputs/PLAN06_THERMOMPNN_AGGREGATE_REPORT.md",
    ],
    "Plan 06 - Rare Chemistry Enzyme Candidate Discovery": [
        "outputs/plan07_rare_chemistry_bridge_2026-05-15/PLAN07_RARE_CHEMISTRY_BRIDGE_REPORT.md",
        "outputs/plan07_rare_chemistry_bridge_2026-05-15/PLAN07_RESEARCH_STYLE_WRITEUP.md",
        "outputs/plan07_rare_chemistry_bridge_2026-05-15/PLAN07_CANDIDATE_SPECIFIC_COLABFOLD_REPORT.md",
        "outputs/plan07_claim_hardening_2026-05-17/PLAN07_CLAIM_HARDENING_REPORT.md",
        "outputs/plan07_reference_ligand_pocket_comparison_2026-05-17/PLAN07_REFERENCE_LIGAND_POCKET_COMPARISON_REPORT.md",
        "outputs/plan06_07_iqtree_phylogeny_2026-05-17/PLAN06_07_IQTREE_PHYLOGENY_REPORT.md",
    ],
    "Plan 07 - Biomaterials / Biopolymer Candidate Discovery": [
        "outputs/plan08_pre_wetlab_screen_2026-05-18/PLAN08_PRE_WETLAB_SCREEN_REPORT.md",
        "outputs/plan08_pre_wetlab_screen_2026-05-18/PLAN08_RESEARCH_STYLE_WRITEUP.md",
    ],
    "Plan 08 - Extremophile Enzyme Atlas / Release Layer": [
        "outputs/plan09_release_metadata_stability_2026-05-17/PLAN09_RELEASE_METADATA_STABILITY_REPORT.md",
        "outputs/plan09_claim_hardening_2026-05-17/PLAN09_CLAIM_HARDENING_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/HIGH_PRECISION_REPORT.md",
        "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening/PLAN02_09_TIGHTENING_REPORT.md",
    ],
}


PACKET_GROUPS = {
    "Plan 01 - High-Priority BGC Validation Packets": "outputs/plan01_strict_bgc_triage_2026-05-14/plan01_high_priority_validation_packets/*.md",
    "Plan 01 - Top 50 Strict BGC Packets": "outputs/plan01_strict_bgc_triage_2026-05-14/plan01_top_50_strict_bgc_packets/*.md",
    "Plan 02/08 - Lab-Ready High-Precision Enzyme Packets": "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_high_precision_packets/*.md",
    "Plan 02/08 - Strict Lab-Ready Enzyme Packets": "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_candidate_packets/*.md",
    "Plan 03 - Nitrogen-Cycle Candidate Packets": "outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/*.md",
    "Plan 04 - PGP Wet-Lab Planning Packets": "outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/*.md",
    "Plan 05 - Stability Wet-Lab Planning Packets": "outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/*.md",
    "Plan 06 - Rare-Chemistry Wet-Lab Planning Packets": "outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/*.md",
    "Plan 07 - Biomaterials Candidate Packets": "outputs/plan08_pre_wetlab_screen_2026-05-18/plan08_top_candidate_packets/*.md",
}


CSV_TABLES = [
    "outputs/plan01_integrated_candidate_packet_2026-05-18/plan01_integrated_bgc_candidate_packet.csv",
    "outputs/plan01_strict_bgc_triage_2026-05-14/plan01_finalists_novelty_check.csv",
    "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_high_precision_shortlist.csv",
    "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_shortlist.csv",
    "outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_candidate_packet_manifest.csv",
    "outputs/plan04_claim_hardening_2026-05-17/plan04_finalist_claim_hardening.csv",
    "outputs/plan06_claim_hardening_2026-05-17/plan06_finalist_claim_hardening.csv",
    "outputs/plan07_claim_hardening_2026-05-17/plan07_finalist_claim_hardening.csv",
    "outputs/plan08_pre_wetlab_screen_2026-05-18/plan08_candidate_packet_manifest.csv",
    "outputs/plan09_release_metadata_stability_2026-05-17/plan09_stability_feature_scores.csv",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: str | Path) -> str:
    p = ROOT / path if isinstance(path, str) else path
    return p.read_text(encoding="utf-8", errors="replace").strip()


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return path.stem


def extract_backticked_id(title: str) -> str:
    m = re.search(r"`([^`]+)`", title)
    return m.group(1) if m else title


def display_numbered_text(text: str) -> str:
    text = text.replace("Plan 02/09", "Plan 02/08")
    mapping = {"06": "05", "07": "06", "08": "07", "09": "08"}
    return re.sub(r"Plan (06|07|08|09)\b", lambda m: f"Plan {mapping[m.group(1)]}", text)


def demote_markdown_headings(text: str, levels: int = 3) -> str:
    demoted: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})(\s+.*)$", line)
        if match:
            hashes = "#" * min(6, len(match.group(1)) + levels)
            demoted.append(f"{hashes}{match.group(2)}")
        else:
            demoted.append(line)
    return "\n".join(demoted)


def infer_purpose(path: Path, title: str) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    name = path.name.lower()
    if "plan01" in rel(path).lower():
        return "secondary-metabolite/BGC discovery and expert-review natural-product follow-up"
    if "plan02_09" in rel(path).lower():
        target = re.search(r"Target family:\s*`([^`]+)`", text)
        condition = re.search(r"Condition:\s*`([^`]+)`", text)
        bits = [target.group(1) if target else "enzyme", condition.group(1) if condition else ""]
        return " / ".join([b for b in bits if b]) + " biocatalyst hypothesis"
    if "plan03" in rel(path).lower():
        track = re.search(r"- Track:\s*(.+)", text)
        rep = re.search(r"- Representative marker/protein:\s*(.+)", text)
        return "; ".join([x.group(1).strip() for x in [track, rep] if x]) or "nitrogen-cycle pathway hypothesis"
    if "plan04" in rel(path).lower():
        hyp = re.search(r"Primary hypothesis:\s*(.+)", text)
        return hyp.group(1).strip() if hyp else "plant-growth-promotion genome hypothesis"
    if "plan06" in rel(path).lower():
        fam = re.search(r"Family:\s*`?([^`\n]+)`?", text)
        axis = re.search(r"Primary stability axis:\s*`?([^`\n]+)`?", text)
        return " / ".join([x.group(1).strip() for x in [fam, axis] if x]) + " stability-screening enzyme hypothesis"
    if "plan07" in rel(path).lower():
        hyp = re.search(r"Primary hypothesis:\s*(.+)", text)
        return hyp.group(1).strip() if hyp else "rare-chemistry enzyme hypothesis"
    if "plan08" in rel(path).lower():
        track = re.search(r"- Track:\s*(.+)", text)
        rep = re.search(r"- Representative feature:\s*(.+)", text)
        return "; ".join([x.group(1).strip() for x in [track, rep] if x]) or "biomaterials hypothesis"
    return "candidate hypothesis"


def packet_paths() -> list[tuple[str, list[Path]]]:
    groups = []
    for label, pattern in PACKET_GROUPS.items():
        paths = sorted(ROOT.glob(pattern))
        if paths:
            groups.append((label, paths))
    return groups


def row_count(path: Path) -> int:
    with path.open(encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return max(0, len(rows) - 1)


def build_inventory_rows() -> list[tuple[str, str, str, str]]:
    rows = []
    for group, paths in packet_paths():
        for p in paths:
            title = first_heading(p)
            candidate = display_numbered_text(extract_backticked_id(title))
            rows.append((group, candidate, infer_purpose(p, title), rel(p)))
    return rows


def add_source(lines: list[str], path: Path, level: int = 3) -> None:
    heading = "#" * level
    lines.extend(
        [
            "",
            "---",
            "",
            f"{heading} Source: `{rel(path)}`",
            "",
            demote_markdown_headings(path.read_text(encoding="utf-8", errors="replace").strip()),
            "",
        ]
    )


def add_tabular_source(lines: list[str], path: Path) -> None:
    suffix = path.suffix.lower().lstrip(".") or "text"
    lines.extend(
        [
            "",
            "---",
            "",
            f"### Tabular Source: `{rel(path)}`",
            "",
            f"Rows: {row_count(path)}",
            "",
            f"```{suffix}",
            path.read_text(encoding="utf-8", errors="replace").strip(),
            "```",
            "",
        ]
    )


def main() -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d")
    inventory = build_inventory_rows()
    lines: list[str] = [
        "# Perusing Biological Datasets",
        "",
        f"Generated: {now}",
        "",
        "## Abstract",
        "",
        "This report presents a single computational discovery campaign for prioritizing biological candidates from genomics-scale datasets. The work is organized as one screening funnel with eight domain-specific modules: secondary-metabolite biosynthetic gene clusters, industrial and extremophile enzymes, nitrogen-cycle pathways, plant-growth-promotion genomes, naturally stable enzyme homologs, rare-chemistry enzymes, biomaterial/biopolymer systems, and an extremophile enzyme atlas/release layer. The modules differ in evidence type and screening logic, but they share the same end-to-end structure: assemble a candidate universe, annotate function and context, apply domain-specific evidence gates, harden novelty and safety claims, downselect to wet-lab-facing hypotheses, and preserve every packetized candidate with source evidence.",
        "",
        "The integrated screen produced computationally prioritized hypotheses rather than validated products. Plan 01 produced three strongest BGC keep candidates for natural-product and antibiotic-lead follow-up discussion while preserving broader high-priority BGC queues. Plans 02 and 08 produced strict and high-precision enzyme review queues across ketoreductase, lipase, protease, transaminase, peroxidase, dehalogenase, esterase, monooxygenase, glycosidase, nitrilase, cellulase, and xylanase families. Plan 03 produced six nitrogen-cycle pathway candidates for nitrogen fixation, N2O-reduction, urease/rhizosphere nitrogen availability, and nitrate/nitrite transformation follow-up. Plan 04 produced four plant-growth-promotion genome candidates for osmoprotection/stress support, phosphate solubilization, siderophore production, and antifungal/BGC hypotheses. Plan 05 produced four stability-oriented enzyme candidates for salt/desiccation/stress-tolerance screening. Plan 06 produced four rare-chemistry candidates for redox, organosulfur, rare-sugar, and dehalogenation chemistry. Plan 07 produced six immediate biomaterials candidates and three review candidates spanning PHA/biopolymer, EPS/capsule export, protein-material adhesion, pigment/melanin-like chemistry, and BGC-derived material hypotheses.",
        "",
        "All claims in this report remain computational and pre-wet-lab. The candidates are hypotheses for expert review and controlled validation discussions, not demonstrated antibiotics, validated enzymes, proven nitrogen-cycle phenotypes, plant-growth products, biomaterials, expression-ready constructs, field interventions, environmental releases, or safety determinations.",
        "",
        "## Integrated Screening Process",
        "",
        "The project should be read as one staged discovery workflow rather than eight independent studies. First, candidate universes were assembled from genome, gene, BGC, metadata, marker, and annotation artifacts. Second, each candidate was assigned a biological role using the strongest available domain evidence: BGC callers and product-class lookups for secondary metabolism, enzyme-family and active-site evidence for biocatalysis, marker-gene/pathway context for nitrogen cycling, genome-level trait screens for plant-growth promotion, stability-axis evidence for natural stable homologs, ligand/pocket context for rare chemistry, and material-relevant pathway or surface-feature evidence for biomaterials.",
        "",
        "Third, the same hardening logic was applied across modules: candidates had to survive increasingly specific filters for annotation plausibility, novelty or dereplication, practical recovery context, source metadata, safety/context flags, and wet-lab interpretability. The evidence gate changed by biological question, but the decision standard stayed consistent: move forward only when the computational record supported a bounded, testable hypothesis and clearly stated what remained unproven.",
        "",
        "Fourth, the screen separated immediate wet-lab candidates from review-only candidates. Immediate candidates have enough annotation, context, and practicality support to justify expert wet-lab planning. Review-only candidates remain scientifically interesting but require additional chemistry, product-class, sequence, organism, or safety clarification before they should be treated as wet-lab priorities.",
        "",
        "## Screening Differences By Plan",
        "",
        "| Report plan | Screening lens | Main evidence gates | Output role |",
        "|---|---|---|---|",
        "| 01 | Secondary-metabolite/BGC discovery | antiSMASH/GECCO/SanntiS support, BGC boundary review, MIBiG/BiG-SCAPE dereplication, product-class lookup, safety/context checks | Natural-product and antibiotic-lead follow-up hypotheses |",
        "| 02 | Industrial biocatalyst discovery | Enzyme-family assignment, active-site plausibility, Pfam/UniRef recovery, structure/pocket checks, family-level assay relevance | Lab-ready and expert-review enzyme queues |",
        "| 03 | Nitrogen-cycle pathway discovery | Marker/pathway coherence, representative protein support, genome/source context, IQ-TREE phylogeny update | Nitrogen-cycle phenotype hypotheses for controlled validation |",
        "| 04 | Plant-growth-promotion genome discovery | Genome-level PGP trait evidence, reference ANI, strain dereplication, safety/context filtering, practicality checks | PGP genome hypotheses for controlled isolate or organism-level review |",
        "| 05 | Natural stability discovery | Stability-axis scoring, structure models, loop/disorder and energy proxies, IQ-TREE context, ThermoMPNN aggregate evidence without mutation design | Naturally stable enzyme homolog hypotheses |",
        "| 06 | Rare-chemistry discovery | Rare-function annotations, structural plausibility, ligand/pocket comparison, phylogenetic context, safety/practicality screens | Redox, organosulfur, rare-sugar, and dehalogenation chemistry hypotheses |",
        "| 07 | Biomaterials discovery | PHA/EPS/protein-material/pigment/BGC evidence, export/recovery context, material-subtype scoring, unresolved-chemistry triage | Immediate biomaterial candidates plus BGC review packets |",
        "| 08 | Extremophile enzyme atlas/release layer | Metadata-linked stress context, stability-feature scoring, high-precision enzyme crosswalk, release-readiness organization | Traceable atlas and candidate release layer supporting Plans 02 and 05 |",
        "",
        "## Screening Modules And Outputs",
        "",
        "| Report plan | Original source plan | Completed focus | Candidate-level output preserved here |",
        "|---|---|---|---|",
        "| 01 | 01 | Secondary metabolite/BGC discovery | Integrated 3 keep candidates, hold candidates, high-priority BGC validation packets, and top-50 strict BGC packets |",
        "| 02 | 02 | Industrial biocatalyst discovery | High-precision and strict lab-ready enzyme packets plus hardening reports |",
        "| 03 | 03 | Nitrogen-cycle pathway discovery | 6 pre-wet-lab pathway packets plus Kaggle IQ-TREE phylogeny update |",
        "| 04 | 04 | Plant-growth-promotion genome discovery | 4 wet-lab planning genome packets plus reference/safety hardening |",
        "| 05 | 06 | Stability-focused enzyme discovery | 4 wet-lab planning enzyme packets plus structure, IQ-TREE, and ThermoMPNN aggregate layers |",
        "| 06 | 07 | Rare-chemistry enzyme discovery | 4 wet-lab planning enzyme packets plus structure/ligand-pocket layers |",
        "| 07 | 08 | Biomaterials and biopolymer discovery | 6 immediate packets and 3 review BGC/material packets |",
        "| 08 | 09 | Extremophile enzyme atlas and release layer | 4,071-row high-precision atlas summary, 40-row lab-ready crosswalk, release metadata, and stability-feature model |",
        "",
        "## Candidate Inventory",
        "",
        "The following table lists the packetized candidates preserved from the unified screen. The source path column keeps the original artifact locations, while the report-facing labels use the consecutive Plan 01-08 numbering.",
        "",
        "| Source group | Candidate | Purpose / hypothesis | Packet path |",
        "|---|---|---|---|",
    ]
    for group, candidate, purpose, path in inventory:
        lines.append(f"| {group} | `{candidate}` | {purpose} | `{path}` |")

    lines.extend(
        [
            "",
            "## Raw Artifact Table Inventory",
            "",
            "The combined report keeps markdown reports, candidate packets, and the key result tables inline. The table below gives row counts for the tabular appendices that follow.",
            "",
            "| Artifact | Rows |",
            "|---|---:|",
        ]
    )
    for path_s in CSV_TABLES:
        p = ROOT / path_s
        if p.exists():
            lines.append(f"| `{path_s}` | {row_count(p)} |")

    lines.extend(
        [
            "",
            "## Source Evidence Appendices",
            "",
            "The integrated narrative above is the primary report body. The following appendices retain the original source reports in screening-module order so every claim remains auditable without presenting the work as separate standalone studies.",
        ]
    )
    for plan, paths in PLAN_REPORTS.items():
        lines.extend(["", "---", "", f"## {plan}", ""])
        for path_s in paths:
            p = ROOT / path_s
            if p.exists():
                add_source(lines, p, level=3)
            else:
                lines.extend(["", f"Missing source artifact: `{path_s}`", ""])

    lines.extend(
        [
            "",
            "---",
            "",
            "## Candidate Packet Appendices",
            "",
            "These appendices retain the wet-lab-facing and review packet details from the unified screen.",
        ]
    )
    for group, paths in packet_paths():
        lines.extend(["", "---", "", f"## {group}", ""])
        for p in paths:
            add_source(lines, p, level=3)

    lines.extend(
        [
            "",
            "---",
            "",
            "## Tabular Result Appendices",
            "",
            "The following CSV artifacts are embedded verbatim to preserve the candidate-level tabular evidence behind the integrated screen.",
        ]
    )
    for path_s in CSV_TABLES:
        p = ROOT / path_s
        if p.exists():
            add_tabular_source(lines, p)

    report_text = "\n".join(lines).rstrip() + "\n"
    OUT.write_text(report_text, encoding="utf-8")
    print(OUT)
    print(f"candidate_inventory_rows={len(inventory)}")
    print(f"line_count={len(report_text.splitlines())}")


if __name__ == "__main__":
    main()
