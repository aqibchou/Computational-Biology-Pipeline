# Plan 03 - Nitrogen-Cycle Candidate Archive

Generated: 2026-05-18

Nitrogen-fixation, N2O-reduction, urease/rhizosphere, and nitrate/nitrite transformation packets.

This archive preserves candidate-packet evidence for review. It is not a wet-lab protocol, synthesis instruction set, organism-release plan, or safety clearance.

Packet count: `6`

## Packet Index

| # | Packet | Source path |
|---:|---|---|
| 1 | Plan 03 Candidate Packet 1: `PLAN03:MGYG000517341:nitrogen_fixation:MGYG000517341_00816` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/01_MGYG000517341_nitrogen_fixation_MGYG000517341_00816.md` |
| 2 | Plan 03 Candidate Packet 2: `PLAN03:MGYG000478572:n2o_reduction:MGYG000478572_00459` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/02_MGYG000478572_n2o_reduction_MGYG000478572_00459.md` |
| 3 | Plan 03 Candidate Packet 3: `PLAN03:MGYG000473561:n2o_reduction:MGYG000473561_03510` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/03_MGYG000473561_n2o_reduction_MGYG000473561_03510.md` |
| 4 | Plan 03 Candidate Packet 4: `PLAN03:MGYG000511828:urea_rhizosphere:MGYG000511828_04091` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/04_MGYG000511828_urea_rhizosphere_MGYG000511828_04091.md` |
| 5 | Plan 03 Candidate Packet 5: `PLAN03:MGYG000517341:urea_rhizosphere:MGYG000517341_01850` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/05_MGYG000517341_urea_rhizosphere_MGYG000517341_01850.md` |
| 6 | Plan 03 Candidate Packet 6: `PLAN03:MGYG000511829:nitrate_nitrite_transformation:MGYG000511829_04732` | `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/06_MGYG000511829_nitrate_nitrite_transformation_MGYG000511829_04732.md` |

## Full Packet Text


---

## Packet 1: Plan 03 Candidate Packet 1: `PLAN03:MGYG000517341:nitrogen_fixation:MGYG000517341_00816`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/01_MGYG000517341_nitrogen_fixation_MGYG000517341_00816.md`

