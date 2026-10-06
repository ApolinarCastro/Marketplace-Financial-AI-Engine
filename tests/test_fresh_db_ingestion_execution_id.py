"""Fresh-DB ledger execution_id contract tests (PFO-FRESH-DB-EXECUTION-ID-001).

Proves a brand-new DatabaseV4 can ingest through the real pipeline:
  1. fresh schema contains execution_id (nullable, legacy-compatible),
  2. pre-existing tables without the column still migrate,
  3. fresh ingestion completes and every new ledger row carries the
     ingestion record's execution_id,
  4. financial content unchanged (8 rows, total 20800.0).

All tests use isolated tmp_path databases + isolated RAW dirs.
No test touches data/db/meli_financial_v4.db, 01_Raw/, or production state.
"""
from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

import pytest

from engine.v4.database import DatabaseV4

GOLDEN_INPUT = Path("tests/golden/e2e_v1/input/ML_Facturacion_E2E_V1.xlsx")
ARCHIVO = "ML_Facturacion_E2E_V1.xlsx"


def _fresh_db(tmp_path: Path, name: str = "fresh.db") -> DatabaseV4:
    return DatabaseV4(db_path=str(tmp_path / name), read_only=False)


def test_fresh_schema_contains_execution_id_nullable(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        cols = db.query(
            "SELECT column_name, data_type, is_nullable FROM information_schema.columns "
            "WHERE table_name = 'marketplace_ledger_v1' ORDER BY ordinal_position"
        )
        by_name = {r["column_name"]: r for _, r in cols.iterrows()}
        assert "execution_id" in by_name, f"columns: {list(by_name)}"
        assert by_name["execution_id"]["data_type"] == "VARCHAR"
        assert str(by_name["execution_id"]["is_nullable"]).upper() == "YES"
    finally:
        db.close()


def test_legacy_table_without_column_still_migrates(tmp_path: Path):
    import duckdb

    legacy_path = tmp_path / "legacy.db"
    con = duckdb.connect(str(legacy_path))
    try:
        con.execute(
            "CREATE TABLE marketplace_ledger_v1 (marketplace TEXT, "
            "id_transaccion TEXT, monto DOUBLE)"
        )
        con.execute(
            "INSERT INTO marketplace_ledger_v1 VALUES ('ML', 'LEGACY-1', 100.0)"
        )
    finally:
        con.close()
    db = DatabaseV4(db_path=str(legacy_path), read_only=False)
    try:
        cols = db.query(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'marketplace_ledger_v1'"
        )["column_name"].tolist()
        assert "execution_id" in cols
        rows = db.query("SELECT id_transaccion, monto FROM marketplace_ledger_v1").values.tolist()
        assert rows == [["LEGACY-1", 100.0]]
    finally:
        db.close()


def test_fresh_db_ingestion_completes_with_execution_id(tmp_path: Path):
    from engine.v4.ingestion import IngestionRegistry
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    import engine.v4.surgical_loader as sl_mod

    raw_dir = tmp_path / "raw" / "ML" / "Facturacion"
    raw_dir.mkdir(parents=True)
    shutil.copy2(GOLDEN_INPUT, raw_dir / ARCHIVO)

    db = _fresh_db(tmp_path, "ingest.db")
    db.is_read_only = False
    DatabaseV4._instance = db
    DatabaseV4._register_shutdown_hook()
    orig_dir = sl_mod.DIR_FACTURACION
    sl_mod.DIR_FACTURACION = raw_dir
    try:
        registry = IngestionRegistry(db=db)
        orch = IngestionOrchestrator(db=db, registry=registry, post_persist_stages=False)
        record = asyncio.run(orch.run(
            file_path=str(raw_dir / ARCHIVO), user="PFO_FRESH_DB_TEST"))
        assert record.status == "COMPLETED"
        assert (record.errors or []) == []
        assert int(record.records_new or 0) == 8

        DatabaseV4.reset()
        import duckdb as _ddb
        con = _ddb.connect(str(tmp_path / "ingest.db"), read_only=True)
        try:
            stats = con.execute(
                "SELECT COUNT(*) AS rows, COUNT(execution_id) AS with_exec, "
                "COUNT(DISTINCT execution_id) AS distinct_exec, "
                "COALESCE(SUM(monto), 0) AS total "
                "FROM marketplace_ledger_v1 "
                f"WHERE archivo_origen = '{ARCHIVO}'"
            ).fetchone()
            exec_ids = con.execute(
                "SELECT DISTINCT execution_id FROM marketplace_ledger_v1 "
                f"WHERE archivo_origen = '{ARCHIVO}'"
            ).fetchall()
        finally:
            con.close()
        assert int(stats[0]) == 8
        assert int(stats[1]) == 8
        assert int(stats[2]) == 1
        assert round(float(stats[3]), 2) == 20800.0
        assert len(exec_ids) == 1
        assert str(exec_ids[0][0]) == str(record.execution_id)
    finally:
        sl_mod.DIR_FACTURACION = orig_dir
        try:
            DatabaseV4.reset()
            DatabaseV4._instances = {}
            DatabaseV4._instance = None
            DatabaseV4._shutdown_registered = False
        except Exception:
            pass
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
