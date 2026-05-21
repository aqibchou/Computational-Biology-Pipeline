# Plan 03 Workflow: Nitrogen-Cycle Enzyme Discovery

## Goal

Run Plan 03 as a rigorous pre-wet-lab screen for microbial nitrogen-cycle pathway hypotheses. The output should be a small, defensible shortlist of candidates with marker-model support, pathway completeness, genomic-neighborhood evidence, source-environment rationale, novelty, quality/safety context, and realistic assay handoff.

Strongest safe claim:

> Computationally prioritized nitrogen-cycle pathway and enzyme hypotheses with marker-model, pathway-context, source-metadata, novelty, genome-quality, and safety-context support.

Avoid claiming:

> Nitrogen fixation activity, nitrous oxide reduction activity, fertilizer-efficiency improvement, plant-growth benefit, greenhouse performance, field performance, emissions reduction, environmental safety, or deployable microbial inoculant status.

## 1. Starting Point And Main Risk

Use the May 14 Plan 03 artifacts as a first-pass candidate pool, not as final evidence.

Existing first-pass inputs:

- `outputs/computational_execution_2026-05-14/03_nitrogen_cycle_enzyme_discovery/candidates.csv`
- `outputs/computational_execution_2026-05-14/03_nitrogen_cycle_enzyme_discovery/nitrogen_pathway_candidates.csv`
- `outputs/computational_execution_2026-05-14/03_nitrogen_cycle_enzyme_discovery/n2o_reducer_shortlist.csv`
- `outputs/computational_execution_2026-05-14/03_nitrogen_cycle_enzyme_discovery/rhizosphere_nitrogen_signature.csv`
- `outputs/computational_execution_2026-05-14/source_genomes.csv`
- local MGnify genome cache under `outputs/computational_execution_2026-05-14/cache/mgnify_genomes/`

Known first-pass weakness:

- Broad annotation text can confuse nitrogen-cycle enzymes with unrelated beta-propeller, cupredoxin, cytochrome oxidase, amidohydrolase, carbon-nitrogen hydrolase, Fe-S, regulator, and housekeeping proteins.
- Single-gene hits are not enough for multi-gene nitrogen pathways.
- Nitrous oxide reductase calls are especially vulnerable to false positives from copper-center and cytochrome oxidase domains unless `nosZ` and accessory context are confirmed.
- Nitrogenase calls are vulnerable to false positives from generic P-loop ATPases, ParA/MinD-like proteins, and Fe-S proteins unless `nifH/nifD/nifK` and accessory context are confirmed.

The Plan 03 refinement must therefore be stricter than the first pass.

## 2. Candidate Tracks

Rank each biology separately rather than forcing all nitrogen hits into one list.

| Track | Target | Primary output |
|---|---|---|
| Nitrogen fixation | `nifH`, `nifD`, `nifK`, and accessory/cofactor genes | `plan03_nitrogenase_cluster_shortlist.csv` |
| Nitrous oxide reduction / denitrification completion | `nosZ` plus `nosD/F/Y/R` context; denitrification modules ending in N2O reduction | `plan03_n2o_reducer_shortlist.csv` |
| Nitrification / ammonia oxidation | `amoA/B/C`, `hao`, comammox-like context after AMO/pMMO discrimination | `plan03_nitrification_amo_hao_shortlist.csv` |
| Nitrate/nitrite transformation | `nar/nap`, `nirS/nirK`, `nor`, `nrfA`, assimilatory nitrate/nitrite pathways | `plan03_nitrate_nitrite_transformation_shortlist.csv` |
| Urea metabolism and rhizosphere nitrogen availability | `ureA/B/C` plus `ureD/E/F/G`, urea transport, plant/rhizosphere context | `plan03_urea_rhizosphere_shortlist.csv` |
| Rhizosphere nitrogen signature | genome- or community-level marker patterns linked to plant-associated nitrogen potential | `plan03_rhizosphere_nitrogen_signature.md` |

