from __future__ import annotations

import csv
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "outputs" / "perusing_biological_datasets_report_package_2026-05-18"
ARCHIVE_DIR = PACKAGE_DIR / "candidate_archives"
REPORT_MD = PACKAGE_DIR / "Perusing_Biological_Datasets_Research_Report.md"


ARCHIVE_SPECS = [
    {
        "filename": "01_secondary_metabolite_bgc_candidate_archive.md",
        "label": "Plan 01 - Secondary Metabolite / BGC Candidate Archive",
        "description": "High-priority and top-50 strict BGC review packets for natural-product and antibiotic-lead follow-up hypotheses.",
        "patterns": [
            "outputs/plan01_strict_bgc_triage_2026-05-14/plan01_high_priority_validation_packets/*.md",
            "outputs/plan01_strict_bgc_triage_2026-05-14/plan01_top_50_strict_bgc_packets/*.md",
        ],
    },
    {
        "filename": "02_08_biocatalyst_extremophile_enzyme_candidate_archive.md",
        "label": "Plans 02/08 - Biocatalyst And Extremophile Enzyme Candidate Archive",
        "description": "High-precision and strict enzyme packets spanning the industrial biocatalyst screen and extremophile/release layer.",
        "patterns": [
            "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_high_precision_packets/*.md",
            "outputs/plan02_09_deep_strict_2026-05-14/lab_ready_candidate_packets/*.md",
        ],
    },
    {
        "filename": "03_nitrogen_cycle_candidate_archive.md",
        "label": "Plan 03 - Nitrogen-Cycle Candidate Archive",
        "description": "Nitrogen-fixation, N2O-reduction, urease/rhizosphere, and nitrate/nitrite transformation packets.",
        "patterns": ["outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/*.md"],
    },
    {
        "filename": "04_plant_growth_promotion_candidate_archive.md",
        "label": "Plan 04 - Plant-Growth-Promotion Genome Candidate Archive",
        "description": "Genome-level PGP wet-lab planning packets with trait, source, reference, and safety-context evidence.",
        "patterns": ["outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/*.md"],
    },
    {
        "filename": "05_natural_stability_candidate_archive.md",
        "label": "Plan 05 - Natural Stability Candidate Archive",
        "description": "Naturally stable homolog packets for salt, pH, and stress-condition enzyme hypotheses.",
        "patterns": ["outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/*.md"],
    },
    {
        "filename": "06_rare_chemistry_candidate_archive.md",
        "label": "Plan 06 - Rare-Chemistry Candidate Archive",
        "description": "Rare-chemistry enzyme packets for redox, organosulfur, rare-sugar, and dehalogenation hypotheses.",
        "patterns": ["outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/*.md"],
    },
    {
        "filename": "07_biomaterials_candidate_archive.md",
        "label": "Plan 07 - Biomaterials Candidate Archive",
        "description": "Biopolymer/EPS, protein-material, pigment, and BGC/material review packets.",
        "patterns": ["outputs/plan08_pre_wetlab_screen_2026-05-18/plan08_top_candidate_packets/*.md"],
    },
]


ATLAS_ARCHIVE = {
    "filename": "08_extremophile_atlas_archive.md",
    "label": "Plan 08 - Extremophile Enzyme Atlas Archive",
    "description": "Release-layer archive for the extremophile enzyme atlas and stability-feature score table.",
    "report": "outputs/plan09_release_metadata_stability_2026-05-17/PLAN09_RELEASE_METADATA_STABILITY_REPORT.md",
    "csv": "outputs/plan09_release_metadata_stability_2026-05-17/plan09_stability_feature_scores.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return path.stem


def demote_headings(text: str, levels: int = 1) -> str:
    out: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})(\s+.*)$", line)
        if m:
            out.append(f"{'#' * min(6, len(m.group(1)) + levels)}{m.group(2)}")
        else:
            out.append(line)
    return "\n".join(out)


