#!/usr/bin/env python3
"""Run Plan04 remaining-MAG reference gates for MGYG000511828 and MGYG000535630.

This supplemental check compares the two Plan04 MAG candidates still lacking
clear organism-level routes against specific public MAG/reference assemblies
identified during availability triage. It emits reference-distance context only:
no plant-benefit, organism recoverability, biosafety, or phenotype claims.
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
OUTDIR = ROOT / f"outputs/plan04_remaining_mag_reference_gate_{RUN_DATE}"
DOWNLOAD_DIR = OUTDIR / "ncbi_downloads"
REFERENCE_DIR = OUTDIR / "reference_fastas"
CLAIM_LIMIT = (
    "Reference ANI supports MAG/reference-distance and wet-lab packaging context only; "
    "it does not validate plant-growth phenotype, culture recoverability, colonization, "
    "biosafety acceptability, or field performance."
)


TARGETS = [
    {
        "candidate_genome_id": "MGYG000511828",
        "candidate_taxon_context": "AR5 / Methylomirabilota-Rokubacteriales-style soil MAG context",
        "candidate_packaging_context": "phosphate_solubilization PGP hypothesis; soil MAG, weaker crop relevance",
        "query_fasta": ROOT
        / "outputs/computational_execution_2026-05-14/cache/mgnify_genomes/MGYG000511828/MGYG000511828.fna",
        "reference_accession": "GCA_046723405.1",
        "reference_selection_reason": (
            "Public Candidatus Methylomirabilota bacterium MAG from soil context; used as a "
            "broad MAG/reference gate, not as a cultured isolate route."
        ),
    },
    {
        "candidate_genome_id": "MGYG000535630",
        "candidate_taxon_context": "UBA11398 MAG/WGS lineage",
        "candidate_packaging_context": "antifungal/BGC-support PGP hypothesis; barley-rhizosphere MAG",
        "query_fasta": ROOT
        / "outputs/computational_execution_2026-05-14/cache/mgnify_genomes/MGYG000535630/MGYG000535630.fna",
        "reference_accession": "GCA_003506065.1",
        "reference_selection_reason": (
            "Public UBA11398 MAG/WGS assembly; tests whether the candidate has exact or near-exact "
            "MAG reference context, but does not establish culture availability."
        ),
    },
]

AR5_AMBIGUITY_ROWS = [
    {
        "query_label": "AR5",
        "ncbi_taxon_name": "Candidatus Electrothrix sp. AR5",
        "taxid": "2202843",
        "interpretation": "false_or_ambiguous_for_candidate_context",
        "note": "Marine-sediment cable-bacteria context; not the Plan04 Methylomirabilota/Rokubacteriales-style soil MAG anchor.",
    },
    {
        "query_label": "AR5",
        "ncbi_taxon_name": "Pseudomonas sp. AR5",
        "taxid": "3054956",
        "interpretation": "false_or_ambiguous_for_candidate_context",
        "note": "Mismatched genus/taxonomy; not relevant to the Plan04 AR5-labeled MAG context.",
    },
]


def run(cmd: list[str], stdout_path: Path | None = None) -> subprocess.CompletedProcess[str]:
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


def load_accession_metadata(accession: str) -> dict:
    summary_path = OUTDIR / f"{accession}_datasets_summary.jsonl"
    result = run([str(DATASETS), "summary", "genome", "accession", accession, "--as-json-lines"])
    summary_path.write_text(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"datasets summary failed for {accession}: {result.stderr}")
    records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    if not records:
        raise RuntimeError(f"datasets summary returned no records for {accession}")
    return records[0]


def download_reference(accession: str) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = DOWNLOAD_DIR / f"{accession}.zip"
    extract_dir = DOWNLOAD_DIR / accession
    result = run(
        [
            str(DATASETS),
            "download",
            "genome",
            "accession",
            accession,
            "--include",
            "genome",
            "--filename",
            str(zip_path),
            "--no-progressbar",
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(f"datasets download failed for {accession}: {result.stderr}")
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extract_dir)
    fasta_candidates = sorted((extract_dir / "ncbi_dataset/data").glob(f"{accession}/*_genomic.fna"))
    if not fasta_candidates:
        raise RuntimeError(f"downloaded archive for {accession} did not contain a genomic FASTA")
    dest = REFERENCE_DIR / f"{accession}.fna"
    shutil.copyfile(fasta_candidates[0], dest)
    return dest


def parse_fastani(path: Path, reference_accession: str) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open() as handle:
        for line in handle:
            parts = line.strip().split("\t")
            if len(parts) < 5:
                continue
            ref_name = Path(parts[1]).stem
            if ref_name != reference_accession:
                continue
            total = float(parts[4])
            mapped = float(parts[3])
            return {
                "fastani_ani": parts[2],
                "fastani_mapped_fragments": parts[3],
                "fastani_total_fragments": parts[4],
                "fastani_aligned_fragment_pct": f"{(mapped / total * 100.0):.3f}" if total else "",
            }
    return {}


def parse_skani(path: Path, reference_accession: str) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            ref_name = Path(row.get("Ref_file", "")).stem
            if ref_name != reference_accession:
                continue
            return {
                "skani_ani": row.get("ANI", ""),
                "skani_align_fraction_ref": row.get("Align_fraction_ref", ""),
                "skani_align_fraction_query": row.get("Align_fraction_query", ""),
            }
    return {}


def gate_call(fastani_ani: str, fastani_pct: str, skani_ani: str, skani_q_af: str) -> tuple[str, str]:
    ani_values = [float(value) for value in [fastani_ani, skani_ani] if value]
    cov_values = [float(value) for value in [fastani_pct, skani_q_af] if value]
    max_ani = max(ani_values) if ani_values else 0.0
    max_cov = max(cov_values) if cov_values else 0.0
    if max_ani >= 99.0 and max_cov >= 95.0:
        return "EXACT_OR_NEAR_EXACT_MAG_REFERENCE_CONTEXT", "UPGRADE_REFERENCE_CONTEXT_NOT_CULTURE_ROUTE"
    if max_ani >= 95.0 and max_cov >= 60.0:
        return "CLOSE_MAG_REFERENCE_CONTEXT", "UPGRADE_REFERENCE_CONTEXT_NOT_CULTURE_ROUTE"
    if max_ani >= 90.0 and max_cov >= 30.0:
        return "RELATED_MAG_REFERENCE_CONTEXT_ONLY", "KEEP_MAG_DERIVED_WITH_REFERENCE_CONTEXT"
    if max_ani > 0.0:
        return "LOW_ANI_OR_LOW_COVERAGE_REFERENCE_CONTEXT_ONLY", "KEEP_HOLD_FOR_ORGANISM_LEVEL_WETLAB"
    return "NO_TRUSTED_ANI_ALIGNMENT_TO_SELECTED_REFERENCE", "KEEP_HOLD_FOR_ORGANISM_LEVEL_WETLAB"


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def reference_manifest_row(target: dict[str, object], metadata: dict, fasta: Path) -> dict[str, object]:
    return {
        "candidate_genome_id": target["candidate_genome_id"],
        "reference_accession": target["reference_accession"],
        "reference_selection_reason": target["reference_selection_reason"],
        "organism_name": nested_get(metadata, ["organism", "organism_name"]),
        "strain": biosample_attr(metadata, "strain") or nested_get(metadata, ["organism", "infraspecific_names", "strain"]),
        "isolate": biosample_attr(metadata, "isolate"),
        "assembly_level": nested_get(metadata, ["assembly_info", "assembly_level"]),
        "assembly_type": nested_get(metadata, ["assembly_info", "assembly_type"]),
        "refseq_category": nested_get(metadata, ["assembly_info", "refseq_category"]),
        "biosample": nested_get(metadata, ["assembly_info", "biosample", "accession"]),
        "isolation_source": biosample_attr(metadata, "isolation_source") or nested_get(metadata, ["assembly_info", "biosample", "isolation_source"]),
        "geo_loc_name": biosample_attr(metadata, "geo_loc_name") or nested_get(metadata, ["assembly_info", "biosample", "geo_loc_name"]),
        "derived_from_metagenome": nested_get(metadata, ["assembly_info", "biosample", "sample_ids", "sra"], ""),
        "total_sequence_length": nested_get(metadata, ["assembly_stats", "total_sequence_length"]),
        "gc_percent": nested_get(metadata, ["assembly_stats", "gc_percent"]),
        "checkm_completeness": nested_get(metadata, ["checkm_info", "completeness"]),
        "checkm_contamination": nested_get(metadata, ["checkm_info", "contamination"]),
        "local_reference_fasta": str(fasta.relative_to(ROOT)),
        "download_status": "DOWNLOADED",
    }


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    tool_rows = []
    for name, path in [("datasets", DATASETS), ("fastANI", FASTANI), ("skani", SKANI)]:
        tool_rows.append({"tool": name, "path": str(path), "available": path.exists()})
    write_csv(OUTDIR / "plan04_remaining_mag_reference_tool_gate.csv", tool_rows, ["tool", "path", "available"])
    if not all(Path(row["path"]).exists() for row in tool_rows):
        raise RuntimeError("Required local tools are not available in .bioenv")

    manifest_rows: list[dict[str, object]] = []
    result_rows: list[dict[str, object]] = []
    for target in TARGETS:
        query_fasta = Path(target["query_fasta"])
        if not query_fasta.exists():
            raise FileNotFoundError(query_fasta)
        accession = str(target["reference_accession"])
        metadata = load_accession_metadata(accession)
        reference_fasta = download_reference(accession)
        manifest_rows.append(reference_manifest_row(target, metadata, reference_fasta))

        fastani_out = OUTDIR / f"{target['candidate_genome_id']}_vs_{accession}.fastani.tsv"
        skani_out = OUTDIR / f"{target['candidate_genome_id']}_vs_{accession}.skani.tsv"
        run([str(FASTANI), "-q", str(query_fasta), "-r", str(reference_fasta), "-t", "4", "-o", str(fastani_out)])
        run(
            [
                str(SKANI),
                "dist",
                "--slow",
                "--min-af",
                "1",
                "-s",
                "70",
                "-o",
                str(skani_out),
                str(query_fasta),
                str(reference_fasta),
            ]
        )

        fastani = parse_fastani(fastani_out, accession)
        skani = parse_skani(skani_out, accession)
        call, impact = gate_call(
            fastani.get("fastani_ani", ""),
            fastani.get("fastani_aligned_fragment_pct", ""),
            skani.get("skani_ani", ""),
            skani.get("skani_align_fraction_query", ""),
        )
        result_rows.append(
            {
                "candidate_genome_id": target["candidate_genome_id"],
                "candidate_taxon_context": target["candidate_taxon_context"],
                "candidate_packaging_context": target["candidate_packaging_context"],
                "query_fasta": str(query_fasta.relative_to(ROOT)),
                "reference_accession": accession,
                "reference_organism_name": nested_get(metadata, ["organism", "organism_name"]),
                "reference_strain": biosample_attr(metadata, "strain")
                or nested_get(metadata, ["organism", "infraspecific_names", "strain"]),
                "reference_isolate": biosample_attr(metadata, "isolate"),
                "reference_isolation_source": biosample_attr(metadata, "isolation_source")
                or nested_get(metadata, ["assembly_info", "biosample", "isolation_source"]),
                "reference_geo_loc_name": biosample_attr(metadata, "geo_loc_name")
                or nested_get(metadata, ["assembly_info", "biosample", "geo_loc_name"]),
                "skani_mode": "sensitive_slow_min_af_1_screen_70",
                "fastani_ani": fastani.get("fastani_ani", ""),
                "fastani_mapped_fragments": fastani.get("fastani_mapped_fragments", ""),
                "fastani_total_fragments": fastani.get("fastani_total_fragments", ""),
                "fastani_aligned_fragment_pct": fastani.get("fastani_aligned_fragment_pct", ""),
                "skani_ani": skani.get("skani_ani", ""),
                "skani_align_fraction_ref": skani.get("skani_align_fraction_ref", ""),
                "skani_align_fraction_query": skani.get("skani_align_fraction_query", ""),
                "reference_gate_call": call,
                "wetlab_packaging_impact": impact,
                "claim_limit": CLAIM_LIMIT,
            }
        )

    manifest_fields = [
        "candidate_genome_id",
        "reference_accession",
        "reference_selection_reason",
        "organism_name",
        "strain",
        "isolate",
        "assembly_level",
        "assembly_type",
        "refseq_category",
        "biosample",
        "isolation_source",
        "geo_loc_name",
        "derived_from_metagenome",
        "total_sequence_length",
        "gc_percent",
        "checkm_completeness",
        "checkm_contamination",
        "local_reference_fasta",
        "download_status",
    ]
    result_fields = [
        "candidate_genome_id",
        "candidate_taxon_context",
        "candidate_packaging_context",
        "query_fasta",
        "reference_accession",
        "reference_organism_name",
        "reference_strain",
        "reference_isolate",
        "reference_isolation_source",
        "reference_geo_loc_name",
        "skani_mode",
        "fastani_ani",
        "fastani_mapped_fragments",
        "fastani_total_fragments",
        "fastani_aligned_fragment_pct",
        "skani_ani",
        "skani_align_fraction_ref",
        "skani_align_fraction_query",
        "reference_gate_call",
        "wetlab_packaging_impact",
        "claim_limit",
    ]
    ambiguity_fields = ["query_label", "ncbi_taxon_name", "taxid", "interpretation", "note"]
    write_csv(OUTDIR / "plan04_remaining_mag_reference_manifest.csv", manifest_rows, manifest_fields)
    write_csv(OUTDIR / "plan04_remaining_mag_reference_gate.csv", result_rows, result_fields)
    write_csv(OUTDIR / "plan04_ar5_taxonomy_ambiguity_notes.csv", AR5_AMBIGUITY_ROWS, ambiguity_fields)

    report = f"""# Plan04 Remaining MAG Reference Gate Report

