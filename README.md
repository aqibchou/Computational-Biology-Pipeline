# Perusing Biological Datasets: What This Project Found

This is the top-level README for the Computational Biology Pipeline repository. The repository is now laid out from the default GitHub directory: completed plan documents live at the root, reusable scripts live in `scripts/`, and the report package lives in `outputs/`.

This project started with a simple question: can public genomics datasets be mined hard enough to produce real, traceable, wet-lab-worthy biological candidates?

The answer from this computational run is yes. Across the completed genomics plans, this work found novel wet-lab candidates in every screened category: natural-product gene clusters, industrial enzymes, nitrogen-cycle pathways, plant-growth-promotion genomes, naturally stable enzyme homologs, rare-chemistry enzymes, biomaterials, and an extremophile enzyme atlas.

These are computational discoveries, not validated wet-lab results yet. In this writeup, "novel wet-lab candidate" means a candidate that survived the computational filters well enough to justify expert review and experimental testing. It does not mean the candidate has already been shown to work in the lab. That distinction matters, but the results are still exciting: the project turned broad biological datasets into a concrete candidate portfolio.

## The Short Version

The completed campaign produced:

- 3 strong secondary-metabolite / natural-product BGC candidates.
- 2 current industrial enzyme bridge leads, plus larger strict and high-precision enzyme queues.
- 6 nitrogen-cycle pathway candidates.
- 4 plant-growth-promotion genome hypotheses, with one especially clean organism-level lead.
- 4 natural enzyme homologs prioritized for stress-condition / stability testing.
- 4 rare-chemistry enzyme candidates.
- 6 immediate biomaterial candidates, plus 3 BGC/material review holds.
- A 4,071-row extremophile enzyme atlas for future stability-focused screening.

The most exciting part is the breadth. This was not one narrow screen. The same general evidence workflow was adapted across very different biological problems, and each module still produced candidates worth keeping.

## How The Search Worked

The workflow was built around a repeated pattern:

1. Start with a broad candidate universe from public genome, gene, protein, BGC, pathway, or metadata resources.
2. Assign a biological hypothesis using the strongest available annotations.
3. Remove obvious false positives and generic annotation hits.
4. Add context: source environment, genome quality, pathway neighborhood, dereplication, structure, phylogeny, safety-context notes, or provenance.
5. Downselect to candidates that are specific enough to test.
6. Archive the evidence so every candidate can be traced back to the files that produced it.

This matters because genomics data is noisy. A generic enzyme annotation can look more useful than it is. A nitrogen marker can be a false positive. A BGC can look complete when the boundary is weak. A biomaterial-like keyword can be housekeeping biology. The main achievement here was not just finding candidates; it was filtering aggressively enough that the surviving candidates are easier to explain and test.

## Plan 01: Natural Products And BGCs

Plan 01 searched for secondary-metabolite biosynthetic gene clusters that could be interesting for natural-product discovery and future antibiotic-lead exploration.

The screen found 3 strong BGC candidates:

- `MGYG000517341:MGYG000517341_17:38631-49536`: RiPP-like BGC candidate with no close full-MIBiG BiG-SCAPE link at the tested cutoffs.
- `MGYG000473561:MGYG000473561_12:259192-267836`: T3PKS / polyketide-like BGC candidate with high sequence-novelty context.
- `MGYG000517341:MGYG000517341_21:36974-66085`: betalactone-like BGC candidate with no close full-MIBiG BiG-SCAPE link at the tested cutoffs.

The final keep candidates survived whole-MAG antiSMASH support, boundary review, product-class review, MIBiG/BiG-SCAPE dereplication, and safety-context checks. Four other candidates were held because their boundary or domain logic was not clean enough, which makes the final three more credible.

What comes next: chemistry-first validation. The next question is whether these BGCs produce detectable compounds, whether those compounds are novel at the chemistry level, and whether any product has useful bioactivity.

## Plan 02: Industrial Biocatalyst Discovery

Plan 02 searched for enzyme candidates that could become useful industrial biocatalyst leads.

The broad screen produced strict and high-precision enzyme queues across dehalogenases, glycosidases, lipases, proteases, esterases, transaminases, nitrilases, cellulases, xylanases, peroxidases, and related families. From that larger universe, two current bridge leads stood out:

- `MGYG000527579_00796`: dehalogenase candidate. This is the cleanest activity-first enzyme lead. It has strong structure support, active-site context, and a clear family hypothesis.
- `MGYG000517010_03432`: glycosidase candidate. This is a strong secondary lead with full-length structure support and useful pocket geometry, but it needs expert catalytic-residue review before it is as clean as the dehalogenase.

