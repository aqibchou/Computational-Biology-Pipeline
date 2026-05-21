# Industrial Biocatalyst Discovery

## 1. Objective

Find enzymes from environmental sequence resources that are plausible industrial biocatalysts under harsh or useful process conditions: high temperature, salinity, organic solvent exposure, extreme pH, high substrate load, metal exposure, or detergent exposure.

## 2. Hypotheses

- Extreme-environment homologs of known industrial enzyme families can preserve catalytic motifs while improving stability or process tolerance.
- Genomic context and environmental metadata can identify substrate relevance before wet-lab screening.
- A shortlist is valuable only when it contains assayable sequences with conserved active sites and clear process-condition hypotheses.

## 3. Required Source IDs

Required:

- `MG-MGNIFY`
- `MG-GENOMES`
- `REF-UNIPROT`
- `ENZ-BRENDA`
- `STR-AFDB`
- `TAX-GTDB`

Conditional:

- `CAZ-CAZY`
- `CAZ-DBCAN`
- `ENZ-RHEA`
- `STR-PDB`
- `GEN-SRA`

## 4. Target Enzyme Classes

Primary target classes:

- Lipases and esterases.
- Proteases.
- Nitrilases.
- Transaminases.
- Ketoreductases.
- Monooxygenases.
- Peroxidases.
- Dehalogenases.
- Glycosidases, cellulases, xylanases, and laccases.

Track process-condition goals separately:

- Thermostable.
- Halotolerant.
- Acid-stable.
- Alkali-stable.
- Solvent-tolerant.
- Detergent-tolerant.
- Metal-tolerant.

## 5. Data Build

1. Build positive-control seed sets from Swiss-Prot, BRENDA, and reviewed industrial enzyme literature.
2. Record catalytic motifs, EC/Rhea reactions, known substrate classes, pH optima, temperature optima, cofactors, and organism sources.
3. Search MGnify proteins/MGnify Genomes by sequence profiles or domain HMMs.
4. Cluster hits with MMseqs2 to remove near duplicates.
5. Normalize taxonomy with GTDB.
6. Attach environment metadata and biome labels.
7. Pull AlphaFold DB models where available or queue local prediction for top candidates.

## 6. Feature Engineering

Function evidence:

- EC/Rhea match confidence.
- Domain/HMM hit e-value and coverage.
- Catalytic motif conservation.
- Active-site residue conservation.
- Best reviewed UniProt neighbor identity and coverage.

Stability/process evidence:

- Source environment condition match.
- Homolog temperature/pH optima from BRENDA.
- Predicted protein length and domain completeness.
- Salt-bridge, charged-surface, proline, glycine, and cysteine pattern features.
- Signal peptide or secretion evidence for extracellular enzymes.
- Structure confidence and active-site geometry.

Commercial practicality:

- Assay simplicity.
- Substrate availability.
- Cofactor cost.
- Expression feasibility.
- Safety flags from source organism and product.

## 7. Ranking

```text
score =
  0.20 * catalytic_confidence
+ 0.18 * process_condition_match
+ 0.16 * sequence_novelty
+ 0.14 * active_site_and_structure_confidence
+ 0.12 * assay_feasibility
+ 0.10 * expression_feasibility
+ 0.06 * genomic_context_support
+ 0.04 * safety_and_ip_risk_score
```

Maintain family-specific rankings rather than one global list so a large hydrolase family does not crowd out rarer chemistries.

## 8. Validation Plan

Computational:

- Manual motif review for top 20 per enzyme class.
- Foldseek or PDB comparison for structural analogs.
- BRENDA condition cross-check for closest characterized enzymes.
- Genomic-neighborhood review for substrate-processing genes.

Experimental handoff:

- Codon-optimized synthesis of top candidates.
- Expression screening in a safe microbial host.
- Activity assay under standard and target process conditions.
- Stability time-course under heat, pH, salt, solvent, detergent, or metal stress as relevant.

## 9. Deliverables

- `industrial_enzyme_candidates.csv`: scored enzyme table.
- `family_rankings/`: family-specific top lists.
- `top_candidate_packets/`: sequence, source, motif, structure, and assay packet for each lead.
- `assay_queue.md`: wet-lab assay design and stop/go criteria.

## 10. Completion Checklist

- [ ] Seed sets and BRENDA/UniProt releases recorded.
- [ ] Each candidate has a target process-condition hypothesis.
- [ ] Each candidate has catalytic motif evidence or is explicitly marked exploratory.
- [ ] Top candidates have structure confidence and active-site review.
- [ ] Ranking separates novelty from catalytic confidence.
- [ ] Wet-lab assays are feasible with non-hazardous substrates where possible.

