"""Tests for C3: Orchestrator finalize wiring.

Validates that IngestionOrchestrator.run() correctly:
- Reads cert_result["overall_status"] from context["CERTIFY"]["cert_result"]
- Reads knowledge_result["overall_status"] from context["KNOWLEDGE"]["knowledge_result"]
- Sets certification_triggered=True only when CERTIFY stage passes and cert has overall_status
- Sets knowledge_updated=True only when KNOWLEDGE stage passes and knowledge has overall_status=="PASS"
- Falls back correctly when stages are skipped or fail
"""
from __future__ import annotations
from pathlib import Path
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_db():
    db = MagicMock()
    import pandas as pd
    db.query.return_value = pd.DataFrame()
    db.file_registered.return_value = False
    db.register_file = MagicMock()
    return db


def _make_csv(tmp_path: Path) -> Path:
    p = tmp_path / "test.csv"
    p.write_text("col1,col2\n1,2\n", encoding="utf-8")
    return p


def _mock_persistence():
    pe = MagicMock()
    pe.persist.return_value = {"records_inserted": 10, "errors": []}
    return pe


@pytest.mark.anyio
async def test_orchestrator_finalize_cert_passes(mock_db, tmp_path):
    """CERTIFY passes with overall_status -> certification_triggered=True."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {
        "overall_status": "PASS", "reconciliation": {"executed": True}
    }
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.certification_triggered is True
    assert record.certification_result == "PASS"
    assert record.status == "COMPLETED"


@pytest.mark.anyio
async def test_orchestrator_finalize_cert_degraded(mock_db, tmp_path):
    """CERTIFY passes with DEGRADED -> certification_triggered=True (still has overall_status)."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {
        "overall_status": "DEGRADED", "reconciliation": {"executed": True}
    }
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.certification_triggered is True
    assert record.certification_result == "DEGRADED"


@pytest.mark.anyio
async def test_orchestrator_finalize_cert_fails(mock_db, tmp_path):
    """CERTIFY fails (status=FAILED) -> certification_triggered=False."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.side_effect = Exception("Cert crash")
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.certification_triggered is False
    assert record.certification_result is None


@pytest.mark.anyio
async def test_orchestrator_finalize_knowledge_passes(mock_db, tmp_path):
    """KNOWLEDGE passes with overall_status=PASS -> knowledge_updated=True."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {"overall_status": "PASS"}
    orchestrator.knowledge = MagicMock()
    orchestrator.knowledge.trigger.return_value = {
        "overall_status": "PASS", "knowledge_index": {"executed": True, "status": "PASS"}
    }
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.knowledge_updated is True


@pytest.mark.anyio
async def test_orchestrator_finalize_knowledge_skipped(mock_db, tmp_path):
    """KNOWLEDGE returns overall_status=DEGRADED -> knowledge_updated=False."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {"overall_status": "PASS"}
    orchestrator.knowledge = MagicMock()
    orchestrator.knowledge.trigger.return_value = {
        "overall_status": "DEGRADED", "knowledge_index": {"executed": False, "status": "SKIPPED"}
    }
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.knowledge_updated is False


@pytest.mark.anyio
async def test_orchestrator_finalize_knowledge_no_overall(mock_db, tmp_path):
    """KNOWLEDGE returns result without overall_status -> knowledge_updated=False."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {"overall_status": "PASS"}
    orchestrator.knowledge = MagicMock()
    orchestrator.knowledge.trigger.return_value = {"knowledge_index": {"executed": True}}
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.knowledge_updated is False


@pytest.mark.anyio
async def test_orchestrator_default_wiring_creates_knowledge_indexer(mock_db):
    """Default constructor creates KnowledgeIndexer+PatternRegistry for KnowledgeTrigger."""
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    kt = orchestrator.knowledge
    assert kt._has_indexer is True
    assert kt._has_registry is True
    assert kt.indexer is not None
    assert kt.registry is not None


@pytest.mark.anyio
async def test_orchestrator_knowledge_content_reads_correct_depth(mock_db, tmp_path):
    """Verify finalize reads knowledge_result at cert_result depth pattern.

    Context structure is:
      context["KNOWLEDGE"] = {"status": "PASS", "knowledge_result": {...}}
    NOT:
      context["KNOWLEDGE"] = {"status": "PASS", "overall_status": "..."}
    """
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    orchestrator = IngestionOrchestrator(db=mock_db)
    orchestrator.persistence = _mock_persistence()
    orchestrator.certification = MagicMock()
    orchestrator.certification.trigger.return_value = {"overall_status": "PASS"}
    inner = MagicMock()
    inner.trigger.return_value = {
        "overall_status": "PASS",
        "knowledge_index": {"executed": True, "status": "PASS"},
    }
    orchestrator.knowledge = inner
    p = _make_csv(tmp_path)
    record = await orchestrator.run(p)
    assert record.knowledge_updated is True
    inner.trigger.return_value = {
        "overall_status": "DEGRADED",
        "knowledge_index": {"executed": False, "status": "SKIPPED"},
    }
    record2 = await orchestrator.run(p)
    assert record2.knowledge_updated is False
