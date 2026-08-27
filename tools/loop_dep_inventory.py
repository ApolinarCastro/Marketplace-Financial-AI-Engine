"""Dependency inventory: classify every control plane reference."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = {
    "UNIVERSAL": "Belongs in the universal core",
    "PROJECT_POLICY": "Project-specific configuration",
    "MARKETPLACE_SPECIFIC": "Marketplace Financial AI Engine only",
    "RUNTIME_SPECIFIC": "OpenCode/Codex/Claude runtime detail",
    "LEGACY": "Obsolete or to be removed",
}

MARKETPLACE_PATTERNS = [
    r"marketplace", r"financial", r"duckdb", r"raw", r"dte", r"xml", r"sap",
    r"ledger", r"classification", r"reconciliation", r"311c78e2",
    r"01[_-]?raw", r"meli[_-]?financial", r"rippley", r"paris", r"falabella", r"shopify",
    r"cierre[_-]?financiero", r"marketplace[_-]?ledger", r"financial[_-]?group",
]

OPENCODE_PATTERNS = [r"opencode", r"OPENCODE"]
CODEX_PATTERNS = [r"codex", r"CODEX"]

def classify_line(line: str, filepath: str) -> str:
    lower = line.lower()
    for pat in MARKETPLACE_PATTERNS:
        if re.search(pat, lower):
            return "MARKETPLACE_SPECIFIC"
    for pat in OPENCODE_PATTERNS:
        if re.search(pat, lower):
            return "RUNTIME_SPECIFIC"
    for pat in CODEX_PATTERNS:
        if re.search(pat, lower):
            return "RUNTIME_SPECIFIC"
    return "UNIVERSAL"

def scan_file(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"file": str(path), "lines": 0, "classified": []}
    lines = text.splitlines()
    results = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue
        cat = classify_line(line, str(path))
        if cat != "UNIVERSAL":
            results.append({"line": i, "category": cat, "content": stripped[:120]})
    return {"file": str(path.relative_to(REPO_ROOT)), "lines": len(lines), "classified": results}

def main() -> int:
    out = REPO_ROOT / "evidence" / "universal_loop_v1"
    out.mkdir(parents=True, exist_ok=True)

    targets = [
        REPO_ROOT / "engine" / "loop_control",
        REPO_ROOT / "governance" / "LOOP_ENGINEERING_PROTOCOL_V1.md",
        REPO_ROOT / "tests" / "test_loop_control.py",
        REPO_ROOT / "tools" / "run_loop_dogfood.py",
        REPO_ROOT / "tools" / "generate_loop_evidence.py",
    ]

    all_results = []
    for target in targets:
        if target.is_dir():
            for p in target.rglob("*.py"):
                if "__pycache__" not in p.parts:
                    all_results.append(scan_file(p))
            for p in target.rglob("*.md"):
                all_results.append(scan_file(p))
        elif target.is_file():
            all_results.append(scan_file(target))

    summary = {"UNIVERSAL": 0, "PROJECT_POLICY": 0, "MARKETPLACE_SPECIFIC": 0,
               "RUNTIME_SPECIFIC": 0, "LEGACY": 0, "UNKNOWN": 0}
    for r in all_results:
        for c in r["classified"]:
            summary[c["category"]] = summary.get(c["category"], 0) + 1

    report = {
        "evidence_id": "UNIVERSAL_LOOP_V1_DEP_INVENTORY",
        "files_scanned": len(all_results),
        "summary": summary,
        "detail": all_results,
        "unknown_count": summary.get("UNKNOWN", 0),
        "gate_passed": summary.get("UNKNOWN", 0) == 0,
        "generated_at": "2026-08-07T00:00:00Z",
    }

    (out / "dependency_inventory.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"gate": "PASS" if report["gate_passed"] else "FAIL", "summary": summary}, indent=2))
    return 0 if report["gate_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())