## 3. Dataset Selection

Prioritize datasets where nitrogen-cycle function is plausible and interpretable.

High-priority environments:

- Agricultural soil
- Rhizosphere and root-associated microbiomes
- Wetlands, sediments, and oxygen-gradient habitats
- Freshwater and marine sediments
- Wastewater, activated sludge, and nutrient-removal systems
- Fertilizer-exposed or nitrogen-amended studies, when metadata is explicit
- Saline, drought, cold, or other stress contexts only when they add an ecology rationale

Metadata to record for each genome, MAG, or sample:

- Source biome and exact sample descriptor
- Crop or plant host when available
- Soil/sediment/water/wastewater context
- Fertilizer or nitrogen amendment metadata
- Oxygen/redox/anaerobic context
- pH, salinity, temperature, geography, and season when available
- Study accession and sample accession
- MGnify catalogue or raw-read source

Use MGnify and MGnify Genomes first. Expand to raw SRA/ENA only if the target environment is missing from the processed dataset or if independent validation samples are needed.

For large HMMER, KOfam, phylogeny, or broad dereplication jobs, use the Kaggle CLI compute path if local execution becomes slow or memory-heavy.

## 4. Genome And MAG Quality Gate

Each source genome or MAG must receive a quality call before pathway scoring.

| Gate | Pass threshold | Use |
|---|---|---|
| High-quality genome/MAG | completeness >= 90%, contamination <= 5%, usable contiguity | eligible for wet-lab-facing shortlist |
| Good-quality MAG | completeness >= 80%, contamination <= 5-10%, pathway genes coherent | eligible only with strong pathway context |
| Low-quality MAG | completeness < 80% or contamination > 10% | atlas/support only |
| Isolate or cultured relative | isolate metadata or close reference/culture route | improves practical handoff |
| Fragmented pathway | key genes split across many short contigs or absent coordinates | hold unless strongly supported |

Additional checks:

- Confirm GTDB taxonomy.
- Deduplicate by species/genus/study so one overrepresented organism does not dominate.
- Flag gut/clinical/pathogen-adjacent sources separately from environmental/agricultural sources.
- Record contig, start/end coordinates, strand, and neighboring genes for every top marker.
- Reject or hold candidates where pathway completeness could plausibly be contamination or binning artifact.

## 5. Marker Model Build

Build a versioned marker-model manifest before re-scoring candidates.

Required output:

- `plan03_marker_model_manifest.csv`

Each marker model row should record:

- Canonical marker name
- Target track
- Database source: UniProt, InterPro, Pfam-A, TIGRFAM, eggNOG, KOfam, MetaCyc, Rhea, or curated local reference
- Accession or model ID
- Trusted cutoff, gathering threshold, e-value threshold, coverage threshold, and model length
- Known false-positive families
- Positive-control references
- Negative-control/confusable references
- Whether the marker is sufficient alone or requires pathway/neighborhood partners

Suggested marker logic:

| Pathway | Strong evidence | Common false-positive risk |
|---|---|---|
| Nitrogenase | `nifH` plus `nifD/nifK` or `nifENB` accessory context | generic P-loop ATPases, ParA/MinD, Fe-S assembly proteins |
| Nitrous oxide reduction | full-length `nosZ` with copper-binding/catalytic motif support plus `nosD/F/Y/R` or denitrification context | COX2/cupredoxin/cytochrome oxidase copper-center proteins |
| Denitrification | coherent `nar/nap -> nirS/nirK -> nor -> nos` module | isolated reductases or regulators with no pathway continuity |
| Nitrification | `amoA/B/C` plus `hao` or comammox context; AMO/pMMO phylogenetic discrimination | particulate methane monooxygenase and unrelated copper monooxygenases |
| DNRA | `nrfA` plus electron-transfer and nitrate/nitrite context | generic multiheme cytochromes |
| Urease | `ureA/B/C` plus accessory `ureD/E/F/G` and/or urea transporter | broad amidohydrolases and unrelated metallo-dependent hydrolases |

