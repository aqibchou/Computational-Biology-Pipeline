# Plan 04: Plant-Growth-Promotion Results

Plan 04 evaluated plant-associated genomes and MAGs as plant-growth-promotion (PGP) hypotheses. This module was different from the single-gene enzyme screens because the candidate unit was an organism or genome-level hypothesis.

That made the screen stricter. A single plant-benefit annotation was not enough. The strongest candidates needed source relevance, trait co-occurrence, genome quality, reference or culture plausibility, and no obvious local computational safety blocker.

## What Happened

The first-pass Plan 04 table contained many noisy trait-like hits. The final screen shifted from protein keyword ranking to genome-level evidence. It asked whether each genome had a coherent plant-associated story and whether there was a practical path to discuss or recover the organism.

Reference ANI and strain dereplication became the key upgrade. This strengthened `MGYG000517341` substantially and kept the other candidates in lower-confidence or hold categories.

## Main Results

| Candidate | Frame | Result |
|---|---|---|
| `MGYG000517341` | Osmoprotection and stress-associated PGP | Cleanest organism-level lead. |
| `MGYG000535629` | Siderophore-linked PGP in a Bacteriovorax context | Lower-confidence surrogate or trait hypothesis. |
| `MGYG000535630` | Antifungal/BGC rhizosphere hypothesis | Organism-level hold. |
| `MGYG000511828` | Phosphate-solubilization genome hypothesis | Organism-level hold. |

`MGYG000517341` is the most practical Plan 04 result. It is an isolate from tomato rhizosphere with 100.0 percent completeness, 0.21 percent contamination, 87 contigs, N50 178,766, seven supported PGP trait classes, and exact fastANI/skani support to NCBI reference `GCF_040152065.1` strain UC4318. It also had same-species/type-material ANI support and passed the computational safety-context review with no genome AMR rows and no candidate AMR hits in the checked artifacts.

The other candidates remained useful but less clean:

- `MGYG000535629` had barley rhizosphere context and siderophore-linked trait evidence, but only distant genus-level reference support.
- `MGYG000535630` had plant/rhizosphere context and antifungal/BGC framing, but selected reference gating had low ANI and low coverage.
- `MGYG000511828` had a coherent phosphate-solubilization story, but source/culture path and reference context were weaker.

## Why This Matters

Plan 04 produced one of the most practical and consequential candidates in the repository. If `MGYG000517341` performs in controlled plant-association assays, the result could matter for plant stress resilience, nutrient-use efficiency, and agricultural microbiome work.

The strongest claim is:

> `MGYG000517341` is a computationally prioritized plant-associated genome-level PGP hypothesis with source, trait, reference, and safety-context support.

## What Is Not Proven

The screen does not prove plant-growth benefit, trait expression, root colonization, greenhouse performance, field performance, environmental release suitability, or organism safety. Those claims require organism access, controlled plant-association testing, trait-expression assays, and formal safety review.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/04_plant_growth_promotion_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_09_pgp_lead_profile.png`
