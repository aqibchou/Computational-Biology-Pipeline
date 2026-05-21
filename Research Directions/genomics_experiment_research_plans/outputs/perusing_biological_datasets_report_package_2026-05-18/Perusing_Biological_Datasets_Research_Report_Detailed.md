---
header-includes:
  - \usepackage{graphicx}
  - \usepackage{multicol}
  - \usepackage{enumitem}
  - \usepackage{titlesec}
  - \geometry{bottom=0.6in}
  - \setlength{\columnsep}{0.24in}
  - \setlength{\multicolsep}{5pt plus 1pt minus 1pt}
  - \setlength{\parskip}{3pt}
  - \titlespacing*{\subsection}{0pt}{0.85\baselineskip}{0.35\baselineskip}
  - \titlespacing*{\subsubsection}{0pt}{0.7\baselineskip}{0.25\baselineskip}
  - \setlist{leftmargin=*,nosep}
  - \setlength{\emergencystretch}{8em}
  - \newcommand{\reporttableportrait}{\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.16}\sloppy}
  - \newcommand{\reporttablewide}{\footnotesize\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{1.13}\sloppy}
---

\begin{titlepage}
\centering
\vspace*{0.32\textheight}
{\Huge\bfseries Perusing Biological Datasets\par}
\vspace{1.5cm}
{\Large By: Aqib Choudhary\par}
\vspace{1.25cm}
\includegraphics[width=0.78\textwidth]{figures/title_process_panel.png}
\vfill
\end{titlepage}

## Abstract

This report presents a single integrated computational discovery campaign for prioritizing biological candidates from heterogeneous genomics datasets. The work is organized as one staged screen rather than as eight unrelated studies. Each screening module began with a broad candidate universe, applied function- and context-specific evidence gates, removed common false positives, hardened novelty and safety-context claims, and produced bounded pre-wet-lab hypotheses for expert review. The result is a high-leverage candidate portfolio: multiple classes of biologically plausible leads were reduced from broad genomic search spaces into a smaller set of traceable, testable hypotheses. The modules differed in biological target and evidence type, but they shared the same overall standard: a candidate was advanced only when the computational evidence supported a specific, testable hypothesis and the remaining uncertainty could be stated clearly.

The campaign covered eight screening lenses. Plan 01 prioritized secondary-metabolite biosynthetic gene clusters (BGCs). Plan 02 prioritized industrial biocatalyst candidates. Plan 03 prioritized nitrogen-cycle pathway candidates. Plan 04 prioritized plant-growth-promotion (PGP) genome hypotheses. Plan 05 prioritized natural enzyme homologs for stability testing. Plan 06 prioritized rare-chemistry enzyme hypotheses. Plan 07 prioritized biomaterials and biopolymer candidates. Plan 08 organized the extremophile enzyme atlas and dataset-release/stability-feature layer supporting the enzyme screens. The completed work produced three strong BGC keep candidates, broad strict and high-precision enzyme queues with two current bridge leads, six nitrogen-cycle candidates, four PGP genome hypotheses with one cleanest organism-level lead, four natural-stability enzyme candidates, four rare-chemistry enzyme candidates, six immediate biomaterial candidates plus three BGC/material review holds, and a 4,071-row extremophile enzyme atlas. If a subset of these candidates passes wet-lab screening, the most consequential directions include natural-product discovery, industrial biocatalysis, agricultural nitrogen cycling, plant stress resilience, rare enzyme chemistry, and microbial biomaterials.

The conclusions remain computational and pre-wet-lab, but the evidence base is substantial: candidate selection is supported by convergent annotation, context, dereplication, structure, phylogeny, safety-context, and provenance layers. The campaign does not validate antibiotic activity, enzyme activity, substrate scope, nitrogen flux, plant-growth benefit, biomaterial production, organism safety, field performance, product performance, or environmental release suitability. It establishes a rigorous launch point for wet-lab prioritization by converting large biological datasets into traceable candidate hypotheses with explicit claim boundaries, candidate archives, and a full supporting technical appendix.

## 1. Purpose And Report Structure

The 325-page supporting appendix preserves the full computational record: source reports, packet text, embedded tabular artifacts, and detailed audit trails. That document is intentionally exhaustive. It is appropriate for internal traceability, but it is too long and too raw to function as a grant-facing or collaborator-facing research report.

This detailed report is the intermediate layer. It is longer and more rigorous than a five-page summary, but it is still designed to be readable. It synthesizes the campaign as one process, explains the plan-by-plan screening differences, reports the main candidate outcomes, and preserves enough candidate-level detail to support scientific review. The candidate archives remain separate so that this report does not become a raw packet dump.

The package is organized in three layers:

- Main research report: this document. It states the scientific rationale, methods, results, and limitations.
- Candidate archives: separate files grouped by screening module. They preserve full candidate packet text and source paths.
- Full supporting appendix: the 325-page compiled record. It retains the full report and table lineage.

The main report uses report-facing Plan 01 through Plan 08 numbering. For traceability, some source artifact paths still contain original plan numbers from the working directory. In particular, report Plan 05 corresponds to original Plan 06, report Plan 06 corresponds to original Plan 07, report Plan 07 corresponds to original Plan 08, and report Plan 08 corresponds to original Plan 09.

## 2. Integrated Screening Design

The central contribution of the campaign is a reusable computational prioritization pattern. The biological targets differ, but each module follows the same general structure:

1. Define a broad candidate universe from genome, gene, BGC, annotation, marker, source-metadata, or release artifacts.
2. Assign a functional hypothesis using the strongest available evidence for that biological class.
3. Apply false-positive filters specific to the target class.
4. Add novelty, dereplication, source-context, quality, and safety-context checks.
5. Downselect into immediate candidates, review holds, or archive-only records.
6. State the strongest bounded claim and the remaining experimental gaps.

This workflow is intentionally conservative. It is easier for a computational screen to overstate a result than to understate it. A generic annotation can look like a meaningful enzyme, a housekeeping lipid-A gene can look like a biosurfactant clue, a partial nitrogen marker can look like a pathway, and a BGC boundary can look more complete than it is. The screening logic therefore emphasized negative control: candidates were removed or held when the evidence did not support the specific claim being considered.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_01_integrated_workflow.png}
{\scriptsize \textbf{Figure 1. Integrated screening workflow.} The same conservative prioritization pattern was adapted across all eight biological lenses.\par}
\end{center}

The campaign also distinguishes between three categories of output:

- Immediate pre-wet-lab candidates: hypotheses with enough annotation, context, quality, and practicality support to justify expert wet-lab planning.
- Review candidates: scientifically interesting candidates whose product chemistry, boundary, structure, source, or safety context is not yet clean enough for direct wet-lab prioritization.
- Archive candidates: candidates retained for traceability, second-wave review, or evidence completeness but not currently prioritized.

This project is not a simple "top score wins" screen. The strongest candidates are those that survive multiple independent forms of scrutiny, not merely those with the highest first-pass score.

## 3. Data And Evidence Types

The screen reused local computational artifacts produced across the genomics work. These included candidate tables, genome metadata, BGC calls, protein annotations, source-environment labels, genome quality fields, local safety-context tables, candidate packets, structure summaries, phylogeny outputs, and release metadata. The strongest modules used multiple orthogonal evidence layers rather than a single annotation source.

The main evidence classes were:

- BGC evidence: antiSMASH, GECCO, SanntiS, product-class annotations, BGC boundary review, MIBiG and BiG-SCAPE context, and whole-MAG support.
- Enzyme evidence: enzyme-family assignment, closest reviewed-reference context, Pfam/HMMER recovery, UniRef or Swiss-Prot-style recovery, motif and active-site plausibility, structure confidence, and pocket/ligand context.
- Pathway evidence: marker specificity, pathway completeness, genomic neighborhood, marker-family phylogeny, and source context.
- Genome-level trait evidence: genome quality, trait co-occurrence, isolate/culture context, reference ANI, strain dereplication, and local safety-context filters.
- Stability evidence: source-condition labels, charge/composition features, stability-axis scores, structure proxies, loop/disorder comparison, ThermoMPNN aggregate summaries, and benchmark framing.
- Material evidence: PHA/EPS loci, capsule/export signals, surface protein/domain hypotheses, pigment/tyrosinase evidence, and BGC/material review logic.
- Release evidence: source manifests, checksums, row counts, column manifests, stability-feature scores, and atlas-level organization.

No evidence class was treated as proof of phenotype. Computational evidence can support a hypothesis, but expression, activity, product identity, organism behavior, and safety require experimental data.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_02_evidence_stack.png}
{\scriptsize \textbf{Figure 2. Evidence stack.} Candidates advance by surviving multiple independent evidence layers rather than by score alone.\par}
\end{center}

## 4. Screening Differences By Module

The module map below summarizes how the shared screen changed by biological target.

- **Plan 01, secondary-metabolite BGC discovery:** BGC caller support, boundary/domain review, whole-MAG support, MIBiG/BiG-SCAPE dereplication, product-class lookup, and safety/context checks. Output role: natural-product review hypotheses.
- **Plan 02, industrial biocatalyst discovery:** enzyme-family assignment, active-site plausibility, Pfam/UniRef recovery, structure/pocket checks, and family-level assay precedent. Output role: pre-lab-review and expert-review enzyme queues.
- **Plan 03, nitrogen-cycle pathway discovery:** marker specificity, pathway coherence, representative protein support, genome/source context, and IQ-TREE phylogeny update. Output role: nitrogen-cycle pathway hypotheses.
- **Plan 04, plant-growth-promotion genome discovery:** trait co-occurrence, genome quality, reference ANI, strain dereplication, isolate/culture path, and safety/context filters. Output role: PGP genome hypotheses.
- **Plan 05, natural stability discovery:** stability-axis scoring, structure models, loop/disorder and energy proxies, IQ-TREE context, and ThermoMPNN aggregate summaries. Output role: natural homolog hypotheses for stability testing.
- **Plan 06, rare chemistry discovery:** rare-function annotations, Rhea/EC consistency, structural plausibility, ligand-pocket comparison, and phylogenetic context. Output role: rare-chemistry enzyme hypotheses.
- **Plan 07, biomaterials discovery:** PHA, EPS, protein-material, pigment, and BGC evidence; export and recovery context; material-subtype scoring; and unresolved-chemistry triage. Output role: biomaterial candidates and BGC-material review holds.
- **Plan 08, enzyme atlas:** metadata-linked stress context, stability-feature scoring, high-precision enzyme crosswalk, and dataset release/provenance organization. Output role: traceable extremophile atlas supporting enzyme prioritization.

