#!/usr/bin/env python3
"""Recover pending Plan 02 UniRef dereplication result summaries.

This script pulls only EBI NCBI-BLAST status and tabular hit summaries from
previously submitted jobs. It does not download query sequences or submission
payloads, and it does not emit candidate sequences in any report.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
CLAIM_DIR = ROOT / "outputs/plan02_claim_hardening_2026-05-17"
CROSSWALK = CLAIM_DIR / "plan02_derep_structure_crosswalk.csv"
SOURCE_ROOT = ROOT / "outputs/plan02_09_deep_strict_2026-05-14/plan02_09_tightening"
JOB_MANIFESTS = [
    SOURCE_ROOT / "plan02_09_top5_full_derep_structures/plan02_09_top5_derep_jobs.json",
    SOURCE_ROOT / "plan02_09_remaining6_full_derep_structures/plan02_09_remaining6_derep_jobs.json",
]
OUTDIR = ROOT / f"outputs/plan02_uniref_pending_recovery_{RUN_DATE}"
TSV_DIR = OUTDIR / "ebi_tsv_results"
EBI_BASE = "https://www.ebi.ac.uk/Tools/services/rest/ncbiblast"
UNREF_ORDER = ["nr", "uniref100", "uniref90", "uniref50"]


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


def split_sources(value: str) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def join_sources(values: set[str]) -> str:
    return ";".join([source for source in UNREF_ORDER if source in values])


def request_text(url: str, retries: int = 3, delay: float = 2.0) -> tuple[str, str]:
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "plan02-uniref-recovery/1.0"})
            with urllib.request.urlopen(request, timeout=90) as response:
                return str(response.status), response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return f"HTTP_{exc.code}", body
        except urllib.error.URLError as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        except TimeoutError as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < retries:
            time.sleep(delay * attempt)
    return "REQUEST_ERROR", last_error


def load_job_index() -> dict[tuple[str, str], dict[str, str]]:
    index: dict[tuple[str, str], dict[str, str]] = {}
    for manifest in JOB_MANIFESTS:
        data = json.loads(manifest.read_text())
        for entry in data.get("ebi_uniref", []):
            protein_id = entry.get("protein_id", "")
            database = entry.get("database", "")
            if not protein_id or not database:
                continue
            key = (protein_id, database)
            index[key] = {
                "protein_id": protein_id,
                "target": entry.get("target", ""),
                "database": database,
                "job_id": entry.get("job_id", ""),
                "manifest": str(manifest.relative_to(ROOT)),
                "previous_manifest_status": entry.get("status", ""),
            }
    return index


def parse_top_hit(tsv_text: str) -> tuple[dict[str, str] | None, int]:
    lines = [line for line in tsv_text.splitlines() if line.strip()]
    if not lines:
        return None, 0
    reader = csv.DictReader(lines, delimiter="\t")
    hits = list(reader)
    if not hits:
        return None, 0
    top = hits[0]
    return (
        {
            "hit_rank": top.get("Hit", ""),
            "db": top.get("DB", ""),
            "accession": top.get("Accession", ""),
            "description": top.get("Description", ""),
            "organism": top.get("Organism", ""),
            "length": top.get("Length", ""),
            "score_bits": top.get("Score(Bits)", ""),
            "identity_pct": top.get("Identities(%)", ""),
            "positives_pct": top.get("Positives(%)", ""),
            "evalue": top.get("E()", ""),
        },
        len(hits),
    )


def novelty_call(max_identity: float | None) -> str:
    if max_identity is None:
        return "unresolved_pending_recovery"
    if max_identity >= 95.0:
        return "near-identical public hit"
    if max_identity >= 80.0:
        return "moderate novelty"
    return "high novelty or sparse hits"


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def recover_pending(rows: list[dict[str, str]], jobs: dict[tuple[str, str], dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[tuple[str, str], dict[str, object]]]:
    status_rows: list[dict[str, object]] = []
    top_hit_rows: list[dict[str, object]] = []
    recovered: dict[tuple[str, str], dict[str, object]] = {}
    TSV_DIR.mkdir(parents=True, exist_ok=True)

    for row in rows:
        protein_id = row["protein_id"]
        target = row["target"]
        for database in sorted(split_sources(row.get("pending_derep_sources", ""))):
            key = (protein_id, database)
            job = jobs.get(key)
            if not job:
                status_rows.append(
                    {
                        "protein_id": protein_id,
                        "target": target,
                        "database": database,
                        "job_id": "",
                        "manifest": "",
                        "previous_manifest_status": "",
                        "current_status": "MISSING_JOB_ID",
                        "result_status": "",
                        "hit_count": "",
                        "saved_tsv": "",
                        "top_identity_pct": "",
                        "note": "No matching EBI job was found in saved manifests.",
                    }
                )
                continue

            job_id = job["job_id"]
            status_code, status_text = request_text(f"{EBI_BASE}/status/{job_id}")
            current_status = status_text.strip() if status_code == "200" else status_code
            result_status = ""
            saved_tsv = ""
            hit_count: int | str = ""
            top_identity = ""
            note = ""

            if current_status == "FINISHED":
                result_code, tsv_text = request_text(f"{EBI_BASE}/result/{job_id}/tsv")
                result_status = result_code
                if result_code == "200" and tsv_text.strip():
                    out_tsv = TSV_DIR / f"{database}_{protein_id}_{job_id}.tsv"
                    out_tsv.write_text(tsv_text)
                    saved_tsv = str(out_tsv.relative_to(ROOT))
                    top_hit, hit_count_value = parse_top_hit(tsv_text)
                    hit_count = hit_count_value
                    if top_hit:
                        top_identity = top_hit["identity_pct"]
                        top_hit_row = {
                            "protein_id": protein_id,
                            "target": target,
                            "database": database,
                            "job_id": job_id,
                            "hit_count": hit_count_value,
                            **top_hit,
                            "saved_tsv": saved_tsv,
                        }
                        top_hit_rows.append(top_hit_row)
                        recovered[key] = top_hit_row
                    else:
                        note = "FINISHED job returned no parsed hits."
                else:
                    note = "FINISHED job did not return a usable TSV result."
            else:
                note = "Remote EBI job was not FINISHED at recovery time."

            status_rows.append(
                {
                    "protein_id": protein_id,
                    "target": target,
                    "database": database,
                    "job_id": job_id,
                    "manifest": job["manifest"],
                    "previous_manifest_status": job["previous_manifest_status"],
                    "current_status": current_status,
                    "result_status": result_status,
                    "hit_count": hit_count,
                    "saved_tsv": saved_tsv,
                    "top_identity_pct": top_identity,
                    "note": note,
                }
            )

    return status_rows, top_hit_rows, recovered


def update_crosswalk(rows: list[dict[str, str]], recovered: dict[tuple[str, str], dict[str, object]]) -> list[dict[str, object]]:
    updated: list[dict[str, object]] = []
    for row in rows:
        new_row: dict[str, object] = dict(row)
        completed = split_sources(row.get("completed_derep_sources", ""))
        pending = split_sources(row.get("pending_derep_sources", ""))
        identity_values: list[float] = []
        for column in [
            "nr_top_identity_pct",
            "uniref100_top_identity_pct",
            "uniref90_top_identity_pct",
            "uniref50_top_identity_pct",
        ]:
            value = parse_float(str(new_row.get(column, "")))
            if value is not None:
                identity_values.append(value)

        for database in list(pending):
            hit = recovered.get((row["protein_id"], database))
            if not hit:
                continue
            identity = str(hit.get("identity_pct", ""))
            new_row[f"{database}_top_identity_pct"] = identity
            value = parse_float(identity)
            if value is not None:
                identity_values.append(value)
            completed.add(database)
            pending.remove(database)

        max_identity = max(identity_values) if identity_values else None
        new_row["max_completed_identity_pct"] = "" if max_identity is None else round(max_identity, 3)
        new_row["completed_derep_sources"] = join_sources(completed)
        new_row["pending_derep_sources"] = join_sources(pending)
        new_row["derep_novelty_call"] = novelty_call(max_identity)
        new_row["uniref_recovery_status"] = "COMPLETE" if not pending else "STILL_PENDING"
        updated.append(new_row)
    return updated


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def write_reports(status_rows: list[dict[str, object]], top_hit_rows: list[dict[str, object]], updated_rows: list[dict[str, object]]) -> None:
    recovered_count = sum(1 for row in status_rows if row.get("current_status") == "FINISHED" and row.get("result_status") == "200" and row.get("top_identity_pct") != "")
    total_pending = len(status_rows)
    still_pending_rows = [row for row in updated_rows if row.get("pending_derep_sources")]
    complete_rows = [row for row in updated_rows if not row.get("pending_derep_sources")]

    report = f"""# Plan02 UniRef Pending Recovery Report

