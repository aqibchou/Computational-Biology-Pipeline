# Plan 04 - Plant-Growth-Promotion Genome Candidate Archive

Generated: 2026-05-18

Genome-level PGP wet-lab planning packets with trait, source, reference, and safety-context evidence.

This archive preserves candidate-packet evidence for review. It is not a wet-lab protocol, synthesis instruction set, organism-release plan, or safety clearance.

Packet count: `4`

## Packet Index

| # | Packet | Source path |
|---:|---|---|
| 1 | Plan 04 Wet-Lab Planning Candidate 01 | `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/01_MGYG000517341_osmoprotection_stress.md` |
| 2 | Plan 04 Wet-Lab Planning Candidate 02 | `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/02_MGYG000511828_phosphate_solubilization.md` |
| 3 | Plan 04 Wet-Lab Planning Candidate 03 | `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/03_MGYG000535629_siderophore_production.md` |
| 4 | Plan 04 Wet-Lab Planning Candidate 04 | `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/04_MGYG000535630_antifungal_bgc.md` |

## Full Packet Text


---

## Packet 1: Plan 04 Wet-Lab Planning Candidate 01

Source: `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/01_MGYG000517341_osmoprotection_stress.md`

### Plan 04 Wet-Lab Planning Candidate 01

Candidate: `plan04:MGYG000517341:pgp_genome`
Genome: `MGYG000517341`
Primary hypothesis: osmoprotection/drought-salinity stress candidate from tomato rhizosphere/stress context; test stress-growth and seedling support as hypotheses.
Bridge score: `95.224`

#### Source

