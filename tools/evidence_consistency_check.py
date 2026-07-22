"""Evidence Consistency Check — FASE 1B-R5.

Auditoría automática que verifica:
  - summary.json contiene todos los campos obligatorios (C3, C6)
  - Cada C*.json tiene trazabilidad completa (C4)
  - No existen afirmaciones en el informe que no estén respaldadas por evidencia (C1, C5)
  - La clasificación 4 niveles es correcta (C7)

Usage:
    python tools/evidence_consistency_check.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / "evidence" / "fase_1b"

REQUIRED_METADATA = [
    ("execution_id", "execution_id"),
    ("commit", "git_commit"),
    ("branch", "git_branch"),
    ("repository", "repository"),
    ("timestamp", "timestamp"),
    ("harness_version", "harness_version"),
    ("status", "status"),
    ("validation", "validation"),
    ("certification", "certification"),
]

REQUIRED_SUMMARY_EXEC = [
    "execution_id",
    "commit",
    "timestamp",
    "harness_version",
    "repository",
    "branch",
]

REQUIRED_SUMMARY_FIELDS = [
    "unique_tests",
    "aggregate_executions",
    "execution_groups",
    "duplicated_files",
    "implementation_status",
    "validation_status",
    "verification_status",
    "certification_status",
    "classification_status",
]

REQUIRED_CLASSIFICATION = [
    "implemented",
    "validated",
    "verified",
    "certified",
    "status",
]

CORRECTIONS = ["C1", "C2", "C3", "C4"]

# ── Verificaciones ───────────────────────────────────────────────────


def check_traceability(
    issues: list[str],
    prefix: str,
    data: dict,
    fields: list[str] | list[tuple[str, str]],
    use_alias: bool = False,
):
    """Check that all required fields exist and are non-empty.

    If use_alias=True, fields are (display_name, actual_field) tuples.
    """
    if use_alias:
        for display, actual in fields:
            val = data.get(actual)
            if val is None or val == "":
                issues.append(f"{prefix}.{actual} ({display}) is missing or empty")
    else:
        for f in fields:
            val = data.get(f)
            if val is None or val == "":
                issues.append(f"{prefix}.{f} is missing or empty")


def check_classification_chain(issues: list[str], prefix: str, cls: dict):
    """Validate 4-level classification invariants."""
    status = cls.get("status", "")
    implemented = cls.get("implemented", False)
    validated = cls.get("validated", False)
    verified = cls.get("verified", False)
    certified = cls.get("certified", False)

    # CERTIFIED requires all lower levels
    if certified and not verified:
        issues.append(f"{prefix}: CERTIFIED without VERIFIED")
    if verified and not validated:
        issues.append(f"{prefix}: VERIFIED without VALIDATED")
    if validated and not implemented:
        issues.append(f"{prefix}: VALIDATED without IMPLEMENTED")

    # status string must match booleans
    if status == "CERTIFIED" and not certified:
        issues.append(f"{prefix}: status=CERTIFIED but certified=False")
    if status == "VERIFIED" and not verified:
        issues.append(f"{prefix}: status=VERIFIED but verified=False")
    if status == "VALIDATED" and not validated:
        issues.append(f"{prefix}: status=VALIDATED but validated=False")
    if status == "IMPLEMENTED" and not implemented:
        issues.append(f"{prefix}: status=IMPLEMENTED but implemented=False")

    if status not in ["IMPLEMENTED", "VALIDATED", "VERIFIED", "CERTIFIED", "NOT_IMPLEMENTED"]:
        issues.append(f"{prefix}: unknown classification status '{status}'")


# ── Main check ───────────────────────────────────────────────────────


def run_check() -> dict:
    issues: list[str] = []
    warnings: list[str] = []

    # Find latest summary
    summaries = sorted(EVIDENCE_DIR.glob("*summary_*.json"))
    if not summaries:
        return {"passed": False, "issues": ["No summary.json found in evidence/fase_1b/"]}
    summary_path = summaries[-1]

    summary = json.load(open(summary_path, encoding="utf-8"))
    ex = summary.get("execution", {})
    s = summary.get("summary", {})
    meta = summary.get("meta", {})
    cls = meta.get("classification", {})

    # C3 + C6: summary.execution fields
    check_traceability(issues, "summary.execution", ex, REQUIRED_SUMMARY_EXEC)
    check_traceability(issues, "summary.summary", s, REQUIRED_SUMMARY_FIELDS)
    check_traceability(issues, "classification", cls, REQUIRED_CLASSIFICATION)

    # C7: classification chain invariants
    check_classification_chain(issues, "summary.meta.classification", cls)

    # C4: Each individual C*.json
    evidence_dir = ex.get("evidence_base_path")
    evidence_path = Path(evidence_dir) if evidence_dir else EVIDENCE_DIR

    for corr in CORRECTIONS:
        found = sorted(evidence_path.glob(f"*{corr}_*.json"))
        if not found:
            issues.append(f"Individual evidence for {corr}: file not found")
            continue
        ev_path = found[0]
        ev = json.load(open(ev_path, encoding="utf-8"))
        m = ev.get("metadata", {})

        # C4: mandatory metadata (with field name aliases)
        check_traceability(issues, f"{corr}.metadata", m, REQUIRED_METADATA, use_alias=True)

        # C7: classification in individual evidence
        ev_cls = ev.get("classification", {})
        check_traceability(issues, f"{corr}.classification", ev_cls, REQUIRED_CLASSIFICATION)
        check_classification_chain(issues, f"{corr}.classification", ev_cls)

        # C2: verification_status
        r3 = ev.get("r3_metrics", {})
        if "verification_status" not in r3:
            issues.append(f"{corr}: r3_metrics.verification_status is missing")
        else:
            vs = r3["verification_status"]
            if vs not in ["VERIFIED", "PARTIALLY_VERIFIED", "NOT_VERIFIED"]:
                issues.append(f"{corr}: r3_metrics.verification_status='{vs}' invalid")

        # C1: no "docstring updated" or cosmetic claims
        desc = m.get("description", "").lower()
        cosmetic_keywords = ["docstring", "cosmetic", "minor", "refactor", "comment", "beautify", "formatting"]
        for kw in cosmetic_keywords:
            if kw in desc:
                issues.append(f"{corr}: description contains cosmetic keyword '{kw}': '{m.get('description')}'")

    # C5: Markdown consistency — cross-reference
    agents_md = ROOT / "AGENTS.md"
    if agents_md.exists():
        md_text = agents_md.read_text(encoding="utf-8")
        # Look for FASE 1B entries that might reference the evidence
        fase_lines = [l.strip() for l in md_text.split("\n") if "FASE 1B" in l]
        if not fase_lines:
            warnings.append("No FASE 1B references found in AGENTS.md")
        # Check for unverifiable claims
        for kw in cosmetic_keywords:
            found_lines = [(i, l.strip()) for i, l in enumerate(md_text.split("\n"), 1) if kw in l.lower()]
            for ln, line in found_lines:
                if "prohibido" not in line.lower() and "prohibition" not in line.lower():
                    warnings.append(f"AGENTS.md line {ln}: contains '{kw}': '{line[:80]}...'")

    passed = len(issues) == 0
    return {
        "passed": passed,
        "issues": issues,
        "warnings": warnings,
        "summary_path": str(summary_path),
        "execution_id": ex.get("execution_id", ""),
        "commit": ex.get("commit", ""),
        "timestamp": ex.get("timestamp", ""),
        "harness_version": ex.get("harness_version", ""),
        "result": "VERIFIED" if passed else "NOT_VERIFIED",
        "verification": {
            "evidence_count": len(CORRECTIONS),
            "issues_found": len(issues),
            "warnings_found": len(warnings),
        },
    }


def main():
    result = run_check()
    print(f"\n{'='*60}")
    print(f"  EVIDENCE CONSISTENCY CHECK — FASE 1B-R5")
    print(f"{'='*60}")
    print(f"  PASSED         : {'YES' if result['passed'] else 'NO'}")
    print(f"  Result         : {result['result']}")
    print(f"  Execution ID   : {result['execution_id']}")
    print(f"  Commit         : {result['commit']}")
    print(f"  Timestamp      : {result['timestamp']}")
    print(f"  Harness Ver    : {result['harness_version']}")
    print(f"\n  VERIFICATION")
    print(f"  {'-'*56}")
    print(f"  Evidence Files : {result['verification']['evidence_count']}")
    print(f"  Issues Found   : {result['verification']['issues_found']}")
    print(f"  Warnings       : {result['verification']['warnings_found']}")
    if result['issues']:
        print(f"\n  ISSUES:")
        for iss in result['issues']:
            print(f"    [FAIL] {iss}")
    if result['warnings']:
        print(f"\n  WARNINGS:")
        for w in result['warnings']:
            print(f"    [WARN] {w}")
    if result['passed']:
        print(f"\n  No issues found. Evidence is consistent and traceable.")
    print(f"\n  Evidence       : {result['summary_path']}")
    print(f"{'='*60}\n")
    return 0 if result['passed'] else 1


if __name__ == "__main__":
    sys.exit(main())
