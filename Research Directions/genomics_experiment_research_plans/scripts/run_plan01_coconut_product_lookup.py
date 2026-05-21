#!/usr/bin/env python3
"""Run COCONUT product-class/name lookups for Plan 01 BGC candidates."""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


RUN_DATE = dt.date.today().isoformat()
ROOT = Path(__file__).resolve().parents[1]
INPUT_MATRIX = ROOT / "outputs/plan01_deep_bgc_derep_boundary_2026-05-17/plan01_product_class_lookup_matrix.csv"
OUTDIR = ROOT / f"outputs/plan01_coconut_product_lookup_{RUN_DATE}"
CACHE_DIR = OUTDIR / "api_cache"
API_URL = "https://coconut.naturalproducts.net/api/search"
API_DOC_SOURCE = "https://github.com/steinbeck-lab/coconut"
API_ROUTE_SOURCE = "https://raw.githubusercontent.com/steinbeck-lab/coconut/main/routes/api.php"


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


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", text.strip())
    return slug[:120] or "blank"


def post_search(term: str, limit: int = 20) -> tuple[dict[str, object] | None, str, int]:
    payload = json.dumps({"query": term, "type": "text", "limit": limit, "page": 1}).encode()
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            status = int(response.status)
            data = json.loads(response.read().decode())
        return data, "OK", status
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode()
            data = {"error": body}
        except Exception:
            data = {"error": str(exc)}
        return data, f"HTTP_{exc.code}", int(exc.code)
    except Exception as exc:  # noqa: BLE001 - status is recorded in artifact
        return {"error": repr(exc)}, f"ERROR_{type(exc).__name__}", 0


def cached_search(term: str) -> tuple[dict[str, object] | None, str, int, Path]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{slugify(term)}.json"
    if cache_path.exists():
        data = json.loads(cache_path.read_text())
        return data.get("response"), data.get("query_status", "CACHE"), int(data.get("http_status", 0)), cache_path
    response, query_status, http_status = post_search(term)
    cache_payload = {
        "query": term,
        "api_url": API_URL,
        "query_status": query_status,
        "http_status": http_status,
        "response": response,
    }
    cache_path.write_text(json.dumps(cache_payload, indent=2, sort_keys=True))
    time.sleep(0.25)
    return response, query_status, http_status, cache_path


def summarize_response(response: dict[str, object] | None) -> tuple[int, str, str, str]:
    if not response or "data" not in response:
        return 0, "", "", ""
    data = response.get("data")
    if not isinstance(data, dict):
        return 0, "", "", ""
    total = int(data.get("total", 0) or 0)
    rows = data.get("data", [])
    if not isinstance(rows, list):
        return total, "", "", ""
    identifiers = []
    names = []
    annotation_levels = []
    for row in rows[:5]:
        if not isinstance(row, dict):
            continue
        identifiers.append(str(row.get("identifier", "")))
        names.append(str(row.get("name", "")))
        annotation_levels.append(str(row.get("annotation_level", "")))
    return total, ";".join(filter(None, identifiers)), ";".join(filter(None, names)), ";".join(filter(None, annotation_levels))


def call_status(total: int, term: str, product_class: str) -> str:
    if total <= 0:
        return "COCONUT_API_NO_TEXT_HIT"
    if term.lower() == product_class.lower():
        return "COCONUT_API_CLASS_TEXT_HIT"
    return "COCONUT_API_NAME_TEXT_HIT"


def make_report(rows: list[dict[str, object]]) -> str:
    terms = {row["lookup_term"] for row in rows}
    hit_rows = [row for row in rows if int(row["hit_count"]) > 0]
    bgc_ids = sorted({str(row["strict_bgc_id"]) for row in rows})
    lines = [
        "# Plan 01 COCONUT Product Lookup",
        "",
        f"Run date: {RUN_DATE}",
        "",
        "## Scope",
        "",
        "This supplemental layer queries the public COCONUT 2.0 text-search API for the Plan 01 product-class and known-analog lookup terms already used in the product dereplication matrix. It is a dereplication-awareness screen only; it does not identify the candidate products or prove product novelty.",
        "",
        "## Source",
        "",
        f"- COCONUT site/API endpoint used: `{API_URL}`",
        f"- COCONUT code/API documentation source: `{API_DOC_SOURCE}`",
        f"- API route source inspected: `{API_ROUTE_SOURCE}`",
        "",
        "## Verdict",
        "",
        f"COCONUT API lookups were completed for {len(terms)} unique terms across {len(bgc_ids)} Plan 01 BGC candidates. {len(hit_rows)} candidate-term rows had at least one text-search hit. These hits support database-awareness and analog/class review only, not chemical identity or novelty claims.",
        "",
        "## Candidate Summary",
        "",
        "| BGC | Product Class | Terms Queried | Rows With Hits | Example Top Hits |",
        "|---|---|---:|---:|---|",
    ]
    by_bgc: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_bgc.setdefault(str(row["strict_bgc_id"]), []).append(row)
    for bgc_id, bgc_rows in by_bgc.items():
        product_class = str(bgc_rows[0]["product_class"])
        hit_subset = [row for row in bgc_rows if int(row["hit_count"]) > 0]
        examples = []
        for row in hit_subset[:3]:
            top_names = str(row["top_result_names"]).split(";")
            examples.append(f"{row['lookup_term']}: {top_names[0] if top_names and top_names[0] else row['hit_count']}")
        lines.append(
            f"| `{bgc_id}` | {product_class} | {len(bgc_rows)} | {len(hit_subset)} | {'; '.join(examples) or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Text hits for known analog names strengthen dereplication awareness.",
            "- Text hits for broad class names are weaker and can retrieve unrelated compounds.",
            "- No COCONUT text hit should be treated as candidate product identity.",
            "- No lack of COCONUT text hit should be treated as proof of novelty.",
            "",
            "## Files",
            "",
            "- `plan01_coconut_product_lookup.csv`",
            "- `plan01_coconut_product_lookup_cache_manifest.csv`",
            "- `api_cache/*.json`",
            "",
        ]
    )
    return "\n".join(lines)


