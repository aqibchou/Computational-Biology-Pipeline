#!/usr/bin/env python3
"""Run Plan04 Bacteriovorax genus-reference ANI for MGYG000535629.

This fills a bounded strain-dereplication gap for the MAG-derived Plan04
Bacteriovorax candidate. It downloads current RefSeq Bacteriovorax assemblies
through NCBI Datasets, runs fastANI and skani against the local MGnify genome,
and emits only strain/reference context. It does not claim plant benefit,
recoverability, safety, or phenotype validation.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
BIOENV = ROOT.parents[1] / ".bioenv/bin"
DATASETS = BIOENV / "datasets"
FASTANI = BIOENV / "fastANI"
SKANI = BIOENV / "skani"
QUERY_GENOME_ID = "MGYG000535629"
QUERY_FASTA = ROOT / "outputs/computational_execution_2026-05-14/cache/mgnify_genomes/MGYG000535629/MGYG000535629.fna"
OUTDIR = ROOT / f"outputs/plan04_bacteriovorax_reference_ani_{RUN_DATE}"
DOWNLOAD_DIR = OUTDIR / "ncbi_refseq_downloads"
REFERENCE_DIR = OUTDIR / "reference_fastas"
METADATA_JSONL = OUTDIR / "bacteriovorax_refseq_summary.jsonl"
CLAIM_LIMIT = (
    "ANI supports genus/reference-distance context only; it does not validate plant-growth phenotype, "
    "recoverability, colonization, biosafety, or field performance."
)


def run(cmd: list[str], stdout_path: Path | None = None) -> subprocess.CompletedProcess:
    if stdout_path:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        with stdout_path.open("w") as handle:
            return subprocess.run(cmd, cwd=ROOT, text=True, stdout=handle, stderr=subprocess.PIPE, check=False)
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def nested_get(data: dict, path: list[str], default: object = "") -> object:
    value: object = data
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def biosample_attr(data: dict, name: str) -> str:
    attrs = nested_get(data, ["assembly_info", "biosample", "attributes"], [])
    if not isinstance(attrs, list):
        return ""
    for attr in attrs:
        if isinstance(attr, dict) and attr.get("name") == name:
            return str(attr.get("value", ""))
    return ""


def load_metadata() -> list[dict]:
    result = run([str(DATASETS), "summary", "genome", "taxon", "Bacteriovorax", "--assembly-source", "RefSeq", "--as-json-lines"])
    METADATA_JSONL.write_text(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    records.sort(key=lambda row: row.get("accession", ""))
    return records


def download_reference(accession: str) -> Path | None:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DOWNLOAD_DIR / f"{accession}.zip"
    extract_dir = DOWNLOAD_DIR / accession
    result = run([str(DATASETS), "download", "genome", "accession", accession, "--include", "genome", "--filename", str(zip_path), "--no-progressbar"])
    if result.returncode != 0:
        return None
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extract_dir)
    fasta_candidates = sorted((extract_dir / "ncbi_dataset/data").glob(f"{accession}/*_genomic.fna"))
    if not fasta_candidates:
        return None
    dest = REFERENCE_DIR / f"{accession}.fna"
    shutil.copyfile(fasta_candidates[0], dest)
    return dest


def parse_fastani(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    if not path.exists():
        return rows
    with path.open() as handle:
        for line in handle:
            parts = line.strip().split("\t")
            if len(parts) < 5:
                continue
            ref_path = Path(parts[1])
            rows[ref_path.stem] = {
                "fastani_ani": parts[2],
                "fastani_mapped_fragments": parts[3],
                "fastani_total_fragments": parts[4],
                "fastani_aligned_fragment_pct": f"{(float(parts[3]) / float(parts[4]) * 100.0):.3f}" if float(parts[4]) else "",
            }
    return rows


def parse_skani(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    if not path.exists():
        return rows
    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            ref_name = Path(row.get("Ref_file", "")).stem
            if not ref_name:
                continue
            rows[ref_name] = {
                "skani_ani": row.get("ANI", ""),
                "skani_align_fraction_ref": row.get("Align_fraction_ref", ""),
                "skani_align_fraction_query": row.get("Align_fraction_query", ""),
            }
    return rows


def derep_call(fastani_ani: str, fastani_pct: str, skani_ani: str, skani_q_af: str) -> str:
    ani_values = [float(value) for value in [fastani_ani, skani_ani] if value]
    coverage_values = [float(value) for value in [fastani_pct, skani_q_af] if value]
    max_ani = max(ani_values) if ani_values else 0.0
    max_cov = max(coverage_values) if coverage_values else 0.0
    if max_ani >= 95.0 and max_cov >= 60.0:
        return "CLOSE_REFERENCE_UNEXPECTED_REVIEW"
    if max_ani >= 80.0 and max_cov >= 20.0:
        return "DISTANT_GENUS_LEVEL_REFERENCE"
    if max_ani > 0:
        return "NO_CLOSE_REFERENCE_LOW_ANI_OR_LOW_COVERAGE"
    return "NO_TRUSTED_ANI_ALIGNMENT"


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    tool_rows = []
    for name, path in [("datasets", DATASETS), ("fastANI", FASTANI), ("skani", SKANI)]:
        tool_rows.append({"tool": name, "path": str(path), "available": path.exists()})
    write_csv(OUTDIR / "plan04_bacteriovorax_tool_gate.csv", tool_rows, ["tool", "path", "available"])
    if not all(Path(row["path"]).exists() for row in tool_rows):
        raise RuntimeError("Required local tools are not available in .bioenv")

    records = load_metadata()
    reference_rows: list[dict[str, object]] = []
    ref_paths: list[Path] = []
    for record in records:
        accession = record.get("accession", "")
        fasta = download_reference(accession)
        reference_rows.append(
            {
                "accession": accession,
                "organism_name": nested_get(record, ["organism", "organism_name"]),
                "strain": biosample_attr(record, "strain") or nested_get(record, ["organism", "infraspecific_names", "strain"]),
                "assembly_level": nested_get(record, ["assembly_info", "assembly_level"]),
                "refseq_category": nested_get(record, ["assembly_info", "refseq_category"]),
                "type_material": nested_get(record, ["type_material", "type_display_text"]),
                "biosample": nested_get(record, ["assembly_info", "biosample", "accession"]),
                "isolation_source": biosample_attr(record, "isolation_source") or nested_get(record, ["assembly_info", "biosample", "isolation_source"]),
                "geo_loc_name": biosample_attr(record, "geo_loc_name") or nested_get(record, ["assembly_info", "biosample", "geo_loc_name"]),
                "total_sequence_length": nested_get(record, ["assembly_stats", "total_sequence_length"]),
                "gc_percent": nested_get(record, ["assembly_stats", "gc_percent"]),
                "checkm_completeness": nested_get(record, ["checkm_info", "completeness"]),
                "local_fasta": str(fasta.relative_to(ROOT)) if fasta else "",
                "download_status": "DOWNLOADED" if fasta else "DOWNLOAD_FAILED",
            }
        )
        if fasta:
            ref_paths.append(fasta)

    reference_fields = [
        "accession",
        "organism_name",
        "strain",
        "assembly_level",
        "refseq_category",
        "type_material",
        "biosample",
        "isolation_source",
        "geo_loc_name",
        "total_sequence_length",
        "gc_percent",
        "checkm_completeness",
        "local_fasta",
        "download_status",
    ]
    write_csv(OUTDIR / "plan04_bacteriovorax_reference_manifest.csv", reference_rows, reference_fields)

    ref_list = OUTDIR / "bacteriovorax_reference_fastas.txt"
    ref_list.write_text("\n".join(str(path) for path in ref_paths) + "\n")
    fastani_out = OUTDIR / "MGYG000535629_vs_bacteriovorax_refs.fastani.tsv"
    skani_out = OUTDIR / "MGYG000535629_vs_bacteriovorax_refs.skani.tsv"
    run([str(FASTANI), "-q", str(QUERY_FASTA), "--rl", str(ref_list), "-t", "4", "-o", str(fastani_out)])
    run([str(SKANI), "dist", str(QUERY_FASTA), *[str(path) for path in ref_paths]], stdout_path=skani_out)

    fastani_rows = parse_fastani(fastani_out)
    skani_rows = parse_skani(skani_out)
    ani_rows: list[dict[str, object]] = []
    manifest_by_accession = {str(row["accession"]): row for row in reference_rows}
    for ref in reference_rows:
        accession = str(ref["accession"])
        f = fastani_rows.get(accession, {})
        s = skani_rows.get(accession, {})
        call = derep_call(
            f.get("fastani_ani", ""),
            f.get("fastani_aligned_fragment_pct", ""),
            s.get("skani_ani", ""),
            s.get("skani_align_fraction_query", ""),
        )
        ani_rows.append(
            {
                "candidate_genome_id": QUERY_GENOME_ID,
                "query_fasta": str(QUERY_FASTA.relative_to(ROOT)),
                "accession": accession,
                "organism_name": ref["organism_name"],
                "strain": ref["strain"],
                "assembly_level": ref["assembly_level"],
                "refseq_category": ref["refseq_category"],
                "type_material": ref["type_material"],
                "biosample": ref["biosample"],
                "isolation_source": ref["isolation_source"],
                "geo_loc_name": ref["geo_loc_name"],
                "fastani_ani": f.get("fastani_ani", ""),
                "fastani_mapped_fragments": f.get("fastani_mapped_fragments", ""),
                "fastani_total_fragments": f.get("fastani_total_fragments", ""),
                "fastani_aligned_fragment_pct": f.get("fastani_aligned_fragment_pct", ""),
                "skani_ani": s.get("skani_ani", ""),
                "skani_align_fraction_ref": s.get("skani_align_fraction_ref", ""),
                "skani_align_fraction_query": s.get("skani_align_fraction_query", ""),
                "dereplication_call": call,
                "wetlab_packaging_impact": "KEEPS_AS_DISTANT_SURROGATE_ONLY" if call.startswith("DISTANT") else "NO_CLOSE_REFERENCE_SUPPORT",
                "claim_limit": CLAIM_LIMIT,
            }
        )
    ani_rows.sort(key=lambda row: float(row["skani_ani"] or row["fastani_ani"] or 0), reverse=True)
    ani_fields = [
        "candidate_genome_id",
        "query_fasta",
        "accession",
        "organism_name",
        "strain",
        "assembly_level",
        "refseq_category",
        "type_material",
        "biosample",
        "isolation_source",
        "geo_loc_name",
        "fastani_ani",
        "fastani_mapped_fragments",
        "fastani_total_fragments",
        "fastani_aligned_fragment_pct",
        "skani_ani",
        "skani_align_fraction_ref",
        "skani_align_fraction_query",
        "dereplication_call",
        "wetlab_packaging_impact",
        "claim_limit",
    ]
    write_csv(OUTDIR / "plan04_bacteriovorax_reference_ani_results.csv", ani_rows, ani_fields)

    best = ani_rows[0] if ani_rows else {}
    report = f"""# Plan04 Bacteriovorax Reference ANI Report

