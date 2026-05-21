# Plan 04 Pre-Wet-Lab Screen Plan

Date: 2026-05-17

## Objective

Complete a rigorous pre-wet-lab computational screen for Plan 04, plant-growth-promoting microbiome discovery, using the same narrowing discipline that worked for Plans 01, 02, 06, 07, and 09.

The goal is not to claim plant-growth benefit. The goal is to move from a noisy first-pass candidate table to a small, defensible set of 3-5 wet-lab planning candidates with clear hypotheses, source context, trait evidence, safety screening, and assay handoff logic.

## What The Finished Plans Did

The completed plans all used the same narrowing pattern:

1. Start from a broad computational candidate table.
2. Remove obvious false positives with strict target-specific rules.
3. Build a balanced review queue rather than simply sorting by raw score.
4. Run novelty or dereplication checks against reviewed references.
5. Add candidate-specific manual evidence, including domains, neighborhoods, MSAs, structure proxies, safety, and expression or feasibility checks where relevant.
6. Downselect to roughly 10-20 strong candidates.
7. Finalize 3-5 wet-lab planning candidates with packets, a report, and a completion audit.

Completed-plan precedents:

- Plan 01 narrowed GO BGCs to 3 advance candidates using domain logic, MIBiG/core BLAST, safety screening, edge/completeness review, and feasibility ranking.
- Plan 02/09 narrowed 40 lab-ready enzyme candidates to a top 5 using Swiss-Prot reciprocal search, MSA, catalytic support, AlphaFold availability, and expression risk.
- Plan 06 narrowed 3,237 focused rows to 19 strict candidates and 4 wet-lab candidates.
- Plan 07 narrowed 11,805 first-pass candidates to 300, then 40, then 16, then 4 wet-lab candidates.

## Current Plan 04 State

The current Plan 04 first-pass output contains 12,676 raw rows. This table is useful as a discovery substrate but too noisy for wet-lab planning.

Main issues:

- The current first pass includes contexts outside the Plan 04 priority surface, including gut, hydrothermal, polar, marine, and generic saline environments.
- The genuinely relevant local source set is mainly rhizosphere, soil, and desert plant/rhizosphere data, about 4,726 raw hits from 9 relevant MAGs.
- The current table is dominated by `phosphate_solubilization` hits because the keyword screen catches broad terms such as phosphate, kinase, phosphotransferase, PLP enzymes, and housekeeping genes.
- Existing evidence packets are protein-level keyword packets, not genome/MAG-level plant-benefit dossiers.

Therefore Plan 04 should not be completed by sorting the current score column. It needs a genome-level, multi-trait bridge.

## Implementation Target

Implement a dedicated bridge script:

```text
scripts/run_plan04_pgp_bridge.py
```

Write outputs to a dated directory:

```text
Research Directions/genomics_experiment_research_plans/outputs/plan04_pgp_bridge_YYYY-MM-DD/
```

The bridge should reuse:

- `outputs/computational_execution_2026-05-14/04_plant_growth_promoting_microbiome_discovery/candidates.csv`
- `outputs/computational_execution_2026-05-14/source_genomes.csv`
- cached MGnify genome annotations under `outputs/computational_execution_2026-05-14/cache/mgnify_genomes/`
- Plan 01 style safety screening patterns
- Plan 02/06/07 style sequence validation, novelty, and balanced downselection patterns

## Stage 1: Source Cleanup And Optional Expansion

Keep only Plan 04-relevant contexts:

- Rhizosphere
- Root-associated
- Endophyte, if available
- Plant-associated desert or drought/salinity contexts
- Terrestrial soil only when metadata supports plant or agricultural relevance

Exclude from the strict bridge unless explicitly plant-associated:

- Gut
- Hydrothermal
- Polar
- Marine sediment
- Generic saline

Initial local relevant genome set:

- `MGYG000535630`, rhizosphere, barley-rhizosphere-v2-0
- `MGYG000535629`, rhizosphere, barley-rhizosphere-v2-0
- `MGYG000535628`, rhizosphere, barley-rhizosphere-v2-0
- `MGYG000511829`, soil, soil-v1-0
- `MGYG000511828`, soil, soil-v1-0
- `MGYG000511826`, soil, soil-v1-0
- `MGYG000518629`, desert plant rhizosphere, barley-rhizosphere-v2-0
- `MGYG000517651`, desert plant rhizosphere, maize-rhizosphere-v1-0
- `MGYG000517233`, desert plant rhizosphere, tomato-rhizosphere-v1-0

