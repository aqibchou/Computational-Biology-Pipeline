# Plan 06 - Rare-Chemistry Candidate Archive

Generated: 2026-05-18

Rare-chemistry enzyme packets for redox, organosulfur, rare-sugar, and dehalogenation hypotheses.

This archive preserves candidate-packet evidence for review. It is not a wet-lab protocol, synthesis instruction set, organism-release plan, or safety clearance.

Packet count: `4`

## Packet Index

| # | Packet | Source path |
|---:|---|---|
| 1 | Plan 07 Wet-Lab Candidate Packet 01 | `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/01_MGYG000478572_02342_redox.md` |
| 2 | Plan 07 Wet-Lab Candidate Packet 02 | `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/02_MGYG000521810_01693_organosulfur.md` |
| 3 | Plan 07 Wet-Lab Candidate Packet 03 | `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/03_MGYG000478572_01361_rare_sugar.md` |
| 4 | Plan 07 Wet-Lab Candidate Packet 04 | `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/04_MGYG000517233_02445_dehalogenation.md` |

## Full Packet Text


---

## Packet 1: Plan 07 Wet-Lab Candidate Packet 01

Source: `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/01_MGYG000478572_02342_redox.md`

### Plan 07 Wet-Lab Candidate Packet 01

Candidate: `07:MGYG000478572:MGYG000478572_02342:redox`
Protein: `MGYG000478572_02342`
Rare chemistry class: `redox`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_RARE_CHEMISTRY`
Bridge score: `111.268`

#### Source Context

- Genome: `MGYG000478572`
- Biome/catalogue: `root:Environmental:Aquatic:Marine` / `marine-v2-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Oleiphilaceae;g__Marinobacter;s__Marinobacter salinexigens`
- Completeness/contamination: `99.57` / `0.02`
- Source/extreme label: `saline` / `salt`

#### Novelty and Reaction Evidence

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `Q64FW2` `All-trans-retinol 13,14-reductase OS=Mus musculus OX=10090 GN=Retsat PE=1 SV=3`
- Top hit identity/query coverage: `40.755` / `93.0`
- Reciprocal call: `reciprocal_best_returns_candidate`; reciprocal best candidate `07:MGYG000478572:MGYG000478572_02342:redox`
- Mapped ECs: `1.3.99.23`
- Rhea IDs: `RHEA:19193`
- Rhea terms: ``
- BRENDA titles: `Information on EC 1.3.99.23 - all-trans-retinol 13,14-reductase - BRENDA Enzyme Database`

#### MSA, Active-Site, and Structure

- MSA: `ok`; sequences `9`
- Active-site/residue call: `SUPPORTED_ACTIVE_SITE_AND_REACTION_CONTEXT`
- Candidate residue markers: `flavin_or_fad_annotation`
- Same-class Swiss-Prot hits in top 10: `6`
- AFDB proxy status: `available`; mean pLDDT `94.815`
- Proxy loop note: `low_loop_risk`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (high_partner_or_cofactor)
- Cofactor risk: `high_partner_or_cofactor`
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a rare-chemistry hypothesis candidate. Wet-lab testing should first establish soluble expression and wild-type activity against a safe, focused substrate panel. Product identity must be confirmed analytically before any new-reaction or new-specificity claim.

#### Sequence

```fasta
>MGYG000478572_02342 redox
MVVTNSSSGKLKPSSIRIGTRYRANRLNGPYDAIVIGSGIGGLTTAACLSKAGKKVLVLEQHYTAGGYTHSYARNGYEWD
VGVHYIGDMGSPHTLGRRLFDYITDGKLEWAPMDENYDRFFLGDKVVNLRAGKEGLRISLLNSFPEEQEAIDRYIKLLGD
VADGMQWYTLSKLSPGMLSPLVEKGLDFTLPDCFNRTTWDVLSDLTDNEELIGAITGQWGDCGVTPKQSSFMVHALIAKH
YLYGGFYPVGGASEIAKTIIPVIQASGGEVFTYADVTDILLEKGRASGVRMADGEEVRSPLVISNAGVINTFEHLLPEEV
ASRVGYQGKREHITPSMPHIGLYIGLKGTPEELGLPRTNFWIYPSADHDGNVERFLKHPDTSPLPVVYISFPAAKDPDYQ
NRWPGTSTIEIVAPTTWELFAPWQGTTWGKRGDDYETLKAQVTERILNVMYEKLPQLKGKVDYVETSTPLSTAWFCRYGR
GELYGLDHTPERFEQDWLKPKTGIPGLYLTGQDILTCGVVGAMIGGLVTTLAIRGWRGAGLARRIFMG
```


---

## Packet 2: Plan 07 Wet-Lab Candidate Packet 02

Source: `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/02_MGYG000521810_01693_organosulfur.md`

### Plan 07 Wet-Lab Candidate Packet 02

Candidate: `07:MGYG000521810:MGYG000521810_01693:organosulfur`
Protein: `MGYG000521810_01693`
Rare chemistry class: `organosulfur`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_RARE_CHEMISTRY`
Bridge score: `109.489`