- Catalogue: `tomato-rhizosphere-v1-0`
- Biome: `root:Host-associated:Plants:Rhizosphere`
- Query/source label: `saline` / `saline`
- Host/crop/source: `tomato`
- Metadata strength: `DIRECT_PLANT_STRESS_CONTEXT`
- ENA sample/study: `SAMN41552033` / `SRP510093`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Pseudomonadaceae;g__Azotobacter;s__Azotobacter salinestris`
- Completeness/contamination: `100.0` / `0.21`
- Genome quality call: `HIGH_QUALITY`

#### Supported Traits

- Supported traits: `antifungal_bgc;biofilm_colonization;iaa_support;nitrogen_availability;osmoprotection_stress;phosphate_solubilization;siderophore_production`
- Trait strengths: `{"antifungal_bgc": "STRONG", "biofilm_colonization": "STRONG", "iaa_support": "STRONG", "nitrogen_availability": "STRONG", "osmoprotection_stress": "STRONG", "phosphate_solubilization": "STRONG", "siderophore_production": "STRONG"}`
- Weak or absent traits: `ACC deaminase`
- BGC products: `NAGGN;NI-siderophore;NRP;NRP,Polyketide;NRPS;NRPS,NRP-metallophore,T1PKS;NRPS-like;Polyketide;RiPP-like;Terpene;Unknown;betalactone;hglE-KS,T3PKS;redox-cofactor;terpene`

#### Driver Proteins

| Protein | Trait | Strength | Rule evidence | Top Swiss-Prot hit | Novelty |
|---|---|---|---|---|---|
| `MGYG000517341_04109` | antifungal or BGC support | strong | antifungal enzyme/metabolite support | `Q8Z289` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000517341_00457` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000517341_00458` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000517341_00012` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000517341_00932` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000517341_01977` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000517341_03057` | indole acetic acid support | strong | IAA-specific annotation | `C1DLQ1` | LOW_NOVELTY_CLOSE_SWISSPROT |
| `MGYG000517341_00049` | nitrogen availability | strong | nitrogenase/nif marker support | `n/a` | not_checked |
| `MGYG000517341_00260` | nitrogen availability | strong | nitrogenase/nif marker support | `n/a` | not_checked |
| `MGYG000517341_00439` | nitrogen availability | strong | nitrogenase/nif marker support | `n/a` | not_checked |
| `MGYG000517341_03956` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `A0A4D6G3C8` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000517341_03975` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `M1VMF7` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000517341_00013` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000517341_02262` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `P55174` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000517341_02263` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |
| `MGYG000517341_02264` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |
| `MGYG000517341_00481` | siderophore production | strong | siderophore gene/receptor/transport support | `n/a` | not_checked |
| `MGYG000517341_01836` | siderophore production | strong | siderophore BGC support | `n/a` | not_checked |
| `MGYG000517341_01838` | siderophore production | strong | siderophore BGC support | `n/a` | not_checked |

#### Safety And Feasibility

- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMRFinder rows: `0`
- Candidate AMR driver hits: `none`
- Mobilome feature count: `79764`
- Toxin/virulence/pathogen terms: `none` / `none` / `none`
- Feasibility score: `100.0`

#### Handoff

- First assay: growth assay under salt/osmotic/desiccation-relevant stress.
- Remaining caveat: safety context requires institutional review before culturing; plant-growth benefit remains unvalidated until controlled assays

#### Boundary

This is a pre-wet-lab planning packet. It does not validate plant-growth promotion, pathogen suppression, drought tolerance, salinity tolerance, greenhouse performance, field performance, or crop-yield benefit.


---

## Packet 2: Plan 04 Wet-Lab Planning Candidate 02

Source: `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/02_MGYG000511828_phosphate_solubilization.md`

### Plan 04 Wet-Lab Planning Candidate 02

Candidate: `plan04:MGYG000511828:pgp_genome`
Genome: `MGYG000511828`
Primary hypothesis: phosphate solubilization candidate from unknown source; test nutrient-availability phenotype before plant-benefit claims.
Bridge score: `77.083`

#### Source

- Catalogue: `soil-v1-0`
- Biome: `root:Environmental:Terrestrial:Soil`
- Query/source label: `soil` / `soil`
- Host/crop/source: `unknown`
- Metadata strength: `INDIRECT_SOIL_CONTEXT`
- ENA sample/study: `SAMN44605170` / `SRP385305`
- Taxonomy: `d__Bacteria;p__Methylomirabilota;c__Methylomirabilia;o__Rokubacteriales;f__CSP1-6;g__AR5;s__`
- Completeness/contamination: `85.87` / `3.39`
- Genome quality call: `GOOD_QUALITY`

#### Supported Traits

- Supported traits: `antifungal_bgc;biofilm_colonization;iaa_support;nitrogen_availability;osmoprotection_stress;phosphate_solubilization`
- Trait strengths: `{"antifungal_bgc": "STRONG", "biofilm_colonization": "STRONG", "iaa_support": "STRONG", "nitrogen_availability": "MODERATE", "osmoprotection_stress": "STRONG", "phosphate_solubilization": "STRONG"}`
- Weak or absent traits: `siderophore production;ACC deaminase`
- BGC products: `NRP;NRPS;NRPS-like;Polyketide;RiPP-like;Unknown;phosphonate;redox-cofactor;terpene`

#### Driver Proteins

| Protein | Trait | Strength | Rule evidence | Top Swiss-Prot hit | Novelty |
|---|---|---|---|---|---|
| `MGYG000511828_03229` | antifungal or BGC support | strong | antifungal enzyme/metabolite support | `P58293` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_00286` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000511828_00287` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000511828_00308` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000511828_02610` | biofilm/root colonization | strong | biofilm/root-colonization support | `P55702` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_02612` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000511828_00719` | indole acetic acid support | strong | IAA-specific annotation | `Q3A503` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_04216` | indole acetic acid support | strong | IAA-specific annotation | `n/a` | not_checked |
| `MGYG000511828_01984` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `n/a` | not_checked |
| `MGYG000511828_02992` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `Q72E85` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_04088` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `n/a` | not_checked |
| `MGYG000511828_00129` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000511828_00130` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000511828_00574` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000511828_05000` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `A4VL90` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_05001` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `A5FUM6` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000511828_05002` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |

#### Safety And Feasibility

- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMRFinder rows: `1`
- Candidate AMR driver hits: `none`
- Mobilome feature count: `90340`
- Toxin/virulence/pathogen terms: `none` / `neighborhood:virulence` / `none`
- Feasibility score: `94.122`

#### Handoff

