"""Tests for Phase P34.2 — KnowledgeConsolidationEngine (KCE)."""
from __future__ import annotations
import pytest
import json
import yaml
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def kce():
    from engine.v4.database import DatabaseV4
    from engine.v4.knowledge.kce import KnowledgeConsolidationEngine, KCEConfig
    db = DatabaseV4.get()
    cfg = KCEConfig(
        governance_dir=str(ROOT / "governance"),
        knowledge_index_path=str(ROOT / "knowledge_index.yaml"),
        taxonomy_dir=str(ROOT / "KnowledgeBase" / "Marketplace" / "Taxonomy"),
        dry_run=True,
    )
    return KnowledgeConsolidationEngine(db=db, config=cfg)


# ── PACKAGE EXISTS ─────────────────────────────────────────────────

def test_knowledge_package_exists():
    from engine.v4.knowledge import kce, audit_scanner, decision_parser, knowledge_indexer, retention_manager
    assert kce.KnowledgeConsolidationEngine is not None
    assert audit_scanner.AuditScanner is not None
    assert decision_parser.DecisionParser is not None
    assert knowledge_indexer.KnowledgeIndexer is not None
    assert retention_manager.RetentionManager is not None


# ── KCE ENGINE ─────────────────────────────────────────────────────

def test_kce_consolidate_returns_result(kce):
    result = kce.consolidate()
    assert result is not None
    assert hasattr(result, "audit_entries")
    assert hasattr(result, "decision_entries")
    assert hasattr(result, "taxonomy_entries")


def test_kce_decision_entries_have_required_fields(kce):
    result = kce.consolidate()
    for entry in result.decision_entries:
        assert "id" in entry
        assert "type" in entry
        assert "status" in entry
        assert entry["type"] in ("governance", "audit", "taxonomy", "certification", "decision")


def test_kce_scans_governance_files(kce):
    result = kce.consolidate()
    assert result.files_scanned > 10


def test_kce_taxonomy_entries_detected(kce):
    result = kce.consolidate()
    assert len(result.taxonomy_entries) >= 4


def test_kce_coverage_gaps_analyzed(kce):
    result = kce.consolidate()
    assert hasattr(result, "coverage_gaps")
    for gap in result.coverage_gaps:
        assert "knowledge_id" in gap
        assert "reason" in gap


def test_kce_status_report(kce):
    report = kce.status_report()
    assert "total_entries" in report
    assert report["total_entries"] >= 10
    assert "by_type" in report
    assert "by_status" in report
    assert "governance" in report["by_type"]
    assert "ACTIVE" in report["by_status"]


# ── AUDIT SCANNER ──────────────────────────────────────────────────

def test_audit_scanner_coverage():
    from engine.v4.database import DatabaseV4
    from engine.v4.knowledge.audit_scanner import AuditScanner
    db = DatabaseV4.get()
    scanner = AuditScanner(db)
    entries = scanner.scan()
    assert isinstance(entries, list)
    coverage = scanner.coverage_summary()
    assert isinstance(coverage, dict)
    if len(entries) > 0:
        e = entries[0]
        assert e.knowledge_id
        assert e.knowledge_type == "audit"
        assert e.marketplace


# ── DECISION PARSER ────────────────────────────────────────────────

def test_decision_parser_parses_governance():
    from engine.v4.knowledge.decision_parser import DecisionParser
    parser = DecisionParser(ROOT / "governance")
    decisions = parser.scan_all()
    assert len(decisions) > 10
    ids = [d.knowledge_id for d in decisions]
    dec_ids = [i for i in ids if i.startswith("DEC-")]
    assert len(dec_ids) >= 5


def test_decision_parser_parses_single_file():
    from engine.v4.knowledge.decision_parser import DecisionParser
    parser = DecisionParser(ROOT / "governance")
    gov_dir = ROOT / "governance"
    files = list(gov_dir.glob("*.md"))
    if files:
        f = files[0]
        parsed = parser.parse_file(f)
        assert len(parsed) >= 1
        assert parsed[0].knowledge_id
        assert parsed[0].title


# ── KNOWLEDGE INDEXER ─────────────────────────────────────────────

def test_knowledge_indexer_reads_yaml():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    indexer = KnowledgeIndexer()
    entries = indexer.read()
    assert len(entries) >= 10


