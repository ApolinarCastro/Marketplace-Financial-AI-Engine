"""
bootstrap_runtime.py — Bootstrap required artifacts from main repo to worktree.

Reads runtime_manifest.json from the main repository, copies missing required
artifacts (DBs, templates, taxonomies, fixtures, config) into the current
worktree, preserving SHA256 hashes. Completely idempotent.

Usage:
    python tools/bootstrap_runtime.py

Environment:
    CANONICAL_REPO  — override main repo detection (optional, auto-detected via git)
    CALLER_WORKTREE — override worktree detection (optional, auto-detected via git)

Exit codes:
    0 = all required artifacts available
    1 = some artifacts could not be bootstrapped
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────
#  PATH DETECTION (auto or env override)
# ─────────────────────────────────────────────────────────────────────

if "CALLER_WORKTREE" in os.environ:
    WT_ROOT = Path(os.environ["CALLER_WORKTREE"]).resolve()
else:
    WT_ROOT = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True
        ).stdout.strip()
    )

if "CANONICAL_REPO" in os.environ:
    MAIN_ROOT = Path(os.environ["CANONICAL_REPO"]).resolve()
else:
    _common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True, text=True
    ).stdout.strip()
    MAIN_ROOT = Path(_common).parent.resolve()

MANIFEST_PATH = (
    MAIN_ROOT / "governance" / "coordination" / "runtime_manifest.json"
)


# ─────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _copy_file(src: Path, dst: Path) -> tuple:
    _ensure_dir(dst)
    if dst.exists():
        old_hash = _sha256(dst)
        if old_hash == _sha256(src):
            return ("SKIP", "hash match")
        return ("SKIP", f"exists with different hash ({old_hash[:12]}) — won't overwrite")
    shutil.copy2(src, dst)
    new_hash = _sha256(dst)
    return ("COPIED", f"{_sha256(src)[:12]}")


# ─────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  BOOTSTRAP RUNTIME — Required Artifact Materializer")
    print("=" * 70)
    print()
    print(f"  Worktree: {WT_ROOT}")
    print(f"  Main repo: {MAIN_ROOT}")
    print(f"  Manifest: {MANIFEST_PATH}")
    print()

    if not MANIFEST_PATH.exists():
        print(f"  FAIL: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    all_artifacts = (
        manifest.get("runtime", {}).get("artifacts", [])
        + manifest.get("test", {}).get("artifacts", [])
    )

    ops = {"COPIED": 0, "SKIP": 0, "FAIL": 0}
    details = []

    for art in all_artifacts:
        rel = art["path"]
        expected_sha = art.get("sha256")

        src = MAIN_ROOT / rel
        dst = WT_ROOT / rel

        if not src.exists():
            details.append((rel, "FAIL", f"source missing in main repo"))
            ops["FAIL"] += 1
            continue

        action, note = _copy_file(src, dst)

        if action == "COPIED":
            verify = _sha256(dst)
            if expected_sha and verify != expected_sha:
                details.append((rel, "FAIL",
                    f"copied but hash mismatch: expected {expected_sha[:12]} got {verify[:12]}"))
                ops["FAIL"] += 1
            else:
                details.append((rel, "COPIED",
                    f"{os.path.getsize(dst):,} bytes  {verify[:12]}"))
                ops["COPIED"] += 1
        elif action == "SKIP":
            details.append((rel, "SKIP", note))
            ops["SKIP"] += 1
        else:
            details.append((rel, "ERROR", note))
            ops["ERROR"] = ops.get("ERROR", 0) + 1

    # Also copy contract documents (not in runtime/test manifest but required)
    contract_files = [
        ("governance/coordination/CERTIFICATION_CONTRACT.md", None),
        ("governance/coordination/runtime_manifest.json", None),
    ]
    for crel, _ in contract_files:
        cs = MAIN_ROOT / crel
        cd = WT_ROOT / crel
        if cs.exists() and not cd.exists():
            _ensure_dir(cd)
            shutil.copy2(cs, cd)
            details.append((crel, "COPIED",
                f"{os.path.getsize(cd):,} bytes  {_sha256(cd)[:12]}"))
            ops["COPIED"] += 1
        elif cd.exists():
            details.append((crel, "SKIP", "already exists"))

    # Report
    print(f"{'Artifact':50s} {'Action':8s} Details")
    print("-" * 90)
    for rel, action, note in sorted(details, key=lambda x: x[1]):
        a_pad = "OK" if action == "COPIED" else action
        print(f"  {rel:48s} {a_pad:8s} {note}")

    print()
    print(f"  COPIED: {ops['COPIED']}  SKIP: {ops['SKIP']}  FAIL: {ops['FAIL']}")
    print()

    if ops["FAIL"] > 0:
        print("  VERDICT: BOOTSTRAP_INCOMPLETE")
        sys.exit(1)
    else:
        print("  VERDICT: BOOTSTRAP_COMPLETE")
        print()
        print("  Run tools/verify_runtime_contract.py to validate.")
        sys.exit(0)


if __name__ == "__main__":
    main()
