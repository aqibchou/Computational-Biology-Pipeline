#!/usr/bin/env python3
"""Plan08 pre-wet-lab biomaterials screen.

This script produces candidate-level prioritization artifacts only. It does not
emit gene sequences, construct designs, synthesis instructions, or material
performance claims.
"""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "outputs" / "computational_execution_2026-05-14"
PLAN08_INPUT = INPUT_DIR / "08_biosurfactants_biopolymers_and_biomaterials" / "candidates.csv"
SOURCE_GENOMES = INPUT_DIR / "source_genomes.csv"
CACHE_DIR = INPUT_DIR / "cache" / "mgnify_genomes"
PLAN01_BGC = ROOT / "outputs" / "plan01_strict_bgc_triage_2026-05-14" / "plan01_top_50_strict_bgc_queue.csv"
PLAN01_BIGSCAPE = (
    ROOT
    / "outputs"
    / "plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17"
    / "plan01_bigscape_full_mibig_closest_cross_source_pairs.csv"
)
PLAN04_FINALISTS = ROOT / "outputs" / "plan04_claim_hardening_2026-05-17" / "plan04_finalist_claim_hardening.csv"
PLAN04_ISOLATES = ROOT / "outputs" / "plan04_claim_hardening_2026-05-17" / "plan04_isolate_availability_triage.csv"
PLAN04_ANI = ROOT / "outputs" / "plan04_reference_ani_2026-05-17" / "plan04_reference_ani_results.csv"

OUT_DIR = ROOT / "outputs" / "plan08_pre_wetlab_screen_2026-05-18"
PACKET_DIR = OUT_DIR / "plan08_top_candidate_packets"


TRACKS = {
    "biosurfactant": "biosurfactant_bgc",
    "biosurfactant_bgc": "biosurfactant_bgc",
    "biopolymer": "biopolymer_eps",
    "exopolysaccharide": "biopolymer_eps",
    "adhesive_biofilm": "protein_materials",
    "metal_binding": "protein_materials",
    "self_assembling": "protein_materials",
    "melanin": "pigment_materials",
}

TRACK_LABELS = {
    "biosurfactant_bgc": "Biosurfactants / BGCs",
    "biopolymer_eps": "Biopolymers / EPS",
    "protein_materials": "Protein materials",
    "pigment_materials": "Pigments / functional materials",
}

PHA_TERMS = [
    "phac",
    "phar",
    "phasin",
    "polyhydroxy",
    "poly(3-hydroxy",
    "poly-beta-hydroxy",
    "polyhydroxyalkanoate",
    "hydroxyalkanoate",
    "phb_acc",
]
EPS_TERMS = [
    "exopolysaccharide",
    "capsular",
    "capsule",
    "wzc",
    "wzz",
    "gumd",
    "polyprenyl glycosylphosphotransferase",
    "glycosyltransferase",
    "colanic",
    "ybjh",
    "yjbh",
    "yjb",
    "exod",
    "alginate",
    "cellulose",
    "pul",
    "cazy",
]
PROTEIN_MATERIAL_TERMS = [
    "adhesin",
    "pily1",
    "pilc",
    "yada",
    "collagen-binding",
    "biofilm",
    "matrix",
    "curli",
    "fimbrial",
    "surface",
    "lipoprotein",
    "pep-cterm",
    "s-layer",
    "repeat",
    "coiled",
    "beta-propeller",
    "vwa",
    "serralysin",
    "metal-binding",
    "sec-c",
]
PIGMENT_TERMS = ["tyrosinase", "melanin", "polyphenol oxidase", "laccase", "copper-binding"]
TRUE_BIOSURFACTANT_TERMS = [
    "surfactin",
    "rhamnolipid",
    "rhamnosyltransferase",
    "lipopeptide",
    "glycolipid",
    "sophorolipid",
    "iturin",
    "fengycin",
    "lichenysin",
]
STRONG_DIRECT_BIOSURFACTANT_TERMS = [
    "surfactin",
    "rhamnolipid",
    "rhamnosyltransferase",
    "glycolipid",
    "sophorolipid",
    "iturin",
    "fengycin",
    "lichenysin",
]
HOUSEKEEPING_TERMS = [
    "lipid a",
    "lpx",
    "lipopolysaccharide",
    "ribosomal",
    "inositol monophosphatase",
    "nucleic-acid-binding",
    "rna subunit",
    "glucose-1-phosphate",
    "glmu",
    "tol-pal",
]
TOXIN_VIRULENCE_TERMS = ["toxin", "hemolysin", "virulence", "pathogenicity", "type iii secretion"]
PATHOGEN_CONTEXT_TERMS = [
    "escherichia",
    "salmonella",
    "klebsiella",
    "acinetobacter baumannii",
    "staphylococcus aureus",
    "streptococcus pyogenes",
    "enterococcus faecium",
    "vibrio cholerae",
    "pseudomonas aeruginosa",
]


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


def has_any(text: str, terms: list[str]) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def term_hits(text: str, terms: list[str]) -> list[str]:
    low = text.lower()
    return sorted({term for term in terms if term.lower() in low})


def parse_attrs(attr_text: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for part in attr_text.split(";"):
        if not part:
            continue
        if "=" in part:
            key, value = part.split("=", 1)
            attrs[key] = unquote(value)
    return attrs


def protein_number(protein_id: str) -> int | None:
    match = re.search(r"_(\d+)$", protein_id or "")
    if not match:
        return None
    return int(match.group(1))


def candidate_text(row: dict[str, str]) -> str:
    keys = [
        "target",
        "annotation_text",
        "evidence",
        "ec",
        "kegg_ko",
        "kegg_module",
        "cazy",
        "pfams",
        "interpro_ids",
        "product_class",
        "nearest_mibig",
        "context_text",
    ]
    return norm(" ".join(str(row.get(key, "")) for key in keys))


def track_for(row: dict[str, str]) -> str:
    return TRACKS.get(str(row.get("target", "")).lower(), "protein_materials")


def source_context_text(row: dict[str, str], source: dict[str, str]) -> str:
    keys = [
        "source_query",
        "query_label",
        "extreme_label",
        "biome",
        "catalogue",
        "taxon_lineage",
        "geographic_origin",
    ]
    return norm(" ".join(str(row.get(k, "") or source.get(k, "")) for k in keys))


def load_sources() -> dict[str, dict[str, str]]:
    return {row["genome_id"]: row for row in read_csv(SOURCE_GENOMES)}


def parse_gff_features(path: Path, wanted_types: set[str] | None = None) -> list[dict[str, object]]:
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
            ftype = parts[2]
            if wanted_types is not None and ftype not in wanted_types:
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
                    "type": ftype,
                    "start": start,
                    "end": end,
                    "strand": parts[6],
                    "attrs": attrs,
                    "raw_attrs": parts[8],
                }
            )
    return features


def load_gene_maps(genome_ids: set[str]) -> dict[str, dict[str, dict[str, object]]]:
    maps: dict[str, dict[str, dict[str, object]]] = {}
    for genome_id in sorted(genome_ids):
        path = CACHE_DIR / genome_id / f"{genome_id}.gff"
        gene_map: dict[str, dict[str, object]] = {}
        for feature in parse_gff_features(path, {"CDS"}):
            attrs = feature["attrs"]
            ids = [attrs.get("ID", ""), attrs.get("locus_tag", "")]
            for pid in ids:
                if pid:
                    gene_map[pid] = feature
        maps[genome_id] = gene_map
    return maps


def load_clusters(genome_ids: set[str]) -> dict[str, list[dict[str, object]]]:
    cluster_map: dict[str, list[dict[str, object]]] = {}
    for genome_id in sorted(genome_ids):
        genome_dir = CACHE_DIR / genome_id
        clusters: list[dict[str, object]] = []
        for suffix, source_name, types in [
            ("_antismash.gff", "antiSMASH", {"region"}),
            ("_gecco.gff", "GECCO", {"BGC"}),
            ("_sanntis.gff", "SanntiS", {"CLUSTER"}),
            ("_dbcan.gff", "dbCAN", {"predicted PUL"}),
        ]:
            for feature in parse_gff_features(genome_dir / f"{genome_id}{suffix}", types):
                attrs = feature["attrs"]
                product = (
                    attrs.get("product")
                    or attrs.get("Type")
                    or attrs.get("Name")
                    or attrs.get("nearest_MiBIG_class")
                    or attrs.get("substrate_dbcan-pul")
                    or attrs.get("substrate_dbcan-sub")
                    or ""
                )
                score = attrs.get("score") or attrs.get("ProbabilityAverage") or ""
                clusters.append(
                    {
                        "cluster_source": source_name,
                        "cluster_id": attrs.get("ID", ""),
                        "contig": feature["contig"],
                        "start": feature["start"],
                        "end": feature["end"],
                        "product": product,
                        "score": score,
                        "nearest_mibig": attrs.get("nearest_MiBIG", ""),
                        "nearest_mibig_class": attrs.get("nearest_MiBIG_class", ""),
                        "attrs": feature["raw_attrs"],
                    }
                )
        cluster_map[genome_id] = clusters
    return cluster_map


