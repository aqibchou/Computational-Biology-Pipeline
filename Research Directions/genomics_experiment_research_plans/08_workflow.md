# Plan 08 Workflow: Biosurfactants, Biopolymers, and Biomaterials

## Goal

Run Plan 08 as a focused pre-wet-lab screen for microbial biomaterials hypotheses. The output should be a small, defensible shortlist of candidates with pathway, source-environment, novelty, export/recovery, safety-context, and assay-feasibility support.

Strongest safe claim:

> Computationally prioritized microbial biomaterials hypotheses with pathway, source-environment, novelty, export/recovery, safety-context, and assay-feasibility support.

Avoid claiming:

> New material discovered, high-performance biosurfactant, biodegradable plastic producer, safe industrial strain, or validated material property.

## 1. Define Candidate Tracks

Split Plan 08 into separate candidate queues rather than forcing all material types into one ranking.

| Track | Target |
|---|---|
| Biosurfactants | Lipopeptide, glycolipid, rhamnolipid, surfactin-like, and other biosurfactant-like BGCs |
| Biopolymers / EPS | PHA, exopolysaccharide, alginate/cellulose-like, capsule, and export loci |
| Protein Materials | Adhesive proteins, biofilm matrix proteins, metal/silica-binding proteins, repetitive proteins, and self-assembling proteins |
| Pigments / Functional Materials | Melanin and related polymerizable pigment pathways |

## 2. Dataset Selection

Prioritize environments where material-producing traits are plausible.

- Marine interfaces
- Oil or hydrocarbon-contaminated sites
- Sediments
- Saline habitats
- Deserts and soil crusts
- Biofilms
- Metal-rich environments
- Wastewater or industrial sites

Use MGnify and MGnify Genomes first. Expand to raw SRA/ENA only if metadata quality and compute budget justify it.

## 3. Genome/MAG Quality Gate

For each source genome or MAG, record:

- Completeness
- Contamination
- Contig fragmentation
- GTDB taxonomy
- Source metadata strength
- Cultured/isolate availability when possible

Low-quality MAGs can remain as atlas/support evidence, but should not become top wet-lab candidates without additional support.

## 4. Pathway and BGC Detection

Use separate detection logic by candidate class.

For biosurfactant-like BGCs:

- Run or reuse antiSMASH.
- Dereplicate against MIBiG.
- Run BiG-SCAPE when candidate BGCs look promising.
- Record product class, BGC completeness, family links, and nearest known clusters.

For biopolymer, EPS, pigment, and protein material candidates:

- Annotate with UniProt, InterPro, Pfam, dbCAN, eggNOG, or equivalent local annotation sources.
- Identify PHA, EPS, capsule, secretion/export, melanin, adhesive, biofilm matrix, metal-binding, and repetitive/self-assembling protein features.
- Add SignalP/TMHMM-style secretion and membrane prediction if available.

## 5. Feature Engineering

Score each candidate using evidence that directly affects material plausibility and wet-lab practicality.

| Feature | Why It Matters |
|---|---|
| Pathway/BGC completeness | Reduces isolated false-positive hits |
| Export/secretion machinery | Many material products must leave or decorate the cell surface |
| Precursor metabolism | Supports production feasibility |
| Source-environment fit | Oil, saline, biofilm, desert, sediment, or metal context strengthens plausibility |
| Novelty | Avoids rediscovering obvious known systems |
| Assay feasibility | Prioritizes candidates with clear first-pass tests |
| Safety context | Avoids problematic producers or loci |
| Isolate/culture path | Improves wet-lab practicality |

## 6. Dereplication and Novelty

For biosurfactant and BGC candidates:

- Compare to MIBiG.
- Check nearest known product classes.
- Separate close known clusters from divergent candidates.
- Use conservative language: BGC-family distinct, not new molecule.

For proteins and enzymes:

- Run UniRef/nr-style dereplication where practical.
- Validate Pfam/domain support.
- Compare against reviewed homologs.
- Review catalytic or functional residues when relevant.

## 7. Safety and Practicality Screen

Reject or hold candidates with:

- Pathogen-adjacent taxonomy
- Toxin or virulence context
- AMR or mobilome concerns near candidate loci
- Poor MAG quality
- No coherent pathway
- No export or recovery route
- Impossible or unclear assay

This is a screening layer only, not biosafety clearance.

## 8. Rank Candidates Separately

Produce separate ranked lists by material class.

- `plan08_biosurfactant_bgc_shortlist.csv`
- `plan08_biopolymer_eps_shortlist.csv`
- `plan08_protein_materials_shortlist.csv`
- `plan08_pigment_materials_shortlist.csv`

Suggested scoring:

```text
score =
  0.20 * pathway_or_bgc_completeness
+ 0.17 * material_application_fit
+ 0.15 * source_environment_support
+ 0.13 * export_or_extracellular_evidence
+ 0.12 * novelty
+ 0.10 * assay_and_recovery_feasibility
+ 0.08 * taxonomy_and_genome_quality
+ 0.05 * safety_score
```

## 9. Candidate Packet Build

For each top candidate, create a packet with:

- Genome/source metadata
- Target material class
- Pathway/BGC gene table
- Key genes and domains
- Nearest known homologs or BGCs
- Novelty/dereplication result
- Export/secretion evidence
- Source-environment rationale
- Safety/context screen
- Assay recommendation
- Strongest safe claim
- Remaining experimental gaps

## 10. Wet-Lab Screen Design

Map each candidate type to a simple first-pass assay.

| Candidate Type | First Assay |
|---|---|
| Biosurfactant | Drop-collapse, oil-spreading, emulsification index, surface tension |
| PHA/biopolymer | Nile red/Nile blue staining, GC-MS after methanolysis |
| EPS | Capsule/EPS staining, carbohydrate quantification, rheology |
| Adhesive/coating protein | Recombinant expression, surface adhesion/coating assay |
| Melanin/pigment | Pigment induction, UV-vis, oxidative polymer assay |
| Metal/silica-binding protein | Binding assay against target material surface |

## 11. Final Outputs

Expected outputs:

- `plan08_biomaterials_candidate_master.csv`
- `plan08_biosurfactant_bgc_shortlist.csv`
- `plan08_biopolymer_eps_shortlist.csv`
- `plan08_protein_materials_shortlist.csv`
- `plan08_pigment_materials_shortlist.csv`
- `plan08_safety_and_recovery_gate.csv`
- `plan08_top_candidate_packets/`
- `PLAN08_PRE_WETLAB_SCREEN_REPORT.md`
- `PLAN08_RESEARCH_STYLE_WRITEUP.md`

## Expected End State

The expected final screen should produce a small number of defensible pre-wet-lab material candidates, likely split as:

- 2-3 biosurfactant/BGC candidates
- 2-3 EPS/PHA/biopolymer candidates
- 1-2 proteinaceous material candidates

The final report should clearly separate computational prioritization from measured material performance.
