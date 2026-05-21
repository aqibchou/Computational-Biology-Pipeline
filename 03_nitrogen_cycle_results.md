# Plan 03: Nitrogen-Cycle Results

Plan 03 screened environmental genomes for nitrogen-cycle pathway hypotheses connected to nitrogen fixation, nitrous oxide reduction, urea/rhizosphere nitrogen cycling, and nitrate or nitrite transformation.

This was one of the most societally important screens because nitrogen availability, fertilizer efficiency, and N2O emissions are major agricultural and climate-linked problems. It was also one of the easiest screens to overclaim, so the final logic emphasized marker specificity and pathway context.

## What Happened

The first-pass screen produced 655 nitrogen-cycle hits. Many were not strong enough to keep. The cleanup rejected 324 hits as housekeeping or unrelated domains, held 103 for low coverage or fragment status, held 53 as single-gene-only cases, held 28 for low genome quality, and held 22 for confusable domains.

After rebuilding around marker specificity, pathway completeness, genomic neighborhood, source context, genome quality, and safety/practicality gates, the final master table contained 116 genome-track pathway profiles. Six candidates advanced to immediate pre-wet-lab packets.

IQ-TREE was also completed for narG/napA, nifH, nosZ, and ureC marker families. The phylogenies strengthened bookkeeping and family context, but small nifH and nosZ family sizes limit broad evolutionary claims.

## Main Results

| Candidate | Track | Score | Interpretation |
|---|---:|---:|---|
| `MGYG000517341_00816` | nifH nitrogen fixation | 91.90 | Nitrogen-fixation pathway hypothesis from genome `MGYG000517341`. |
| `MGYG000478572_00459` | nosZ nitrous oxide reduction | 91.61 | N2O-reduction hypothesis from genome `MGYG000478572`. |
| `MGYG000473561_03510` | nosZ nitrous oxide reduction | 91.25 | N2O-reduction hypothesis from genome `MGYG000473561`. |
| `MGYG000511828_04091` | ureC alpha urea/rhizosphere nitrogen | 87.70 | Urea and rhizosphere nitrogen hypothesis from genome `MGYG000511828`. |
| `MGYG000517341_01850` | ureC alpha urea/rhizosphere nitrogen | 86.42 | Urea and rhizosphere nitrogen hypothesis from genome `MGYG000517341`. |
| `MGYG000511829_04732` | narG/napA nitrate/nitrite transformation | 80.72 | Nitrate/nitrite transformation hypothesis from genome `MGYG000511829`. |

The screen also made an important negative call: nitrification and ammonia-oxidation candidates were not advanced because AMO/pMMO identity and complete amoABC/hao support were not clean enough.

## Why This Matters

The final six candidates are compelling because they survived a screen that actively rejected noisy marker hits. For nitrogen biology, that restraint is a strength. Weak marker-like annotations can easily imply phenotypes that are not real.

The strongest claim is:

> Six nitrogen-cycle pathway hypotheses were computationally prioritized with marker-model, pathway-context, source-metadata, novelty, genome-quality, safety-context, and marker-phylogeny support.

## What Is Not Proven

The screen does not prove nitrogen fixation, nitrous oxide reduction, urease activity, nitrate/nitrite flux, fertilizer efficiency, plant benefit, greenhouse performance, field performance, or environmental safety. Those outcomes require controlled expression, pathway, organism, or soil/plant assays.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/03_nitrogen_cycle_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_08_nitrogen_candidate_tracks.png`