Do not rely on informal marker names alone. Every retained call needs model provenance and threshold evidence.

## 6. Orthogonal Annotation And False-Positive Audit

For every candidate row, collect orthogonal evidence:

- HMM/profile hit against the marker manifest
- KOfam/KEGG module evidence when available
- Pfam/InterPro/TIGRFAM domain support
- eggNOG or UniProt annotation
- Protein length and coverage against expected marker length
- Active-site or cofactor motif support where relevant
- Genomic-neighborhood support
- Taxonomic plausibility for the pathway

Required output:

- `plan03_marker_false_positive_audit.csv`

The false-positive audit should explicitly label:

- `PASS_MARKER_SPECIFIC`
- `PASS_PATHWAY_CONTEXT`
- `HOLD_SINGLE_GENE_ONLY`
- `HOLD_CONFUSABLE_DOMAIN`
- `HOLD_LOW_COVERAGE_OR_FRAGMENT`
- `HOLD_LOW_GENOME_QUALITY`
- `HOLD_TAXON_OR_SOURCE_CONTEXT`
- `REJECT_HOUSEKEEPING_OR_UNRELATED_DOMAIN`

## 7. Pathway Reconstruction

Build genome-level pathway profiles, not only protein-level hits.

Required output:

- `plan03_genome_pathway_profiles.csv`

For each genome, record:

- Presence/absence of each marker family
- Copy number normalized by genome completeness
- Marker contig IDs and coordinate spans
- Whether key genes are co-localized
- Pathway completeness score by track
- Whether genes are on the same contig, adjacent contigs, or scattered
- Missing essential markers
- Accessory/cofactor/regulatory support
- Source environment fit
- MAG quality risk

Track-specific completeness rules:

- Nitrogen fixation: prioritize clusters with `nifH`, `nifD`, `nifK`, and accessory/cofactor genes; hold isolated `nifH`-like or Fe-S/P-loop hits.
- Nitrous oxide reduction: prioritize `nosZ` with accessory genes and upstream denitrification context; hold copper-center-only calls.
- Nitrification: require AMO/HAO context or a strong phylogenetic placement; hold generic monooxygenase or pMMO-like uncertainty.
- Urease: require catalytic subunits plus accessory maturation genes; hold broad amidohydrolase-only hits.
- Rhizosphere signature: treat multi-marker plant-associated patterns as ecological hypotheses, not organism performance.

## 8. Phylogeny And Dereplication

Run marker-family phylogenies for finalists, not for every noisy first-pass hit.

Required outputs:

- `plan03_marker_phylogeny_summary.csv`
- `plan03_marker_dereplication_and_novelty.csv`

For each finalist marker family:

- Build a reference set from reviewed UniProt/Swiss-Prot, representative UniRef, GTDB-linked taxa, and candidate sequences.
- Remove near-identical duplicates.
- Align with MAFFT or equivalent.
- Trim poorly aligned regions.
- Run FastTree for broad triage if needed.
- Run IQ-TREE or IQ-TREE-grade phylogeny for finalists where practical.
- Record nearest characterized homolog, identity, coverage, phylogenetic placement, and whether the candidate is a close known enzyme or a divergent family member.

Novelty language:

- Use `sequence-divergent nitrogen-cycle marker candidate`.
- Use `BGC/pathway/marker-family distinct` only if supported by clustering or phylogeny.
- Do not use `new nitrogenase`, `new N2O reducer`, or `improved nitrogen-cycle enzyme` without experimental data.

## 9. Structure And Motif Review

Use structure evidence only for top enzyme-level candidates where it helps distinguish true function from confusable domains.

Required output:

- `plan03_structure_motif_review.csv`

Review:

