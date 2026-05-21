# Novel Antibiotics and Antimicrobial Natural Products

## 1. Objective

Mine environmental genomes and MAGs for biosynthetic gene clusters (BGCs) likely to encode novel antimicrobial natural products, then produce a ranked top-100 BGC candidate packet for natural-products collaborators.

## 2. Hypotheses

- Underexplored environments and rare taxa contain BGCs distant from known MIBiG clusters.
- BGCs with conserved biosynthetic logic but unusual tailoring domains, resistance genes, or transport/regulatory context are more likely to encode bioactive products.
- Novelty is not sufficient; candidates must also have enough completeness, product-class interpretability, and expression feasibility to justify wet-lab follow-up.

## 3. Required Source IDs

Required:

- `MG-GENOMES`
- `TAX-GTDB`
- `BGC-MIBIG`
- `BGC-ANTISMASH`
- `CHEM-PUBCHEM`
- `CHEM-CHEMBL`

Conditional:

- `GEN-SRA`
- `GEN-ENA`
- `STR-AFDB`
- `STR-FOLDSEEK`
- `AMR-CARD`

## 4. Data Build

Primary first pass:

1. Freeze selected MGnify Genomes catalogues from competitive environments: soil, marine sediments, sponge/invertebrate-associated microbiomes, insect microbiomes, rhizosphere, and extreme habitats.
2. Pull antiSMASH DB BGCs for the same taxa or environments where already available.
3. Normalize taxonomy with GTDB release recorded in the manifest.
4. Compare candidate clusters to MIBiG 4.0 JSON entries and antiSMASH DB neighborhoods.
5. Link predicted product classes and known analog molecules to PubChem and ChEMBL where possible.

Raw-read expansion only after the first pass:

- Select a narrow environment/function target.
- Assemble with explicit QC, contamination, binning, and contig-edge rules.
- Re-run antiSMASH locally and record all assembly failures.

## 5. Targets

Prioritize:

- NRPS clusters.
- Type I, II, and III PKS clusters.
- Hybrid PKS-NRPS clusters.
- RiPP clusters.
- Terpene clusters.
- Siderophore clusters.
- Unusual halogenase, methyltransferase, glycosyltransferase, or oxidase tailoring modules.
- Clusters from rare GTDB lineages or under-sampled biomes.

Deprioritize:

- Highly fragmented clusters at contig edges.
- Clusters nearly identical to MIBiG entries unless a novel tailoring block is present.
- Candidates dominated by common household genera or heavily sampled pathogens unless the goal is method benchmarking.

## 6. Feature Engineering

BGC features:

- BGC class and antiSMASH confidence.
- Core biosynthetic gene count.
- Contig-edge flag and completeness proxy.
- Domain architecture and module order.
- Predicted substrate specificity for NRPS/PKS modules.
- Tailoring enzyme diversity.
- Resistance, transporter, regulator, and self-protection genes nearby.
- Cluster length and gene density.

Novelty features:

- Best MIBiG cluster similarity.
- Best antiSMASH DB neighbor similarity.
- BiG-SCAPE family membership if computed.
- Taxonomic rarity of the cluster family.
- Environment rarity and sampling depth.
- Product-class novelty versus known PubChem/ChEMBL compounds.

Feasibility features:

- Complete core biosynthetic genes.
- Manageable cluster size for cloning or refactoring.
- Presence of native regulatory clues.
- Availability of source isolate versus MAG-only origin.
- Product-class assay availability.

## 7. Ranking

```text
score =
  0.22 * cluster_novelty
+ 0.18 * product_class_antimicrobial_plausibility
+ 0.16 * cluster_completeness
+ 0.13 * rare_taxon_or_environment
+ 0.12 * tailoring_and_resistance_context
+ 0.10 * expression_feasibility
+ 0.06 * chemical_dereplication_gap
+ 0.03 * safety_and_compliance_score
```

Produce separate ranked lists for:

- High-confidence antimicrobial-like BGCs.
- High-novelty BGCs with uncertain bioactivity.
- Expression-ready clusters from isolates.
- MAG-only exploratory clusters.

## 8. Validation Plan

Computational validation:

- Confirm source accessions and taxonomy.
- Confirm BGC is not a near-duplicate of known MIBiG clusters.
- Inspect domain architecture manually for the top 100.
- Search PubChem/ChEMBL for predicted product-family analogs.
- Flag possible toxin, virulence, or AMR-adjacent clusters for biosafety review.

Wet-lab handoff:

- Synthetic biology or native-host expression.
- LC-MS/MS metabolomics with molecular networking.
- Bioactivity assays against safe indicator panels selected by collaborators.
- Dereplication against known natural products before claiming novelty.

## 9. Safety

This plan is for antimicrobial discovery and dereplication, not pathogen optimization. Do not engineer virulence, enhance resistance, or distribute hazardous clusters without institutional review. AMR genes near BGCs are context features and safety flags, not engineering targets.

## 10. Deliverables

- `bgc_candidate_table.csv`: top candidates with source accessions, taxonomy, BGC class, novelty, utility, feasibility, and safety flags.
- `top_100_bgc_packets/`: one markdown packet per top candidate.
- `mibig_dereplication.tsv`: MIBiG nearest-neighbor evidence.
- `chemical_crosslinks.tsv`: PubChem/ChEMBL links for predicted product classes.
- `natural_products_summary.md`: collaborator-facing summary and validation queue.

## 11. Completion Checklist

- [ ] MGnify Genomes and antiSMASH DB versions recorded.
- [ ] MIBiG version recorded.
- [ ] All candidates have source genome/MAG and contig identifiers.
- [ ] GTDB taxonomy attached or failure reason recorded.
- [ ] Top 100 have manual domain architecture review.
- [ ] Near-known clusters are separated from high-novelty clusters.
- [ ] Safety flags reviewed before wet-lab recommendation.
- [ ] Claims are limited to computational BGC potential unless metabolomics or assay data exists.

