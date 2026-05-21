# Plan 05 - Natural Stability Candidate Archive

Generated: 2026-05-18

Naturally stable homolog packets for salt, pH, and stress-condition enzyme hypotheses.

This archive preserves candidate-packet evidence for review. It is not a wet-lab protocol, synthesis instruction set, organism-release plan, or safety clearance.

Packet count: `4`

## Packet Index

| # | Packet | Source path |
|---:|---|---|
| 1 | Plan 06 Wet-Lab Candidate Packet 01 | `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/01_MGYG000478572_00760_esterase.md` |
| 2 | Plan 06 Wet-Lab Candidate Packet 02 | `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/02_MGYG000517341_01521_dehalogenase.md` |
| 3 | Plan 06 Wet-Lab Candidate Packet 03 | `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/03_MGYG000518629_02280_esterase.md` |
| 4 | Plan 06 Wet-Lab Candidate Packet 04 | `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/04_MGYG000478572_01589_transaminase.md` |

## Full Packet Text


---

## Packet 1: Plan 06 Wet-Lab Candidate Packet 01

Source: `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/01_MGYG000478572_00760_esterase.md`

### Plan 06 Wet-Lab Candidate Packet 01

Candidate: `06:MGYG000478572:MGYG000478572_00760:salt_esterase`
Protein: `MGYG000478572_00760`
Family: `esterase`
Primary stability axis: `salt`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_NATURAL_HOMOLOG`
Bridge score: `133.119`

#### Source Context

- Genome: `MGYG000478572`
- Biome/catalogue: `root:Environmental:Aquatic:Marine` / `marine-v2-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Oleiphilaceae;g__Marinobacter;s__Marinobacter salinexigens`
- Completeness/contamination: `99.57` / `0.02`
- Condition label: `salt`

#### Stability Evidence

- Salt score: `50.116`
- Heat score: `20.488`
- pH score: `13.22`
- Solvent/detergent score: `32.172`
- Sequence charge/proline: `0.2088` / `0.064`

#### Novelty, MSA, and Structure

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `P18773` `Esterase OS=Acinetobacter venetianus (strain ATCC 31012 / DSM 23050 / BCRC 14357 / CCUG 45561 / CIP 110063 / KCTC 2702 / LMG 19082 / RAG-1) OX=1191460 GN=est PE=3 SV=2`
- Top hit identity/query coverage: `39.367` / `73.0`
- MSA: `ok`; sequences `9`
- Catalytic review: `SUPPORTED_BY_MOTIF_AND_FAMILY_MSA`
- AlphaFold DB status: `available`; mean pLDDT `95.827`
- Structure checks: salt-bridge proxy `1`; loop note `low_loop_risk`
- BRENDA EC-page condition sections: `temperature_optimum;temperature_stability;ph_optimum;ph_stability;solvent`

#### Expression and Safety

- Expression risk: `LOW_EXPRESSION_RISK` (no_major_expression_flags)
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a natural homolog candidate, not a mutation-design output. Wet-lab testing should first establish soluble expression, activity retention under the nominated stress condition, and substrate relevance. Mutation design remains deferred until the natural homolog baseline is measured.

#### Sequence

```fasta
>MGYG000478572_00760 esterase salt
MLQHLLEAGLRQTMTRLVRPLLTPALPVSLQRTLIAQAYRSSIPPRGSLFTKEILATVPVTRCQYGESTRGVILYLHGGG
YIIGSSKTHRGLTGHLAKTSGCEVIAPDYRLAPEHPFPAALEDALAVYQSLLSQGCNAGDIAVAGDSAGGGLTITLALRL
KELGLPLPSSLTVFSPWTDLTQTNLYSPECEPVLQEAWTEKAATLYAGKEALTNPLISPVFGDLSGLPPLLIQVGSEEIL
LNDAERLAKVADRDDVEVRLEVYNSLWHVFQVHSGQLERATTALEAAGRHIKAHLAG
```


---

## Packet 2: Plan 06 Wet-Lab Candidate Packet 02

Source: `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/02_MGYG000517341_01521_dehalogenase.md`

### Plan 06 Wet-Lab Candidate Packet 02

Candidate: `06:MGYG000517341:MGYG000517341_01521:salt_dehalogenase`
Protein: `MGYG000517341_01521`
Family: `dehalogenase`
Primary stability axis: `salt`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_NATURAL_HOMOLOG`
Bridge score: `128.637`

#### Source Context

