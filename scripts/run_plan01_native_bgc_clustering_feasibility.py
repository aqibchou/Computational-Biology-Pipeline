#!/usr/bin/env python3
"""Audit feasibility of native BiG-SCAPE/CORASON-style Plan 01 clustering."""

from __future__ import annotations

import csv
import datetime as dt
import shutil
import subprocess
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / f"outputs/plan01_native_bgc_clustering_feasibility_{RUN_DATE}"


def run(cmd: list[str]) -> tuple[str, str, int]:
    try:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=30)
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except Exception as exc:  # noqa: BLE001 - output is an audit artifact
        return "", repr(exc), 999


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def find_inputs() -> list[Path]:
    patterns = ["*.gbk", "*.gbff", "*.gb", "*.json"]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(ROOT.glob(f"outputs/plan01*/**/{pattern}"))
    return sorted(files)


def classify_input(path: Path) -> str:
    name = path.name.lower()
    text = str(path).lower()
    if name.endswith((".gbk", ".gbff", ".gb")):
        return "GENBANK_NATIVE_CLUSTER_INPUT_CANDIDATE"
    if "mibig_json" in text:
        return "MIBIG_METADATA_JSON_NOT_CLUSTER_INPUT"
    if "api_cache" in text:
        return "API_CACHE_JSON_NOT_CLUSTER_INPUT"
    return "JSON_NOT_NATIVE_CLUSTER_INPUT"


def make_report(tool_rows: list[dict[str, object]], input_rows: list[dict[str, object]], kaggle_rows: list[dict[str, object]]) -> str:
    genbank_count = sum(1 for row in input_rows if row["input_class"] == "GENBANK_NATIVE_CLUSTER_INPUT_CANDIDATE")
    lines = [
        "# Plan 01 Native BGC Clustering Feasibility Audit",
        "",
        f"Run date: {RUN_DATE}",
        "",
        "## Scope",
        "",
        "This audit checks whether a native BiG-SCAPE/CORASON-style BGC family clustering run can be launched from the current workspace. It does not substitute for native clustering.",
        "",
        "## Verdict",
        "",
    ]
    if genbank_count:
        lines.append(f"Native clustering inputs appear available: {genbank_count} GenBank-like files were found. A Kaggle or local clustering run can be prepared from these files.")
    else:
        lines.append("Native clustering is currently blocked by missing BGC GenBank inputs. The workspace has markdown packets, MIBiG/API caches, and derived tables, but no antiSMASH/GECCO `.gbk`/`.gbff` region files for BiG-SCAPE/CORASON.")
    lines.extend(
        [
            "",
            "## Tool And Compute Gate",
            "",
            "| Item | Status | Evidence |",
            "|---|---|---|",
        ]
    )
    for row in tool_rows:
        lines.append(f"| {row['item']} | {row['status']} | {row['evidence']} |")
    for row in kaggle_rows:
        lines.append(f"| {row['item']} | {row['status']} | {row['evidence']} |")
    lines.extend(
        [
            "",
            "## Input Gate",
            "",
            f"- GenBank-like BGC input files found: {genbank_count}",
            f"- Non-native JSON/cache artifacts found under Plan01 outputs: {sum(1 for row in input_rows if row['input_class'] != 'GENBANK_NATIVE_CLUSTER_INPUT_CANDIDATE')}",
            "",
            "## Next Action To Complete Native Clustering",
            "",
            "Provide or regenerate antiSMASH/GECCO GenBank region files for the Plan 01 finalists, then run BiG-SCAPE/BiG-SLiCE-style clustering locally or through Kaggle CLI. If the run is heavy, route it through Kaggle as requested.",
            "",
            "## Claim Boundary",
            "",
            "Until native clustering is run on proper BGC region files, Plan 01 cluster-family novelty should remain labeled as a proxy/local-GCF result, not a true BiG-SCAPE/CORASON result.",
            "",
        ]
    )
    return "\n".join(lines)


