# Plant-Growth-Promoting Microbiome Discovery

## 1. Objective

Identify microbial strains, MAGs, and pathway signatures associated with plant growth, drought tolerance, salinity tolerance, nutrient availability, and pathogen resistance.

## 2. Hypotheses

- Plant-associated microbiomes contain repeated pathway combinations linked to resilience traits.
- Candidate organisms are stronger when multiple plant-benefit mechanisms co-occur in the same genome or stable community context.
- Phenotype metadata is often incomplete, so confidence must be graded separately from genomic potential.

## 3. Required Source IDs

Required:

- `MG-MGNIFY`
- `MG-GENOMES`
- `ECO-EMP`
- `TAX-GTDB`
- `REF-UNIPROT`
- `ENZ-BRENDA`

Conditional:

- `GEN-SRA`
- `BGC-ANTISMASH`
- `BGC-MIBIG`
- `PATH-KEGG`
- `PATH-METACYC`

## 4. Target Functions

Track genes/pathways related to:

- Phosphate solubilization.
- Nitrogen fixation and nitrogen availability.
- Siderophore production.
- ACC deaminase.
- Indole acetic acid production.
- Osmoprotectant synthesis.
- Antifungal metabolites.
- Biofilm formation.
- Root colonization and adhesion.
- Salinity and drought stress response.

## 5. Data Build

1. Freeze plant/rhizosphere/root/endophyte datasets from MGnify and EMP-derived resources.
2. Capture crop/plant host, tissue compartment, soil type, stress condition, phenotype, and treatment metadata where available.
3. Normalize genomes/MAGs through GTDB.
4. Annotate target functions using UniProt, InterPro/eggNOG, BRENDA, and conditional pathway databases.
5. Run antiSMASH for BGC-mediated antifungal/siderophore/natural-product features where genome assemblies permit.
6. Build a community-level matrix: sample by pathway signature.

## 6. Feature Engineering

Genome/MAG features:

- Plant-benefit pathway count and completeness.
- Co-occurrence of complementary functions.
- Root-colonization and biofilm evidence.
- Siderophore/BGC evidence.
- Stress-tolerance gene signatures.
- Taxonomic novelty and known safety status.

Dataset features:

- Host plant/crop.
- Tissue compartment.
- Stress condition.
- Treatment status.
- Replication level.
- Phenotype metadata strength.

## 7. Ranking

```text
score =
  0.20 * plant_benefit_pathway_support
+ 0.17 * phenotype_metadata_strength
+ 0.15 * multi_trait_complementarity
+ 0.14 * source_relevance_to_target_crop_or_stress
+ 0.12 * genome_quality_and_taxonomy_confidence
+ 0.10 * feasibility_for_isolation_or_formulation
+ 0.07 * novelty
+ 0.05 * safety_score
```

Create separate outputs for:

- Candidate strains/MAGs.
- Community pathway signatures.
- Crop/stress-specific signatures.
- Antifungal natural-product candidates.

## 8. Validation Plan

Computational:

- Check phenotype labels against original study metadata.
- Confirm target genes are not isolated false positives.
- Identify whether candidate taxa have known plant-beneficial or plant-pathogenic reports.
- Separate isolate-available candidates from MAG-only candidates.

Experimental:

- In vitro phosphate, siderophore, ACC deaminase, IAA, osmotic stress, or antifungal screens.
- Plant seedling assays under controlled stress.
- Greenhouse validation for top microbial consortia.
- Field validation only after greenhouse replication.

## 9. Deliverables

- `plant_growth_candidate_microbes.csv`
- `crop_stress_pathway_signatures.csv`
- `antifungal_bgc_subqueue.csv`
- `candidate_packets/`
- `greenhouse_validation_plan.md`

## 10. Completion Checklist

- [ ] Plant/rhizosphere dataset accessions recorded.
- [ ] Host, compartment, and stress metadata scored for strength.
- [ ] Candidate functions have model IDs and thresholds.
- [ ] Pathogen/safety flags checked for top taxa.
- [ ] Candidate strains/MAGs are separated from community signatures.
- [ ] Crop-resilience claims are not made without plant assay evidence.