The plan-by-plan differences are therefore methodological adaptations, not separate project identities. The same evidence discipline was applied across modules, but the filters were tuned to the biological claim.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_05_evidence_map.png}
{\scriptsize \textbf{Figure 3. Cross-module evidence coverage.} Green marks strong evidence layers; gold marks contextual or partial layers; gray marks layers that were not central to that module.\par}
\end{center}

## 5. Detailed Methods And Evidence Hardening

The campaign was designed around a practical problem in computational biology: public and local genomics datasets are rich enough to produce thousands of plausible leads, but most first-pass leads are too weak, too generic, or too ambiguous for serious wet-lab discussion. The goal was not to maximize the number of candidates. The goal was to reduce broad candidate universes into smaller sets where each candidate could be defended with a clear chain of evidence.

### 5.1 Candidate Universe Construction

Each module began with a different type of input universe. The BGC module began from strict BGC calls and downstream product-class/dereplication artifacts. The enzyme modules began from large enzyme-family candidate tables and high-precision crosswalks. The nitrogen-cycle module began from marker and pathway hits. The PGP module began from genome-level candidates with plant-associated trait signals. The stability module reused the enzyme universe but filtered it by stability-relevant families and source-condition signals. The rare-chemistry module started from a broad set of rare-function annotations and reaction-class labels. The biomaterials module began from material-associated annotations and then incorporated BGC and genome-context evidence. The atlas module organized the enzyme outputs into a data-publication-style table with metadata and stability-feature scores.

This heterogeneity is a strength of the campaign, but it also creates a risk: a candidate score in one module is not directly comparable to a score in another module. A BGC score, a pathway score, a stability-axis score, and a material-subtype score are not measuring the same thing. The report therefore treats each score as module-local evidence and compares candidates across modules using readiness categories rather than raw numerical scores.

### 5.2 Functional Plausibility

Functional plausibility was the first major gate. For BGCs, plausibility required more than a product-class label. The screen checked whether the candidate had coherent BGC caller support, boundary context, domain logic, whole-MAG support where available, and dereplication context. For enzymes, plausibility required an interpretable family assignment plus some combination of reviewed-reference support, motif evidence, structure confidence, active-site plausibility, Rhea/EC support, or family-specific assay precedent. For nitrogen-cycle candidates, plausibility required marker specificity and pathway context, not just a single marker-like annotation. For PGP candidates, plausibility required trait co-occurrence and ecological context, not merely one plant-associated keyword. For biomaterials, plausibility required material-specific features rather than broad surface, transporter, or housekeeping annotations.

The purpose of this gate was to avoid "annotation optimism." Many annotations are useful as search hints but not strong enough for candidate claims. For example, a broad hydrolase annotation may suggest a possible enzyme family, but it does not define substrate scope. A lipid-A gene may be relevant to microbial envelope biology, but it is not a biosurfactant candidate by itself. A NifH-like domain can be real but still fail as a nitrogen-fixation candidate if the surrounding nitrogenase cluster is missing or confusable. The campaign explicitly demoted such cases.

### 5.3 Context And Recoverability

Context was interpreted differently by module. For BGCs, context meant genome, contig, boundary, product-class, and dereplication context. For enzymes, context meant source environment, closest reviewed homologs, family evidence, structure evidence, and assay tractability. For PGP candidates, context meant plant-associated source metadata, isolate or reference availability, strain-level or species-level reference support, and trait co-occurrence. For nitrogen-cycle candidates, context meant genomic neighborhood and whether the pathway made biological sense beyond the representative marker. For biomaterials, context meant whether the source organism and local annotations supported a plausible material readout.

Recoverability was especially important for organism-level and material-related hypotheses. A genome-level PGP candidate can be compelling computationally but impractical if no culture path, reference path, or isolate context exists. A material candidate can have an interesting domain but be less useful if there is no plausible product or recovery route. The campaign did not eliminate every access-limited candidate, but it separated practical candidates from review-only hypotheses.

### 5.4 Novelty And Dereplication

Novelty was treated as a supporting claim, not as a stand-alone result. For BGCs, novelty was evaluated using MIBiG and BiG-SCAPE context, including targeted and full-MIBiG comparisons. A lack of close BiG-SCAPE linkage at defined cutoffs strengthens a discovery hypothesis, but it does not prove chemical novelty. The product may still be known, convergent, not expressed, or misannotated.

For enzymes, novelty was generally interpreted through closest reviewed-reference identity and query coverage, reciprocal context where available, and family-level support. A low-identity match can support novelty, but if the annotation becomes too vague, functional plausibility drops. The best enzyme candidates therefore occupy a useful middle ground: distant enough to be interesting, close enough or motif-supported enough to define a testable hypothesis.

For pathway and organism-level screens, novelty was less central than coherence. The nitrogen-cycle screen needed clean marker/pathway calls more than novelty. The PGP screen needed reference and trait coherence more than novelty. The biomaterials screen needed material-specificity and product plausibility more than sequence divergence.

### 5.5 Structure, Phylogeny, And Reaction Evidence

Structure and phylogeny were used as hardening layers, not as replacements for wet-lab validation. Plan 03 added IQ-TREE marker-family context for nitrogen-cycle markers. Plan 05 used candidate-specific structures, loop/disorder comparison, structure-energy proxies, ThermoMPNN aggregate summaries, and IQ-TREE3 finalist phylogenies. Plan 06 used candidate-specific structures, reaction-family context, Rhea/EC mapping, and reference ligand-pocket comparison. Plan 02 used structure and active-site bridge evidence for the current dehalogenase and glycosidase leads.

These layers are scientifically useful because they reduce ambiguity. A predicted structure with high confidence can make an enzyme hypothesis more credible, and a phylogeny can show whether a candidate sits in a plausible marker or reaction-family context. However, neither structure nor phylogeny proves activity. Predicted structures do not measure catalysis, product identity, stability, substrate scope, or expression. Phylogenies do not prove phenotype. The report therefore uses these layers to strengthen prioritization, not to validate function.

### 5.6 Safety And Claim Discipline

The campaign used computational safety-context screens to identify obvious local concerns such as candidate-near AMR, mobilome, toxin, virulence, or problematic neighborhood context. These screens are useful for triage. They are not final biosafety decisions. A pass with context note means no obvious local computational blocker was found in the checked artifacts; it does not mean the candidate is safe to use, express, synthesize, release, or commercialize.

Claim discipline was treated as a methodological requirement. Each candidate class has a tempting but unsafe overclaim. BGCs can be overclaimed as antibiotics. Enzymes can be overclaimed as validated catalysts. Nitrogen-cycle markers can be overclaimed as nitrogen flux or emissions reduction. PGP genomes can be overclaimed as crop-benefit organisms. Biomaterial annotations can be overclaimed as material production. The report avoids those claims and states what remains unproven.

### 5.7 Downselection Logic

A candidate advanced only if the evidence supported a specific hypothesis. The screen did not require every candidate to have every evidence layer, because the biology differs across modules. Instead, it required each candidate to clear the evidence layers most relevant to its claim.

For example, a Plan 05 stability candidate needed enzyme-family support, novelty, structure confidence, stability-axis rationale, expression-risk review, and safety-context screening. A Plan 04 PGP candidate needed source context, trait coherence, genome quality, reference or isolate plausibility, and safety-context review. A Plan 01 BGC candidate needed BGC evidence, boundary/domain logic, product-class context, dereplication, and safety/context review. This modular logic is why the report presents plan-specific screening differences while still treating the campaign as one process.

### 5.8 Reproducibility And Tool Provenance

The table below moves the most important reproducibility details from the appendix into the main report. It is not a replacement for the source artifacts, but it gives reviewers enough context to understand what was actually run, what counted as a hard gate, and where computational uncertainty remains.

The provenance digest is:

- **Plan 01 BGCs:** 80 strict packets, seven finalist rows, and three keep candidates. Tooling: antiSMASH 8.0.4, BiG-SCAPE 2.0.3 with full Pfam-A, and MIBiG 4.0 BLAST/cache. Keep required whole-MAG antiSMASH support, no close BiG-SCAPE link at 0.3 or 0.5, no boundary/domain blocker, and no local safety flag. Remaining limitation: no product detection, expression evidence, chemical structure, titer, bioactivity, or chemical novelty proof.
- **Plan 02 enzymes:** 17,932 strict rows, 4,071 high-precision rows, 40 review packets, and two bridge leads. Tooling: full Pfam-A 38.1 `hmmscan --cut_ga`, Swiss-Prot/UniRef/nr dereplication, reciprocal checks, ESMFold/ColabFold structures, and pocket review. Promotion required at least two independent functional layers plus family, motif, dereplication, structure/pocket, and safety-context support. Remaining limitation: activity, substrate scope, kinetics, expression, solubility, and experimental safety review are unmeasured.
- **Plan 03 nitrogen cycle:** 655 first-pass hits, 116 genome-track pathway profiles, and six packets. Evidence: KEGG, Pfam, InterPro, eggNOG, false-positive rules, and Kaggle IQ-TREE 3.1.2 for support-rich families. Promotion required marker specificity, pathway/neighborhood coherence, and rejection or hold of housekeeping, fragment, low-quality, single-gene, and AMO/pMMO-confusable cases. Remaining limitation: IQ-TREE support is local-marker context only; nosZ has three local sequences and is not support-rich.
- **Plan 04 PGP:** 1,679 strict trait hits collapsed to four final genome hypotheses. Evidence: trait matrix, Swiss-Prot driver validation, fastANI/skani reference gates, isolate/cultured-relative triage, source context, and safety context. Promotion required plant or soil relevance, primary trait support, multi-trait architecture, genome quality, no safety hold, and practical reference or isolate route. Remaining limitation: trait genes do not prove trait expression, colonization, plant benefit, organism safety, or field utility.
- **Plan 05 natural stability:** 3,237 focused enzyme rows, 19 shortlist rows, six strict advances, and four immediate candidates. Evidence: ColabFold structures, family MSA, BRENDA context, IQ-TREE3, ThermoMPNN aggregate ddG summaries on Kaggle T4, and bounded charge/salt-bridge proxies. Promotion required family support, stress-axis rationale, reviewed-homolog context, structure confidence, expression-risk review, safety-context pass, and benchmark mapping. Remaining limitation: stability proxies do not measure stability; ThermoMPNN is retained only as candidate-level aggregate context, not mutation advice.
- **Plan 06 rare chemistry:** 11,805 first-pass rows, 300 priority rows, 40 MSA/structure rows, 16 downselected rows, and four immediate candidates. Evidence: Swiss-Prot/reciprocal checks, Rhea/EC and BRENDA reaction mapping, finalist ColabFold, IQ-TREE3 reaction-family context, and ligand-pocket comparison. Promotion required reaction-family mapping, active-site or pocket context, reviewed-homolog MSA, structure confidence, dependency-risk annotation, and safety-context pass. Remaining limitation: reaction-family evidence does not prove substrate specificity, activity, product identity, partner availability, or expression.
- **Plan 07 biomaterials:** 731 first-pass rows plus Plan 01 BGC review rows, 746 final rows, six immediate packets, and three BGC-material holds. Evidence: BGC context, PHA/EPS/pigment/protein-material logic, source metadata, genome quality, recovery gates, and safety gates. Immediate packets required material-specific evidence, source support, export or recovery plausibility, assay feasibility, no unresolved safety hold, and resolved chemistry. Remaining limitation: no metabolomics, product detection, secretion validation, yield, rheology, coating performance, or material-property data.
- **Plan 08 atlas:** 4,071 high-precision atlas rows over 1,289 manifest files. Evidence: source manifests, checksums, row counts, high-precision enzyme crosswalk, and stability-feature model. Promotion here means dataset/provenance readiness, stress metadata, enzyme linkage, genome quality, and dependency penalties. Remaining limitation: atlas scores organize hypotheses; habitat metadata and feature scores are not stability measurements.

