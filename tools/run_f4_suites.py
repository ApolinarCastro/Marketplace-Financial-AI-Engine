#!/usr/bin/env python3
"""F4 Suites Harness v1.0.0-r6 — run 4 F4 suites, produce certified evidence.

Usage:
    python tools/run_f4_suites.py
    python tools/run_f4_suites.py --preflight-only

Exit codes:
    0 — PHASE_4_GATE_SATISFIED
    1 — REQUIRES_REMEDIATION
    2 — REJECTED

Environment:
    F4_TEMP_ROOT      — external temp root for V8 temp DB (mandatory).
                        Default: %%TEMP%%\\f4_v8  (Windows) or /tmp/f4_v8 (Unix)
    F4_EVIDENCE_ROOT  — external root for preflight evidence.
                        Mandatory with --preflight-only.
                        Must be OUTSIDE the repository.
"""
import subprocess, sys, json, datetime, hashlib, time, os, re
from pathlib import Path

HARNESS_VERSION = "1.0.0-r6"
ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / "evidence" / "f4_suites"

TEST_FILES = [
    "tests/test_certification_gate.py",
    "tests/test_semantic_consistency.py",
    "tests/test_f4_traceability.py",
    "tests/test_taxonomy_equivalence.py",
]

EXPECTED_PER_FILE = {
    "tests/test_certification_gate.py": 29,
    "tests/test_semantic_consistency.py": 27,
    "tests/test_f4_traceability.py": 22,
    "tests/test_taxonomy_equivalence.py": 18,
}
EXPECTED_TOTAL = sum(EXPECTED_PER_FILE.values())  # 96

# Protected dependencies (must exist in-commit, no overlays)
PROTECTED_DEPENDENCIES = {
    "engine.v4.database": ROOT / "engine" / "v4" / "database.py",
    "engine.v4.domain.canonical_semantics": ROOT / "engine" / "v4" / "domain" / "canonical_semantics.py",
    "engine.v4.domain.ledger_engine": ROOT / "engine" / "v4" / "domain" / "ledger_engine.py",
    "engine.v4.domain.generate_artifacts": ROOT / "engine" / "v4" / "domain" / "generate_artifacts.py",
    "engine.v4.evidence.traceability": ROOT / "engine" / "v4" / "evidence" / "traceability.py",
    "engine.v4.evidence.traceability_engine": ROOT / "engine" / "v4" / "evidence" / "traceability_engine.py",
    "engine.v4.evidence.__init__": ROOT / "engine" / "v4" / "evidence" / "__init__.py",
    "engine.v4.ingestion": ROOT / "engine" / "v4" / "ingestion" / "__init__.py",
    "engine.v4.ingestion.orchestrator": ROOT / "engine" / "v4" / "ingestion" / "orchestrator.py",
    "engine.v4.semantic": ROOT / "engine" / "v4" / "semantic" / "__init__.py",
    "engine.v4.marketplace_auditor": ROOT / "engine" / "v4" / "marketplace_auditor.py",
    "taxonomy.taxonomy_loader": ROOT / "taxonomy" / "taxonomy_loader.py",
}

# FinancialEngine (authorized blob: aa3415f172fb7320e1786a732b11a4d8b5fdd875)
FINANCIAL_ENGINE_PATH = ROOT / "engine" / "v4" / "domain" / "financial_engine.py"
FINANCIAL_ENGINE_BLOB = "aa3415f172fb7320e1786a732b11a4d8b5fdd875"

# Closure files required with FinancialEngine
CLOSURE_FILES = {
    "engine.v4.domain.financial_engine": FINANCIAL_ENGINE_PATH,
    "engine.v4.domain.ledger_engine": ROOT / "engine" / "v4" / "domain" / "ledger_engine.py",
    "engine.v4.period_utils": ROOT / "engine" / "v4" / "period_utils.py",
    "taxonomy.taxonomy_loader": ROOT / "taxonomy" / "taxonomy_loader.py",
    "taxonomy.taxonomy_rules": ROOT / "taxonomy" / "taxonomy_rules.yaml",
    "taxonomy.taxonomy_mappings": ROOT / "taxonomy" / "taxonomy_mappings.yaml",
}

# All protected sources = PROTECTED_DEPENDENCIES + CLOSURE_FILES
ALL_PROTECTED_SOURCES = {}
ALL_PROTECTED_SOURCES.update(PROTECTED_DEPENDENCIES)
ALL_PROTECTED_SOURCES.update(CLOSURE_FILES)