### Plan 03 Candidate Packet 1: `PLAN03:MGYG000517341:nitrogen_fixation:MGYG000517341_00816`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Nitrogen fixation
- Representative marker/protein: `nifH` / `MGYG000517341_00816`
- Plan03 score/status: 91.9 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000517341`; type `Isolate`; quality `HIGH_QUALITY`; completeness 100.0; contamination 0.21
- Source: saline / root:Host-associated:Plants:Rhizosphere / tomato-rhizosphere-v1-0
- Taxonomy: d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Pseudomonadaceae;g__Azotobacter;s__Azotobacter salinestris

#### Pathway Evidence

- Core markers present: `nifD_vnfD_alpha;nifH;nifK_vnfK_beta`
- Accessory markers present: `nifB;nif_vnf_accessory`
- Cluster core markers: `nifD_vnfD_alpha;nifH;nifK_vnfK_beta`
- Cluster accessory markers: `nifB;nif_vnf_accessory`
- Missing core markers: `none`
- Neighborhood: contig=MGYG000517341_4;span_bp=102066;markers=nifB,nifD_vnfD_alpha,nifH,nifK_vnfK_beta,nif_vnf_accessory

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `nif_vnf_accessory` | `MGYG000517341_00774` | sfnR_2 Sigma54-dependent transcriptional activator SfnR | `` | `PF00158` | MGYG000517341_4:19663-20604 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |
| `nifD_vnfD_alpha` | `MGYG000517341_00811` | vnfK Nitrogenase vanadium-iron protein beta chain | `ko:K02591` | `PF00148` | MGYG000517341_4:57385-58812 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |
| `nifK_vnfK_beta` | `MGYG000517341_00811` | vnfK Nitrogenase vanadium-iron protein beta chain | `ko:K02591` | `PF00148` | MGYG000517341_4:57385-58812 | `PASS_MARKER_SPECIFIC` |
| `nif_vnf_accessory` | `MGYG000517341_00812` | vnfG Nitrogenase vanadium-iron protein delta chain | `ko:K00531` | `PF03139` | MGYG000517341_4:58868-59209 | `PASS_MARKER_SPECIFIC` |
| `nifD_vnfD_alpha` | `MGYG000517341_00813` | vnfD Nitrogenase vanadium-iron protein alpha chain | `ko:K02586` | `PF00148` | MGYG000517341_4:59209-60633 | `PASS_MARKER_SPECIFIC` |
| `nifK_vnfK_beta` | `MGYG000517341_00813` | vnfD Nitrogenase vanadium-iron protein alpha chain | `ko:K02586` | `PF00148` | MGYG000517341_4:59209-60633 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |
| `nifH` | `MGYG000517341_00816` | nifH1_1 Nitrogenase iron protein 1 | `ko:K02588` | `PF00142` | MGYG000517341_4:63045-63917 | `PASS_MARKER_SPECIFIC` |
| `nif_vnf_accessory` | `MGYG000517341_00820` | hypothetical protein | `ko:K02596` | `` | MGYG000517341_4:66491-67033 | `PASS_MARKER_SPECIFIC` |
| `nifD_vnfD_alpha` | `MGYG000517341_00821` | nifK_1 Nitrogenase molybdenum-iron protein beta chain | `ko:K02592` | `PF00148` | MGYG000517341_4:67030-68412 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |
| `nifK_vnfK_beta` | `MGYG000517341_00821` | nifK_1 Nitrogenase molybdenum-iron protein beta chain | `ko:K02592` | `PF00148` | MGYG000517341_4:67030-68412 | `PASS_MARKER_SPECIFIC` |
| `nifD_vnfD_alpha` | `MGYG000517341_00822` | nifD_1 Nitrogenase molybdenum-iron protein alpha chain | `ko:K02587` | `PF00148` | MGYG000517341_4:68414-69823 | `PASS_MARKER_SPECIFIC` |
| `nifK_vnfK_beta` | `MGYG000517341_00822` | nifD_1 Nitrogenase molybdenum-iron protein alpha chain | `ko:K02587` | `PF00148` | MGYG000517341_4:68414-69823 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |
| `nif_vnf_accessory` | `MGYG000517341_00823` | vnfA_1 Nitrogen fixation protein VnfA | `ko:K02584` | `PF00158` | MGYG000517341_4:70071-71639 | `PASS_MARKER_SPECIFIC` |
| `nif_vnf_accessory` | `MGYG000517341_00826` | vnfA_2 Nitrogen fixation protein VnfA | `ko:K02584` | `PF00158` | MGYG000517341_4:73467-75029 | `PASS_MARKER_SPECIFIC` |
| `nifB` | `MGYG000517341_00878` | moaA_1 GTP 3',8-cyclase | `ko:K03639` | `PF04055,PF06463` | MGYG000517341_4:120734-121729 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: none_detected
- Recovery/culture path: `CULTURED_CLOSE_RELATIVE_AND_MGNIFY_ISOLATE`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate marker/pathway identity first; nitrogenase activity testing requires appropriate collaborators and controlled conditions. This does not imply agronomic nitrogen fixation.

#### Strongest Safe Claim

Computationally prioritized nitrogenase-cluster hypothesis with marker, neighborhood, source, and safety-context support.

#### Remaining Experimental Gaps

Does not prove nitrogen fixation activity, plant benefit, fertilizer replacement, or environmental safety.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.


---

## Packet 2: Plan 03 Candidate Packet 2: `PLAN03:MGYG000478572:n2o_reduction:MGYG000478572_00459`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/02_MGYG000478572_n2o_reduction_MGYG000478572_00459.md`