The operational gates below are the most review-critical thresholds that are now carried in the main report rather than left only in scripts or packet artifacts.

- **Plan 01 BGC boundary review:** contig-edge proximity was retained as `edge_flag_500bp`; candidates with edge/domain blockers were held even if product-class annotation looked interesting.
- **Plan 02 full-family validation:** full Pfam-A 38.1 was used through `hmmscan --cut_ga`; Pfam/domain support was interpreted only with motif, dereplication, structure, pocket, and safety-context evidence.
- **Plan 03 marker specificity:** exact KO support scored 1.00, exact gene-name support 0.95, marker text support 0.82, and Pfam support 0.76; length-outside-range applied a 0.18 penalty, and confusable terms applied a 0.35 penalty unless an exact KO was present.
- **Plan 03 pathway advance:** candidates were held if genome quality was below 0.40, safety score below 0.50, marker specificity below 0.72, or pathway completeness below 0.58. Advance required completeness at least 0.84, neighborhood support at least 0.55, and source support at least 0.65, plus track-specific core-marker rules.
- **Plan 04 genome quality and reference context:** MGYG000517341 was treated as the clean lead because it was isolate-level, 100.0 percent complete, 0.21 percent contaminated, and had exact fastANI/skani support to GCF_040152065.1 strain UC4318 plus same-species/type-material ANI support. MAGs without close reference or culture routes were downgraded even with coherent trait annotations.
- **Plan 07 biomaterials advance:** immediate packets required final score at least 72 with pathway/material score at least 0.65, application score at least 0.65, safety score at least 0.55, assay score at least 0.55, and no low-quality, housekeeping, weak-specificity, or unresolved BGC-chemistry hold.
- **Candidate-near AMR/mobile windows:** Plan 03 and Plan 07 used 10,000 bp candidate-near AMR/mobile windows around anchor genes; Plan 07 BGC/CAZyme-style local context used a 1,000 bp overlap/nearby window where applicable.

### 5.9 Score Calibration

The campaign uses several different scores. They are not calibrated probabilities and are not compared across plans. A score of 91 in the nitrogen-cycle module is not equivalent to a score of 91 in the biomaterials module. The scores are local ranking aids after false-positive filtering.

The score definitions are:

- **Claim-hardening score:** evidence-convergence score retained in finalist artifacts, not a calibrated probability. Ranges: Plan 01 keep calls 9.25-9.5, Plan 04 final rows 7.0-9.5, Plan 05 immediate rows 9.5-10.0, and Plan 06 immediate rows 9.0-9.75. It is used only after named hard gates pass; it is not a measured effect size, success probability, or safety clearance.
- **Plan 02 enzyme claim-hardening:** two bridge leads scored 11.75 and 11.25 from preserved evidence tokens: domain proxy, MSA, residue pass, catalytic call, dereplication novelty, structure, pocket, expression risk, dependency risk, benchmark, and substrate-panel presence. Both leads were marked as CRO-ready computational packages; the dehalogenase ranked cleaner because active-site geometry and pLDDT evidence were stronger. The score is not enzyme activity, substrate scope, kinetic fitness, expression yield, or lab safety.
- **Bridge score:** local rank score over family support, novelty, structure, context, dependency, expression risk, and assayability. Where the historical weight file was not retained, the score is treated as opaque local rank only. It orders bridge queues after evidence gates and is not validated activity, kinetic fitness, stability, or commercial readiness.
- **Plan 03 pathway final score:** weighted 0-100 score using 20 percent marker specificity, 18 percent completeness, 15 percent neighborhood, 13 percent outcome relevance, 11 percent source support, 10 percent novelty, 7 percent assay, 4 percent genome quality, and 2 percent safety. Six candidates scored 80.72-91.9 after false-positive cleanup and track-specific core-marker requirements. The score is not nitrogen flux, expression, greenhouse effect, emissions reduction, or fertilizer efficiency.
- **Plan 04 PGP bridge score:** 0-100 score over plant-benefit trait support, multi-trait complementarity, crop/stress relevance, wet-lab feasibility, novelty or underexplored taxonomy, genome quality, and safety triage. MGYG000517341 scored 95.224. The score was used with exact/same-species ANI, isolate status, genome quality, source context, and safety context; lower-confidence MAGs were not promoted on score alone.
- **Plan 07 biomaterials final score:** weighted 0-100 score using 20 percent pathway/BGC completeness, 17 percent material fit, 15 percent source support, 13 percent export/recovery, 12 percent novelty, 10 percent assay feasibility, 8 percent genome quality, and 5 percent safety. Immediate packets required score at least 72 plus pathway, application, safety, and assay floors. It is not material production, yield, identity, rheology, adhesion strength, pigment identity, or industrial performance.
- **Plan 08 stability-feature score:** atlas ranking over source-condition label, genome quality, annotation evidence, high-precision enzyme linkage, environmental replication, and dependency penalties. It organized the 4,071-row atlas into reusable stability-testing tracks and provenance bundles; it is not measured thermostability, salt tolerance, solvent tolerance, expression, or activity.

### 5.10 Safety Context Definition

Safety context was used as a triage gate, not as clearance. The report uses terms such as `PASS_WITH_CONTEXT_NOTE` and `NO_LOCAL_FLAGS_DETECTED` because the screen looked for obvious local computational blockers. Those terms are not statements that a gene, organism, construct, product, or environmental use is safe.

The safety score begins at 1.0 in the pathway/material modules and is reduced for context flags. In Plan 03, penalties were pathogen-adjacent taxonomy -0.35, gut source -0.18, genome AMR -0.18, candidate-near AMR within 10,000 bp -0.30, candidate-near mobile element within 10,000 bp -0.16, virulence keyword -0.25, and toxin keyword -0.08. In Plan 07, penalties were pathogen-adjacent taxonomy -0.35, gut source -0.20, genome AMR -0.20, stress-resistance-only rows -0.08, candidate-near AMR within 10,000 bp -0.35, candidate-near mobile element within 10,000 bp -0.18, toxin/virulence keyword -0.35, and contamination above 5 percent -0.15. A score of at least 0.65 produced `PASS_WITH_CONTEXT_NOTE`; lower scores were held or sent to safety-context review.

The safety-context screen is summarized by candidate class:

- **BGCs:** inspected cached AMRFinder outputs, mobilome GFF context, toxin/virulence/mobility keyword scans, contig-edge review, and `edge_flag_500bp`. antiSMASH, BiG-SCAPE, and MIBiG context were retained; rows with AMR, mobile, toxin, virulence, boundary, or domain blockers were not treated as clean packets. A pass means no obvious local computational blocker was detected for packaging; it does not replace institutional biosafety review, product toxicity review, producer-handling review, or therapeutic/environmental safety assessment.
- **Enzyme coding sequences:** inspected candidate-near AMR/mobile context where available, genome-level flags when relevant, dependency notes, and expression-risk notes. No universal window was preserved for every early Plan 02/05/06 packet; later candidate-near windows used 10,000 bp. A pass means the coding-sequence hypothesis did not carry an obvious local computational blocker. Expression safety, substrate/product hazards, host selection, scale-up risk, and lab-specific approval remain outside this report.
- **Genome-level PGP candidates:** inspected genome AMR rows, candidate AMR hits, mobilome burden, mobile-neighborhood terms, toxin/virulence/pathogen terms, source context, and reference/culture availability. MGYG000517341 had genome AMR rows = 0 and no candidate AMR hits; mobile terms remained as context. A pass means no obvious local safety hold was found in checked artifacts. Organism safety, colonization risk, plant/soil/ecosystem behavior, greenhouse or field permissions, and release suitability remain outside this report.
- **Biomaterial candidates:** inspected candidate-near AMR and mobile counts, genome AMR and mobilome rows, recovery route, source taxonomy, and material-track specificity. The module used a 10,000 bp AMR/mobile window around candidate coordinates and a 1,000 bp overlap/nearby window for BGC and CAZyme-like context; immediate packets needed safety score at least 0.55. A pass means the candidate was not blocked by obvious local safety or recovery concerns. Producer safety, product toxicity, purification safety, material exposure risk, and industrial handling approval remain outside this report.
- **Atlas rows:** inspected manifest integrity, source provenance, genome quality, and dependency penalties. The atlas encoded dataset traceability only; no biological safety clearance was encoded. A pass means the row is traceable and prioritized for future review; it carries no biological or environmental safety interpretation.

### 5.11 Candidate Evidence Matrix And Residual Risk

This report makes the review-critical uncertainty visible near the methods rather than hiding it in packet archives. The strongest evidence layer and first discriminator for each candidate class are:

