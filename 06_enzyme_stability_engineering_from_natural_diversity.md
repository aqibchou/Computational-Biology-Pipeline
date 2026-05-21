# Enzyme Stability Engineering From Natural Diversity

## 1. Objective

Use natural enzyme diversity to identify sequence and structure patterns associated with thermostability, pH tolerance, salt tolerance, and solvent/detergent tolerance, then rank natural homologs and mutation ideas for engineering.

## 2. Hypotheses

- Stability-associated sequence patterns can be learned from characterized enzymes and extreme-environment homologs.
- Natural homologs from thermophiles, halophiles, acidophiles, alkaliphiles, and solvent-exposed environments provide practical variants before artificial design.
- Engineering suggestions must remain grounded in homolog evidence and structural context, not generic mutation folklore.

## 3. Required Source IDs

Required:

- `ENZ-BRENDA`
- `REF-UNIPROT`
- `STR-AFDB`
- `MG-MGNIFY`
- `MG-GENOMES`
- `TAX-GTDB`

Conditional:

- `STR-PDB`
- `STR-FOLDSEEK`
- `CAZ-DBCAN`

## 4. Data Build

1. Select enzyme families with BRENDA temperature and pH optima or stability data.
2. Build family-specific positive and negative examples using UniProt reviewed records where available.
3. Pull environmental homologs from MGnify/MGnify Genomes with biome labels.
4. Cluster homologs and create representative sequences at multiple identity thresholds.
5. Attach taxonomy, environment, BRENDA condition labels, and AlphaFold/PDB structure evidence.
6. Split by family before modeling to avoid leakage from close homologs.

## 5. Model Targets

Targets:

- Thermostability.
- pH tolerance.
- Salt tolerance.
- Solvent tolerance.
- Detergent tolerance.

Labels:

- Direct measured values from BRENDA/literature when available.
- Environment-derived weak labels only when clearly marked.
- No single model should mix measured and weak labels without an explicit label-source feature.

## 6. Feature Engineering

Sequence features:

- Amino acid composition.
- Charged residue distribution.
- Proline/glycine patterns.
- Cysteine and disulfide potential.
- Predicted signal peptide and secretion.
- Motif conservation.
- Family-specific MSA positions.

Structure features:

- Predicted confidence.
- Surface charge.
- Salt-bridge/contact proxies.
- Core packing proxies.
- Loop length and disorder proxies.
- Active-site distance from proposed mutations.

Context features:

- Source environment.
- GTDB taxonomy.
- BRENDA organism condition records.
- Industrial assay relevance.

## 7. Ranking

```text
score =
  0.20 * measured_or_reference_stability_support
+ 0.17 * environment_condition_match
+ 0.15 * catalytic_motif_integrity
+ 0.14 * structure_confidence
+ 0.12 * novelty_within_family
+ 0.10 * expression_and_assay_feasibility
+ 0.07 * model_uncertainty_calibration
+ 0.05 * safety_score
```

Produce two outputs:

- Natural homolog shortlist.
- Mutation suggestion shortlist, only when supported by family alignments and structure context.

## 8. Validation Plan

Computational:

- Family-wise cross-validation.
- Leave-clade-out evaluation when enough data exists.
- Negative controls for non-stability-correlated families.
- Manual inspection of proposed mutations near active sites.

Experimental:

- Express natural homologs first.
- Measure activity and residual activity across target stress condition.
- Only test mutation suggestions after the natural-homolog baseline is established.

## 9. Deliverables

- `stability_training_table.csv`
- `natural_stable_homologs.csv`
- `mutation_suggestions.csv`
- `model_card.md`
- `top_candidate_packets/`

## 10. Completion Checklist

- [ ] Measured labels and weak environmental labels separated.
- [ ] Family splits prevent close-homolog leakage.
- [ ] Top homologs preserve catalytic motifs.
- [ ] Structure confidence recorded before mutation suggestions.
- [ ] Mutation suggestions avoid active-site disruption unless explicitly justified.
- [ ] Claims distinguish predicted stability from measured stability.