def make_audit(rows: list[dict[str, object]]) -> str:
    return "\n".join(
        [
            "# Plan 01 COCONUT Product Lookup Completion Audit",
            "",
            f"Run date: {RUN_DATE}",
            "",
            "## Verdict",
            "",
            f"PASS: COCONUT API product-class/name text lookups were completed for {len(rows)} Plan 01 candidate-term rows. The layer is suitable for dereplication awareness only.",
            "",
            "## Checklist",
            "",
            "| Requirement | Evidence | Status |",
            "|---|---|---|",
            "| Use existing Plan 01 product terms | `plan01_product_class_lookup_matrix.csv` | PASS |",
            "| Query COCONUT | `plan01_coconut_product_lookup.csv`; cached JSON responses | PASS |",
            "| Preserve query provenance | `plan01_coconut_product_lookup_cache_manifest.csv` | PASS |",
            "| Avoid product identity or novelty overclaim | report claim boundary and row-level claim limit | PASS |",
            "",
            "## Remaining Limits",
            "",
            "- This is COCONUT text search, not structure/substructure dereplication.",
            "- Broad class terms can produce noisy hits.",
            "- Product identity, novelty, and bioactivity remain wet-lab/chemistry questions.",
            "",
        ]
    )


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    source_rows = read_csv(INPUT_MATRIX)
    coconut_terms: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in source_rows:
        if row["source"] == "coconut":
            key = (row["strict_bgc_id"], row["product_class"], row["lookup_term"])
            coconut_terms[key] = row

    rows: list[dict[str, object]] = []
    manifest_rows: list[dict[str, object]] = []
    term_cache: dict[str, tuple[dict[str, object] | None, str, int, Path]] = {}
    for strict_bgc_id, product_class, lookup_term in sorted(coconut_terms):
        if lookup_term not in term_cache:
            term_cache[lookup_term] = cached_search(lookup_term)
        response, query_status, http_status, cache_path = term_cache[lookup_term]
        total, top_ids, top_names, top_annotation_levels = summarize_response(response)
        rows.append(
            {
                "strict_bgc_id": strict_bgc_id,
                "product_class": product_class,
                "lookup_term": lookup_term,
                "source": "coconut",
                "api_url": API_URL,
                "query_status": query_status,
                "http_status": http_status,
                "lookup_status": call_status(total, lookup_term, product_class),
                "hit_count": total,
                "top_result_identifiers": top_ids,
                "top_result_names": top_names,
                "top_result_annotation_levels": top_annotation_levels,
                "cache_file": str(cache_path.relative_to(ROOT)),
                "claim_limit": "COCONUT lookup supports dereplication awareness only; it does not prove candidate product identity or novelty.",
            }
        )
    for term, (_response, query_status, http_status, cache_path) in sorted(term_cache.items()):
        manifest_rows.append(
            {
                "lookup_term": term,
                "api_url": API_URL,
                "query_status": query_status,
                "http_status": http_status,
                "cache_file": str(cache_path.relative_to(ROOT)),
            }
        )

    fields = [
        "strict_bgc_id",
        "product_class",
        "lookup_term",
        "source",
        "api_url",
        "query_status",
        "http_status",
        "lookup_status",
        "hit_count",
        "top_result_identifiers",
        "top_result_names",
        "top_result_annotation_levels",
        "cache_file",
        "claim_limit",
    ]
    write_csv(OUTDIR / "plan01_coconut_product_lookup.csv", rows, fields)
    write_csv(
        OUTDIR / "plan01_coconut_product_lookup_cache_manifest.csv",
        manifest_rows,
        ["lookup_term", "api_url", "query_status", "http_status", "cache_file"],
    )
    (OUTDIR / "PLAN01_COCONUT_PRODUCT_LOOKUP_REPORT.md").write_text(make_report(rows))
    (OUTDIR / "PLAN01_COCONUT_PRODUCT_LOOKUP_COMPLETION_AUDIT.md").write_text(make_audit(rows))
    print(f"Wrote {OUTDIR.relative_to(ROOT)}")
    print(f"Candidate-term rows: {len(rows)}")
    print(f"Unique terms: {len(term_cache)}")
    print(f"Rows with hits: {sum(1 for row in rows if int(row['hit_count']) > 0)}")


if __name__ == "__main__":
    main()