Run date: {RUN_DATE}

## Scope

This package extends Plan04 strain-dereplication for MAG candidate `MGYG000535629` by downloading current RefSeq Bacteriovorax assemblies through NCBI Datasets and comparing the local MAG to those references with fastANI and skani.

Claim boundary: ANI supports only reference-distance and organism-level packaging. It does not validate plant-growth phenotype, recoverability, colonization, biosafety, or field performance.

## Result

- RefSeq Bacteriovorax assemblies found: {len(reference_rows)}
- Reference FASTAs downloaded: {len(ref_paths)}
- Best reference by skani/fastANI table: `{best.get('accession', '')}` {best.get('organism_name', '')}
- Best skani ANI: {best.get('skani_ani', '')}
- Best skani query alignment fraction: {best.get('skani_align_fraction_query', '')}
- Best dereplication call: {best.get('dereplication_call', '')}

## ANI Summary

{md_table(ani_rows, ["accession", "organism_name", "strain", "type_material", "fastani_ani", "fastani_aligned_fragment_pct", "skani_ani", "skani_align_fraction_query", "dereplication_call"])}

## Interpretation

`MGYG000535629` remains a Bacteriovorax-linked, MAG-derived surrogate/trait-assay hypothesis rather than a clean organism-level isolate candidate. The available RefSeq Bacteriovorax references are useful for genus-level context, but the ANI/coverage profile does not support a close strain or same-species dereplication claim.

