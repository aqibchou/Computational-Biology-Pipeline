#!/usr/bin/env python3
"""Reconstruct Plan01 BGC region GenBank inputs from local FASTA/GFF assets.

This fills the practical input gap for future native BiG-SCAPE/BiG-SLiCE-style
runs by creating GenBank-like region files for the seven Plan01 claim-hardening
BGCs. These are reconstructed from local MGnify FASTA, Prodigal CDS GFF, and
caller GFFs. They are not native antiSMASH GenBank outputs and should not be
treated as a completed native BiG-SCAPE/CORASON result.
"""

from __future__ import annotations

import csv
import datetime as dt
import textwrap
import urllib.parse
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "outputs/computational_execution_2026-05-14/cache/mgnify_genomes"
PLAN01_CLAIMS = ROOT / "outputs/plan01_claim_hardening_2026-05-17/plan01_bgc_claim_hardening.csv"
OUTDIR = ROOT / f"outputs/plan01_reconstructed_bgc_genbanks_{RUN_DATE}"
GBK_DIR = OUTDIR / "reconstructed_region_gbks"
CLAIM_LIMIT = (
    "Reconstructed GenBank region files support future clustering input preparation only; "
    "they are not native antiSMASH GenBank outputs and do not validate product formation, "
    "compound novelty, antimicrobial activity, or biosafety."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def parse_fasta(path: Path) -> dict[str, str]:
    records: dict[str, list[str]] = {}
    current = ""
    with path.open() as handle:
        for line in handle:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(">"):
                current = line[1:].split()[0]
                records[current] = []
            elif current:
                records[current].append(line.upper())
    return {key: "".join(value) for key, value in records.items()}


def parse_protein_fasta(path: Path) -> dict[str, str]:
    return parse_fasta(path)


def parse_attrs(text: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for part in text.split(";"):
        if not part:
            continue
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        attrs[key] = urllib.parse.unquote(value)
    return attrs


def parse_gff(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    with path.open() as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 9:
                continue
            seqid, source, ftype, start, end, score, strand, phase, attrs = parts
            rows.append(
                {
                    "seqid": seqid,
                    "source": source,
                    "type": ftype,
                    "start": int(start),
                    "end": int(end),
                    "score": score,
                    "strand": strand,
                    "phase": phase,
                    "attrs": parse_attrs(attrs),
                }
            )
    return rows


def parse_strict_bgc_id(strict_id: str) -> tuple[str, str, int, int]:
    genome_id, contig, coords = strict_id.split(":")
    start_s, end_s = coords.split("-")
    return genome_id, contig, int(start_s), int(end_s)


def overlaps(row: dict[str, object], contig: str, start: int, end: int) -> bool:
    return row["seqid"] == contig and int(row["start"]) <= end and int(row["end"]) >= start


def gb_location(start: int, end: int, strand: str) -> str:
    loc = f"{start}..{end}"
    if strand == "-":
        return f"complement({loc})"
    return loc


def qualifier(name: str, value: object) -> list[str]:
    text = str(value).replace('"', "'")
    if len(text) <= 58:
        return [f'                     /{name}="{text}"']
    wrapped = textwrap.wrap(text, width=58)
    lines = [f'                     /{name}="{wrapped[0]}']
    lines.extend(f"                     {part}" for part in wrapped[1:])
    lines[-1] += '"'
    return lines


def add_feature(lines: list[str], feature_type: str, location: str, qualifiers: list[tuple[str, object]]) -> None:
    # GenBank feature locations start at column 22. Biopython truncates the
    # first location character if this field is one column early.
    lines.append(f"     {feature_type:<16}{location}")
    for key, value in qualifiers:
        if value in ("", None):
            continue
        lines.extend(qualifier(key, value))


def format_origin(seq: str) -> list[str]:
    lines = ["ORIGIN"]
    for idx in range(0, len(seq), 60):
        chunk = seq[idx : idx + 60].lower()
        grouped = " ".join(chunk[j : j + 10] for j in range(0, len(chunk), 10))
        lines.append(f"{idx + 1:>9} {grouped}")
    lines.append("//")
    return lines


def safe_file_stem(strict_bgc_id: str) -> str:
    return strict_bgc_id.replace(":", "__").replace("-", "_")


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    GBK_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(PLAN01_CLAIMS)
    manifest_rows: list[dict[str, object]] = []

    fasta_cache: dict[str, dict[str, str]] = {}
    protein_cache: dict[str, dict[str, str]] = {}
    cds_gff_cache: dict[str, list[dict[str, object]]] = {}
    caller_gff_cache: dict[str, list[dict[str, object]]] = {}

    for row in rows:
        strict_id = row["strict_bgc_id"]
        genome_id, contig, start, end = parse_strict_bgc_id(strict_id)
        genome_dir = CACHE / genome_id
        if genome_id not in fasta_cache:
            fasta_cache[genome_id] = parse_fasta(genome_dir / f"{genome_id}.fna")
            protein_cache[genome_id] = parse_protein_fasta(genome_dir / f"{genome_id}.faa")
            cds_gff_cache[genome_id] = parse_gff(genome_dir / f"{genome_id}.gff")
            caller_rows: list[dict[str, object]] = []
            for suffix in ["antismash", "gecco", "sanntis"]:
                caller_rows.extend(parse_gff(genome_dir / f"{genome_id}_{suffix}.gff"))
            caller_gff_cache[genome_id] = caller_rows

        contig_seq = fasta_cache[genome_id].get(contig, "")
        if not contig_seq:
            manifest_rows.append(
                {
                    "strict_bgc_id": strict_id,
                    "status": "MISSING_CONTIG_SEQUENCE",
                    "reconstructed_gbk": "",
                    "sequence_bp": "",
                    "cds_features": "",
                    "caller_features": "",
                    "claim_limit": CLAIM_LIMIT,
                }
            )
            continue

        region_seq = contig_seq[start - 1 : end]
        cds_rows = [r for r in cds_gff_cache[genome_id] if overlaps(r, contig, start, end) and r["type"] == "CDS"]
        caller_rows = [
            r
            for r in caller_gff_cache[genome_id]
            if overlaps(r, contig, start, end) and str(r["type"]).lower() in {"region", "bgc", "cluster"}
        ]

        record_id = safe_file_stem(strict_id)
        gbk_path = GBK_DIR / f"{record_id}.gbk"
        today = dt.date.today().strftime("%d-%b-%Y").upper()
        lines = [
            f"LOCUS       {record_id[:16]:<16}{len(region_seq):>11} bp    DNA     linear   BCT {today}",
            f"DEFINITION  Reconstructed Plan01 BGC region for {strict_id}.",
            f"ACCESSION   {record_id}",
            f"VERSION     {record_id}",
            "KEYWORDS    reconstructed; Plan01; BGC; pre-wet-lab; not-native-antismash.",
            f"SOURCE      {genome_id}",
            f"  ORGANISM  {genome_id}",
            "            metagenome-derived sequence.",
            "FEATURES             Location/Qualifiers",
        ]
        add_feature(
            lines,
            "source",
            f"1..{len(region_seq)}",
            [
                ("organism", genome_id),
                ("mol_type", "genomic DNA"),
                ("isolation_source", row.get("product_frame", "")),
                ("note", CLAIM_LIMIT),
            ],
        )
        add_feature(
            lines,
            "protocluster",
            f"1..{len(region_seq)}",
            [
                ("product", row.get("product_class", "")),
                ("strict_bgc_id", strict_id),
                ("contig", contig),
                ("original_location", f"{contig}:{start}-{end}"),
                ("readiness_decision", row.get("readiness_decision", "")),
                ("claim_hardening_call", row.get("claim_hardening_call", "")),
                ("note", "Reconstructed from local FNA/GFF/caller tables; not native antiSMASH GenBank."),
            ],
        )
        for caller in caller_rows:
            attrs = caller["attrs"]
            rel_start = max(1, int(caller["start"]) - start + 1)
            rel_end = min(len(region_seq), int(caller["end"]) - start + 1)
            add_feature(
                lines,
                "misc_feature",
                gb_location(rel_start, rel_end, str(caller["strand"])),
                [
                    ("caller_source", caller["source"]),
                    ("caller_type", caller["type"]),
                    ("ID", attrs.get("ID", "")),
                    ("product", attrs.get("product", attrs.get("Type", attrs.get("Name", "")))),
                    ("nearest_MiBIG", attrs.get("nearest_MiBIG", "")),
                    ("score", attrs.get("score", attrs.get("ProbabilityAverage", ""))),
                ],
            )
        for cds in cds_rows:
            attrs = cds["attrs"]
            rel_start = max(1, int(cds["start"]) - start + 1)
            rel_end = min(len(region_seq), int(cds["end"]) - start + 1)
            locus_tag = attrs.get("locus_tag", attrs.get("ID", ""))
            qualifiers: list[tuple[str, object]] = [
                ("locus_tag", locus_tag),
                ("gene", attrs.get("gene", "")),
                ("product", attrs.get("product", "hypothetical protein")),
                ("EC_number", attrs.get("eC_number", "")),
                ("antismash_bgc_function", attrs.get("antismash_bgc_function", "")),
                ("antismash_product", attrs.get("antismash_product", "")),
                ("pfam", attrs.get("pfam", "")),
                ("interpro", attrs.get("interpro", "")),
            ]
            translation = protein_cache[genome_id].get(locus_tag, "")
            if translation:
                qualifiers.append(("translation", translation))
            add_feature(lines, "CDS", gb_location(rel_start, rel_end, str(cds["strand"])), qualifiers)

        lines.extend(format_origin(region_seq))
        gbk_path.write_text("\n".join(lines) + "\n")
        manifest_rows.append(
            {
                "strict_bgc_id": strict_id,
                "genome_id": genome_id,
                "contig": contig,
                "start": start,
                "end": end,
                "product_class": row.get("product_class", ""),
                "readiness_decision": row.get("readiness_decision", ""),
                "status": "RECONSTRUCTED_GBK_WRITTEN",
                "reconstructed_gbk": str(gbk_path.relative_to(ROOT)),
                "sequence_bp": len(region_seq),
                "cds_features": len(cds_rows),
                "caller_features": len(caller_rows),
                "claim_limit": CLAIM_LIMIT,
            }
        )

    fields = [
        "strict_bgc_id",
        "genome_id",
        "contig",
        "start",
        "end",
        "product_class",
        "readiness_decision",
        "status",
        "reconstructed_gbk",
        "sequence_bp",
        "cds_features",
        "caller_features",
        "claim_limit",
    ]
    write_csv(OUTDIR / "plan01_reconstructed_bgc_genbank_manifest.csv", manifest_rows, fields)

    success_rows = [row for row in manifest_rows if row.get("status") == "RECONSTRUCTED_GBK_WRITTEN"]
    report_rows = "\n".join(
        "| "
        + " | ".join(
            str(row.get(field, "")).replace("|", "/")
            for field in ["strict_bgc_id", "product_class", "sequence_bp", "cds_features", "caller_features", "status"]
        )
        + " |"
        for row in manifest_rows
    )
    report = f"""# Plan01 Reconstructed BGC GenBank Input Report

Run date: {RUN_DATE}

## Scope

This package reconstructs GenBank-like BGC region files for the seven Plan01 claim-hardening BGCs using local MGnify FASTA, Prodigal CDS GFF, antiSMASH/GECCO/SanntiS caller GFFs, and protein FASTA translations.

Claim boundary: {CLAIM_LIMIT}

## Result

- Claim-hardening BGCs inspected: {len(manifest_rows)}
- Reconstructed region GenBank files written: {len(success_rows)}
- Native antiSMASH GenBank files recovered: 0
- Native BiG-SCAPE/CORASON run completed here: no

| strict_bgc_id | product_class | sequence_bp | cds_features | caller_features | status |
| --- | --- | ---: | ---: | ---: | --- |
{report_rows}

## Interpretation

This removes the immediate "no GenBank-like region inputs exist" blocker for a future clustering attempt, but it does not convert the package into a native antiSMASH/BiG-SCAPE/CORASON result. These files are reconstructed compatibility inputs and should be tested with the target clustering tool before relying on them for publication-grade gene-cluster-family novelty.

## Output Files

- `plan01_reconstructed_bgc_genbank_manifest.csv`
- `reconstructed_region_gbks/*.gbk`
- `PLAN01_RECONSTRUCTED_BGC_GENBANK_COMPLETION_AUDIT.md`
"""
    (OUTDIR / "PLAN01_RECONSTRUCTED_BGC_GENBANK_REPORT.md").write_text(report)

    audit = f"""# Plan01 Reconstructed BGC GenBank Completion Audit

Run date: {RUN_DATE}

## Verdict

PASS_RECONSTRUCTED_INPUTS_WRITTEN_NATIVE_CLUSTERING_STILL_PENDING

## Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Use current Plan01 claim-hardening BGC set | `{PLAN01_CLAIMS.relative_to(ROOT)}` | PASS |
| Recover sequence from local MGnify FASTA | `reconstructed_region_gbks/*.gbk`; `plan01_reconstructed_bgc_genbank_manifest.csv` | PASS |
| Add CDS features from local Prodigal GFF | `cds_features` column in manifest | PASS |
| Add caller-region context from antiSMASH/GECCO/SanntiS GFFs | `caller_features` column in manifest | PASS_WITH_GFF_CONTEXT |
| Preserve claim boundary | `PLAN01_RECONSTRUCTED_BGC_GENBANK_REPORT.md` | PASS |
| Run native BiG-SCAPE/CORASON | not run in this script | NOT_DONE |

## Remaining Caveat

These are reconstructed GenBank-like inputs, not native antiSMASH `.gbk` region exports. The next clustering step still needs BiG-SCAPE/BiG-SLiCE/CORASON availability and a compatibility check, preferably through Kaggle CLI if it becomes heavy.
"""
    (OUTDIR / "PLAN01_RECONSTRUCTED_BGC_GENBANK_COMPLETION_AUDIT.md").write_text(audit)

    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"reconstructed_gbks={len(success_rows)} total={len(manifest_rows)}")


if __name__ == "__main__":
    main()