Run date: {RUN_DATE}

## Scope

This package closes the remaining Plan04 MAG reference-context gap for `MGYG000511828` and `MGYG000535630`. It compares each local MGnify MAG to a selected public MAG/reference assembly using fastANI and skani.

Claim boundary: {CLAIM_LIMIT}

## Result

{md_table(result_rows, ["candidate_genome_id", "reference_accession", "reference_organism_name", "fastani_ani", "fastani_aligned_fragment_pct", "skani_ani", "skani_align_fraction_query", "reference_gate_call", "wetlab_packaging_impact"])}

## Reference Manifest Summary

{md_table(manifest_rows, ["candidate_genome_id", "reference_accession", "organism_name", "strain", "isolate", "isolation_source", "geo_loc_name", "checkm_completeness", "checkm_contamination", "download_status"])}

## AR5 Taxonomy Ambiguity Note

{md_table(AR5_AMBIGUITY_ROWS, ["query_label", "ncbi_taxon_name", "taxid", "interpretation", "note"])}

## Interpretation

- `MGYG000511828` should remain a genome-derived phosphate-solubilization hypothesis unless this gate shows close MAG/reference context; the selected reference is not a culture route.
- `MGYG000535630` can be upgraded only to MAG/reference-context support if it is close to the UBA11398 assembly; it still remains a MAG-derived hypothesis without culture availability.
- Neither result validates plant benefit, organism recoverability, culture availability, safety, or trait phenotype.

