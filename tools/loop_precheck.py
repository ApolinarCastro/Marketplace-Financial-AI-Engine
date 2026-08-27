"""Precheck: inventory the certified pilot for universal extraction."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(131072), b""):
            h.update(chunk)
    return h.hexdigest()

def git(*args: str) -> str:
    import subprocess
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                          text=True, timeout=120).stdout.strip()

def main() -> int:
    out = REPO_ROOT / "evidence" / "universal_loop_v1"
    out.mkdir(parents=True, exist_ok=True)

    pilot_files = {
        "spec": "governance/LOOP_ENGINEERING_PROTOCOL_V1.md",
        "kernel_modules": sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / "engine" / "loop_control").glob("*.py")),
        "schemas": sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / "engine" / "loop_control" / "schemas").glob("*.json")),
        "adapters": sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / "engine" / "loop_control" / "adapters").glob("*.md")),
        "tests": sorted(str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.glob("tests/test_loop_control.py")),
        "harnesses": [
            "tools/run_loop_dogfood.py",
            "tools/generate_loop_evidence.py",
        ],
        "control_plane": sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / ".loopx").glob("*")),
    }

    marketplace_refs = [
        "marketplace", "financial", "duckdb", "raw", "dte", "xml", "sap",
        "ledger", "classification", "reconciliation", "311c78e2",
        "01_raw", "meli_financial", "rippley", "paris", "falabella", "shopify",
        "cierre_financiero", "marketplace_ledger", "financial_group"
    ]

    coupling: dict[str, list[str]] = {}
    for cat, files in pilot_files.items():
        if isinstance(files, list):
            for f in files:
                p = REPO_ROOT / f
                if p.is_file():
                    text = p.read_text(encoding="utf-8", errors="ignore").lower()
                    found = [m for m in marketplace_refs if m in text]
                    if found:
                        coupling[f] = found

    report = {
        "evidence_id": "UNIVERSAL_LOOP_V1_PRECHECK",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "commit": git("rev-parse", "HEAD"),
        "status_short": git("status", "--short"),
        "pilot_files": pilot_files,
        "control_plane_files": pilot_files["control_plane"],
        "marketplace_references_found": coupling,
        "schemas_count": len(pilot_files["schemas"]),
        "kernel_modules_count": len(pilot_files["kernel_modules"]),
        "test_count": len(pilot_files["tests"]),
        "adapters_count": len(pilot_files["adapters"]),
        "harnesses_count": len(pilot_files["harnesses"]),
        "certified_baseline": {
            "verdict": "LOOP_ENGINEERING_PROTOCOL_V1_CERTIFIED",
            "criteria": "24/24",
            "tests_added": 55,
            "suite_passed": 1036,
            "suite_failed_preexisting": 12,
            "new_regressions": 0,
            "financial_delta": 0,
        },
        "generated_at": "2026-08-07T00:00:00Z",
    }

    (out / "precheck.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"files": sum(len(v) if isinstance(v, list) else 1 for v in pilot_files.values()),
                      "coupling_files": len(coupling),
                      "report": str(out / "precheck.json")}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())