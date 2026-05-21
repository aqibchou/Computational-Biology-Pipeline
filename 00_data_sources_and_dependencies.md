# Data Sources And Dependencies

This file explains the source and tool backbone behind the completed computational biology pipeline. It is a record of what the campaign depended on, not a step-by-step execution guide.

Access date for the original registry: 2026-05-14.

## Source Backbone

The work relied on public genomics, protein, enzyme, structure, pathway, BGC, and chemistry resources. The table below preserves the role each source played in the completed screens.

| ID | Source | Role In This Project |
|---|---|---|
| `GEN-SRA` | NCBI Sequence Read Archive | Raw sequencing provenance and possible expansion source when processed resources were not enough. |
| `GEN-ENA` | European Nucleotide Archive | Public sequence and assembly provenance, especially through MGnify-linked records. |
| `GEN-DDBJ` | DNA Data Bank of Japan | INSDC provenance partner for nucleotide records. |
| `MG-MGNIFY` | MGnify | Main processed metagenomics and microbiome analysis backbone. |
| `MG-GENOMES` | MGnify Genomes | Primary genome and MAG source for environmental, rhizosphere, marine, desert, and other microbial candidates. |
| `TAX-GTDB` | Genome Taxonomy Database | Taxonomic normalization for bacterial and archaeal genomes. |
| `STR-AFDB` | AlphaFold Protein Structure Database | Predicted structure context for enzyme prioritization and confidence review. |
| `STR-PDB` | RCSB Protein Data Bank | Experimental structure reference where available. |
| `REF-UNIPROT` | UniProt | Reviewed and unreviewed protein reference labels, closest-hit context, and functional anchors. |
| `ENZ-BRENDA` | BRENDA | Enzyme reaction, condition, and literature-backed family context. |
| `ENZ-RHEA` | Rhea | Curated reaction identifiers and EC/Rhea mapping for enzyme and rare-chemistry candidates. |
| `CAZ-CAZY` | CAZy | Carbohydrate-active enzyme family context. |
| `CAZ-DBCAN` | dbCAN/run_dbcan | CAZyme and polysaccharide-related annotation support. |
| `BGC-MIBIG` | MIBiG | Experimentally characterized BGC reference set for dereplication and novelty context. |
| `BGC-ANTISMASH` | antiSMASH DB and local antiSMASH outputs | BGC detection, product-class framing, and whole-MAG BGC support. |
| `CHEM-PUBCHEM` | PubChem | Compound and bioactivity cross-reference context where chemistry became relevant. |
| `CHEM-CHEMBL` | ChEMBL | Bioactivity and small-molecule context for natural-product interpretation. |
| `AMR-CARD` | CARD | AMR context for surveillance-style safety triage, not resistance engineering. |
| `AMR-NCBI` | NCBI AMRFinderPlus | AMR and related gene screening context. |
| `ECO-EMP` | Earth Microbiome Project | Environmental and biome context. |
| `PATH-KEGG` | KEGG | Conditional pathway interpretation source, with licensing limitations. |
| `PATH-METACYC` | BioCyc/MetaCyc | Conditional pathway interpretation source, with subscription/access limitations. |
| `DOM-INTERPRO` | InterPro/InterProScan | Domain and functional-site context. |
| `ORTH-EGGNOG` | eggNOG/eggNOG-mapper | Orthology and broad functional annotation context. |
| `CLUST-MMSEQS` | MMseqs2 | Homolog clustering and dereplication. |
| `STR-FOLDSEEK` | Foldseek | Structural-neighbor search context where needed. |

## How The Sources Mapped To The Completed Screens

| Completed module | Main source types used |
|---|---|
| Plan 01 natural products and BGCs | MGnify Genomes, GTDB, antiSMASH, MIBiG, BiG-SCAPE, PubChem/ChEMBL context |
| Plan 02 industrial biocatalysts | MGnify/MGnify Genomes, UniProt, BRENDA, Rhea, Pfam/HMMER, AlphaFold/ColabFold |
| Plan 03 nitrogen cycle | MGnify/MGnify Genomes, GTDB, UniProt/BRENDA context, pathway markers, IQ-TREE |
| Plan 04 plant-growth promotion | MGnify Genomes, source metadata, GTDB, ANI/skani/fastANI reference context, trait annotations |
| Plan 05 natural enzyme stability | Enzyme candidate tables, UniProt/BRENDA, ColabFold, IQ-TREE, stability-feature proxies |
| Plan 06 rare chemistry | UniProt, BRENDA, Rhea/EC mapping, structure models, ligand-pocket and phylogeny context |
| Plan 07 biomaterials | MGnify Genomes, BGC outputs, UniProt/InterPro/dbCAN-style material annotations, recovery and safety context |
| Plan 08 extremophile atlas | MGnify/MGnify Genomes, enzyme candidate queues, source manifests, checksums, stability-feature scoring |

## Compute And Tooling Context

The completed work mixed lightweight tabular processing, medium-weight annotation, and heavier structure or phylogeny hardening.

Lightweight layers included metadata freezing, accession tracking, candidate scoring, source manifest checks, and report generation in Python.

Medium-weight layers included sequence clustering, HMM/profile evidence, BGC caller output review, AMR/safety-context screening, CAZyme or pathway context, and candidate packet generation.

Heavier layers included BiG-SCAPE/MIBiG dereplication, candidate-specific ColabFold structure generation, IQ-TREE phylogenies, and ThermoMPNN aggregate summaries for the natural-stability module.

The repository keeps scripts and final report artifacts, but it does not keep large downloaded databases, temporary execution folders, model caches, raw Kaggle outputs, or other bulky intermediates.

## Why This File Is Kept

The source registry matters because it shows the project was not an isolated scoring exercise. The candidate claims were built from multiple public evidence layers, and each major module used sources appropriate to its biological question.

The file also helps future readers understand what would need to be refreshed before a new run: database versions, access terms, tool versions, source metadata, and release-specific identifiers can all change over time.