- AlphaFold DB homologs or candidate-specific models when available
- pLDDT/PAE or confidence proxy
- Fold similarity to characterized references
- Conservation of catalytic residues, metal/cofactor ligands, signal peptides, transmembrane regions, and periplasmic/export context
- Whether low-confidence regions affect the inferred active site or cofactor site

Structure should not upgrade a candidate if the marker model and pathway context are weak.

## 10. Source, Safety, And Practicality Screen

Required output:

- `plan03_safety_source_practicality_gate.csv`

Hold or reject candidates with:

- Pathogen-adjacent taxonomy or clinical/gut source context without strong environmental rationale
- Toxin, virulence, AMR, or mobilome context near candidate loci
- Poor MAG quality or contamination risk
- No coherent pathway context
- No assay route
- No culture/isolate/recovery path when organism-level wet lab work is proposed
- Candidate source that would imply environmental release or inoculant testing without institutional review

This is only computational triage. It is not biosafety clearance.

## 11. Feature Engineering And Scoring

Score protein-level and genome-level candidates separately, then merge them into track-specific rankings.

Suggested scoring:

```text
score =
  0.20 * marker_specificity
+ 0.18 * pathway_completeness
+ 0.15 * genomic_neighborhood_support
+ 0.13 * target_outcome_relevance
+ 0.11 * source_environment_metadata_strength
+ 0.10 * novelty_or_phylogenetic_interest
+ 0.07 * assay_and_recovery_feasibility
+ 0.04 * genome_quality
+ 0.02 * safety_context_score
```

Feature definitions:

| Feature | Strong evidence |
|---|---|
| Marker specificity | curated HMM/profile support with coverage, threshold, and false-positive audit pass |
| Pathway completeness | required catalytic and accessory genes present for the track |
| Genomic-neighborhood support | compact operon or same-contig pathway module |
| Target outcome relevance | N2O reduction, nitrogen fixation, rhizosphere nitrogen availability, or validated nitrogen transformation class |
| Source metadata strength | agricultural/rhizosphere/wetland/wastewater/oxygen-gradient context with stable accessions |
| Novelty | divergent but interpretable marker family or underexplored taxon |
| Assay/recovery feasibility | clear first-pass assay and practical isolate, MAG, or gene-level route |
| Genome quality | high completeness, low contamination, stable taxonomy |
| Safety context | no direct AMR/mobilome/toxin/pathogen flags near candidate |

## 12. Ranking Outputs

Produce separate ranked tables:

- `plan03_nitrogen_pathway_candidate_master.csv`
- `plan03_nitrogenase_cluster_shortlist.csv`
- `plan03_n2o_reducer_shortlist.csv`
- `plan03_nitrification_amo_hao_shortlist.csv`
- `plan03_nitrate_nitrite_transformation_shortlist.csv`
- `plan03_urea_rhizosphere_shortlist.csv`
- `plan03_marker_false_positive_audit.csv`
- `plan03_genome_pathway_profiles.csv`
- `plan03_safety_source_practicality_gate.csv`
- `plan03_marker_dereplication_and_novelty.csv`
- `plan03_marker_phylogeny_summary.csv`
- `plan03_structure_motif_review.csv`

Ranking rules:

- No candidate can be top-tier on a single broad annotation hit.
- No low-quality MAG can become a wet-lab lead without independent support.
- No organism-level candidate can be packaged as an inoculant or field candidate.
- N2O claims require `nosZ` specificity plus context.
- Nitrogen fixation claims require core nitrogenase cluster context.
- Urease claims require urease subunits plus accessory support.

## 13. Candidate Packet Build

Required output:

- `plan03_top_candidate_packets/`

Each packet must include:

- Candidate ID and track
- Genome/MAG/source accessions
- GTDB taxonomy
- Genome quality and source metadata
- Marker-model hits with thresholds and coverage
- Pathway gene table
- Neighborhood table
- False-positive audit result
- Closest characterized homologs
- Phylogeny/dereplication result
- Structure/motif review if available
- Safety/source/practicality screen
- Assay recommendation
- Strongest safe claim
- Remaining experimental gaps

