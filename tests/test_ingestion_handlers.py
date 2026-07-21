"""Tests for ETAPA 5-10: Ingestion Handlers.

Tests each handler independently with mock DB.
PersistenceEngine uses MockLoader to avoid real DB mutations.
"""
from __future__ import annotations
import json
import hashlib
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
import pytest

from engine.v4.ingestion import IngestionRegistry
from engine.v4.ingestion.handlers.file_detector import FileDetector
from engine.v4.ingestion.handlers.integrity_validator import IntegrityValidator
from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier
from engine.v4.ingestion.handlers.persistence_engine import PersistenceEngine
from engine.v4.ingestion.handlers.certification_trigger import CertificationTrigger
from engine.v4.ingestion.handlers.knowledge_trigger import KnowledgeTrigger


# ─── Helpers ───

def _make_mock_db():
    """Create a mock DatabaseV4 with query/execute capability."""
    db = MagicMock()
    import pandas as pd
    # file_registry.empty return (no duplicates by default)
    db.query.return_value = pd.DataFrame()
    db.file_registered.return_value = False
    return db


def _make_csv(tmp_path: Path, name: str = "test.csv", content: str = "col1,col2\n1,2\n"):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def _make_xlsx(tmp_path: Path, name: str = "test.xlsx", sheets: list[str] | None = None):
    import pandas as pd
    p = tmp_path / name
    with pd.ExcelWriter(p, engine="openpyxl") as writer:
        for s in (sheets or ["Sheet1"]):
            pd.DataFrame({"a": [1]}).to_excel(writer, sheet_name=s, index=False)
    return p


def _make_xml(tmp_path: Path, name: str = "test.xml", content: str = "<root><item>1</item></root>"):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


# ─── FileDetector Tests ───

class TestFileDetector:
    def test_detect_basic_file(self, tmp_path):
        p = _make_csv(tmp_path)
        d = FileDetector()
        result = d.detect(str(p))
        assert result["file_name"] == "test.csv"
        assert result["extension"] == ".csv"
        assert result["file_size_bytes"] > 0
        assert len(result["sha256"]) == 64

    def test_detect_marketplace_ml(self):
        d = FileDetector()
        assert d._detect_marketplace("ML_Facturacion_202601.xlsx") == "ML"
        assert d._detect_marketplace("MercadoLibre_report.csv") == "ML"
        assert d._detect_marketplace("meli_ventas.xlsx") == "ML"

    def test_detect_marketplace_paris(self):
        d = FileDetector()
        assert d._detect_marketplace("PARIS_Dropshipping_202601.xlsx") == "PARIS"
        assert d._detect_marketplace("Cencosud_ventas.xlsx") == "PARIS"

    def test_detect_marketplace_ripley(self):
        d = FileDetector()
        assert d._detect_marketplace("RIPLEY_202601.xlsx") == "RIPLEY"

    def test_detect_marketplace_falabella(self):
        d = FileDetector()
        assert d._detect_marketplace("FALABELLA_ordenes.csv") == "FALABELLA"

    def test_detect_document_type(self):
        d = FileDetector()
        assert d._detect_document_type("ML_Facturacion.xlsx") == "facturacion"
        assert d._detect_document_type("Poscobro_202601.xlsx") == "poscobro"
        assert d._detect_document_type("liberaciones_202601.xlsx") == "liberaciones"
        assert d._detect_document_type("dteproveedor_5371.xml") == "dte"

    def test_detect_period_yyyymm(self):
        d = FileDetector()
        assert d._detect_period("ML_Facturacion_2026-01.xlsx") == "2026-01"
        assert d._detect_period("2025-12_report.xlsx") == "2025-12"

    def test_detect_period_spanish_month(self):
        d = FileDetector()
        assert d._detect_period("1 enero 2026 - 31 enero 2026.xlsx") == "2026-01"
        assert d._detect_period("1 junio 2026 - 30 junio 2026.xlsx") == "2026-06"

    def test_detect_period_year_first(self):
        d = FileDetector()
        assert d._detect_period("2026 enero.xlsx") == "2026-01"

    def test_detect_no_period(self):
        d = FileDetector()
        assert d._detect_period("unknown_file.xlsx") is None

    def test_detect_unknown_marketplace(self):
        d = FileDetector()
        assert d._detect_marketplace("random_file.csv") is None

    def test_sha256_consistency(self, tmp_path):
        p = _make_csv(tmp_path, content="hello,world\n1,2\n")
        d = FileDetector()
        h1 = d._compute_sha256(p)
        h2 = hashlib.sha256(p.read_bytes()).hexdigest()
        assert h1 == h2