If this strict local set does not produce enough strong candidates, expand using MGnify Genomes plant/rhizosphere/root catalogues before final scoring.

## Stage 2: Collapse Protein Hits Into Genome/MAG Candidates

Plan 04 should rank organisms or MAGs, not isolated protein hits.

Build:

```text
plan04_genome_trait_matrix.csv
```

One row per genome/MAG with fields for:

- Genome ID
- Source query and query label
- Catalogue
- Biome
- Host/crop/stress metadata where available
- GTDB taxonomy
- Completeness
- Contamination
- Genome quality score
- Trait support by class
- Driver proteins for each trait
- BGC/antiSMASH/GECCO/SanntiS support
- AMR/mobile/toxin/virulence safety context
- Final trait score, metadata score, safety score, and bridge score

Trait classes:

- Phosphate solubilization
- Nitrogen availability
- Siderophore production
- ACC deaminase
- Indole acetic acid support
- Osmoprotection and drought/salinity stress response
- Antifungal activity or antifungal BGC support
- Biofilm, root colonization, adhesion, EPS, or secretion support

## Stage 3: Target-Specific False-Positive Filters

Replace broad keyword matching with trait-specific evidence rules.

### Phosphate Solubilization

Accept stronger evidence such as:

- PQQ-dependent glucose dehydrogenase or related gluconic-acid phosphate-solubilization logic
- Phytase
- PhoD/PhoA/PhoX or credible phosphatase families
- Phosphonatase or phosphonate utilization pathway support
- Coherent pathway or neighborhood support

Reject or downgrade:

- Generic kinases
- Generic phosphotransferases
- Generic ATPases
- Generic PLP enzymes
- Any hit where "phosphate" appears only as a cofactor, substrate annotation, or housekeeping pathway term

### Nitrogen Availability

Accept:

- Nitrogen fixation support, especially nifHDK or coherent nitrogenase-associated cluster evidence
- Urease plus accessory genes and transport context
- Nitrate/nitrite assimilation support with multiple pathway components

Downgrade:

- Single isolated nitrate reductase, urease, or nitrogen-metabolism hit without pathway context

### Siderophore Production

Accept:

- Siderophore BGC or antiSMASH/GECCO/SanntiS support
- Siderophore biosynthesis genes plus receptor/transport context
- TonB or ABC siderophore machinery only as support, not a standalone primary claim

### ACC Deaminase

Accept:

- Clear `acdS` or ACC deaminase-like annotation with reviewed homolog support
- PLP enzyme assignment consistent with ACC deaminase family
- Reciprocal reviewed-reference support where possible

Reject or downgrade:

- Generic aminotransferases
- Generic PLP enzymes without ACC deaminase-specific support

### Indole Acetic Acid Support

Accept:

- Tryptophan-dependent IAA pathway evidence
- Indole-3-acetic-acid related enzymes with coherent pathway support

Downgrade:

- Generic tryptophan metabolism without IAA pathway specificity

### Osmoprotection And Stress Response

Accept:

- Ectoine synthesis or transport
- Glycine betaine synthesis or transport
- Trehalose synthesis
- Compatible-solute transporters
- Drought/desiccation/salinity response context, especially from plant-associated desert or rhizosphere catalogues

### Antifungal And BGC Support

Accept:

- Chitinase, beta-glucanase, or lytic enzyme support with secretion or neighborhood context
- Siderophore or antifungal natural-product BGCs with Plan 01 style BGC review
- Multi-caller BGC support when available

Downgrade:

- Generic hydrolases without substrate specificity
- BGCs with weak domain logic, boundary issues, or rediscovery/safety burden

### Biofilm, Root Colonization, Adhesion, EPS

Use these as support features rather than final standalone claims unless multiple colonization-related systems co-occur.

Accept support from:

- EPS or capsular polysaccharide biosynthesis/export
- Adhesins
- Biofilm matrix genes
- Secretion/export machinery
- Root-associated source metadata

## Stage 4: Metadata And Phenotype Strength

Score metadata separately from genomic potential.

Metadata features:

- Host crop or plant, for example barley, maize, tomato
- Root/rhizosphere compartment
- Desert, drought, salinity, or stress-relevant source
- Soil type where available
- Treatment or phenotype labels where available
- ENA sample and study accession availability
- Replication or catalogue confidence