- First assay: phosphate-solubilization plate or liquid assay with insoluble phosphate source.
- Remaining caveat: soil context is indirect rather than crop/rhizosphere-specific; safety context requires institutional review before culturing; plant-growth benefit remains unvalidated until controlled assays

#### Boundary

This is a pre-wet-lab planning packet. It does not validate plant-growth promotion, pathogen suppression, drought tolerance, salinity tolerance, greenhouse performance, field performance, or crop-yield benefit.


---

## Packet 3: Plan 04 Wet-Lab Planning Candidate 03

Source: `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/03_MGYG000535629_siderophore_production.md`

### Plan 04 Wet-Lab Planning Candidate 03

Candidate: `plan04:MGYG000535629:pgp_genome`
Genome: `MGYG000535629`
Primary hypothesis: siderophore production candidate from barley source; test siderophore/antagonism activity with safe controls.
Bridge score: `85.229`

#### Source

- Catalogue: `barley-rhizosphere-v2-0`
- Biome: `root:Host-associated:Plants:Rhizosphere`
- Query/source label: `rhizosphere` / `rhizosphere`
- Host/crop/source: `barley`
- Metadata strength: `DIRECT_PLANT_CONTEXT`
- ENA sample/study: `SAMEA119169879` / `ERP178658`
- Taxonomy: `d__Bacteria;p__Bdellovibrionota;c__Bacteriovoracia;o__Bacteriovoracales;f__Bacteriovoracaceae;g__Bacteriovorax;s__`
- Completeness/contamination: `82.08` / `4.12`
- Genome quality call: `GOOD_QUALITY`

#### Supported Traits

- Supported traits: `antifungal_bgc;biofilm_colonization;iaa_support;osmoprotection_stress;phosphate_solubilization;siderophore_production`
- Trait strengths: `{"antifungal_bgc": "MODERATE", "biofilm_colonization": "STRONG", "iaa_support": "STRONG", "osmoprotection_stress": "STRONG", "phosphate_solubilization": "STRONG", "siderophore_production": "STRONG"}`
- Weak or absent traits: `nitrogen availability;ACC deaminase`
- BGC products: `NI-siderophore;RiPP-like;Unknown;phosphonate;ranthipeptide`

#### Driver Proteins

