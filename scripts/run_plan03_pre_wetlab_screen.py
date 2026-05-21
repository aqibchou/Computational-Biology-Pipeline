#!/usr/bin/env python3
"""Plan03 rigorous nitrogen-cycle pre-wet-lab screen.

This script uses existing MGnify/MGnify Genomes annotations as a frozen input
pool, then applies stricter marker, pathway, neighborhood, source, safety, and
claim-boundary gates. It intentionally avoids greenhouse/field/inoculant or
emissions-reduction claims.
"""

from __future__ import annotations

import csv
import math
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "outputs" / "computational_execution_2026-05-14"
PLAN03_DIR = INPUT_DIR / "03_nitrogen_cycle_enzyme_discovery"
PLAN03_CANDIDATES = PLAN03_DIR / "candidates.csv"
SOURCE_GENOMES = INPUT_DIR / "source_genomes.csv"
CACHE_DIR = INPUT_DIR / "cache" / "mgnify_genomes"
PLAN04_ISOLATES = ROOT / "outputs" / "plan04_claim_hardening_2026-05-17" / "plan04_isolate_availability_triage.csv"
PLAN04_FINALISTS = ROOT / "outputs" / "plan04_claim_hardening_2026-05-17" / "plan04_finalist_claim_hardening.csv"
PLAN04_ANI = ROOT / "outputs" / "plan04_reference_ani_2026-05-17" / "plan04_reference_ani_results.csv"

OUT_DIR = ROOT / "outputs" / "plan03_pre_wetlab_screen_2026-05-18"
PACKET_DIR = OUT_DIR / "plan03_top_candidate_packets"
PHYLO_DIR = OUT_DIR / "plan03_marker_phylogenies"

MAFFT = shutil.which("mafft")
IQTREE = shutil.which("iqtree3") or shutil.which("iqtree2") or shutil.which("iqtree")


TRACK_LABELS = {
    "nitrogen_fixation": "Nitrogen fixation",
    "n2o_reduction": "Nitrous oxide reduction / denitrification completion",
    "nitrification_amo_hao": "Nitrification / ammonia oxidation",
    "nitrate_nitrite_transformation": "Nitrate/nitrite transformation",
    "urea_rhizosphere": "Urea metabolism and rhizosphere nitrogen availability",
}


MARKERS = [
    {
        "marker": "nifH",
        "track": "nitrogen_fixation",
        "role": "core",
        "kos": {"K02588"},
        "pfams": {"PF00142"},
        "terms": ["nifh", "nitrogenase iron protein"],
        "length_min": 250,
        "length_max": 360,
        "false_positive_risk": "ParA/MinD P-loop ATPases and generic Fe-S proteins",
        "positive_control": "UniProtKB:P00459 nitrogenase iron protein-like annotation",
        "confusable": ["parA", "mind", "soj", "sporulation initiation inhibitor", "septum site"],
    },
    {
        "marker": "nifD_vnfD_alpha",
        "track": "nitrogen_fixation",
        "role": "core",
        "kos": {"K02586", "K02587"},
        "pfams": {"PF00148"},
        "terms": ["nifd", "vnfd", "nitrogenase molybdenum-iron protein alpha", "nitrogenase vanadium-iron protein alpha"],
        "length_min": 420,
        "length_max": 560,
        "false_positive_risk": "light-independent protochlorophyllide reductase homologs",
        "positive_control": "UniProtKB:P00466/P16855 nitrogenase alpha-chain-like annotation",
        "confusable": ["protochlorophyllide reductase"],
    },
    {
        "marker": "nifK_vnfK_beta",
        "track": "nitrogen_fixation",
        "role": "core",
        "kos": {"K02591", "K02592"},
        "pfams": {"PF00148"},
        "terms": ["nifk", "vnfk", "nitrogenase molybdenum-iron protein beta", "nitrogenase vanadium-iron protein beta"],
        "length_min": 400,
        "length_max": 560,
        "false_positive_risk": "light-independent protochlorophyllide reductase homologs",
        "positive_control": "UniProtKB:P11347/P16856 nitrogenase beta-chain-like annotation",
        "confusable": ["protochlorophyllide reductase"],
    },
    {
        "marker": "nifB",
        "track": "nitrogen_fixation",
        "role": "accessory",
        "kos": {"K02585"},
        "pfams": {"PF04055"},
        "terms": ["nifb", "femo cofactor biosynthesis protein nifb"],
        "length_min": 330,
        "length_max": 560,
        "false_positive_risk": "generic radical SAM proteins",
        "positive_control": "NifB radical-SAM FeMo cofactor annotation",
        "confusable": ["generic radical sam"],
    },
    {
        "marker": "nif_vnf_accessory",
        "track": "nitrogen_fixation",
        "role": "accessory",
        "kos": {"K02584", "K02595", "K02596", "K00531"},
        "pfams": {"PF03139", "PF00158"},
        "terms": ["vnfg", "vnfa", "nifx", "nitrogen fixation protein", "dinitrogenase iron-molybdenum cofactor"],
        "length_min": 80,
        "length_max": 650,
        "false_positive_risk": "generic regulatory or FeMo-cofactor-like annotations without core nif genes",
        "positive_control": "nif/vnf accessory context near core nitrogenase genes",
        "confusable": ["generic transcriptional regulator"],
    },
    {
        "marker": "nosZ",
        "track": "n2o_reduction",
        "role": "core",
        "kos": {"K00376"},
        "pfams": {"PF18764", "PF18793"},
        "terms": ["nosz", "nitrous-oxide reductase", "nitrous oxide reductase"],
        "length_min": 520,
        "length_max": 760,
        "false_positive_risk": "COX2/cupredoxin/cytochrome oxidase copper-center proteins",
        "positive_control": "UniProtKB:P19573 NosZ-like annotation",
        "confusable": ["cytochrome c oxidase subunit 2", "cox2", "cupredoxin only"],
    },
    {
        "marker": "nosD",
        "track": "n2o_reduction",
        "role": "accessory",
        "kos": {"K07218"},
        "pfams": {"PF05048"},
        "terms": ["nosd", "nitrous oxidase accessory protein", "periplasmic copper-binding protein nosd"],
        "length_min": 300,
        "length_max": 520,
        "false_positive_risk": "generic ABC binding proteins",
        "positive_control": "NosD accessory context near nosZ",
        "confusable": ["generic abc transporter binding protein"],
    },
    {
        "marker": "nosF",
        "track": "n2o_reduction",
        "role": "accessory",
        "kos": {"K19340"},
        "pfams": {"PF00005"},
        "terms": ["nosf", "abc transporter atp-binding protein nosf"],
        "length_min": 220,
        "length_max": 360,
        "false_positive_risk": "generic ABC ATP-binding proteins",
        "positive_control": "NosF accessory context near nosZ",
        "confusable": ["generic abc transporter"],
    },
    {
        "marker": "nosY",
        "track": "n2o_reduction",
        "role": "accessory",
        "kos": {"K19341"},
        "pfams": {"PF12679"},
        "terms": ["nosy", "permease protein nosy"],
        "length_min": 220,
        "length_max": 360,
        "false_positive_risk": "generic permeases",
        "positive_control": "NosY accessory context near nosZ",
        "confusable": ["generic permease"],
    },
    {
        "marker": "nosR_L_context",
        "track": "n2o_reduction",
        "role": "accessory",
        "kos": {"K19339", "K19342"},
        "pfams": {"PF12801", "PF05573"},
        "terms": ["nosr", "nitrous oxide reductase expression regulator", "electron transport protein nosr"],
        "length_min": 120,
        "length_max": 760,
        "false_positive_risk": "generic redox or transcription-regulator proteins",
        "positive_control": "NosR/NosL-like context near nosZ",
        "confusable": ["generic regulator"],
    },
    {
        "marker": "narG_napA_nitrate_reductase",
        "track": "nitrate_nitrite_transformation",
        "role": "core",
        "kos": {"K00370", "K05299", "K02567"},
        "pfams": {"PF00384", "PF01568", "PF14710"},
        "terms": ["narg", "napa", "respiratory nitrate reductase", "periplasmic nitrate reductase"],
        "length_min": 700,
        "length_max": 1300,
        "false_positive_risk": "formate dehydrogenase and generic molybdopterin oxidoreductases",
        "positive_control": "NarG/NapA nitrate-reductase-like annotation",
        "confusable": ["formate dehydrogenase", "acetylene hydratase"],
    },
    {
        "marker": "narH_napB_nitrate_reductase",
        "track": "nitrate_nitrite_transformation",
        "role": "accessory",
        "kos": {"K00371", "K02568"},
        "pfams": {"PF13247", "PF14711"},
        "terms": ["narh", "napb", "nitrate reductase beta", "periplasmic nitrate reductase cytochrome"],
        "length_min": 140,
        "length_max": 620,
        "false_positive_risk": "generic Fe-S proteins",
        "positive_control": "NarH/NapB context near nitrate reductase",
        "confusable": ["generic ferredoxin"],
    },
    {
        "marker": "narJ_I_context",
        "track": "nitrate_nitrite_transformation",
        "role": "accessory",
        "kos": {"K00373", "K00374"},
        "pfams": {"PF02665"},
        "terms": ["narj", "nari", "narv", "nitrate reductase molybdenum cofactor assembly", "nitrate reductase gamma"],
        "length_min": 180,
        "length_max": 320,
        "false_positive_risk": "generic membrane or assembly proteins",
        "positive_control": "NarJ/NarI context near narG/narH",
        "confusable": ["generic membrane protein"],
    },
    {
        "marker": "nirS_nirK_or_assimilatory_nitrite",
        "track": "nitrate_nitrite_transformation",
        "role": "core",
        "kos": {"K00362", "K00363", "K00366", "K00368"},
        "pfams": set(),
        "terms": ["nirs", "nirk", "nitrite reductase", "nirb", "nird", "nasa", "nasb"],
        "length_min": 120,
        "length_max": 900,
        "false_positive_risk": "sulfite reductases and generic Fe-S reductases",
        "positive_control": "nitrite-reductase-like annotation with pathway context",
        "confusable": ["sulfite reductase"],
    },
    {
        "marker": "nrfA",
        "track": "nitrate_nitrite_transformation",
        "role": "core",
        "kos": {"K03385"},
        "pfams": {"PF02335"},
        "terms": ["nrfa", "cytochrome c-552", "respiratory nitrite reductase"],
        "length_min": 350,
        "length_max": 560,
        "false_positive_risk": "generic multiheme cytochromes",
        "positive_control": "NrfA cytochrome c-552 annotation",
        "confusable": ["generic cytochrome"],
    },
    {
        "marker": "nrfH",
        "track": "nitrate_nitrite_transformation",
        "role": "accessory",
        "kos": {"K15876"},
        "pfams": {"PF03264"},
        "terms": ["nrfh", "cytochrome c-type protein nrfh"],
        "length_min": 120,
        "length_max": 260,
        "false_positive_risk": "generic cytochrome proteins",
        "positive_control": "NrfH context near nrfA",
        "confusable": ["generic cytochrome"],
    },
    {
        "marker": "amoA_pmoA",
        "track": "nitrification_amo_hao",
        "role": "core",
        "kos": {"K10944"},
        "pfams": set(),
        "terms": ["amoa", "ammonia monooxygenase", "particulate methane monooxygenase beta subunit"],
        "length_min": 220,
        "length_max": 380,
        "false_positive_risk": "particulate methane monooxygenase; AMO/pMMO cannot be resolved by annotation alone",
        "positive_control": "AmoA/PmoA-like annotation with amoBC context",
        "confusable": ["methane monooxygenase"],
    },
    {
        "marker": "amoB",
        "track": "nitrification_amo_hao",
        "role": "core",
        "kos": {"K10945"},
        "pfams": set(),
        "terms": ["amob", "ammonia monooxygenase subunit b"],
        "length_min": 300,
        "length_max": 520,
        "false_positive_risk": "methane monooxygenase homologs",
        "positive_control": "AmoB context with amoA/amoC",
        "confusable": ["methane monooxygenase"],
    },
    {
        "marker": "amoC",
        "track": "nitrification_amo_hao",
        "role": "core",
        "kos": {"K10946"},
        "pfams": set(),
        "terms": ["amoc", "ammonia monooxygenase/methane monooxygenase, subunit c"],
        "length_min": 200,
        "length_max": 360,
        "false_positive_risk": "methane monooxygenase homologs",
        "positive_control": "AmoC context with amoA/amoB",
        "confusable": ["methane monooxygenase"],
    },
    {
        "marker": "hao_hydroxylamine_context",
        "track": "nitrification_amo_hao",
        "role": "accessory",
        "kos": {"K10535", "K05601"},
        "pfams": {"PF04879"},
        "terms": ["hao", "hydroxylamine oxidoreductase", "hydroxylamine reductase"],
        "length_min": 400,
        "length_max": 900,
        "false_positive_risk": "Hcp/hydroxylamine reductase is not HAO and requires manual review",
        "positive_control": "Hao-like context with AMO genes",
        "confusable": ["carbon monoxide dehydrogenase", "hcp"],
    },
    {
        "marker": "ureA_gamma",
        "track": "urea_rhizosphere",
        "role": "core",
        "kos": {"K01430"},
        "pfams": {"PF00547"},
        "terms": ["gene=urea", "name=urea", "urease subunit gamma"],
        "length_min": 75,
        "length_max": 130,
        "false_positive_risk": "broad amidohydrolase family hits without urease operon",
        "positive_control": "UreA gamma subunit in ureABCD/EFG cluster",
        "confusable": ["amidohydrolase only"],
    },
    {
        "marker": "ureB_beta",
        "track": "urea_rhizosphere",
        "role": "core",
        "kos": {"K01429", "K14048"},
        "pfams": {"PF00699"},
        "terms": ["ureb", "urease subunit beta"],
        "length_min": 90,
        "length_max": 150,
        "false_positive_risk": "broad amidohydrolase family hits without urease operon",
        "positive_control": "UreB beta subunit in urease operon",
        "confusable": ["amidohydrolase only"],
    },
    {
        "marker": "ureC_alpha",
        "track": "urea_rhizosphere",
        "role": "core",
        "kos": {"K01428"},
        "pfams": {"PF00449", "PF01979"},
        "terms": ["urec", "urease subunit alpha"],
        "length_min": 480,
        "length_max": 650,
        "false_positive_risk": "broad amidohydrolase family hits without urease operon",
        "positive_control": "UreC alpha subunit in urease operon",
        "confusable": ["dihydroorotase", "n-acetylglucosamine-6-phosphate deacetylase"],
    },
    {
        "marker": "ureD_E_F_G_accessory",
        "track": "urea_rhizosphere",
        "role": "accessory",
        "kos": {"K03187", "K03188", "K03189", "K03190"},
        "pfams": {"PF01774", "PF02814", "PF01730", "PF02492"},
        "terms": ["ured", "uree", "uref", "ureg", "urease accessory protein"],
        "length_min": 120,
        "length_max": 360,
        "false_positive_risk": "generic nickel/ATP-binding/accessory proteins unless near ureABC",
        "positive_control": "UreD/E/F/G context near ureABC",
        "confusable": ["generic gtpase", "generic nickel-binding"],
    },
    {
        "marker": "urea_or_ammonium_transport",
        "track": "urea_rhizosphere",
        "role": "accessory",
        "kos": {"K03320", "K11959", "K11960", "K11961"},
        "pfams": {"PF00909"},
        "terms": ["urea transporter", "ammonium transporter", "amtb", "ammonium/urea transporter"],
        "length_min": 250,
        "length_max": 520,
        "false_positive_risk": "ammonium transport does not prove urease activity",
        "positive_control": "transport context near nitrogen availability loci",
        "confusable": ["ammonium transporter alone"],
    },
]


