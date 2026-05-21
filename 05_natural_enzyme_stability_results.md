# Plan 05: Natural Enzyme Stability Results

Plan 05 was the stability-first extension of the enzyme work. It did not design mutations or propose optimized variants. Instead, it asked whether naturally occurring homologs from stress-associated contexts could be prioritized for experimental testing under salt, pH, heat, solvent, detergent, or related stress axes.

## What Happened

The focused input pool contained 3,237 enzyme rows across dehalogenases, esterases, glycosidases, lipases, proteases, and transaminases. The screen produced 19 natural-stability shortlist candidates, 19 strict bridge candidates, six strict advance calls, and four immediate wet-lab planning candidates.

The hardening pass added candidate-specific structures, family MSA context, BRENDA condition context, IQ-TREE3 phylogenies, loop/disorder comparison, charge and salt-bridge proxies, ThermoMPNN aggregate summaries, expression-risk notes, and safety-context review.

These layers make Plan 05 one of the cleanest near-term wet-lab packages in the repository.

## Main Results

| Candidate | Family | Stress axis | Bridge score | Interpretation |
|---|---|---|---:|---|
| `MGYG000478572_00760` | Esterase | Salt | 133.119 | Cleanest near-term Plan 05 lead. High sequence novelty, strong structure confidence, low expression risk, marine/salt context, and a straightforward esterase hypothesis. |
| `MGYG000517341_01521` | Dehalogenase | Salt | 128.637 | Attractive dehalogenase hypothesis with useful novelty and structure support, but flexible-region and structure-confidence caveats remain. |
| `MGYG000518629_02280` | Esterase-like | pH | 126.830 | pH-axis esterase-like candidate with useful novelty and expression-design uncertainty. |
| `MGYG000478572_01589` | Transaminase | Salt | 121.602 | Strong structural candidate with cofactor complexity from PLP dependence. |

Two backup strict-pass candidates were also retained in the source material: `MGYG000478572_02520`, a salt-axis protease, and `MGYG000517233_02590`, a pH-axis esterase.

## Why This Matters

The top candidate, `MGYG000478572_00760`, is one of the strongest first experimental picks in the whole campaign. It combines a clear enzyme hypothesis with strong structure confidence, low expression risk, novelty, and a plausible salt-axis rationale.

The strongest claim is:

> Four natural enzyme homologs were computationally prioritized for stress-condition testing with layered sequence, structure, phylogeny, safety-context, and stability-proxy evidence.

## What Is Not Proven

The screen does not prove enzyme activity, expression, substrate scope, stress tolerance, thermal stability, salt tolerance, pH stability, or industrial process performance. Stability proxies and ThermoMPNN aggregate context support prioritization only.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/05_natural_stability_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_10_stability_candidates.png`