def row_count(path: Path) -> int:
    with path.open(encoding="utf-8", errors="replace", newline="") as handle:
        return max(0, sum(1 for _ in csv.reader(handle)) - 1)


def packet_paths(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(sorted(ROOT.glob(pattern)))
    return paths


def write_packet_archive(spec: dict[str, object]) -> dict[str, object]:
    paths = packet_paths(spec["patterns"])  # type: ignore[arg-type]
    out_path = ARCHIVE_DIR / str(spec["filename"])
    lines = [
        f"# {spec['label']}",
        "",
        f"Generated: {dt.datetime.now().strftime('%Y-%m-%d')}",
        "",
        str(spec["description"]),
        "",
        "This archive preserves candidate-packet evidence for review. It is not a wet-lab protocol, synthesis instruction set, organism-release plan, or safety clearance.",
        "",
        f"Packet count: `{len(paths)}`",
        "",
        "## Packet Index",
        "",
        "| # | Packet | Source path |",
        "|---:|---|---|",
    ]
    for idx, path in enumerate(paths, 1):
        lines.append(f"| {idx} | {first_heading(path)} | `{rel(path)}` |")

    lines.extend(["", "## Full Packet Text", ""])
    for idx, path in enumerate(paths, 1):
        lines.extend(
            [
                "",
                "---",
                "",
                f"## Packet {idx}: {first_heading(path)}",
                "",
                f"Source: `{rel(path)}`",
                "",
                demote_headings(path.read_text(encoding="utf-8", errors="replace").strip(), levels=2),
                "",
            ]
        )

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"label": spec["label"], "path": out_path, "count": len(paths), "description": spec["description"]}


def write_atlas_archive() -> dict[str, object]:
    out_path = ARCHIVE_DIR / ATLAS_ARCHIVE["filename"]
    report_path = ROOT / ATLAS_ARCHIVE["report"]
    csv_path = ROOT / ATLAS_ARCHIVE["csv"]
    rows = row_count(csv_path)

    preview_lines: list[str] = []
    with csv_path.open(encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        preview = [next(reader) for _ in range(25)]
    preview_lines.append("| " + " | ".join(header) + " |")
    preview_lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for row in preview:
        preview_lines.append("| " + " | ".join(row) + " |")

    lines = [
        f"# {ATLAS_ARCHIVE['label']}",
        "",
        f"Generated: {dt.datetime.now().strftime('%Y-%m-%d')}",
        "",
        str(ATLAS_ARCHIVE["description"]),
        "",
        "This archive indexes the full atlas table rather than duplicating every row into Markdown. The full CSV remains the authoritative archive artifact.",
        "",
        f"Full atlas CSV: `{rel(csv_path)}`",
        f"Atlas rows: `{rows}`",
        "",
        "## Source Report",
        "",
        demote_headings(report_path.read_text(encoding="utf-8", errors="replace").strip(), levels=1),
        "",
        "## First 25 Stability-Feature Rows",
        "",
        *preview_lines,
        "",
    ]
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"label": ATLAS_ARCHIVE["label"], "path": out_path, "count": rows, "description": ATLAS_ARCHIVE["description"]}


def archive_table(archive_infos: list[dict[str, object]]) -> list[str]:
    lines = ["| Archive | Contents | Records |", "|---|---|---:|"]
    for info in archive_infos:
        rel_path = rel(info["path"])  # type: ignore[arg-type]
        lines.append(f"| `{rel_path}` | {info['description']} | {info['count']} |")
    return lines


