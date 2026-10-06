"""DocumentMatchWriter — persistence tests for validated document matches.

All tests run against isolated temporary databases (tmp_path).
No test touches data/db/meli_financial_v4.db, 01_Raw/, or production state.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.v4.database import DatabaseV4
from engine.v4.matching.document_match_writer import (
    DocumentMatchConflictError,
    DocumentMatchError,
    DocumentMatchWriter,
    deterministic_match_id,
)


def _fresh_db(tmp_path: Path) -> DatabaseV4:
    return DatabaseV4(db_path=str(tmp_path / "test_match.db"), read_only=False)


def _match(**overrides) -> dict:
    base = {
        "marketplace": "ML",
        "ledger_id": "TEST-LEDGER-001",
        "order_id": "TEST-ORDER-001",
        "folio_xml": "TEST-FOLIO-001",
        "match_rule": "TEST_RULE",
        "match_source": "pfo_test",
        "match_status": "CONCILIATED",
        "document_date": "2026-06-15",
        "document_amount": 20800.0,
        "created_by": "pfo_test",
    }
    base.update(overrides)
    return base


# ── PASO 5: fresh DB creates the table, empty ─────────────────────────

def test_fresh_db_creates_document_match_table_empty(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        cols = db.query(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'document_match_v1' ORDER BY ordinal_position"
        )["column_name"].tolist()
        assert cols == [
            "match_id", "marketplace", "ledger_id", "order_id", "folio_xml",
            "tipo_dte", "match_rule", "match_source", "match_timestamp",
            "match_status", "document_date", "document_amount",
            "reference_document", "created_by", "execution_id",
        ], f"schema mismatch: {cols}"
        assert db.query("SELECT COUNT(*) AS n FROM document_match_v1")["n"].iloc[0] == 0
    finally:
        db.close()


def test_deterministic_match_id_stable():
    a = deterministic_match_id("ML", "TEST-LEDGER-001")
    b = deterministic_match_id("ML", "TEST-LEDGER-001")
    assert a == b
    assert a.startswith("dm-")
    assert deterministic_match_id("ML", "OTHER") != a


# ── PASO 6: insert + readback + idempotent re-write ───────────────────

def test_writer_insert_and_readback(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        writer = DocumentMatchWriter(db=db)
        out = writer.write(_match())
        assert out["outcome"] == "INSERTED"
        assert writer.count() == 1

        row = writer.find_existing("ML", "TEST-LEDGER-001")
        assert row is not None
        assert row["match_status"] == "CONCILIATED"
        assert row["order_id"] == "TEST-ORDER-001"
        assert float(row["document_amount"]) == 20800.0
        assert out["match_id"] == row["match_id"]
    finally:
        db.close()


def test_writer_duplicate_identical_is_idempotent(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        writer = DocumentMatchWriter(db=db)
        first = writer.write(_match())
        second = writer.write(_match())
        assert first["outcome"] == "INSERTED"
        assert second["outcome"] == "SKIPPED_EXISTING"
        assert second["match_id"] == first["match_id"]
        assert writer.count() == 1
    finally:
        db.close()


def test_writer_conflicting_match_raises(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        writer = DocumentMatchWriter(db=db)
        writer.write(_match())
        with pytest.raises(DocumentMatchConflictError):
            writer.write(_match(match_status="REJECTED"))
        assert writer.count() == 1
    finally:
        db.close()


# ── PASO 8: negative tests ────────────────────────────────────────────

def test_writer_rejects_missing_marketplace(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        with pytest.raises(DocumentMatchError):
            DocumentMatchWriter(db=db).write(_match(marketplace=""))
    finally:
        db.close()


def test_writer_rejects_missing_ledger_id(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        with pytest.raises(DocumentMatchError):
            DocumentMatchWriter(db=db).write(_match(ledger_id=""))
    finally:
        db.close()


def test_writer_rejects_invalid_status(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        with pytest.raises(DocumentMatchError):
            DocumentMatchWriter(db=db).write(_match(match_status="MAYBE"))
        assert db.query("SELECT COUNT(*) AS n FROM document_match_v1")["n"].iloc[0] == 0
    finally:
        db.close()


def test_writer_rejects_missing_document_date(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        rec = _match()
        del rec["document_date"]
        with pytest.raises(DocumentMatchError):
            DocumentMatchWriter(db=db).write(rec)
    finally:
        db.close()


# ── PASO 7: reconciliation coverage consumption ───────────────────────

def test_reconciliation_document_coverage_consumes_writer_output(tmp_path: Path):
    """1 matched ledger row / 1 ledger row = document_coverage 100.0.

    Uses the exact join contract from ReconciliationEngine._document_coverage:
    clasificado LEFT JOIN document_match_v1 ON marketplace + ledger_id.
    """
    db = _fresh_db(tmp_path)
    try:
        db.execute(
            "INSERT INTO marketplace_ledger_clasificado_v1 (marketplace, "
            "id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha, "
            "clasificacion_operativa, include_in_operational_pnl, financial_group) "
            "VALUES ('ML', 'TEST-LEDGER-001', 'TEST-ORDER-001', 'Cargo por venta (Venta)', "
            "'INGRESO_VENTA', 50000.0, '2026-06-01', 'Cargo por venta (Venta)', TRUE, 'ingresos')"
        )
        writer = DocumentMatchWriter(db=db)
        out = writer.write(_match())
        assert out["outcome"] == "INSERTED"

        cov = db.query(
            "SELECT COUNT(*) AS total, "
            "SUM(CASE WHEN d.match_id IS NOT NULL THEN 1 ELSE 0 END) AS matched "
            "FROM marketplace_ledger_clasificado_v1 c "
            "LEFT JOIN document_match_v1 d ON c.marketplace = d.marketplace "
            "AND c.id_transaccion = d.ledger_id "
            "WHERE c.marketplace = 'ML' AND c.fecha >= '2026-06-01'"
        ).iloc[0]
        total = float(cov["total"])
        matched = float(cov["matched"])
        assert total == 1.0
        assert matched == 1.0
        assert (matched / total * 100) == 100.0
    finally:
        db.close()
