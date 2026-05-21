# Genomics and Microbiome Discovery Results

Created: 2026-05-14  
Original source instruction file: local workspace note `Research Directions/genomics.md`  
Purpose: document the completed computational genomics screens, the candidates they produced, and the scripts/results needed to audit the work.

## Scope

This GitHub-ready subset focuses on the screens that were actually completed and packaged:

- The shared environmental sequencing to candidate-selection pipeline.
- The open data backbone: SRA/ENA/DDBJ, MGnify, MGnify Genomes, GTDB, AlphaFold DB, UniProt, BRENDA, CAZy/dbCAN, MIBiG, and antiSMASH DB.
- Completed candidate-discovery screens for natural products, enzymes, nitrogen cycling, plant-growth promotion, natural enzyme stability, rare chemistry, biomaterials, and the extremophile enzyme atlas.

The original uncompleted AMR-surveillance and enzyme-pathway-anomaly experiment files are intentionally not part of the minimal GitHub push.

## Shared Protocol

Read this first:

- `00_shared_genomics_discovery_protocol.md`

The shared protocol defines the common evidence standard:

```text
processed public genomic data
-> accession and metadata freeze
-> assembly or existing assembly selection
-> gene/protein prediction
-> homolog clustering
-> domain and enzyme annotation
-> taxonomy and genomic-neighborhood context
-> structure/function inference
-> novelty, utility, feasibility, and safety ranking
-> candidate packets for synthesis, expression, assay, or field validation
```

## Source Registry

Use this file before executing any plan:

- `00_fact_check_source_registry_and_dependency_matrix.md`

It records source IDs, URLs, access notes, verified facts as of 2026-05-14, license or access cautions, and the plan-to-source matrix. Database counts and access policies must be rechecked at run time.

## Completed Plan Documents

1. `01_novel_antibiotics_and_antimicrobial_natural_products.md`
2. `02_industrial_biocatalyst_discovery.md`
3. `03_nitrogen_cycle_enzyme_discovery.md`
4. `04_plant_growth_promoting_microbiome_discovery.md`
5. `06_enzyme_stability_engineering_from_natural_diversity.md`
6. `07_rare_chemistry_and_new_enzyme_reaction_discovery.md`
7. `08_biosurfactants_biopolymers_and_biomaterials.md`
8. `09_extremophile_enzyme_atlas.md`

## Priority Recommendation

For fastest credible execution, start with:

1. Extremophile enzyme atlas.
2. Industrial biocatalyst discovery.
3. Enzyme stability engineering from natural diversity.
4. Plant-growth-promoting microbiome discovery.
5. Nitrogen-cycle enzyme discovery.

These directions can produce defensible computational candidate lists with processed resources before heavy raw-read assembly or wet-lab work. Novel antibiotics and AMR surveillance have very high impact, but require stricter biosafety, clinical interpretation, and collaboration controls.

## Directory Checklist

- [ ] Every plan lists required and conditional source IDs.
- [ ] Every plan lists software and compute dependencies.
- [ ] Every plan has dataset-freeze requirements.
- [ ] Every plan defines ranking features and weights or tiers.
- [ ] Every plan has domain-specific validation logic.
- [ ] Every plan has completion criteria and deliverables.
- [ ] Every external source has a registry entry.
- [ ] Every run records access dates, query parameters, versions, failed downloads, and excluded records.
- [ ] Every final claim is tied to evidence level, accession IDs, and reproducible artifacts.

## Completed Results Package

A packaged computational-discovery report is included at:

- `outputs/perusing_biological_datasets_report_package_2026-05-18/Perusing_Biological_Datasets_Research_Report_Detailed.md`
- `outputs/perusing_biological_datasets_report_package_2026-05-18/pdf_build/Perusing_Biological_Datasets_Research_Report_Detailed.pdf`
- `outputs/perusing_biological_datasets_report_package_2026-05-18/candidate_archives/`

The candidate archive contains 187 packetized candidate records plus the 4,071-row extremophile enzyme atlas index. These are computational candidates for wet-lab follow-up, not validated biological products.

## GitHub Results Overview

For the simpler, less formal summary of the completed candidate discovery work, use the repository homepage:

- `README.md`