def write_archive_index(archive_infos: list[dict[str, object]]) -> Path:
    index_path = ARCHIVE_DIR / "00_CANDIDATE_ARCHIVE_INDEX.md"
    packet_total = sum(int(info["count"]) for info in archive_infos if "Extremophile Enzyme Atlas" not in str(info["label"]))
    lines = [
        "# Candidate Archive Index",
        "",
        f"Generated: {dt.datetime.now().strftime('%Y-%m-%d')}",
        "",
        "This directory separates the candidate evidence from the polished research report. The archives preserve pre-wet-lab candidate packet text and source paths, while the main report stays short enough for grant or collaborator review.",
        "",
        f"Packetized candidate records across archives: `{packet_total}`",
        f"Extremophile atlas rows indexed separately: `{archive_infos[-1]['count']}`",
        "",
        "## Archives",
        "",
        *archive_table(archive_infos),
        "",
        "## Claim Boundary",
        "",
        "These archives preserve computational candidate evidence. They should not be treated as validated activity claims, safety determinations, expression-ready instructions, field-use proposals, or product claims.",
        "",
    ]
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


def write_research_report(archive_infos: list[dict[str, object]], archive_index: Path) -> None:
    lines = [
        "# Perusing Biological Datasets",
        "",
        "## Abstract",
        "",
        "This report describes a single computational genomics discovery campaign that prioritized biological candidates from heterogeneous public and local datasets. The campaign used eight screening modules, but the modules functioned as one staged process: assemble candidate universes, assign biological function and context, apply domain-specific evidence gates, harden novelty and safety claims, and package only bounded hypotheses for expert wet-lab discussion. The supporting appendix preserves the complete technical record, while this report summarizes the integrated workflow, screening differences, most defensible candidate classes, and remaining validation gaps.",
        "",
        "The campaign produced computationally prioritized hypotheses spanning secondary-metabolite biosynthetic gene clusters, industrial and extremophile enzymes, nitrogen-cycle pathways, plant-growth-promotion genomes, naturally stable enzyme homologs, rare-chemistry enzymes, and microbial biomaterial systems. The strongest outputs are three BGC keep candidates for natural-product/antibiotic-lead review, two current enzyme bridge leads, six nitrogen-cycle pathway packets, one cleanest PGP genome lead plus three lower-confidence PGP hypotheses, four naturally stable enzyme homologs, four rare-chemistry enzyme hypotheses, six immediate biomaterial candidates plus three BGC/material review holds, and a 4,071-row extremophile enzyme atlas.",
        "",
        "All findings remain computational and pre-wet-lab. The report does not claim validated antibiotic activity, validated enzyme activity, nitrogen flux, plant-growth benefit, material production, organism safety, field readiness, or product performance. The intended use is prioritization: deciding which hypotheses deserve expert review, controlled validation planning, and later experimental testing.",
        "",
        "## Report Package",
        "",
        "| Artifact | Role |",
        "|---|---|",
        "| `outputs/Perusing_Biological_Datasets.md` | Full supporting technical appendix in Markdown |",
        "| `outputs/perusing_latex_build/Perusing_Biological_Datasets.pdf` | Compiled 325-page supporting appendix PDF |",
        f"| `{rel(archive_index)}` | Index for separated candidate archives |",
        "| This report | Grant/collaborator-facing synthesis capped below 40 compiled pages |",
        "",
        "## Integrated Screening Design",
        "",
        "The campaign was organized around a common decision standard rather than a common biological endpoint. Each module asked whether a candidate had enough computational support to justify a bounded, testable hypothesis. The evidence used to answer that question varied by biology: BGC structure and dereplication for secondary metabolites, enzyme-family and active-site evidence for biocatalysts, marker/pathway coherence for nitrogen cycling, genome-level trait coherence for PGP candidates, stability-axis evidence for natural homologs, ligand or reaction-family context for rare chemistry, and material-pathway/domain evidence for biomaterials.",
        "",
        "The screen had four shared stages. First, candidate universes were assembled from genome, gene, BGC, annotation, marker, source-metadata, and release artifacts. Second, candidates were scored or gated for functional plausibility. Third, candidates were hardened against common false-positive modes: generic annotations, housekeeping pathways, incomplete domains, weak boundaries, low genome quality, lack of source context, poor recovery path, and local computational safety flags. Fourth, candidates were sorted into immediate pre-wet-lab packets, review holds, or archive-only evidence.",
        "",
        "This framing matters because the project is not eight unrelated studies. It is one reusable computational prioritization system tested across eight biological question types. The plan-by-plan differences are the screening lenses, not the overall process.",
        "",
        "## Screening Differences",
        "",
        "| Report plan | Screening lens | Main evidence gates | Output role |",
        "|---|---|---|---|",
        "| 01 | Secondary-metabolite/BGC discovery | antiSMASH/GECCO/SanntiS support, BGC boundary review, MIBiG/BiG-SCAPE dereplication, product-class lookup, safety/context checks | Natural-product and antibiotic-lead review hypotheses |",
        "| 02 | Industrial biocatalyst discovery | Enzyme-family assignment, active-site plausibility, Pfam/UniRef recovery, structure/pocket checks, family-level assay precedent | Lab-ready and expert-review enzyme queues |",
        "| 03 | Nitrogen-cycle pathway discovery | Marker/pathway coherence, representative protein support, genome/source context, IQ-TREE phylogeny update | Nitrogen-cycle phenotype hypotheses |",
        "| 04 | Plant-growth-promotion genomes | Trait co-occurrence, reference ANI, strain dereplication, isolate/culture path, safety/context filters | PGP genome hypotheses |",
        "| 05 | Natural stability discovery | Stability-axis scoring, structure models, loop/disorder and energy proxies, IQ-TREE context, ThermoMPNN aggregate summaries | Naturally stable enzyme homolog hypotheses |",
        "| 06 | Rare chemistry discovery | Rare-function annotations, Rhea/EC consistency, structural plausibility, ligand-pocket comparison, phylogenetic context | Redox, organosulfur, rare-sugar, and dehalogenation hypotheses |",
        "| 07 | Biomaterials discovery | PHA/EPS/protein-material/pigment/BGC evidence, export/recovery context, material subtype scoring, unresolved-chemistry triage | Immediate biomaterial candidates plus BGC review packets |",
        "| 08 | Extremophile enzyme atlas | Metadata-linked stress context, stability-feature scoring, high-precision enzyme crosswalk, release-readiness organization | Traceable atlas supporting enzyme prioritization |",
        "",
        "## Results",
        "",
        "### Plan 01: Secondary-Metabolite BGC Discovery",
        "",
        "Plan 01 produced a three-candidate keep set after integrating whole-MAG antiSMASH, within-region BiG-SCAPE, targeted-MIBiG comparisons, full-MIBiG comparisons, product-class lookup, and boundary/domain review. The three strongest BGC hypotheses are retained for expert natural-product review, including antibiotic-lead discussion where appropriate, but none are validated antimicrobial candidates.",
        "",
        "| Candidate | Product frame | Strongest computational support | Claim boundary |",
        "|---|---|---|---|",
        "| `MGYG000517341:MGYG000517341_17:38631-49536` | RiPP-like | Whole-MAG antiSMASH support; no close targeted/full MIBiG BiG-SCAPE link at 0.3/0.5 cutoffs | Product identity and activity unvalidated |",
        "| `MGYG000473561:MGYG000473561_12:259192-267836` | T3PKS / SanntiS-polyketide | High sequence novelty; no close targeted/full MIBiG BiG-SCAPE link at 0.3/0.5 cutoffs | Chemistry and bioactivity unvalidated |",
        "| `MGYG000517341:MGYG000517341_21:36974-66085` | Betalactone | Whole-MAG antiSMASH support; no close targeted/full MIBiG BiG-SCAPE link at 0.3/0.5 cutoffs | Product formation and novelty remain computational |",
        "",
        "Four additional BGCs remain computational holds because newer dereplication layers did not resolve domain or contig-edge blockers. This is a useful result: the screen did not simply promote high-scoring BGCs; it rejected or held candidates when boundaries or biosynthetic logic were weak.",
        "",
        "### Plans 02 And 08: Enzyme Discovery And Extremophile Atlas",
        "",
        "The enzyme screen produced broad high-precision and strict review queues, then narrowed current bridge attention to a dehalogenase and a glycosidase. The extremophile atlas added release metadata, checksum/provenance structure, and a stability-feature model over 4,071 high-precision rows. Together, these modules form the activity-first enzyme discovery and atlas layer of the campaign.",
        "",
        "| Candidate or layer | Role | Current interpretation | Main limitation |",
        "|---|---|---|---|",
        "| `MGYG000527579_00796` | Dehalogenase bridge lead | Stronger current enzyme bridge candidate; direct structure support and active-site lock with mechanistic review note | Activity and substrate scope unvalidated |",
        "| `MGYG000517010_03432` | Glycosidase bridge lead | Retained if full-length structure limitation is accepted; motif support in candidate-specific chunks | Full-length structure/domain orientation unresolved |",
        "| 4,071-row extremophile atlas | Release/stability prioritization layer | Traceable table for stress-associated enzyme prioritization | Stability-feature scores are heuristics, not measurements |",
        "",
        "The enzyme/atlas result is useful for monetization and partnership discussions because enzyme assays can often be staged cleanly, but the safe claim is still prioritization, not product performance.",
        "",
        "### Plan 03: Nitrogen-Cycle Pathway Discovery",
        "",
        "Plan 03 reviewed 655 first-pass nitrogen-cycle hits and rebuilt the ranking around marker specificity, pathway completeness, genomic neighborhood, source context, genome quality, and safety/practicality gates. Six candidates advanced to immediate pre-wet-lab packets.",
        "",
        "| Rank | Candidate | Track | Representative marker | Score |",
        "|---:|---|---|---|---:|",
        "| 1 | `PLAN03:MGYG000517341:nitrogen_fixation:MGYG000517341_00816` | Nitrogen fixation | `nifH` | 91.90 |",
        "| 2 | `PLAN03:MGYG000478572:n2o_reduction:MGYG000478572_00459` | N2O reduction | `nosZ` | 91.61 |",
        "| 3 | `PLAN03:MGYG000473561:n2o_reduction:MGYG000473561_03510` | N2O reduction | `nosZ` | 91.25 |",
        "| 4 | `PLAN03:MGYG000511828:urea_rhizosphere:MGYG000511828_04091` | Urea/rhizosphere nitrogen | `ureC` | 87.70 |",
        "| 5 | `PLAN03:MGYG000517341:urea_rhizosphere:MGYG000517341_01850` | Urea/rhizosphere nitrogen | `ureC` | 86.42 |",
        "| 6 | `PLAN03:MGYG000511829:nitrate_nitrite_transformation:MGYG000511829_04732` | Nitrate/nitrite transformation | `narG/napA` | 80.72 |",
        "",
        "The IQ-TREE update strengthened the marker-family layer for `narG/napA`, `nifH`, and `ureC`; `nosZ` completed with only three local finalist-family sequences and therefore remains topology/bookkeeping support rather than a deep novelty claim. Nitrification/ammonia-oxidation calls were held because AMO/pMMO identity and full pathway support were not clean enough.",
        "",
        "### Plan 04: Plant-Growth-Promotion Genome Discovery",
        "",
        "Plan 04 evaluated plant-associated genome and MAG candidates as organism-level PGP hypotheses. The strongest result is one practical lead, not a validated plant-growth organism.",
        "",
        "| Candidate | Primary trait frame | Interpretation | Practical status |",
        "|---|---|---|---|",
        "| `MGYG000517341` | Osmoprotection/stress-associated PGP | Strongest hypothesis; high-quality tomato/rhizosphere/stress context, multi-trait architecture, safety-context pass, exact/same-species ANI support | Cleanest organism-level candidate |",
        "| `MGYG000535629` | Siderophore/Bacteriovorax-linked PGP | Useful barley-rhizosphere hypothesis, but only distant genus-level reference context | Lower-confidence hypothesis |",
        "| `MGYG000535630` | Antifungal BGC/rhizosphere | Interesting source and trait context, but weak selected-reference gate | Organism-level hold |",
        "| `MGYG000511828` | Phosphate-solubilization | Coherent trait hypothesis with weaker source/culture route | Organism-level hold |",
        "",
        "This module is consequential for agricultural framing, but its claims must remain conservative. Genome-level trait coherence can justify controlled tests; it cannot establish plant growth promotion, root colonization, crop benefit, ecological behavior, or release safety.",
        "",
        "### Plan 05: Natural Stability Enzyme Discovery",
        "",
        "Plan 05 converted the enzyme universe into a stability-first screen for naturally stable homologs. A focused pool of 3,237 enzyme candidates was filtered to 19 natural-stability shortlist candidates, 19 strict bridge candidates, six strict advance calls, and four immediate wet-lab planning packets.",
        "",
        "| Rank | Candidate | Family | Axis | Interpretation |",
        "|---:|---|---|---|---|",
        "| 1 | `MGYG000478572_00760` | Esterase | Salt | Cleanest near-term stability lead; strong structure confidence and low expression-risk profile |",
        "| 2 | `MGYG000517341_01521` | Dehalogenase | Salt | Attractive but higher flexible-region/structure-confidence caveat |",
        "| 3 | `MGYG000518629_02280` | Esterase | pH | Divergent esterase-like pH-axis candidate with expression-design uncertainty |",
        "| 4 | `MGYG000478572_01589` | Transaminase | Salt | Strong structure confidence and salt-axis score, with PLP/cofactor complexity |",
        "",
        "The final hardening pass added candidate-specific structures, IQ-TREE3 phylogenies, loop/disorder comparison, charge/salt-bridge proxies, ThermoMPNN aggregate summaries, and benchmark framing. These layers make Plan 05 the cleanest enzyme wet-lab package, but they still do not validate activity or stability.",
        "",
        "### Plan 06: Rare-Chemistry Enzyme Discovery",
        "",
        "Plan 06 intentionally targeted less common or underexplored chemistry rather than only standard high-confidence enzyme families. The bridge reduced 11,805 candidates to a 300-candidate priority queue, 40 strict bridge candidates, 16 downselected candidates, and four immediate wet-lab planning candidates.",
        "",
        "| Rank | Candidate | Class | Interpretation | Main caveat |",
        "|---:|---|---|---|---|",
        "| 1 | `MGYG000478572_02342` | Redox | Strongest all-around rare-chemistry package with reaction-family and pocket support | Cofactor/partner dependency |",
        "| 2 | `MGYG000521810_01693` | Organosulfur | Coherent sulfurtransferase/rhodanese-like hypothesis from hydrothermal context | Signal-like region and partial pocket context |",
        "| 3 | `MGYG000478572_01361` | Rare sugar | Novel epimerase/dehydratase-like hypothesis | Substrate specificity and pocket context unresolved |",
        "| 4 | `MGYG000517233_02445` | Dehalogenation | Lowest expression-risk finalist with excellent structural confidence | Manual pocket review needed before substrate claims |",
        "",
        "This module is high-upside but more speculative than Plans 02 and 05. It should be presented as a rare-chemistry hypothesis generator with experimentally testable leads, not as a substrate-specific enzyme package.",
        "",
        "### Plan 07: Biomaterials Discovery",
        "",
        "Plan 07 started from 731 first-pass biomaterials hits and added genome-quality, source-environment, recovery, BGC, and safety-context gates. The immediate packet set contains six candidates; three BGC/material candidates are retained as review holds because product chemistry is unresolved.",
        "",
        "| Candidate | Track | Subtype | Status |",
        "|---|---|---|---|",
        "| `MGYG000517341_02043` | Biopolymers/EPS | PHA/polyhydroxyalkanoate | Immediate packet |",
        "| `MGYG000478572_01331` | Biopolymers/EPS | EPS/capsule export | Immediate packet |",
        "| `MGYG000517341_00932` | Biopolymers/EPS | EPS/capsule export | Immediate packet |",
        "| `MGYG000517341_02173` | Protein materials | Surface adhesive protein | Immediate packet |",
        "| `MGYG000521810_02082` | Protein materials | Surface adhesive protein | Immediate packet |",
        "| `MGYG000517341_02282` | Pigments/materials | Tyrosinase/melanin-like | Immediate packet |",
        "| `MGYG000517341:MGYG000517341_27:9851-55107` | Biosurfactant/BGC | NRP/lipopeptide-like review | Review hold |",
        "| `MGYG000517341:MGYG000517341_2:234333-279288` | Biosurfactant/BGC | NRP/lipopeptide-like review | Review hold |",
        "| `MGYG000521810:MGYG000521810_13:25308-46111` | Biosurfactant/BGC | Hserlactone BGC review | Review hold |",
        "",
        "The important methodological result is that generic surface, transporter, metal-binding, and housekeeping envelope annotations no longer dominate the top list. The screen now prioritizes coherent PHA/EPS loci, surface-adhesion protein hypotheses, and the single pigment/material candidate while holding unresolved BGC chemistry.",
        "",
        "## Cross-Campaign Interpretation",
        "",
        "The strongest near-term experimental packages are not necessarily the most societally consequential. Plan 05 is the cleanest computational-to-wet-lab enzyme package because its finalists have layered structure, phylogeny, stability-proxy, and safety/context evidence. Plan 02 has the clearest activity-first enzyme bridge lead in `MGYG000527579_00796`. Plan 04 has the clearest organism-level practical lead in `MGYG000517341`, but organism-level PGP claims require much more downstream validation. Plan 01 and Plan 06 may have high discovery upside, but chemistry and product-identity uncertainty make them more speculative. Plan 03 is societally important because nitrogen cycling and N2O reduction are consequential, but the screen supports pathway hypotheses rather than environmental performance. Plan 07 is attractive for materials partnerships but needs product or property validation before impact claims.",
        "",
        "## Candidate Archives",
        "",
        "The detailed candidate evidence has been separated from the main report. This keeps the report readable while preserving traceability.",
        "",
        *archive_table(archive_infos),
        "",
        "## Validation And Claim Boundaries",
        "",
        "The appropriate next step is expert review and controlled validation planning, not broad product or field claims. For enzymes, the first blockers are expression, soluble recovery, baseline activity, substrate scope, and stress-condition behavior. For BGCs, the blockers are product formation, product identity, dereplication at the chemistry level, and activity. For nitrogen-cycle and PGP candidates, the blockers are organism recovery, phenotype measurement, plant or process relevance, and safety review. For biomaterials, the blockers are product formation, material identity, yield, recoverability, and measured material properties.",
        "",
        "No candidate should be described as validated until experimental data support that specific claim. The strongest truthful framing is that this campaign produced a multi-domain, evidence-preserving computational prioritization system and a set of bounded pre-wet-lab hypotheses with explicit uncertainty labels.",
        "",
        "## Conclusion",
        "",
        "Perusing Biological Datasets is best framed as an integrated computational genomics screen that turns heterogeneous biological data into traceable, review-ready candidate hypotheses. The campaign is broad enough to support grant and collaboration narratives, but the claims remain bounded: discovery prioritization, candidate triage, and wet-lab planning support. The full 325-page appendix and the separate candidate archives preserve the detailed evidence; this report provides the concise research narrative suitable for external review.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_infos = [write_packet_archive(spec) for spec in ARCHIVE_SPECS]
    archive_infos.append(write_atlas_archive())
    archive_index = write_archive_index(archive_infos)
    write_research_report(archive_infos, archive_index)
    print(REPORT_MD)
    print(archive_index)
    print(f"archive_count={len(archive_infos)}")
    print(f"packet_archived_records={sum(int(info['count']) for info in archive_infos[:-1])}")
    print(f"atlas_rows={archive_infos[-1]['count']}")


if __name__ == "__main__":
    main()
