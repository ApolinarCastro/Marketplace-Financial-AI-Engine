"""F3-05: CAP-001 Definitive Certification.
Fixed fixture, isolated environment, automatic rollback, proper tracking.

Requirements:
  - 1 fixed fixture (+ generate + save + sha256)
  - Complete isolation (temp DB, temp RAW, guard on official DB+RAW)
  - Automatic rollback (context managers for DatabaseV4 & SurgicalLoader)
  - Proper tracking (records_new, records_existing, ledger_rows_total)
  - 3 clean runs (fresh env each run)
  - 1 idempotent reingest (same env, records_new=0, records_existing=8, total=8, status=IDEMPOTENT)
  - Single Financial Truth preserved (official DB hash unchanged after full suite)
"""
from __future__ import annotations
import hashlib
import gc
import shutil
from contextlib import contextmanager
from pathlib import Path

import pytest

# ── paths ──────────────────────────────────────────────────────────────
FIXTURE_PATH = Path("tests/fixtures/f3_03/f3_03_fixture.xlsx")
FIXTURE_SHA256 = "9BE8EFFCBA44CCE1810E775651F872B2B4891FB61850D0CF5A7AA6859FED7D9A"
FIXTURE_SIZE = 5108

BASELINE = Path("data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db")
OFFICIAL_DB = Path("data/db/meli_financial_v4.db")
OFFICIAL_RAW = Path("01_Raw")

TEMP_BASE = Path("data/db/tmp_f3_05")

FIXTURE_FILENAME = "f3_03_fixture.xlsx"
EXPECTED_ROWS = 8
EXPECTED_TOTAL = 20800.0
EXPECTED_VENTAS = ["F3-03-001", "F3-03-002"]


# ── helpers ────────────────────────────────────────────────────────────
def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


@contextmanager
def redirect_surgical_loader(temp_raw):
    import engine.v4.surgical_loader as sl_mod
    orig = sl_mod.DIR_FACTURACION
    sl_mod.DIR_FACTURACION = temp_raw
    try:
        yield
    finally:
        sl_mod.DIR_FACTURACION = orig