def load_mobilome(genome_ids: set[str]) -> dict[str, list[dict[str, object]]]:
    mobilome: dict[str, list[dict[str, object]]] = {}
    for genome_id in sorted(genome_ids):
        path = CACHE_DIR / genome_id / f"{genome_id}_mobilome.gff"
        features = parse_gff_features(path, None)
        mobilome[genome_id] = features
    return mobilome


def parse_amrfinder(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            low = line.lower()
            if low.startswith("protein identifier") or low.startswith("protein id"):
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
                    "symbol": parts[5] if len(parts) > 5 else "",
                    "element_name": parts[6] if len(parts) > 6 else "",
                    "scope": parts[7] if len(parts) > 7 else "",
                    "type": parts[8] if len(parts) > 8 else "",
                    "subtype": parts[9] if len(parts) > 9 else "",
                    "raw": line,
                }
            )
    return rows


def load_amr(genome_ids: set[str]) -> dict[str, list[dict[str, object]]]:
    return {
        genome_id: parse_amrfinder(CACHE_DIR / genome_id / f"{genome_id}_amrfinderplus.tsv")
        for genome_id in sorted(genome_ids)
    }


def distance_to_interval(start: int, end: int, other_start: int, other_end: int) -> int:
    if end < other_start:
        return other_start - end
    if other_end < start:
        return start - other_end
    return 0


def nearby_features(
    coords: dict[str, object] | None,
    features: list[dict[str, object]],
    window_bp: int,
) -> list[dict[str, object]]:
    if not coords:
        return []
    contig = str(coords.get("contig", ""))
    start = inum(coords.get("start"))
    end = inum(coords.get("end"))
    near = []
    for feature in features:
        if feature.get("contig") != contig:
            continue
        dist = distance_to_interval(start, end, inum(feature.get("start")), inum(feature.get("end")))
        if dist <= window_bp:
            row = dict(feature)
            row["distance_bp"] = dist
            near.append(row)
    return near


def overlapping_clusters(coords: dict[str, object] | None, clusters: list[dict[str, object]]) -> list[dict[str, object]]:
    return nearby_features(coords, clusters, 1000)


def quality_score(source: dict[str, str]) -> tuple[float, str]:
    comp = fnum(source.get("completeness"))
    contam = fnum(source.get("contamination"), 100.0)
    genome_type = source.get("type", "")
    if comp >= 95 and contam <= 2:
        base, call = 1.0, "HIGH_QUALITY"
    elif comp >= 90 and contam <= 5:
        base, call = 0.85, "GOOD_QUALITY"
    elif comp >= 80 and contam <= 5:
        base, call = 0.65, "MODERATE_QUALITY"
    elif comp >= 70 and contam <= 10:
        base, call = 0.45, "LOW_MODERATE_QUALITY"
    else:
        base, call = 0.25, "LOW_QUALITY_HOLD"
    if genome_type.lower() == "isolate" and base < 1.0:
        base = min(1.0, base + 0.08)
    return base, call


def source_score(track: str, source_text: str) -> tuple[float, str]:
    if any(word in source_text for word in ["gut", "digestive", "gastrointestinal"]):
        return 0.25, "HOST_GUT_CONTEXT_DEPRIORITIZED_FOR_MATERIAL_SCREEN"
    score = 0.45
    tags = []
    for term, tag in [
        ("marine", "marine"),
        ("sediment", "sediment"),
        ("saline", "saline"),
        ("hydrothermal", "hydrothermal"),
        ("desert", "desiccation"),
        ("polar", "cold"),
        ("soil", "soil"),
        ("rhizosphere", "rhizosphere"),
        ("oleiphil", "oil-associated taxonomy"),
        ("marinobacter", "marine hydrocarbon-associated genus"),
    ]:
        if term in source_text:
            tags.append(tag)
    if tags:
        score = 0.75
    if track == "biosurfactant_bgc" and any(tag in tags for tag in ["marine", "saline", "oil-associated taxonomy", "marine hydrocarbon-associated genus"]):
        score = 0.95
    elif track == "biopolymer_eps" and any(tag in tags for tag in ["marine", "saline", "rhizosphere", "desiccation", "soil"]):
        score = 0.9
    elif track == "protein_materials" and any(tag in tags for tag in ["marine", "saline", "rhizosphere", "soil", "sediment"]):
        score = 0.85
    elif track == "pigment_materials" and any(tag in tags for tag in ["rhizosphere", "desiccation", "soil", "marine", "saline"]):
        score = 0.8
    return score, ";".join(tags) if tags else "generic_environment_context"


def load_plan04_context() -> dict[str, dict[str, str]]:
    context: dict[str, dict[str, str]] = defaultdict(dict)
    for row in read_csv(PLAN04_FINALISTS):
        context[row.get("genome_id", "")].update(
            {
                "plan04_call": row.get("claim_hardening_call", ""),
                "plan04_score": row.get("claim_hardening_score", ""),
                "plan04_trait": row.get("primary_trait_label", ""),
                "plan04_safety_call": row.get("safety_call", ""),
            }
        )
    for row in read_csv(PLAN04_ISOLATES):
        context[row.get("genome_id", "")].update(
            {
                "availability_call": row.get("availability_call", ""),
                "cultured_relative_note": row.get("cultured_relative_note", ""),
                "surrogate_path": row.get("surrogate_path", ""),
            }
        )
    best_ani: dict[str, str] = {}
    for row in read_csv(PLAN04_ANI):
        genome_id = row.get("candidate_genome_id", "")
        gate = row.get("reference_gate_call", "")
        if genome_id and ("EXACT" in gate or genome_id not in best_ani):
            best_ani[genome_id] = gate
    for genome_id, gate in best_ani.items():
        context[genome_id]["plan04_reference_gate"] = gate
    return context


def recovery_score(source: dict[str, str], plan04: dict[str, str]) -> tuple[float, str]:
    genome_type = norm(source.get("type"))
    availability = plan04.get("availability_call", "")
    if "CULTURED_CLOSE_RELATIVE" in availability or "MGNIFY_ISOLATE" in availability:
        return 1.0, availability
    if genome_type == "isolate":
        return 0.85, "MGNIFY_ISOLATE_METADATA_ONLY"
    if "NO_CULTURED_CLOSE_RELATIVE" in availability:
        return 0.3, availability
    return 0.55, "MAG_OR_UNCONFIRMED_RECOVERY_ROUTE"


def material_subtype(row: dict[str, str], text: str, track: str) -> str:
    if track == "biosurfactant_bgc":
        product = norm(row.get("product_class"))
        if has_any(text, ["lipid a", "lpx", "lipopolysaccharide"]):
            return "lps_lipid_a_housekeeping"
        if "glycolipid-binding" in text or "glycolipid binding" in text:
            return "biosurfactant_like_uncertain"
        if has_any(text + " " + product, STRONG_DIRECT_BIOSURFACTANT_TERMS):
            return "direct_biosurfactant_term"
        if "nrp" in product or "nrps" in product or "nonribosomal" in text:
            return "nrp_lipopeptide_like_bgc_review"
        if "saccharide" in product or "glycolipid" in text:
            return "saccharide_glycolipid_like_bgc_review"
        if "hserlactone" in product:
            return "hserlactone_bgc_review"
        return "biosurfactant_like_uncertain"
    if track == "biopolymer_eps":
        if has_any(text, PHA_TERMS):
            return "pha_polyhydroxyalkanoate"
        if has_any(text, EPS_TERMS):
            return "eps_capsule_export"
        return "biopolymer_uncertain"
    if track == "protein_materials":
        if has_any(text, ["pily1", "pilc", "yada", "collagen-binding", "adhesin"]):
            return "surface_adhesive_protein"
        if "biofilm" in text:
            return "biofilm_matrix_or_regulator"
        if has_any(text, ["metal-binding", "sec-c", "zinc", "iron", "copper"]):
            return "metal_binding_surface_candidate"
        if has_any(text, ["repeat", "coiled", "beta-propeller"]):
            return "repeat_or_self_assembling_candidate"
        return "generic_protein_material_hit"
    if track == "pigment_materials":
        if has_any(text, PIGMENT_TERMS):
            return "tyrosinase_melanin_like"
        return "pigment_uncertain"
    return "unknown"


def locus_support(row: dict[str, str], indexed_by_genome_track: dict[tuple[str, str], list[dict[str, str]]]) -> int:
    pid = row.get("protein_id", "")
    pnum = protein_number(pid)
    if pnum is None:
        return 0
    genome_id = row.get("genome_id", "")
    track = track_for(row)
    count = 0
    for other in indexed_by_genome_track.get((genome_id, track), []):
        onum = protein_number(other.get("protein_id", ""))
        if onum is None:
            continue
        if abs(onum - pnum) <= 10:
            count += 1
    return count