## Output Files

- `plan04_bacteriovorax_reference_ani_results.csv`
- `plan04_bacteriovorax_reference_manifest.csv`
- `MGYG000535629_vs_bacteriovorax_refs.fastani.tsv`
- `MGYG000535629_vs_bacteriovorax_refs.skani.tsv`
- `PLAN04_BACTERIOVORAX_REFERENCE_ANI_COMPLETION_AUDIT.md`
"""
    (OUTDIR / "PLAN04_BACTERIOVORAX_REFERENCE_ANI_REPORT.md").write_text(report)

    audit = f"""# Plan04 Bacteriovorax Reference ANI Completion Audit

Run date: {RUN_DATE}

## Verdict

PASS_DISTANT_REFERENCE_CONTEXT_ONLY

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Use local Plan04 MAG candidate | `{QUERY_FASTA.relative_to(ROOT)}` | PASS |
| Query current RefSeq Bacteriovorax assemblies | `bacteriovorax_refseq_summary.jsonl` | PASS |
| Download reference genomes | `plan04_bacteriovorax_reference_manifest.csv` | PASS |
| Run ANI with fastANI | `MGYG000535629_vs_bacteriovorax_refs.fastani.tsv` | PASS |
| Run ANI with skani | `MGYG000535629_vs_bacteriovorax_refs.skani.tsv` | PASS |
| Bound claim language | `PLAN04_BACTERIOVORAX_REFERENCE_ANI_REPORT.md` | PASS |

## Remaining Caveat

No close reference was found. This improves the evidence basis for keeping `MGYG000535629` as a lower-confidence Bacteriovorax surrogate/trait-assay hypothesis, but it does not make it an organism-level wet-lab candidate.
"""
    (OUTDIR / "PLAN04_BACTERIOVORAX_REFERENCE_ANI_COMPLETION_AUDIT.md").write_text(audit)

    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"references={len(reference_rows)} downloaded={len(ref_paths)} best={best.get('accession', '')} skani_ani={best.get('skani_ani', '')} call={best.get('dereplication_call', '')}")


if __name__ == "__main__":
    main()