Suggested metadata calls:

- `DIRECT_PLANT_STRESS_CONTEXT`: plant/rhizosphere plus stress-relevant source
- `DIRECT_PLANT_CONTEXT`: plant/rhizosphere/root but no explicit stress
- `INDIRECT_SOIL_CONTEXT`: soil with agricultural or plant relevance unclear
- `HOLD_METADATA_REVIEW`: weak or missing metadata

## Stage 5: Safety Gate

Use Plan 01 style safety screening before any wet-lab candidate can advance.

Check:

- AMRFinderPlus rows for the source genome
- Mobilome GFF for nearby mobile elements or genome-level mobile burden
- Toxin keywords
- Virulence keywords
- Pathogen-adjacent taxonomy
- Known problematic genera or source contexts
- Candidate driver proteins near AMR/mobile/toxin/virulence loci where coordinates are available

Safety calls:

- `PASS`
- `PASS_WITH_CONTEXT_NOTE`
- `HOLD_SAFETY_REVIEW`

Any candidate with direct AMR, virulence, toxin, or strong mobile-element burden should be held and excluded from the final wet-lab planning set.

## Stage 6: Reviewed-Reference Validation

For strict genome candidates, select driver proteins for each claimed trait and validate them.

For key driver proteins:

- Extract sequences from cached `.faa` files.
- Run Swiss-Prot/UniProt reviewed-reference search.
- Run reciprocal checks where practical.
- Generate family MSAs for ambiguous but important trait calls.
- Record best reviewed homolog, identity, query coverage, evidence title, and novelty call.

Priority validation targets:

- ACC deaminase
- Chitinase/glucanase
- Phytase or phosphatase
- Siderophore biosynthetic proteins
- Nitrogenase-associated proteins
- Ectoine/betaine/trehalose pathway proteins

Novelty calls:

- `HIGH_SEQUENCE_NOVELTY`
- `MEDIUM_HIGH_SEQUENCE_NOVELTY`
- `MODERATE_NOVELTY_CLOSE_FUNCTIONAL_HOMOLOG`
- `LOW_NOVELTY_CLOSE_SWISSPROT`
- `NO_REVIEWED_HOMOLOG_FOUND`

Plan 04 does not require novelty as strongly as Plans 06/07. A closer reviewed homolog can be useful if it strengthens the biological hypothesis and improves assay interpretability. Novelty should be rewarded, but not allowed to outrank safety, metadata, and trait coherence.

## Stage 7: Scoring

Use a bridge score that rewards multi-trait plant relevance and punishes weak metadata or safety burden.

Suggested scoring:

```text
plan04_bridge_score =
  0.20 * plant_benefit_trait_support
+ 0.17 * metadata_and_source_strength
+ 0.15 * multi_trait_complementarity
+ 0.14 * crop_or_stress_relevance
+ 0.12 * genome_quality_and_taxonomy_confidence
+ 0.10 * wetlab_feasibility
+ 0.07 * novelty_or_underexplored_taxonomy
+ 0.05 * safety_score
```

Additional hard gates:

- Genome completeness preferably `>=80%`
- Contamination preferably `<=5%`
- Candidate should have at least 3 supported PGP/stress traits to be finalist-eligible
- Candidate should have at least 1 primary actionable trait
- Candidate must not have `HOLD_SAFETY_REVIEW`
- Candidate must not rely entirely on generic phosphate/kinase/housekeeping hits

## Stage 8: Balanced Review Queue

Produce:

```text
plan04_balanced_review_queue_40.csv
```

Do not allow one mechanism, one genome, or one catalogue to dominate.

Balance across:

- Rhizosphere/root/desert plant contexts
- Crop/source catalogues
- Mechanisms
- Taxonomic lineages
- Candidate quality

Suggested caps:

- Maximum 6-8 candidates per genome in the review queue
- Maximum 10-12 candidates dominated by phosphate
- At least several candidates with osmoprotection/stress support
- At least several candidates with siderophore or antifungal/BGC support
- At least several candidates from direct plant/rhizosphere context

## Stage 9: Downselect To 10-20

Produce:

```text
plan04_downselected_12.csv
```

Each downselected candidate should have:

- Clear source and sample accession
- Trait matrix evidence
- Primary trait hypothesis
- Supporting secondary traits
- Driver proteins listed
- Metadata strength call
- Safety call
- Genome quality call
- Wet-lab feasibility call
- Main reason for inclusion
- Main remaining caveat