# ─── IntegrityValidator Tests ───

class TestIntegrityValidator:
    def test_valid_csv_passes(self, tmp_path):
        p = _make_csv(tmp_path)
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc123", ".csv")
        assert len(issues) == 0

    def test_invalid_extension(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello")
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc123", ".txt")
        assert any(i["type"] == "invalid_extension" for i in issues)

    def test_empty_file(self, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_text("")
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc", ".csv")
        assert any(i["type"] == "empty_file" for i in issues)

    def test_file_not_found(self, tmp_path):
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(tmp_path / "nonexistent.csv"), "abc", ".csv")
        assert any(i["type"] == "file_not_found" for i in issues)

    def test_duplicate_detected(self, tmp_path):
        p = _make_csv(tmp_path)
        import pandas as pd
        db = _make_mock_db()
        db.query.return_value = pd.DataFrame({
            "file_name": ["existing.csv"],
            "processed_at": ["2026-01-01 12:00:00"],
        })
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "dup_sha", ".csv")
        assert any(i["type"] == "duplicate_file" for i in issues)

    def test_valid_xlsx_passes(self, tmp_path):
        p = _make_xlsx(tmp_path)
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc123", ".xlsx")
        assert len(issues) == 0

    def test_valid_xml_passes(self, tmp_path):
        p = _make_xml(tmp_path)
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc123", ".xml")
        assert len(issues) == 0

    def test_malformed_xml_detected(self, tmp_path):
        p = _make_xml(tmp_path, content="<root><unclosed>")
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc", ".xml")
        assert any(i["type"] == "malformed_xml" for i in issues)

    def test_csv_no_delimiter(self, tmp_path):
        p = _make_csv(tmp_path, content="no delimiter here\n")
        db = _make_mock_db()
        v = IntegrityValidator(db=db)
        issues = v.validate(str(p), "abc", ".csv")
        assert any(i["type"] == "no_delimiter" for i in issues)


# ─── MarketplaceClassifier Tests ───

class TestMarketplaceClassifier:
    def test_classify_ml_with_filename(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "ML_Facturacion_202601.xlsx")
        assert result["marketplace"] == "ML"
        assert result["loader"] == "SurgicalLoader"
        assert result["pipeline"] == "ml_v4"
        assert result["confidence"] == "HIGH"

    def test_classify_paris_with_filename(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "PARIS_Fulfillment_202601.xlsx")
        assert result["marketplace"] == "PARIS"
        assert result["loader"] == "SurgicalLoader"

    def test_classify_ripley_with_filename(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "RIPLEY_202601.xlsx")
        assert result["marketplace"] == "RIPLEY"

    def test_classify_via_path_fallback(self, tmp_path):
        p = tmp_path / "ML" / "data.xlsx"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("dummy")
        c = MarketplaceClassifier()
        result = c.classify(str(p))
        assert result["marketplace"] == "ML"

    def test_classify_unknown(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "random_file.txt")
        assert result["marketplace"] is None
        assert result["confidence"] == "LOW"

    def test_classify_document_type_detected(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "PARIS_Dropshipping_202601.xlsx")
        assert result["document_type"] == "dropshipping"

    def test_classify_period_detected(self):
        c = MarketplaceClassifier()
        result = c.classify("dummy_path", "ML_Facturacion_2026-01.xlsx")
        assert result["period"] == "2026-01"


# ─── Mock Loader for PersistenceEngine Tests ───

class MockLoader:
    def __init__(self, return_count: int = 100):
        self.return_count = return_count
        self.last_marketplace = None

    def load_marketplace(self, marketplace: str) -> int:
        self.last_marketplace = marketplace
        return self.return_count