- Genome: `MGYG000517341`
- Biome/catalogue: `root:Host-associated:Plants:Rhizosphere` / `tomato-rhizosphere-v1-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Pseudomonadaceae;g__Azotobacter;s__Azotobacter salinestris`
- Completeness/contamination: `100.0` / `0.21`
- Condition label: `salt`

#### Stability Evidence

- Salt score: `46.16`
- Heat score: `18.578`
- pH score: `37.883`
- Solvent/detergent score: `19.6`
- Sequence charge/proline: `0.2353` / `0.051`

#### Novelty, MSA, and Structure

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `P60527` `(S)-2-haloacid dehalogenase OS=Agrobacterium tumefaciens (strain RS5) OX=260551 PE=1 SV=1`
- Top hit identity/query coverage: `30.317` / `86.0`
- MSA: `ok`; sequences `9`
- Catalytic review: `SUPPORTED_BY_MOTIF_AND_FAMILY_MSA`
- AlphaFold DB status: `available`; mean pLDDT `94.386`
- Structure checks: salt-bridge proxy `3`; loop note `low_loop_risk`
- BRENDA EC-page condition sections: `temperature_optimum;temperature_stability;ph_optimum;ph_stability;salt_or_nacl;solvent`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (signal_peptide_like_n_terminus)
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a natural homolog candidate, not a mutation-design output. Wet-lab testing should first establish soluble expression, activity retention under the nominated stress condition, and substrate relevance. Mutation design remains deferred until the natural homolog baseline is measured.

#### Sequence

```fasta
>MGYG000517341_01521 dehalogenase salt
MHRFHILLMLLTFLMTGLQPALAEPAQGQTGLKPRVIFFDVNETLLDLESMRQSVGAALGGRQDLLPLWFSAMLHHSLVE
SATEQYHDFGTVGTAALLMVARNHGIALGEEQARSAIVTPLLRLPAHPEVREGLQALKSQGYTLVTLTNSTRRGVQTQLE
NAGLADLFADNLSIEEIRLYKPHLRTYRWAAERLGVKPEEALLVAAHGWDIAGAKAAGMPAIFVARPGQTLYPLAAEPDR
TIREIRELAKVLGSR
```


---

## Packet 3: Plan 06 Wet-Lab Candidate Packet 03

Source: `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/03_MGYG000518629_02280_esterase.md`

### Plan 06 Wet-Lab Candidate Packet 03