- **Plan 01 BGC keep candidates:** whole-MAG antiSMASH support, full Pfam-A BiG-SCAPE context, MIBiG 4.0 dereplication, boundary/domain pass, and no local safety flags. Principal risk: product may be absent, known, misassigned, not expressed, or inactive. First discriminator: chemistry-first product detection and dereplication before any bioactivity language.
- **Plan 02 dehalogenase lead:** candidate MGYG000527579_00796 has HAD_2 family support, direct structure, ColabFold mean pLDDT 97.194, active-site pocket with D5/S110/N111 and D169 review residue, and safety-context pass. Principal risk: activity and substrate scope may not match the computational dehalogenase frame. First discriminator: expression, soluble recovery, baseline activity, and substrate-panel review under approved lab conditions.
- **Plan 02 glycosidase lead:** candidate MGYG000517010_03432 has GH35/GH43 domain support, later full-length ColabFold mean pLDDT 94.591, and pocket geometry around aromatic and acidic residues. Principal risk: acid/base assignment and family numbering remain less clean than the dehalogenase. First discriminator: expert motif/family-numbering review and baseline activity readout.
- **Plan 03 nitrogen candidates:** nitrogenase and urease candidates have marker/pathway coherence, source context, IQ-TREE context for nifH and ureC, and rejection of AMO/pMMO-confusable calls. Principal risk: marker genes may not be expressed, complete, or phenotypically active. First discriminator: controlled pathway-expression and phenotype validation.
- **Plan 03 nosZ candidates:** completed IQ-TREE treefile and pathway-specific packet evidence. Principal risk: only three local nosZ sequences, so phylogeny is topology/bookkeeping rather than support-rich inference. First discriminator: broader external homolog recruitment or direct controlled phenotype evidence.
- **Plan 04 MGYG000517341:** isolate-level genome, 100.0 percent fastANI/skani match to GCF_040152065.1 strain UC4318, same-species/type-material support, high-quality genome, and seven supported PGP trait classes. Principal risk: trait architecture may not translate to root colonization, plant benefit, or safety. First discriminator: organism access, controlled plant-association assays, expression/trait verification, and institutional safety review.
- **Plan 05 natural homolog candidates:** candidate-specific structures, reviewed-homolog MSA support, BRENDA condition context, IQ-TREE3 finalist context, ThermoMPNN aggregate summaries, and charge/salt-bridge proxies. Principal risk: stability and activity are proxy-supported only; MGYG000517341_01521 has a flexible-region caveat. First discriminator: expression, solubility, activity retention under stress-axis panels, and explicit comparison to reference enzymes.
- **Plan 06 rare-chemistry candidates:** Rhea/EC mapping, reviewed-homolog MSA support, finalist ColabFold structures, IQ-TREE3 context, dependency flags, and reference ligand-pocket comparison. Principal risk: reaction-family support may not resolve true substrate or partner dependency. First discriminator: manual pocket review, dependency/cofactor feasibility review, and baseline reaction readout.
- **Plan 06 dehalogenation:** MGYG000517233_02445 has high structure confidence and low expression risk, with Rhea mapping and dehalogenation-class bridge support. Principal risk: closest curated hit is drimenol cyclase-like, so the dehalogenation label depends on reaction-family and pocket evidence rather than closest-name agreement. First discriminator: manual pocket and mechanism review before substrate-specific dehalogenation language.
- **Plan 07 biomaterial packets:** weighted material-specific score, source context, genome quality, recovery/assay feasibility, and demotion of generic material-like annotations. Principal risk: product identity, secretion/recovery, yield, and material performance are unmeasured. First discriminator: product formation and identity confirmation before any performance or commercial-material claim.
- **Plan 08 atlas:** 4,071-row traceable atlas with source manifests, checksums, stability-feature model, and high-precision enzyme crosswalk. Principal risk: source metadata can enrich prioritization but cannot prove stability. First discriminator: use atlas rows only to select candidates for the separate enzyme screens.

## 6. Rejection And Hold Logic

The supporting appendix is valuable because it preserves both positive and negative evidence. The negative evidence is important for scientific rigor. A screen that only lists hits is hard to trust; a screen that records why candidates were rejected or held is much more defensible.

### 6.1 BGC Holds

The BGC module held four candidates even though they remained scientifically interesting. The reasons were concrete: missing condensation-domain support, contig-edge proximity, incomplete PKS-domain logic, and unresolved boundary concerns. These are not cosmetic issues. BGC boundaries and domain content can determine whether a cluster is biologically interpretable. If a cluster sits near a contig edge, the apparent biosynthetic logic may be incomplete. If a nonribosomal peptide-like candidate lacks necessary condensation-domain support, the product-class interpretation can become unstable. Holding these candidates protects the credibility of the three keep calls.

### 6.2 Enzyme Bridge Limitations

The enzyme module preserved broad review queues but narrowed the current bridge around the dehalogenase and glycosidase candidates. The glycosidase remains limited by unresolved full-length structure/domain orientation. This is a real limitation, not a minor formatting issue. A catalytic motif in a chunk can support a hypothesis, but full-length domain architecture can affect folding, substrate access, and interpretation. The report therefore treats the dehalogenase bridge as cleaner than the glycosidase bridge.

### 6.3 Nitrogen-Cycle False Positives

The nitrogen-cycle screen had the clearest false-positive burden. More first-pass hits were rejected as housekeeping or unrelated domains than were passed as marker-specific. This is expected in marker-based screens because many nitrogen-cycle-related domains have broad homologous families or confusable annotations. The decision to hold nitrification/ammonia-oxidation candidates is particularly important. AMO-like annotations can be confusable with pMMO or related membrane/redox systems, and a weak amo-like hit is not enough to claim nitrification potential.

### 6.4 PGP Holds

The PGP screen shows the difference between a trait hypothesis and an organism-level candidate. MGYG000517341 strengthened because it gained exact/same-species reference support and a clearer organism path. MGYG000535629, MGYG000535630, and MGYG000511828 remained lower-confidence or held because reference gates, culture paths, or source/access context were weaker. This is rigorous because organism-level claims require more than trait annotations.

### 6.5 Stability Candidate Caveats

The Plan 05 stability candidates all advanced, but not equally. MGYG000478572_00760 is the cleanest. MGYG000517341_01521 has the main flexible-region/structure-confidence caveat. MGYG000518629_02280 has expression-design uncertainty. MGYG000478572_01589 has PLP/cofactor complexity. These caveats travel with the candidates and make the first experimental cycle sharper rather than weaker.

### 6.6 Rare-Chemistry Uncertainty

Plan 06 is deliberately higher-risk. It targets rare or underexplored chemistry, which means the candidate hypotheses can be valuable even when substrate specificity is not resolved. The redox candidate has cofactor/partner dependency. The organosulfur candidate has signal-like and pocket-context caveats. The rare-sugar candidate has unresolved substrate specificity. The dehalogenation candidate has excellent predicted structure but needs manual pocket interpretation before substrate claims. These are not failures. They are the correct uncertainty labels for a rare-chemistry screen.

### 6.7 Biomaterials Demotions

The biomaterials module made a large number of demotions because many first-pass material-like hits were too generic. This is a major improvement over a naive screen. Material claims require some evidence of product, polymer, surface function, pigment, or material-relevant domain. Generic membrane, transporter, metal-binding, or housekeeping annotations do not meet that standard. The module also separated BGC/material review holds from immediate material candidates because BGC product chemistry was unresolved.

## 7. Comparative Readiness Across The Campaign

The candidates can be grouped into readiness tiers. These tiers are not validation levels; they are prioritization levels.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_03_output_portfolio.png}
{\scriptsize \textbf{Figure 4. Candidate output portfolio.} Counts reflect packaged candidate hypotheses or immediate plus review candidates; the atlas is provenance infrastructure rather than a comparable candidate count.\par}
\end{center}

### Tier 1: Cleanest Near-Term Experimental Hypotheses

The cleanest near-term experimental hypotheses are those with layered evidence and relatively straightforward first validation questions.

- MGYG000478572_00760, Plan 05 salt-prioritized esterase. This has the best combination of novelty, structure confidence, low expression risk, source context, and assayability among the stability candidates.
- MGYG000527579_00796, Plan 02 dehalogenase bridge lead. This has direct candidate structure support and a clearer active-site bridge than the glycosidase lead.
- MGYG000478572_01589, Plan 05 salt-prioritized transaminase. This is structurally strong, although cofactor complexity makes it slightly less simple than the esterase.
- MGYG000517341, Plan 04 PGP genome hypothesis. This is the cleanest organism-level candidate because of trait coherence and reference support, but organism-level validation remains more complex than enzyme validation.

### Tier 2: Strong But More Caveated Hypotheses

These candidates are scientifically strong but have interpretation or validation complications.

- MGYG000517341_01521, Plan 05 salt dehalogenase. Strong functional hypothesis, but flexible-region and construct/context caveats are more prominent.
- MGYG000518629_02280, Plan 05 pH esterase. Interesting divergent esterase-like candidate, but expression-design uncertainty remains.
- MGYG000478572_02342, Plan 06 redox candidate. Strong rare-chemistry package, but redox cofactor and partner dependence are real experimental risks.
- MGYG000521810_01693, Plan 06 organosulfur candidate. Coherent sulfurtransferase hypothesis, but signal-like and pocket-context uncertainty remain.
- The three Plan 01 BGC keep candidates. They are strong computational natural-product review candidates, but product identity and activity are unresolved.

### Tier 3: Review-First Or Context-Dependent Hypotheses

These candidates deserve review and are best treated as review-first hypotheses before first-line wet-lab prioritization.

- MGYG000517010_03432, Plan 02 glycosidase. The later full-length ColabFold run reduced the earlier structure limitation, but acid/base assignment and family-numbering review still need resolution before it is treated as a clean bridge candidate.
- MGYG000478572_01361, Plan 06 rare-sugar candidate. It is high-upside but substrate specificity remains unclear.
- MGYG000517233_02445, Plan 06 dehalogenation candidate. Excellent predicted structure, but pocket review is needed before substrate claims.
- Plan 07 BGC/material review holds. Product chemistry is unresolved, so they remain chemistry-review candidates.
- MGYG000535629, MGYG000535630, and MGYG000511828 from Plan 04. They are useful PGP hypotheses but weaker than MGYG000517341 for near-term organism-level discussion.

### Tier 4: Archive And Second-Wave Candidates

The broader packet archives remain important. They preserve candidates that may become useful if the project shifts priorities, if early candidates fail, or if additional computational or experimental evidence becomes available. This includes the Plan 01 top-50 BGC queue, the Plan 02/08 enzyme queues, Plan 05 backup stability candidates, and Plan 06 second-wave rare-chemistry leads. These archives function as a structured reserve, not as a list of validated findings.

## 8. Module-Specific Methodological Notes

This section gives additional methodological detail for reviewers who need to understand how the same screening philosophy was adapted to different biological targets.

### 8.1 Plan 01 BGC Methodology

The BGC screen treated cluster calls as hypotheses, not as direct product predictions. The first level of evidence was caller agreement and product-class context from antiSMASH, GECCO, and SanntiS-related artifacts. The second level was boundary and domain review. This was essential because BGC false positives can arise when a predicted region is clipped by a contig edge, lacks expected biosynthetic domains, or combines partial signals into an overinterpreted product class. The third level was dereplication against MIBiG-related contexts using BiG-SCAPE outputs. Candidates were not promoted just because they were distant from known clusters; they also needed coherent local BGC logic. The final product was therefore not a ranked list of "novel compounds" but a smaller review set where product-class and dereplication evidence were strong enough for expert natural-product discussion.

