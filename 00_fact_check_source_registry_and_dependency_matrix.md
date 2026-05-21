# Fact-Check Source Registry and Dependency Matrix

Access date for this registry: 2026-05-14  
Instruction source: `../genomics.md`

## Source Registry

| ID | Source | URL | Verified fact or use | Access and license notes |
|---|---|---|---|---|
| GEN-SRA | NCBI Sequence Read Archive | https://www.ncbi.nlm.nih.gov/sra/ | NCBI describes SRA as the largest public repository of high-throughput sequencing data; it accepts all branches of life plus metagenomic and environmental surveys and stores raw sequencing and alignment data. | Open public and controlled-access data; use SRA Toolkit/cloud responsibly and record BioProject, BioSample, and Run accessions. |
| GEN-ENA | European Nucleotide Archive | https://www.ebi.ac.uk/ena/browser/home | Primary INSDC archive used by MGnify for public and submitted sequence data. | Open archive; record ENA study, sample, run, and assembly accessions. |
| GEN-DDBJ | DNA Data Bank of Japan | https://www.ddbj.nig.ac.jp/index-e.html | INSDC partner for nucleotide sequence data. | Open archive; record accession provenance. |
| MG-MGNIFY | MGnify | https://docs.mgnify.org/src/docs/about.html | MGnify is a freely available hub for metagenomic, metatranscriptomic, amplicon, and assembly data with functional and taxonomic analyses plus REST API access; the 2023 MGnify paper reported nearly half a million analyses. | Prefer as first-pass processed data source; record analysis pipeline version and MGYA/MGYS accessions. |
| MG-GENOMES | MGnify Genomes | https://docs.mgnify.org/src/docs/mgnify-genomes.html | Provides biome-specific catalogues of prokaryotic genomes and functional annotations; catalogue update workflow filters low-quality genomes and dereplicates strain/species representatives. | Use quality score, contamination, completeness, catalogue version, genome accession, and biome catalogue in manifests. |
| TAX-GTDB | Genome Taxonomy Database | https://gtdb.ecogenomic.org/ | As of release 11-RS232 dated 2026-04-15, GTDB lists 901,341 genomes, including 878,998 bacteria and 22,343 archaea. | Use for bacterial/archaeal taxonomy normalization; record release. |
| STR-AFDB | AlphaFold Protein Structure Database | https://alphafold.ebi.ac.uk/ | AlphaFold DB provides open access to over 200 million protein structure predictions; the 2024 database paper reports structure coverage for over 214 million protein sequences, and the site advertises March 2026 protein-complex updates. | Predicted structures only; record model version and confidence metrics. |
| STR-PDB | RCSB Protein Data Bank | https://www.rcsb.org/ | Archive and portal for experimentally determined 3D structures from the PDB plus computed structure model access. | Experimental structures are preferred anchors for active-site validation. |
| REF-UNIPROT | UniProt | https://www.ebi.ac.uk/uniprot/index | UniProt provides a comprehensive, high-quality, freely accessible protein sequence and functional information resource; UniProtKB includes reviewed Swiss-Prot and unreviewed TrEMBL. | Use Swiss-Prot labels as higher-confidence references than TrEMBL. |
| ENZ-BRENDA | BRENDA | https://www.brenda-enzymes.org/ | BRENDA release 2026.1 was visible on 2026-05-14; online BRENDA is free under CC BY 4.0 and covers enzyme classes, reactions, specificity, kinetic and condition data. | Respect terms for downloads/API; record release and query date. |
| ENZ-RHEA | Rhea | https://www.rhea-db.org/ | Expert-curated biochemical and transport reaction knowledgebase and UniProtKB standard for enzyme/transporter annotation. | Use for reaction normalization and EC/Rhea mapping. |
| CAZ-CAZY | CAZy | https://www.cazy.org/ | CAZy describes families of structurally related catalytic and carbohydrate-binding modules that degrade, modify, or create glycosidic bonds. | Specialist carbohydrate-active enzyme family reference. |
| CAZ-DBCAN | dbCAN/run_dbcan | https://dbcan.readthedocs.io/ | run_dbcan is the standalone dbCAN3 tool for automated CAZyme annotation using HMMER, DIAMOND, dbCAN_sub, CGC, and substrate prediction components. | Record dbCAN database version and HMM thresholds. |
| BGC-MIBIG | MIBiG | https://mibig.secondarymetabolites.org/ | MIBiG 4.0 describes an updated data standard and repository for experimentally characterized biosynthetic gene clusters with 3,059 curated entries. | Use as known-BGC reference; record JSON version or Zenodo release. |
| BGC-ANTISMASH | antiSMASH DB | https://antismash-db.secondarymetabolites.org/ | antiSMASH DB v4 contains 231,534 high-quality BGC regions from dereplicated high-quality microbial genomes and is generated with antiSMASH 7.1. | Use for precomputed BGC mining; full DB downloads are available. |
| CHEM-PUBCHEM | PubChem | https://www.ncbi.nlm.nih.gov/sites/guide/chemicals-bioassays/ | NCBI site guide describes PubChem BioAssay, Compound, and Substance plus FTP, download, and PUG programmatic access. | Use for compound IDs, structures, bioassays, toxicity, and cross-links. |
| CHEM-CHEMBL | ChEMBL | https://chembl.gitbook.io/chembl-interface-documentation/about | ChEMBL is a curated database of bioactive drug-like small molecules, structures, calculated properties, and abstracted bioactivities. | Use for antimicrobial/natural-product bioactivity cross-checks. |
| AMR-CARD | CARD | https://card.mcmaster.ca/about | CARD is an expert-curated AMR sequence and mutation collection organized by the Antibiotic Resistance Ontology; RGI predicts resistomes from genomic/metagenomic data. | Use for AMR surveillance only; record CARD/RGI versions. |
| AMR-NCBI | NCBI AMRFinderPlus | https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/ | AMRFinderPlus identifies AMR genes, resistance-associated point mutations, and select related gene classes using curated genes and HMMs. | Use with assembled nucleotide/protein sequences; record organism option and database version. |
| ECO-EMP | Earth Microbiome Project | https://earthmicrobiome.ucsd.edu/ | EMP is a systematic effort to characterize global microbial taxonomic and functional diversity using standardized sampling and open-science principles. | Useful for biome metadata, cross-environment ecology, and standard protocols. |
| PATH-KEGG | KEGG | https://kegg.net/en/licensing.html | KEGG has licensing constraints for FTP/mirror/API use beyond public website access. | Treat as conditional/licensed; do not assume bulk availability. |
| PATH-METACYC | BioCyc/MetaCyc | https://www.biocyc.org/ | BioCyc integrates genomes, metabolic networks, regulatory networks, protein features, orthologs, and curated pathway/genome databases; many BioCyc resources require subscription. | Treat broad BioCyc use as conditional/licensed; record free vs subscription source. |
| DOM-INTERPRO | InterPro/InterProScan | https://interpro-documentation.readthedocs.io/en/latest/interpro.html | InterPro integrates protein families, domains, and functional sites from member databases and adds functional annotation/GO terms. | Use for domain annotation; record member DB versions. |
| ORTH-EGGNOG | eggNOG/eggNOG-mapper | https://eggnogdb.org/ | Orthology assignments and functional predictions for comparative genomics. | Use for orthology and broad function transfer; record database version. |
| CLUST-MMSEQS | MMseqs2 | https://github.com/soedinglab/MMseqs2 | Fast and sensitive search and clustering suite for huge protein and nucleotide sequence sets. | Use for homolog clustering and dereplication. |
| STR-FOLDSEEK | Foldseek | https://www.nature.com/articles/s41587-023-01773-0 | Foldseek enables fast protein structure search at large scale. | Use for structural neighbors; confirm with local alignment/inspection for top hits. |