Candidate: `06:MGYG000518629:MGYG000518629_02280:desiccation_esterase`
Protein: `MGYG000518629_02280`
Family: `esterase`
Primary stability axis: `ph`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_NATURAL_HOMOLOG`
Bridge score: `126.83`

#### Source Context

- Genome: `MGYG000518629`
- Biome/catalogue: `root:Host-associated:Plants:Rhizosphere` / `barley-rhizosphere-v2-0`
- Taxonomy: `d__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Sphingobacteriales;f__Sphingobacteriaceae;g__Paradesertivirga;s__Paradesertivirga sp946480915`
- Completeness/contamination: `99.57` / `0.77`
- Condition label: `desiccation`

#### Stability Evidence

- Salt score: `23.456`
- Heat score: `20.09`
- pH score: `37.797`
- Solvent/detergent score: `32.044`
- Sequence charge/proline: `0.2319` / `0.0704`

#### Novelty, MSA, and Structure

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `P82450` `Sialate O-acetylesterase OS=Rattus norvegicus OX=10116 GN=Siae PE=1 SV=2`
- Top hit identity/query coverage: `26.99` / `91.0`
- MSA: `ok`; sequences `5`
- Catalytic review: `SUPPORTED_BY_MOTIF_AND_FAMILY_MSA`
- AlphaFold DB status: `available`; mean pLDDT `89.126`
- Structure checks: salt-bridge proxy `7`; loop note `review_low_confidence_loops`
- BRENDA EC-page condition sections: `temperature_optimum;temperature_stability;ph_optimum;ph_stability;salt_or_nacl;solvent;detergent`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (one_possible_tm_segment;signal_peptide_like_n_terminus)
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `3`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a natural homolog candidate, not a mutation-design output. Wet-lab testing should first establish soluble expression, activity retention under the nominated stress condition, and substrate relevance. Mutation design remains deferred until the natural homolog baseline is measured.

#### Sequence

```fasta
>MGYG000518629_02280 esterase ph
MRNLTACIILFLLALNTKAEIVLPRILAHGMVLQREKPLPIWGTAAAGENITVQFEGQEKKTTADVNGKWIVFLNPLKAS
NKPASLVIKGTNIIQLDNILVGEVWLCSGQSNMEYTMRKNSKIVNADSVQNPAGVHSPVDELEYASNPEIRIFLVNRKEL
VKPNPTHTGWSIARDSALRSFSAAGYFFAKELNEKLNVPIGMISSAIPGSAIEPWIPANGFTSEFFKDKKIGGDPGKFYE
PMIVPLAPFAVKGFLWYQGETNCFQNETIEYTYKMEALISSWRKLWSDKTLPFYYVQIAPFYYSKSTEKYPLTKETLPKF
WEAQQLAMKIPHTGMIATTDLIVTPDDLHPGFKWEIGRRLAQWPLAIDYHLNVTPSGPIYKSMRRKKHKIELNFKYAGKG
LCSKDGKELSQFEIAGNDGKFVPAKAEIKGNKLFISSPAVAKPKNVRFSWEESGKANFYNNDGLPALPFRTNNPLIGQFK
KVN
```


---

## Packet 4: Plan 06 Wet-Lab Candidate Packet 04

Source: `outputs/plan06_deep_stability_bridge_2026-05-15/wetlab_candidate_packets/04_MGYG000478572_01589_transaminase.md`

### Plan 06 Wet-Lab Candidate Packet 04

Candidate: `06:MGYG000478572:MGYG000478572_01589:salt_transaminase`
Protein: `MGYG000478572_01589`
Family: `transaminase`
Primary stability axis: `salt`
Bridge call: `ADVANCE_TO_WETLAB_PLANNING_NATURAL_HOMOLOG`
Bridge score: `121.602`

#### Source Context

- Genome: `MGYG000478572`
- Biome/catalogue: `root:Environmental:Aquatic:Marine` / `marine-v2-0`
- Taxonomy: `d__Bacteria;p__Pseudomonadota;c__Gammaproteobacteria;o__Pseudomonadales;f__Oleiphilaceae;g__Marinobacter;s__Marinobacter salinexigens`
- Completeness/contamination: `99.57` / `0.02`
- Condition label: `salt`

#### Stability Evidence

- Salt score: `53.376`
- Heat score: `22.325`
- pH score: `38.11`
- Solvent/detergent score: `18.998`
- Sequence charge/proline: `0.2444` / `0.0848`

#### Novelty, MSA, and Structure

- Swiss-Prot novelty: `HIGH_SEQUENCE_NOVELTY`
- Top Swiss-Prot hit: `B8DJJ6` `LL-diaminopimelate aminotransferase OS=Nitratidesulfovibrio vulgaris (strain DSM 19637 / Miyazaki F) OX=883 GN=dapL PE=3 SV=1`
- Top hit identity/query coverage: `31.646` / `97.0`
- MSA: `ok`; sequences `9`
- Catalytic review: `SUPPORTED_BY_MOTIF_AND_FAMILY_MSA`
- AlphaFold DB status: `available`; mean pLDDT `96.0`
- Structure checks: salt-bridge proxy `1`; loop note `low_loop_risk`
- BRENDA EC-page condition sections: `temperature_optimum;temperature_stability;ph_optimum;ph_stability;solvent`

#### Expression and Safety

- Expression risk: `MODERATE_EXPRESSION_RISK` (moderate_plp)
- Safety call: `PASS_WITH_CONTEXT_NOTE`
- AMR/mobile context: genome AMR rows `1`, candidate AMR `False`, candidate mobilome `False`

#### Wet-Lab Rationale

This is a natural homolog candidate, not a mutation-design output. Wet-lab testing should first establish soluble expression, activity retention under the nominated stress condition, and substrate relevance. Mutation design remains deferred until the natural homolog baseline is measured.

#### Sequence

```fasta
>MGYG000478572_01589 transaminase salt
MNPNLDRLHPYPFEKLAKLKAGITVPDHIPAISLGIGEPKHPSPGFVKQVIAENLDKLANYPTTKGTEELREAISNWATR
RFNLKEGTLSPADHVVPVNGTREAIFSLVQAVVDSSAPNATVVSPNPFYQVYEGAAFLAGATPVYLPCDGNNGFIPDFDA
VPDDVWQDCQVLFLCSPGNPSGAVIPRETLIRVIELADQHDFIVASDECYSELYPDETNPPEGLLQTCAAIGRDDYARCI
VFHSLSKRSNLPGLRSGFVAGDASILKGYLKYRTYHGCAMPIHNQLASIAAWQDEEHVKTNREAYRAKFEAVVPILREVM
DVDFPDAGFYLWPVTPMDDETFARELSAQQNVHVLPGRYLSRTVDGHNPGENRVRMALVAPVEECVEAASRIVEFVKANT
P
```