Candidate packet calls:

- `ADVANCE_TO_PRE_WETLAB_PACKET`
- `REVIEW_BACKUP_CANDIDATE`
- `HOLD_SINGLE_GENE_ONLY`
- `HOLD_FALSE_POSITIVE_RISK`
- `HOLD_LOW_QUALITY_OR_SAFETY_CONTEXT`

## 14. Wet-Lab Handoff Framing

Map each track to first-pass validation without implying field utility.

| Candidate type | First-pass validation direction | Claim boundary |
|---|---|---|
| Nitrogenase cluster | marker confirmation and nitrogenase activity screen under collaborator-approved conditions | does not prove agronomic nitrogen fixation or plant benefit |
| N2O reducer | marker confirmation and microcosm/headspace N2O transformation screen | does not prove emissions reduction in soil or field |
| Nitrification/ammonia oxidation | ammonia/nitrite/nitrate transformation assay or marker validation | does not prove nitrification performance in deployment |
| DNRA/nitrate/nitrite transformation | nitrogen species transformation screen with appropriate controls | does not prove ecosystem nitrogen retention |
| Urease/rhizosphere N availability | urease activity or community-marker validation | does not prove fertilizer efficiency or plant growth |
| Rhizosphere nitrogen signature | independent sample qPCR/metagenomic marker validation | does not prove causality or crop benefit |

Wet-lab work should be framed as validation of pathway potential. Greenhouse, field, emissions, fertilizer-efficiency, or inoculant claims require replicated experiments beyond this computational workflow.

## 15. Final Reports

Required final narrative outputs:

- `PLAN03_PRE_WETLAB_SCREEN_REPORT.md`
- `PLAN03_RESEARCH_STYLE_WRITEUP.md`
- `PLAN03_PRE_WETLAB_SCREEN_COMPLETION_AUDIT.md`

The report should answer:

- How many first-pass hits were screened?
- How many were rejected as broad or confusable annotations?
- Which marker models and thresholds were used?
- Which pathways were complete versus single-gene-only?
- Which candidates are strongest for N2O reduction, nitrogen fixation, nitrification, urea metabolism, or rhizosphere signatures?
- Which candidates were held due to MAG quality, source context, safety context, lack of pathway coherence, or lack of assay route?
- What is the strongest true claim?
- What claims remain unsupported?

## Expected End State

The expected final Plan 03 package should produce a small, conservative set of pre-wet-lab candidates, likely:

- 1-3 high-confidence N2O reducer or complete-denitrification candidates
- 1-3 nitrogenase-cluster candidates
- 1-2 nitrification/ammonia-oxidation or nitrate/nitrite transformation candidates
- 1-2 urease or rhizosphere nitrogen-availability candidates

If marker specificity or pathway completeness is weak, it is acceptable for a track to produce review holds rather than wet-lab candidates. The final package should favor clean evidence over filling every category.

## Completion Checklist

- [ ] Dataset and source metadata are frozen and versioned.
- [ ] Marker-model manifest records exact model IDs, thresholds, and false-positive risks.
- [ ] Genome/MAG quality gates are applied before pathway scoring.
- [ ] Single-gene hits are separated from pathway-complete candidates.
- [ ] `nosZ`, `nif`, `amo/hao`, `nrf`, and `ure` calls pass track-specific false-positive checks.
- [ ] Genomic-neighborhood evidence is recorded for top candidates.
- [ ] Candidate taxa are plausible for the source environment.
- [ ] Finalists have dereplication and phylogeny context.
- [ ] Safety/source/practicality gate is complete.
- [ ] Candidate packets are generated for only the cleanest candidates.
- [ ] Reports avoid agricultural, climate, field, emissions, inoculant, or environmental-safety overclaims.