def genome_material_counts(rows: list[dict[str, str]]) -> dict[str, Counter]:
    counts: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        text = candidate_text(row)
        genome_id = row.get("genome_id", "")
        if has_any(text, PHA_TERMS):
            counts[genome_id]["pha"] += 1
        if has_any(text, EPS_TERMS):
            counts[genome_id]["eps"] += 1
        if has_any(text, PIGMENT_TERMS):
            counts[genome_id]["pigment"] += 1
        if has_any(text, PROTEIN_MATERIAL_TERMS):
            counts[genome_id]["protein_material"] += 1
        if has_any(text, TRUE_BIOSURFACTANT_TERMS) or has_any(text, ["lipid a", "lpx", "lipopolysaccharide"]):
            counts[genome_id]["biosurfactant_like"] += 1
    return counts


def pathway_score(
    row: dict[str, str],
    text: str,
    track: str,
    subtype: str,
    locus_count: int,
    genome_counts: Counter,
    clusters: list[dict[str, object]],
) -> tuple[float, str]:
    cluster_text = norm(" ".join(str(c.get("product", "")) + " " + str(c.get("cluster_source", "")) for c in clusters))
    if track == "biosurfactant_bgc":
        product = norm(row.get("product_class"))
        if subtype == "lps_lipid_a_housekeeping":
            return 0.25, "lipid-A/LPS housekeeping signal, not a specific biosurfactant BGC"
        if "glycolipid-binding" in text or "glycolipid binding" in text:
            return 0.35, "glycolipid-binding protein annotation only; no production BGC support"
        if has_any(text + " " + product, STRONG_DIRECT_BIOSURFACTANT_TERMS):
            return 0.9, "direct biosurfactant-family term present"
        if "nrp" in product or "nrps" in product:
            return 0.68, "multi-tool NRP/NRPS BGC; lipopeptide chemistry unresolved"
        if "saccharide" in product:
            return 0.58, "saccharide BGC; glycolipid/EPS chemistry unresolved"
        if "hserlactone" in product:
            return 0.56, "hserlactone BGC; biosurfactant relevance unresolved"
        if "nrp" in cluster_text or "saccharide" in cluster_text:
            return 0.55, "nearby BGC context but product chemistry unresolved"
        return 0.35, "no coherent biosurfactant BGC support"

    if track == "biopolymer_eps":
        dbcan_overlap = any(c.get("cluster_source") == "dbCAN" for c in clusters)
        if subtype == "pha_polyhydroxyalkanoate":
            if "phac" in text and genome_counts["pha"] >= 3:
                return 0.95, "PhaC plus same-genome PHA/phasin/PhaR support"
            if "phac" in text:
                return 0.85, "PhaC polymerase family support"
            if "phasin" in text and genome_counts["pha"] >= 2:
                return 0.72, "phasin with same-genome PHA support"
            return 0.65, "PHA-family support but representative gene is not PhaC"
        if subtype == "eps_capsule_export":
            if locus_count >= 3 and dbcan_overlap:
                return 0.9, "EPS/capsule locus with dbCAN/PUL overlap"
            if has_any(text, ["wzc", "wzz", "gumd", "polyprenyl glycosylphosphotransferase"]):
                return 0.82, "core EPS/capsule export or initiation gene"
            if locus_count >= 3:
                return 0.75, "multi-gene EPS/capsule neighborhood"
            return 0.6, "isolated EPS annotation"
        return 0.45, "weak biopolymer specificity"

    if track == "protein_materials":
        if subtype == "surface_adhesive_protein":
            return 0.86, "surface adhesin/domain architecture support"
        if subtype == "biofilm_matrix_or_regulator":
            return 0.62, "biofilm regulator/matrix association, property indirect"
        if subtype == "metal_binding_surface_candidate" and has_any(text, ["surface", "lipoprotein", "periplasmic", "sec-c"]):
            return 0.6, "metal-binding protein with surface/periplasmic context"
        if subtype == "repeat_or_self_assembling_candidate" and not has_any(text, HOUSEKEEPING_TERMS):
            return 0.58, "repeat/self-assembly proxy without direct material validation"
        return 0.32, "generic metal/self-assembling annotation"

    if track == "pigment_materials":
        if has_any(text, ["tyrosinase", "melanin"]):
            if clusters:
                return 0.86, "tyrosinase/melanin-like hit with local BGC/context overlap"
            return 0.78, "tyrosinase/melanin-like hit"
        return 0.45, "weak pigment specificity"

    return 0.4, "track-specific pathway support not available"


def application_score(text: str, track: str, subtype: str) -> tuple[float, str]:
    if track == "biosurfactant_bgc":
        if subtype == "direct_biosurfactant_term":
            return 0.9, "direct biosurfactant material hypothesis"
        if subtype in {"nrp_lipopeptide_like_bgc_review", "saccharide_glycolipid_like_bgc_review", "hserlactone_bgc_review"}:
            return 0.62, "BGC could motivate surface-activity screen but chemistry is unresolved"
        return 0.25, "weak material specificity"
    if track == "biopolymer_eps":
        if subtype == "pha_polyhydroxyalkanoate":
            return 0.88, "clear PHA/biopolymer material class"
        if subtype == "eps_capsule_export":
            return 0.84, "clear EPS/capsule material class"
        return 0.45, "biopolymer class uncertain"
    if track == "protein_materials":
        if subtype == "surface_adhesive_protein":
            return 0.82, "coating/adhesion material hypothesis"
        if subtype == "biofilm_matrix_or_regulator":
            return 0.58, "biofilm material relevance indirect"
        if subtype == "metal_binding_surface_candidate":
            return 0.55, "surface metal-binding hypothesis"
        return 0.35, "generic protein-material proxy"
    if track == "pigment_materials":
        return (0.82, "melanin/polymerizable pigment hypothesis") if has_any(text, PIGMENT_TERMS) else (0.4, "weak pigment relevance")
    return 0.4, "application fit unresolved"


def export_score(text: str, track: str, subtype: str, clusters: list[dict[str, object]]) -> tuple[float, str]:
    if track == "biopolymer_eps":
        if subtype == "pha_polyhydroxyalkanoate":
            return 0.58, "PHA is intracellular/recoverable rather than secreted"
        if has_any(text, ["wzc", "wzz", "exod", "outer membrane", "export", "polyprenyl", "transporter", "capsule"]):
            return 0.85, "EPS/capsule export or surface assembly terms"
        return 0.62, "EPS recovery route plausible but export evidence incomplete"
    if track == "protein_materials":
        if has_any(text, ["surface", "adhesin", "lipoprotein", "periplasmic", "pil", "yada", "serralysin", "pep-cterm"]):
            return 0.86, "surface/periplasmic/adhesin localization terms"
        return 0.42, "no clear extracellular/localization evidence"
    if track == "pigment_materials":
        return 0.6, "pigment pathway is assayable, export route not established"
    if track == "biosurfactant_bgc":
        if has_any(text, ["transporter", "outer membrane", "export", "efflux", "lipoprotein"]):
            return 0.65, "some transport/localization context"
        if clusters:
            return 0.55, "BGC context present, export unresolved"
        return 0.35, "no export/recovery support"
    return 0.4, "export evidence unresolved"


def novelty_score(row: dict[str, str], text: str, track: str) -> tuple[float, str]:
    if row.get("synthetic_bgc_row") == "1":
        reason = row.get("mibig_novelty_reason", "")
        if "distant" in norm(reason) or "no" in norm(reason):
            return 0.78, reason or "BGC-family novelty proxy from Plan01"
        if row.get("nearest_mibig"):
            return 0.58, f"nearest MiBIG context: {row.get('nearest_mibig')}"
        return 0.65, "Plan01 strict BGC distinctness proxy"
    if "hypothetical protein" in text and not has_any(text, HOUSEKEEPING_TERMS):
        return 0.7, "hypothetical protein with material-domain annotation"
    if has_any(text, ["phac", "tyrosinase", "pily1", "yada", "wzc", "wzz", "gumd"]):
        return 0.62, "known family but candidate-specific novelty not resolved"
    return 0.48, "common annotation; no UniRef/nr dereplication layer in this run"


def assay_score(track: str, subtype: str, recovery: float) -> tuple[float, str]:
    if track == "biopolymer_eps":
        if subtype == "pha_polyhydroxyalkanoate":
            base, note = 0.86, "PHA staining/polymer confirmation assays are straightforward"
        elif subtype == "eps_capsule_export":
            base, note = 0.78, "EPS/capsule/carbohydrate assays are straightforward"
        else:
            base, note = 0.45, "biopolymer assay target unresolved"
    elif track == "protein_materials":
        if subtype == "surface_adhesive_protein":
            base, note = 0.68, "adhesion/coating readout possible, expression risk remains"
        else:
            base, note = 0.42, "generic protein-material assay is not specific enough"
    elif track == "pigment_materials":
        base, note = 0.76, "pigment induction/UV-vis style screen is simple"
    elif track == "biosurfactant_bgc":
        base, note = 0.55, "surface activity assays are simple but product chemistry is unresolved"
    else:
        base, note = 0.4, "assay not clearly mapped"
    if recovery < 0.5:
        base -= 0.15
        note += "; recovery/culture path is weak"
    return clip(base), note