def test_knowledge_indexer_search():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    indexer = KnowledgeIndexer()
    results = indexer.search("Financial")
    assert len(results) >= 1
    results_by_type = indexer.search("", type_filter="governance")
    assert len(results_by_type) >= 5
    results_active = indexer.search("", status_filter="ACTIVE")
    assert len(results_active) >= 3


def test_knowledge_indexer_get():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    indexer = KnowledgeIndexer()
    entry = indexer.get("DEC-001")
    assert entry is not None
    assert entry["id"] == "DEC-001"
    assert entry["type"] == "governance"

    missing = indexer.get("NONEXISTENT-999")
    assert missing is None


# ── RETENTION MANAGER ──────────────────────────────────────────────

def test_retention_manager_transitions():
    from engine.v4.knowledge.retention_manager import RetentionManager
    rm = RetentionManager()
    assert rm.allowed_transition("ACTIVE", "OBSOLETE") is True
    assert rm.allowed_transition("ACTIVE", "SUPERSEDED") is True
    assert rm.allowed_transition("ACTIVE", "DELETED") is False
    assert rm.allowed_transition("OBSOLETE", "ARCHIVED") is True
    assert rm.allowed_transition("ARCHIVED", "ACTIVE") is False


def test_retention_manager_suggest_action():
    from engine.v4.knowledge.retention_manager import RetentionManager
    rm = RetentionManager()
    coverage = {"DEC-001", "DEC-002"}

    active_in_coverage = {"id": "DEC-001", "status": "ACTIVE", "type": "governance"}
    assert rm.suggest_action(active_in_coverage, coverage) == "KEEP"

    absorbed = {"id": "DEC-020", "status": "SUPERSEDED", "type": "governance"}
    assert rm.suggest_action(absorbed, coverage) == "ARCHIVE"

    pending = {"id": "RFC-UNKNOWN", "status": "PENDING", "type": "governance"}
    assert rm.suggest_action(pending, coverage) == "MONITOR"


# ── KNOWLEDGE API ──────────────────────────────────────────────────

def test_knowledge_api_list():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "knowledge" in data
    assert data["total"] >= 10


def test_knowledge_api_get():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge/DEC-001")
    if resp.status_code == 200:
        data = resp.json()
        assert data["id"] == "DEC-001"


def test_knowledge_api_get_missing():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge/NONEXISTENT-999")
    assert resp.status_code == 404


def test_knowledge_api_status():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_entries" in data
    assert "by_type" in data
    assert "by_status" in data


def test_knowledge_api_consolidate():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.post("/api/v4/knowledge/consolidate?dry_run=true")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "dry_run"
    assert data["decision_entries"] > 0
    assert data["files_scanned"] > 10


def test_knowledge_api_coverage_gaps():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge/coverage-gaps")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_gaps" in data
    assert "gaps" in data


def test_knowledge_api_search():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge?search=Financial&status=ACTIVE")
    assert resp.status_code == 200
    data = resp.json()
    assert "knowledge" in data


def test_knowledge_api_filter_by_type():
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient
    client = TestClient(knowledge_app)
    resp = client.get("/api/v4/knowledge?type=taxonomy")
    assert resp.status_code == 200
    data = resp.json()
    for entry in data["knowledge"]:
        assert entry["type"] == "taxonomy"


def test_knowledge_api_export(monkeypatch, tmp_path):
    from api.knowledge_api import knowledge_app
    from fastapi.testclient import TestClient

    calls = {}

    class FakeAdapter:
        def __init__(self, vault_path: str):
            calls["vault_path"] = vault_path

        def export_evidence(self, payload):
            calls["payload"] = payload

    monkeypatch.setattr("api.knowledge_api.ObsidianAdapter", FakeAdapter)
    client = TestClient(knowledge_app)
    payload = {
        "evidence_object": {"evidence_hash": "hash-123"},
        "marketplace": "ML",
    }

    resp = client.post(f"/api/v4/knowledge/export?vault_path={tmp_path.as_posix()}", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["evidence_hash"] == "hash-123"
    assert calls["payload"] == payload
    assert calls["vault_path"] == tmp_path.as_posix()