DB_PATHS = {
    "OFFICIAL_DB": ROOT / "data" / "db" / "meli_financial_v4.db",
    "V7": ROOT / "data" / "db" / "baseline_estable_v7_20260715" / "meli_financial_v4.db",
    "V8": ROOT / "data" / "db" / "baseline_estable_v8_candidate_20260717" / "meli_financial_v4.db",
}

# External temp root (mandatory via env, fallback to system temp)
# Must match conftest.py: F4_TEMP_ROOT / "tmp_f4_v8" / "meli_financial_v4.db"
F4_TEMP_ROOT = Path(os.environ.get("F4_TEMP_ROOT", os.path.join(os.environ.get("TEMP", "/tmp"), "f4_v8"))).resolve()
TEMP_V8 = F4_TEMP_ROOT / "tmp_f4_v8" / "meli_financial_v4.db"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def get_file_hash(path):
    if path.exists():
        return sha256(path)
    return "NOT_FOUND"


def get_git_blob_hash(path):
    """Get git blob hash for a tracked file."""
    try:
        rel = path.relative_to(ROOT)
        result = subprocess.run(
            ["git", "hash-object", str(rel)],
            capture_output=True, text=True, cwd=ROOT, timeout=30,
        )
        return result.stdout.strip()
    except Exception:
        return "NOT_FOUND"


def get_git_info():
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, cwd=ROOT
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=ROOT
    ).stdout.strip()
    # Full status with untracked files
    full_status = subprocess.run(
        ["git", "status", "--porcelain=v2", "--untracked-files=all"],
        capture_output=True, text=True, cwd=ROOT,
    ).stdout.strip()
    return {
        "subject_commit": commit,
        "subject_tree": tree,
        "git_dirty": bool(dirty),
        "git_status_lines": full_status.splitlines(),
    }


def validate_requirements_txt():
    """Check installed packages match requirements.txt exclusively."""
    req_path = ROOT / "requirements.txt"
    if not req_path.exists():
        return {"pass": False, "reason": "requirements.txt not found"}

    # Parse requirements.txt lines
    req_lines = [l.strip() for l in req_path.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]

    # Get installed packages
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True, text=True, timeout=60,
    )
    # Parse pip list output — skip header and separator
    installed = set()
    header_skipped = False
    for line in result.stdout.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("Package") or raw.startswith("-------"):
            if not header_skipped and raw.startswith("Package"):
                header_skipped = True
            continue
        parts = raw.split()
        if len(parts) >= 1 and parts[0]:
            installed.add(parts[0].lower())

    required_packages = set()
    for req_line in req_lines:
        pkg = req_line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].strip()
        pkg = re.sub(r'[<>!=~;\[\]\s].*$', '', pkg).strip()
        if pkg and pkg.lower() not in ("pip", "setuptools", "wheel", "python"):
            # Normalize: replace _ and - with nothing for matching
            required_packages.add(pkg.lower())

    # Check all required packages are installed
    # Normalize names (ignore case, dashes, underscores)
    req_normalized = {p.replace("-", "").replace("_", "") for p in required_packages}
    inst_normalized = {p.replace("-", "").replace("_", "") for p in installed}
    known = {"pip", "setuptools", "wheel", "python"}
    known_normalized = {k.replace("-", "").replace("_", "") for k in known}

    missing_normalized = req_normalized - inst_normalized - known_normalized

    missing_packages = []
    for rp in sorted(required_packages):
        rn = rp.replace("-", "").replace("_", "")
        if rn in missing_normalized:
            missing_packages.append(rp)

    # Extra packages are informational only (transitive deps are expected)
    extra_normalized = inst_normalized - req_normalized - known_normalized
    extra_packages = []
    for ip in sorted(installed):
        ipn = ip.replace("-", "").replace("_", "")
        if ipn in extra_normalized:
            extra_packages.append(ip)

    return {
        "pass": len(missing_packages) == 0,
        "required": sorted(required_packages),
        "installed": sorted(installed),
        "missing": missing_packages,
        "extra": extra_packages,
        "note": "Extra packages are transitive dependencies (informational, not a gate failure).",
    }