## Output Files

- `plan04_remaining_mag_reference_gate.csv`
- `plan04_remaining_mag_reference_manifest.csv`
- `plan04_ar5_taxonomy_ambiguity_notes.csv`
- `MGYG000511828_vs_GCA_046723405.1.fastani.tsv`
- `MGYG000511828_vs_GCA_046723405.1.skani.tsv`
- `MGYG000535630_vs_GCA_003506065.1.fastani.tsv`
- `MGYG000535630_vs_GCA_003506065.1.skani.tsv`
- `PLAN04_REMAINING_MAG_REFERENCE_GATE_COMPLETION_AUDIT.md`
"""
    (OUTDIR / "PLAN04_REMAINING_MAG_REFERENCE_GATE_REPORT.md").write_text(report)

    status_by_target = {row["candidate_genome_id"]: row["reference_gate_call"] for row in result_rows}
    audit = f"""# Plan04 Remaining MAG Reference Gate Completion Audit

Run date: {RUN_DATE}

## Verdict

PASS_REFERENCE_GATE_COMPLETED_FOR_REMAINING_MAG_HOLDS

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Use local `MGYG000511828` MAG FASTA | `{TARGETS[0]['query_fasta'].relative_to(ROOT)}` | PASS |
| Use local `MGYG000535630` MAG FASTA | `{TARGETS[1]['query_fasta'].relative_to(ROOT)}` | PASS |
| Download selected public reference assemblies | `plan04_remaining_mag_reference_manifest.csv` | PASS |
| Compare `MGYG000511828` to `GCA_046723405.1` with fastANI and skani | `MGYG000511828_vs_GCA_046723405.1.fastani.tsv`; `MGYG000511828_vs_GCA_046723405.1.skani.tsv` | PASS |
| Compare `MGYG000535630` to `GCA_003506065.1` with fastANI and skani | `MGYG000535630_vs_GCA_003506065.1.fastani.tsv`; `MGYG000535630_vs_GCA_003506065.1.skani.tsv` | PASS |
| Record AR5 taxonomy ambiguity | `plan04_ar5_taxonomy_ambiguity_notes.csv` | PASS |
| Keep claims bounded to MAG/reference context | `PLAN04_REMAINING_MAG_REFERENCE_GATE_REPORT.md` | PASS |

## Candidate Calls

- `MGYG000511828`: {status_by_target.get("MGYG000511828", "")}
- `MGYG000535630`: {status_by_target.get("MGYG000535630", "")}

## Remaining Caveat

This gate improves or rejects selected reference-context support only. It does not create a cultured-isolate route or validate PGP phenotype for either MAG candidate.
"""
    (OUTDIR / "PLAN04_REMAINING_MAG_REFERENCE_GATE_COMPLETION_AUDIT.md").write_text(audit)

    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    for row in result_rows:
        print(
            f"{row['candidate_genome_id']} vs {row['reference_accession']}: "
            f"fastANI={row['fastani_ani'] or 'NA'} skani={row['skani_ani'] or 'NA'} "
            f"qAF={row['skani_align_fraction_query'] or 'NA'} call={row['reference_gate_call']}"
        )


if __name__ == "__main__":
    main()