### Plan 03 Candidate Packet 2: `PLAN03:MGYG000478572:n2o_reduction:MGYG000478572_00459`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Nitrous oxide reduction / denitrification completion
- Representative marker/protein: `nosZ` / `MGYG000478572_00459`
- Plan03 score/status: 91.61 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000478572`; type `MAG`; quality `HIGH_QUALITY`; completeness 99.57; contamination 0.02
- Source: saline / root:Environmental:Aquatic:Marine / marine-v2-0
- Taxonomy: d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Oleiphilaceae;g__Marinobacter;s__Marinobacter salinexigens

#### Pathway Evidence

- Core markers present: `nosZ`
- Accessory markers present: `nosD;nosF;nosR_L_context;nosY`
- Cluster core markers: `nosZ`
- Cluster accessory markers: `nosD;nosF;nosR_L_context;nosY`
- Missing core markers: `none`
- Neighborhood: contig=MGYG000478572_1;span_bp=7954;markers=nosD,nosF,nosR_L_context,nosY,nosZ

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `nosR_L_context` | `MGYG000478572_00458` | hypothetical protein | `ko:K19339` | `PF12801` | MGYG000478572_1:476003-478156 | `PASS_MARKER_SPECIFIC` |
| `nosZ` | `MGYG000478572_00459` | nosZ Nitrous-oxide reductase | `ko:K00376` | `PF18793,PF18764` | MGYG000478572_1:478218-480113 | `PASS_MARKER_SPECIFIC` |
| `nosD` | `MGYG000478572_00460` | nosD putative ABC transporter binding protein NosD | `ko:K07218` | `PF05048` | MGYG000478572_1:480337-481602 | `PASS_MARKER_SPECIFIC` |
| `nosF` | `MGYG000478572_00461` | nosF putative ABC transporter ATP-binding protein NosF | `ko:K19340` | `PF00005` | MGYG000478572_1:481602-482534 | `PASS_MARKER_SPECIFIC` |
| `nosY` | `MGYG000478572_00462` | nosY putative ABC transporter permease protein NosY | `ko:K19341` | `PF12679` | MGYG000478572_1:482531-483361 | `PASS_MARKER_SPECIFIC` |
| `nosR_L_context` | `MGYG000478572_00463` | hypothetical protein | `ko:K19342` | `PF05573` | MGYG000478572_1:483376-483957 | `PASS_MARKER_SPECIFIC` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: none_detected
- Recovery/culture path: `MAG_OR_UNCONFIRMED_RECOVERY_ROUTE`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate nosZ/accessory context, then consider controlled microcosm/headspace N2O transformation assays. This does not imply soil or field emissions reduction.

#### Strongest Safe Claim

Computationally prioritized nitrous-oxide-reduction pathway hypothesis with nosZ/accessory context and source/safety support.

#### Remaining Experimental Gaps

Does not prove N2O reduction activity, emissions reduction, soil performance, or environmental safety.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.


---

## Packet 3: Plan 03 Candidate Packet 3: `PLAN03:MGYG000473561:n2o_reduction:MGYG000473561_03510`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/03_MGYG000473561_n2o_reduction_MGYG000473561_03510.md`

