# Plan 08 - Extremophile Enzyme Atlas Archive

Generated: 2026-05-18

Release-layer archive for the extremophile enzyme atlas and stability-feature score table.

This archive indexes the full atlas table rather than duplicating every row into Markdown. The full CSV remains the authoritative archive artifact.

Full atlas CSV: `outputs/plan09_release_metadata_stability_2026-05-17/plan09_stability_feature_scores.csv`
Atlas rows: `4071`

## Source Report

## Plan 09 Release Metadata And Stability-Feature Report

Run date: 2026-05-17

### Scope

This package adds release-style provenance/checksum metadata and a standalone stability-testing priority model for the Plan09 extremophile enzyme atlas.

Claim boundary: Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance.

### Source Manifest

| manifest_file_count | download_source_kinds | strict_rows | high_precision_rows |
| --- | --- | --- | --- |
| 1289 | 5 | 17932 | 4071 |

### Extremophile Metadata Audit

| extreme_label | row_count | genome_count | catalogue_count | biome_count | geographic_origin_missing_pct | median_quality_score |
| --- | --- | --- | --- | --- | --- | --- |
| desiccation | 1580 | 8 | 4 | 2 | 11.519 | 95.72 |
| heat | 564 | 8 | 1 | 1 | 60.993 | 83.14 |
| marine_salt | 550 | 8 | 1 | 1 | 100.0 | 75.66 |
| heat_biomass | 525 | 3 | 3 | 3 | 0.0 | 90.65 |
| cold | 389 | 8 | 1 | 1 | 62.725 | 76.54 |
| heat_pressure | 271 | 4 | 2 | 2 | 40.221 | 97.47 |
| salt | 192 | 2 | 2 | 2 | 41.146 | 98.95 |

### Top Stability-Testing Tracks

| extreme_label | target | row_count | genome_count | catalogue_count | mean_stability_feature_score | top_protein_id |
| --- | --- | --- | --- | --- | --- | --- |
| desiccation | glycosidase | 737 | 8 | 4 | 92.206 | MGYG000502387_00068 |
| heat_pressure | glycosidase | 28 | 4 | 2 | 89.286 | MGYG000473050_02210 |
| desiccation | esterase | 64 | 8 | 4 | 88.975 | MGYG000502387_00250 |
| desiccation | dehalogenase | 15 | 7 | 4 | 88.889 | MGYG000502387_01278 |
| desiccation | protease | 107 | 8 | 4 | 88.525 | MGYG000502387_00054 |
| desiccation | lipase | 11 | 7 | 4 | 88.384 | MGYG000502387_01307 |
| desiccation | cellulase | 186 | 8 | 4 | 86.29 | MGYG000502387_01211 |
| heat_pressure | nitrilase | 4 | 3 | 2 | 86.111 | MGYG000473050_02978 |
| desiccation | xylanase | 192 | 8 | 4 | 85.677 | MGYG000517010_02368 |
| heat_pressure | protease | 55 | 4 | 2 | 85.0 | MGYG000473050_00272 |
| heat_pressure | esterase | 15 | 4 | 2 | 84.63 | MGYG000473050_00631 |
| salt | glycosidase | 32 | 2 | 2 | 84.375 | MGYG000478572_01569 |

### Top Stability-Feature Candidates

| protein_id | target | extreme_label | stability_feature_score | stability_priority_call |
| --- | --- | --- | --- | --- |
| MGYG000502387_01211 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517010_00514 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517010_00658 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517010_01989 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517010_03126 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517010_03689 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_01746 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_02323 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_02411 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_02533 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_03692 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |
| MGYG000517051_04355 | cellulase | desiccation | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS |

### Interpretation

- Plan09 now has local artifact checksums, CSV row counts, and column manifests suitable for a grant-facing release appendix.
- The stability model is standalone and Plan09-specific; it combines source-condition context, genome quality, annotation evidence, high-precision score, environmental replication, and dependency penalties.
- The model ranks hypotheses for stability testing only. It does not prove stability from habitat, sequence, or annotation.

### Output Files