class TestPersistenceEngine:
    def test_persist_registers_file(self, tmp_path):
        p = _make_csv(tmp_path)
        sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
        db = _make_mock_db()
        loader = MockLoader(return_count=50)
        pe = PersistenceEngine(db=db, loader=loader)
        result = pe.persist(str(p), "ML", sha256)
        assert result["file_registered"] is True
        assert result["loader_executed"] is True
        db.register_file.assert_called_once()

    def test_persist_with_loader_error(self, tmp_path):
        p = _make_csv(tmp_path)
        db = _make_mock_db()
        bad_loader = MagicMock()
        bad_loader.load_marketplace.side_effect = RuntimeError("Loader crash")
        pe = PersistenceEngine(db=db, loader=bad_loader)
        sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
        result = pe.persist(str(p), "ML", sha256)
        assert result["loader_executed"] is False
        assert len(result["errors"]) > 0
        assert "Loader crashed" in result["errors"][0] or "failed" in result["errors"][0].lower()

    def test_mock_loader_injection(self):
        loader = MockLoader(return_count=42)
        result = loader.load_marketplace("PARIS")
        assert result == 42
        assert loader.last_marketplace == "PARIS"

    def test_persist_unknown_marketplace(self, tmp_path):
        p = _make_csv(tmp_path)
        db = _make_mock_db()
        loader = MockLoader()
        pe = PersistenceEngine(db=db, loader=loader)
        sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
        result = pe.persist(str(p), "UNKNOWN", sha256)
        assert result["file_registered"]
        assert loader.last_marketplace == "UNKNOWN"


# ─── CertificationTrigger Tests ───

class TestCertificationTrigger:
    def test_trigger_calls_engines(self):
        db = _make_mock_db()
        import pandas as pd
        # DTE coverage returns data
        db.query.return_value = pd.DataFrame({"total": [100], "with_dte": [50]})

        rec_engine = MagicMock()
        rec_engine.reconcile_ledger_vs_cierre.return_value = {}

        cert_engine = MagicMock()
        cert_engine.certify.return_value = {"kpi1": {"status": "CERTIFIED"}}

        gap_engine = MagicMock()
        gap_engine.analyze.return_value = []

        ct = CertificationTrigger(
            db=db,
            reconciliation_engine=rec_engine,
            certification_engine=cert_engine,
            gap_engine=gap_engine,
        )
        result = ct.trigger("ML", "2026-01")
        assert result["reconciliation"]["executed"] is True
        assert result["certification"]["executed"] is True
        assert result["coverage"]["executed"] is True
        assert result["gaps"]["executed"] is True
        assert result["overall_status"] in ("PASS", "DEGRADED")

    def test_trigger_reconciliation_error(self):
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame({"total": [100], "with_dte": [50]})
        rec_engine = MagicMock()
        rec_engine.reconcile_ledger_vs_cierre.side_effect = ValueError("Recon error")
        cert_engine = MagicMock()
        cert_engine.certify.return_value = {"kpi1": {"status": "CERTIFIED"}}
        gap_engine = MagicMock()
        gap_engine.analyze.return_value = []

        ct = CertificationTrigger(
            db=db, reconciliation_engine=rec_engine,
            certification_engine=cert_engine, gap_engine=gap_engine,
        )
        result = ct.trigger("ML")
        assert "Recon error" in str(result["errors"])


# ─── KnowledgeTrigger Tests ───