### Plan 03 Candidate Packet 3: `PLAN03:MGYG000473561:n2o_reduction:MGYG000473561_03510`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Nitrous oxide reduction / denitrification completion
- Representative marker/protein: `nosZ` / `MGYG000473561_03510`
- Plan03 score/status: 91.25 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000473561`; type `MAG`; quality `HIGH_QUALITY`; completeness 100.0; contamination 0.3
- Source: hydrothermal / root:Environmental:Aquatic:Marine / marine-v2-0
- Taxonomy: d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Flavobacteriales;f__Flavobacteriaceae;g__Maribacter;s__Maribacter hydrothermalis

#### Pathway Evidence

- Core markers present: `nosZ`
- Accessory markers present: `nosD;nosF;nosR_L_context;nosY`
- Cluster core markers: `nosZ`
- Cluster accessory markers: `nosD;nosF;nosR_L_context;nosY`
- Missing core markers: `none`
- Neighborhood: contig=MGYG000473561_50;span_bp=16046;markers=nosD,nosF,nosR_L_context,nosY,nosZ

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `nosZ` | `MGYG000473561_03510` | nosZ Nitrous-oxide reductase | `ko:K00376` | `PF18764` | MGYG000473561_50:166347-168308 | `PASS_MARKER_SPECIFIC` |
| `nosR_L_context` | `MGYG000473561_03511` | hypothetical protein | `ko:K19342` | `` | MGYG000473561_50:168430-169047 | `PASS_MARKER_SPECIFIC` |
| `nosR_L_context` | `MGYG000473561_03512` | hypothetical protein | `ko:K19342` | `PF05573` | MGYG000473561_50:169070-169501 | `PASS_MARKER_SPECIFIC` |
| `nosD` | `MGYG000473561_03513` | nosD putative ABC transporter binding protein NosD | `ko:K07218` | `PF05048` | MGYG000473561_50:169601-170836 | `PASS_MARKER_SPECIFIC` |
| `nosF` | `MGYG000473561_03514` | tcyN L-cystine import ATP-binding protein TcyN | `ko:K19340` | `PF00005` | MGYG000473561_50:170836-171546 | `PASS_MARKER_SPECIFIC` |
| `nosY` | `MGYG000473561_03515` | hypothetical protein | `ko:K19341` | `` | MGYG000473561_50:171539-172321 | `PASS_MARKER_SPECIFIC` |
| `nosR_L_context` | `MGYG000473561_03525` | hypothetical protein | `` | `PF12801,PF11614,PF13746` | MGYG000473561_50:180975-182393 | `PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: genome_amr_rows=1
- Recovery/culture path: `MAG_OR_UNCONFIRMED_RECOVERY_ROUTE`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate nosZ/accessory context, then consider controlled microcosm/headspace N2O transformation assays. This does not imply soil or field emissions reduction.

#### Strongest Safe Claim

Computationally prioritized nitrous-oxide-reduction pathway hypothesis with nosZ/accessory context and source/safety support.

#### Remaining Experimental Gaps

Does not prove N2O reduction activity, emissions reduction, soil performance, or environmental safety.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.


---

## Packet 4: Plan 03 Candidate Packet 4: `PLAN03:MGYG000511828:urea_rhizosphere:MGYG000511828_04091`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/04_MGYG000511828_urea_rhizosphere_MGYG000511828_04091.md`

### Plan 03 Candidate Packet 4: `PLAN03:MGYG000511828:urea_rhizosphere:MGYG000511828_04091`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Urea metabolism and rhizosphere nitrogen availability
- Representative marker/protein: `ureC_alpha` / `MGYG000511828_04091`
- Plan03 score/status: 87.7 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000511828`; type `MAG`; quality `MODERATE_QUALITY`; completeness 85.87; contamination 3.39
- Source: soil / root:Environmental:Terrestrial:Soil / soil-v1-0
- Taxonomy: d__Bacteria;p__Methylomirabilota;c__Methylomirabilia;o__Rokubacteriales;f__CSP1-6;g__AR5;s__

#### Pathway Evidence

- Core markers present: `ureA_gamma;ureB_beta;ureC_alpha`
- Accessory markers present: `ureD_E_F_G_accessory;urea_or_ammonium_transport`
- Cluster core markers: `ureA_gamma;ureB_beta;ureC_alpha`
- Cluster accessory markers: `ureD_E_F_G_accessory`
- Missing core markers: `none`
- Neighborhood: contig=MGYG000511828_601;span_bp=4686;markers=ureA_gamma,ureB_beta,ureC_alpha,ureD_E_F_G_accessory

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `ureA_gamma` | `MGYG000511828_04088` | ureA Urease subunit gamma | `ko:K01430` | `PF00547` | MGYG000511828_601:179-481 | `PASS_MARKER_SPECIFIC` |
| `ureB_beta` | `MGYG000511828_04090` | ureB Urease subunit beta | `ko:K01429,ko:K14048` | `PF00699` | MGYG000511828_601:1025-1372 | `PASS_MARKER_SPECIFIC` |
| `ureC_alpha` | `MGYG000511828_04091` | ureC Urease subunit alpha | `ko:K01428` | `PF00449,PF01979` | MGYG000511828_601:1369-3087 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000511828_04092` | ureE Urease accessory protein UreE | `ko:K03187` | `` | MGYG000511828_601:3192-3563 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000511828_04093` | ureF Urease accessory protein UreF | `ko:K03188` | `PF01730` | MGYG000511828_601:3556-4242 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000511828_04094` | ureG Urease accessory protein UreG | `ko:K03189,ko:K04652` | `PF02492` | MGYG000511828_601:4239-4865 | `PASS_MARKER_SPECIFIC` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: stress_resistance_rows=1
- Recovery/culture path: `NO_CULTURED_CLOSE_RELATIVE_CONFIRMED`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate urease operon identity and urease activity under controlled conditions. This does not imply fertilizer-efficiency or plant-growth benefit.