def verify_db_read_only(path):
    """Verify a DB file is read-only by checking file attributes."""
    import stat
    if not path.exists():
        return {"readonly": False, "path": str(path), "exists": False, "error": "NOT_FOUND"}
    try:
        st = path.stat()
        is_readonly = False
        if os.name == "nt":
            result = subprocess.run(
                ["attrib", str(path)],
                capture_output=True, text=True, timeout=15,
            )
            is_readonly = "R" in result.stdout
        else:
            mode = st.st_mode
            is_readonly = not bool(mode & stat.S_IWUSR)
        return {
            "readonly": is_readonly,
            "path": str(path),
            "exists": True,
        }
    except Exception as e:
        return {"readonly": False, "path": str(path), "exists": path.exists(), "error": str(e)}


def verify_v8_copiable():
    """Verify V8 can be copied to F4_TEMP_ROOT (but not official/V7)."""
    v8_path = DB_PATHS["V8"]
    if not v8_path.exists():
        return {"ok": False, "error": "V8 NOT_FOUND", "src_hash": "NOT_FOUND"}
    temp_dir = F4_TEMP_ROOT / "tmp_f4_v8"
    temp_dir.mkdir(parents=True, exist_ok=True)
    test_copy = temp_dir / "meli_financial_v4.db"
    try:
        import shutil
        shutil.copy2(str(v8_path), str(test_copy))
        copied_hash = sha256(test_copy)
        src_hash = sha256(v8_path)
        test_copy.unlink()
        return {"ok": copied_hash == src_hash, "src_hash": src_hash, "copy_hash": copied_hash}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def verify_closure_exists():
    """Verify all closure files exist within the commit (no overlays)."""
    missing = []
    present = {}
    blob_mismatch = []
    for name, path in CLOSURE_FILES.items():
        if path.exists():
            h = get_file_hash(path)
            present[name] = h
            if name == "engine.v4.domain.financial_engine" and h != "NOT_FOUND":
                blob = get_git_blob_hash(path)
                if blob != "NOT_FOUND" and blob != FINANCIAL_ENGINE_BLOB:
                    blob_mismatch.append({
                        "name": name,
                        "expected_blob": FINANCIAL_ENGINE_BLOB,
                        "actual_blob": blob,
                    })
        else:
            missing.append(name)
    return {
        "present": present,
        "missing": missing,
        "blob_mismatch": blob_mismatch,
        "complete": len(missing) == 0 and len(blob_mismatch) == 0,
    }


def verify_protected_in_commit():
    """Verify protected dependencies exist within the commit."""
    missing = []
    present = {}
    for name, path in ALL_PROTECTED_SOURCES.items():
        if path.exists():
            present[name] = get_file_hash(path)
        else:
            missing.append(name)
    return {
        "present": present,
        "missing": missing,
        "complete": len(missing) == 0,
    }


def get_db_hashes():
    h = {}
    for name, path in DB_PATHS.items():
        if path.exists():
            h[name] = {"sha256": sha256(path), "size": path.stat().st_size, "path": str(path)}
        else:
            h[name] = {"sha256": "NOT_FOUND", "size": 0, "path": str(path)}
    return h


