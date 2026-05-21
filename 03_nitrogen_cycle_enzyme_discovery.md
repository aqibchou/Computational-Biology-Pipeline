# Nitrogen-Cycle Enzyme Discovery

## 1. Objective

Mine soil, rhizosphere, aquatic, wastewater, and environmental genomes for nitrogen-cycle enzymes and pathway configurations relevant to agriculture, fertilizer efficiency, and emissions reduction.

## 2. Hypotheses

- Underexplored microbial lineages encode nitrogen-cycle variants with useful environmental tolerance or pathway coupling.
- Genomic neighborhoods and co-occurring marker genes can distinguish complete pathway potential from isolated annotation hits.
- Nitrous oxide reduction and plant-available nitrogen pathways are especially valuable because they connect microbial function to climate and agriculture outcomes.

## 3. Required Source IDs

Required:

- `MG-MGNIFY`
- `MG-GENOMES`
- `TAX-GTDB`
- `REF-UNIPROT`
- `ENZ-BRENDA`
- `ECO-EMP`

Conditional:

- `GEN-SRA`
- `PATH-KEGG`
- `PATH-METACYC`
- `ENZ-RHEA`

## 4. Target Pathways

Core pathways:

- Nitrogen fixation.
- Nitrification.
- Denitrification.
- Ammonia oxidation.
- Nitrous oxide reduction.
- Urea metabolism.
- Nitrate/nitrite assimilation and dissimilation.

Marker families to track:

- Nitrogenase-associated genes.
- Ammonia monooxygenase.
- Hydroxylamine oxidoreductase.
- Nitrate and nitrite reductases.
- Nitric oxide reductases.
- Nitrous oxide reductase.
- Urease and accessory genes.

Use exact HMMs and gene names from the selected annotation database at run time; do not rely on informal marker names without recording the model source.

## 5. Data Build

1. Select soil, rhizosphere, freshwater, wastewater, wetland, and agricultural datasets with strong metadata.
2. Prefer MGnify/MGnify Genomes processed records for first pass.
3. Build pathway marker HMM/profile sets from UniProt/InterPro/eggNOG and, if licensed, KEGG/MetaCyc.
4. Search genomes/MAGs for pathway completeness.
5. Normalize taxonomy using GTDB.
6. Record environmental variables: crop/plant host, soil type, fertilizer exposure, oxygen status, salinity, pH, temperature, and geography when available.

## 6. Feature Engineering

Pathway features:

- Marker gene presence/absence.
- Pathway completeness score.
- Operon or neighborhood compactness.
- Co-occurrence of transporters, regulators, and cofactor biosynthesis genes.
- Copy number normalized by genome completeness.

Environment features:

- Rhizosphere versus bulk soil.
- Fertilized versus unfertilized when metadata allows.
- Oxygen/anaerobic context.
- Wetland/wastewater/soil source.
- Plant association and crop type.

Novelty and utility:

- Taxonomic novelty.
- Sequence divergence from characterized enzymes.
- Evidence for N2O reduction or reduced nitrogen loss.
- Plant-associated context.

## 7. Ranking

```text
score =
  0.22 * pathway_completeness
+ 0.18 * target_outcome_relevance
+ 0.16 * genomic_context_support
+ 0.14 * environment_metadata_strength
+ 0.12 * taxonomic_or_sequence_novelty
+ 0.10 * feasibility_for_isolation_or_assay
+ 0.08 * annotation_confidence
```

Maintain separate rankings for:

- Novel nitrogenase-associated clusters.
- High-confidence nitrous oxide reducers.
- Rhizosphere nitrogen-availability candidates.
- Microbiome signatures linked to nitrogen-use efficiency.

## 8. Validation Plan

Computational:

- Confirm pathway completeness is not caused by contamination or binning artifacts.
- Review co-localization for multi-gene pathways.
- Compare closest characterized enzymes in UniProt/BRENDA.
- Check whether candidate taxa are plausible for the source environment.

Experimental or field handoff:

- qPCR/metagenomic validation of marker genes in independent samples.
- Microcosm assays for N2O reduction or nitrogen transformation.
- Plant-growth or soil nitrogen assays with appropriate controls.
- Avoid agronomic claims without replicated field or greenhouse evidence.

## 9. Deliverables

- `nitrogen_pathway_candidates.csv`
- `n2o_reducer_shortlist.csv`
- `rhizosphere_nitrogen_signature.md`
- `candidate_packets/`
- `validation_assay_plan.md`

## 10. Completion Checklist

- [ ] Biome and metadata filters are recorded.
- [ ] Marker model sources and thresholds are recorded.
- [ ] MAG completeness/contamination handled before pathway scoring.
- [ ] Pathway completeness is separated from single-gene hits.
- [ ] Top candidates have GTDB taxonomy and genomic-neighborhood evidence.
- [ ] Agricultural or climate impact claims are labeled as hypotheses unless experimentally validated.

