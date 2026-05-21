# Plan 02: Industrial Biocatalyst Results

Plan 02 searched environmental sequence resources for enzyme candidates that could become useful industrial biocatalyst leads. The screen looked for a practical middle ground: candidates that were novel enough to be interesting but still had enough family, structure, and active-site evidence to be experimentally interpretable.

## What Happened

The broad enzyme screen produced strict and high-precision queues across ketoreductases, lipases, proteases, transaminases, peroxidases, dehalogenases, esterases, monooxygenases, glycosidases, nitrilases, cellulases, xylanases, and related families.

The hardening pass separated the broad archive from the first bridge leads. That distinction matters because a large enzyme archive is useful for future mining, but a first wet-lab package needs a smaller set with clearer structure/function logic.

## Main Results

Two current bridge leads stood out:

| Candidate | Enzyme frame | Result |
|---|---|---|
| `MGYG000527579_00796` | Dehalogenase | Cleanest activity-first enzyme lead. It has candidate-specific structure support, active-site context, and a clear family hypothesis. |
| `MGYG000517010_03432` | Glycosidase | Strong secondary lead. Later full-length ColabFold support reduced the earlier structure limitation, but catalytic-residue assignment and family-numbering review remain unresolved. |

`MGYG000527579_00796` is the strongest Plan 02 bridge candidate. The later ColabFold model had mean pLDDT 97.194 on the 0-100 scale, and the active-site review highlighted D5, S110, N111, and D169 as residues for mechanistic review. The safety-context call was pass with context note.

`MGYG000517010_03432` remains useful because the full-length model had mean pLDDT 94.591 and pocket geometry consistent with a glycosidase hypothesis. It is not as clean as the dehalogenase because the catalytic acid/base and family numbering still need expert review.

## Why This Matters

The important result is not only that enzyme candidates were found. The useful result is that the project produced a traceable enzyme universe, narrowed it into strict and high-precision queues, and then identified two current bridge leads with enough evidence for focused wet-lab discussion.

The strongest claim is:

> The campaign produced a traceable enzyme candidate universe, broad strict/high-precision review queues, and two current bridge candidates for industrial biocatalyst follow-up.

## What Is Not Proven

The screen does not prove catalytic activity, substrate scope, kinetics, expression, stability, soluble recovery, process tolerance, or industrial usefulness. Those questions require expression and activity testing.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/02_08_biocatalyst_extremophile_enzyme_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_07_enzyme_bridge_leads.png`
