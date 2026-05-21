# Plan 06: Rare-Chemistry Results

Plan 06 searched for enzyme candidates with plausible rare or underexplored reaction-family hypotheses. This was intentionally higher risk than the activity-first enzyme screen, because rare chemistry often has weaker substrate-specific annotation but higher discovery upside.

## What Happened

The screen began with 11,805 first-pass candidates and retained chemistry classes including dehalogenation, redox, C-H activation, rare-sugar chemistry, organosulfur chemistry, organophosphorus chemistry, and adjacent halogenation.

The narrowing process produced a 300-candidate priority queue, a 40-candidate MSA/structure review queue, 40 strict bridge candidates, 16 downselected rare-chemistry candidates, and four immediate wet-lab planning candidates.

The final hardening pass added Rhea/EC mapping, BRENDA context, reviewed-reference checks, reciprocal checks, MSA review, candidate-specific structures, IQ-TREE3 reaction-family phylogenies, dependency flags, and reference ligand-pocket comparison.

## Main Results

| Candidate | Class | Bridge score | Interpretation |
|---|---|---:|---|
| `MGYG000478572_02342` | Redox | 111.268 | Strongest all-around rare-chemistry candidate, with supported reaction context and structure confidence. Cofactor/partner dependency is the main risk. |
| `MGYG000521810_01693` | Organosulfur | 109.489 | Coherent sulfurtransferase/rhodanese-like hypothesis with partial pocket-context limitations. |
| `MGYG000478572_01361` | Rare sugar | 108.523 | High-upside rare-sugar hypothesis, but substrate specificity and pocket context remain unresolved. |
| `MGYG000517233_02445` | Dehalogenation class | 104.180 | Excellent predicted structure and low expression risk, but manual pocket review is needed before substrate-specific dehalogenation claims. |

The dehalogenation label for `MGYG000517233_02445` is deliberately framed as a reaction-family hypothesis. Its closest curated-name match was not itself a clean substrate-specific dehalogenase annotation, so the result remains promising but bounded.

## Why This Matters

Rare chemistry is one of the highest-upside parts of the project. These candidates are less certain than the cleanest enzyme leads, but a single validated rare-reaction hit could be scientifically valuable.

The strongest claim is:

> Four rare-chemistry enzyme hypotheses were computationally prioritized with sequence novelty, reaction mapping, structure confidence, phylogeny, and safety-context evidence.

## What Is Not Proven

The screen does not prove enzyme activity, substrate specificity, product identity, partner availability, expression, cofactor compatibility, or new reaction chemistry. Product identity and reaction specificity remain experimental questions.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/06_rare_chemistry_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_11_rare_chemistry_candidates.png`