The best candidates were selected because annotation, family evidence, structure, pocket logic, novelty, and safety-context review converged.

What comes next: expression, soluble recovery, activity assays, substrate-scope testing, and kinetics.

## Plan 03: Nitrogen-Cycle Pathway Discovery

Plan 03 searched for candidates connected to nitrogen fixation, nitrous oxide reduction, urea/rhizosphere nitrogen cycling, and nitrate/nitrite transformation.

The final screen advanced 6 nitrogen-cycle candidates:

- `MGYG000517341_00816`: nifH nitrogen-fixation candidate from genome `MGYG000517341`.
- `MGYG000478572_00459`: nosZ nitrous-oxide-reduction candidate from genome `MGYG000478572`.
- `MGYG000473561_03510`: nosZ nitrous-oxide-reduction candidate from genome `MGYG000473561`.
- `MGYG000511828_04091`: ureC alpha urea/rhizosphere nitrogen candidate from genome `MGYG000511828`.
- `MGYG000517341_01850`: ureC alpha urea/rhizosphere nitrogen candidate from genome `MGYG000517341`.
- `MGYG000511829_04732`: narG/napA nitrate/nitrite transformation candidate from genome `MGYG000511829`.

Nitrogen cycling is one of the most societally important parts of the whole project. These candidates point toward questions about nitrogen availability, N2O reduction, rhizosphere nitrogen transformations, and fertilizer-linked biology. The screen also made strong negative calls by rejecting weak AMO/pMMO-like nitrification candidates instead of forcing them through.

What comes next: controlled tests for marker expression, pathway activity, nitrogen transformation, and phenotype-level effects.

## Plan 04: Plant-Growth-Promotion Genome Discovery

Plan 04 searched for plant-growth-promotion genome hypotheses. This plan is different from the single-gene enzyme screens because the candidate is an organism-level hypothesis.

The screen found 4 PGP genome candidates:

- `MGYG000517341`: the cleanest lead. It has tomato/rhizosphere relevance, strong genome quality, osmoprotection and stress-associated trait architecture, reference support, and safety-context support.
- `MGYG000535629`: siderophore-linked PGP hypothesis in a Bacteriovorax context.
- `MGYG000535630`: antifungal-BGC-linked rhizosphere hypothesis.
- `MGYG000511828`: phosphate-solubilization genome hypothesis.

`MGYG000517341` became one of the most practical and consequential candidates in the whole project. It is an isolate from tomato rhizosphere, has 100.0 percent completeness and 0.21 percent contamination, contains seven supported PGP trait classes, and matched public reference material with exact fastANI/skani support. If this performs in controlled plant-association assays, it could matter for plant stress resilience and agricultural microbiome work.

What comes next: organism access, trait expression, plant-association testing, greenhouse-style validation, and formal safety review.

## Plan 05: Natural Enzyme Stability

Plan 05 searched for naturally occurring enzyme homologs that may be worth testing under stress conditions such as salt or pH.

The screen found 4 immediate natural-stability candidates:

- `MGYG000478572_00760`: salt-axis esterase candidate and the cleanest near-term Plan 05 lead.
- `MGYG000517341_01521`: salt-axis dehalogenase candidate with useful novelty and structure support.
- `MGYG000518629_02280`: pH-axis esterase-like candidate.
- `MGYG000478572_01589`: salt-axis transaminase candidate with strong structure support and cofactor complexity.

The finalists have sequence novelty, family support, candidate-specific structures, IQ-TREE phylogeny, loop/disorder comparison, charge/salt-bridge proxy context, ThermoMPNN aggregate summaries, and safety-context review. That is a lot of converging evidence for a first-pass enzyme testing set.

What comes next: expression, activity measurement, and stress-condition panels to test whether these natural homologs actually retain function under the predicted conditions.

## Plan 06: Rare-Chemistry Enzyme Discovery

Plan 06 searched for enzymes with rare or underexplored reaction-family hypotheses.

The screen found 4 rare-chemistry candidates:

- `MGYG000478572_02342`: redox candidate from saline marine `Marinobacter salinexigens`.
- `MGYG000521810_01693`: organosulfur / sulfurtransferase-like candidate from hydrothermal marine sediment `Guyparkeria hydrothermalis`.
- `MGYG000478572_01361`: rare-sugar candidate from saline marine `Marinobacter salinexigens`.
- `MGYG000517233_02445`: dehalogenation-class candidate from desert/rhizosphere `Desertivirga`.

 Rare chemistry is harder to validate and easier to overinterpret, but the final candidates survived reaction-family mapping, reviewed-homolog context, MSA review, structure confidence, phylogeny, dependency flags, and pocket review. These are exactly the kinds of candidates that could become interesting if even one passes a baseline assay.