def safety_score(
    row: dict[str, str],
    text: str,
    source_text: str,
    source: dict[str, str],
    amr_rows: list[dict[str, object]],
    amr_near: list[dict[str, object]],
    mobile_near: list[dict[str, object]],
) -> tuple[float, str, str]:
    flags = []
    pathogen = any(term in source_text for term in PATHOGEN_CONTEXT_TERMS)
    amr_core = [r for r in amr_rows if norm(r.get("type")) == "amr" or norm(r.get("subtype")) == "amr"]
    stress_rows = [r for r in amr_rows if norm(r.get("type")) == "stress"]
    if pathogen:
        flags.append("pathogen_adjacent_taxonomy")
    if any(word in source_text for word in ["gut", "digestive", "gastrointestinal"]):
        flags.append("gut_source_context")
    if amr_core:
        flags.append(f"genome_amr_rows={len(amr_core)}")
    if stress_rows:
        flags.append(f"stress_resistance_rows={len(stress_rows)}")
    if amr_near:
        flags.append(f"candidate_near_amr_rows={len(amr_near)}")
    if mobile_near:
        flags.append(f"candidate_near_mobile_rows={len(mobile_near)}")
    if has_any(text, TOXIN_VIRULENCE_TERMS):
        flags.append("toxin_or_virulence_keyword")

    score = 1.0
    if pathogen:
        score -= 0.35
    if "gut_source_context" in flags:
        score -= 0.2
    if amr_core:
        score -= 0.2
    if stress_rows and not amr_core:
        score -= 0.08
    if amr_near:
        score -= 0.35
    if mobile_near:
        score -= 0.18
    if has_any(text, TOXIN_VIRULENCE_TERMS):
        score -= 0.35
    if fnum(source.get("contamination")) > 5:
        score -= 0.15
    call = "PASS_WITH_CONTEXT_NOTE" if score >= 0.65 else "HOLD_OR_REVIEW_SAFETY_CONTEXT"
    return clip(score), call, ";".join(flags) if flags else "none_detected"


def status_call(
    row: dict[str, object],
    track: str,
    subtype: str,
    score: float,
    pathway: float,
    application: float,
    quality: float,
    safety: float,
    assay: float,
    text: str,
) -> str:
    if quality < 0.45:
        return "HOLD_LOW_GENOME_QUALITY"
    if safety < 0.45:
        return "HOLD_SAFETY_CONTEXT"
    if track == "biosurfactant_bgc":
        if subtype == "lps_lipid_a_housekeeping":
            return "HOLD_HOUSEKEEPING_LPS_NOT_BIOSURFACTANT"
        if score >= 60:
            return "REVIEW_BGC_CHEMISTRY_NOT_RESOLVED"
        return "HOLD_BIOSURFACTANT_EVIDENCE_INCOMPLETE"
    if pathway < 0.55 or application < 0.55:
        return "HOLD_WEAK_MATERIAL_SPECIFICITY"
    if has_any(text, HOUSEKEEPING_TERMS) and track == "protein_materials":
        return "HOLD_HOUSEKEEPING_OR_GENERIC_PROTEIN"
    if score >= 72 and pathway >= 0.65 and application >= 0.65 and safety >= 0.55 and assay >= 0.55:
        return "KEEP_PRE_WETLAB_PACKET"
    if score >= 60:
        return "REVIEW_PRE_WETLAB_BACKUP"
    return "HOLD_LOW_PRIORITY"


def classify_final_call(status: str, track: str) -> str:
    if track == "biosurfactant_bgc":
        return "NOT_ADVANCED_BIOSURFACTANT_CHEMISTRY_UNRESOLVED"
    if status == "KEEP_PRE_WETLAB_PACKET":
        return "ADVANCE_TO_PRE_WETLAB_PACKET"
    return "NOT_ADVANCED"


def load_bigscape_context() -> dict[str, dict[str, str]]:
    context: dict[str, dict[str, str]] = {}
    for row in read_csv(PLAN01_BIGSCAPE):
        left = row.get("left_region_file", "")
        if left:
            context[left] = row
    return context


def bgc_region_file(strict_bgc_id: str) -> str:
    parts = strict_bgc_id.split(":")
    if len(parts) < 2:
        return ""
    contig = parts[1]
    return f"{contig}.region001.gbk"