## Stage 10: Final Wet-Lab Planning Set

Produce:

```text
plan04_wetlab_candidates.csv
```

Aim for 3-5 candidates.

Final set composition:

- 1 drought/salinity rhizosphere candidate with osmoprotection plus colonization support
- 1 nutrient-availability candidate with phosphate plus nitrogen support
- 1 antifungal/siderophore candidate with BGC or secretion support
- 1 high-quality plant-associated MAG with the strongest multi-trait profile
- Optional fifth candidate only if safety and metadata are clean

Final candidate eligibility:

- `PASS` or `PASS_WITH_CONTEXT_NOTE` safety call
- Not dominated by generic housekeeping annotations
- At least 3 supported PGP/stress traits
- At least 1 primary actionable trait
- Strong source context
- Clear assay plan
- No unsupported plant-growth or crop-resilience claim

## Stage 11: Candidate Packets

Write one Markdown packet per finalist:

```text
wetlab_candidate_packets/
```

Each packet should include:

- Candidate rank
- Genome ID and source accession
- Catalogue, biome, host/crop/stress context
- Taxonomy
- Completeness and contamination
- Primary wet-lab hypothesis
- Supported traits
- Rejected or weak traits
- Driver protein table
- Reviewed-reference/novelty results
- BGC or pathway evidence where relevant
- Safety screen
- Feasibility screen
- Proposed pre-wet-lab handoff assays
- Boundaries and caveats

## Stage 12: Reports And Audit

Write:

```text
PLAN04_PGP_BRIDGE_REPORT.md
PLAN04_COMPLETION_AUDIT.md
plan04_pgp_bridge_summary.json
```

The report should include:

- Input row counts
- Source cleanup counts
- Genome/MAG candidate counts
- Strict false-positive rejection counts
- Balanced queue count
- Downselected count
- Wet-lab planning count
- Final 3-5 candidate table
- Interpretation limits
- Output file list

The audit should verify:

- Source contexts were filtered and recorded
- Protein hits were collapsed to genome/MAG candidates
- Trait-specific false-positive filters ran
- Metadata strength was scored
- Safety was screened
- Reviewed-reference validation was attempted for driver proteins
- Balanced review queue was produced
- Downselected 10-20 set was produced
- Final 3-5 wet-lab planning candidates were produced
- Packets, report, and summary JSON exist

## Expected Output Files

```text
plan04_relevant_source_genomes.csv
plan04_trait_filtered_protein_hits.csv
plan04_trait_rejections.csv
plan04_genome_trait_matrix.csv
plan04_driver_proteins.faa
plan04_driver_vs_swissprot.tsv
plan04_driver_reciprocal_vs_candidates.tsv
plan04_driver_validation.csv
plan04_strict_pgp_candidates.csv
plan04_balanced_review_queue_40.csv
plan04_downselected_12.csv
plan04_wetlab_candidates.csv
plan04_crop_stress_pathway_signatures.csv
plan04_antifungal_bgc_subqueue_strict.csv
wetlab_candidate_packets/
PLAN04_PGP_BRIDGE_REPORT.md
PLAN04_COMPLETION_AUDIT.md
plan04_pgp_bridge_summary.json
```

## Completion Bar

Plan 04 pre-wet-lab screening is complete only when there are 3-5 finalist candidates that pass all of the following:

- Plant-associated or clearly relevant soil/desert context.
- Genome completeness preferably `>=80%`.
- Contamination preferably `<=5%`.
- At least 3 supported plant-growth, nutrient, antifungal, colonization, or stress-response traits.
- At least 1 primary actionable wet-lab trait.
- No direct AMR/mobile/toxin/virulence burden.
- Target-specific evidence, not broad keyword hits.
- Clear wet-lab handoff hypothesis.
- Claims framed as hypotheses until plant assays are completed.

## Interpretation Boundaries

These outputs justify wet-lab planning but do not validate plant-growth promotion, drought tolerance, salinity tolerance, pathogen suppression, or crop yield effects.

The final candidates should first be tested in low-risk, controlled assays such as phosphate solubilization, siderophore production, ACC deaminase activity, IAA production, osmotic-stress growth, antifungal plate assays, and seedling assays under controlled stress. Greenhouse work should follow only after controlled assay support.

No field or crop-resilience claims should be made before replicated greenhouse or field validation.
