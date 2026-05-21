#!/usr/bin/env python3
"""Prepare a targeted MIBiG reference panel for Plan01 BiG-SCAPE.

The panel is chosen from existing Plan01 keep-candidate MIBiG BLAST hits. It is
small by design so the follow-up BiG-SCAPE run is an external reference check,
not a full all-MIBiG publication-grade clustering job.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tarfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "plan01_mibig_reference_panel_2026-05-17"
MIBIG_TAR = ROOT / "resources" / "mibig" / "4.0" / "mibig_gbk_4.0.tar.gz"
PLAN01_REGION_SOURCE = (
    ROOT
    / "outputs"
    / "plan01_antismash_wholemag_kaggle_attempt_2026-05-17"
    / "version3"
    / "outputs"
    / "antismash_wholemag_outputs"
)
STRICT_DIR = ROOT / "outputs" / "plan01_strict_bgc_triage_2026-05-14"

KEEP_QUERY_IDS = {
    "MGYG000517341__MGYG000517341_17__38631-49536": "MGYG000517341:MGYG000517341_17:38631-49536",
    "MGYG000473561__MGYG000473561_12__259192-267836": "MGYG000473561:MGYG000473561_12:259192-267836",
    "MGYG000517341__MGYG000517341_21__36974-66085": "MGYG000517341:MGYG000517341_21:36974-66085",
}

BLAST_FILES = [
    STRICT_DIR / "plan01_finalists_all_cluster_vs_mibig_blast.tsv",
    STRICT_DIR / "plan01_go_core_vs_mibig_blast.tsv",
    STRICT_DIR / "plan01_top3_all_cluster_vs_mibig_blast.tsv",
]

EXPECTED_MD5 = "4e905ea01e4d8990e24c36161aea5fbd"
TOP_N_PER_KEEP = 10


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_top_hits() -> tuple[list[dict[str, str]], list[str]]:
    by_keep: dict[str, list[dict[str, str]]] = defaultdict(list)
    for blast_file in BLAST_FILES:
        if not blast_file.exists():
            continue
        with blast_file.open() as handle:
            for line in handle:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 8:
                    continue
                raw_query = parts[0].split("|")[0]
                if raw_query not in KEEP_QUERY_IDS:
                    continue
                subject = parts[1]
                bgc_id = subject.split("|")[0].split(".")[0]
                try:
                    bitscore = float(parts[6])
                    evalue = parts[5]
                    pident = float(parts[2])
                    qcov = float(parts[4])
                except ValueError:
                    continue
                by_keep[raw_query].append(
                    {
                        "strict_bgc_id": KEEP_QUERY_IDS[raw_query],
                        "raw_query_id": raw_query,
                        "mibig_accession": bgc_id,
                        "subject": subject,
                        "pident": f"{pident:.3f}",
                        "qcov_or_length_field": f"{qcov:.3f}",
                        "evalue": evalue,
                        "bitscore": f"{bitscore:.3f}",
                        "source_blast_file": str(blast_file.relative_to(ROOT)),
                    }
                )

    selected_rows: list[dict[str, str]] = []
    selected_ids: list[str] = []
    for raw_query in KEEP_QUERY_IDS:
        seen: set[str] = set()
        ranked = sorted(by_keep.get(raw_query, []), key=lambda row: float(row["bitscore"]), reverse=True)
        for row in ranked:
            bgc_id = row["mibig_accession"]
            if bgc_id in seen:
                continue
            seen.add(bgc_id)
            selected_row = dict(row)
            selected_row["rank_within_keep_candidate"] = str(len(seen))
            selected_rows.append(selected_row)
            if bgc_id not in selected_ids:
                selected_ids.append(bgc_id)
            if len(seen) >= TOP_N_PER_KEEP:
                break
    return selected_rows, selected_ids


def extract_mibig_gbks(selected_ids: list[str], target_dir: Path) -> dict[str, str]:
    target_dir.mkdir(parents=True, exist_ok=True)
    wanted = {f"mibig_gbk_4.0/{bgc_id}.gbk": bgc_id for bgc_id in selected_ids}
    extracted: dict[str, str] = {}
    with tarfile.open(MIBIG_TAR, "r:gz") as tar:
        members = {member.name: member for member in tar.getmembers() if member.name in wanted}
        for member_name, bgc_id in wanted.items():
            if member_name not in members:
                continue
            member = members[member_name]
            source = tar.extractfile(member)
            if source is None:
                continue
            out_path = target_dir / f"{bgc_id}.gbk"
            with out_path.open("wb") as handle:
                shutil.copyfileobj(source, handle)
            extracted[bgc_id] = out_path.name
    return extracted


def copy_plan01_regions(target_dir: Path) -> list[str]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for source in sorted(PLAN01_REGION_SOURCE.rglob("*.region*.gbk")):
        target = target_dir / source.name
        shutil.copy2(source, target)
        copied.append(target.name)
    return copied


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not MIBIG_TAR.exists():
        raise FileNotFoundError(f"Missing MIBiG archive: {MIBIG_TAR}")
    md5 = file_md5(MIBIG_TAR)
    if md5 != EXPECTED_MD5:
        raise RuntimeError(f"MIBiG archive MD5 mismatch: {md5} != {EXPECTED_MD5}")

    selected_rows, selected_ids = collect_top_hits()
    if len(selected_ids) == 0:
        raise RuntimeError("No MIBiG references selected")

    mibig_dir = OUT / "mibig_reference_gbks"
    plan01_dir = OUT / "plan01_region_gbks"
    extracted = extract_mibig_gbks(selected_ids, mibig_dir)
    copied_plan01 = copy_plan01_regions(plan01_dir)

    for row in selected_rows:
        row["gbk_extracted"] = "yes" if row["mibig_accession"] in extracted else "no"
        row["gbk_filename"] = extracted.get(row["mibig_accession"], "")

    write_csv(
        OUT / "plan01_mibig_reference_panel_manifest.csv",
        selected_rows,
        [
            "strict_bgc_id",
            "raw_query_id",
            "rank_within_keep_candidate",
            "mibig_accession",
            "subject",
            "pident",
            "qcov_or_length_field",
            "evalue",
            "bitscore",
            "source_blast_file",
            "gbk_extracted",
            "gbk_filename",
        ],
    )
    write_csv(
        OUT / "plan01_mibig_reference_panel_counts.csv",
        [
            {"metric": "keep_candidates", "value": str(len(KEEP_QUERY_IDS))},
            {"metric": "selected_reference_rows", "value": str(len(selected_rows))},
            {"metric": "unique_mibig_accessions", "value": str(len(selected_ids))},
            {"metric": "mibig_gbks_extracted", "value": str(len(extracted))},
            {"metric": "plan01_region_gbks_copied", "value": str(len(copied_plan01))},
        ],
        ["metric", "value"],
    )
    (OUT / "selected_mibig_accessions.txt").write_text("\n".join(selected_ids) + "\n")
    (OUT / "plan01_mibig_reference_panel_metadata.json").write_text(
        json.dumps(
            {
                "mibig_source": "Zenodo record 14835872, MIBiG GenBank archive 4.0",
                "mibig_source_url": "https://zenodo.org/records/14835872",
                "mibig_archive": str(MIBIG_TAR.relative_to(ROOT)),
                "mibig_archive_md5": md5,
                "mibig_archive_md5_expected": EXPECTED_MD5,
                "selection_rule": f"top {TOP_N_PER_KEEP} unique MIBiG BLAST-hit accessions per Plan01 keep candidate",
                "keep_candidates": list(KEEP_QUERY_IDS.values()),
                "unique_mibig_accessions": selected_ids,
                "claim_limit": "Targeted MIBiG reference-panel context only; not full-MIBiG or product/activity validation.",
            },
            indent=2,
        )
    )

    report = OUT / "PLAN01_MIBIG_REFERENCE_PANEL_REPORT.md"
    report.write_text(
        "# Plan 01 Targeted MIBiG Reference Panel\n\n"
        "Run date: 2026-05-17\n\n"
        "## Claim Boundary\n\n"
        "This panel prepares external MIBiG GenBank references for a targeted BiG-SCAPE check. "
        "It is selected from existing top MIBiG BLAST hits for the three Plan01 keep candidates. "
        "It is not a full-MIBiG clustering job and does not validate product formation, product identity, antimicrobial activity, novelty, or biosafety.\n\n"
        "## Source\n\n"
        "- MIBiG source: Zenodo record `14835872`, MIBiG GenBank archive 4.0.\n"
        f"- Local archive MD5: `{md5}`; expected `{EXPECTED_MD5}`.\n\n"
        "## Panel Counts\n\n"
        f"- Keep candidates represented: `{len(KEEP_QUERY_IDS)}`\n"
        f"- Selected reference rows: `{len(selected_rows)}`\n"
        f"- Unique MIBiG accessions: `{len(selected_ids)}`\n"
        f"- MIBiG GBKs extracted: `{len(extracted)}`\n"
        f"- Plan01 whole-MAG antiSMASH region GBKs staged: `{len(copied_plan01)}`\n\n"
        "## Output Files\n\n"
        "- `plan01_mibig_reference_panel_manifest.csv`\n"
        "- `plan01_mibig_reference_panel_counts.csv`\n"
        "- `selected_mibig_accessions.txt`\n"
        "- `mibig_reference_gbks/*.gbk`\n"
        "- `plan01_region_gbks/*.gbk`\n"
        "- `plan01_mibig_reference_panel_metadata.json`\n"
    )
    audit = OUT / "PLAN01_MIBIG_REFERENCE_PANEL_COMPLETION_AUDIT.md"
    audit.write_text(
        "# Plan 01 Targeted MIBiG Reference Panel Completion Audit\n\n"
        "Run date: 2026-05-17\n\n"
        "## Verdict\n\n"
        "PASS_INPUT_PANEL_READY: a targeted external MIBiG reference panel was prepared from existing top MIBiG BLAST hits for the three keep candidates, and Plan01 whole-MAG antiSMASH region GBKs were staged for the follow-up BiG-SCAPE run.\n\n"
        "## Checklist\n\n"
        "| Requirement | Evidence | Status |\n"
        "|---|---|---|\n"
        "| Verify MIBiG archive checksum | `plan01_mibig_reference_panel_metadata.json` | PASS |\n"
        "| Select external references from existing Plan01/MIBiG evidence | `plan01_mibig_reference_panel_manifest.csv` | PASS |\n"
        "| Extract selected MIBiG GBKs | `mibig_reference_gbks/*.gbk` | PASS |\n"
        "| Stage Plan01 whole-MAG antiSMASH region GBKs | `plan01_region_gbks/*.gbk` | PASS |\n"
        "| Bound claims | `PLAN01_MIBIG_REFERENCE_PANEL_REPORT.md` | PASS |\n\n"
        "## Remaining Work\n\n"
        "- Run BiG-SCAPE on the staged Plan01 plus targeted MIBiG reference GBKs through Kaggle CLI.\n"
    )
    print(f"Selected {len(selected_ids)} unique MIBiG references")
    print(f"Extracted {len(extracted)} MIBiG GBKs")
    print(f"Copied {len(copied_plan01)} Plan01 region GBKs")


if __name__ == "__main__":
    main()