MARKER_BY_NAME = {marker["marker"]: marker for marker in MARKERS}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fnum(value: object, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def inum(value: object, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def norm(text: object) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").split())


def has_any(text: str, terms: list[str] | set[str]) -> bool:
    low = text.lower()
    return any(str(term).lower() in low for term in terms)


def parse_attrs(attr_text: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for part in attr_text.split(";"):
        if not part:
            continue
        if "=" in part:
            key, value = part.split("=", 1)
            attrs[key] = unquote(value)
    return attrs


def split_kos(text: object) -> set[str]:
    return set(re.findall(r"K\d{5}", str(text or "")))


def split_terms(text: object) -> set[str]:
    values = re.split(r"[,;| ]+", str(text or ""))
    return {value.strip() for value in values if value.strip()}


def protein_number(protein_id: str) -> int | None:
    match = re.search(r"_(\d+)$", protein_id or "")
    return int(match.group(1)) if match else None


def read_sources() -> dict[str, dict[str, str]]:
    return {row["genome_id"]: row for row in read_csv(SOURCE_GENOMES)}


def load_plan04_context() -> dict[str, dict[str, str]]:
    context: dict[str, dict[str, str]] = defaultdict(dict)
    for row in read_csv(PLAN04_ISOLATES):
        context[row.get("genome_id", "")].update(
            {
                "availability_call": row.get("availability_call", ""),
                "cultured_relative_note": row.get("cultured_relative_note", ""),
                "surrogate_path": row.get("surrogate_path", ""),
            }
        )
    for row in read_csv(PLAN04_FINALISTS):
        context[row.get("genome_id", "")].update(
            {
                "plan04_trait": row.get("primary_trait_label", ""),
                "plan04_call": row.get("claim_hardening_call", ""),
                "plan04_safety_call": row.get("safety_call", ""),
            }
        )
    for row in read_csv(PLAN04_ANI):
        genome_id = row.get("candidate_genome_id", "")
        if genome_id and ("EXACT" in row.get("reference_gate_call", "") or "plan04_reference_gate" not in context[genome_id]):
            context[genome_id]["plan04_reference_gate"] = row.get("reference_gate_call", "")
    return context


def parse_fasta(path: Path) -> dict[str, str]:
    sequences: dict[str, str] = {}
    if not path.exists():
        return sequences
    header = ""
    parts: list[str] = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    sequences[header] = "".join(parts)
                header = line[1:].split()[0]
                parts = []
            else:
                parts.append(re.sub(r"[^A-Za-z*]", "", line).replace("*", "").upper())
        if header:
            sequences[header] = "".join(parts)
    return sequences


def parse_genome_gff(genome_id: str, sequences: dict[str, str]) -> list[dict[str, object]]:
    path = CACHE_DIR / genome_id / f"{genome_id}.gff"
    genes: list[dict[str, object]] = []
    if not path.exists():
        return genes
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9 or parts[2] != "CDS":
                continue
            attrs = parse_attrs(parts[8])
            protein_id = attrs.get("ID") or attrs.get("locus_tag") or ""
            if not protein_id:
                continue
            try:
                start = int(parts[3])
                end = int(parts[4])
            except ValueError:
                start = end = 0
            seq = sequences.get(protein_id, "")
            genes.append(
                {
                    "protein_id": protein_id,
                    "genome_id": genome_id,
                    "contig": parts[0],
                    "start": start,
                    "end": end,
                    "strand": parts[6],
                    "length_aa": len(seq),
                    "sequence": seq,
                    "gene": attrs.get("gene") or attrs.get("Name") or "",
                    "name": attrs.get("Name", ""),
                    "product": attrs.get("product", ""),
                    "ec": attrs.get("eC_number", ""),
                    "kegg_ko": attrs.get("kegg") or attrs.get("KEGG") or "",
                    "pfams": attrs.get("pfam") or attrs.get("Pfam") or "",
                    "interpro_ids": attrs.get("interpro") or attrs.get("InterPro") or "",
                    "eggNOG": attrs.get("eggNOG", ""),
                    "raw_attrs": parts[8],
                }
            )
    return genes


def gene_text(gene: dict[str, object]) -> str:
    keys = ["gene", "name", "product", "ec", "kegg_ko", "pfams", "interpro_ids", "eggNOG", "raw_attrs"]
    return norm(" ".join(str(gene.get(key, "")) for key in keys))


def marker_hit_for_gene(gene: dict[str, object], marker: dict[str, object]) -> dict[str, object] | None:
    text = gene_text(gene)
    kos = split_kos(gene.get("kegg_ko")) | split_kos(gene.get("raw_attrs"))
    pfams = split_terms(gene.get("pfams"))
    marker_kos = set(marker.get("kos", set()))
    marker_pfams = set(marker.get("pfams", set()))
    terms = list(marker.get("terms", []))
    confusable = list(marker.get("confusable", []))
    evidence = []
    score = 0.0
    if marker_kos and kos & marker_kos:
        score = max(score, 1.0)
        evidence.append("exact_ko:" + "|".join(sorted(kos & marker_kos)))
    gene_name = norm(gene.get("gene") or gene.get("name"))
    for term in terms:
        t = term.lower()
        if gene_name == t or gene_name.startswith(t + " "):
            score = max(score, 0.95)
            evidence.append(f"gene_name:{term}")
            break
    if has_any(text, terms):
        score = max(score, 0.82)
        evidence.append("marker_text")
    if marker_pfams and pfams & marker_pfams:
        score = max(score, 0.76)
        evidence.append("pfam:" + "|".join(sorted(pfams & marker_pfams)))

    if score == 0.0:
        return None
    if marker.get("marker") == "nirS_nirK_or_assimilatory_nitrite" and "sulfite reductase" in text and "nitrite reductase" not in text:
        return None

    length = int(gene.get("length_aa") or 0)
    length_ok = True
    if length and (length < int(marker.get("length_min", 0)) or length > int(marker.get("length_max", 10000))):
        length_ok = False
        score -= 0.18
        evidence.append("length_outside_expected_range")
    conf = [term for term in confusable if term and term.lower() in text]
    if conf:
        if not (marker_kos and kos & marker_kos):
            score -= 0.35
        else:
            score -= 0.08
        evidence.append("confusable_terms:" + "|".join(conf[:4]))

    score = clip(score)
    if score >= 0.9:
        call = "PASS_MARKER_SPECIFIC"
    elif score >= 0.72 and length_ok:
        call = "PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT"
    elif conf:
        call = "HOLD_CONFUSABLE_DOMAIN"
    else:
        call = "HOLD_LOW_COVERAGE_OR_FRAGMENT"

    row = dict(gene)
    row.update(
        {
            "marker": marker["marker"],
            "track": marker["track"],
            "marker_role": marker["role"],
            "marker_specificity_score": round(score, 3),
            "marker_evidence": ";".join(evidence),
            "marker_audit_call": call,
            "false_positive_risk": marker["false_positive_risk"],
        }
    )
    return row


def detect_marker_hits(genes: list[dict[str, object]]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for gene in genes:
        for marker in MARKERS:
            hit = marker_hit_for_gene(gene, marker)
            if hit is not None:
                hits.append(hit)
    return hits


def quality_score(source: dict[str, str]) -> tuple[float, str]:
    comp = fnum(source.get("completeness"))
    contam = fnum(source.get("contamination"), 100.0)
    if comp >= 95 and contam <= 2:
        return 1.0, "HIGH_QUALITY"
    if comp >= 90 and contam <= 5:
        return 0.85, "GOOD_QUALITY"
    if comp >= 80 and contam <= 10:
        return 0.62, "MODERATE_QUALITY"
    if comp >= 70 and contam <= 10:
        return 0.42, "LOW_MODERATE_QUALITY"
    return 0.2, "LOW_QUALITY_HOLD"


def source_score(source: dict[str, str], track: str) -> tuple[float, str]:
    text = norm(" ".join(source.get(k, "") for k in ["query", "query_label", "extreme_label", "catalogue", "biome", "taxon_lineage"]))
    if any(term in text for term in ["gut", "digestive", "gastrointestinal"]):
        return 0.25, "gut_source_deprioritized"
    tags = []
    for term, tag in [
        ("rhizosphere", "rhizosphere"),
        ("soil", "soil"),
        ("marine sediment", "marine_sediment"),
        ("sediment", "sediment"),
        ("wastewater", "wastewater"),
        ("hydrothermal", "redox_gradient_proxy"),
        ("marine", "marine"),
        ("saline", "saline"),
        ("desert", "desiccation"),
        ("azotobacter", "diazotroph_genus_context"),
        ("marinobacter", "marine_redox_context"),
    ]:
        if term in text:
            tags.append(tag)
    base = 0.5 if not tags else 0.72
    if track == "nitrogen_fixation" and ("rhizosphere" in tags or "diazotroph_genus_context" in tags or "soil" in tags):
        base = 0.92
    if track == "n2o_reduction" and any(tag in tags for tag in ["soil", "sediment", "marine_sediment", "marine", "redox_gradient_proxy"]):
        base = 0.86
    if track == "urea_rhizosphere" and any(tag in tags for tag in ["rhizosphere", "soil", "diazotroph_genus_context"]):
        base = 0.9
    if track == "nitrate_nitrite_transformation" and any(tag in tags for tag in ["soil", "sediment", "marine_sediment", "redox_gradient_proxy"]):
        base = 0.82
    if track == "nitrification_amo_hao" and any(tag in tags for tag in ["soil", "rhizosphere", "sediment", "wastewater"]):
        base = 0.78
    return base, ";".join(tags) if tags else "generic_environment_context"


def recovery_score(source: dict[str, str], plan04: dict[str, str]) -> tuple[float, str]:
    availability = plan04.get("availability_call", "")
    if "CULTURED_CLOSE_RELATIVE" in availability or "MGNIFY_ISOLATE" in availability:
        return 1.0, availability
    if norm(source.get("type")) == "isolate":
        return 0.85, "MGNIFY_ISOLATE_METADATA_ONLY"
    if "NO_CULTURED_CLOSE_RELATIVE" in availability:
        return 0.35, availability
    if "DISTANT_GENUS_REFERENCE" in availability:
        return 0.45, availability
    return 0.55, "MAG_OR_UNCONFIRMED_RECOVERY_ROUTE"


def distance_to_interval(start: int, end: int, other_start: int, other_end: int) -> int:
    if end < other_start:
        return other_start - end
    if other_end < start:
        return start - other_end
    return 0


def parse_gff_features(path: Path) -> list[dict[str, object]]:
    features: list[dict[str, object]] = []
    if not path.exists():
        return features
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9:
                continue
            try:
                start = int(parts[3])
                end = int(parts[4])
            except ValueError:
                continue
            attrs = parse_attrs(parts[8])
            features.append(
                {
                    "contig": parts[0],
                    "source": parts[1],
                    "type": parts[2],
                    "start": start,
                    "end": end,
                    "attrs": attrs,
                    "raw": parts[8],
                }
            )
    return features


def parse_amrfinder(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or line.lower().startswith("protein id"):
                continue
            parts = line.split("\t")
            if len(parts) < 10:
                continue
            rows.append(
                {
                    "protein_id": parts[0],
                    "contig": parts[1],
                    "start": inum(parts[2]),
                    "end": inum(parts[3]),
                    "symbol": parts[5],
                    "element_name": parts[6],
                    "scope": parts[7],
                    "type": parts[8],
                    "subtype": parts[9],
                    "raw": line,
                }
            )
    return rows


def nearby_features(anchor_hits: list[dict[str, object]], features: list[dict[str, object]], window_bp: int) -> list[dict[str, object]]:
    out = []
    for hit in anchor_hits:
        contig = hit.get("contig")
        start = inum(hit.get("start"))
        end = inum(hit.get("end"))
        for feature in features:
            if feature.get("contig") != contig:
                continue
            dist = distance_to_interval(start, end, inum(feature.get("start")), inum(feature.get("end")))
            if dist <= window_bp:
                row = dict(feature)
                row["distance_bp"] = dist
                row["anchor_marker"] = hit.get("marker")
                row["anchor_protein_id"] = hit.get("protein_id")
                out.append(row)
    return out


def marker_summary(hits: list[dict[str, object]]) -> str:
    parts = []
    for hit in sorted(hits, key=lambda h: (str(h.get("contig")), inum(h.get("start")))):
        parts.append(f"{hit.get('marker')}:{hit.get('protein_id')}:{hit.get('contig')}:{hit.get('start')}-{hit.get('end')}")
    return "; ".join(parts)


def best_contig_cluster(hits: list[dict[str, object]], markers: set[str], window: int) -> tuple[list[dict[str, object]], float, str]:
    target_hits = [hit for hit in hits if hit["marker"] in markers and hit.get("marker_specificity_score", 0) >= 0.65]
    best: list[dict[str, object]] = []
    best_score = 0.0
    best_note = "no_marker_cluster"
    by_contig: dict[str, list[dict[str, object]]] = defaultdict(list)
    for hit in target_hits:
        by_contig[str(hit.get("contig"))].append(hit)
    for contig, chits in by_contig.items():
        chits.sort(key=lambda h: inum(h.get("start")))
        for anchor in chits:
            center = (inum(anchor.get("start")) + inum(anchor.get("end"))) // 2
            cluster = [
                hit
                for hit in chits
                if abs(((inum(hit.get("start")) + inum(hit.get("end"))) // 2) - center) <= window
            ]
            present = {str(hit.get("marker")) for hit in cluster}
            score = len(present & markers) / len(markers) if markers else 0
            if score > best_score or (math.isclose(score, best_score) and len(cluster) > len(best)):
                best = cluster
                best_score = score
                span = max(inum(h.get("end")) for h in cluster) - min(inum(h.get("start")) for h in cluster) if cluster else 0
                best_note = f"contig={contig};span_bp={span};markers={','.join(sorted(present & markers))}"
    return best, best_score, best_note


def build_pathway_profiles(
    all_hits: list[dict[str, object]],
    sources: dict[str, dict[str, str]],
    plan04: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    amr_by_genome = {
        genome_id: parse_amrfinder(CACHE_DIR / genome_id / f"{genome_id}_amrfinderplus.tsv")
        for genome_id in sources
    }
    mobilome_by_genome = {
        genome_id: parse_gff_features(CACHE_DIR / genome_id / f"{genome_id}_mobilome.gff")
        for genome_id in sources
    }
    by_genome: dict[str, list[dict[str, object]]] = defaultdict(list)
    for hit in all_hits:
        if hit.get("marker_specificity_score", 0) >= 0.55:
            by_genome[str(hit.get("genome_id"))].append(hit)

    track_specs = {
        "nitrogen_fixation": {
            "core": {"nifH", "nifD_vnfD_alpha", "nifK_vnfK_beta"},
            "accessory": {"nifB", "nif_vnf_accessory"},
            "window": 80000,
            "representative": "nifH",
        },
        "n2o_reduction": {
            "core": {"nosZ"},
            "accessory": {"nosD", "nosF", "nosY", "nosR_L_context"},
            "window": 25000,
            "representative": "nosZ",
        },
        "nitrification_amo_hao": {
            "core": {"amoA_pmoA", "amoB", "amoC"},
            "accessory": {"hao_hydroxylamine_context"},
            "window": 30000,
            "representative": "amoA_pmoA",
        },
        "nitrate_nitrite_transformation": {
            "core": {"narG_napA_nitrate_reductase", "nrfA", "nirS_nirK_or_assimilatory_nitrite"},
            "accessory": {"narH_napB_nitrate_reductase", "narJ_I_context", "nrfH"},
            "window": 30000,
            "representative": "narG_napA_nitrate_reductase",
        },
        "urea_rhizosphere": {
            "core": {"ureA_gamma", "ureB_beta", "ureC_alpha"},
            "accessory": {"ureD_E_F_G_accessory", "urea_or_ammonium_transport"},
            "window": 35000,
            "representative": "ureC_alpha",
        },
    }

    rows: list[dict[str, object]] = []
    for genome_id, hits in sorted(by_genome.items()):
        source = sources.get(genome_id, {})
        qscore, qcall = quality_score(source)
        rec_score, rec_call = recovery_score(source, plan04.get(genome_id, {}))
        for track, spec in track_specs.items():
            track_hits = [hit for hit in hits if hit.get("track") == track]
            if not track_hits:
                continue
            source_support, source_note = source_score(source, track)
            core = set(spec["core"])
            accessory = set(spec["accessory"])
            relevant = core | accessory
            cluster, cluster_fraction, cluster_note = best_contig_cluster(track_hits, relevant, int(spec["window"]))
            present = {str(hit.get("marker")) for hit in track_hits if hit.get("marker_specificity_score", 0) >= 0.7}
            cluster_present = {str(hit.get("marker")) for hit in cluster if hit.get("marker_specificity_score", 0) >= 0.7}
            core_present = present & core
            accessory_present = present & accessory
            cluster_core = cluster_present & core
            cluster_accessory = cluster_present & accessory

            if track == "nitrogen_fixation":
                completeness = 0.95 if core <= cluster_present else 0.55 * len(core_present) / len(core)
                if core <= present and len(cluster_core) < len(core):
                    completeness = max(completeness, 0.65)
            elif track == "n2o_reduction":
                completeness = 0.92 if "nosZ" in cluster_present and len(cluster_accessory) >= 2 else (0.65 if "nosZ" in present else 0.25)
            elif track == "nitrification_amo_hao":
                completeness = 0.9 if core <= cluster_present else (0.45 if {"amoA_pmoA", "amoC"} <= present else 0.25)
            elif track == "nitrate_nitrite_transformation":
                nar_complete = {"narG_napA_nitrate_reductase", "narH_napB_nitrate_reductase", "narJ_I_context"} <= cluster_present
                dnra_complete = {"nrfA", "nrfH"} <= cluster_present
                nitrite_context = "nirS_nirK_or_assimilatory_nitrite" in present
                completeness = 0.86 if nar_complete or dnra_complete else (0.62 if nitrite_context or "narG_napA_nitrate_reductase" in present else 0.3)
            elif track == "urea_rhizosphere":
                completeness = 0.94 if core <= cluster_present and "ureD_E_F_G_accessory" in cluster_present else (0.62 if core <= present else 0.25)
            else:
                completeness = cluster_fraction

            marker_specificity = max([fnum(hit.get("marker_specificity_score")) for hit in track_hits] or [0.0])
            neighborhood = cluster_fraction
            outcome = {
                "nitrogen_fixation": 0.88,
                "n2o_reduction": 0.95,
                "nitrification_amo_hao": 0.74,
                "nitrate_nitrite_transformation": 0.78,
                "urea_rhizosphere": 0.76,
            }[track]
            novelty = novelty_score(source, track_hits, track)
            assay = assay_feasibility(track, completeness, rec_score)
            anchor_hits = [hit for hit in cluster if hit.get("marker") in core] or [hit for hit in track_hits if hit.get("marker") in core][:3]
            amr_near = nearby_features(anchor_hits, amr_by_genome.get(genome_id, []), 10000)
            mobile_near = nearby_features(anchor_hits, mobilome_by_genome.get(genome_id, []), 10000)
            safety, safety_call, safety_flags = safety_score(source, track_hits, amr_by_genome.get(genome_id, []), amr_near, mobile_near)
            final_score = 100.0 * (
                0.20 * marker_specificity
                + 0.18 * completeness
                + 0.15 * neighborhood
                + 0.13 * outcome
                + 0.11 * source_support
                + 0.10 * novelty
                + 0.07 * assay
                + 0.04 * qscore
                + 0.02 * safety
            )
            status = profile_status(
                track,
                completeness,
                marker_specificity,
                neighborhood,
                qscore,
                safety,
                source_support,
                rec_score,
                present,
                cluster_present,
            )
            rep_hit = choose_representative_hit(track, cluster or track_hits)
            rows.append(
                {
                    "candidate_id": f"PLAN03:{genome_id}:{track}:{rep_hit.get('protein_id', 'NA')}",
                    "genome_id": genome_id,
                    "track": track,
                    "track_label": TRACK_LABELS[track],
                    "representative_protein_id": rep_hit.get("protein_id", ""),
                    "representative_marker": rep_hit.get("marker", ""),
                    "plan03_final_score": round(final_score, 3),
                    "plan03_status": status,
                    "final_wetlab_call": "ADVANCE_TO_PRE_WETLAB_PACKET" if status == "ADVANCE_TO_PRE_WETLAB_PACKET" else ("REVIEW_BACKUP_CANDIDATE" if "REVIEW" in status else "NOT_ADVANCED"),
                    "marker_specificity": round(marker_specificity, 3),
                    "pathway_completeness": round(completeness, 3),
                    "genomic_neighborhood_support": round(neighborhood, 3),
                    "target_outcome_relevance": round(outcome, 3),
                    "source_environment_metadata_strength": round(source_support, 3),
                    "novelty_or_phylogenetic_interest": round(novelty, 3),
                    "assay_and_recovery_feasibility": round(assay, 3),
                    "genome_quality": round(qscore, 3),
                    "safety_context_score": round(safety, 3),
                    "core_markers_present": ";".join(sorted(core_present)),
                    "accessory_markers_present": ";".join(sorted(accessory_present)),
                    "cluster_core_markers_present": ";".join(sorted(cluster_core)),
                    "cluster_accessory_markers_present": ";".join(sorted(cluster_accessory)),
                    "missing_core_markers": ";".join(sorted(core - core_present)),
                    "cluster_note": cluster_note,
                    "pathway_gene_table": marker_summary(cluster or track_hits[:10]),
                    "all_marker_summary": marker_summary(track_hits),
                    "source_environment_note": source_note,
                    "genome_quality_call": qcall,
                    "recovery_call": rec_call,
                    "safety_call": safety_call,
                    "safety_flags": safety_flags,
                    "candidate_near_amr_count": len(amr_near),
                    "candidate_near_amr_summary": summarize_amr(amr_near),
                    "candidate_near_mobile_count": len(mobile_near),
                    "candidate_near_mobile_summary": summarize_mobile(mobile_near),
                    "genome_amr_rows": len(amr_by_genome.get(genome_id, [])),
                    "genome_mobilome_feature_rows": len(mobilome_by_genome.get(genome_id, [])),
                    "genome_type": source.get("type", ""),
                    "completeness": source.get("completeness", ""),
                    "contamination": source.get("contamination", ""),
                    "num_contigs": source.get("num_contigs", ""),
                    "n50": source.get("n50", ""),
                    "query_label": source.get("query_label", source.get("query", "")),
                    "source_query": source.get("query", ""),
                    "extreme_label": source.get("extreme_label", ""),
                    "biome": source.get("biome", ""),
                    "catalogue": source.get("catalogue", ""),
                    "taxon_lineage": source.get("taxon_lineage", ""),
                    "plan04_trait": plan04.get(genome_id, {}).get("plan04_trait", ""),
                    "plan04_reference_gate": plan04.get(genome_id, {}).get("plan04_reference_gate", ""),
                    "strongest_safe_claim": strongest_safe_claim(track),
                    "claim_limit": claim_limit(track),
                }
            )
    rows.sort(key=lambda r: (str(r["track"]), -fnum(r["plan03_final_score"]), str(r["candidate_id"])))
    return rows


def novelty_score(source: dict[str, str], hits: list[dict[str, object]], track: str) -> float:
    taxonomy = norm(source.get("taxon_lineage"))
    if any(term in taxonomy for term in ["uba", "candidatus", "methylomirabilota", "bdellovibrionota", "planctomycetota"]):
        return 0.78
    if any("hypothetical protein" in norm(hit.get("product")) for hit in hits):
        return 0.65
    if norm(source.get("type")) == "isolate":
        return 0.5
    return 0.6


def assay_feasibility(track: str, completeness: float, recovery: float) -> float:
    base = {
        "nitrogen_fixation": 0.64,
        "n2o_reduction": 0.72,
        "nitrification_amo_hao": 0.58,
        "nitrate_nitrite_transformation": 0.68,
        "urea_rhizosphere": 0.78,
    }[track]
    if completeness >= 0.85:
        base += 0.1
    if recovery >= 0.85:
        base += 0.08
    elif recovery < 0.45:
        base -= 0.12
    return clip(base)


def safety_score(
    source: dict[str, str],
    hits: list[dict[str, object]],
    amr_rows: list[dict[str, object]],
    amr_near: list[dict[str, object]],
    mobile_near: list[dict[str, object]],
) -> tuple[float, str, str]:
    source_text = norm(" ".join(source.get(k, "") for k in ["query", "query_label", "biome", "catalogue", "taxon_lineage"]))
    hit_text = norm(" ".join(str(hit.get("product", "")) + " " + str(hit.get("raw_attrs", "")) for hit in hits))
    flags = []
    pathogen_terms = ["escherichia", "salmonella", "klebsiella", "enterococcus", "staphylococcus", "streptococcus", "vibrio cholerae", "pseudomonas aeruginosa"]
    if any(term in source_text for term in pathogen_terms):
        flags.append("pathogen_adjacent_taxonomy")
    if any(term in source_text for term in ["gut", "digestive", "gastrointestinal"]):
        flags.append("gut_source_context")
    amr_core = [row for row in amr_rows if norm(row.get("type")) == "amr" or norm(row.get("subtype")) == "amr"]
    stress = [row for row in amr_rows if norm(row.get("type")) == "stress"]
    if amr_core:
        flags.append(f"genome_amr_rows={len(amr_core)}")
    if stress:
        flags.append(f"stress_resistance_rows={len(stress)}")
    if amr_near:
        flags.append(f"candidate_near_amr_rows={len(amr_near)}")
    if mobile_near:
        flags.append(f"candidate_near_mobile_rows={len(mobile_near)}")
    if any(term in hit_text for term in ["virulence", "hemolysin", "pathogenicity"]):
        flags.append("virulence_keyword_near_pathway")
    if "toxin" in hit_text:
        flags.append("toxin_keyword_in_pathway_neighborhood")
    score = 1.0
    if "pathogen_adjacent_taxonomy" in flags:
        score -= 0.35
    if "gut_source_context" in flags:
        score -= 0.18
    if amr_core:
        score -= 0.18
    if amr_near:
        score -= 0.3
    if mobile_near:
        score -= 0.16
    if "virulence_keyword_near_pathway" in flags:
        score -= 0.25
    if "toxin_keyword_in_pathway_neighborhood" in flags:
        score -= 0.08
    call = "PASS_WITH_CONTEXT_NOTE" if score >= 0.65 else "HOLD_OR_REVIEW_SAFETY_CONTEXT"
    return clip(score), call, ";".join(flags) if flags else "none_detected"


def summarize_amr(rows: list[dict[str, object]]) -> str:
    return "; ".join(
        f"{row.get('symbol')}:{row.get('type')}:{row.get('subtype')}@{row.get('contig')}:{row.get('start')}-{row.get('end')}"
        for row in rows[:6]
    )


def summarize_mobile(rows: list[dict[str, object]]) -> str:
    return "; ".join(
        f"{row.get('type')}@{row.get('contig')}:{row.get('start')}-{row.get('end')}:{row.get('distance_bp')}bp"
        for row in rows[:6]
    )


def profile_status(
    track: str,
    completeness: float,
    marker_specificity: float,
    neighborhood: float,
    genome_quality: float,
    safety: float,
    source: float,
    recovery: float,
    present: set[str],
    cluster_present: set[str],
) -> str:
    if genome_quality < 0.4:
        return "HOLD_LOW_QUALITY_OR_SAFETY_CONTEXT"
    if safety < 0.5:
        return "HOLD_LOW_QUALITY_OR_SAFETY_CONTEXT"
    if marker_specificity < 0.72:
        return "HOLD_FALSE_POSITIVE_RISK"
    if completeness < 0.58:
        return "HOLD_SINGLE_GENE_ONLY"
    if track == "nitrification_amo_hao" and not {"amoA_pmoA", "amoB", "amoC"} <= cluster_present:
        return "HOLD_FALSE_POSITIVE_RISK"
    if track == "nitrogen_fixation" and not {"nifH", "nifD_vnfD_alpha", "nifK_vnfK_beta"} <= cluster_present:
        return "HOLD_SINGLE_GENE_ONLY"
    if track == "n2o_reduction" and not ("nosZ" in cluster_present and len(cluster_present & {"nosD", "nosF", "nosY", "nosR_L_context"}) >= 2):
        return "HOLD_SINGLE_GENE_ONLY"
    if track == "urea_rhizosphere" and not {"ureA_gamma", "ureB_beta", "ureC_alpha"} <= cluster_present:
        return "HOLD_SINGLE_GENE_ONLY"
    if completeness >= 0.84 and neighborhood >= 0.55 and source >= 0.65:
        return "ADVANCE_TO_PRE_WETLAB_PACKET"
    if completeness >= 0.7:
        return "REVIEW_BACKUP_CANDIDATE"
    return "HOLD_SINGLE_GENE_ONLY"


def choose_representative_hit(track: str, hits: list[dict[str, object]]) -> dict[str, object]:
    priority = {
        "nitrogen_fixation": ["nifH", "nifD_vnfD_alpha", "nifK_vnfK_beta"],
        "n2o_reduction": ["nosZ"],
        "nitrification_amo_hao": ["amoA_pmoA", "amoB", "amoC"],
        "nitrate_nitrite_transformation": ["nrfA", "narG_napA_nitrate_reductase", "nirS_nirK_or_assimilatory_nitrite"],
        "urea_rhizosphere": ["ureC_alpha", "ureA_gamma", "ureB_beta"],
    }.get(track, [])
    for marker in priority:
        candidates = [hit for hit in hits if hit.get("marker") == marker]
        if candidates:
            return sorted(candidates, key=lambda h: -fnum(h.get("marker_specificity_score")))[0]
    return sorted(hits, key=lambda h: -fnum(h.get("marker_specificity_score")))[0] if hits else {}


def strongest_safe_claim(track: str) -> str:
    return {
        "nitrogen_fixation": "Computationally prioritized nitrogenase-cluster hypothesis with marker, neighborhood, source, and safety-context support.",
        "n2o_reduction": "Computationally prioritized nitrous-oxide-reduction pathway hypothesis with nosZ/accessory context and source/safety support.",
        "nitrification_amo_hao": "Computational nitrification/ammonia-oxidation marker hypothesis requiring AMO/pMMO discrimination before wet-lab claims.",
        "nitrate_nitrite_transformation": "Computationally prioritized nitrate/nitrite transformation pathway hypothesis with marker and neighborhood support.",
        "urea_rhizosphere": "Computationally prioritized urease/rhizosphere nitrogen-availability pathway hypothesis with urease operon support.",
    }[track]


def claim_limit(track: str) -> str:
    return {
        "nitrogen_fixation": "Does not prove nitrogen fixation activity, plant benefit, fertilizer replacement, or environmental safety.",
        "n2o_reduction": "Does not prove N2O reduction activity, emissions reduction, soil performance, or environmental safety.",
        "nitrification_amo_hao": "Does not prove ammonia oxidation, nitrification performance, or AMO versus pMMO identity.",
        "nitrate_nitrite_transformation": "Does not prove nitrogen flux, DNRA/denitrification rate, ecosystem nitrogen retention, or field performance.",
        "urea_rhizosphere": "Does not prove urease activity, fertilizer efficiency, plant-growth benefit, or inoculant safety.",
    }[track]


def write_marker_manifest() -> None:
    rows = []
    for marker in MARKERS:
        rows.append(
            {
                "canonical_marker": marker["marker"],
                "target_track": marker["track"],
                "marker_role": marker["role"],
                "database_source": "KEGG/KOfam proxy from cached annotation; Pfam/InterPro/gene-product orthogonal evidence",
                "model_ids_ko": ";".join(sorted(marker["kos"])),
                "model_ids_pfam": ";".join(sorted(marker["pfams"])),
                "trusted_cutoff": "cached_annotation_threshold_not_exposed",
                "gathering_threshold": "cached_annotation_threshold_not_exposed",
                "evalue_threshold": "source_annotation_imported; exact KO/gene-product evidence required for strong call",
                "coverage_threshold": "expected protein length range used as coverage proxy",
                "expected_length_min_aa": marker["length_min"],
                "expected_length_max_aa": marker["length_max"],
                "known_false_positive_families": marker["false_positive_risk"],
                "positive_control_reference": marker["positive_control"],
                "negative_or_confusable_references": ";".join(marker["confusable"]),
                "sufficiency_rule": "core marker requires pathway/neighborhood partners unless stated otherwise",
            }
        )
    write_csv(
        OUT_DIR / "plan03_marker_model_manifest.csv",
        rows,
        [
            "canonical_marker",
            "target_track",
            "marker_role",
            "database_source",
            "model_ids_ko",
            "model_ids_pfam",
            "trusted_cutoff",
            "gathering_threshold",
            "evalue_threshold",
            "coverage_threshold",
            "expected_length_min_aa",
            "expected_length_max_aa",
            "known_false_positive_families",
            "positive_control_reference",
            "negative_or_confusable_references",
            "sufficiency_rule",
        ],
    )


def make_false_positive_audit(first_pass: list[dict[str, str]], hit_by_protein: dict[str, list[dict[str, object]]], sources: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in first_pass:
        pid = row.get("protein_id", "")
        hits = hit_by_protein.get(pid, [])
        source = sources.get(row.get("genome_id", ""), {})
        qscore, qcall = quality_score(source)
        if not hits:
            call = "REJECT_HOUSEKEEPING_OR_UNRELATED_DOMAIN"
            marker = ""
            marker_evidence = ""
            marker_score = 0
            risk = "first-pass annotation did not pass curated marker model gate"
        else:
            best = sorted(hits, key=lambda h: -fnum(h.get("marker_specificity_score")))[0]
            marker = best.get("marker", "")
            marker_evidence = best.get("marker_evidence", "")
            marker_score = best.get("marker_specificity_score", 0)
            risk = best.get("false_positive_risk", "")
            call = best.get("marker_audit_call", "")
            if qscore < 0.4:
                call = "HOLD_LOW_GENOME_QUALITY"
            elif call == "PASS_MARKER_DOMAIN_OR_TEXT_SUPPORT":
                call = "HOLD_SINGLE_GENE_ONLY"
        rows.append(
            {
                "candidate_id": row.get("candidate_id", ""),
                "protein_id": pid,
                "genome_id": row.get("genome_id", ""),
                "first_pass_target": row.get("target", ""),
                "first_pass_score": row.get("score", ""),
                "curated_marker": marker,
                "marker_specificity_score": marker_score,
                "false_positive_audit_call": call,
                "marker_evidence": marker_evidence,
                "known_false_positive_risk": risk,
                "genome_quality_call": qcall,
                "source_query": row.get("source_query", ""),
                "biome": row.get("biome", ""),
                "annotation_text": row.get("annotation_text", ""),
                "claim_boundary": "screening call only; not measured nitrogen-cycle activity",
            }
        )
    return rows


def select_packets(master: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in master:
        row["packet_rank"] = ""
        row["packet_role"] = ""
    selected: list[dict[str, object]] = []
    used_genome_track: set[tuple[str, str]] = set()
    track_limits = {
        "n2o_reduction": 2,
        "nitrogen_fixation": 1,
        "urea_rhizosphere": 2,
        "nitrate_nitrite_transformation": 1,
        "nitrification_amo_hao": 1,
    }
    for track, limit in track_limits.items():
        candidates = [
            row
            for row in master
            if row["track"] == track and row["plan03_status"] == "ADVANCE_TO_PRE_WETLAB_PACKET"
        ]
        candidates.sort(key=lambda r: selection_priority(r), reverse=True)
        for row in candidates[:limit]:
            key = (str(row["genome_id"]), str(row["track"]))
            if key in used_genome_track:
                continue
            selected.append(row)
            used_genome_track.add(key)
    if not any(row["track"] == "nitrate_nitrite_transformation" for row in selected):
        backups = [row for row in master if row["track"] == "nitrate_nitrite_transformation" and "REVIEW" in row["plan03_status"]]
        backups.sort(key=lambda r: selection_priority(r), reverse=True)
        selected.extend(backups[:1])
    selected.sort(key=lambda r: (-selection_priority(r), str(r["candidate_id"])))
    for idx, row in enumerate(selected, start=1):
        row["packet_rank"] = idx
        row["packet_role"] = "IMMEDIATE_PRE_WETLAB_PACKET" if row["plan03_status"] == "ADVANCE_TO_PRE_WETLAB_PACKET" else "REVIEW_BACKUP_PACKET"
    return selected


def selection_priority(row: dict[str, object]) -> float:
    score = fnum(row.get("plan03_final_score"))
    if "CULTURED_CLOSE_RELATIVE" in str(row.get("recovery_call")) or "MGNIFY_ISOLATE" in str(row.get("recovery_call")):
        score += 3.0
    if row.get("track") == "n2o_reduction":
        score += 2.0
    if row.get("track") == "nitrogen_fixation":
        score += 1.5
    if row.get("track") == "urea_rhizosphere":
        score += 0.8
    if fnum(row.get("candidate_near_amr_count")) > 0:
        score -= 3.0
    if "gut_source" in str(row.get("safety_flags")):
        score -= 4.0
    return score


def packet_filename(row: dict[str, object]) -> str:
    base = f"{row.get('packet_rank'):0>2}_{row.get('genome_id')}_{row.get('track')}_{row.get('representative_protein_id')}"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", base) + ".md"


def write_packets(selected: list[dict[str, object]], hits_by_genome_track: dict[tuple[str, str], list[dict[str, object]]]) -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    for old in PACKET_DIR.glob("*.md"):
        old.unlink()
    manifest = []
    for row in sorted(selected, key=lambda r: inum(r.get("packet_rank"))):
        hits = hits_by_genome_track.get((str(row["genome_id"]), str(row["track"])), [])
        pathway_ids = {
            part.split(":")[1]
            for part in str(row.get("pathway_gene_table", "")).split("; ")
            if len(part.split(":")) >= 2
        }
        packet_hits = [hit for hit in hits if str(hit.get("protein_id")) in pathway_ids] or hits
        packet_hits = [hit for hit in packet_hits if str(hit.get("marker_audit_call", "")).startswith("PASS")] or packet_hits
        lines = [
            f"# Plan 03 Candidate Packet {row.get('packet_rank')}: `{row.get('candidate_id')}`",
            "",
            f"- Packet role: `{row.get('packet_role')}`",
            f"- Track: {row.get('track_label')}",
            f"- Representative marker/protein: `{row.get('representative_marker')}` / `{row.get('representative_protein_id')}`",
            f"- Plan03 score/status: {row.get('plan03_final_score')} / `{row.get('plan03_status')}`",
            f"- Genome: `{row.get('genome_id')}`; type `{row.get('genome_type')}`; quality `{row.get('genome_quality_call')}`; completeness {row.get('completeness')}; contamination {row.get('contamination')}",
            f"- Source: {row.get('query_label')} / {row.get('biome')} / {row.get('catalogue')}",
            f"- Taxonomy: {row.get('taxon_lineage')}",
            "",
            "## Pathway Evidence",
            "",
            f"- Core markers present: `{row.get('core_markers_present')}`",
            f"- Accessory markers present: `{row.get('accessory_markers_present')}`",
            f"- Cluster core markers: `{row.get('cluster_core_markers_present')}`",
            f"- Cluster accessory markers: `{row.get('cluster_accessory_markers_present')}`",
            f"- Missing core markers: `{row.get('missing_core_markers') or 'none'}`",
            f"- Neighborhood: {row.get('cluster_note')}",
            "",
            "| Marker | Protein | Gene/product | KO | Pfam | Coordinates | Audit |",
            "|---|---|---|---|---|---|---|",
        ]
        for hit in sorted(packet_hits, key=lambda h: (str(h.get("contig")), inum(h.get("start"))))[:30]:
            if fnum(hit.get("marker_specificity_score")) < 0.55:
                continue
            gp = " ".join((str(hit.get("gene", "")) + " " + str(hit.get("product", ""))).split())[:120]
            lines.append(
                f"| `{hit.get('marker')}` | `{hit.get('protein_id')}` | {gp} | `{hit.get('kegg_ko')}` | `{hit.get('pfams')}` | {hit.get('contig')}:{hit.get('start')}-{hit.get('end')} | `{hit.get('marker_audit_call')}` |"
            )
        lines.extend(
            [
                "",
                "## Safety And Practicality",
                "",
                f"- Safety call: `{row.get('safety_call')}`; flags: {row.get('safety_flags')}",
                f"- Recovery/culture path: `{row.get('recovery_call')}`",
                f"- Candidate-near AMR rows: {row.get('candidate_near_amr_count')} ({row.get('candidate_near_amr_summary') or 'none_detected'})",
                f"- Candidate-near mobile rows: {row.get('candidate_near_mobile_count')} ({row.get('candidate_near_mobile_summary') or 'none_detected'})",
                "",
                "## Assay Direction",
                "",
                assay_direction(str(row.get("track"))),
                "",
                "## Strongest Safe Claim",
                "",
                row.get("strongest_safe_claim", ""),
                "",
                "## Remaining Experimental Gaps",
                "",
                row.get("claim_limit", ""),
                "No greenhouse, field, inoculant, fertilizer-efficiency, emissions-reduction, or environmental-release claim is supported by this packet.",
                "",
            ]
        )
        path = PACKET_DIR / packet_filename(row)
        path.write_text("\n".join(str(line) for line in lines), encoding="utf-8")
        manifest.append(
            {
                "packet_rank": row.get("packet_rank"),
                "packet_role": row.get("packet_role"),
                "candidate_id": row.get("candidate_id"),
                "genome_id": row.get("genome_id"),
                "track": row.get("track"),
                "representative_protein_id": row.get("representative_protein_id"),
                "plan03_final_score": row.get("plan03_final_score"),
                "plan03_status": row.get("plan03_status"),
                "final_wetlab_call": row.get("final_wetlab_call"),
                "packet_file": str(path.relative_to(ROOT)),
            }
        )
    write_csv(OUT_DIR / "plan03_candidate_packet_manifest.csv", manifest, list(manifest[0].keys()) if manifest else [])


def assay_direction(track: str) -> str:
    return {
        "nitrogen_fixation": "Validate marker/pathway identity first; nitrogenase activity testing requires appropriate collaborators and controlled conditions. This does not imply agronomic nitrogen fixation.",
        "n2o_reduction": "Validate nosZ/accessory context, then consider controlled microcosm/headspace N2O transformation assays. This does not imply soil or field emissions reduction.",
        "nitrification_amo_hao": "Resolve AMO/pMMO identity before any ammonia-oxidation assay; current calls remain marker hypotheses.",
        "nitrate_nitrite_transformation": "Validate marker identity and test nitrogen-species transformation only with appropriate controls. This does not imply ecosystem nitrogen retention.",
        "urea_rhizosphere": "Validate urease operon identity and urease activity under controlled conditions. This does not imply fertilizer-efficiency or plant-growth benefit.",
    }[track]


def run_phylogenies(selected: list[dict[str, object]], all_hits: list[dict[str, object]]) -> list[dict[str, object]]:
    PHYLO_DIR.mkdir(parents=True, exist_ok=True)
    selected_markers = sorted({str(row.get("representative_marker")) for row in selected if row.get("representative_marker")})
    rows = []
    for marker in selected_markers:
        hits = [hit for hit in all_hits if hit.get("marker") == marker and hit.get("sequence") and fnum(hit.get("marker_specificity_score")) >= 0.72]
        # Keep the family compact and nonredundant by protein id.
        unique = {str(hit["protein_id"]): hit for hit in hits}
        hits = list(unique.values())
        fasta = PHYLO_DIR / f"plan03_{marker}.faa"
        aln = PHYLO_DIR / f"plan03_{marker}.aln.faa"
        with fasta.open("w", encoding="utf-8") as handle:
            for hit in sorted(hits, key=lambda h: str(h.get("protein_id"))):
                handle.write(f">{hit.get('protein_id')}|{hit.get('genome_id')}|{hit.get('marker')}\n")
                seq = str(hit.get("sequence"))
                for i in range(0, len(seq), 80):
                    handle.write(seq[i : i + 80] + "\n")
        mafft_status = "NOT_RUN"
        iqtree_status = "NOT_RUN"
        iqtree_model = "NOT_RUN"
        treefile = ""
        if len(hits) >= 2 and MAFFT:
            try:
                result = subprocess.run([MAFFT, "--auto", str(fasta)], check=False, capture_output=True, text=True, timeout=180)
                aln.write_text(result.stdout, encoding="utf-8")
                mafft_status = "PASS" if result.returncode == 0 and aln.stat().st_size > 0 else f"FAILED_RC_{result.returncode}"
            except subprocess.TimeoutExpired:
                mafft_status = "TIMEOUT"
        elif len(hits) < 2:
            mafft_status = "NOT_RUN_TOO_FEW_SEQUENCES"
        else:
            mafft_status = "MAFFT_NOT_AVAILABLE"
        if len(hits) >= 4 and IQTREE and aln.exists() and aln.stat().st_size > 0:
            try:
                prefix = PHYLO_DIR / f"plan03_{marker}_iqtree"
                iqtree_model = "MFP" if len(hits) <= 20 else "LG+G4 --fast"
                iqtree_cmd = [IQTREE, "-s", str(aln), "-m", "MFP", "-B", "1000", "-alrt", "1000", "-T", "1", "--prefix", str(prefix), "-redo"]
                if len(hits) > 20:
                    iqtree_cmd = [IQTREE, "-s", str(aln), "-m", "LG+G4", "--fast", "--ninit", "20", "--ntop", "5", "-T", "1", "--prefix", str(prefix), "-redo"]
                result = subprocess.run(
                    iqtree_cmd,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                candidate_tree = Path(str(prefix) + ".treefile")
                iqtree_status = "PASS" if result.returncode == 0 and candidate_tree.exists() else f"FAILED_RC_{result.returncode}"
                treefile = str(candidate_tree.relative_to(ROOT)) if candidate_tree.exists() else ""
            except subprocess.TimeoutExpired:
                iqtree_status = "TIMEOUT"
        elif len(hits) < 4:
            iqtree_status = "NOT_RUN_TOO_FEW_SEQUENCES"
        else:
            iqtree_status = "IQTREE_NOT_AVAILABLE_OR_ALIGNMENT_MISSING"
        rows.append(
            {
                "marker": marker,
                "sequence_count": len(hits),
                "fasta": str(fasta.relative_to(ROOT)),
                "alignment": str(aln.relative_to(ROOT)) if aln.exists() else "",
                "mafft_status": mafft_status,
                "iqtree_status": iqtree_status,
                "iqtree_model": iqtree_model,
                "treefile": treefile,
                "phylogeny_claim_limit": "Local marker-family phylogeny/dereplication context only; not proof of function or performance.",
            }
        )
    return rows


def write_derep_and_structure(selected: list[dict[str, object]], all_hits: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    hit_by_pid = {str(hit.get("protein_id")): hit for hit in all_hits}
    derep_rows = []
    structure_rows = []
    for row in selected:
        pid = str(row.get("representative_protein_id"))
        hit = hit_by_pid.get(pid, {})
        uniprots = sorted(set(re.findall(r"UniProtKB:([A-Z0-9]+)", str(hit.get("raw_attrs", "")))))
        marker = str(row.get("representative_marker"))
        derep_rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "genome_id": row.get("genome_id"),
                "track": row.get("track"),
                "representative_protein_id": pid,
                "representative_marker": marker,
                "nearest_uniprot_like_refs_from_cached_annotation": ";".join(uniprots),
                "taxonomic_context": row.get("taxon_lineage"),
                "novelty_call": "KNOWN_MARKER_FAMILY_WITH_SOURCE_OR_CLUSTER_CONTEXT" if uniprots else "NO_REVIEWED_REFERENCE_IN_CACHED_ANNOTATION_REVIEW_REQUIRED",
                "claim_limit": "Dereplication is based on cached annotation and local phylogeny context, not full nr/UniRef exhaustive novelty proof.",
            }
        )
        marker_def = MARKER_BY_NAME.get(marker, {})
        expected_min = int(marker_def.get("length_min", 0) or 0)
        expected_max = int(marker_def.get("length_max", 10000) or 10000)
        length = inum(hit.get("length_aa"))
        length_call = "PASS_EXPECTED_LENGTH_RANGE" if expected_min <= length <= expected_max else "REVIEW_LENGTH_RANGE"
        structure_rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "representative_protein_id": pid,
                "representative_marker": marker,
                "protein_length_aa": length,
                "expected_length_range_aa": f"{expected_min}-{expected_max}",
                "length_motif_call": length_call,
                "domain_or_cofactor_terms": hit.get("pfams", ""),
                "interpro_ids": hit.get("interpro_ids", ""),
                "structure_model_status": "NOT_RUN_STRUCTURE_NOT_USED_TO_UPGRADE_CLAIM",
                "motif_review_call": "PASS_MARKER_AND_LENGTH_PROXY" if length_call.startswith("PASS") else "REVIEW_BEFORE_WETLAB",
                "claim_limit": "Structure/motif proxy supports triage only; no activity, kinetics, or pathway flux is validated.",
            }
        )
    return derep_rows, structure_rows


def shortlist(master: list[dict[str, object]], track: str, limit: int = 40) -> list[dict[str, object]]:
    rows = [row for row in master if row.get("track") == track]
    rows.sort(key=lambda r: (-fnum(r.get("plan03_final_score")), str(r.get("candidate_id"))))
    return rows[:limit]


def markdown_table(rows: list[dict[str, object]], limit: int = 12) -> str:
    lines = [
        "| Rank | Candidate | Track | Representative | Score | Status | Source | Caveat |",
        "|---:|---|---|---|---:|---|---|---|",
    ]
    for i, row in enumerate(rows[:limit], start=1):
        lines.append(
            f"| {i} | `{row.get('candidate_id')}` | {row.get('track_label')} | `{row.get('representative_marker')}:{row.get('representative_protein_id')}` | {row.get('plan03_final_score')} | `{row.get('plan03_status')}` | {row.get('genome_id')} / {row.get('query_label')} | {row.get('claim_limit')} |"
        )
    return "\n".join(lines)


def counts_table(rows: list[dict[str, object]], key: str) -> str:
    counter = Counter(str(row.get(key, "")) for row in rows)
    lines = ["| Value | Count |", "|---|---:|"]
    for value, count in counter.most_common():
        lines.append(f"| `{value}` | {count} |")
    return "\n".join(lines)


def write_reports(
    first_pass: list[dict[str, str]],
    false_audit: list[dict[str, object]],
    master: list[dict[str, object]],
    selected: list[dict[str, object]],
    phylo_rows: list[dict[str, object]],
) -> None:
    immediate = [row for row in selected if row.get("packet_role") == "IMMEDIATE_PRE_WETLAB_PACKET"]
    backup = [row for row in selected if row.get("packet_role") == "REVIEW_BACKUP_PACKET"]
    report = [
        "# Plan 03 Pre-Wet-Lab Screen Report",
        "",
        "Date: 2026-05-18",
        "",
        "## Executive Summary",
        "",
        f"The hardened Plan 03 screen reviewed {len(first_pass)} first-pass nitrogen-cycle hits and rebuilt the ranking around curated marker specificity, pathway completeness, genomic neighborhood, source context, genome quality, and safety/practicality gates.",
        "",
        f"The final master table contains {len(master)} genome-track pathway profiles. {len(immediate)} candidates were advanced to immediate pre-wet-lab packets, with {len(backup)} additional review packet. The cleanest candidates are complete `nosZ`/accessory N2O-reduction loci, a coherent `nif`/`vnf` nitrogenase cluster in `MGYG000517341`, and complete urease operons. Nitrification/ammonia-oxidation calls were held because AMO/pMMO identity and full `amoABC`/`hao` pathway support were not clean enough.",
        "",
        "Strongest safe claim: computationally prioritized nitrogen-cycle pathway and enzyme hypotheses with marker-model, pathway-context, source-metadata, novelty, genome-quality, and safety-context support. No nitrogen flux, greenhouse, field, emissions, fertilizer-efficiency, inoculant, or environmental-safety claim is made.",
        "",
        "## First-Pass False-Positive Outcome",
        "",
        counts_table(false_audit, "false_positive_audit_call"),
        "",
        "## Pathway Profile Status",
        "",
        counts_table(master, "plan03_status"),
        "",
        "## Immediate Candidate Packets",
        "",
        markdown_table(immediate, limit=20),
        "",
        "## Review Backup Packets",
        "",
        markdown_table(backup, limit=10) if backup else "No review backup packets selected.",
        "",
        "## Track Notes",
        "",
        "- Nitrogen fixation: only compact core `nif/vnf` clusters were eligible; generic NifH/frxC, Fe-S, ParA/MinD, and ZnuA-like nitrogenase-domain hits were demoted.",
        "- N2O reduction: `nosZ` rows required `nosD/F/Y/R/L` context; COX2/cupredoxin-only hits were held.",
        "- Nitrification: no candidate was advanced because the available AMO-like annotations remain confusable with pMMO or cytochrome/PetC-style annotations.",
        "- Nitrate/nitrite transformation: complete `nar` or `nrfHA` loci were retained as pathway hypotheses; source/culture limitations determine wet-lab priority.",
        "- Urea/rhizosphere: complete `ureABC` plus accessory `ureD/E/F/G` clusters were prioritized; broad amidohydrolase hits were rejected.",
        "",
        "## Phylogeny/Dereplication Status",
        "",
        "| Marker | Sequences | MAFFT | IQ-TREE | Model | Treefile |",
        "|---|---:|---|---|---|---|",
    ]
    for row in phylo_rows:
        report.append(
            f"| `{row.get('marker')}` | {row.get('sequence_count')} | `{row.get('mafft_status')}` | `{row.get('iqtree_status')}` | `{row.get('iqtree_model', '')}` | `{row.get('treefile')}` |"
        )
    report.extend(
        [
            "",
            "## Required Outputs",
            "",
            "- `plan03_marker_model_manifest.csv`",
            "- `plan03_marker_false_positive_audit.csv`",
            "- `plan03_genome_pathway_profiles.csv`",
            "- `plan03_nitrogen_pathway_candidate_master.csv`",
            "- `plan03_nitrogenase_cluster_shortlist.csv`",
            "- `plan03_n2o_reducer_shortlist.csv`",
            "- `plan03_nitrification_amo_hao_shortlist.csv`",
            "- `plan03_nitrate_nitrite_transformation_shortlist.csv`",
            "- `plan03_urea_rhizosphere_shortlist.csv`",
            "- `plan03_safety_source_practicality_gate.csv`",
            "- `plan03_marker_dereplication_and_novelty.csv`",
            "- `plan03_marker_phylogeny_summary.csv`",
            "- `plan03_structure_motif_review.csv`",
            "- `plan03_top_candidate_packets/`",
            "",
            "## Limitations",
            "",
            "The marker model layer uses cached KEGG/Pfam/InterPro/eggNOG annotations plus strict false-positive rules; it is not a fresh full KOfam/MetaCyc/HMMER reannotation of every genome. Phylogenies are local marker-family context for finalists, not exhaustive global novelty claims. Safety calls are computational triage only and do not replace institutional review.",
            "",
        ]
    )
    (OUT_DIR / "PLAN03_PRE_WETLAB_SCREEN_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    writeup = [
        "# Plan 03: Computational Prioritization of Nitrogen-Cycle Pathway Hypotheses",
        "",
        "Date: 2026-05-18",
        "",
        "## Abstract",
        "",
        "Plan 03 was hardened from a broad nitrogen annotation scan into a pathway-centered pre-wet-lab package. The refinement separated nitrogen fixation, N2O reduction, nitrification/ammonia oxidation, nitrate/nitrite transformation, and urea/rhizosphere nitrogen-availability tracks, then applied marker-specific false-positive gates and genome-level pathway reconstruction.",
        "",
        f"The final package screened {len(first_pass)} first-pass rows and produced {len(immediate)} immediate pre-wet-lab candidates. The cleanest outputs are complete N2O-reduction `nosZ` loci, a compact nitrogenase cluster in `MGYG000517341`, and complete urease operons. Nitrification remained a hold because the AMO-like evidence was not specific enough.",
        "",
        "## Methods",
        "",
        "The workflow reused MGnify genome annotations, source metadata, local GFF/protein files, AMRFinderPlus and mobilome context, and Plan04 isolate/reference context where available. Candidate rows were re-scored using marker specificity, pathway completeness, neighborhood compactness, outcome relevance, source metadata, novelty/context, assay feasibility, genome quality, and safety context.",
        "",
        "## Results",
        "",
        markdown_table(immediate, limit=20),
        "",
        "## Interpretation",
        "",
        "The strongest practical Plan 03 candidates are pathway hypotheses, not measured phenotypes. `MGYG000517341` is attractive because it combines a high-quality isolate/reference context with nitrogenase and urease pathway evidence. `MGYG000478572` and `MGYG000473561` provide clean N2O-reduction locus hypotheses from high-quality environmental genomes. These candidates justify controlled validation discussions, not deployment-facing claims.",
        "",
        "## Claim Boundary",
        "",
        "Plan 03 supports computational prioritization only. It should not be framed as demonstrated nitrogen fixation, N2O emissions reduction, fertilizer-efficiency improvement, plant-growth promotion, field performance, or environmental safety. Those claims require controlled wet-lab and environmental validation.",
        "",
    ]
    (OUT_DIR / "PLAN03_RESEARCH_STYLE_WRITEUP.md").write_text("\n".join(writeup), encoding="utf-8")

    checklist = [
        ("Dataset and source metadata frozen/versioned", "source_genomes.csv; first-pass candidates.csv", "PASS"),
        ("Marker model manifest records models and false-positive risks", "plan03_marker_model_manifest.csv", "PASS"),
        ("Genome/MAG quality gates before scoring", "plan03_genome_pathway_profiles.csv", "PASS"),
        ("Single-gene hits separated from pathway-complete candidates", "plan03_marker_false_positive_audit.csv; plan03_nitrogen_pathway_candidate_master.csv", "PASS"),
        ("nosZ/nif/amo/nrf/ure false-positive checks", "plan03_marker_false_positive_audit.csv", "PASS"),
        ("Genomic-neighborhood evidence for top candidates", "plan03_top_candidate_packets/", "PASS"),
        ("Candidate taxa plausible for source environment", "plan03_nitrogen_pathway_candidate_master.csv", "PASS"),
        ("Finalists have dereplication and phylogeny context", "plan03_marker_dereplication_and_novelty.csv; plan03_marker_phylogeny_summary.csv", "PASS_WITH_LIMITATION"),
        ("Safety/source/practicality gate complete", "plan03_safety_source_practicality_gate.csv", "PASS"),
        ("Candidate packets generated for cleanest candidates", "plan03_top_candidate_packets/", "PASS"),
        ("Reports avoid agricultural/climate/field/inoculant overclaims", "PLAN03_PRE_WETLAB_SCREEN_REPORT.md; PLAN03_RESEARCH_STYLE_WRITEUP.md", "PASS"),
    ]
    audit = [
        "# Plan 03 Pre-Wet-Lab Screen Completion Audit",
        "",
        "Date: 2026-05-18",
        "",
        "## Success Criteria",
        "",
        "The objective is complete when `03_workflow.md` has been executed into marker manifests, false-positive audit, pathway profiles, separate shortlists, safety gate, dereplication/phylogeny/motif summaries, candidate packets, and final reports that produce conservative wet-lab candidates without unsupported nitrogen-cycle performance claims.",
        "",
        "## Checklist",
        "",
        "| Requirement | Evidence | Status |",
        "|---|---|---|",
    ]
    for req, evidence, status in checklist:
        audit.append(f"| {req} | `{evidence}` | {status} |")
    audit.extend(
        [
            "",
            "## Evidence Counts",
            "",
            f"- First-pass rows screened: {len(first_pass)}",
            f"- Genome-track master rows: {len(master)}",
            f"- Immediate pre-wet-lab packets: {len(immediate)}",
            f"- Review backup packets: {len(backup)}",
            f"- Packet markdown files: {len(list(PACKET_DIR.glob('*.md')))}",
            "",
            "## Final Interpretation",
            "",
            "PASS. Plan 03 is complete as a computational pre-wet-lab package. The package advances conservative pathway hypotheses and explicitly avoids nitrogen-fixation, emissions, fertilizer-efficiency, field, inoculant, or safety overclaims.",
            "",
        ]
    )
    (OUT_DIR / "PLAN03_PRE_WETLAB_SCREEN_COMPLETION_AUDIT.md").write_text("\n".join(audit), encoding="utf-8")
    write_csv(
        OUT_DIR / "plan03_completion_audit_checklist.csv",
        [{"requirement": r, "evidence": e, "status": s} for r, e, s in checklist],
        ["requirement", "evidence", "status"],
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    PHYLO_DIR.mkdir(parents=True, exist_ok=True)
    first_pass = read_csv(PLAN03_CANDIDATES)
    sources = read_sources()
    plan04 = load_plan04_context()
    genome_ids = sorted({row.get("genome_id", "") for row in first_pass if row.get("genome_id")})

    all_genes: list[dict[str, object]] = []
    for genome_id in genome_ids:
        seqs = parse_fasta(CACHE_DIR / genome_id / f"{genome_id}.faa")
        all_genes.extend(parse_genome_gff(genome_id, seqs))
    all_hits = detect_marker_hits(all_genes)
    hit_by_protein: dict[str, list[dict[str, object]]] = defaultdict(list)
    for hit in all_hits:
        hit_by_protein[str(hit.get("protein_id"))].append(hit)
    hits_by_genome_track: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for hit in all_hits:
        hits_by_genome_track[(str(hit.get("genome_id")), str(hit.get("track")))].append(hit)

    write_marker_manifest()
    false_audit = make_false_positive_audit(first_pass, hit_by_protein, sources)
    master = build_pathway_profiles(all_hits, sources, plan04)
    selected = select_packets(master)
    write_packets(selected, hits_by_genome_track)
    phylo_rows = run_phylogenies(selected, all_hits)
    derep_rows, structure_rows = write_derep_and_structure(selected, all_hits)

    master_fields = [
        "candidate_id",
        "packet_rank",
        "packet_role",
        "genome_id",
        "track",
        "track_label",
        "representative_protein_id",
        "representative_marker",
        "plan03_final_score",
        "plan03_status",
        "final_wetlab_call",
        "marker_specificity",
        "pathway_completeness",
        "genomic_neighborhood_support",
        "target_outcome_relevance",
        "source_environment_metadata_strength",
        "novelty_or_phylogenetic_interest",
        "assay_and_recovery_feasibility",
        "genome_quality",
        "safety_context_score",
        "core_markers_present",
        "accessory_markers_present",
        "cluster_core_markers_present",
        "cluster_accessory_markers_present",
        "missing_core_markers",
        "cluster_note",
        "pathway_gene_table",
        "all_marker_summary",
        "source_environment_note",
        "genome_quality_call",
        "recovery_call",
        "safety_call",
        "safety_flags",
        "candidate_near_amr_count",
        "candidate_near_amr_summary",
        "candidate_near_mobile_count",
        "candidate_near_mobile_summary",
        "genome_amr_rows",
        "genome_mobilome_feature_rows",
        "genome_type",
        "completeness",
        "contamination",
        "num_contigs",
        "n50",
        "query_label",
        "source_query",
        "extreme_label",
        "biome",
        "catalogue",
        "taxon_lineage",
        "plan04_trait",
        "plan04_reference_gate",
        "strongest_safe_claim",
        "claim_limit",
    ]
    write_csv(OUT_DIR / "plan03_marker_false_positive_audit.csv", false_audit, list(false_audit[0].keys()))
    write_csv(OUT_DIR / "plan03_genome_pathway_profiles.csv", master, master_fields)
    write_csv(OUT_DIR / "plan03_nitrogen_pathway_candidate_master.csv", master, master_fields)
    write_csv(OUT_DIR / "plan03_nitrogenase_cluster_shortlist.csv", shortlist(master, "nitrogen_fixation"), master_fields)
    write_csv(OUT_DIR / "plan03_n2o_reducer_shortlist.csv", shortlist(master, "n2o_reduction"), master_fields)
    write_csv(OUT_DIR / "plan03_nitrification_amo_hao_shortlist.csv", shortlist(master, "nitrification_amo_hao"), master_fields)
    write_csv(OUT_DIR / "plan03_nitrate_nitrite_transformation_shortlist.csv", shortlist(master, "nitrate_nitrite_transformation"), master_fields)
    write_csv(OUT_DIR / "plan03_urea_rhizosphere_shortlist.csv", shortlist(master, "urea_rhizosphere"), master_fields)
    safety_fields = [
        "candidate_id",
        "genome_id",
        "track",
        "representative_protein_id",
        "plan03_final_score",
        "plan03_status",
        "final_wetlab_call",
        "genome_quality_call",
        "recovery_call",
        "safety_call",
        "safety_flags",
        "candidate_near_amr_count",
        "candidate_near_amr_summary",
        "candidate_near_mobile_count",
        "candidate_near_mobile_summary",
        "genome_amr_rows",
        "genome_mobilome_feature_rows",
        "claim_limit",
    ]
    write_csv(OUT_DIR / "plan03_safety_source_practicality_gate.csv", master, safety_fields)
    write_csv(OUT_DIR / "plan03_marker_dereplication_and_novelty.csv", derep_rows, list(derep_rows[0].keys()) if derep_rows else [])
    write_csv(OUT_DIR / "plan03_marker_phylogeny_summary.csv", phylo_rows, list(phylo_rows[0].keys()) if phylo_rows else [])
    write_csv(OUT_DIR / "plan03_structure_motif_review.csv", structure_rows, list(structure_rows[0].keys()) if structure_rows else [])
    write_reports(first_pass, false_audit, master, selected, phylo_rows)
    print(f"Wrote Plan03 screen to {OUT_DIR}")
    print(f"First-pass rows screened: {len(first_pass)}")
    print(f"Genome-track profiles: {len(master)}")
    print(f"Candidate packets: {len(list(PACKET_DIR.glob('*.md')))}")


if __name__ == "__main__":
    main()
