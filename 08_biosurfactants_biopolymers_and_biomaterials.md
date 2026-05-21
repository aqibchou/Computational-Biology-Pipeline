# Biosurfactants, Biopolymers, and Biomaterials

## 1. Objective

Mine microbial genomes and metagenomes for genes and pathways that could produce useful biological materials: biosurfactants, bioplastics, exopolysaccharides, adhesives, biofilms, melanins, silica/metal-binding proteins, and self-assembling proteins.

## 2. Hypotheses

- Material-producing pathways are enriched in environments with interfaces, stress, biofilms, metals, hydrocarbons, or desiccation.
- Candidate value increases when pathway evidence, secretion/export machinery, environmental context, and material assay feasibility align.
- This direction bridges biology and materials but requires careful separation between genomic potential and measured material performance.

## 3. Required Source IDs

Required:

- `MG-MGNIFY`
- `MG-GENOMES`
- `BGC-MIBIG`
- `BGC-ANTISMASH`
- `REF-UNIPROT`
- `ENZ-BRENDA`
- `CHEM-PUBCHEM`

Conditional:

- `CHEM-CHEMBL`
- `PATH-METACYC`
- `STR-AFDB`

## 4. Target Product Classes

Product/pathway classes:

- Lipopeptide and glycolipid biosurfactants.
- Polyhydroxyalkanoate and related biopolymer pathways.
- Exopolysaccharide synthesis/export loci.
- Adhesive and biofilm matrix proteins.
- Melanin biosynthesis.
- Silica-binding and metal-binding proteins.
- Self-assembling proteins and repetitive matrix proteins.

Applications:

- Biodegradable materials.
- Oil-spill cleanup.
- Soil stabilization.
- Cosmetics and food texture.
- Medical materials.
- Battery binder or coating concepts.

## 5. Data Build

1. Select environments likely to enrich material traits: oil-contaminated sites, marine interfaces, soil crusts, deserts, biofilms, sediments, saline habitats, and metal-rich environments.
2. Retrieve genomes/MAGs and metadata from MGnify/MGnify Genomes.
3. Run antiSMASH for biosurfactant-like BGCs and MIBiG dereplication.
4. Annotate polymer, EPS, PHA, melanin, secretion/export, and biofilm matrix genes using UniProt/BRENDA/InterPro.
5. Link predicted product classes to PubChem where molecular analogs are known.
6. Normalize taxonomy and deduplicate by species cluster/study.

## 6. Feature Engineering

Pathway features:

- Complete biosynthetic pathway or BGC evidence.
- Export/secretion machinery.
- Regulatory genes.
- Repeated or modular protein architecture.
- Predicted extracellular localization.
- Polymer precursor metabolism support.

Material-use features:

- Source environment matching target application.
- Known product-class utility.
- Expected assay simplicity.
- Product recovery feasibility.
- Safety of source organism and product.
- Novelty relative to MIBiG/UniProt.

## 7. Ranking

```text
score =
  0.20 * pathway_or_bgc_completeness
+ 0.17 * material_application_fit
+ 0.15 * source_environment_support
+ 0.13 * export_or_extracellular_evidence
+ 0.12 * novelty
+ 0.10 * assay_and_recovery_feasibility
+ 0.08 * taxonomic_and_genome_quality
+ 0.05 * safety_score
```

Produce separate queues for biosurfactants, biopolymers/EPS, and proteinaceous materials.

## 8. Validation Plan

Computational:

- Confirm complete pathway/BGC rather than isolated enzyme hits.
- Dereplicate against MIBiG and known product classes.
- Check source-environment plausibility.
- Flag pathogen or toxin-associated producers.

Experimental:

- Biosurfactant surface-tension/emulsification assays.
- Polymer staining/GC-MS/NMR depending on product class.
- EPS rheology and composition assays.
- Adhesion/coating/material property assays with non-pathogenic expression hosts where possible.

## 9. Deliverables

- `biomaterials_pathway_candidates.csv`
- `biosurfactant_bgc_shortlist.csv`
- `biopolymer_eps_shortlist.csv`
- `protein_materials_shortlist.csv`
- `candidate_packets/`

## 10. Completion Checklist

- [ ] Product classes separated by pathway type.
- [ ] BGC/pathway completeness recorded.
- [ ] MIBiG/antiSMASH dereplication completed.
- [ ] Export/extracellular evidence reviewed for top candidates.
- [ ] Source organism safety flags documented.
- [ ] Material-performance claims withheld until assay evidence exists.

