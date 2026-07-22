"""
verify_runtime_contract.py

Validates the runtime environment against CERTIFICATION_CONTRACT.md v1.0.

Checks:
- All 13 runtime artifacts exist with correct SHA256
- All 5 test artifacts exist with correct SHA256
- Official DB integrity
- Templates present
- Taxonomy files present
- F4 suite files available
- F4 harness available

Usage:
    python tools/verify_runtime_contract.py

Exit codes:
    0 = ALL PASS (contract satisfied)
    1 = ONE OR MORE CHECKS FAILED (contract not satisfied)
"""

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 1
ERROR = 2

status = PASS
results = []


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(artifact_id: str, description: str, path: Path, expected_sha: str = None):
    global status
    if not path.exists():
        results.append((FAIL, artifact_id, f"MISSING: {path}"))
        status = FAIL
        return
    if path.is_file():
        actual = _sha256(path)
        if expected_sha and actual != expected_sha:
            results.append((FAIL, artifact_id,
                f"SHA256 MISMATCH: {path}\n  Expected: {expected_sha}\n  Actual:   {actual}"))
            status = FAIL
            return
        actual_sz = path.stat().st_size
        results.append((PASS, artifact_id, f"OK ({actual_sz:,} bytes)  {path}"))
    else:
        results.append((PASS, artifact_id, f"OK (directory)  {path}"))


def header(label: str):
    results.append((2, "", f"\n{'='*70}"))
    results.append((2, "", f"  {label}"))
    results.append((2, "", f"{'='*70}"))


# ─────────────────────────────────────────────────────────────────────
#  RUNTIME ARTIFACTS (section 5.1 of contract)
# ─────────────────────────────────────────────────────────────────────
header("RUNTIME ARTIFACTS — Required for system operation")

RUNTIME = [
    ("R1",  "Official DB",               "data/db/meli_financial_v4.db",
     "c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce"),
    ("R2",  "Dashboard template",        "templates/dashboard.html",
     "52e30b990dcdb9fa1d88bccd026be66481b5d9fc2e2efd51fd51cad9d24af8f5"),
    ("R3",  "Executive template",        "templates/executive_dashboard.html",
     "818d66cd6a79edf621b0028587e6d2199badacbb2496728cc08093f8b33da388"),
    ("R4",  "Copilot template",          "templates/copilot.html",
     "cc6f956af7a4fa1295507992e1d9c4944b1c6a6cb2ce43c803548fea623a0f89"),
    ("R5",  "Upload Center template",    "templates/upload_center.html",
     "8abd13f04a5ca117c86e487971440868671693d177fe3cf2c01c0e7b664cbc2f"),
    ("R6",  "Documentary Dashboard",     "templates/documentary_dashboard.html",
     "be713aa11edbf97b82a6633106d27c17354461a8a06f59ea7535565d0f2d5c92"),
    ("R7",  "ML taxonomy",              "KnowledgeBase/Marketplace/Taxonomy/ml_v1.json",
     "ba9087b87a54ebc74898d319701741e3876600217080410ea9cf8dcc5a7898ac"),
    ("R8",  "PARIS taxonomy",           "KnowledgeBase/Marketplace/Taxonomy/paris_v1.json",
     "21b7117646badf3324321ff30acbbe405d18cdd748c3e82b643476cbe1c81458"),
    ("R9",  "RIPLEY taxonomy",          "KnowledgeBase/Marketplace/Taxonomy/ripley_v1.json",
     "220f8f314d1377a1e16dde6181de39a1f51c3b7c6a0c0690c2732f653be93cdc"),
    ("R10", "FALABELLA taxonomy",       "KnowledgeBase/Marketplace/Taxonomy/falabella_v1.json",
     "30942ba71f8f30c00a31edf953376304bdf721142b30452cd854b21cdfe5c80f"),
    ("R11", "Taxonomy rules",           "taxonomy/taxonomy_rules.yaml",
     "ba856b6a05c61d5d2c976f0b3d2e239c61c2251ccdd61d2e3a54438d3ff452b6"),
    ("R12", "Taxonomy mappings",        "taxonomy/taxonomy_mappings.yaml",
     "f3e0090370c2048e67d9cd85282c631eb3b63d51e8ffc978dc71f21d36cba233"),
    ("R13", "Taxonomy loader",          "taxonomy/taxonomy_loader.py",
     "f12d67a4f30078f56d431253e9f11c8d8a6f1cc158af8aaceaefa39ba2964b19"),
]

