# Rare Chemistry and New Enzyme Reaction Discovery

## 1. Objective

Identify proteins that may catalyze reactions poorly represented in current enzyme databases, with emphasis on rare cofactors, unusual active-site residues, atypical genomic neighborhoods, and structural outliers near known enzyme families.

## 2. Hypotheses

- Some proteins annotated as unknown or generic family members preserve catalytic folds but diverge at substrate-binding or cofactor-positioning residues.
- Genomic neighborhoods can reveal substrate or pathway context for proteins with weak sequence annotation.
- The strongest rare-chemistry candidates combine fold plausibility, active-site novelty, pathway context, and a tractable assay.

## 3. Required Source IDs

Required:

- `REF-UNIPROT`
- `STR-AFDB`
- `ENZ-BRENDA`
- `ENZ-RHEA`
- `CHEM-PUBCHEM`
- `MG-MGNIFY`

Conditional:

- `BGC-MIBIG`
- `BGC-ANTISMASH`
- `PATH-METACYC`
- `STR-PDB`

## 4. Target Domains

Focus areas:

- Halogenation.
- C-H activation.
- Dehalogenation.
- Redox chemistry.
- Stereoselective synthesis.
- Rare sugar transformations.
- Organosulfur metabolism.
- Organophosphorus metabolism.
- Unusual cofactor-dependent transformations.

## 5. Data Build

1. Build reference reaction sets from Rhea, BRENDA, UniProt, and PDB where available.
2. Identify known catalytic folds and motifs for each chemistry class.
3. Search MGnify and UniProt unreviewed/unknown proteins for remote homologs.
4. Attach AlphaFold DB structures or predict structures for top unresolved sequences.
5. Search structural neighbors with Foldseek/PDB.
6. Build genomic-neighborhood context from MGnify Genomes or source assemblies.
7. Link substrates/products to PubChem and Rhea IDs where possible.

## 6. Feature Engineering

Rare-chemistry features:

- Known fold match with sequence divergence.
- Conserved catalytic residues.
- Novel substrate-binding pocket residues.
- Unusual cofactor-binding motifs.
- Pathway-neighborhood support.
- Co-localized transporter or substrate-processing genes.
- Environment suggesting unusual substrate exposure.

Novelty features:

- Unknown/generic UniProt annotation.
- Low identity to characterized Swiss-Prot enzymes.
- Structural similarity higher than sequence similarity.
- Outlier position in family tree or embedding space.

Feasibility:

- Soluble protein size.
- Cofactor availability.
- Safe and available substrates.
- Assay readout simplicity.

## 7. Ranking

```text
score =
  0.20 * fold_and_active_site_plausibility
+ 0.18 * reaction_novelty
+ 0.16 * genomic_context_support
+ 0.14 * assay_feasibility
+ 0.12 * structure_confidence
+ 0.10 * environmental_relevance
+ 0.06 * taxonomic_novelty
+ 0.04 * safety_score
```

Keep separate queues for experimentally tractable chemistry and frontier exploratory chemistry.

## 8. Validation Plan

Computational:

- Manual active-site inspection.
- Rhea reaction mapping and gap analysis.
- Structural superposition with experimentally characterized enzymes.
- Pocket comparison against closest known function.

Experimental:

- Begin with broad substrate panels only after safe substrate selection.
- Use LC-MS or colorimetric assays depending on reaction class.
- Confirm products by analytical chemistry before naming a new reaction.

## 9. Deliverables

- `rare_chemistry_candidates.csv`
- `reaction_gap_map.tsv`
- `structure_neighbor_table.tsv`
- `top_candidate_packets/`
- `assay_design_notes.md`

## 10. Completion Checklist

- [ ] Reaction classes mapped to Rhea/BRENDA identifiers where possible.
- [ ] Top candidates have both sequence and structure evidence.
- [ ] Genomic-neighborhood support recorded.
- [ ] Assay feasibility and substrate safety assessed.
- [ ] New-reaction claims withheld until product chemistry is validated.

