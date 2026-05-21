# Plan 01: Natural Products And Biosynthetic Gene Clusters

Plan 01 searched public environmental genome data for biosynthetic gene clusters (BGCs) that looked strong enough for natural-product expert review. The focus was not to claim a new antibiotic directly. The focus was to identify BGCs with enough novelty, product-class coherence, boundary quality, and dereplication support to justify chemistry-first follow-up.

## What Happened

The screen began from BGC calls and candidate packets generated from environmental genome and MAG resources. The hardening pass added whole-MAG antiSMASH support, product-class review, boundary review, MIBiG/BiG-SCAPE dereplication, safety-context notes, and feasibility review.

The final integrated package contained seven finalist-level BGCs. Three were retained as strong keep candidates. Four were held because newer evidence exposed unresolved boundary, contig-edge, or domain-logic problems.

That narrowing is the main result. The screen did not simply rank antiSMASH hits. It separated BGCs with coherent natural-product review evidence from BGCs that could mislead downstream interpretation.

## Main Results

The three strong keep candidates were:

| Candidate | Product frame | Key interpretation |
|---|---|---|
| `MGYG000517341:MGYG000517341_17:38631-49536` | RiPP-like | Medium-high novelty context, whole-MAG antiSMASH support, and no close full-MIBiG BiG-SCAPE link at the tested cutoffs. |
| `MGYG000473561:MGYG000473561_12:259192-267836` | T3PKS / polyketide-like | High sequence-novelty context and no close full-MIBiG BiG-SCAPE link at the tested cutoffs. |
| `MGYG000517341:MGYG000517341_21:36974-66085` | Betalactone-like | Medium-high novelty context, whole-MAG support, and no close full-MIBiG BiG-SCAPE link at the tested cutoffs. |

The four held candidates were also informative:

| Candidate | Why It Was Held |
|---|---|
| `MGYG000517341:MGYG000517341_6:34029-49595` | Unresolved NRP domain logic, including missing condensation-domain support. |
| `MGYG000517651:MGYG000517651_16:191-10832` | Contig-edge and condensation-domain issues. |
| `MGYG000511828:MGYG000511828_123:121-7601` | Contig-edge and incomplete PKS-domain issues. |
| `MGYG000320982:MGYG000320982_59:318-28393` | Contig-edge proximity. |

## Why This Matters

Natural-product discovery is high variance. Many BGCs look interesting at first pass, but product identity, expression, chemistry, and bioactivity often fail later. This screen is valuable because it made that uncertainty explicit and still produced three BGCs that survived a more rigorous review path.

The strongest claim is:

> Three BGCs were computationally prioritized as natural-product review hypotheses with multiple dereplication and boundary checks.

## What Is Not Proven

The screen does not prove product identity, compound novelty, antimicrobial activity, production, titer, safety, or commercial utility. Those questions require chemistry-first validation, metabolomics, dereplication at the compound level, and bioactivity testing after product evidence exists.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/01_secondary_metabolite_bgc_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_06_bgc_candidate_panel.png`
