from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNEL = "aqibchoudhary35/plan01-big-scape-full-mibig-20260517"
OUT_DIR = ROOT / "outputs" / "plan01_bigscape_full_mibig_kaggle_attempt_2026-05-17"
STATUS_JSON = OUT_DIR / "plan01_bigscape_full_mibig_poll_status.json"


def run(cmd: list[str], timeout: int | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def status() -> tuple[str, str]:
    result = run(["python3", "-m", "kaggle.cli", "kernels", "status", KERNEL], timeout=120)
    text = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r'has status "([^"]+)"', text)
    return (match.group(1) if match else "UNKNOWN", text)


def next_version_dir() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    existing = []
    for path in OUT_DIR.glob("version*"):
        if path.is_dir():
            suffix = path.name.replace("version", "")
            if suffix.isdigit():
                existing.append(int(suffix))
    next_id = max(existing, default=0) + 1
    return OUT_DIR / f"version{next_id}"


def write_status(payload: dict[str, object]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True))


def pull_and_summarize() -> int:
    target = next_version_dir()
    target.mkdir(parents=True, exist_ok=True)
    pull = run(
        [
            "python3",
            "-m",
            "kaggle.cli",
            "kernels",
            "output",
            KERNEL,
            "-p",
            str(target.relative_to(ROOT)),
            "-o",
        ],
        timeout=3600,
    )
    if pull.returncode != 0:
        write_status(
            {
                "kernel": KERNEL,
                "status": "COMPLETE_BUT_PULL_FAILED",
                "target": str(target.relative_to(ROOT)),
                "pull_stdout": pull.stdout,
                "pull_stderr": pull.stderr,
            }
        )
        return pull.returncode

    summary = run(["python3", "scripts/summarize_plan01_bigscape_full_mibig.py"], timeout=1800)
    verifier = run(["python3", "scripts/verify_pre_wetlab_hardening_artifacts.py"], timeout=300)
    write_status(
        {
            "kernel": KERNEL,
            "status": "COMPLETE_PULLED_AND_SUMMARIZED",
            "target": str(target.relative_to(ROOT)),
            "pull_stdout": pull.stdout,
            "pull_stderr": pull.stderr,
            "summarizer_returncode": summary.returncode,
            "summarizer_stdout": summary.stdout,
            "summarizer_stderr": summary.stderr,
            "verifier_returncode": verifier.returncode,
            "verifier_stdout": verifier.stdout,
            "verifier_stderr": verifier.stderr,
        }
    )
    return 0 if summary.returncode == 0 and verifier.returncode == 0 else 1


def main() -> int:
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    max_wait = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    started = time.time()
    while True:
        current_status, raw = status()
        write_status(
            {
                "kernel": KERNEL,
                "status": current_status,
                "raw_status": raw,
                "elapsed_wait_seconds": round(time.time() - started, 3),
                "next_action": "pull_and_summarize_when_complete",
            }
        )
        print(raw)
        if current_status == "KernelWorkerStatus.COMPLETE":
            return pull_and_summarize()
        if current_status in {"KernelWorkerStatus.ERROR", "KernelWorkerStatus.CANCELLED", "KernelWorkerStatus.FAILED"}:
            return 2
        if interval <= 0 or (max_wait > 0 and time.time() - started >= max_wait):
            return 0
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