class TestKnowledgeTrigger:
    def test_trigger_calls_indexer_and_patterns(self):
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame({
            "detalle": ["Comision", "Descuento"],
            "cnt": [10, 5],
            "total": [100.0, -50.0],
            "has_negative": [False, True],
        })

        indexer = MagicMock()
        indexer.build_knowledge_index.return_value = True

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer)
        result = kt.trigger("ML", "2026-01")
        assert result["knowledge_index"]["executed"] is True
        assert result["knowledge_index"]["status"] == "PASS"
        assert len(result["new_patterns"]) == 2

    def test_trigger_indexer_error(self):
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame()
        indexer = MagicMock()
        indexer.build_knowledge_index.side_effect = RuntimeError("Indexer crash")

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer)
        result = kt.trigger("ML")
        assert "Indexer crash" in str(result["errors"])
        assert result["knowledge_index"]["status"] == "ERROR"

    def test_trigger_with_registry_calls_obsidian(self, tmp_path):
        """C4: KnowledgeTrigger with pattern_registry + obsidian_path exports patterns."""
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame({
            "detalle": ["Comision"],
            "cnt": [10],
            "total": [100.0],
            "has_negative": [False],
        })

        indexer = MagicMock()
        indexer.build_knowledge_index.return_value = True

        registry = MagicMock()
        vault = tmp_path / "obsidian_vault"
        vault.mkdir(parents=True, exist_ok=True)
        registry.to_obsidian.return_value = 5

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer, pattern_registry=registry, obsidian_path=str(vault))
        result = kt.trigger("ML", "2026-01")
        assert result["knowledge_index"]["executed"] is True
        assert result["knowledge_index"]["status"] == "PASS"
        assert len(result["new_patterns"]) == 1
        assert result["obsidian_written"] == 5
        registry.to_obsidian.assert_called_once_with(vault)

    def test_trigger_no_indexer_skipped(self):
        """C2: KnowledgeTrigger without indexer returns SKIPPED."""
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame()
        kt = KnowledgeTrigger(db=db)
        result = kt.trigger("ML")
        assert result["knowledge_index"]["executed"] is False
        assert result["knowledge_index"]["status"] == "SKIPPED"
        assert result["knowledge_index"]["reason"] == "No indexer provided"

    def test_trigger_with_registry_no_obsidian_path(self):
        """C4: KnowledgeTrigger with registry but no obsidian_path skips export."""
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame()

        indexer = MagicMock()
        indexer.build_knowledge_index.return_value = True
        registry = MagicMock()

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer, pattern_registry=registry)
        result = kt.trigger("ML")
        assert result["knowledge_index"]["executed"] is True
        assert result["obsidian_written"] == 0
        registry.to_obsidian.assert_not_called()

    def test_trigger_with_registry_vault_not_found(self, tmp_path):
        """C4: Obsidian export is skipped when vault path doesn't exist."""
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame()

        indexer = MagicMock()
        indexer.build_knowledge_index.return_value = True
        registry = MagicMock()
        vault = tmp_path / "nonexistent_vault"

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer, pattern_registry=registry, obsidian_path=str(vault))
        result = kt.trigger("ML")
        assert result["obsidian_written"] == 0
        registry.to_obsidian.assert_not_called()

    def test_trigger_with_registry_obsidian_error(self, tmp_path):
        """C4: Obsidian export error is captured but doesn't crash trigger."""
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame()

        indexer = MagicMock()
        indexer.build_knowledge_index.return_value = True
        registry = MagicMock()
        registry.to_obsidian.side_effect = RuntimeError("Disk full")
        vault = tmp_path / "obsidian_vault"
        vault.mkdir(parents=True, exist_ok=True)

        kt = KnowledgeTrigger(db=db, knowledge_indexer=indexer, pattern_registry=registry, obsidian_path=str(vault))
        result = kt.trigger("ML")
        assert "Disk full" in str(result["errors"])
        assert result["obsidian_written"] == 0

    def test_find_new_detalles_queries_ledger(self):
        db = _make_mock_db()
        import pandas as pd
        db.query.return_value = pd.DataFrame({
            "detalle": ["Comision", "Descuento", "Reembolso"],
            "cnt": [100, 50, 25],
            "total": [1000.0, -200.0, -50.0],
            "has_negative": [False, True, True],
        })
        kt = KnowledgeTrigger(db=db)
        detalles = kt._find_new_detalles("ML")
        assert len(detalles) == 3
        assert detalles[0]["detalle"] == "Comision"
        assert detalles[0]["count"] == 100


# ─── IngestionRegistry Integration Tests ───

class TestIngestionRegistry:
    def test_create_record(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            f.write("a,b\n1,2\n")
            tmp = f.name
        try:
            reg = IngestionRegistry(db=_make_mock_db())
            rec = reg.create_record("test.csv", tmp)
            assert rec.status == "STARTED"
            assert rec.execution_id is not None
            assert rec.file_name == "test.csv"
        finally:
            Path(tmp).unlink(missing_ok=True)

    def test_add_error_sets_failed(self):
        reg = IngestionRegistry(db=_make_mock_db())
        rec = reg.create_record("test.csv", "dummy")
        reg.add_error(rec, "test error")
        assert rec.status == "FAILED"
        assert "test error" in rec.errors

    def test_finalize_sets_certified(self):
        reg = IngestionRegistry(db=_make_mock_db())
        rec = reg.create_record("test.csv", "dummy")
        reg.finalize(rec, certification_triggered=True, certification_result="PASS")
        assert rec.status == "CERTIFIED"
        assert rec.certification_triggered is True
        assert rec.end_time is not None
        assert rec.execution_time_seconds is not None

    def test_finalize_sets_persisted(self):
        reg = IngestionRegistry(db=_make_mock_db())
        rec = reg.create_record("test.csv", "dummy")
        reg.finalize(rec)
        assert rec.status == "PERSISTED"
        assert rec.certification_triggered is False
