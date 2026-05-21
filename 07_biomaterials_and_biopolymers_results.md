# Plan 07: Biomaterials And Biopolymers Results

Plan 07 screened microbial biomaterial hypotheses across biopolymer/EPS, protein-material, pigment/material, and BGC/material tracks. The key challenge was separating material-specific evidence from generic surface, membrane, transporter, or housekeeping annotations.

## What Happened

The screen started from 731 first-pass biomaterials hits. After adding BGC, genome-quality, source-environment, recovery, and safety-context gates, and after incorporating Plan 01 strict BGC review rows for the biosurfactant/BGC track, the final master table contained 746 rows.

The false-positive burden was large and informative. The screen held 406 rows for weak material specificity, 96 as review backups, 78 for low genome quality, 54 as housekeeping lipid-A/LPS rather than biosurfactant evidence, and smaller groups for generic protein, incomplete biosurfactant evidence, low priority, or safety context. Sixty-three rows were kept as pre-wet-lab packet candidates, and six became the immediate packet set.

## Main Results

| Candidate | Track | Subtype | Score | Interpretation |
|---|---|---|---:|---|
| `MGYG000517341_02043` | Biopolymers/EPS | PHA / polyhydroxyalkanoate | 84.04 | Clearest PHA/biopolymer hypothesis with PhaC and same-genome PHA/phasin/PhaR support. |
| `MGYG000478572_01331` | Biopolymers/EPS | EPS / capsule export | 84.43 | EPS/capsule export hypothesis with supported export/recovery logic and MAG-route uncertainty. |
| `MGYG000517341_00932` | Biopolymers/EPS | EPS / capsule export | 83.47 | EPS/capsule hypothesis with SanntiS saccharide and dbCAN capsule-polysaccharide context. |
| `MGYG000517341_02173` | Protein materials | Surface adhesive protein | 83.27 | Surface-adhesive hypothesis with localization support and expression/folding questions. |
| `MGYG000521810_02082` | Protein materials | Surface adhesive protein | 83.27 | Surface-adhesive hypothesis with locus support and partial recovery route. |
| `MGYG000517341_02282` | Pigments / functional materials | Tyrosinase / melanin-like | 79.04 | Compact pigment/material hypothesis requiring pigment identity confirmation. |

Three BGC/material candidates remain review holds:

- `MGYG000517341:MGYG000517341_27:9851-55107`, NRP/lipopeptide-like BGC review.
- `MGYG000517341:MGYG000517341_2:234333-279288`, NRP/lipopeptide-like BGC review.
- `MGYG000521810:MGYG000521810_13:25308-46111`, hserlactone BGC review.

## Why This Matters

Plan 07 produced a practical biomaterial starting set across several material classes. The most useful part of the result is the filtering discipline: lipid-A/LPS and other broad envelope annotations were not allowed to become biosurfactant or material claims by default.

The strongest claim is:

> The screen produced computational biomaterial hypotheses with pathway, source-environment, novelty/recovery, safety-context, and assay-feasibility support.

## What Is Not Proven

The screen does not prove material production, polymer chemistry, pigment identity, recoverability, yield, coating behavior, rheology, performance, product safety, or organism safety. Those results require product-identity and material-property testing.

## Where The Evidence Lives

- Main report: `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- Candidate archive: `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/07_biomaterials_candidate_archive.md`
- Figure: `outputs/perusing_biological_datasets_report_package_2026-05-18/figures/figure_12_biomaterial_candidate_packets.png`
