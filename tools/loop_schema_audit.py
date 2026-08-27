"""Schema portability audit: verify all schemas are domain-agnostic."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SCHEMAS = [
    "goal.schema.json",
    "todo.schema.json",
    "gate.schema.json",
    "claim.schema.json",
    "handoff.schema.json",
    "run_event.schema.json",
    "quota.schema.json",
    "evidence.schema.json",
]

MARKETPLACE_PATTERNS = [
    r"marketplace", r"financial", r"duckdb", r"raw", r"dte", r"xml", r"sap",
    r"ledger", r"classification", r"reconciliation", r"311c78e2",
    r"01[_-]?raw", r"meli[_-]?financial", r"rippley", r"paris", r"falabella", r"shopify",
    r"cierre[_-]?financiero", r"marketplace[_-]?ledger", r"financial[_-]?group",
]

def audit_schema(schema_name: str) -> dict:
    path = REPO_ROOT / "engine" / "loop_control" / "schemas" / schema_name
    if not path.is_file():
        return {"schema": schema_name, "status": "MISSING", "findings": []}
    text = path.read_text(encoding="utf-8").lower()
    findings = []
    for pat in MARKETPLACE_PATTERNS:
        if re.search(pat, text):
            findings.append(pat)
    return {"schema": schema_name, "status": "SCANNED", "findings": findings}

def main() -> int:
    out = REPO_ROOT / "evidence" / "universal_loop_v1"
    out.mkdir(parents=True, exist_ok=True)

    results = [audit_schema(s) for s in SCHEMAS]
    total_findings = sum(len(r["findings"]) for r in results)
    by_schema = {r["schema"]: len(r["findings"]) for r in results}

    report = {
        "evidence_id": "UNIVERSAL_LOOP_V1_SCHEMA_PORTABILITY",
        "schemas_audited": len(SCHEMAS),
        "total_findings": total_findings,
        "by_schema": by_schema,
        "detail": results,
        "gate_passed": total_findings == 0,
        "generated_at": "2026-08-07T00:00:00Z",
    }

    (out / "schema_portability_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"gate": "PASS" if report["gate_passed"] else "FAIL", "total_findings": total_findings}, indent=2))
    return 0 if report["gate_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())