#!/usr/bin/env python3
"""F4 Suites Harness v1.0.0-r5 — run 4 F4 suites, produce certified evidence.

Usage:
    python tools/run_f4_suites.py

Exit codes:
    0 — PHASE_4_GATE_SATISFIED
    1 — REQUIRES_REMEDIATION
    2 — REJECTED
"""
import subprocess, sys, json, datetime, hashlib, time, os, re
from pathlib import Path

HARNESS_VERSION = "1.0.0-r5"
ROOT = Path(__file__).resolve().parent.parent
JUNIT_XML = ROOT / "evidence" / "f4_suites" / "junit.xml"

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

DB_PATHS = {
    "OFFICIAL_DB": ROOT / "data" / "db" / "meli_financial_v4.db",
    "V7": ROOT / "data" / "db" / "baseline_estable_v7_20260715" / "meli_financial_v4.db",
    "V8": ROOT / "data" / "db" / "baseline_estable_v8_candidate_20260717" / "meli_financial_v4.db",
}
TEMP_V8 = ROOT / "data" / "db" / "tmp_f4_v8"
EVIDENCE_DIR = ROOT / "evidence" / "f4_suites"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def get_hashes():
    h = {}
    for name, path in DB_PATHS.items():
        if path.exists():
            h[name] = {"sha256": sha256(path), "size": path.stat().st_size, "path": str(path)}
        else:
            h[name] = {"sha256": "NOT_FOUND", "size": 0, "path": str(path)}
    return h


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
    nodeids = list(dict.fromkeys(nodeids))  # deduplicate preserving order
    return nodeids