@contextmanager
def redirect_databasev4(temp_db_path):
    from engine.v4 import database as db_module
    DatabaseV4 = db_module.DatabaseV4
    orig_path = db_module.DB_PATH
    DatabaseV4.reset()
    db = DatabaseV4(db_path=str(temp_db_path), read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    try:
        yield
    finally:
        DatabaseV4.reset()
        db_module.DB_PATH = orig_path


def create_env():
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    gc.collect()
    if TEMP_BASE.exists():
        shutil.rmtree(TEMP_BASE, ignore_errors=True)
        gc.collect()
        if TEMP_BASE.exists():
            import time
            time.sleep(0.3)
            shutil.rmtree(TEMP_BASE, ignore_errors=True)
    TEMP_BASE.mkdir(parents=True)
    temp_db = TEMP_BASE / "meli_financial_v4.db"
    shutil.copy2(BASELINE, temp_db)
    temp_raw = TEMP_BASE / "01_Raw" / "ML" / "Facturacion"
    temp_raw.mkdir(parents=True)
    shutil.copy2(FIXTURE_PATH, temp_raw / FIXTURE_FILENAME)
    return {"temp_db": temp_db, "temp_raw": temp_raw}


def destroy_env():
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    gc.collect()
    if TEMP_BASE.exists():
        shutil.rmtree(TEMP_BASE, ignore_errors=True)


def collect_raw_files():
    return sorted(
        str(p.relative_to(OFFICIAL_RAW))
        for p in OFFICIAL_RAW.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )


# ── module-scoped guard fixture ───────────────────────────────────────
@pytest.fixture(scope="module")
def isolation_guard():
    before_hash = sha256(OFFICIAL_DB)
    before_raw = collect_raw_files()
    yield
    after_hash = sha256(OFFICIAL_DB)
    after_raw = collect_raw_files()
    assert after_hash == before_hash, (
        f"GUARD F3-05: Official DB hash changed!"
        f" Before {before_hash}, after {after_hash}"
    )
    assert after_raw == before_raw, (
        "GUARD F3-05: Official RAW files changed!"
    )


# ── tests ─────────────────────────────────────────────────────────────
@pytest.mark.anyio
async def test_f3_05_fixture_immutable(isolation_guard):
    assert FIXTURE_PATH.exists(), f"Fixture not found at {FIXTURE_PATH}"
    actual_sha = sha256(FIXTURE_PATH)
    assert actual_sha == FIXTURE_SHA256, (
        f"Fixture SHA256 mismatch! Expected {FIXTURE_SHA256}, got {actual_sha}"
    )
    actual_size = FIXTURE_PATH.stat().st_size
    assert actual_size == FIXTURE_SIZE, (
        f"Fixture size mismatch! Expected {FIXTURE_SIZE}, got {actual_size}"
    )


@pytest.mark.anyio
async def test_f3_05_three_clean_runs(isolation_guard):
    for i in range(1, 4):
        env = create_env()
        try:
            ledger_rows, total, ventas = await run_pipeline_on(env)
            assert ledger_rows == EXPECTED_ROWS, (
                f"Run {i}: expected {EXPECTED_ROWS} rows, got {ledger_rows}"
            )
            assert total == EXPECTED_TOTAL, (
                f"Run {i}: expected ${EXPECTED_TOTAL}, got ${total}"
            )
            assert ventas == EXPECTED_VENTAS, (
                f"Run {i}: ventas mismatch: {ventas}"
            )
        finally:
            destroy_env()


@pytest.mark.anyio
async def test_f3_05_idempotent_reingest(isolation_guard):
    env = create_env()
    try:
        # First ingest
        with redirect_databasev4(env["temp_db"]), redirect_surgical_loader(env["temp_raw"]):
            r1_records_new, r1_records_existing, r1_total = await run_pipeline_tracked(env)
            assert r1_records_new == EXPECTED_ROWS, (
                f"First ingest: expected {EXPECTED_ROWS} new, got {r1_records_new}"
            )
            assert r1_records_existing == 0, (
                f"First ingest: expected 0 existing, got {r1_records_existing}"
            )

        # Verify total after first ingest (fresh connection to avoid singleton issues)
        verify_total, verify_ventas = await query_ledger(env)
        assert verify_total == EXPECTED_TOTAL, (
            f"First ingest total: expected ${EXPECTED_TOTAL}, got ${verify_total}"
        )
        assert verify_ventas == EXPECTED_VENTAS, (
            f"First ingest ventas: expected {EXPECTED_VENTAS}, got {verify_ventas}"
        )

        # Reingest (same env, same DB)
        with redirect_databasev4(env["temp_db"]), redirect_surgical_loader(env["temp_raw"]):
            r2_records_new, r2_records_existing, r2_total = await run_pipeline_tracked(env)
            assert r2_records_new == 0, (
                f"Reingest: expected 0 new, got {r2_records_new}"
            )
            assert r2_records_existing == EXPECTED_ROWS, (
                f"Reingest: expected {EXPECTED_ROWS} existing, got {r2_records_existing}"
            )
            assert r2_records_new == 0 and r2_records_existing == EXPECTED_ROWS, (
                "Reingest: expected IDEMPOTENT (no new rows)"
            )

        # Verify total unchanged after reingest
        verify2_total, verify2_ventas = await query_ledger(env)
        assert verify2_total == EXPECTED_TOTAL, (
            f"Reingest total: expected ${EXPECTED_TOTAL}, got ${verify2_total}"
        )
        assert verify2_ventas == EXPECTED_VENTAS, (
            f"Reingest ventas: expected {EXPECTED_VENTAS}, got {verify2_ventas}"
        )
    finally:
        destroy_env()


# ── pipeline execution helpers ────────────────────────────────────────
async def run_pipeline_on(env):
    """Run pipeline on fresh env, return (ledger_rows, total, ventas)."""
    with redirect_databasev4(env["temp_db"]), redirect_surgical_loader(env["temp_raw"]):
        from engine.v4.database import DatabaseV4
        from engine.v4.ingestion import IngestionRegistry
        from engine.v4.ingestion.orchestrator import IngestionOrchestrator

        db = DatabaseV4._instance
        registry = IngestionRegistry(db=db)
        orch = IngestionOrchestrator(db=db, registry=registry)
        await orch.run(
            file_path=str(env["temp_raw"] / FIXTURE_FILENAME),
            user="f3_05_test",
        )

    return await query_ledger_full(env)  # (row_count, total, ventas)


async def run_pipeline_tracked(env):
    """Run pipeline on existing env, return (records_new, records_existing, total).

    Uses before/after query with archivo_origen filter.
    """
    from engine.v4.database import DatabaseV4
    from engine.v4.ingestion import IngestionRegistry
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator

    db = DatabaseV4._instance

    before_rows = int(db.query(
        "SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
        [FIXTURE_FILENAME]
    ).iloc[0, 0])

    registry = IngestionRegistry(db=db)
    orch = IngestionOrchestrator(db=db, registry=registry)
    record = await orch.run(
        file_path=str(env["temp_raw"] / FIXTURE_FILENAME),
        user="f3_05_test",
    )

    after_rows = int(db.query(
        "SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
        [FIXTURE_FILENAME]
    ).iloc[0, 0])
    after_total = float(db.query(
        "SELECT COALESCE(SUM(monto), 0) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
        [FIXTURE_FILENAME]
    ).iloc[0, 0])

    records_new = after_rows - before_rows
    records_existing = before_rows

    return records_new, records_existing, round(after_total, 2)


async def query_ledger(env):
    """Query ledger from temp DB in a fresh connection, return (total, ventas)."""
    con = _fresh_con(env)
    try:
        total = float(con.execute(
            "SELECT COALESCE(SUM(monto), 0) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
            [FIXTURE_FILENAME]
        ).fetchone()[0])
        ventas = [r[0] for r in con.execute(
            "SELECT order_id FROM ventas_marketplace WHERE source_file = ? ORDER BY order_id",
            [FIXTURE_FILENAME]
        ).fetchall()]
    finally:
        con.close()
    return total, (ventas or [])


async def query_ledger_full(env):
    """Query ledger from temp DB in a fresh connection, return (row_count, total, ventas)."""
    con = _fresh_con(env)
    try:
        row_count = int(con.execute(
            "SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
            [FIXTURE_FILENAME]
        ).fetchone()[0])
        total = float(con.execute(
            "SELECT COALESCE(SUM(monto), 0) FROM marketplace_ledger_v1 WHERE archivo_origen = ?",
            [FIXTURE_FILENAME]
        ).fetchone()[0])
        ventas = [r[0] for r in con.execute(
            "SELECT order_id FROM ventas_marketplace WHERE source_file = ? ORDER BY order_id",
            [FIXTURE_FILENAME]
        ).fetchall()]
    finally:
        con.close()
    return row_count, total, (ventas or [])


def _fresh_con(env):
    import duckdb
    return duckdb.connect(str(env["temp_db"]), read_only=True)