def make_audit(input_rows: list[dict[str, object]]) -> str:
    genbank_count = sum(1 for row in input_rows if row["input_class"] == "GENBANK_NATIVE_CLUSTER_INPUT_CANDIDATE")
    status = "PASS_FEASIBILITY_AUDIT_INPUTS_PRESENT" if genbank_count else "BLOCKED_MISSING_GENBANK_BGC_INPUTS"
    return "\n".join(
        [
            "# Plan 01 Native BGC Clustering Feasibility Completion Audit",
            "",
            f"Run date: {RUN_DATE}",
            "",
            "## Verdict",
            "",
            f"{status}: native BGC family clustering was not run in this pass. The audit identifies the concrete input/tool gate.",
            "",
            "## Checklist",
            "",
            "| Requirement | Evidence | Status |",
            "|---|---|---|",
            "| Check local BiG-SCAPE/CORASON availability | `plan01_native_bgc_clustering_tool_gate.csv` | PASS |",
            "| Check Kaggle CLI path for heavy run | `plan01_native_bgc_clustering_kaggle_gate.csv` | PASS |",
            "| Check for native BGC GenBank inputs | `plan01_native_bgc_clustering_input_manifest.csv` | PASS |",
            "| Avoid mislabeled proxy as native clustering | report claim boundary | PASS |",
            "",
            "## Remaining Work",
            "",
            "- Regenerate or supply antiSMASH/GECCO GenBank region files for Plan 01 finalists.",
            "- Launch native clustering through Kaggle CLI if compute/tool install is heavy.",
            "",
        ]
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    tool_rows = []
    for tool in ["bigscape", "bigscape.py", "corason", "cblaster", "antismash"]:
        path = shutil.which(tool)
        tool_rows.append(
            {
                "item": tool,
                "status": "AVAILABLE" if path else "NOT_IN_PATH",
                "evidence": path or "not found by shutil.which",
            }
        )
    kaggle_version_out, kaggle_version_err, kaggle_version_code = run(["python3", "-m", "kaggle.cli", "--version"])
    kaggle_list_out, kaggle_list_err, kaggle_list_code = run(["python3", "-m", "kaggle.cli", "kernels", "list", "--mine", "--page-size", "1"])
    kaggle_rows = [
        {
            "item": "kaggle_cli_version",
            "status": "AVAILABLE" if kaggle_version_code == 0 else "FAILED",
            "evidence": kaggle_version_out or kaggle_version_err,
        },
        {
            "item": "kaggle_cli_authenticated_kernel_list",
            "status": "AVAILABLE" if kaggle_list_code == 0 else "FAILED",
            "evidence": (kaggle_list_out or kaggle_list_err).replace("\n", " | ")[:500],
        },
    ]
    input_rows = [
        {
            "path": str(path.relative_to(ROOT)),
            "input_class": classify_input(path),
            "bytes": path.stat().st_size,
        }
        for path in find_inputs()
    ]
    write_csv(OUTDIR / "plan01_native_bgc_clustering_tool_gate.csv", tool_rows, ["item", "status", "evidence"])
    write_csv(OUTDIR / "plan01_native_bgc_clustering_kaggle_gate.csv", kaggle_rows, ["item", "status", "evidence"])
    write_csv(OUTDIR / "plan01_native_bgc_clustering_input_manifest.csv", input_rows, ["path", "input_class", "bytes"])
    (OUTDIR / "PLAN01_NATIVE_BGC_CLUSTERING_FEASIBILITY_REPORT.md").write_text(
        make_report(tool_rows, input_rows, kaggle_rows)
    )
    (OUTDIR / "PLAN01_NATIVE_BGC_CLUSTERING_FEASIBILITY_COMPLETION_AUDIT.md").write_text(make_audit(input_rows))
    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"GenBank-like inputs: {sum(1 for row in input_rows if row['input_class'] == 'GENBANK_NATIVE_CLUSTER_INPUT_CANDIDATE')}")
    print(f"Input artifacts inspected: {len(input_rows)}")


if __name__ == "__main__":
    main()