### 8.2 Plan 02 Enzyme Methodology

The enzyme screen used activity-first logic. A candidate needed an interpretable enzyme-family assignment and enough evidence to make the family call experimentally meaningful. This included reviewed-reference context, Pfam/HMMER or related family support, active-site or motif plausibility, sequence recovery, and structural review where available. The workflow also separated large review queues from current bridge leads. This is important because a 40-candidate or 80-candidate archive can be useful for future exploration, while a first experimental package needs to be much smaller. The Plan 02 bridge therefore emphasized candidates with the cleanest structure/function story rather than candidates that merely scored well in a broad enzyme table.

### 8.3 Plan 03 Nitrogen-Cycle Methodology

The nitrogen-cycle screen used marker specificity and pathway coherence as its main safeguards. Nitrogen-cycle genes sit in families with many confusable homologs, and individual marker-like hits can be misleading without neighborhood or pathway context. The screen therefore demoted housekeeping and unrelated domains, held low-coverage fragments, held single-gene-only cases, and required track-specific pathway logic. For nitrogen fixation, compact nif or vnf cluster context mattered. For N2O reduction, nosZ needed accessory context. For nitrate/nitrite transformation, complete nar or nrf-type loci were more credible than isolated redox annotations. For nitrification, weak AMO-like calls were held because AMO/pMMO ambiguity remained unresolved. The IQ-TREE layer then added marker-family context for finalists, but it did not replace phenotype validation.

### 8.4 Plan 04 PGP Methodology

The PGP screen was the most organism-centered module. It did not treat one trait annotation as enough. Instead, it asked whether a genome-level candidate had a coherent plant-associated story: source relevance, trait co-occurrence, genome quality, practical organism or reference access, and no obvious local computational safety burden. Reference ANI and strain dereplication were especially important because organism-level validation is difficult if the candidate cannot be linked to a practical isolate, reference, or close cultured relative. This is why MGYG000517341 strengthened substantially while other candidates remained lower-confidence or held. The method is intentionally stricter than a trait keyword search because PGP claims can easily overreach.

### 8.5 Plan 05 Natural Stability Methodology

The stability module reused the enzyme universe but changed the question. Instead of asking only whether a protein might perform a useful reaction, it asked whether a natural homolog might be worth testing under a stress axis such as salt, pH, heat, or solvent/detergent exposure. The screen used sequence-derived features, source context, family support, BRENDA condition precedent, structure confidence, loop/disorder comparison, charge/salt-bridge proxies, ThermoMPNN aggregate summaries, and phylogeny. These are all proxies. They do not measure stability. Their role is to improve the odds that first-round experimental testing starts with plausible natural homologs rather than arbitrary enzyme hits. The module explicitly avoided mutation design or optimization claims.

### 8.6 Plan 06 Rare-Chemistry Methodology

The rare-chemistry module deliberately accepted more functional uncertainty than the standard enzyme screen because its target space was more exploratory. The workflow prioritized chemistry classes such as redox, organosulfur, rare-sugar, and dehalogenation, then used Rhea/EC mapping, reviewed-reference context, reciprocal checks, MSA review, active-site support, predicted structures, and ligand-pocket comparisons to reduce ambiguity. A candidate could be interesting even if substrate specificity was unresolved, but the report preserves that uncertainty. The method therefore produces reaction-family hypotheses, not substrate-specific claims. This distinction is crucial for rare chemistry because the highest-upside candidates are often not the cleanest annotation matches.

### 8.7 Plan 07 Biomaterials Methodology

The biomaterials screen had to distinguish material-specific evidence from generic cell-surface or housekeeping biology. This was the main reason many first-pass hits were demoted. PHA, EPS/capsule export, surface-adhesive protein, pigment, and BGC/material hypotheses each require different evidence. A PHA-like candidate needs pathway coherence, an EPS candidate needs capsule/export or carbohydrate-context support, a protein-material candidate needs more than generic membrane association, and a pigment candidate needs a plausible pigment/enzyme link. Biosurfactant/BGC rows were held when product chemistry was unresolved. This method protects the report from overclaiming material production or performance based on broad annotations.

### 8.8 Plan 08 Atlas Methodology

The atlas module is not a candidate validation module. It is an infrastructure and data-publication/provenance-readiness layer for the enzyme universe. It organized source manifests, row counts, checksums, high-precision enzyme rows, extremophile metadata, and stability-feature scores. Its stability-feature model combines source-condition context, genome quality, annotation support, high-precision score, environmental replication, and dependency penalties. This makes the enzyme universe more navigable and reusable. It does not convert source metadata into measured stability. The atlas is best used as a prioritization and provenance layer that supports later enzyme-screen decisions.

## 9. Results: Plan 01 Secondary-Metabolite BGC Discovery

Plan 01 focused on secondary-metabolite biosynthetic gene clusters. The module identified natural-product discovery hypotheses that are plausible enough, novel enough, and bounded enough to justify expert review, including antibiotic-lead discussion where the chemistry later supports that direction.

The integrated Plan 01 package represents seven finalist-level candidates. Three were retained as strong keep candidates, and four were held because newer evidence did not resolve boundary or domain blockers. The keep candidates all had whole-MAG antiSMASH direct-region support and no close targeted-MIBiG or full-MIBiG BiG-SCAPE link at the 0.3 or 0.5 cutoffs. This is important because it reduces the chance that these BGCs simply reproduce close known MIBiG families. However, BiG-SCAPE distance is still computational dereplication context, not chemical novelty proof.

The three keep candidates are:

- MGYG000517341:MGYG000517341_17:38631-49536. Product frame: RiPP-like. Integrated call: strong pre-wet-lab expert review with full-MIBiG BiG-SCAPE support. Novelty call: medium-high. Whole-MAG nearest distance: 0.947787. Full-MIBiG nearest accession: BGC0000591, nearest distance 0.656250. Bounded claim: computational RiPP-like BGC review candidate with no close full-MIBiG BiG-SCAPE link at the tested cutoffs.
- MGYG000473561:MGYG000473561_12:259192-267836. Product frame: SanntiS-polyketide with whole-MAG T3PKS support. Novelty call: high sequence novelty. Whole-MAG nearest distance: 0.916402. Full-MIBiG nearest accession: BGC0003137, nearest distance 0.584122. Bounded claim: computational T3PKS/polyketide-like BGC review candidate with high sequence-novelty context and no close full-MIBiG BiG-SCAPE link at the tested cutoffs.
- MGYG000517341:MGYG000517341_21:36974-66085. Product frame: betalactone. Novelty call: medium-high. Whole-MAG nearest distance: 0.850429. Full-MIBiG nearest accession: BGC0001095, nearest distance 0.696282. Bounded claim: computational betalactone-like BGC review candidate with no close full-MIBiG BiG-SCAPE link at the tested cutoffs.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_06_bgc_candidate_panel.png}
{\scriptsize \textbf{Figure 6. Plan 01 BGC candidate panel.} The three keep candidates are framed as natural-product review hypotheses, with product identity and activity left for chemistry-first validation.\par}
\end{center}

The four held candidates show why the hardening process matters:

- MGYG000517341:MGYG000517341_6:34029-49595 was held for unresolved NRP domain logic, including no condensation domain detected.
- MGYG000517651:MGYG000517651_16:191-10832 was held for contig-edge and condensation-domain issues.
- MGYG000511828:MGYG000511828_123:121-7601 was held for contig-edge and incomplete PKS-domain issues.
- MGYG000320982:MGYG000320982_59:318-28393 was held because of contig-edge proximity.

The key scientific result is not simply that three BGCs remain. It is that the screen separated BGCs with a defensible computational review basis from BGCs whose boundaries or biosynthetic logic could mislead downstream interpretation. The strongest Plan 01 claim is: three BGCs are computationally prioritized natural-product review hypotheses with multiple dereplication and boundary checks. This report does not claim product identity, compound novelty, antimicrobial activity, production, titer, or safety; those are the high-value questions that make the BGC set worth chemistry-first follow-up.

## 10. Results: Plans 02 And 08 Enzyme Discovery And Extremophile Atlas

The activity-first enzyme work and the extremophile atlas are tightly linked. Plan 02 focused on industrial biocatalyst discovery. Plan 08 added release metadata, stability-feature scoring, and atlas organization for the larger enzyme universe. Together they form the enzyme-discovery backbone of the campaign.

The enzyme screen produced strict and high-precision review queues across ketoreductases, lipases, proteases, transaminases, peroxidases, dehalogenases, esterases, monooxygenases, glycosidases, nitrilases, cellulases, and xylanases. From that broader space, the current wet-lab bridge focuses most clearly on two candidates:

- MGYG000527579_00796, a dehalogenase bridge lead.
- MGYG000517010_03432, a glycosidase bridge lead.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_07_enzyme_bridge_leads.png}
{\scriptsize \textbf{Figure 7. Plan 02 enzyme bridge leads.} The dehalogenase is the cleaner current bridge lead; the glycosidase remains useful but needs catalytic-residue review.\par}
\end{center}

MGYG000527579_00796 is the cleaner of the two current bridge candidates. It has direct candidate-specific structure support, a normalized mean pLDDT of 0.967 in the bridge summary and a later ColabFold mean pLDDT of 97.194 on the 0-100 scale, plus an active-site lock around D5, S110, and N111, with D169 kept as a mechanistic review residue. The safety-context call is pass with context note. The strongest bounded claim is that MGYG000527579_00796 is a computationally prioritized dehalogenase candidate with structure and active-site support. The unresolved items are activity, substrate scope, kinetic behavior, expression, and experimental safety review.

MGYG000517010_03432 remains interesting but less clean. It is a glycosidase candidate with GH35/GH43-style domain support, a later full-length ColabFold model with mean pLDDT 94.591 on the 0-100 scale, and pocket geometry around an aromatic platform plus acidic residues. This later structure removes the earlier full-length-structure blocker, but it does not remove the acid/base assignment and family-numbering review. The strongest bounded claim is that it is a computational glycosidase hypothesis with structure support that still needs expert catalytic-residue review before it is treated as a clean bridge lead. It is framed as a strong secondary enzyme lead rather than as equally clean to the dehalogenase.

The Plan 08 atlas adds a broader dataset-provenance and stability-prioritization layer. The atlas includes 4,071 high-precision rows and data-publication-style provenance over 1,289 manifest files. Its extremophile metadata audit captured desiccation, heat, marine-salt, heat-biomass, cold, heat-pressure, and salt labels. The top stability-testing tracks included desiccation glycosidases, heat-pressure glycosidases, desiccation esterases, desiccation dehalogenases, desiccation proteases, desiccation lipases, desiccation cellulases, heat-pressure nitrilases, desiccation xylanases, heat-pressure proteases, heat-pressure esterases, and salt glycosidases.