| Protein | Trait | Strength | Rule evidence | Top Swiss-Prot hit | Novelty |
|---|---|---|---|---|---|
| `MGYG000535629_00136` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000535629_00137` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `Q47318` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_00138` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000535629_02011` | biofilm/root colonization | strong | biofilm/root-colonization support | `Q9I3S1` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_02012` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000535629_00044` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000535629_01867` | indole acetic acid support | strong | IAA-specific annotation | `Q2LUR0` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_03529` | indole acetic acid support | strong | IAA-specific annotation | `n/a` | not_checked |
| `MGYG000535629_03057` | indole acetic acid support | moderate | tryptophan-dependent IAA pathway support | `n/a` | not_checked |
| `MGYG000535629_00160` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000535629_00292` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000535629_00523` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `P41751` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_00053` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `Q73MU2` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_01359` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |
| `MGYG000535629_00983` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |
| `MGYG000535629_00137` | siderophore production | strong | siderophore BGC support | `Q47318` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_00138` | siderophore production | strong | siderophore BGC support | `Q9UUE3` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535629_00139` | siderophore production | strong | siderophore BGC support | `Q76BS7` | HIGH_SEQUENCE_NOVELTY |

#### Safety And Feasibility

- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMRFinder rows: `0`
- Candidate AMR driver hits: `none`
- Mobilome feature count: `63493`
- Toxin/virulence/pathogen terms: `none` / `none` / `none`
- Feasibility score: `91.518`

#### Handoff

- First assay: CAS siderophore assay with non-pathogenic culture controls.
- Remaining caveat: safety context requires institutional review before culturing; plant-growth benefit remains unvalidated until controlled assays

#### Boundary

This is a pre-wet-lab planning packet. It does not validate plant-growth promotion, pathogen suppression, drought tolerance, salinity tolerance, greenhouse performance, field performance, or crop-yield benefit.


---

## Packet 4: Plan 04 Wet-Lab Planning Candidate 04

Source: `outputs/plan04_pgp_bridge_2026-05-17/wetlab_candidate_packets/04_MGYG000535630_antifungal_bgc.md`

### Plan 04 Wet-Lab Planning Candidate 04

Candidate: `plan04:MGYG000535630:pgp_genome`
Genome: `MGYG000535630`
Primary hypothesis: antifungal or BGC support candidate from barley source; test siderophore/antagonism activity with safe controls.
Bridge score: `87.001`

#### Source

- Catalogue: `barley-rhizosphere-v2-0`
- Biome: `root:Host-associated:Plants:Rhizosphere`
- Query/source label: `rhizosphere` / `rhizosphere`
- Host/crop/source: `barley`
- Metadata strength: `DIRECT_PLANT_CONTEXT`
- ENA sample/study: `SAMEA119169862` / `ERP178658`
- Taxonomy: `d__Bacteria;p__Actinomycetota;c__Actinomycetes;o__S36-B12;f__S36-B12;g__UBA11398;s__`
- Completeness/contamination: `84.01` / `2.22`
- Genome quality call: `GOOD_QUALITY`

#### Supported Traits

- Supported traits: `antifungal_bgc;biofilm_colonization;iaa_support;nitrogen_availability;osmoprotection_stress;phosphate_solubilization`
- Trait strengths: `{"antifungal_bgc": "MODERATE", "biofilm_colonization": "STRONG", "iaa_support": "STRONG", "nitrogen_availability": "MODERATE", "osmoprotection_stress": "STRONG", "phosphate_solubilization": "STRONG"}`
- Weak or absent traits: `siderophore production;ACC deaminase`
- BGC products: `Polyketide;T3PKS;Terpene;terpene`

#### Driver Proteins

| Protein | Trait | Strength | Rule evidence | Top Swiss-Prot hit | Novelty |
|---|---|---|---|---|---|
| `MGYG000535630_01824` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `n/a` | not_checked |
| `MGYG000535630_01825` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `O53507` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535630_01826` | antifungal or BGC support | moderate | BGC product-class support requiring domain review | `P54981` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000535630_01578` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | NO_REVIEWED_HOMOLOG_FOUND |
| `MGYG000535630_00213` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000535630_00577` | biofilm/root colonization | strong | biofilm/root-colonization support | `n/a` | not_checked |
| `MGYG000535630_01108` | indole acetic acid support | strong | IAA-specific annotation | `Q47RR4` | MEDIUM_HIGH_SEQUENCE_NOVELTY |
| `MGYG000535630_01717` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `n/a` | not_checked |
| `MGYG000535630_01718` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `n/a` | not_checked |
| `MGYG000535630_01719` | nitrogen availability | moderate | nitrogen availability pathway enzyme support | `n/a` | not_checked |
| `MGYG000535630_00064` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000535630_00067` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `Q9HLE2` | HIGH_SEQUENCE_NOVELTY |
| `MGYG000535630_00517` | osmoprotection/drought-salinity stress | strong | compatible-solute/osmoprotection support | `n/a` | not_checked |
| `MGYG000535630_01133` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | NO_REVIEWED_HOMOLOG_FOUND |
| `MGYG000535630_01244` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |
| `MGYG000535630_01482` | phosphate solubilization | strong | phosphate-specific enzyme/pathway term | `n/a` | not_checked |

#### Safety And Feasibility

- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMRFinder rows: `0`
- Candidate AMR driver hits: `none`
- Mobilome feature count: `35520`
- Toxin/virulence/pathogen terms: `none` / `neighborhood:pathogenicity island;neighborhood:virulence` / `none`
- Feasibility score: `95.518`

#### Handoff

- First assay: safe in vitro antagonism assay against approved non-risk plant fungal model.
- Remaining caveat: safety context requires institutional review before culturing; BGC support requires manual product-class/domain review; plant-growth benefit remains unvalidated until controlled assays

#### Boundary

This is a pre-wet-lab planning packet. It does not validate plant-growth promotion, pathogen suppression, drought tolerance, salinity tolerance, greenhouse performance, field performance, or crop-yield benefit.