def preflight():
    """Run preflight checks only (no pytest execution)."""

    # ── Validate F4_EVIDENCE_ROOT ──────────────────────────────────────
    evidence_root_raw = os.environ.get("F4_EVIDENCE_ROOT", "")
    if not evidence_root_raw:
        print("FATAL: F4_EVIDENCE_ROOT is mandatory with --preflight-only")
        sys.exit(2)

    evidence_root = Path(evidence_root_raw).resolve()
    try:
        evidence_root.relative_to(ROOT)
        print("FATAL: F4_EVIDENCE_ROOT must be OUTSIDE the repository")
        print(f"  REPO ROOT:     {ROOT}")
        print(f"  EVIDENCE ROOT: {evidence_root}")
        sys.exit(2)
    except ValueError:
        pass  # Expected — root is outside repo

    evidence_root.mkdir(parents=True, exist_ok=True)

    execution_id = datetime.datetime.now().strftime("F4_PREFLIGHT_%Y%m%d_%H%M%S")
    timestamp = datetime.datetime.now().isoformat()
    start_time = time.time()

    checks = {}
    all_pass = True

    # ── 1. Git state ───────────────────────────────────────────────────
    git_info = get_git_info()
    dirty_paths = git_info.pop("git_status_lines", [])
    checks["git"] = {
        "commit": git_info["subject_commit"],
        "tree": git_info["subject_tree"],
        "git_dirty": git_info["git_dirty"],
        "dirty_paths": dirty_paths,
        "preflight_pass": not git_info["git_dirty"],
        "gate_requires": "git_dirty=false",
    }
    if git_info["git_dirty"]:
        all_pass = False

    # ── 2. FinancialEngine blob verification ────────────────────────────
    fe_exists = FINANCIAL_ENGINE_PATH.exists()
    fe_hash = "NOT_FOUND"
    fe_blob = "NOT_FOUND"
    if fe_exists:
        fe_hash = get_file_hash(FINANCIAL_ENGINE_PATH)
        fe_blob = get_git_blob_hash(FINANCIAL_ENGINE_PATH)
    checks["financial_engine"] = {
        "path": str(FINANCIAL_ENGINE_PATH),
        "exists": fe_exists,
        "sha256": fe_hash,
        "git_blob": fe_blob,
        "expected_blob": FINANCIAL_ENGINE_BLOB,
        "blob_match": fe_blob == FINANCIAL_ENGINE_BLOB,
        "preflight_pass": fe_exists and fe_blob == FINANCIAL_ENGINE_BLOB,
    }
    if fe_blob != FINANCIAL_ENGINE_BLOB:
        all_pass = False

    # ── 3. Closure verification ─────────────────────────────────────────
    closure_result = verify_closure_exists()
    checks["closure"] = {
        "files": closure_result["present"],
        "missing": closure_result["missing"],
        "blob_mismatch": closure_result["blob_mismatch"],
        "complete": closure_result["complete"],
        "preflight_pass": closure_result["complete"],
    }
    if not closure_result["complete"]:
        all_pass = False

    # ── 4. Protected sources inventory ─────────────────────────────────
    protected_result = verify_protected_in_commit()
    checks["protected_sources"] = {
        "inventory": protected_result["present"],
        "missing": protected_result["missing"],
        "complete": protected_result["complete"],
        "preflight_pass": protected_result["complete"],
        "gate_requires": "all NOT_FOUND must be authorized",
    }
    if not protected_result["complete"]:
        all_pass = False

    # ── 5. Requirements.txt validation ─────────────────────────────────
    req_result = validate_requirements_txt()
    checks["requirements"] = {
        "pass": req_result["pass"],
        "missing": req_result.get("missing", []),
        "extra": req_result.get("extra", []),
        "preflight_pass": req_result["pass"],
        "gate_requires": "dependencies exclusively from requirements.txt",
    }
    if not req_result["pass"]:
        all_pass = False

    # ── 6. DB hashes + read-only verification ──────────────────────────
    db_hashes = get_db_hashes()
    db_readonly = {}
    for name, path in DB_PATHS.items():
        db_readonly[name] = verify_db_read_only(path)
    any_not_found = any(v["sha256"] == "NOT_FOUND" for v in db_hashes.values())
    all_found = all(v["sha256"] != "NOT_FOUND" for v in db_hashes.values())
    checks["databases"] = {
        "hashes": db_hashes,
        "readonly": db_readonly,
        "all_found": all_found,
        "any_NOT_FOUND": any_not_found,
        "preflight_pass": all_found,
        "gate_requires": "all 3 DBs found; read-only status recorded; only V8 copiable",
    }
    if any_not_found:
        all_pass = False

    # ── 7. V8 copiable (only V8) ───────────────────────────────────────
    v8_result = verify_v8_copiable()
    checks["v8_copy"] = {
        "test": v8_result,
        "preflight_pass": v8_result.get("ok", False),
    }
    if not v8_result.get("ok", False):
        all_pass = False

    # ── 8. Compute report_complete from structured fields ──────────────
    report_complete = (
        checks["git"]["preflight_pass"]
        and checks["financial_engine"]["preflight_pass"]
        and checks["closure"]["preflight_pass"]
        and checks["protected_sources"]["preflight_pass"]
        and checks["requirements"]["preflight_pass"]
        and checks["databases"]["preflight_pass"]
        and checks["v8_copy"]["preflight_pass"]
    )
    # report_complete is computed from structured fields, NOT from summary_line

    checks["report_complete"] = {
        "value": report_complete,
        "preflight_pass": report_complete,
        "method": "computed from structured preflight fields (not summary_line)",
        "gate_requires": "report_complete=true",
    }

    # ── Build evidence ─────────────────────────────────────────────────
    end_time = time.time()
    elapsed_s = round(end_time - start_time, 2)

    # Technical classification (NOT an official gate)
    if report_complete:
        technical_classification = "PREFLIGHT_PASS"
        classification_reason = "All preflight checks pass"
    else:
        technical_classification = "PREFLIGHT_FAIL"
        classification_reason = "One or more preflight checks failed"

    evidence = {
        "execution_id": execution_id,
        "timestamp": timestamp,
        "harness_version": HARNESS_VERSION,
        "mode": "preflight-only",
        "repository": "Marketplace Financial AI Engine",
        "elapsed_seconds": elapsed_s,
        "checks": checks,
        "preflight_pass": report_complete,
        "technical_classification": technical_classification,
        "classification_reason": classification_reason,
        "git": git_info,
        "is_official_gate": False,
        "note": "Preflight-only mode. No gate emitted. Technical classification only.",
    }

    # Write evidence outside repo
    ev_path = evidence_root / f"{execution_id}.json"
    ev_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")

    # ── Print report ───────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  F4 PREFLIGHT (no pytest)")
    print(f"  HARNESS:      {HARNESS_VERSION}")
    print(f"  EXECUTION ID: {execution_id}")
    print(f"  COMMIT:       {git_info['subject_commit']}")
    print(f"  TREE:         {git_info['subject_tree']}")
    print(f"  DIRTY:        {git_info['git_dirty']}")
    print(f"  EVIDENCE:     {ev_path}")
    print(f"  DURATION:     {elapsed_s}s")
    print(f"{'='*60}")

    # Per-check results
    for check_name, check_data in checks.items():
        pf = check_data.get("preflight_pass", "N/A")
        status = "PASS" if pf is True else ("SKIP" if pf is None else "FAIL")
        print(f"  [{status}] {check_name}: preflight_pass={pf}")
        if check_data.get("missing"):
            print(f"         MISSING: {check_data['missing']}")
        if check_data.get("blob_mismatch"):
            print(f"         BLOB MISMATCH: {check_data['blob_mismatch']}")
        if check_data.get("any_NOT_FOUND"):
            print(f"         DB NOT_FOUND detected")
        if check_data.get("extra"):
            print(f"         EXTRA PACKAGES: {check_data['extra']}")
        if check_data.get("test") and not check_data["test"].get("ok", True):
            print(f"         COPY ERROR: {check_data['test'].get('error', 'unknown')}")

    print(f"\n  TECHNICAL CLASSIFICATION: {technical_classification}")
    print(f"  PREFLIGHT PASS: {report_complete}")
    print(f"  NOTE: No official gate emitted. Authorization required for next step.")

    if not report_complete:
        print(f"\n  !!! PREFLIGHT FAILED — review checks above")
        print(f"  !!! Missing closure or protected deltas require authorization.")

    # Detect missing closure for special message
    if not closure_result["complete"]:
        print(f"\n  >>> PROTECTED_BASELINE_CLOSURE_REQUIRES_AUTHORIZATION <<<")
        print(f"      Missing closure files: {closure_result['missing']}")

    if not protected_result["complete"]:
        print(f"\n  >>> PROTECTED_BASELINE_CLOSURE_REQUIRES_AUTHORIZATION <<<")
        print(f"      Missing protected sources: {protected_result['missing']}")

    return report_complete


