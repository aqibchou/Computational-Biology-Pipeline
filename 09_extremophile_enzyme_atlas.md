# Extremophile Enzyme Atlas

## 1. Objective

Build an atlas of enzymes from extreme environments and rank them by novelty, predicted stability, environmental extremeness, known-function proximity, structure confidence, active-site conservation, and commercial relevance.

## 2. Hypotheses

- Extreme environments provide selection pressure for proteins that tolerate heat, salt, acidity, alkalinity, cold, pressure, radiation, desiccation, solvents, or industrial contaminants.
- A general atlas is a strong MVP because environment metadata can guide enzyme discovery before narrow assay selection.
- The most useful atlas separates environment-derived stability hypotheses from measured stability evidence.

## 3. Required Source IDs

Required:

- `MG-MGNIFY`
- `MG-GENOMES`
- `REF-UNIPROT`
- `ENZ-BRENDA`
- `STR-AFDB`
- `TAX-GTDB`

Conditional:

- `CAZ-DBCAN`
- `GEN-SRA`
- `ECO-EMP`
- `STR-FOLDSEEK`

## 4. Target Environments

Extreme environment classes:

- Hot springs.
- Hydrothermal vents.
- Acid mine drainage.
- Saline lakes and hypersaline soils.
- Polar ice and permafrost.
- Deserts.
- Deep subsurface.
- Radioactive sites.
- Industrial wastewater.
- Solvent/hydrocarbon-contaminated sites.

## 5. Initial Atlas Tracks

Produce separate track tables for:

- Thermophilic esterases.
- Acid-stable proteases.
- Salt-tolerant hydrolases.
- Solvent-tolerant oxidoreductases.
- Cold-active enzymes.
- Metal-tolerant enzymes.
- Radiation/desiccation-associated repair or antioxidant enzymes.

## 6. Data Build

1. Define an environment ontology and keyword map before querying.
2. Pull MGnify analyses and MGnify Genomes catalogues with extreme-environment metadata.
3. Record metadata strength for each sample: measured condition, inferred condition, or keyword-only.
4. Predict or retrieve protein functions using UniProt, BRENDA, InterPro/eggNOG, and CAZy/dbCAN where relevant.
5. Cluster homologs by enzyme family.
6. Attach GTDB taxonomy.
7. Retrieve AlphaFold DB structures or queue structure prediction for top sequences not covered.

## 7. Feature Engineering

Environment features:

- Extreme-condition type.
- Measured condition value where available.
- Metadata strength.
- Environmental uniqueness.
- Replicate/study support.

Enzyme features:

- Family/domain annotation.
- Catalytic motif conservation.
- Best characterized neighbor.
- Sequence novelty within family.
- Structure confidence.
- Active-site conservation.
- Predicted secretion/localization where relevant.

Commercial relevance:

- Assay availability.
- Industrial use class.
- Cofactor/substrate cost.
- Expression feasibility.
- Safety of source organism.

## 8. Ranking

```text
score =
  0.18 * environment_extremeness
+ 0.17 * catalytic_confidence
+ 0.15 * predicted_or_reference_stability
+ 0.14 * novelty
+ 0.12 * structure_and_active_site_confidence
+ 0.10 * commercial_relevance
+ 0.08 * metadata_strength
+ 0.06 * expression_and_safety_feasibility
```

Do not collapse all enzyme classes into one ranking. Publish family and environment track rankings.

## 9. Validation Plan

Computational:

- Check that each environment label comes from metadata, not only project title.
- Confirm top candidates are complete proteins.
- Compare to characterized homologs and BRENDA condition data.
- Manually inspect motifs and structures for the top 10 per track.

Experimental:

- Express top family-specific candidates.
- Test activity under standard conditions first.
- Test stress tolerance only after baseline activity is confirmed.
- Compare to a known enzyme benchmark.

## 10. Deliverables

- `extreme_environment_samples.csv`
- `extremophile_enzyme_atlas.parquet`
- `track_rankings/`
- `top_candidate_packets/`
- `atlas_summary.md`

## 11. Completion Checklist

- [ ] Environment ontology and keyword map recorded.
- [ ] Metadata strength scored for all samples.
- [ ] Enzyme families ranked by track.
- [ ] Top candidates have catalytic motif and structure review.
- [ ] Stability claims separated into measured, inferred, and predicted.
- [ ] Candidate packets include assay recommendations and benchmarks.