The atlas is valuable because it makes the enzyme discovery layer traceable and reusable. It is a prioritization and provenance table rather than a validation table. Habitat labels and stability-feature scores can guide prioritization, but they do not prove that a protein is stable, active, expressible, or industrially useful.

The strongest combined claim for Plans 02 and 08 is: the campaign produced a traceable enzyme candidate universe, strict and high-precision enzyme review queues, two current bridge candidates, and a provenance-ready atlas for future stability-testing prioritization. The claim does not extend to validated biocatalysts; it establishes a strong, audit-ready starting point for discovering them.

## 11. Results: Plan 03 Nitrogen-Cycle Pathway Discovery

Plan 03 screened nitrogen-cycle pathway hypotheses. It began with 655 first-pass nitrogen-cycle hits and rebuilt the ranking around marker specificity, pathway completeness, genomic neighborhood, source context, genome quality, and safety/practicality gates. The final master table contained 116 genome-track pathway profiles, and six candidates advanced to immediate pre-wet-lab packets.

The first-pass false-positive outcome shows how aggressive the cleanup had to be. The screen rejected 324 hits as housekeeping or unrelated domains, passed 125 as marker-specific, held 103 for low coverage or fragment status, held 53 as single-gene-only cases, held 28 for low genome quality, and held 22 for confusable domains. This step is central to the rigor of Plan 03. Nitrogen-cycle annotation can be misleading if generic NifH-like, redox, copper-binding, Fe-S, amidohydrolase, or membrane-associated annotations are accepted without pathway context.

The six advanced candidates were:

- `MGYG000517341_00816`, Plan 03 nitrogen-fixation packet from genome MGYG000517341. Representative marker: nifH. Score: 91.9. Source context: saline. Claim boundary: does not prove nitrogen fixation activity, plant benefit, fertilizer replacement, or environmental safety.
- `MGYG000478572_00459`, Plan 03 nitrous-oxide-reduction packet from genome MGYG000478572. Representative marker: nosZ. Score: 91.61. Source context: saline. Claim boundary: does not prove N2O reduction activity, emissions reduction, soil performance, or environmental safety.
- `MGYG000473561_03510`, Plan 03 nitrous-oxide-reduction packet from genome MGYG000473561. Representative marker: nosZ. Score: 91.25. Source context: hydrothermal. Claim boundary: does not prove N2O reduction activity or environmental performance.
- `MGYG000511828_04091`, Plan 03 urea and rhizosphere nitrogen packet from genome MGYG000511828. Representative marker: ureC alpha. Score: 87.7. Source context: soil. Claim boundary: does not prove urease activity, fertilizer efficiency, plant-growth benefit, or inoculant safety.
- `MGYG000517341_01850`, Plan 03 urea and rhizosphere nitrogen packet from genome MGYG000517341. Representative marker: ureC alpha. Score: 86.42. Source context: saline. Claim boundary: does not prove urease activity or plant benefit.
- `MGYG000511829_04732`, Plan 03 nitrate and nitrite transformation packet from genome MGYG000511829. Representative marker: narG or napA nitrate reductase. Score: 80.72. Source context: soil. Claim boundary: does not prove nitrogen flux, DNRA or denitrification rate, ecosystem nitrogen retention, or field performance.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_08_nitrogen_candidate_tracks.png}
{\scriptsize \textbf{Figure 8. Plan 03 nitrogen-cycle packets.} Six pathway hypotheses survived marker-specificity, pathway-context, source, and safety filters.\par}
\end{center}

The phylogeny update improved the evidence layer. IQ-TREE was completed for narG/napA, nifH, nosZ, and ureC. The narG/napA family had 39 sequences and completed ModelFinder, UFBoot, and SH-aLRT support. The nifH family had four sequences and placed MGYG000517341_00816 with MGYG000517341_02910 at strong local support, but the small family size limits broad evolutionary claims. The nosZ tree completed, but only three sequences were present, so it is useful for topology/bookkeeping rather than support-rich inference. The ureC family had 17 sequences and placed the two ureC candidates in a broader supported UreC context.

The screen also made important negative calls. Nitrification and ammonia-oxidation candidates were not advanced because AMO/pMMO identity and complete amoABC/hao support were not clean enough. That restraint is scientifically important. A less rigorous screen could have promoted AMO-like annotations prematurely.

The strongest Plan 03 claim is: six nitrogen-cycle pathway hypotheses were computationally prioritized with marker-model, pathway-context, source-metadata, novelty, genome-quality, safety-context, and marker-phylogeny support. The claim does not extend to measured nitrogen transformation, greenhouse performance, emissions reduction, fertilizer efficiency, or environmental safety; those are precisely the consequential outcomes that make the best Plan 03 candidates important to validate.

## 12. Results: Plan 04 Plant-Growth-Promotion Genome Discovery

Plan 04 evaluated plant-associated genomes and MAGs as plant-growth-promotion hypotheses. This module differs from the enzyme and BGC modules because the candidate unit is an organism or genome-level hypothesis, not a single protein or gene cluster. That makes the claim space broader and riskier. The screen therefore emphasized trait coherence, source/ecology, reference access, strain-level context, and safety-context filtering.

The final interpretation is that Plan 04 produced one cleanest organism-level lead and three lower-confidence or held hypotheses:

- MGYG000517341. Primary frame: osmoprotection and stress-associated PGP. This is the strongest Plan 04 hypothesis. It has high-quality genome context, tomato and rhizosphere relevance, stress-relevant trait architecture, safety-context pass, trait literature support, and exact same-species ANI support to public reference material. The reference gate was the most important upgrade: MGYG000517341 matched NCBI reference GCF_040152065.1 strain UC4318 at 100 percent fastANI and skani support, with additional same-species support against reference and type material. This makes it the cleanest organism-level candidate for collaborator discussion.
- MGYG000535629. Primary frame: siderophore-linked PGP hypothesis in a Bacteriovorax context. It has barley rhizosphere context and useful trait evidence, but RefSeq ANI supported only distant genus-level context. It remains a lower-confidence surrogate or trait hypothesis rather than a clean organism-level candidate.
- MGYG000535630. Primary frame: antifungal BGC hypothesis in a rhizosphere context. It remains interesting because of plant and rhizosphere context, but selected reference gating was low ANI and low coverage. It is an organism-level hold.
- MGYG000511828. Primary frame: phosphate solubilization. The trait story is coherent, but the source and culture path is weaker, and selected Methylomirabilota reference gating was low ANI and low coverage. It is also an organism-level hold.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_09_pgp_lead_profile.png}
{\scriptsize \textbf{Figure 9. Plan 04 PGP lead profile.} MGYG000517341 is the cleanest organism-level discussion lead because source context, genome quality, ANI support, trait architecture, and safety-context triage converge.\par}
\end{center}

The organism-level evidence digest separates the apparent biological appeal of a PGP trait from practical recoverability and reference support.

- **MGYG000517341:** isolate from tomato rhizosphere; completeness 100.0 percent; contamination 0.21 percent; 87 contigs; N50 178,766; seven supported PGP trait classes; exact fastANI/skani match to NCBI GCF_040152065.1 strain UC4318; same-species/type-material ANI support. Safety/packaging: pass with context note, genome AMR rows = 0, candidate AMR hits = none, toxin/virulence/pathogen terms = none, and mobilome terms present as context. This is the cleanest organism-level discussion lead, while still not a validated PGP organism.
- **MGYG000535629:** MAG from barley rhizosphere; good quality; six supported trait classes with siderophore framing in a Bacteriovorax context; distant genus-level context only, best skani ANI 90.12 with low query alignment fraction. Safety/packaging: pass with context note, but no close isolate or recovery route was resolved. It remains a useful trait hypothesis with a weaker organism-level route.
- **MGYG000535630:** MAG from barley rhizosphere; good quality; six supported trait classes with antifungal/BGC framing; selected UBA11398 reference gate was low ANI and low coverage. Safety/packaging: pass with context note, but organism-level recovery remains unresolved. It stays on hold until better reference or recovery route exists.
- **MGYG000511828:** MAG from soil context; good quality; six supported trait classes with phosphate-solubilization framing; selected Methylomirabilota gate was low ANI and low coverage. Safety/packaging: pass with context note, but crop/source and culture path are weaker. It stays on hold for organism-level packaging.

The most scientifically important outcome of Plan 04 is the distinction between trait coherence and phenotype validation. A genome can encode traits associated with osmoprotection, phosphate solubilization, siderophore production, or antifungal potential, but it does not follow that the organism improves plant growth. It may not colonize roots, express the relevant traits under tested conditions, be recoverable, or be safe for intended use. The screen supports prioritization only.

The strongest Plan 04 claim is: MGYG000517341 is a computationally prioritized plant-associated genome-level PGP hypothesis with source, trait, reference, and safety-context support. The remaining candidates are lower-confidence or held hypotheses. No plant-growth effect, greenhouse performance, field performance, release suitability, or organism safety is established.

## 13. Results: Plan 05 Natural Stability Enzyme Discovery

Plan 05 was a stability-first extension of the enzyme universe. Instead of designing mutations, it asked whether natural homologs from stress-associated contexts could be prioritized for experimental validation of activity and stress tolerance. This distinction is important. The screen does not propose engineered variants or optimization strategies. It prioritizes naturally occurring proteins as wild-type hypotheses.

The focused Plan 05 input pool contained 3,237 rows across dehalogenases, esterases, glycosidases, lipases, proteases, and transaminases. The stability-axis distribution was dominated by salt-associated candidates, with additional solvent/detergent, pH, and heat-axis rows. The screen produced 19 natural-stability shortlist candidates, 19 strict bridge candidates, six strict advance calls, and four immediate wet-lab planning candidates.

The four immediate candidates are:

- MGYG000478572_00760. Family: esterase. Primary axis: salt. Bridge score: 133.119. Closest curated hit: P18773 esterase at 39.367 percent identity and 73.0 percent query coverage. Novelty: high sequence novelty. Expression risk: low. Safety/context: pass with context note. Candidate-specific ColabFold mean pLDDT: 96.301. Interpretation: cleanest near-term Plan 05 lead because it combines high sequence novelty, strong structure confidence, low expression risk, marine/salt context, and a straightforward esterase hypothesis.
- MGYG000517341_01521. Family: dehalogenase. Primary axis: salt. Bridge score: 128.637. Closest curated hit: P60527, an S-2-haloacid dehalogenase, at 30.317 percent identity and 86.0 percent query coverage. Novelty: high sequence novelty. Expression risk: moderate. Candidate-specific ColabFold mean pLDDT: 90.371. Interpretation: attractive dehalogenase hypothesis, but it has the main flexible-region and structure-confidence caveat in the immediate set.
- MGYG000518629_02280. Family: esterase. Primary axis: pH. Bridge score: 126.830. Closest curated hit: P82450 sialate O-acetylesterase at 26.990 percent identity and 91.0 percent query coverage. Novelty: high sequence novelty. Expression risk: moderate. Candidate-specific ColabFold mean pLDDT: 94.137. Interpretation: pH-axis esterase-like candidate with useful novelty, but expression-design uncertainty remains.
- MGYG000478572_01589. Family: transaminase. Primary axis: salt. Bridge score: 121.602. Closest curated hit: B8DJJ6 LL-diaminopimelate aminotransferase at 31.646 percent identity and 97.0 percent query coverage. Novelty: high sequence novelty. Expression risk: moderate because of PLP/cofactor dependence. Candidate-specific ColabFold mean pLDDT: 96.985. Interpretation: strong structural candidate and strong salt-axis score, with biochemical complexity from cofactor dependence.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_10_stability_candidates.png}
{\scriptsize \textbf{Figure 10. Plan 05 stability-test candidates.} Four natural homologs were prioritized for stress-condition testing, with stability still treated as unmeasured.\par}
\end{center}

The final hardening pass made Plan 05 one of the strongest packages in the campaign. All four finalists gained candidate-specific structures, IQ-TREE3 phylogenies, loop/disorder comparison, charge/salt-bridge proxies, ThermoMPNN aggregate context, and benchmark framing. These layers improve prioritization confidence, but they do not measure activity or stability.

Two backup strict-pass candidates were also retained in the source material: MGYG000478572_02520, a salt-axis protease, and MGYG000517233_02590, a pH-axis esterase. They remain useful second-wave candidates if the immediate set fails expression or if the stability panel is broadened later.

The strongest Plan 05 claim is: four natural enzyme homologs were computationally prioritized for stress-condition testing with layered sequence, structure, phylogeny, safety-context, and stability-proxy evidence. They are not validated stable enzymes.

## 14. Results: Plan 06 Rare-Chemistry Enzyme Discovery

Plan 06 was designed to identify candidates with plausible rare or underexplored chemistry. It is intentionally more speculative than the activity-first enzyme screen. The goal was to produce testable rare-chemistry hypotheses, not clean substrate-specific assignments.

The workflow began with 11,805 first-pass candidates and retained chemistry classes including dehalogenation, redox, C-H activation, rare-sugar chemistry, organosulfur chemistry, organophosphorus chemistry, and adjacent halogenation. It produced a 300-candidate priority queue, a 40-candidate MSA/structure review queue, 40 strict bridge candidates, 16 downselected rare-chemistry candidates, and four immediate wet-lab planning candidates.

The four immediate candidates are:

- MGYG000478572_02342. Class: redox. Source context: saline marine Marinobacter salinexigens. Bridge score: 111.268. Closest curated hit: Q64FW2 all-trans-retinol 13,14-reductase at 40.755 percent identity and 93.0 percent query coverage. Rhea support: RHEA:19193. Expression risk: moderate. Active-site call: supported active-site/reaction context. Candidate-specific ColabFold mean pLDDT: 94.336. Interpretation: strongest all-around Plan 06 candidate, but redox cofactor/partner dependency remains the main risk.
- MGYG000521810_01693. Class: organosulfur. Source context: hydrothermal marine sediment Guyparkeria hydrothermalis. Bridge score: 109.489. Closest curated hit: P16385 thiosulfate sulfurtransferase at 29.885 percent identity and 77.0 percent query coverage. Rhea support: RHEA:16881 and RHEA:21740. Expression risk: moderate. Candidate-specific ColabFold mean pLDDT: 93.154. Interpretation: coherent sulfurtransferase/rhodanese-like hypothesis with partial pocket-context limitations.
- MGYG000478572_01361. Class: rare sugar. Source context: saline marine Marinobacter salinexigens. Bridge score: 108.523. Closest curated hit: P0A5D2 uncharacterized epimerase-like hit at 26.027 percent identity and 69.0 percent query coverage. Rhea support: RHEA:22168. Expression risk: moderate. Candidate-specific ColabFold mean pLDDT: 89.37. Interpretation: high-upside rare-sugar hypothesis, but substrate specificity and pocket context remain unresolved.
- MGYG000517233_02445. Class: dehalogenation. Source context: desert/rhizosphere Desertivirga. Bridge score: 104.18. Closest curated hit: A0A0U5GNT1 drimenol cyclase at 26.238 percent identity and 98.0 percent query coverage. Rhea support: RHEA:11192. Expression risk: low. Candidate-specific ColabFold mean pLDDT: 98.359. Interpretation: best direct structure confidence and lowest expression risk in the set, but manual pocket review is needed before substrate-specific dehalogenation claims. The dehalogenation label is a reaction-family hypothesis because the closest curated-name match is not itself a clean substrate-specific dehalogenase annotation.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_11_rare_chemistry_candidates.png}
{\scriptsize \textbf{Figure 11. Plan 06 rare-chemistry candidates.} These candidates are reaction-family hypotheses; substrate-specific assignments remain experimental.\par}
\end{center}

The final hardening pass added formal IQ-TREE3 reaction-family phylogenies, standardized cofactor/partner dependency flags, Rhea/EC consistency review, and reference ligand-pocket comparison. The pocket layer produced one pass-level reference pocket context and three partial or manual-review-limited cases. This supports a cautious interpretation: the rare-chemistry set is strong enough for hypothesis-driven experimental planning, but not for validated function claims.

The strongest Plan 06 claim is: four rare-chemistry enzyme hypotheses were computationally prioritized with sequence novelty, reaction mapping, structure confidence, phylogeny, and safety-context evidence. They are not validated enzymes, and substrate-specific claims remain experimental.

## 15. Results: Plan 07 Biomaterials And Biopolymers

Plan 07 screened microbial biomaterials, including biopolymer/EPS candidates, protein-material candidates, pigment/material candidates, and biosurfactant/BGC review candidates. It started from 731 first-pass biomaterials hits and added BGC, genome-quality, source-environment, recovery, and safety-context gates. After adding Plan 01 strict BGC review rows for the biosurfactant/BGC track, the final master table contained 746 rows.

The track distribution was dominated by protein-material candidates, followed by biosurfactant BGCs, biopolymer/EPS candidates, and one pigment/material candidate. The status calls show the main false-positive burden: 406 rows were held for weak material specificity, 96 were kept as review backups, 78 were held for low genome quality, 63 were kept as pre-wet-lab packet candidates, 54 were held as housekeeping lipid-A/LPS rather than biosurfactant evidence, and smaller groups were held for generic protein, incomplete biosurfactant evidence, low priority, or safety context.

The immediate packet set contains six candidates:

- MGYG000517341_02043. Track: biopolymers/EPS. Subtype: PHA/polyhydroxyalkanoate. Score: 84.04. Status: keep pre-wet-lab packet. Claim boundary: does not prove polymer production, chemistry, yield, material properties, or organism safety.
- MGYG000478572_01331. Track: biopolymers/EPS. Subtype: EPS/capsule export. Score: 84.43. Status: keep pre-wet-lab packet. Claim boundary: does not prove recoverable polymer or material performance.
- MGYG000517341_00932. Track: biopolymers/EPS. Subtype: EPS/capsule export. Score: 83.47. Status: keep pre-wet-lab packet. Claim boundary: does not prove polymer production, polymer chemistry, yield, material properties, or organism safety.
- MGYG000517341_02173. Track: protein materials. Subtype: surface adhesive protein. Score: 83.27. Status: keep pre-wet-lab packet. Claim boundary: does not prove expression, folding, coating performance, adhesion strength, or safety.
- MGYG000521810_02082. Track: protein materials. Subtype: surface adhesive protein. Score: 83.27. Status: keep pre-wet-lab packet. Claim boundary: does not prove expression, folding, coating performance, adhesion strength, or safety.
- MGYG000517341_02282. Track: pigments/functional materials. Subtype: tyrosinase/melanin-like. Score: 79.04. Status: keep pre-wet-lab packet. Claim boundary: does not prove pigment production, melanin identity, yield, or functional material performance.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_12_biomaterial_candidate_packets.png}
{\scriptsize \textbf{Figure 12. Plan 07 biomaterial packets.} The six immediate biomaterial candidates are grouped by material hypothesis and first unresolved product-performance gap.\par}
\end{center}

The six immediate material packets are not equally complete. The PHA/EPS rows have the clearest first-pass product logic, the surface-protein rows have more expression/localization uncertainty, and the tyrosinase row is compact but depends on product-identity confirmation.

- **MGYG000517341_02043, PHA:** pathway complete with PhaC plus same-genome PHA/phasin/PhaR support, score 0.95. Export/recovery is partial because PHA is an intracellular recoverable polymer, score 0.58. Product class is specific PHA, recovery is plausible through the isolate/close-culture route, and assay simplicity scored 0.86. Remaining gap: polymer formation, chemistry, yield, and material-property measurement.
- **MGYG000478572_01331, EPS:** pathway complete with core EPS/capsule export or initiation gene support, score 0.82, and locus support count 3. Export/recovery is supported, score 0.85. Product class is EPS/capsule, recovery is partial because the route is MAG or unconfirmed, and assay simplicity scored 0.78. Remaining gap: recoverable EPS, carbohydrate identity, yield, and rheology.
- **MGYG000517341_00932, EPS:** pathway complete with EPS/capsule gene plus SanntiS saccharide and dbCAN capsule-polysaccharide context. Export/recovery is supported, score 0.85. Product class is EPS/capsule, recovery is plausible through the isolate/close-culture route, and assay simplicity scored 0.78. Remaining gap: recoverable EPS, carbohydrate identity, yield, and rheology.
- **MGYG000517341_02173, surface protein:** pathway evidence is partial, with surface adhesin/domain architecture score 0.86. Export/recovery is supported by localization score 0.86. Product class remains a partial surface-adhesive hypothesis, recovery is plausible through the isolate/close-culture route, and assay score is partial at 0.68. Remaining gap: expression, folding, localization, surface binding, and coating performance.
- **MGYG000521810_02082, surface protein:** pathway evidence is partial, with surface adhesin/domain architecture score 0.86 and locus support count 3. Export/recovery score is 0.86. Product class remains a partial surface-adhesive hypothesis, recovery is partial from MGnify isolate metadata only, and assay score is partial at 0.68. Remaining gap: expression, folding, localization, surface binding, and coating performance.
- **MGYG000517341_02282, pigment:** pathway evidence is partial, with tyrosinase/melanin-like hit plus local context, score 0.86. Export/recovery is partial because the export route is not established, score 0.60. Product class remains a partial melanin-like pigment hypothesis, recovery is plausible through the isolate/close-culture route, and assay simplicity scored 0.76. Remaining gap: pigment production, melanin identity, yield, functional material behavior, and candidate-near mobile context.