#### Strongest Safe Claim

Computationally prioritized urease/rhizosphere nitrogen-availability pathway hypothesis with urease operon support.

#### Remaining Experimental Gaps

Does not prove urease activity, fertilizer efficiency, plant-growth benefit, or inoculant safety.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.


---

## Packet 5: Plan 03 Candidate Packet 5: `PLAN03:MGYG000517341:urea_rhizosphere:MGYG000517341_01850`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/05_MGYG000517341_urea_rhizosphere_MGYG000517341_01850.md`

### Plan 03 Candidate Packet 5: `PLAN03:MGYG000517341:urea_rhizosphere:MGYG000517341_01850`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Urea metabolism and rhizosphere nitrogen availability
- Representative marker/protein: `ureC_alpha` / `MGYG000517341_01850`
- Plan03 score/status: 86.42 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000517341`; type `Isolate`; quality `HIGH_QUALITY`; completeness 100.0; contamination 0.21
- Source: saline / root:Host-associated:Plants:Rhizosphere / tomato-rhizosphere-v1-0
- Taxonomy: d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Pseudomonadaceae;g__Azotobacter;s__Azotobacter salinestris

#### Pathway Evidence

- Core markers present: `ureA_gamma;ureB_beta;ureC_alpha`
- Accessory markers present: `ureD_E_F_G_accessory;urea_or_ammonium_transport`
- Cluster core markers: `ureA_gamma;ureB_beta;ureC_alpha`
- Cluster accessory markers: `ureD_E_F_G_accessory`
- Missing core markers: `none`
- Neighborhood: contig=MGYG000517341_9;span_bp=8255;markers=ureA_gamma,ureB_beta,ureC_alpha,ureD_E_F_G_accessory

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `ureD_E_F_G_accessory` | `MGYG000517341_01843` | ureG_2 Urease accessory protein UreG | `ko:K03189` | `PF02492` | MGYG000517341_9:81401-82015 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000517341_01844` | ureF Urease accessory protein UreF | `ko:K03188` | `PF01730` | MGYG000517341_9:82031-82705 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000517341_01845` | ureE Urease accessory protein UreE | `ko:K03187` | `PF02814,PF05194` | MGYG000517341_9:82702-83202 | `PASS_MARKER_SPECIFIC` |
| `ureC_alpha` | `MGYG000517341_01850` | ureC Urease subunit alpha | `ko:K01428` | `PF00449,PF01979` | MGYG000517341_9:86403-88103 | `PASS_MARKER_SPECIFIC` |
| `ureB_beta` | `MGYG000517341_01851` | ureB Urease subunit beta | `ko:K01429` | `PF00699` | MGYG000517341_9:88198-88503 | `PASS_MARKER_SPECIFIC` |
| `ureA_gamma` | `MGYG000517341_01852` | ureA Urease subunit gamma | `ko:K01430` | `PF00547` | MGYG000517341_9:88514-88816 | `PASS_MARKER_SPECIFIC` |
| `ureD_E_F_G_accessory` | `MGYG000517341_01853` | ureD Urease accessory protein UreD | `ko:K03190` | `PF01774` | MGYG000517341_9:88817-89656 | `PASS_MARKER_SPECIFIC` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: none_detected
- Recovery/culture path: `CULTURED_CLOSE_RELATIVE_AND_MGNIFY_ISOLATE`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate urease operon identity and urease activity under controlled conditions. This does not imply fertilizer-efficiency or plant-growth benefit.

#### Strongest Safe Claim

Computationally prioritized urease/rhizosphere nitrogen-availability pathway hypothesis with urease operon support.

#### Remaining Experimental Gaps

Does not prove urease activity, fertilizer efficiency, plant-growth benefit, or inoculant safety.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.


---

## Packet 6: Plan 03 Candidate Packet 6: `PLAN03:MGYG000511829:nitrate_nitrite_transformation:MGYG000511829_04732`

Source: `outputs/plan03_pre_wetlab_screen_2026-05-18/plan03_top_candidate_packets/06_MGYG000511829_nitrate_nitrite_transformation_MGYG000511829_04732.md`

### Plan 03 Candidate Packet 6: `PLAN03:MGYG000511829:nitrate_nitrite_transformation:MGYG000511829_04732`

- Packet role: `IMMEDIATE_PRE_WETLAB_PACKET`
- Track: Nitrate/nitrite transformation
- Representative marker/protein: `narG_napA_nitrate_reductase` / `MGYG000511829_04732`
- Plan03 score/status: 80.72 / `ADVANCE_TO_PRE_WETLAB_PACKET`
- Genome: `MGYG000511829`; type `MAG`; quality `MODERATE_QUALITY`; completeness 81.54; contamination 4.68
- Source: soil / root:Environmental:Terrestrial:Soil / soil-v1-0
- Taxonomy: d__Bacteria;p__Actinomycetota;c__CALGFH01;o__CALGFH01;f__CALGFH01;g__DASVXQ01;s__

#### Pathway Evidence

- Core markers present: `narG_napA_nitrate_reductase;nirS_nirK_or_assimilatory_nitrite`
- Accessory markers present: `narH_napB_nitrate_reductase;narJ_I_context`
- Cluster core markers: `narG_napA_nitrate_reductase;nirS_nirK_or_assimilatory_nitrite`
- Cluster accessory markers: `narH_napB_nitrate_reductase;narJ_I_context`
- Missing core markers: `nrfA`
- Neighborhood: contig=MGYG000511829_676;span_bp=8485;markers=narG_napA_nitrate_reductase,narH_napB_nitrate_reductase,narJ_I_context,nirS_nirK_or_assimilatory_nitrite

| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |
|---|---|---|---|---|---|---|
| `nirS_nirK_or_assimilatory_nitrite` | `MGYG000511829_04727` | hypothetical protein | `ko:K00368` | `` | MGYG000511829_676:2021-3220 | `PASS_MARKER_SPECIFIC` |
| `narJ_I_context` | `MGYG000511829_04730` | hypothetical protein | `ko:K00373` | `PF02613` | MGYG000511829_676:5070-5696 | `PASS_MARKER_SPECIFIC` |
| `narH_napB_nitrate_reductase` | `MGYG000511829_04731` | narY Respiratory nitrate reductase 2 beta chain | `ko:K00371` | `PF13247,PF14711` | MGYG000511829_676:5693-7363 | `PASS_MARKER_SPECIFIC` |
| `narG_napA_nitrate_reductase` | `MGYG000511829_04732` | napA Periplasmic nitrate reductase | `ko:K00370` | `PF00384,PF01568` | MGYG000511829_676:7363-10506 | `PASS_MARKER_SPECIFIC` |

#### Safety And Practicality

- Safety call: `PASS_WITH_CONTEXT_NOTE`; flags: genome_amr_rows=4
- Recovery/culture path: `MAG_OR_UNCONFIRMED_RECOVERY_ROUTE`
- Candidate-near AMR rows: 0 (none_detected)
- Candidate-near mobile rows: 0 (none_detected)

#### Assay Direction

Validate marker identity and test nitrogen-species transformation only with appropriate controls. This does not imply ecosystem nitrogen retention.

#### Strongest Safe Claim

Computationally prioritized nitrate/nitrite transformation pathway hypothesis with marker and neighborhood support.

#### Remaining Experimental Gaps

Does not prove nitrogen flux, DNRA/denitrification rate, ecosystem nitrogen retention, or field performance.
No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.
