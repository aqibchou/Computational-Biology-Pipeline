# Screening Framework

This repository records a completed computational genomics discovery campaign. The shared framework below explains how the screens were run and how the resulting candidates should be interpreted.

The campaign did not treat a database hit as a discovery by itself. Each module started from broad public or local genomics-derived search space, then narrowed candidates through annotation quality, source context, dereplication, structure or pathway evidence, safety-context triage, and practical wet-lab handoff logic.

## What The Pipeline Did

Across the completed modules, the screening pattern was:

```text
public genome, protein, BGC, pathway, or metadata resources
-> candidate universe
-> annotation and source-context cleanup
-> false-positive removal
-> module-specific evidence scoring
-> dereplication, structure, phylogeny, or pathway hardening
-> safety/context review
-> candidate archives and wet-lab planning hypotheses
```

The exact evidence differed by plan. BGC candidates needed boundary and product-class logic. Enzyme candidates needed family, motif, structure, and assayability evidence. Nitrogen-cycle candidates needed marker specificity and pathway context. Plant-growth-promotion candidates needed genome-level trait coherence and reference support. Biomaterial candidates needed product-class or recovery plausibility rather than generic surface annotations.

## Evidence Standard

The central standard was simple: a candidate advanced only when the computational evidence supported a specific, testable hypothesis.

The outputs are therefore best read as pre-wet-lab hypotheses, not as validated biological products. A candidate could be strong enough to justify expert review while still lacking measured activity, expression, product identity, safety approval, or field performance.

The evidence levels used throughout the work were:

| Level | Meaning |
|---|---|
| 0 | Idea only; no sequence-backed candidate |
| 1 | Accession-backed sequence hit with basic metadata |
| 2 | Clustered homolog with domain annotation and taxonomy |
| 3 | Genomic-neighborhood, pathway, or source context supports the hypothesis |
| 4 | Structure, active-site, or marker-family evidence supports prioritization |
| 5 | Literature, database, or close-reference evidence supports a functional analog |
| 6 | In vitro, metabolomics, material, or organism-level validation |
| 7 | Replicated validation under intended deployment conditions |

Most candidates in this repository sit around computational Levels 3 to 5. Levels 6 and 7 require new wet-lab work.

## How Hits Were Removed

A major part of the project was deciding what not to keep. The screens intentionally removed or demoted:

- BGCs with unresolved boundary, contig-edge, or domain-logic problems.
- Generic enzyme annotations without enough family or active-site support.
- Nitrogen-cycle hits that looked like housekeeping, fragmentary, or confusable domains.
- Plant-growth-promotion hits where one trait keyword did not support an organism-level hypothesis.
- Biomaterial hits that were actually generic membrane, lipid-A/LPS, transporter, or surface biology.
- Candidates with unresolved safety-context flags or weak practical handoff paths.

These negative calls are part of the result. They make the surviving candidates more credible.

## What A Safety Pass Means

The repository uses computational safety-context triage. That means the screen looked for obvious local issues such as candidate-near AMR, mobilome, toxin, virulence, pathogen-adjacent taxonomy, or problematic source context where those artifacts were available.

A `PASS_WITH_CONTEXT_NOTE` does not mean a candidate is safe to express, synthesize, release, commercialize, or use. It means no obvious local computational blocker was detected in the checked artifacts. Institutional biosafety review, host choice, expression conditions, product hazards, organism handling, and environmental use remain outside this repository.

## Why The Markdown Files Exist

The top-level Markdown files are intentionally kept because they make the repository readable without opening the full report first:

- `README.md` gives the plain-language overview.
- `PROJECT_INDEX.md` maps the repository.
- `00_data_sources_and_dependencies.md` explains the data and reference backbone.
- This file explains the shared screening logic.
- `01_...` through `08_...` explain what happened in each completed module.
- `outputs/.../candidate_archives/` preserves candidate packet evidence.

The old workflow/runbook files were removed from the top level because they made the repo read like instructions rather than a completed research record.