for rid, desc, rel_path, sha in RUNTIME:
    check(rid, desc, ROOT / rel_path, sha)

# ─────────────────────────────────────────────────────────────────────
#  TEST ARTIFACTS (section 5.2 of contract)
# ─────────────────────────────────────────────────────────────────────
header("TEST ARTIFACTS — Required for certification execution")

TEST = [
    ("T1", "V8 Baseline DB",
     "data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db",
     "733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00"),
    ("T2", "V9 Baseline DB",
     "data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/meli_financial_v4.db",
     "c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce"),
    ("T3", "Test conftest",
     "tests/conftest.py",
     "508f57c442e8078e1979d3f60ffb5c768d4d49c5e32239109a2f7e44db4522f0"),
    ("T4", "F4 harness",
     "tools/run_f4_suites.py",
     "172a4462f5498f101aed6110f2705c5b1c8fca0cadf8bcd3e819ff1d46f86c31"),
    ("T5", "F3 traceability fixture",
     "tests/fixtures/f3_03/f3_03_fixture.xlsx",
     "9be8effcba44cce1810e775651f872b2b4891fb61850d0cf5a7aa6859fed7d9a"),
]

for tid, desc, rel_path, sha in TEST:
    check(tid, desc, ROOT / rel_path, sha)

# ─────────────────────────────────────────────────────────────────────
#  F4 SUITE FILES (section 6.3 of contract)
# ─────────────────────────────────────────────────────────────────────
header("F4 CERTIFICATION SUITE — 96 tests in 4 files")

SUITE = [
    "tests/test_certification_gate.py",
    "tests/test_semantic_consistency.py",
    "tests/test_f4_traceability.py",
    "tests/test_taxonomy_equivalence.py",
]

for rel_path in SUITE:
    p = ROOT / rel_path
    if p.exists():
        sz = p.stat().st_size
        results.append((PASS, "S", f"OK ({sz:,} bytes)  {rel_path}"))
    else:
        results.append((FAIL, "S", f"MISSING: {rel_path}"))
        status = FAIL

# ─────────────────────────────────────────────────────────────────────
#  CONTRACT DOCUMENT (section 4)
# ─────────────────────────────────────────────────────────────────────
header("CONTRACT DOCUMENTS")

contracts = [
    ("CERTIFICATION_CONTRACT.md",
     "governance/coordination/CERTIFICATION_CONTRACT.md"),
    ("Runtime Manifest",
     "governance/coordination/runtime_manifest.json"),
]

for desc, rel_path in contracts:
    check("C", desc, ROOT / rel_path)

# ─────────────────────────────────────────────────────────────────────
#  REPORT
# ─────────────────────────────────────────────────────────────────────
header("SUMMARY")

passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)

for code, aid, msg in results:
    if code == PASS:
        prefix = "  PASS"
    elif code == FAIL:
        prefix = "  FAIL"
    else:
        prefix = "       "
    print(f"{prefix}  [{aid}] {msg}")

print()
print(f"  Total: {passed + failed} checks, {passed} PASS, {failed} FAIL")
print()

if status == PASS:
    print("  VERDICT: RUNTIME_CONTRACT_SATISFIED")
    print("  All required artifacts are present with correct hashes.")
    print("  F4 certification suite is available for execution.")
else:
    print("  VERDICT: RUNTIME_CONTRACT_NOT_SATISFIED")
    print("  One or more required artifacts are missing or corrupted.")
    print("  See above for details.")

sys.exit(status)