What comes next: manual mechanism review, expression, cofactor/dependency checks, baseline reaction readouts, and substrate-specific testing.

## Plan 07: Biomaterials And Biopolymers

Plan 07 searched for microbial biomaterial candidates across biopolymer/EPS, protein-material, pigment/material, and BGC/material tracks.

The screen found 6 immediate biomaterial candidates:

- `MGYG000517341_02043`: PHA / polyhydroxyalkanoate candidate.
- `MGYG000478572_01331`: EPS / capsule export candidate.
- `MGYG000517341_00932`: EPS / capsule export candidate.
- `MGYG000517341_02173`: surface adhesive protein candidate.
- `MGYG000521810_02082`: surface adhesive protein candidate.
- `MGYG000517341_02282`: tyrosinase / melanin-like pigment candidate.

It also retained 3 BGC/material review holds:

- `MGYG000517341:MGYG000517341_27:9851-55107`: NRP/lipopeptide-like BGC review hold.
- `MGYG000517341:MGYG000517341_2:234333-279288`: NRP/lipopeptide-like BGC review hold.
- `MGYG000521810:MGYG000521810_13:25308-46111`: hserlactone BGC review hold.

The biomaterials screen produced multiple classes of testable material hypotheses. It also filtered out a lot of false positives, especially generic lipid-A/LPS and broad surface-protein annotations that should not be treated as real biosurfactant or material evidence. The remaining set is much more practical for targeted product-identity and material-property testing.

What comes next: product formation, product identity, recoverability, yield, rheology, coating/adhesion behavior, pigment identity, and material performance.

## Plan 08: Extremophile Enzyme Atlas

Plan 08 organized the enzyme work into a reusable atlas.

The result is a 4,071-row extremophile enzyme atlas with source manifests, row counts, checksums, high-precision enzyme links, extremophile metadata, and stability-feature scores. It includes tracks such as desiccation glycosidases, heat-pressure glycosidases, desiccation esterases, desiccation dehalogenases, desiccation proteases, desiccation lipases, desiccation cellulases, heat-pressure nitrilases, desiccation xylanases, heat-pressure proteases, heat-pressure esterases, and salt glycosidases.

Top stability-feature examples include cellulase candidates such as `MGYG000502387_01211`, `MGYG000517010_00514`, `MGYG000517010_00658`, and related high-priority desiccation-track rows.

What comes next: selecting small experimental panels from the atlas and testing actual expression, activity, and stress tolerance.

## What I Think Is Most Important

The most mature near-term wet-lab package is Plan 05, because the natural-stability enzyme candidates have the most complete computational-to-experimental bridge.

The strongest single activity-first enzyme lead is the Plan 02 dehalogenase `MGYG000527579_00796`.

The most practical organism-level lead is the Plan 04 PGP candidate `MGYG000517341`.

The highest-upside discovery spaces are Plan 01 and Plan 06, because natural products and rare chemistry can produce very valuable hits if even one candidate validates.

The most societally consequential directions are Plan 03 and Plan 04, because nitrogen cycling, nitrous oxide reduction, fertilizer-linked biology, plant stress tolerance, and rhizosphere microbiomes are major agricultural and climate-linked problems.

The most partnership-friendly product area may be Plan 07, because biomaterial candidates can be tested with relatively intuitive product-identity and performance assays.

## Where The Evidence Lives

The detailed evidence is preserved in the report package:

- Main detailed report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive index: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/00_CANDIDATE_ARCHIVE_INDEX.md`
- Candidate archives: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/`
- PDF version: `outputs/perusing_biological_datasets_report_package_2026-05-18/pdf_build/Perusing_Biological_Datasets_Research_Report_Detailed.pdf`

The archive contains 187 packetized candidate records plus the 4,071-row extremophile atlas index.

For a file-by-file index of the completed plan documents and supporting package, see `PROJECT_INDEX.md`.

## Bottom Line

This repository documents a computational genomics discovery campaign that found novel wet-lab candidates across every completed plan. The candidates are not proven biological products yet, but they are real, traceable, evidence-backed starting points for wet-lab follow-up.

That is the point of this project: take messy public biological data, screen it carefully, remove the obvious noise, and produce a candidate portfolio that is exciting enough to test and organized enough to audit.
