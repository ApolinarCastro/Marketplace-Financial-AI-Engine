"""Generate Execution Board — Sprint 0 CAP-based operational tracking.

Reads code, DB, evidence vault, git, and harness state to produce
execution_board.json and execution_board.md.

Usage:
    python tools/generate_execution_board.py
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / "evidence" / "fase_1b"
HARNESS_PATH = ROOT / "tools" / "validate_fase_1b.py"
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"


# ── Git ────────────────────────────────────────────────────────────────


def _get_git_info() -> dict:
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        ).stdout.strip()
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        ).stdout.strip()[:12]
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        ).stdout.strip()
        return {
            "branch": branch or "unknown",
            "commit": commit or "unknown",
            "dirty": bool(status),
        }
    except Exception:
        return {"branch": "unknown", "commit": "unknown", "dirty": False}


# ── Harness ────────────────────────────────────────────────────────────


def _get_harness_info() -> dict:
    if not HARNESS_PATH.exists():
        return {"path": "tools/validate_fase_1b.py", "version": None, "exists": False}
    text = HARNESS_PATH.read_text(encoding="utf-8")
    m = re.search(r'HARNESS_VERSION\s*=\s*"([^"]+)"', text)
    return {
        "path": "tools/validate_fase_1b.py",
        "version": m.group(1) if m else None,
        "exists": True,
    }


# ── Database ───────────────────────────────────────────────────────────


def _get_db_info() -> dict:
    result = {
        "path": "data/db/meli_financial_v4.db",
        "exists": DB_PATH.exists(),
        "tables": {},
    }
    if not result["exists"]:
        return result
    try:
        import duckdb
        con = duckdb.connect(str(DB_PATH), read_only=True)
        for tbl in ["file_registry", "ingestion_registry"]:
            try:
                row = con.execute(
                    f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{tbl}'"
                ).fetchone()
                exists = row and row[0] > 0
                if exists:
                    cnt = con.execute(f"SELECT COUNT(*) FROM \"{tbl}\"").fetchone()[0]
                    result["tables"][tbl] = {"exists": True, "count": cnt}
                else:
                    result["tables"][tbl] = {"exists": False}
            except Exception:
                result["tables"][tbl] = {"exists": False}
        con.close()
    except ImportError:
        result["error"] = "duckdb not available"
    except Exception as e:
        result["error"] = str(e)
    return result


# ── Evidence Vault ─────────────────────────────────────────────────────


def _get_evidence_info() -> dict:
    info = {
        "latest_summary": None,
        "summaries_found": [],
        "latest_execution_id": None,
        "latest_result": None,
        "all_execution_ids": [],
    }
    if not EVIDENCE_DIR.exists():
        return info
    summaries = sorted(EVIDENCE_DIR.glob("*summary*.json"))
    info["summaries_found"] = [s.name for s in summaries]
    info["latest_summary"] = summaries[-1].name if summaries else None
    if summaries:
        try:
            data = json.loads(summaries[-1].read_text(encoding="utf-8"))
            info["latest_execution_id"] = data.get("execution", {}).get("execution_id")
            info["latest_result"] = data.get("summary", {}).get("verification_status")
            for s in summaries:
                try:
                    d = json.loads(s.read_text(encoding="utf-8"))
                    eid = d.get("execution", {}).get("execution_id")
                    if eid:
                        info["all_execution_ids"].append(eid)
                except Exception:
                    pass
        except Exception:
            pass
    return info


# ── Code inspection helpers ────────────────────────────────────────────


def _path_exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def _file_contains(rel: str, pattern: str) -> bool:
    p = ROOT / rel
    if not p.exists() or not p.is_file():
        return False
    try:
        return bool(re.search(pattern, p.read_text(encoding="utf-8", errors="ignore")))
    except Exception:
        return False


def _class_exists(base_rel: str, class_name: str) -> bool:
    p = ROOT / base_rel
    if p.is_dir():
        for f in sorted(p.rglob("*.py")):
            if _file_contains(str(f.relative_to(ROOT)), rf"class\s+{class_name}\b"):
                return True
        return False
    return _file_contains(base_rel, rf"class\s+{class_name}\b")


# ── CAP definitions ────────────────────────────────────────────────────


def _build_capabilities(git_commit: str, db_info: dict, evidence_info: dict) -> list[dict]:
    caps = []

    # ── CAP-001 Upload Center E2E ─────────────────────────────────────
    c1 = {
        "cap_id": "CAP-001",
        "name": "Upload Center E2E",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": "PASS",
        "blocking_issue": "Tests contaminate official DB and data/uploads/; not isolated",
        "next_gate": "Isolated tests with temp DB, temp uploads, cleanup",
        "evidence_refs": [],
        "missing_evidence": [
            "isolated_tests_temp_db",
            "isolated_tests_temp_uploads",
            "cleanup_after_tests",
            "browser_upload_e2e",
            "execution_id_from_upload_response",
            "file_created_in_data_uploads",
            "ingestion_registry_row_created",
        ],
    }
    refs = []
    if _path_exists("templates/upload_center.html"):
        refs.append("templates/upload_center.html")
    if _file_contains("api/api.py", r'@app\.get\("/upload"'):
        refs.append("api/api.py: GET /upload")
    if _file_contains("api/api.py", r'@app\.post\("/api/v4/ingestion/upload"'):
        refs.append("api/api.py: POST /api/v4/ingestion/upload")
    if _path_exists("tests/test_upload_center_e2e.py"):
        refs.append("tests/test_upload_center_e2e.py")
    if refs:
        c1["evidence_refs"] = refs
    caps.append(c1)

    # ── CAP-002 Ingestion Registry ────────────────────────────────────
    c2 = {
        "cap_id": "CAP-002",
        "name": "Ingestion Registry",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "IMPLEMENTED",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": None,
        "next_gate": "ingestion_registry_schema_and_3_runs",
        "evidence_refs": [],
        "missing_evidence": [
            "3 controlled uploads",
            "execution_id",
            "start_time",
            "end_time",
            "sha256",
            "status",
            "marketplace",
            "document_type",
            "errors",
            "warnings",
        ],
    }
    refs = []
    if _class_exists("engine/v4/ingestion", "IngestionRegistry"):
        refs.append("IngestionRegistry class")
    if _file_contains("api/api.py", r"ingestion/registry"):
        refs.append("api/api.py: GET /api/v4/ingestion/registry")
    db_reg = db_info.get("tables", {}).get("ingestion_registry", {})
    if db_reg.get("exists"):
        refs.append(f"ingestion_registry (db): {db_reg.get('count', 0)} rows")
        if db_reg.get("count", 0) > 0:
            c2["evidence_status"] = "VALIDATED"
            c2["last_result"] = "VALIDATED"
    if refs:
        c2["evidence_refs"] = refs
    else:
        c2["evidence_status"] = "NOT_STARTED"
        c2["operational_status"] = "NOT_STARTED"
    caps.append(c2)

    # ── CAP-003 File Registry ─────────────────────────────────────────
    c3 = {
        "cap_id": "CAP-003",
        "name": "File Registry",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": None,
        "next_gate": "file_registry_upload_coverage",
        "evidence_refs": [],
        "missing_evidence": [
            "sha256_match",
            "file_name",
            "source",
            "rows_processed",
            "processed_at",
            "duplicate_upload_traceability",
        ],
    }
    refs = []
    if _class_exists("engine/v4/ingestion/handlers", "PersistenceEngine"):
        refs.append("PersistenceEngine class")
    if _file_contains("engine/v4/database.py", r"def register_file"):
        refs.append("engine/v4/database.py: register_file")
    if _file_contains("engine/v4/surgical_loader.py", r"def _register_file"):
        refs.append("engine/v4/surgical_loader.py: _register_file")
    db_fr = db_info.get("tables", {}).get("file_registry", {})
    if db_fr.get("exists"):
        refs.append(f"file_registry (db): {db_fr.get('count', 0)} rows")
    if refs:
        c3["evidence_refs"] = refs
    else:
        c3["evidence_status"] = "NOT_STARTED"
        c3["operational_status"] = "NOT_STARTED"
    caps.append(c3)

    # ── CAP-004 Certification Trigger ─────────────────────────────────
    c4 = {
        "cap_id": "CAP-004",
        "name": "Certification Trigger",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": None,
        "next_gate": "post_ingestion_certification_payload",
        "evidence_refs": [],
        "missing_evidence": [
            "certification_triggered",
            "certification_result",
            "reconciliation",
            "certification",
            "coverage",
            "gaps",
            "errors",
            "overall_status",
            "summary_persisted",
        ],
    }
    refs = []
    if _class_exists("engine/v4/ingestion/handlers", "CertificationTrigger"):
        refs.append("CertificationTrigger class")
    if _file_contains("engine/v4/ingestion/orchestrator.py", r"certification"):
        refs.append("orchestrator.py: certification wiring")
    if refs:
        c4["evidence_refs"] = refs
    else:
        c4["evidence_status"] = "NOT_STARTED"
        c4["operational_status"] = "NOT_STARTED"
    caps.append(c4)

    # ── CAP-005 Knowledge Trigger ─────────────────────────────────────
    c5 = {
        "cap_id": "CAP-005",
        "name": "Knowledge Trigger",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": "KnowledgeTrigger puede quedar SKIPPED si no recibe indexer",
        "next_gate": "knowledge_index_not_skipped",
        "evidence_refs": [],
        "missing_evidence": [
            "indexer_injected",
            "knowledge_index_executed_true",
            "knowledge_index_not_skipped",
        ],
    }
    refs = []
    has_default_wiring = False
    if _class_exists("engine/v4/ingestion/handlers", "KnowledgeTrigger"):
        refs.append("KnowledgeTrigger class")
    if _class_exists("engine/v4/knowledge", "KnowledgeIndexer") or _file_contains(
        "engine/v4/knowledge/knowledge_indexer.py", r"def build_knowledge_index"
    ):
        refs.append("build_knowledge_index (knowledge_indexer.py)")
    if _file_contains("engine/v4/ingestion/orchestrator.py", r"KnowledgeIndexer\(") and _file_contains(
        "engine/v4/ingestion/orchestrator.py", r"PatternRegistry\("):
        has_default_wiring = True
        refs.append("orchestrator.py: default KnowledgeIndexer + PatternRegistry wiring")
    for sn in evidence_info.get("summaries_found", []):
        refs.append(f"evidence/{sn}")
    if has_default_wiring and evidence_info.get("latest_result"):
        c5["last_result"] = evidence_info.get("latest_result")
    if not has_default_wiring:
        c5["blocking_issue"] = "KnowledgeTrigger sin wiring por defecto verificable en orchestrator"
        c5["next_gate"] = "inject_default_indexer_and_registry"
    if refs:
        c5["evidence_refs"] = refs
    else:
        c5["evidence_status"] = "NOT_STARTED"
    caps.append(c5)

    # ── CAP-006 Obsidian Sync ─────────────────────────────────────────
    c6 = {
        "cap_id": "CAP-006",
        "name": "Obsidian Sync",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": "knowledge_api.py no montada en api.py; dashboard.html contiene stub de Obsidian",
        "next_gate": "obsidian_export_real_file",
        "evidence_refs": [],
        "missing_evidence": [
            "knowledge_api_mounted",
            "frontend_connected_to_backend",
            "obsidian_export_real_file",
        ],
    }
    refs = []
    if _class_exists("engine/v4/certification/knowledge", "ObsidianAdapter"):
        refs.append("ObsidianAdapter class")
    if _path_exists("api/knowledge_api.py"):
        refs.append("api/knowledge_api.py")
        knowledge_refs = []
        if _file_contains("api/knowledge_api.py", r"knowledge/export"):
            knowledge_refs.append("/api/v4/knowledge/export endpoint")
        if _file_contains("api/knowledge_api.py", r"knowledge/consolidate"):
            knowledge_refs.append("/api/v4/knowledge/consolidate endpoint")
        if _file_contains("api/knowledge_api.py", r"knowledge/status"):
            knowledge_refs.append("/api/v4/knowledge/status endpoint")
        if knowledge_refs:
            refs.append(f"endpoints: {', '.join(knowledge_refs)}")
    if _file_contains("templates/dashboard.html", r"(?i)obsidian"):
        refs.append("dashboard.html: Obsidian stub")
    if refs:
        c6["evidence_refs"] = refs
    else:
        c6["evidence_status"] = "NOT_STARTED"
    caps.append(c6)

    # ── CAP-007 Copilot Evidence ──────────────────────────────────────
    c7 = {
        "cap_id": "CAP-007",
        "name": "Copilot Evidence",
        "operational_status": "IMPLEMENTED",
        "evidence_status": "PARTIAL",
        "last_execution_id": None,
        "last_commit": git_commit,
        "last_result": None,
        "blocking_issue": None,
        "next_gate": "copilot_answer_after_upload_with_evidence",
        "evidence_refs": [],
        "missing_evidence": [
            "post_upload_copilot_question",
            "sql_or_api_source",
            "marketplace",
            "period",
            "amount",
            "traceability",
            "execution_id_relation",
        ],
    }
    refs = []
    if _class_exists("engine/v4/copilot", "CopilotEngine"):
        refs.append("CopilotEngine class")
    copilot_dir = ROOT / "engine" / "v4" / "copilot"
    if copilot_dir.is_dir():
        py_files = [f for f in copilot_dir.iterdir() if f.suffix == ".py" and f.name != "__init__.py"]
        if py_files:
            refs.append(f"handlers: {len(py_files)} files in engine/v4/copilot/")
    if refs:
        c7["evidence_refs"] = refs
    else:
        c7["evidence_status"] = "NOT_STARTED"
        c7["operational_status"] = "NOT_STARTED"
    caps.append(c7)

    return caps


# ── Board building ─────────────────────────────────────────────────────


# Canonical state models per Plan Maestro §6
CANONICAL_OPERATIONAL = ["IMPLEMENTED", "VALIDATED", "VERIFIED", "CERTIFIED", "NOT_STARTED"]
CANONICAL_EVIDENCE = ["VALIDATED", "IMPLEMENTED", "PARTIAL", "NOT_STARTED"]

def _canonical_operational(status: str) -> str:
    """Map legacy/non-canonical operational status to canonical."""
    mapping = {
        "DONE": "IMPLEMENTED",
        "VERIFY": "VALIDATED",
        "DOING": "IMPLEMENTED",
        "BLOCKED": "IMPLEMENTED",  # blocked capabilities are implemented but blocked
        "READY": "IMPLEMENTED",
        "BACKLOG": "NOT_STARTED",
    }
    return mapping.get(status, status if status in CANONICAL_OPERATIONAL else "IMPLEMENTED")

def _canonical_evidence(status: str) -> str:
    """Map legacy/non-canonical evidence status to canonical."""
    mapping = {
        "DONE": "IMPLEMENTED",
        "VERIFY": "VALIDATED",
        "DOING": "IMPLEMENTED",
        "BLOCKED": "PARTIAL",
        "READY": "PARTIAL",
        "BACKLOG": "NOT_STARTED",
    }
    return mapping.get(status, status if status in CANONICAL_EVIDENCE else "PARTIAL")


def _build_summary(capabilities: list[dict], evidence_info: dict) -> dict:
    by_operational_status: dict[str, int] = {}
    by_evidence_status: dict[str, int] = {}
    for cap in capabilities:
        op = _canonical_operational(cap["operational_status"])
        ev = _canonical_evidence(cap["evidence_status"])
        by_operational_status[op] = by_operational_status.get(op, 0) + 1
        by_evidence_status[ev] = by_evidence_status.get(ev, 0) + 1
    return {
        "total_capabilities": len(capabilities),
        "by_operational_status": by_operational_status,
        "by_evidence_status": by_evidence_status,
        "latest_evidence_result": evidence_info.get("latest_result"),
        "latest_execution_id": evidence_info.get("latest_execution_id"),
    }


def build_board() -> dict:
    git_info = _get_git_info()
    harness_info = _get_harness_info()
    db_info = _get_db_info()
    evidence_info = _get_evidence_info()
    capabilities = _build_capabilities(git_info["commit"], db_info, evidence_info)
    summary = _build_summary(capabilities, evidence_info)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "Marketplace Financial Operating System",
        "git": git_info,
        "harness": harness_info,
        "database": db_info,
        "evidence": evidence_info,
        "summary": summary,
        "capabilities": capabilities,
    }


def generate_markdown(board: dict) -> str:
    lines = [
        "# Execution Board",
        "",
        f"**Generated at:** {board['generated_at']}",
        f"**Commit:** {board['git']['commit']}",
        f"**Branch:** {board['git']['branch']}",
        f"**Harness:** {board['harness'].get('version', 'N/A')}",
        f"**Capability Summary:** {board['summary']['by_operational_status']}",
        "",
        "| CAP | Name | Operational | Evidence | Last Result | Blocking Issue | Next Gate |",
        "|---|---|---|---|---|---|---|",
    ]
    for cap in board["capabilities"]:
        lr = cap.get("last_result") or "-"
        bi = cap.get("blocking_issue") or "-"
        lines.append(
            f"| {cap['cap_id']} | {cap['name']} | {cap['operational_status']} | "
            f"{cap['evidence_status']} | {lr} | {bi} | {cap['next_gate']} |"
        )
    lines.append("")
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────


def main():
    print("Generating Execution Board...")
    board = build_board()

    json_path = ROOT / "execution_board.json"
    json_path.write_text(
        json.dumps(board, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"  {json_path} written.")

    md_path = ROOT / "execution_board.md"
    md_content = generate_markdown(board)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"  {md_path} written.")

    caps = board["capabilities"]
    counts = {}
    for c in caps:
        s = c["operational_status"]
        counts[s] = counts.get(s, 0) + 1

    print(f"\nExecution Board generated successfully.\n")
    print(f"Capabilities detected: {len(caps)}")
    for s in ["BLOCKED", "READY", "DOING", "VERIFY", "CERTIFIED", "BACKLOG"]:
        if counts.get(s):
            print(f"  {s}: {counts[s]}")
    print(f"\nOutput:")
    print(f"  {json_path.name}")
    print(f"  {md_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