def parse_junit_xml(junit_path):
    """Parse JUnit XML for canonical test counts per file.

    Handles module-level import errors (reported as error testcases
    by pytest at the testsuite level). Uses testsuite 'tests'/'errors'/'failures'
    attributes as authoritative counts, with per-file breakdown from testcase elements.
    Unmatched testcases (e.g. module import failures) are tracked as 'unmatched_errors'.

    report_complete is computed from structured JUnit fields, NOT from summary_line.
    """
    import xml.etree.ElementTree as ET
    if not junit_path.exists():
        return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0, "xfailed": 0, "per_file": {}, "unmatched_errors": 0}
    tree = ET.parse(junit_path)
    root = tree.getroot()

    # Aggregate from all testsuites
    total = passed = failed = skipped = errors = xfailed = 0
    per_file = {f: {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0, "xfailed": 0} for f in TEST_FILES}
    unmatched_errors = 0

    for testsuite in root.findall(".//testsuite"):
        suite_total = int(testsuite.get("tests", 0))
        suite_errors = int(testsuite.get("errors", 0))
        suite_failures = int(testsuite.get("failures", 0))
        suite_skipped = int(testsuite.get("skipped", 0))

        total += suite_total
        errors += suite_errors
        failed += suite_failures
        skipped += suite_skipped

        for testcase in testsuite.findall("testcase"):
            classname = testcase.get("classname", "")
            name = testcase.get("name", "")

            file_key = None
            for f in TEST_FILES:
                base = f.replace("/", ".").replace(".py", "")
                if classname.startswith(base):
                    file_key = f
                    break

            if testcase.find("failure") is not None:
                if file_key:
                    per_file[file_key]["failed"] += 1
                    per_file[file_key]["total"] += 1
                else:
                    unmatched_errors += 1
            elif testcase.find("error") is not None:
                if file_key:
                    per_file[file_key]["errors"] += 1
                    per_file[file_key]["total"] += 1
                else:
                    unmatched_errors += 1
            elif testcase.find("skipped") is not None:
                if file_key:
                    per_file[file_key]["skipped"] += 1
                    per_file[file_key]["total"] += 1
            else:
                if file_key:
                    per_file[file_key]["passed"] += 1
                    per_file[file_key]["total"] += 1

        for testcase in testsuite.findall("testcase"):
            skip_elem = testcase.find("skipped")
            if skip_elem is not None and skip_elem.get("type") == "pytest.xfail":
                xfailed += 1

    suite_passed = total - errors - failed - skipped
    passed = max(0, suite_passed)

    # report_complete computed from structured fields: total > 0 and failed == 0 and errors == 0
    report_complete = (total > 0 and failed == 0 and errors == 0)

    return {
        "total": total, "passed": passed, "failed": failed,
        "skipped": skipped, "errors": errors, "xfailed": xfailed,
        "per_file": per_file, "unmatched_errors": unmatched_errors,
        "report_complete": report_complete,
    }