- `plan09_source_file_manifest.csv`
- `plan09_download_source_summary.csv`
- `plan09_extremophile_metadata_audit.csv`
- `plan09_stability_feature_model_spec.csv`
- `plan09_stability_feature_scores.csv`
- `plan09_stability_track_summary.csv`
- `PLAN09_RELEASE_METADATA_STABILITY_COMPLETION_AUDIT.md`

## First 25 Stability-Feature Rows

| candidate_id | protein_id | genome_id | target | condition | extreme_label | catalogue | biome | quality_score | high_precision_score | strict_evidence | condition_source_feature | condition_source_points | genome_quality_points | annotation_evidence_points | high_precision_score_points | environmental_replication_points | dependency_penalty | track_row_count | track_genome_count | track_catalogue_count | track_biome_count | stability_feature_score | stability_priority_call | claim_limit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| strict:MGYG000502387:MGYG000502387_01211:cellulase | MGYG000502387_01211 | MGYG000502387 | cellulase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517010:MGYG000517010_00514:cellulase | MGYG000517010_00514 | MGYG000517010 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 99.09 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517010:MGYG000517010_00658:cellulase | MGYG000517010_00658 | MGYG000517010 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 99.09 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517010:MGYG000517010_01989:cellulase | MGYG000517010_01989 | MGYG000517010 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 99.09 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517010:MGYG000517010_03126:cellulase | MGYG000517010_03126 | MGYG000517010 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 99.09 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517010:MGYG000517010_03689:cellulase | MGYG000517010_03689 | MGYG000517010 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 99.09 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_01746:cellulase | MGYG000517051_01746 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_02323:cellulase | MGYG000517051_02323 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_02411:cellulase | MGYG000517051_02411 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_02533:cellulase | MGYG000517051_02533 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_03692:cellulase | MGYG000517051_03692 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000517051:MGYG000517051_04355:cellulase | MGYG000517051_04355 | MGYG000517051 | cellulase | desiccation | desiccation | tomato-rhizosphere-v1-0 | root:Host-associated:Plants:Rhizosphere | 98.07 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000518629:MGYG000518629_01184:cellulase | MGYG000518629_01184 | MGYG000518629 | cellulase | desiccation | desiccation | barley-rhizosphere-v2-0 | root:Host-associated:Plants:Rhizosphere | 95.72 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000518629:MGYG000518629_01185:cellulase | MGYG000518629_01185 | MGYG000518629 | cellulase | desiccation | desiccation | barley-rhizosphere-v2-0 | root:Host-associated:Plants:Rhizosphere | 95.72 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000518629:MGYG000518629_02804:cellulase | MGYG000518629_02804 | MGYG000518629 | cellulase | desiccation | desiccation | barley-rhizosphere-v2-0 | root:Host-associated:Plants:Rhizosphere | 95.72 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000518629:MGYG000518629_03657:cellulase | MGYG000518629_03657 | MGYG000518629 | cellulase | desiccation | desiccation | barley-rhizosphere-v2-0 | root:Host-associated:Plants:Rhizosphere | 95.72 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 186 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00068:glycosidase | MGYG000502387_00068 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00082:glycosidase | MGYG000502387_00082 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00132:glycosidase | MGYG000502387_00132 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00134:glycosidase | MGYG000502387_00134 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00184:glycosidase | MGYG000502387_00184 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00185:glycosidase | MGYG000502387_00185 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00273:glycosidase | MGYG000502387_00273 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00274:glycosidase | MGYG000502387_00274 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
| strict:MGYG000502387:MGYG000502387_00275:glycosidase | MGYG000502387_00275 | MGYG000502387 | glycosidase | desiccation | desiccation | soil-v1-0 | root:Environmental:Terrestrial:Soil | 95.62 | 100.0 | specific_name_or_description;domain_family_support;ec_class_support;cazy_dbcan_support | DESICCATION_ASSOCIATED_SOURCE_TRACK | 1.5 | 2.0 | 2.0 | 1.5 | 2.0 | 0.0 | 737 | 8 | 4 | 2 | 100.0 | HIGH_PRIORITY_STABILITY_TESTING_HYPOTHESIS | Stability-feature scoring is a computational prioritization heuristic; it does not validate enzyme activity, expression, stability, condition tolerance, substrate scope, or industrial performance. |