def synthesize_bgc_rows(sources: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    bigscape = load_bigscape_context()
    for bgc in read_csv(PLAN01_BGC):
        if bgc.get("strict_status") != "accepted":
            continue
        product = bgc.get("product_class", "")
        product_low = norm(product)
        include = False
        if any(term in product_low for term in ["nrp", "nrps", "saccharide", "hserlactone"]):
            include = True
        if any(term in product_low for term in ["lipopeptide", "glycolipid", "rhamnolipid", "surfactin"]):
            include = True
        if not include:
            continue
        genome_id = bgc.get("genome_id", "")
        source = sources.get(genome_id, {})
        region_file = bgc_region_file(bgc.get("strict_bgc_id", ""))
        bs = bigscape.get(region_file, {})
        rows.append(
            {
                "candidate_id": f"08BGC:{bgc.get('strict_bgc_id', '')}",
                "protein_id": "",
                "target": "biosurfactant_bgc",
                "score": bgc.get("strict_plan01_score", ""),
                "evidence": "strict Plan01 BGC candidate reused for Plan08 biosurfactant-like BGC review",
                "annotation_text": " ".join(
                    [
                        "product_class=" + product,
                        "support_sources=" + bgc.get("support_sources", ""),
                        "context=" + bgc.get("context_text", ""),
                    ]
                ).strip(),
                "protein_length": "",
                "genome_id": genome_id,
                "source_query": bgc.get("source_query") or source.get("query", ""),
                "query_label": bgc.get("query_label") or source.get("query_label", ""),
                "extreme_label": bgc.get("extreme_label") or source.get("extreme_label", ""),
                "biome": bgc.get("biome") or source.get("biome", ""),
                "catalogue": bgc.get("catalogue") or source.get("catalogue", ""),
                "taxon_lineage": bgc.get("taxon_lineage") or source.get("taxon_lineage", ""),
                "completeness": bgc.get("completeness") or source.get("completeness", ""),
                "contamination": bgc.get("contamination") or source.get("contamination", ""),
                "ec": "",
                "kegg_ko": "",
                "kegg_module": "",
                "cazy": "",
                "pfams": "",
                "interpro_ids": "",
                "evidence_level": "BGC-level strict triage",
                "synthetic_bgc_row": "1",
                "strict_bgc_id": bgc.get("strict_bgc_id", ""),
                "product_class": product,
                "nearest_mibig": bgc.get("nearest_mibig", ""),
                "mibig_novelty_reason": bgc.get("mibig_novelty_reason", ""),
                "plan01_strict_score": bgc.get("strict_plan01_score", ""),
                "plan01_support_sources": bgc.get("support_sources", ""),
                "plan01_safety_flags": bgc.get("safety_flags", ""),
                "plan01_mobile_hit_count": bgc.get("mobile_hit_count", ""),
                "plan01_amr_hit_count": bgc.get("amr_hit_count", ""),
                "bigscape_similarity": bs.get("bigscape_similarity", ""),
                "bigscape_distance": bs.get("bigscape_distance", ""),
                "bigscape_claim_limit": bs.get("claim_limit", ""),
            }
        )
    return rows


def material_token_summary(text: str) -> str:
    hits = []
    for label, terms in [
        ("PHA", PHA_TERMS),
        ("EPS", EPS_TERMS),
        ("protein_material", PROTEIN_MATERIAL_TERMS),
        ("pigment", PIGMENT_TERMS),
        ("biosurfactant_direct", TRUE_BIOSURFACTANT_TERMS),
        ("housekeeping", HOUSEKEEPING_TERMS),
    ]:
        found = term_hits(text, terms)
        if found:
            hits.append(f"{label}:{'|'.join(found[:6])}")
    return "; ".join(hits) if hits else "none"


def compute_master_rows() -> list[dict[str, object]]:
    sources = load_sources()
    plan04 = load_plan04_context()
    raw_rows = read_csv(PLAN08_INPUT)
    bgc_rows = synthesize_bgc_rows(sources)
    all_rows = raw_rows + bgc_rows
    genome_ids = {row.get("genome_id", "") for row in all_rows if row.get("genome_id")}
    gene_maps = load_gene_maps(genome_ids)
    clusters_by_genome = load_clusters(genome_ids)
    mobilome_by_genome = load_mobilome(genome_ids)
    amr_by_genome = load_amr(genome_ids)
    genome_counts = genome_material_counts(raw_rows)

    indexed_by_genome_track: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        indexed_by_genome_track[(row.get("genome_id", ""), track_for(row))].append(row)

    master: list[dict[str, object]] = []
    for row in all_rows:
        genome_id = row.get("genome_id", "")
        source = sources.get(genome_id, {})
        source_text = source_context_text(row, source)
        track = track_for(row)
        text = candidate_text(row)
        subtype = material_subtype(row, text, track)
        coords = gene_maps.get(genome_id, {}).get(row.get("protein_id", ""))
        clusters = overlapping_clusters(coords, clusters_by_genome.get(genome_id, []))
        if row.get("synthetic_bgc_row") == "1":
            clusters = []
        mobile_near = nearby_features(coords, mobilome_by_genome.get(genome_id, []), 10000)
        amr_near = nearby_features(coords, amr_by_genome.get(genome_id, []), 10000)
        locus_count = locus_support(row, indexed_by_genome_track)
        quality, quality_call = quality_score(source)
        src_score, src_note = source_score(track, source_text)
        recovery, recovery_call = recovery_score(source, plan04.get(genome_id, {}))
        path_score, path_note = pathway_score(row, text, track, subtype, locus_count, genome_counts.get(genome_id, Counter()), clusters)
        app_score, app_note = application_score(text, track, subtype)
        exp_score, exp_note = export_score(text, track, subtype, clusters)
        nov_score, nov_note = novelty_score(row, text, track)
        assay, assay_note = assay_score(track, subtype, recovery)
        safe, safety_call, safety_flags = safety_score(
            row,
            text,
            source_text,
            source,
            amr_by_genome.get(genome_id, []),
            amr_near,
            mobile_near,
        )

        if row.get("synthetic_bgc_row") == "1":
            if inum(row.get("plan01_mobile_hit_count")) > 0:
                safe = max(0.0, safe - 0.12)
                safety_flags = safety_flags + ";plan01_cluster_mobile_context"
            if inum(row.get("plan01_amr_hit_count")) > 0:
                safe = max(0.0, safe - 0.25)
                safety_flags = safety_flags + ";plan01_cluster_amr_context"

        final_score = 100.0 * (
            0.20 * path_score
            + 0.17 * app_score
            + 0.15 * src_score
            + 0.13 * exp_score
            + 0.12 * nov_score
            + 0.10 * assay
            + 0.08 * quality
            + 0.05 * safe
        )
        status = status_call(row, track, subtype, final_score, path_score, app_score, quality, safe, assay, text)

        cluster_summary = "; ".join(
            f"{c.get('cluster_source')}:{c.get('cluster_id')}:{c.get('product')}:{c.get('score')}"
            for c in clusters[:5]
        )
        mobile_summary = "; ".join(
            f"{m.get('type')}@{m.get('contig')}:{m.get('start')}-{m.get('end')}:{m.get('distance_bp')}bp"
            for m in mobile_near[:5]
        )
        amr_summary = "; ".join(
            f"{a.get('symbol')}:{a.get('type')}:{a.get('subtype')}@{a.get('contig')}:{a.get('start')}-{a.get('end')}"
            for a in amr_near[:5]
        )

        out = {
            "candidate_id": row.get("candidate_id", ""),
            "protein_id": row.get("protein_id", ""),
            "strict_bgc_id": row.get("strict_bgc_id", ""),
            "track": track,
            "track_label": TRACK_LABELS[track],
            "target": row.get("target", ""),
            "material_subtype": subtype,
            "plan08_final_score": round(final_score, 3),
            "plan08_status": status,
            "final_wetlab_call": classify_final_call(status, track),
            "pathway_or_bgc_completeness": round(path_score, 3),
            "material_application_fit": round(app_score, 3),
            "source_environment_support": round(src_score, 3),
            "export_or_recovery_evidence": round(exp_score, 3),
            "novelty_score": round(nov_score, 3),
            "assay_and_recovery_feasibility": round(assay, 3),
            "taxonomy_and_genome_quality": round(quality, 3),
            "safety_score": round(safe, 3),
            "pathway_note": path_note,
            "application_note": app_note,
            "source_environment_note": src_note,
            "export_recovery_note": exp_note,
            "novelty_note": nov_note,
            "assay_note": assay_note,
            "genome_quality_call": quality_call,
            "recovery_call": recovery_call,
            "safety_call": safety_call,
            "safety_flags": safety_flags,
            "locus_support_count_pm10": locus_count,
            "same_genome_pha_hits": genome_counts.get(genome_id, Counter()).get("pha", 0),
            "same_genome_eps_hits": genome_counts.get(genome_id, Counter()).get("eps", 0),
            "same_genome_protein_material_hits": genome_counts.get(genome_id, Counter()).get("protein_material", 0),
            "candidate_material_tokens": material_token_summary(text),
            "cluster_overlap_summary": cluster_summary,
            "candidate_near_mobile_count": len(mobile_near),
            "candidate_near_mobile_summary": mobile_summary,
            "candidate_near_amr_count": len(amr_near),
            "candidate_near_amr_summary": amr_summary,
            "genome_amr_rows": len(amr_by_genome.get(genome_id, [])),
            "genome_mobilome_feature_rows": len(mobilome_by_genome.get(genome_id, [])),
            "genome_id": genome_id,
            "protein_length": row.get("protein_length", ""),
            "annotation_text": row.get("annotation_text", ""),
            "evidence": row.get("evidence", ""),
            "evidence_level": row.get("evidence_level", ""),
            "source_query": row.get("source_query") or source.get("query", ""),
            "query_label": row.get("query_label") or source.get("query_label", ""),
            "extreme_label": row.get("extreme_label") or source.get("extreme_label", ""),
            "biome": row.get("biome") or source.get("biome", ""),
            "catalogue": row.get("catalogue") or source.get("catalogue", ""),
            "genome_type": source.get("type", ""),
            "completeness": row.get("completeness") or source.get("completeness", ""),
            "contamination": row.get("contamination") or source.get("contamination", ""),
            "num_contigs": source.get("num_contigs", ""),
            "n50": source.get("n50", ""),
            "taxon_lineage": row.get("taxon_lineage") or source.get("taxon_lineage", ""),
            "contig": coords.get("contig", "") if coords else "",
            "start": coords.get("start", "") if coords else row.get("start", ""),
            "end": coords.get("end", "") if coords else row.get("end", ""),
            "product_class": row.get("product_class", ""),
            "nearest_mibig": row.get("nearest_mibig", ""),
            "mibig_novelty_reason": row.get("mibig_novelty_reason", ""),
            "plan01_strict_score": row.get("plan01_strict_score", ""),
            "plan01_support_sources": row.get("plan01_support_sources", ""),
            "plan01_safety_flags": row.get("plan01_safety_flags", ""),
            "bigscape_similarity": row.get("bigscape_similarity", ""),
            "bigscape_distance": row.get("bigscape_distance", ""),
            "plan04_call": plan04.get(genome_id, {}).get("plan04_call", ""),
            "plan04_trait": plan04.get(genome_id, {}).get("plan04_trait", ""),
            "plan04_reference_gate": plan04.get(genome_id, {}).get("plan04_reference_gate", ""),
            "strongest_safe_claim": safe_claim(track, subtype),
            "claim_limit": claim_limit(track),
        }
        master.append(out)

    master.sort(key=lambda r: (str(r["track"]), -fnum(r["plan08_final_score"]), str(r["candidate_id"])))
    mark_selected_candidates(master)
    return master


def safe_claim(track: str, subtype: str) -> str:
    if track == "biosurfactant_bgc":
        return "Computational biosurfactant-like BGC review candidate; product chemistry and surface activity remain unvalidated."
    if track == "biopolymer_eps":
        if subtype == "pha_polyhydroxyalkanoate":
            return "Computationally prioritized PHA/biopolymer pathway hypothesis with genome/source/safety context support."
        if subtype == "eps_capsule_export":
            return "Computationally prioritized EPS/capsule/export locus hypothesis with genome/source/safety context support."
    if track == "protein_materials":
        return "Computationally prioritized protein-material hypothesis with domain/localization/source/safety context support."
    if track == "pigment_materials":
        return "Computationally prioritized melanin-like pigment pathway hypothesis with source/safety context support."
    return "Computational biomaterials hypothesis; experimental validation is required."


def claim_limit(track: str) -> str:
    if track == "biosurfactant_bgc":
        return "Does not prove biosurfactant production, molecule identity, titer, surface tension change, or safety."
    if track == "biopolymer_eps":
        return "Does not prove polymer production, polymer chemistry, yield, material properties, or organism safety."
    if track == "protein_materials":
        return "Does not prove expression, folding, coating performance, adhesion strength, or safety."
    if track == "pigment_materials":
        return "Does not prove pigment production, melanin identity, yield, or functional material performance."
    return "Computational prioritization only."


def selection_priority(row: dict[str, object]) -> float:
    score = fnum(row.get("plan08_final_score"))
    text = norm(row.get("annotation_text"))
    subtype = str(row.get("material_subtype"))
    recovery = str(row.get("recovery_call", ""))
    source_note = str(row.get("source_environment_note", ""))
    if "CULTURED_CLOSE_RELATIVE" in recovery or "MGNIFY_ISOLATE" in recovery:
        score += 1.0
    if "oil-associated" in source_note or "marine hydrocarbon-associated" in source_note:
        score += 0.4
    if subtype == "pha_polyhydroxyalkanoate":
        if "poly(3-hydroxyalkanoate) polymerase subunit phac" in text or "phaC_N".lower() in text:
            score += 1.5
        if "duf3141" in text:
            score -= 1.0
    if subtype == "eps_capsule_export":
        if has_any(text, ["wzc", "wzz", "gumd", "polyprenyl glycosylphosphotransferase"]):
            score += 0.6
        if row.get("cluster_overlap_summary"):
            score += 0.2
    if subtype == "surface_adhesive_protein":
        if has_any(text, ["pily1", "pilc"]):
            score += 1.0
        if has_any(text, ["yada", "collagen-binding", "serralysin"]):
            score += 0.8
        if has_any(text, ["znu", "mntc", "abc-type metal ion transport"]):
            score -= 2.0
    return score


def select_diverse(rows: list[dict[str, object]], max_count: int) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    used_subtypes: set[str] = set()
    genome_counts: Counter = Counter()
    keep_rows = [r for r in rows if r.get("plan08_status") == "KEEP_PRE_WETLAB_PACKET"]
    review_rows = [r for r in rows if str(r.get("plan08_status", "")).startswith("REVIEW")]
    for pool in [keep_rows, review_rows]:
        for row in sorted(pool, key=lambda r: (-selection_priority(r), -fnum(r.get("plan08_final_score")))):
            if len(selected) >= max_count:
                break
            subtype = str(row.get("material_subtype"))
            genome_id = str(row.get("genome_id"))
            if subtype in used_subtypes and len(selected) < max_count - 1:
                continue
            if genome_counts[genome_id] >= 2:
                continue
            selected.append(row)
            used_subtypes.add(subtype)
            genome_counts[genome_id] += 1
        if len(selected) >= max_count:
            break
    if len(selected) < max_count:
        already = {str(r.get("candidate_id")) for r in selected}
        for row in sorted(keep_rows + review_rows, key=lambda r: (-selection_priority(r), -fnum(r.get("plan08_final_score")))):
            if len(selected) >= max_count:
                break
            if str(row.get("candidate_id")) in already:
                continue
            selected.append(row)
            already.add(str(row.get("candidate_id")))
    return selected


def mark_selected_candidates(master: list[dict[str, object]]) -> None:
    for row in master:
        row["packet_rank"] = ""
        row["packet_role"] = ""

    by_track: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in master:
        by_track[str(row["track"])].append(row)

    selected: list[dict[str, object]] = []
    selected.extend(select_diverse(by_track["biopolymer_eps"], 3))
    selected.extend(select_diverse(by_track["protein_materials"], 2))
    selected.extend(select_diverse(by_track["pigment_materials"], 1))

    bgc_review = [
        row
        for row in sorted(by_track["biosurfactant_bgc"], key=lambda r: -fnum(r.get("plan08_final_score")))
        if row.get("plan08_status") == "REVIEW_BGC_CHEMISTRY_NOT_RESOLVED" and row.get("strict_bgc_id")
    ][:3]
    if len(bgc_review) < 3:
        already = {row.get("candidate_id") for row in bgc_review}
        for row in sorted(by_track["biosurfactant_bgc"], key=lambda r: -fnum(r.get("plan08_final_score"))):
            if len(bgc_review) >= 3:
                break
            if row.get("plan08_status") != "REVIEW_BGC_CHEMISTRY_NOT_RESOLVED":
                continue
            if row.get("candidate_id") in already:
                continue
            bgc_review.append(row)
            already.add(row.get("candidate_id"))
    selected.extend(bgc_review)

    for rank, row in enumerate(selected, start=1):
        row["packet_rank"] = rank
        if row["track"] == "biosurfactant_bgc":
            row["packet_role"] = "BGC_REVIEW_PACKET_NOT_IMMEDIATE_WETLAB"
        else:
            row["packet_role"] = "IMMEDIATE_PRE_WETLAB_PACKET"


def shortlist_rows(master: list[dict[str, object]], track: str, limit: int = 40) -> list[dict[str, object]]:
    rows = [row for row in master if row.get("track") == track]
    rows.sort(key=lambda r: (-fnum(r.get("plan08_final_score")), str(r.get("candidate_id"))))
    return rows[:limit]


def assay_recommendation(row: dict[str, object]) -> str:
    subtype = str(row.get("material_subtype"))
    if subtype == "pha_polyhydroxyalkanoate":
        return "First-pass PHA staining and orthogonal polymer-chemistry confirmation after institutional review; no production optimization implied."
    if subtype == "eps_capsule_export":
        return "First-pass EPS/capsule staining and carbohydrate quantification; rheology only after production is experimentally observed."
    if subtype == "surface_adhesive_protein":
        return "Protein-only expression feasibility and surface adhesion/coating readout after biosafety and synthesis review; no construct design is provided here."
    if subtype == "tyrosinase_melanin_like":
        return "Pigment induction or enzyme/pigment readout with UV-vis-style confirmation; identity and material performance remain untested."
    if str(row.get("track")) == "biosurfactant_bgc":
        return "Only a chemistry-review packet now; surface-activity assays should wait for product-class clarification or organism-level phenotyping."
    return "Assay route needs manual review before wet-lab packaging."


def related_gene_rows(candidate: dict[str, object], master: list[dict[str, object]]) -> list[dict[str, object]]:
    genome_id = str(candidate.get("genome_id"))
    track = str(candidate.get("track"))
    pnum = protein_number(str(candidate.get("protein_id")))
    related = []
    for row in master:
        if row.get("genome_id") != genome_id or row.get("track") != track:
            continue
        if pnum is not None and row.get("protein_id"):
            onum = protein_number(str(row.get("protein_id")))
            if onum is None or abs(onum - pnum) > 10:
                continue
        related.append(row)
    related.sort(key=lambda r: (-fnum(r.get("plan08_final_score")), str(r.get("protein_id"))))
    return related[:12]


def packet_filename(row: dict[str, object]) -> str:
    rank = inum(row.get("packet_rank"))
    cid = str(row.get("protein_id") or row.get("strict_bgc_id") or row.get("candidate_id"))
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", cid)[:100]
    return f"{rank:02d}_{safe}_{row.get('material_subtype')}.md"


def write_candidate_packets(master: list[dict[str, object]]) -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    for old in PACKET_DIR.glob("*.md"):
        old.unlink()
    selected = [row for row in master if row.get("packet_rank")]
    selected.sort(key=lambda r: inum(r.get("packet_rank")))
    manifest = []
    for row in selected:
        related = related_gene_rows(row, master)
        role = row.get("packet_role")
        title_id = row.get("protein_id") or row.get("strict_bgc_id") or row.get("candidate_id")
        lines = [
            f"# Plan 08 Candidate Packet {row.get('packet_rank')}: `{title_id}`",
            "",
            f"- Packet role: `{role}`",
            f"- Track: {row.get('track_label')}",
            f"- Material subtype: `{row.get('material_subtype')}`",
            f"- Plan08 score/status: {row.get('plan08_final_score')} / `{row.get('plan08_status')}`",
            f"- Final wet-lab call: `{row.get('final_wetlab_call')}`",
            f"- Genome: `{row.get('genome_id')}`; type `{row.get('genome_type')}`; quality `{row.get('genome_quality_call')}`; completeness {row.get('completeness')}; contamination {row.get('contamination')}",
            f"- Source: {row.get('query_label')} / {row.get('biome')} / {row.get('catalogue')}",
            f"- Taxonomy: {row.get('taxon_lineage')}",
            "",
            "## Evidence Summary",
            "",
            f"- Pathway/BGC support: {row.get('pathway_note')}",
            f"- Material application fit: {row.get('application_note')}",
            f"- Export/recovery evidence: {row.get('export_recovery_note')}",
            f"- Novelty/dereplication context: {row.get('novelty_note')}",
            f"- Candidate material tokens: {row.get('candidate_material_tokens')}",
            f"- Cluster/PUL overlap: {row.get('cluster_overlap_summary') or 'none_detected'}",
            f"- Plan04 context: {row.get('plan04_trait') or 'not a Plan04 finalist'}; {row.get('plan04_reference_gate') or row.get('recovery_call')}",
            "",
            "## Local Gene / Locus Context",
            "",
            "| Candidate/protein | Target | Subtype | Score | Key annotation |",
            "|---|---|---|---:|---|",
        ]
        for rel in related:
            ann = " ".join(str(rel.get("annotation_text", "")).split())[:180]
            cid = rel.get("protein_id") or rel.get("strict_bgc_id") or rel.get("candidate_id")
            lines.append(
                f"| `{cid}` | {rel.get('target')} | {rel.get('material_subtype')} | {rel.get('plan08_final_score')} | {ann} |"
            )
        if not related:
            lines.append("| n/a | n/a | n/a | n/a | BGC-level row; see Plan01 strict BGC context columns. |")
        lines.extend(
            [
                "",
                "## Safety and Practicality Screen",
                "",
                f"- Safety call: `{row.get('safety_call')}`; flags: {row.get('safety_flags')}",
                f"- Candidate-near AMR rows: {row.get('candidate_near_amr_count')} ({row.get('candidate_near_amr_summary') or 'none_detected'})",
                f"- Candidate-near mobile rows: {row.get('candidate_near_mobile_count')} ({row.get('candidate_near_mobile_summary') or 'none_detected'})",
                f"- Recovery/culture path: {row.get('recovery_call')}",
                "",
                "## Assay Direction",
                "",
                assay_recommendation(row),
                "",
                "## Strongest Safe Claim",
                "",
                row.get("strongest_safe_claim", ""),
                "",
                "## Remaining Experimental Gaps",
                "",
                row.get("claim_limit", ""),
                "No gene sequence, synthesis instruction, strain-engineering plan, or performance claim is included in this packet.",
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
                "protein_id": row.get("protein_id"),
                "strict_bgc_id": row.get("strict_bgc_id"),
                "track": row.get("track"),
                "material_subtype": row.get("material_subtype"),
                "plan08_final_score": row.get("plan08_final_score"),
                "plan08_status": row.get("plan08_status"),
                "final_wetlab_call": row.get("final_wetlab_call"),
                "packet_file": str(path.relative_to(ROOT)),
            }
        )
    write_csv(OUT_DIR / "plan08_candidate_packet_manifest.csv", manifest, list(manifest[0].keys()) if manifest else [])


def counts_table(rows: list[dict[str, object]], key: str) -> str:
    counter = Counter(str(row.get(key, "")) for row in rows)
    lines = ["| Value | Count |", "|---|---:|"]
    for value, count in counter.most_common():
        lines.append(f"| `{value}` | {count} |")
    return "\n".join(lines)


def markdown_candidate_table(rows: list[dict[str, object]], limit: int = 12) -> str:
    lines = [
        "| Rank | Candidate | Track | Subtype | Score | Status | Genome/source | Main caveat |",
        "|---:|---|---|---|---:|---|---|---|",
    ]
    for idx, row in enumerate(rows[:limit], start=1):
        cid = row.get("protein_id") or row.get("strict_bgc_id") or row.get("candidate_id")
        source = f"{row.get('genome_id')} / {row.get('query_label')}"
        lines.append(
            f"| {idx} | `{cid}` | {row.get('track_label')} | `{row.get('material_subtype')}` | {row.get('plan08_final_score')} | `{row.get('plan08_status')}` | {source} | {row.get('claim_limit')} |"
        )
    return "\n".join(lines)


def write_reports(master: list[dict[str, object]]) -> None:
    selected = [row for row in master if row.get("packet_rank")]
    selected.sort(key=lambda r: inum(r.get("packet_rank")))
    immediate = [row for row in selected if row.get("packet_role") == "IMMEDIATE_PRE_WETLAB_PACKET"]
    bgc_review = [row for row in selected if row.get("packet_role") == "BGC_REVIEW_PACKET_NOT_IMMEDIATE_WETLAB"]
    first_pass = read_csv(PLAN08_INPUT)

    report_lines = [
        "# Plan 08 Pre-Wet-Lab Screen Report",
        "",
        "Date: 2026-05-18",
        "",
        "## Executive Summary",
        "",
        f"The hardened Plan 08 screen started from {len(first_pass)} first-pass biomaterials hits and added BGC, genome-quality, source-environment, recovery, and safety-context gates. The final master table contains {len(master)} rows after adding Plan01 strict BGC review rows for the biosurfactant/BGC track.",
        "",
        f"The immediate wet-lab-facing packet set contains {len(immediate)} candidates: biopolymer/EPS, protein-material, and pigment hypotheses with coherent pathway or domain evidence. Biosurfactant/BGC rows were not advanced as immediate wet-lab leads because the available BGC/product annotations do not resolve a specific lipopeptide, glycolipid, rhamnolipid, or surfactin-like product. Three BGC review packets are retained for chemistry follow-up, not direct wet-lab packaging.",
        "",
        "Strongest safe claim: computationally prioritized microbial biomaterials hypotheses with pathway, source-environment, novelty/recovery, safety-context, and assay-feasibility support. No material production, performance, molecule identity, organism safety, or industrial utility is claimed.",
        "",
        "## Inputs Reused",
        "",
        f"- First-pass Plan08 candidates: `{PLAN08_INPUT.relative_to(ROOT)}`",
        f"- Source genomes: `{SOURCE_GENOMES.relative_to(ROOT)}`",
        "- Local annotations: genome GFF, antiSMASH, GECCO, SanntiS, dbCAN, AMRFinderPlus, and mobilome files under the May 14 MGnify cache",
        f"- Plan01 strict BGC context: `{PLAN01_BGC.relative_to(ROOT)}`",
        f"- Plan04 culture/isolate context: `{PLAN04_FINALISTS.relative_to(ROOT)}` and `{PLAN04_ISOLATES.relative_to(ROOT)}`",
        "",
        "## Filter Summary",
        "",
        "### Tracks",
        "",
        counts_table(master, "track"),
        "",
        "### Status Calls",
        "",
        counts_table(master, "plan08_status"),
        "",
        "## Immediate Pre-Wet-Lab Packet Set",
        "",
        markdown_candidate_table(immediate, limit=20),
        "",
        "## Biosurfactant/BGC Review Holds",
        "",
        markdown_candidate_table(bgc_review, limit=10),
        "",
        "These BGCs are scientifically useful review targets, but they should not be described as biosurfactant candidates ready for wet-lab validation until product chemistry is clarified. The first-pass lipid-A/LPS hits were explicitly demoted as housekeeping envelope biosynthesis rather than biosurfactant evidence.",
        "",
        "## What Changed From The First Pass",
        "",
        "- Generic metal-binding, self-assembling, transporter, and housekeeping hits no longer dominate the top list.",
        "- Lipid-A/LPS genes are retained in the master table for traceability but held as `HOLD_HOUSEKEEPING_LPS_NOT_BIOSURFACTANT`.",
        "- The strongest practical candidates now come from coherent PHA/EPS loci, surface adhesin/domain candidates, and the single tyrosinase/melanin-like pigment hit.",
        "- `MGYG000517341` benefits from prior Plan04 isolate/reference context; the report still treats this as computational packaging, not phenotype or safety validation.",
        "",
        "## Output Files",
        "",
        "- `plan08_biomaterials_candidate_master.csv`",
        "- `plan08_biosurfactant_bgc_shortlist.csv`",
        "- `plan08_biopolymer_eps_shortlist.csv`",
        "- `plan08_protein_materials_shortlist.csv`",
        "- `plan08_pigment_materials_shortlist.csv`",
        "- `plan08_safety_and_recovery_gate.csv`",
        "- `plan08_candidate_packet_manifest.csv`",
        "- `plan08_top_candidate_packets/`",
        "- `PLAN08_RESEARCH_STYLE_WRITEUP.md`",
        "- `PLAN08_PRE_WETLAB_SCREEN_COMPLETION_AUDIT.md`",
        "",
        "## Wet-Lab Screen Framing",
        "",
        "| Candidate type | First-pass readout | Claim boundary |",
        "|---|---|---|",
        "| PHA/biopolymer | PHA staining and orthogonal polymer-chemistry confirmation after review | Does not prove polymer yield or material performance |",
        "| EPS/capsule | EPS/capsule staining and carbohydrate quantification | Does not prove recoverable polymer or rheology |",
        "| Adhesive/coating protein | Protein-only feasibility and surface adhesion/coating readout after review | Does not prove expression, folding, or coating strength |",
        "| Melanin/pigment | Pigment/enzyme readout with UV-vis-style confirmation | Does not prove melanin identity or functional material performance |",
        "| Biosurfactant/BGC review | Chemistry review first; organism/product assays only after clarification | Does not prove biosurfactant production or surface activity |",
        "",
        "## Limitations",
        "",
        "This screen still relies on annotations, local neighborhood logic, and source metadata. It does not include new SignalP/TMHMM predictions, UniRef/nr dereplication for every protein, metabolomics, product detection, transcriptomics, or measured material properties. Safety calls are computational triage only and do not replace institutional review.",
        "",
    ]
    (OUT_DIR / "PLAN08_PRE_WETLAB_SCREEN_REPORT.md").write_text("\n".join(report_lines), encoding="utf-8")

    writeup_lines = [
        "# Plan 08: Computational Prioritization of Microbial Biomaterials Hypotheses",
        "",
        "Date: 2026-05-18",
        "",
        "## Abstract",
        "",
        "Plan 08 was hardened from a broad annotation-first biomaterials scan into a pre-wet-lab prioritization package for microbial biomaterials hypotheses. The workflow separated biosurfactant/BGC, biopolymer/EPS, protein-material, and pigment tracks; scored each row for pathway coherence, material fit, source context, export/recovery, novelty, assay feasibility, genome quality, and safety context; and generated candidate packets for the strongest wet-lab-facing hypotheses.",
        "",
        f"The final package contains {len(master)} scored rows and {len(immediate)} immediate pre-wet-lab packets. The cleanest results are PHA/EPS and surface/pigment hypotheses, especially candidates from high-quality `MGYG000517341` and marine `MGYG000478572` contexts. Biosurfactant-like BGCs remain review candidates rather than immediate wet-lab leads because product-class evidence is insufficient to claim a specific biosurfactant family.",
        "",
        "## Methods",
        "",
        "The input set was the May 14 Plan 08 candidate table. Candidate rows were mapped to four tracks and augmented with source-genome quality, MGnify catalogue metadata, local genome coordinates, antiSMASH/GECCO/SanntiS/dbCAN overlaps, AMRFinderPlus and mobilome context, Plan01 strict BGC review rows, and Plan04 isolate/culture context where available.",
        "",
        "Each row received a bounded score using the weights specified in `08_workflow.md`: pathway/BGC completeness, material application fit, source-environment support, export/recovery evidence, novelty, assay/recovery feasibility, taxonomy/genome quality, and safety score. The screen intentionally prioritized evidence coherence over raw first-pass annotation score.",
        "",
        "## Results",
        "",
        "The first-pass table was noisy: many high-scoring rows were generic metal-binding proteins, self-assembly proxies, lipid-A/LPS genes, transporters, or housekeeping enzymes. The hardened status calls demoted these rows and promoted candidates with clearer material logic.",
        "",
        "### Immediate Candidate Set",
        "",
        markdown_candidate_table(immediate, limit=20),
        "",
        "### Biosurfactant/BGC Outcome",
        "",
        "The biosurfactant track is the main conservative result. The screen found BGCs with NRP/NRPS, saccharide, hserlactone, and related product-class context, but not enough evidence to call any of them a clean lipopeptide, glycolipid, rhamnolipid, surfactin-like, or otherwise direct biosurfactant lead. They are retained as review packets, not wet-lab-ready biosurfactant candidates.",
        "",
        "## Interpretation",
        "",
        "The strongest near-term Plan 08 claims are about computational prioritization, not discovered materials. The PHA/EPS candidates are attractive because their gene annotations and locus context map to straightforward first-pass assays. The adhesive-protein candidates are scientifically interesting but carry expression and localization uncertainty. The tyrosinase/melanin-like candidate is compact and assayable but needs product identity confirmation.",
        "",
        "## Claim Boundary",
        "",
        "Plan 08 can be framed as a pre-wet-lab biomaterials hypothesis package. It should not be framed as discovery of a new biosurfactant, polymer producer, biodegradable plastic strain, coating protein, pigment material, or safe industrial organism. Wet-lab testing remains required for production, identity, yield, material properties, and biosafety acceptability.",
        "",
    ]
    (OUT_DIR / "PLAN08_RESEARCH_STYLE_WRITEUP.md").write_text("\n".join(writeup_lines), encoding="utf-8")

    audit_rows = [
        {"requirement": "Read workflow and preserve claim boundaries", "artifact": "08_workflow.md; PLAN08_PRE_WETLAB_SCREEN_REPORT.md", "status": "PASS"},
        {"requirement": "Build master candidate table", "artifact": "plan08_biomaterials_candidate_master.csv", "status": "PASS"},
        {"requirement": "Rank biosurfactant/BGC track separately", "artifact": "plan08_biosurfactant_bgc_shortlist.csv", "status": "PASS"},
        {"requirement": "Rank biopolymer/EPS track separately", "artifact": "plan08_biopolymer_eps_shortlist.csv", "status": "PASS"},
        {"requirement": "Rank protein-material track separately", "artifact": "plan08_protein_materials_shortlist.csv", "status": "PASS"},
        {"requirement": "Rank pigment/material track separately", "artifact": "plan08_pigment_materials_shortlist.csv", "status": "PASS"},
        {"requirement": "Safety and recovery gate", "artifact": "plan08_safety_and_recovery_gate.csv", "status": "PASS"},
        {"requirement": "Candidate packets", "artifact": "plan08_top_candidate_packets/", "status": "PASS"},
        {"requirement": "Wet-lab screen framing without overclaims", "artifact": "PLAN08_PRE_WETLAB_SCREEN_REPORT.md", "status": "PASS"},
        {"requirement": "Research-style writeup", "artifact": "PLAN08_RESEARCH_STYLE_WRITEUP.md", "status": "PASS"},
    ]
    write_csv(
        OUT_DIR / "plan08_completion_audit_checklist.csv",
        audit_rows,
        ["requirement", "artifact", "status"],
    )
    audit_lines = [
        "# Plan 08 Pre-Wet-Lab Screen Completion Audit",
        "",
        "Date: 2026-05-18",
        "",
        "## Success Criteria",
        "",
        "The workflow is complete if it produces the required master table, separate ranked track shortlists, safety/recovery gate, candidate packets, pre-wet-lab report, and research-style writeup while clearly separating computational prioritization from measured material performance.",
        "",
        "## Artifact Checklist",
        "",
        "| Requirement | Artifact | Status |",
        "|---|---|---|",
    ]
    for row in audit_rows:
        audit_lines.append(f"| {row['requirement']} | `{row['artifact']}` | {row['status']} |")
    audit_lines.extend(
        [
            "",
            "## Evidence Counts",
            "",
            f"- Master rows: {len(master)}",
            f"- Immediate pre-wet-lab packets: {len(immediate)}",
            f"- Biosurfactant/BGC review packets, not immediate wet-lab: {len(bgc_review)}",
            f"- Candidate packet markdown files: {len(list(PACKET_DIR.glob('*.md')))}",
            "",
            "## Final Interpretation",
            "",
            "PASS. The Plan 08 computational screen is complete for pre-wet-lab packaging. The result is deliberately conservative: clean wet-lab-facing packets were produced for PHA/EPS, protein-material, and pigment hypotheses; biosurfactant/BGC candidates are held for chemistry clarification rather than advanced as direct biosurfactant leads.",
            "",
        ]
    )
    (OUT_DIR / "PLAN08_PRE_WETLAB_SCREEN_COMPLETION_AUDIT.md").write_text("\n".join(audit_lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    master = compute_master_rows()
    fields = [
        "candidate_id",
        "protein_id",
        "strict_bgc_id",
        "packet_rank",
        "packet_role",
        "track",
        "track_label",
        "target",
        "material_subtype",
        "plan08_final_score",
        "plan08_status",
        "final_wetlab_call",
        "pathway_or_bgc_completeness",
        "material_application_fit",
        "source_environment_support",
        "export_or_recovery_evidence",
        "novelty_score",
        "assay_and_recovery_feasibility",
        "taxonomy_and_genome_quality",
        "safety_score",
        "pathway_note",
        "application_note",
        "source_environment_note",
        "export_recovery_note",
        "novelty_note",
        "assay_note",
        "genome_quality_call",
        "recovery_call",
        "safety_call",
        "safety_flags",
        "locus_support_count_pm10",
        "same_genome_pha_hits",
        "same_genome_eps_hits",
        "same_genome_protein_material_hits",
        "candidate_material_tokens",
        "cluster_overlap_summary",
        "candidate_near_mobile_count",
        "candidate_near_mobile_summary",
        "candidate_near_amr_count",
        "candidate_near_amr_summary",
        "genome_amr_rows",
        "genome_mobilome_feature_rows",
        "genome_id",
        "protein_length",
        "annotation_text",
        "evidence",
        "evidence_level",
        "source_query",
        "query_label",
        "extreme_label",
        "biome",
        "catalogue",
        "genome_type",
        "completeness",
        "contamination",
        "num_contigs",
        "n50",
        "taxon_lineage",
        "contig",
        "start",
        "end",
        "product_class",
        "nearest_mibig",
        "mibig_novelty_reason",
        "plan01_strict_score",
        "plan01_support_sources",
        "plan01_safety_flags",
        "bigscape_similarity",
        "bigscape_distance",
        "plan04_call",
        "plan04_trait",
        "plan04_reference_gate",
        "strongest_safe_claim",
        "claim_limit",
    ]
    write_csv(OUT_DIR / "plan08_biomaterials_candidate_master.csv", master, fields)
    write_csv(OUT_DIR / "plan08_biosurfactant_bgc_shortlist.csv", shortlist_rows(master, "biosurfactant_bgc"), fields)
    write_csv(OUT_DIR / "plan08_biopolymer_eps_shortlist.csv", shortlist_rows(master, "biopolymer_eps"), fields)
    write_csv(OUT_DIR / "plan08_protein_materials_shortlist.csv", shortlist_rows(master, "protein_materials"), fields)
    write_csv(OUT_DIR / "plan08_pigment_materials_shortlist.csv", shortlist_rows(master, "pigment_materials"), fields)

    safety_fields = [
        "candidate_id",
        "protein_id",
        "strict_bgc_id",
        "track",
        "material_subtype",
        "plan08_final_score",
        "plan08_status",
        "final_wetlab_call",
        "genome_id",
        "genome_type",
        "genome_quality_call",
        "recovery_call",
        "safety_score",
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
    write_csv(OUT_DIR / "plan08_safety_and_recovery_gate.csv", master, safety_fields)
    write_candidate_packets(master)
    write_reports(master)

    print(f"Wrote {len(master)} Plan08 scored rows to {OUT_DIR}")
    print(f"Wrote {len(list(PACKET_DIR.glob('*.md')))} candidate packet files")


if __name__ == "__main__":
    main()