#### Source Context

- Genome: `MGYG000521810`
- Biome/catalogue: `root:Environmental:Aquatic:Marine:Sediment` / `marine-sediment-v1-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Halothiobacillales;f__Halothiobacillaceae;g__Guyparkeria;s__Guyparkeria hydrothermalis`
- Completeness/contamination: `99.26` / `0.33`
- Source/extreme label: `hydrothermal` / `heat_pressure`

#### Novelty and Reaction Evidence

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `P16385` `Putative thiosulfate sulfurtransferase OS=Saccharopolyspora erythraea OX=1836 GN=cysA PE=1 SV=1`
- Top hit identity/query coverage: `29.885` / `77.0`
- Reciprocal call: `reciprocal_best_returns_other_plan07_candidate`; reciprocal best candidate `07:MGYG000511829:MGYG000511829_05846:organosulfur`
- Mapped ECs: `2.8.1.1;2.8.1.2`
- Rhea IDs: `RHEA:16881;RHEA:21740`
- Rhea terms: `organosulfur`
- BRENDA titles: `Information on EC 2.8.1.1 - thiosulfate sulfurtransferase - BRENDA Enzyme Database`

#### MSA, Active-Site, and Structure

- MSA: `ok`; sequences `9`
- Active-site/residue call: `SUPPORTED_ACTIVE_SITE_AND_REACTION_CONTEXT`
- Candidate residue markers: `phosphorus_annotation;sulfur_annotation`
- Same-class Swiss-Prot hits in top 10: `10`
- AFDB proxy status: `available`; mean pLDDT `96.067`
- Proxy loop note: `low_loop_risk`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (signal_peptide_like_n_terminus;moderate_partner_or_cofactor)
- Cofactor risk: `moderate_partner_or_cofactor`
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a rare-chemistry hypothesis candidate. Wet-lab testing should first establish soluble expression and wild-type activity against a safe, focused substrate panel. Product identity must be confirmed analytically before any new-reaction or new-specificity claim.

#### Sequence

```fasta
>MGYG000521810_01693 organosulfur
MNFKRFLAVPAGAAALAVAQGAWALDVPGPVVDPQWLNDNLDQVTVLQIAGSEKAFAMAPKYETVKGKKVVSVVSGHVPG
ARFVDWGKVRVERMENGKKVGKLIPEKADFEAFVQALGVDQDDTVVIVPLGLSGSDYTKATRLYWQMKYFGHDDMALLDG
GLANWLAAGFDAETGQPEKVEAGDWVATDERDEILATYAEVREAVDSNGKVQLLDARPPNQYLGVFSKSKTVPGHLPGAK
NVPTDVLVRADGAAANFLPESSYRSIMDFKQIDAEGAAIAYCNSGNLASGLWFVASEIMGNEQAALYDGSMKEYGMYVDD
GATSVNPAQLY
```


---

## Packet 3: Plan 07 Wet-Lab Candidate Packet 03

Source: `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/03_MGYG000478572_01361_rare_sugar.md`

### Plan 07 Wet-Lab Candidate Packet 03

