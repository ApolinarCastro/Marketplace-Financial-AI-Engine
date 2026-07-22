"""Tests for Phase 12.1 — Data Lineage Engine."""
from __future__ import annotations
import pytest
from engine.v4.lineage import LineageEngine, LineageRecord
from engine.v4.database import DatabaseV4


@pytest.fixture
def engine():
    return LineageEngine()


def test_trace_transaction_found(engine):
    db = DatabaseV4.get()
    sample = db.query("SELECT id_transaccion FROM marketplace_ledger_v1 LIMIT 1")
    if sample.empty:
        pytest.skip("No transactions in ledger")
    tid = str(sample.iloc[0]["id_transaccion"])
    record = engine.trace_transaction(tid)
    assert record is not None
    assert record.id_transaccion == tid
    assert len(record.steps) >= 2


def test_trace_transaction_not_found(engine):
    record = engine.trace_transaction("NONEXISTENT_ID")
    assert record is None


def test_trace_order_found(engine):
    db = DatabaseV4.get()
    sample = db.query("SELECT id_orden FROM marketplace_ledger_v1 WHERE id_orden IS NOT NULL AND id_orden != '' LIMIT 1")
    if sample.empty:
        pytest.skip("No orders in ledger")
    oid = str(sample.iloc[0]["id_orden"])
    records = engine.trace_order(oid)
    assert len(records) >= 1


def test_trace_document_found(engine):
    db = DatabaseV4.get()
    sample = db.query("SELECT folio_xml FROM marketplace_ledger_v1 WHERE folio_xml IS NOT NULL AND folio_xml != '' LIMIT 1")
    if sample.empty:
        pytest.skip("No documents in ledger")
    folio = str(sample.iloc[0]["folio_xml"])
    records = engine.trace_document(folio)
    assert len(records) >= 1


def test_include_in_operational_pnl_flag(engine):
    db = DatabaseV4.get()
    sample = db.query("SELECT id_transaccion FROM marketplace_ledger_clasificado_v1 WHERE COALESCE(include_in_operational_pnl, 1) = 0 LIMIT 1")
    if sample.empty:
        pytest.skip("No non-operational transactions")
    tid = str(sample.iloc[0]["id_transaccion"])
    record = engine.trace_transaction(tid)
    assert record is not None
    assert record.include_in_operational_pnl is False
