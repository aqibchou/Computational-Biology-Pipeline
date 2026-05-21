# Shared Genomics Discovery Protocol

## 1. Objective

Provide a common execution standard for all genomics, metagenomics, microbiome, enzyme, biosynthetic-gene-cluster, and ecology discovery plans in this directory.

The standard is intentionally conservative: a computational hit is a candidate, not a demonstrated function. Strong claims require sequence evidence, metadata provenance, taxonomic context, annotation consistency, structure evidence, and either literature or experimental validation.

## 2. Core Pipeline

```text
environmental sequencing data
-> assemble reads or select existing assemblies/MAGs
-> predict genes and proteins
-> cluster homologs
-> annotate domains and enzyme families
-> infer structure and function
-> rank novelty, utility, feasibility, and safety
-> select candidates for synthesis, expression, assay, or field validation
```

## 3. Preferred Data Strategy

Start with processed resources:

- MGnify analyses and MGnify Genomes catalogues.
- antiSMASH DB for already predicted biosynthetic gene clusters.
- MIBiG, UniProt, BRENDA, CAZy/dbCAN, Rhea, CARD, and AlphaFold DB for reference labels.

Use raw SRA/ENA/DDBJ reads only after the target environment, function, and evidence model are defined. Raw-read discovery is powerful but expensive and error-prone because quality control, host removal, assembly, binning, annotation, dereplication, and contamination filtering all become part of the claim.

## 4. Reproducibility Requirements

Every experiment run must create a run manifest with:

- Plan file and git commit or file hash.
- Date and timezone.
- Source IDs and exact URLs or API endpoints.
- Query strings, filters, accession lists, and download timestamps.
- Database versions, release numbers, and citation metadata.
- Software versions, command lines, parameters, random seeds, and hardware class.
- Exclusion reasons for failed, contaminated, low-quality, or license-restricted records.
- Output file checksums.
- Known limitations and claims explicitly not supported by the run.

No candidate should appear in a final shortlist without stable accession identifiers for the source sample, assembly or MAG, contig/scaffold, predicted gene/protein, taxonomy, and annotation evidence.

## 5. Minimum Evidence Levels

Use these levels in every report:

- Level 0: idea only; no candidate or data artifact.
- Level 1: accession-backed sequence hit with basic metadata.
- Level 2: clustered homolog with domain annotation and taxonomy.
- Level 3: genomic-neighborhood or pathway context supports the hypothesis.
- Level 4: structure or active-site evidence supports the predicted role.
- Level 5: literature, database, or ortholog evidence supports a close functional analog.
- Level 6: in vitro or metabolomics validation.
- Level 7: replicated assay under target deployment conditions.

Computational discovery plans in this directory generally aim for Level 3 to Level 5 packets. Level 6 and Level 7 require wet-lab collaboration.

## 6. Common Quality Gates

Dataset gates:

- Use INSDC accessions whenever available.
- Reject records without sufficient sample/environment metadata for the target question.
- For MAGs, require explicit completeness, contamination, and quality method fields when possible.
- Deduplicate by sequence identity, species cluster, and study accession so overrepresented organisms do not dominate rankings.

Sequence gates:

- Remove fragments unless the project explicitly targets partial proteins.
- Flag proteins with internal stops, frameshifts, suspicious low-complexity regions, or obvious assembly edge truncation.
- Use orthogonal annotation: sequence similarity, profile HMM/domain evidence, and genomic context.

Structure gates:

- Treat AlphaFold DB or local predictions as models, not experimental structures.
- Use pLDDT/PAE or equivalent confidence metrics and do not rely on low-confidence active-site geometry.
- Compare folds with Foldseek or TM-align, then manually inspect active-site residues for top candidates.

Taxonomy gates:

- Normalize taxonomy through GTDB where bacterial/archaeal genome context matters.
- Record whether the protein comes from an isolate genome, MAG, contig, metagenomic protein catalogue, or raw assembly.
- Score phylogenetic novelty separately from functional novelty.

## 7. Ranking Framework

Each project can tune weights, but all rankings must include:

- Novelty: sequence distance, cluster rarity, taxonomic distribution, and database absence.
- Utility: target reaction, pathway, phenotype, environmental relevance, and commercial or scientific value.
- Feasibility: protein length, secretion/signal peptide where relevant, expression risk, cofactors, assay availability, and synthesis constraints.
- Evidence consistency: agreement among domain annotation, sequence homology, structure, catalytic residues, genomic neighborhood, and environmental metadata.
- Safety and compliance: AMR, toxin, pathogen, dual-use, biosecurity, biosafety, and access-license flags.

## 8. Candidate Packet Standard

Every final candidate packet must include:

- Candidate ID and stable source accessions.
- Protein or BGC sequence coordinates.
- Source environment, host, biome, and study.
- GTDB or equivalent taxonomy.
- Homolog cluster membership and representative sequence.
- Domain calls with thresholds and database version.
- Known-function nearest neighbors and their evidence levels.
- Genomic-neighborhood diagram or tabular neighborhood.
- Structure model source, confidence, and structural-neighbor evidence.
- Active-site or motif conservation analysis where applicable.
- Novelty score, utility score, feasibility score, and safety flags.
- Recommended assay and explicit failure criteria.

## 9. Safety and Compliance

Antimicrobial natural products and AMR work must remain discovery and surveillance oriented. Do not optimize pathogens, improve resistance phenotypes, or provide experimental procedures that enable resistance transfer. Candidate expression, culturing, and bioactivity assays require institutional biosafety review and appropriate collaborators.

For all plans:

- Avoid reconstructing pathogenic strains from metagenomes.
- Avoid publishing actionable sequences for toxins or resistance-enhancing constructs without review.
- Keep clinical and environmental surveillance claims separated from diagnostic claims unless the pipeline has been validated for that use.

## 10. Completion Standard

A plan is complete only when:

- Required sources were versioned and recorded.
- The target dataset was frozen.
- Candidate generation and ranking were executed or explicitly scoped as a plan-only artifact.
- Top candidates have evidence packets.
- Limitations and unsupported claims are documented.
- A final shortlist/report maps every claim to reproducible evidence.