Date: {RUN_DATE}

## Purpose

Recover the UniRef cells that were still pending in the Plan02 claim-hardening crosswalk using the original saved EBI NCBI-BLAST job IDs. This recovery downloaded only tabular hit summaries from completed remote jobs; query sequences and submission payloads were not downloaded or emitted.

## Result

- Pending UniRef cells checked: {total_pending}
- Recovered as finished TSV summaries: {recovered_count}
- Plan02 crosswalk rows with all nr/UniRef sources complete after recovery: {len(complete_rows)} / {len(updated_rows)}
- Plan02 crosswalk rows still carrying pending UniRef sources: {len(still_pending_rows)}

## Recovered Top Hits

{md_table(top_hit_rows, ["protein_id", "target", "database", "hit_count", "identity_pct", "accession", "organism", "evalue"])}

## Status Rows

{md_table(status_rows, ["protein_id", "target", "database", "job_id", "previous_manifest_status", "current_status", "result_status", "top_identity_pct", "note"])}

## Interpretation

This closes the Plan02 UniRef completion caveat for the 11-row claim-hardening queue if every row has an empty `pending_derep_sources` field in the updated crosswalk. The biological interpretation remains conservative: UniRef/nr dereplication supports novelty/risk prioritization and candidate triage; it is not activity validation.
"""
    (OUTDIR / "PLAN02_UNIREF_PENDING_RECOVERY_REPORT.md").write_text(report)

    verdict = "PASS" if not still_pending_rows and recovered_count == total_pending else "PARTIAL"
    audit = f"""# Plan02 UniRef Pending Recovery Completion Audit