Three BGC/material candidates remain review holds rather than immediate wet-lab candidates:

- MGYG000517341:MGYG000517341_27:9851-55107. Subtype: NRP/lipopeptide-like BGC review. Status: review BGC chemistry not resolved.
- MGYG000517341:MGYG000517341_2:234333-279288. Subtype: NRP/lipopeptide-like BGC review. Status: review BGC chemistry not resolved.
- MGYG000521810:MGYG000521810_13:25308-46111. Subtype: hserlactone BGC review. Status: review BGC chemistry not resolved.

The important methodological result is that generic material-like annotations were not allowed to dominate. Lipid-A/LPS genes were explicitly demoted as housekeeping envelope biosynthesis rather than biosurfactant evidence. Generic metal-binding, self-assembling, transporter, and housekeeping hits were held or demoted when they did not support material-specific claims.

The strongest Plan 07 claim is: the screen produced computational biomaterial hypotheses with pathway, source-environment, novelty/recovery, safety-context, and assay-feasibility support. It does not prove material production, yield, product identity, recoverability, performance, or organism safety.

## 16. Cross-Campaign Interpretation

The campaign produced several classes of output with different strengths and risks. Taken together, the results are unusually broad for a single computational genomics effort: they connect natural products, enzymes, nitrogen cycling, plant-associated genomes, rare chemistry, biomaterials, and provenance infrastructure under one evidence-preserving screening framework.

The cleanest near-term wet-lab package is Plan 05. Its four natural homolog candidates prioritized for stability testing have layered evidence: sequence novelty, family support, candidate-specific structures, phylogeny, stability proxies, ThermoMPNN aggregate context, expression-risk flags, and safety-context screening. This does not validate stability, but it makes the candidates unusually explainable and experimentally tractable for a first-pass enzyme validation package.

The strongest activity-first enzyme bridge candidate is MGYG000527579_00796 from Plan 02. It is more focused than the broad enzyme queues and has direct structure and active-site support. The glycosidase MGYG000517010_03432 remains a credible secondary bridge lead, with later full-length ColabFold support, while its acid/base assignment and family-numbering review keep it slightly behind the dehalogenase.

The most practical organism-level candidate is MGYG000517341 from Plan 04. It benefits from trait coherence, source context, reference support, and practical organism-level framing. If this candidate performs in controlled plant-association assays, it could become one of the most societally relevant outputs in the campaign because plant stress resilience and nutrient-use efficiency are high-impact agricultural problems. Organism-level claims remain intrinsically higher risk than isolated enzyme claims because plant benefit, colonization, and safety depend on complex experimental systems.

The most societally consequential modules are Plan 03 and Plan 04, because nitrogen cycling, N2O reduction, fertilizer efficiency, and plant stress resilience are important agricultural and climate-linked problems. These modules are also the most validation-intensive. Pathway or trait evidence is not phenotype evidence, but the computational narrowing is meaningful because it identifies a small set of candidates where controlled experiments could test genuinely consequential hypotheses.

The highest discovery-upside modules are Plan 01 and Plan 06. BGCs and rare-chemistry enzymes are high-variance spaces where a single validated hit can be scientifically valuable. Product identity, reaction specificity, and activity cannot be inferred confidently from computational evidence alone, so these modules are framed as discovery hypotheses rather than validated product leads. That framing preserves credibility while still recognizing the upside.

Plan 07 is attractive for biomaterials partnerships because it gives multiple material classes and relatively intuitive readouts. Material claims require measured production, purification or recovery, identity, yield, and performance. The current evidence supports candidate prioritization and creates a practical starting set for product-identity and material-property testing.

Plan 08 is best understood as infrastructure. It makes the enzyme work more reusable by organizing atlas metadata, source provenance, row counts, and stability-feature scores. Its value is traceability and prioritization, not direct candidate validation.

## 17. Scientific Rigor And Quality Control

The scientific rigor of the campaign comes from multiple forms of constraint.

First, the screens used domain-specific false-positive logic. Plan 01 held BGCs with unresolved domain or contig-edge problems. Plan 03 rejected housekeeping and confusable nitrogen-marker hits. Plan 07 demoted housekeeping lipid-A/LPS annotations rather than calling them biosurfactants. Plan 04 separated trait coherence from organism-level practicality. These negative calls are as important as the positive candidates.

Second, the strongest outputs use layered evidence. A candidate is more credible when annotation, source context, novelty, structure, phylogeny, and safety/context review agree. This report emphasizes convergence rather than any single score.

Third, the project retained traceability. Candidate archives preserve packet text and source paths. The full appendix preserves detailed reports and table evidence. This makes it possible to audit why each candidate was advanced, held, or retained for review.

Fourth, the report maintains claim discipline. It does not treat computational scores as measurements. It does not treat environmental source as phenotype. It does not treat structure confidence as activity. It does not treat absence of local computational safety flags as final safety clearance.

The main remaining methodological weaknesses are also clear:

- Some modules still rely heavily on cached annotations rather than fresh full reannotation across all genomes.
- Several candidate classes need broader external dereplication or experimental product confirmation.
- Some phylogenies have small local sequence families, especially nosZ.
- Some structure claims rely on predicted models and proxy metrics rather than experimental structures.
- Genome-level and organism-level claims remain much harder to validate than single-protein claims.
- Safety/context triage is computational and cannot replace institutional review.

These weaknesses do not invalidate the campaign. They define what must happen next.

## 18. Validation Roadmap

The next stage is staged validation rather than broad simultaneous testing.

\begin{center}
\includegraphics[width=0.98\linewidth]{figures/figure_04_validation_ladder.png}
{\scriptsize \textbf{Figure 5. Validation ladder.} The present report supports computational prioritization and expert-review planning; stronger biological or product claims require new experimental data.\par}
\end{center}

For enzyme candidates, the first questions are expression, soluble recovery, baseline activity, substrate scope, and condition-dependent behavior. Plan 05 and the Plan 02 dehalogenase are the most coherent first enzyme set because they have the best computational-to-wet-lab bridge evidence.

For BGC candidates, the first questions are product formation, product identity, dereplication at the chemistry level, and bioactivity only after product evidence exists. Plan 01 remains expert-review and chemistry-first.

For nitrogen-cycle candidates, the first questions are organism or gene-context recovery, marker/pathway expression, and controlled phenotype measurement. Greenhouse, emissions, fertilizer, soil, or field claims begin only after controlled phenotype evidence supports them.

For PGP candidates, the first questions are organism access, controlled plant-association testing, trait expression, and safety review. MGYG000517341 is the cleanest discussion lead, but it is not a validated PGP organism.

For biomaterials candidates, the first questions are product formation, material identity, recoverability, and measured material properties. BGC/material review holds remain product-chemistry review candidates until chemistry is clarified.

The validation roadmap is milestone-based. A candidate moves from computational priority to validated candidate only after the specific experimental evidence supports that exact claim.

## 19. Candidate Archives

Candidate details have been separated into archives so this report remains readable while retaining evidence traceability.

| Archive | Contents | Records |
|---|---|---:|
| 01 secondary metabolite BGC | Plan 01 high-priority and top-50 BGC packets | 80 |
| 02/08 enzyme and atlas-linked enzymes | Plans 02/08 high-precision and strict enzyme packets | 80 |
| 03 nitrogen cycle | Plan 03 nitrogen-cycle packets | 6 |
| 04 plant-growth promotion | Plan 04 PGP genome packets | 4 |
| 05 natural stability | Plan 05 natural-stability enzyme packets | 4 |
| 06 rare chemistry | Plan 06 rare-chemistry enzyme packets | 4 |
| 07 biomaterials | Plan 07 biomaterials and BGC/material packets | 9 |
| 08 extremophile atlas | Plan 08 atlas report and stability-feature table index | 4,071 atlas rows |

The files are stored under `candidate_archives/` with the same numeric prefixes used in the table.

The candidate archives are evidence files, not validation reports. They preserve computational packet details and source paths for review.

## 20. Claim Boundaries

The strongest truthful framing is:

This campaign produced an integrated, evidence-preserving computational prioritization system across multiple genomics-derived biological candidate classes. It identified review-ready and pre-wet-lab hypotheses with explicit evidence gates, candidate archives, and traceable supporting artifacts. The portfolio is scientifically meaningful because several candidates sit at the intersection of strong computational evidence and high-impact application areas, including natural-product discovery, enzyme biotechnology, climate-relevant nitrogen cycling, plant stress resilience, and biomaterials.

This report does not claim:

- validated antibiotics or antimicrobial compounds
- validated enzymes or industrial catalysts
- validated nitrogen fixation, N2O reduction, or nitrogen flux
- validated PGP organisms or plant-growth benefits
- validated biomaterials or material properties
- environmental safety or release readiness
- expression-ready or synthesis-ready biological products
- field-ready applications

The distinction strengthens the credibility of the project. The report is optimistic because the candidate portfolio is strong, and it is credible because each claim is tied to the evidence actually produced.

## 21. Conclusion

Perusing Biological Datasets is a unified computational genomics campaign that turns large biological datasets into traceable, bounded candidate hypotheses. Its strength is breadth plus evidence discipline: the same prioritization logic was adapted across BGCs, enzymes, nitrogen pathways, PGP genomes, stability-focused homologs, rare chemistry, biomaterials, and atlas infrastructure.

The most mature near-term packages are the Plan 05 natural-stability enzyme set, the Plan 02 dehalogenase bridge lead, and the Plan 04 MGYG000517341 PGP genome hypothesis. The highest-upside but more uncertain packages are Plan 01 BGC discovery and Plan 06 rare chemistry. Plan 03 and Plan 07 are societally and commercially interesting because they connect to nitrogen cycling, plant-associated traits, and biomaterials; their next value inflection point is careful phenotype or material validation.

The full 325-page appendix and the separate candidate archives preserve the detailed evidence. This report provides the scientific narrative: one integrated screen, plan-specific methods, consequential candidate classes, bounded results, and a clear path from computational prioritization to responsible experimental validation. If wet-lab screening confirms even a subset of the strongest candidates, the campaign could support meaningful follow-on work in biotechnology, agriculture, environmental microbiology, natural products, and biomaterials.
