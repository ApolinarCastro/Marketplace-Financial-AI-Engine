"""Domain coupling report: find marketplace-specific refs in core kernel."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_MODULES = [
    "engine/loop_control/__init__.py",
    "engine/loop_control/constants.py",
    "engine/loop_control/state_store.py",
    "engine/loop_control/kernel.py",
    "engine/loop_control/goal_manager.py",
    "engine/loop_control/todo_manager.py",
    "engine/loop_control/claim_manager.py",
    "engine/loop_control/gate_manager.py",
    "engine/loop_control/quota_manager.py",
    "engine/loop_control/evidence_manager.py",
    "engine/loop_control/handoff_manager.py",
    "engine/loop_control/recovery.py",
    "engine/loop_control/scope.py",
    "engine/loop_control/validation.py",
]

MARKETPLACE_PATTERNS = [
    r"marketplace", r"financial", r"duckdb", r"raw", r"dte", r"xml", r"sap",
    r"ledger", r"classification", r"reconciliation", r"311c78e2",
    r"01[_-]?raw", r"meli[_-]?financial", r"rippley", r"paris", r"falabella", r"shopify",
    r"cierre[_-]?financiero", r"marketplace[_-]?ledger", r"financial[_-]?group",
]

def scan_module(rel_path: str) -> dict:
    p = REPO_ROOT / rel_path
    if not p.is_file():
        return {"module": rel_path, "status": "MISSING", "findings": []}
    text = p.read_text(encoding="utf-8", errors="ignore")
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for pat in MARKETPLACE_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                findings.append({"line": i, "pattern": pat, "code": stripped[:120]})
    return {"module": rel_path, "status": "SCANNED", "findings": findings}

def main() -> int:
    out = REPO_ROOT / "evidence" / "universal_loop_v1"
    out.mkdir(parents=True, exist_ok=True)

    results = [scan_module(m) for m in CORE_MODULES]
    total_findings = sum(len(r["findings"]) for r in results)
    by_module = {r["module"]: len(r["findings"]) for r in results}
    by_pattern = {}
    for r in results:
        for f in r["findings"]:
            by_pattern[f["pattern"]] = by_pattern.get(f["pattern"], 0) + 1

    report = {
        "evidence_id": "UNIVERSAL_LOOP_V1_DOMAIN_COUPLING",
        "core_modules_scanned": len(CORE_MODULES),
        "total_findings": total_findings,
        "by_module": by_module,
        "by_pattern": by_pattern,
        "detail": results,
        "gate_passed": total_findings == 0,
        "generated_at": "2026-08-07T00:00:00Z",
    }

    (out / "domain_coupling_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"gate": "PASS" if report["gate_passed"] else "FAIL",
                      "total_findings": total_findings,
                      "by_module": by_module}, indent=2))
    return 0 if report["gate_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())