Candidate: `07:MGYG000478572:MGYG000478572_01361:rare_sugar`
Protein: `MGYG000478572_01361`
Rare chemistry class: `rare_sugar`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_RARE_CHEMISTRY`
Bridge score: `108.523`

#### Source Context

- Genome: `MGYG000478572`
- Biome/catalogue: `root:Environmental:Aquatic:Marine` / `marine-v2-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Oleiphilaceae;g__Marinobacter;s__Marinobacter salinexigens`
- Completeness/contamination: `99.57` / `0.02`
- Source/extreme label: `saline` / `salt`

#### Novelty and Reaction Evidence

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `P0A5D2` `Uncharacterized protein Mb0513 OS=Mycobacterium bovis (strain ATCC BAA-935 / AF2122/97) OX=233413 GN=BQ2027_MB0513 PE=3 SV=1`
- Top hit identity/query coverage: `26.027` / `69.0`
- Reciprocal call: `reciprocal_best_returns_other_plan07_candidate`; reciprocal best candidate `07:MGYG000511829:MGYG000511829_03232:rare_sugar`
- Mapped ECs: `5.1.3.2`
- Rhea IDs: `RHEA:22168`
- Rhea terms: `rare_sugar`
- BRENDA titles: `Information on EC 5.1.3.2 - UDP-glucose 4-epimerase - BRENDA Enzyme Database`

#### MSA, Active-Site, and Structure

- MSA: `ok`; sequences `9`
- Active-site/residue call: `SUPPORTED_ACTIVE_SITE_AND_REACTION_CONTEXT`
- Candidate residue markers: `rare_sugar_annotation`
- Same-class Swiss-Prot hits in top 10: `4`
- AFDB proxy status: `available`; mean pLDDT `83.68`
- Proxy loop note: `review_low_confidence_loops`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (moderate_cofactor)
- Cofactor risk: `moderate_cofactor`
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a rare-chemistry hypothesis candidate. Wet-lab testing should first establish soluble expression and wild-type activity against a safe, focused substrate panel. Product identity must be confirmed analytically before any new-reaction or new-specificity claim.

#### Sequence

```fasta
>MGYG000478572_01361 rare_sugar
MSEKRRPHILVTGAAGALAQKVINQLRGTCDLVAVDFREQVYLGDDIPSYRIDFTKRVFEDLFRRYQFDGVIHLGRIMSS
QLTRMRRYNANVLGTQKLLDLSHKYGIKRVVVLSTFHVYGAVAYNPALIDESAPLKSAGLSADLVDSVELENLANIYLWR
YPDLNITILRPCNIVGPGVRNTMSNLLASERAPALAGFSPMMQFIHIDDMSDAIVQAYKKPVRGVFNVAPQDWVAYQHAL
KLCGCKRIPIPSIPPAVPKLILRTLKLRSFPSYLMAFFKYPVVIDGRAFAREFDFEPKRPLMEIFRFYRDNKKPV
```


---

## Packet 4: Plan 07 Wet-Lab Candidate Packet 04

Source: `outputs/plan07_rare_chemistry_bridge_2026-05-15/wetlab_candidate_packets/04_MGYG000517233_02445_dehalogenation.md`

### Plan 07 Wet-Lab Candidate Packet 04

Candidate: `07:MGYG000517233:MGYG000517233_02445:dehalogenation`
Protein: `MGYG000517233_02445`
Rare chemistry class: `dehalogenation`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_RARE_CHEMISTRY`
Bridge score: `104.18`

#### Source Context

- Genome: `MGYG000517233`
- Biome/catalogue: `root:Host-associated:Plants:Rhizosphere` / `tomato-rhizosphere-v1-0`
- Taxonomy: `d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Sphingobacteriales;f__Sphingobacteriaceae;g__Desertivirga;s__`
- Completeness/contamination: `72.19` / `1.23`
- Source/extreme label: `desert` / `desiccation`

#### Novelty and Reaction Evidence

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `A0A0U5GNT1` `Drimenol cyclase drtB OS=Aspergillus calidoustus OX=454130 GN=drtB PE=1 SV=1`
- Top hit identity/query coverage: `26.238` / `98.0`
- Reciprocal call: `reciprocal_best_returns_other_plan07_candidate`; reciprocal best candidate `07:MGYG000518629:MGYG000518629_00074:halogenation`
- Mapped ECs: `3.8.1.2`
- Rhea IDs: `RHEA:11192`
- Rhea terms: `halide_or_dehalogenation`
- BRENDA titles: `Information on EC 3.8.1.2 - (S)-2-haloacid dehalogenase - BRENDA Enzyme Database`

#### MSA, Active-Site, and Structure

- MSA: `ok`; sequences `9`
- Active-site/residue call: `SUPPORTED_NEEDS_MANUAL_POCKET_REVIEW`
- Candidate residue markers: `dehalogenase_annotation;hxxh_metal_site;phosphorus_annotation`
- Same-class Swiss-Prot hits in top 10: `1`
- AFDB proxy status: `available`; mean pLDDT `89.873`
- Proxy loop note: `review_low_confidence_loops`

#### Expression and Safety

- Expression risk: `LOW_EXPRESSION_RISK` (no_major_expression_flags)
- Cofactor risk: `low`
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a rare-chemistry hypothesis candidate. Wet-lab testing should first establish soluble expression and wild-type activity against a safe, focused substrate panel. Product identity must be confirmed analytically before any new-reaction or new-specificity claim.

#### Sequence

```fasta
>MGYG000517233_02445 dehalogenation
MIDTIIFDLGAVLIDWHPFHLYRKIFADELEMQQFIDTICTNSWNEEQDGGRSLAEGTELLVKQFPEHEENIRAYYGRWE
EMLNGPIQGTVDIFKELKDSGRYRILALSNWSAETYPIAQSKFDFLNWFDGVVVSGTERMRKPHPEFYHLLLDRYQVSPE
NALFIDDNLRNVEAGRRLGIESVHFTSPAELRKELQQRSLL
```