def run():
    execution_id = datetime.datetime.now().strftime("F4_%Y%m%d_%H%M%S")
    timestamp = datetime.datetime.now().isoformat()

    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT
    ).stdout.strip()

    # Pre-run state
    pre_hashes = get_hashes()
    pre_temp_v8_exists = TEMP_V8.exists()
    nodeids = collect_nodeids()

    # Build command
    test_paths = [str(ROOT / f) for f in TEST_FILES]
    cmd_list = [sys.executable, "-m", "pytest"] + test_paths + [
        "-v", "--tb=short",
        f"--junitxml={JUNIT_XML}",
    ]
    command_str = " ".join(cmd_list)

    # Execute
    start_ts = datetime.datetime.now().isoformat()
    start_time = time.time()
    proc = subprocess.run(cmd_list, capture_output=True, text=True, cwd=ROOT, timeout=900)
    end_time = time.time()
    end_ts = datetime.datetime.now().isoformat()
    elapsed_s = round(end_time - start_time, 2)

    # Post-run state
    post_hashes = get_hashes()
    post_temp_v8_exists = TEMP_V8.exists()

    stdout = proc.stdout
    stderr = proc.stderr
    returncode = proc.returncode

    # Parse summary line
    summary_line = ""
    for line in stdout.splitlines():
        ls = line.strip()
        if "passed" in ls and "failed" in ls and ls.startswith("=="):
            summary_line = ls.strip("=").strip()
            break
        if "passed" in ls and "warning" in ls and "in " in ls:
            summary_line = ls
            break

    # Parse outcomes from pytest output lines (not summary)
    outcomes = {"PASS": 0, "FAIL": 0, "SKIP": 0, "XFAIL": 0, "ERROR": 0}
    for line in stdout.splitlines():
        ls = line.strip()
        if "::" not in ls:
            if ls.startswith("ERROR") or ls.startswith("ERRORS"):
                outcomes["ERROR"] += 1
            continue
        rest = ls.split("::", 1)[1] if "::" in ls else ls
        if " PASSED " in rest or rest.endswith("PASSED"):
            outcomes["PASS"] += 1
        elif " FAILED " in rest or rest.endswith("FAILED"):
            outcomes["FAIL"] += 1
        elif " SKIP" in rest or "SKIPPED" in rest:
            outcomes["SKIP"] += 1
        elif " XFAIL" in rest:
            outcomes["XFAIL"] += 1
        elif " ERROR" in rest or rest.endswith("ERROR"):
            outcomes["ERROR"] += 1

    # Mutation check
    mutation = False
    mutation_detail = {}
    for name in pre_hashes:
        if pre_hashes[name]["sha256"] != post_hashes[name]["sha256"]:
            mutation = True
            mutation_detail[name] = {
                "pre": pre_hashes[name]["sha256"],
                "post": post_hashes[name]["sha256"],
            }

    # Temp cleanup check
    temp_cleaned = not post_temp_v8_exists

    # Report complete
    report_complete = bool(summary_line)

    # ── Automatic classification ──
    collected = len(nodeids)
    all_pass = (outcomes["PASS"] == collected
                and outcomes["FAIL"] == 0
                and outcomes["SKIP"] == 0
                and outcomes["XFAIL"] == 0
                and outcomes["ERROR"] == 0
                and collected == EXPECTED_TOTAL)
    no_mutation = not mutation
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
        "commit": commit,
        "harness_version": HARNESS_VERSION,
        "repository": "Marketplace Financial AI Engine",
        "command": command_str,
        "timeout_seconds": 600,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "elapsed_seconds": elapsed_s,
        "returncode": returncode,
        "summary_line": summary_line,
        "nodeids_collected": collected,
        "expected_total": EXPECTED_TOTAL,
        "expected_per_file": EXPECTED_PER_FILE,
        "outcomes": outcomes,
        "nodeids": nodeids,
        "pre_run_hashes": pre_hashes,
        "post_run_hashes": post_hashes,
        "mutation_detected": mutation,
        "mutation_detail": mutation_detail if mutation else None,
        "temp_v8_cleaned": temp_cleaned,
        "report_complete": report_complete,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
    }

    # Write evidence
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    ev_path = EVIDENCE_DIR / f"{execution_id}.json"
    ev_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")

    # Print report
    print(f"\n{'='*60}")
    print(f"  HARNESS:      {HARNESS_VERSION}")
    print(f"  EXECUTION ID: {execution_id}")
    print(f"  COMMIT:       {commit}")
    print(f"  DURATION:     {elapsed_s}s")
    print(f"  RETURNCODE:   {returncode}")
    print(f"  COLLECTED:    {collected}")
    print(f"  OUTCOMES:     {json.dumps(outcomes)}")
    print(f"  SUMMARY:      {summary_line}")
    print(f"  MUTATION:     {mutation}")
    print(f"  TEMP CLEANED: {temp_cleaned}")
    print(f"  VERDICT:      {verdict}")
    print(f"  REASON:       {verdict_reason}")
    print(f"  JUNIT:        {JUNIT_XML}")
    print(f"  EVIDENCE:     {ev_path}")
    print(f"{'='*60}\n")

    # Print per-file counts
    for f in TEST_FILES:
        f_nodeids = [n for n in nodeids if n.startswith(f.replace("/", ".").replace(".py", ""))]
        print(f"  {f}: {len(f_nodeids)} tests")

    if outcomes["PASS"] > 0:
        print(f"\n  PASSED ({outcomes['PASS']}):")
        for line in stdout.splitlines():
            ls = line.strip()
            if "::" in ls and ls.endswith("PASSED"):
                print(f"    {ls}")

    if outcomes.get("FAIL", 0) > 0:
        print(f"\n  FAILED ({outcomes['FAIL']}):")
        for line in stdout.splitlines():
            ls = line.strip()
            if ls.endswith("FAILED"):
                print(f"    {ls}")

    if outcomes.get("ERROR", 0) > 0 and stderr.strip():
        print(f"\n  STDERR:")
        print(stderr[:3000])

    return evidence


if __name__ == "__main__":
    ev = run()
    sys.exit(ev["exit_code"])