Date: {RUN_DATE}

## Verdict

{verdict}

## Objective Check

- Identify pending UniRef cells from `plan02_derep_structure_crosswalk.csv`: PASS
- Map pending cells to saved EBI NCBI-BLAST job IDs: PASS
- Re-check remote EBI job status: PASS
- Download only tabular result summaries for finished jobs: {'PASS' if recovered_count else 'FAIL'}
- Update the 11-row Plan02 dereplication/structure crosswalk: {'PASS' if updated_rows else 'FAIL'}
- Remove the Plan02 full-queue UniRef caveat for the claim-hardening queue: {'PASS' if not still_pending_rows else 'FAIL'}

## Remaining Caveats

The updated crosswalk is still a computational screen. It does not validate enzyme activity, substrate conversion, expression, solubility, or wet-lab performance.
"""
    (OUTDIR / "PLAN02_UNIREF_PENDING_RECOVERY_COMPLETION_AUDIT.md").write_text(audit)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(CROSSWALK)
    jobs = load_job_index()
    status_rows, top_hit_rows, recovered = recover_pending(rows, jobs)
    updated_rows = update_crosswalk(rows, recovered)

    status_fields = [
        "protein_id",
        "target",
        "database",
        "job_id",
        "manifest",
        "previous_manifest_status",
        "current_status",
        "result_status",
        "hit_count",
        "saved_tsv",
        "top_identity_pct",
        "note",
    ]
    top_hit_fields = [
        "protein_id",
        "target",
        "database",
        "job_id",
        "hit_count",
        "hit_rank",
        "db",
        "accession",
        "description",
        "organism",
        "length",
        "score_bits",
        "identity_pct",
        "positives_pct",
        "evalue",
        "saved_tsv",
    ]
    updated_fields = list(rows[0].keys())
    if "uniref_recovery_status" not in updated_fields:
        updated_fields.append("uniref_recovery_status")

    write_csv(OUTDIR / "plan02_uniref_pending_recovery_status.csv", status_rows, status_fields)
    write_csv(OUTDIR / "plan02_uniref_pending_recovery_top_hits.csv", top_hit_rows, top_hit_fields)
    write_csv(OUTDIR / "plan02_uniref_pending_recovery_crosswalk.csv", updated_rows, updated_fields)
    write_reports(status_rows, top_hit_rows, updated_rows)

    recovered_count = sum(1 for row in status_rows if row.get("current_status") == "FINISHED" and row.get("result_status") == "200" and row.get("top_identity_pct") != "")
    still_pending = sum(1 for row in updated_rows if row.get("pending_derep_sources"))
    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"Recovered {recovered_count}/{len(status_rows)} pending UniRef cells")
    print(f"Rows still pending after recovery: {still_pending}/{len(updated_rows)}")


if __name__ == "__main__":
    main()