## Software Dependency Classes

Low compute:

- Accession retrieval: ENA browser/API, MGnify API, NCBI Entrez/SRA metadata, FTP downloads.
- Tabular processing: Python, pandas, duckdb, pyarrow.
- Sequence utilities: seqkit, fastp for small raw-read checks.
- Annotation lookup: UniProt REST, Rhea, BRENDA, PubChem PUG, ChEMBL API.

Medium compute:

- Assembly and gene prediction: MEGAHIT/metaSPAdes, Prodigal/Prodigal-GV, Prokka or Bakta.
- Homolog clustering: MMseqs2/Linclust.
- Domain annotation: InterProScan, HMMER, eggNOG-mapper, run_dbcan, AMRFinderPlus/RGI where relevant.
- BGC mining: antiSMASH, BiG-SCAPE/CORASON if cluster-family networking is needed.
- Structure search: AlphaFold DB downloads, Foldseek, TM-align.

Heavy compute:

- Large raw-SRA assembly, MAG binning, and dereplication.
- Local protein structure prediction for non-AFDB candidates.
- Large all-vs-all structure comparisons.
- Wet-lab expression, metabolomics, bioactivity, kinetics, greenhouse, or soil-microcosm assays.

## Plan-To-Source Matrix

| Plan | Required source IDs | Conditional source IDs |
|---|---|---|
| 01 antibiotics/natural products | MG-GENOMES, TAX-GTDB, BGC-MIBIG, BGC-ANTISMASH, CHEM-PUBCHEM, CHEM-CHEMBL | GEN-SRA, GEN-ENA, STR-AFDB, STR-FOLDSEEK, AMR-CARD |
| 02 industrial biocatalysts | MG-MGNIFY, MG-GENOMES, REF-UNIPROT, ENZ-BRENDA, STR-AFDB, TAX-GTDB | CAZ-CAZY, CAZ-DBCAN, ENZ-RHEA, STR-PDB, GEN-SRA |
| 03 nitrogen cycle | MG-MGNIFY, MG-GENOMES, TAX-GTDB, REF-UNIPROT, ENZ-BRENDA, ECO-EMP | GEN-SRA, PATH-KEGG, PATH-METACYC, ENZ-RHEA |
| 04 plant-growth microbiome | MG-MGNIFY, MG-GENOMES, ECO-EMP, TAX-GTDB, REF-UNIPROT, ENZ-BRENDA | GEN-SRA, BGC-ANTISMASH, BGC-MIBIG, PATH-KEGG, PATH-METACYC |
| 05 AMR surveillance | GEN-SRA, MG-MGNIFY, TAX-GTDB, AMR-CARD, AMR-NCBI | STR-AFDB, STR-FOLDSEEK, GEN-ENA, CHEM-PUBCHEM |
| 06 stability engineering | ENZ-BRENDA, REF-UNIPROT, STR-AFDB, MG-MGNIFY, MG-GENOMES, TAX-GTDB | STR-PDB, STR-FOLDSEEK, CAZ-DBCAN |
| 07 rare chemistry | REF-UNIPROT, STR-AFDB, ENZ-BRENDA, ENZ-RHEA, CHEM-PUBCHEM, MG-MGNIFY | BGC-MIBIG, BGC-ANTISMASH, PATH-METACYC, STR-PDB |
| 08 biosurfactants/materials | MG-MGNIFY, MG-GENOMES, BGC-MIBIG, BGC-ANTISMASH, REF-UNIPROT, ENZ-BRENDA, CHEM-PUBCHEM | CHEM-CHEMBL, PATH-METACYC, STR-AFDB |
| 09 extremophile atlas | MG-MGNIFY, MG-GENOMES, REF-UNIPROT, ENZ-BRENDA, STR-AFDB, TAX-GTDB | CAZ-DBCAN, GEN-SRA, ECO-EMP, STR-FOLDSEEK |
| 10 anomaly miner | REF-UNIPROT, STR-AFDB, ENZ-BRENDA, MG-MGNIFY, TAX-GTDB, BGC-MIBIG, CAZ-CAZY, CHEM-PUBCHEM | BGC-ANTISMASH, ENZ-RHEA, STR-PDB, STR-FOLDSEEK |

## Source-Use Rules

- Prefer official source pages and primary database papers over secondary summaries.
- Recheck release numbers and terms before execution.
- Do not mix database versions inside one candidate ranking unless the manifest records the reason.
- Treat predicted annotations as hypotheses. Upgrade evidence only when independent methods agree.
- For licensed/conditional sources such as KEGG and broad BioCyc access, define an open fallback before starting the run.