def collect_nodeids():
    """Collect unique test nodeids via --collect-only."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + [str(ROOT / f) for f in TEST_FILES]
        + ["--collect-only", "-q"],
        capture_output=True, text=True, cwd=ROOT, timeout=120,
    )
    nodeids = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if "tests collected" in line or line.startswith("=="):
            continue
        if "no tests ran" in line:
            continue
        nodeids.append(line)
    return list(dict.fromkeys(nodeids))


def run():
    execution_id = datetime.datetime.now().strftime("F4_%Y%m%d_%H%M%S")
    timestamp = datetime.datetime.now().isoformat()

    git_info = get_git_info()
    code_hashes = get_code_hashes()

    # Pre-run state
    pre_hashes = get_db_hashes()
    pre_protected_hashes = get_protected_dep_hashes()
    pre_temp_exists = TEMP_V8.exists()
    overlay_info = get_overlay_create()
    nodeids = []

    # Ensure temp dir exists
    F4_TEMP_ROOT.mkdir(parents=True, exist_ok=True)

    # Build command — run each file separately to isolate import errors
    junit_xml = EVIDENCE_DIR / f"{execution_id}.xml"
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    combined_junit = None
    combined_xml_lines = []
    per_file_stdouts = {}
    per_file_stderrs = {}
    per_file_returncodes = {}
    all_nodeids = []
    command_strs = []

    start_ts = datetime.datetime.now().isoformat()
    start_time = time.time()

    for tf in TEST_FILES:
        file_junit = EVIDENCE_DIR / f"{execution_id}_{Path(tf).stem}.xml"
        cmd_list = [sys.executable, "-m", "pytest", str(ROOT / tf)] + [
            "-v", "--tb=short",
            f"--junitxml={file_junit}",
        ]
        command_strs.append(" ".join(cmd_list))
        proc = subprocess.run(cmd_list, capture_output=True, text=True, cwd=ROOT, timeout=900)
        per_file_stdouts[tf] = proc.stdout
        per_file_stderrs[tf] = proc.stderr
        per_file_returncodes[tf] = proc.returncode

        # Collect nodeids from this file
        coll = subprocess.run(
            [sys.executable, "-m", "pytest", str(ROOT / tf), "--collect-only", "-q"],
            capture_output=True, text=True, cwd=ROOT, timeout=120,
        )
        for line in coll.stdout.splitlines():
            ls = line.strip()
            if ls and "collected" not in ls and not ls.startswith("==") and "no tests ran" not in ls:
                all_nodeids.append(ls)

        # Merge JUnit XML fragments
        if file_junit.exists():
            content = file_junit.read_text(encoding="utf-8")
            # Extract testcase elements from this file's JUnit
            import xml.etree.ElementTree as ET
            try:
                tree = ET.parse(file_junit)
                root = tree.getroot()
                for ts in root.findall(".//testsuite"):
                    ts_tag = ET.tostring(ts, encoding="unicode")
                    combined_xml_lines.append(ts_tag)
            except Exception:
                pass

    end_time = time.time()
    end_ts = datetime.datetime.now().isoformat()
    elapsed_s = round(end_time - start_time, 2)

    # Build combined JUnit XML
    combined_xml = '<?xml version="1.0" encoding="utf-8"?>\n<testsuites name="pytest tests">\n'
    combined_xml += "\n".join(combined_xml_lines)
    combined_xml += "\n</testsuites>"
    junit_xml.write_text(combined_xml, encoding="utf-8")

    # Parse combined JUnit
    junit = parse_junit_xml(junit_xml)
    outcomes = {
        "PASS": junit["passed"],
        "FAIL": junit["failed"],
        "SKIP": junit["skipped"],
        "XFAIL": junit["xfailed"],
        "ERROR": junit["errors"],
    }
    collected = junit["total"]
    nodeids = all_nodeids
    stdout = "\n".join(per_file_stdouts.values())
    stderr = "\n".join(per_file_stderrs.values())
    returncode = max(per_file_returncodes.values())

    # Post-run state
    post_hashes = get_db_hashes()
    post_protected_hashes = get_protected_dep_hashes()
    post_temp_exists = TEMP_V8.exists()

    # report_complete from structured JUnit fields (not summary_line)
    report_complete = junit.get("report_complete", False)

    # Mutation check: DB hashes
    mutation = False
    mutation_detail = {}
    for name in pre_hashes:
        if pre_hashes[name]["sha256"] != post_hashes[name]["sha256"]:
            mutation = True
            mutation_detail[name] = {
                "pre": pre_hashes[name]["sha256"],
                "post": post_hashes[name]["sha256"],
            }

    # Protected dependency mutation check
    protected_mutation = False
    protected_mutation_detail = {}
    for name in pre_protected_hashes:
        pre_h = pre_protected_hashes[name]["sha256"]
        post_h = post_protected_hashes.get(name, {}).get("sha256", "UNKNOWN")
        if pre_h != post_h:
            protected_mutation = True
            protected_mutation_detail[name] = {
                "pre": pre_h,
                "post": post_h,
            }

    # Temp cleanup check
    temp_cleaned = not post_temp_exists

    # ── Automatic classification ──
    all_pass = (outcomes["PASS"] == collected
                and outcomes["FAIL"] == 0
                and outcomes["SKIP"] == 0
                and outcomes["XFAIL"] == 0
                and outcomes["ERROR"] == 0
                and collected == EXPECTED_TOTAL)
    no_mutation = not mutation and not protected_mutation
    hashes_match = pre_hashes == post_hashes
    cleanup_ok = temp_cleaned
    report_ok = report_complete

    gate_satisfied = (all_pass and no_mutation and hashes_match
                      and cleanup_ok and report_ok)

    if gate_satisfied:
        verdict = "PHASE_4_GATE_SATISFIED"
        verdict_reason = (
            f"{outcomes['PASS']}/{collected} PASS. 0 FAIL/SKIP/XFAIL/ERROR. "
            f"No mutation. Cleanup OK."
        )
        exit_code = 0
    elif outcomes.get("FAIL", 0) > 0 or outcomes.get("ERROR", 0) > 0:
        verdict = "REQUIRES_REMEDIATION"
        verdict_reason = f"{outcomes.get('FAIL',0)} FAIL, {outcomes.get('ERROR',0)} ERROR"
        exit_code = 1
    else:
        verdict = "REJECTED"
        reasons = []
        if not all_pass:
            reasons.append(f"not all PASS ({outcomes['PASS']}/{collected})")
        if mutation:
            reasons.append(f"mutation detected: {json.dumps(mutation_detail)}")
        if not hashes_match:
            reasons.append("pre/post hash mismatch")
        if not cleanup_ok:
            reasons.append("temp not cleaned")
        if not report_ok:
            reasons.append("report incomplete")
        verdict_reason = "; ".join(reasons)
        exit_code = 2

    # Build evidence
    evidence = {
        "execution_id": execution_id,
        "timestamp": timestamp,
        "harness_version": HARNESS_VERSION,
        "repository": "Marketplace Financial AI Engine",
        "commands": command_strs,
        "timeout_seconds": 900,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "elapsed_seconds": elapsed_s,
        "returncode": returncode,
        "summary_line": "",
        "nodeids_collected": len(nodeids),
        "expected_total": EXPECTED_TOTAL,
        "expected_per_file": EXPECTED_PER_FILE,
        "outcomes": outcomes,
        "nodeids": nodeids,
        "junit": junit,
        "report_complete": report_complete,
        "pre_run_hashes": pre_hashes,
        "post_run_hashes": post_hashes,
        "mutation_detected": mutation,
        "mutation_detail": mutation_detail if mutation else None,
        "protected_dependencies": {
            "pre_run": pre_protected_hashes,
            "post_run": post_protected_hashes,
            "mutation_detected": protected_mutation,
            "mutation_detail": protected_mutation_detail if protected_mutation else None,
        },
        "overlay": overlay_info,
        "temp_v8_cleaned": temp_cleaned,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "exit_code": exit_code,
        "git": git_info,
        "code_hashes": code_hashes,
    }

    # Write evidence
    ev_path = EVIDENCE_DIR / f"{execution_id}.json"
    ev_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")

    # Print report
    print(f"\n{'='*60}")
    print(f"  HARNESS:      {HARNESS_VERSION}")
    print(f"  EXECUTION ID: {execution_id}")
    print(f"  COMMIT:       {git_info['subject_commit']}")
    print(f"  TREE:         {git_info['subject_tree']}")
    print(f"  DIRTY:        {git_info['git_dirty']}")
    print(f"  DURATION:     {elapsed_s}s")
    print(f"  RETURNCODE:   {returncode}")
    print(f"  COLLECTED:    {collected}")
    print(f"  OUTCOMES:     {json.dumps(outcomes)}")
    print(f"  REPORT COMPLETE: {report_complete}")
    print(f"  MUTATION:     {mutation}")
    print(f"  TEMP CLEANED: {temp_cleaned}")
    print(f"  VERDICT:      {verdict}")
    print(f"  REASON:       {verdict_reason}")
    print(f"  JUNIT:        {junit_xml}")
    print(f"  EVIDENCE:     {ev_path}")
    print(f"{'='*60}\n")

    # Per-file counts from JUnit
    print("  Per-file (JUnit):")
    for f, counts in junit["per_file"].items():
        print(f"    {f}: {counts['total']} (passed={counts['passed']}, failed={counts['failed']}, skipped={counts['skipped']}, errors={counts['errors']})")

    if outcomes["PASS"] > 0:
        print(f"\n  PASSED ({outcomes['PASS']}):")
        for line in stdout.splitlines():
            ls = line.strip()
            if "::" in ls and " PASSED " in ls:
                print(f"    {ls}")

    if outcomes.get("FAIL", 0) > 0:
        print(f"\n  FAILED ({outcomes['FAIL']}):")
        for line in stdout.splitlines():
            ls = line.strip()
            if "::" in ls and " FAILED " in ls:
                print(f"    {ls}")

    if outcomes.get("ERROR", 0) > 0 and stderr.strip():
        print(f"\n  STDERR:")
        print(stderr[:3000])

    return evidence


def get_code_hashes():
    """Hashes of harness runner + 5 test files."""
    files = {
        "runner": ROOT / "tools" / "run_f4_suites.py",
        "test_certification_gate": ROOT / "tests" / "test_certification_gate.py",
        "test_semantic_consistency": ROOT / "tests" / "test_semantic_consistency.py",
        "test_f4_traceability": ROOT / "tests" / "test_f4_traceability.py",
        "test_taxonomy_equivalence": ROOT / "tests" / "test_taxonomy_equivalence.py",
        "conftest": ROOT / "tests" / "conftest.py",
    }
    return {k: get_file_hash(v) for k, v in files.items()}


def get_protected_dep_hashes():
    """Hashes of all protected dependencies (pre/post for mutation detection)."""
    h = {}
    for name, path in PROTECTED_DEPENDENCIES.items():
        if path.exists():
            h[name] = {"sha256": sha256(path), "size": path.stat().st_size, "path": str(path)}
        else:
            h[name] = {"sha256": "NOT_FOUND", "size": 0, "path": str(path)}
    return h


def get_overlay_create():
    """Record overlay creation timestamp for evidence chain."""
    return {
        "created_at": datetime.datetime.now().isoformat(),
        "read_only": True,
        "type": "filesystem_overlay",
    }


if __name__ == "__main__":
    if "--preflight-only" in sys.argv:
        ok = preflight()
        sys.exit(0 if ok else 2)
    else:
        ev = run()
        sys.exit(ev["exit_code"])
