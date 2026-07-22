"""F3-03 Controlled Ingestion Test.
Isolates fixture in temp directory. Monkey-patches SurgicalLoader.DIR_FACTURACION.
Validates exact financial content + idempotency.
"""
import sys; sys.path.insert(0, ".")
import asyncio
import shutil
import os
import json
import gc
import time
import traceback
import hashlib
import openpyxl
from pathlib import Path
from engine.v4.database import DatabaseV4
from engine.v4.ingestion.orchestrator import IngestionOrchestrator
from engine.v4.ingestion import IngestionRegistry, IngestionRecord
from engine.v4.surgical_loader import SurgicalLoader

# ── paths ────────────────────────────────────────────────
BASELINE = Path("data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db")
TEMP_DIR = Path("data/db/tmp_f3_03")
TEMP_DB  = TEMP_DIR / "meli_financial_v4.db"
TEMP_RAW = TEMP_DIR / "01_Raw" / "ML" / "Facturacion"
FIXTURE_FILE = TEMP_RAW / "_f3_03_fixture.xlsx"

# ── fixture data ─────────────────────────────────────────
FIXTURE_ROWS = [
    ("F3-03-001", "Cargo por venta", 9500.0, 50000.0, "2026-06-01"),
    ("F3-03-002", "Cargo por venta", 5700.0, 30000.0, "2026-06-02"),
    ("F3-03-001", "Anulaci\u00f3n del cargo por venta", -9500.0, 50000.0, "2026-06-15"),
    ("F3-03-003", "Env\u00edo", 1500.0, 0.0, "2026-06-03"),
    ("F3-03-004", "Publicidad", 2000.0, 0.0, "2026-06-04"),
]

# Expected ledger rows in id_transaccion order (alphabetical).
# read_excel_auto strips header row (index 0), so iterrows starts at index 1.
# File is _f3_03_fixture.xlsx, so f.name = "_f3_03_fixture.xlsx".
EXPECTED_LEDGER = [
    ("CHG__f3_03_fixture.xlsx_4", "F3-03-003", "CARGO", -1500.0, "Env\u00edo"),
    ("CHG__f3_03_fixture.xlsx_5", "F3-03-004", "CARGO", -2000.0, "Publicidad"),
    ("COMM_F3-03-001__f3_03_fixture.xlsx_1", "F3-03-001", "EGRESO_COMISION", -9500.0, "Cargo por venta (Comisi\u00f3n)"),
    ("COMM_F3-03-002__f3_03_fixture.xlsx_2", "F3-03-002", "EGRESO_COMISION", -5700.0, "Cargo por venta (Comisi\u00f3n)"),
    ("REFUND_F3-03-001__f3_03_fixture.xlsx_3", "F3-03-001", "DEVOLUCION", -50000.0, "Devoluci\u00f3n de venta"),
    ("REVCOMM_F3-03-001__f3_03_fixture.xlsx_3", "F3-03-001", "AJUSTE", 9500.0, "Anulaci\u00f3n del cargo por venta"),
    ("SALE_F3-03-001__f3_03_fixture.xlsx_1", "F3-03-001", "INGRESO_VENTA", 50000.0, "Cargo por venta (Venta)"),
    ("SALE_F3-03-002__f3_03_fixture.xlsx_2", "F3-03-002", "INGRESO_VENTA", 30000.0, "Cargo por venta (Venta)"),
]

EXPECTED_TOTAL = sum(r[3] for r in EXPECTED_LEDGER)  # 20800.0
EXPECTED_VENTAS = ["F3-03-001", "F3-03-002"]

# ── helpers ──────────────────────────────────────────────
class Env:
    _orig_dir = None

    @classmethod
    def setup(cls):
        # Remove old temp dir completely
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
            gc.collect()
            if TEMP_DIR.exists():
                time.sleep(0.5)
                shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_RAW.mkdir(parents=True, exist_ok=True)

        # Copy baseline DB
        shutil.copy2(BASELINE, TEMP_DB)
        # Ensure temp DB is writable
        os.chmod(TEMP_DB, 0o644)

        # Create fixture XLSX
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(["Venta", "Detalle", "Valor del cargo", "Total de la venta", "Fecha"])
        for r in FIXTURE_ROWS:
            ws.append(list(r))
        wb.save(FIXTURE_FILE)
        cls.fixture_sha256 = hashlib.sha256(FIXTURE_FILE.read_bytes()).hexdigest()

        # Monkey-patch DIR_FACTURACION module variable to use temp directory
        import engine.v4.surgical_loader as sl_mod
        cls._orig_dir = sl_mod.DIR_FACTURACION
        sl_mod.DIR_FACTURACION = TEMP_RAW

    @classmethod
    def teardown(cls):
        # Restore original directory
        import engine.v4.surgical_loader as sl_mod
        if cls._orig_dir is not None:
            sl_mod.DIR_FACTURACION = cls._orig_dir
        # Reset DatabaseV4 singleton
        DatabaseV4.reset()
        DatabaseV4._instances = {}
        DatabaseV4._instance = None
        DatabaseV4._shutdown_registered = False
        # Remove temp dir
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)

    @classmethod
    def fresh_db(cls) -> DatabaseV4:
        DatabaseV4.reset()
        import gc; gc.collect()
        # Copy fresh baseline
        if TEMP_DB.exists():
            TEMP_DB.unlink()
        shutil.copy2(BASELINE, TEMP_DB)
        os.chmod(TEMP_DB, 0o644)
        db = DatabaseV4(db_path=str(TEMP_DB), read_only=False)
        db.conn.execute("SET enable_progress_bar=false;")
        db.is_read_only = False
        DatabaseV4._instance = db
        DatabaseV4._register_shutdown_hook()
        return db

async def run_pipeline() -> IngestionRecord:
    db = Env.fresh_db()
    registry = IngestionRegistry(db=db)
    orch = IngestionOrchestrator(db=db, registry=registry)
    record = await orch.run(
        file_path=str(FIXTURE_FILE),
        user="f3_03_test",
    )
    return record

def validate_ledger() -> dict:
    # Close any existing DatabaseV4 connection to avoid DuckDB lock conflicts
    DatabaseV4.reset()
    con = __import__("duckdb").connect(str(TEMP_DB), read_only=True)
    try:
        ledger = con.execute(
            "SELECT id_transaccion, id_orden, tipo_movimiento, monto, detalle "
            "FROM marketplace_ledger_v1 "
            "WHERE archivo_origen = '_f3_03_fixture.xlsx' "
            "ORDER BY id_transaccion"
        ).fetchall()
        ventas = con.execute(
            "SELECT order_id FROM ventas_marketplace "
            "WHERE source_file = '_f3_03_fixture.xlsx' "
            "ORDER BY order_id"
        ).fetchall()
        ledger_total = con.execute(
            "SELECT COALESCE(SUM(monto), 0) FROM marketplace_ledger_v1 "
            "WHERE archivo_origen = '_f3_03_fixture.xlsx'"
        ).fetchone()[0]
    finally:
        con.close()
    return {
        "ledger": ledger,
        "ventas": [r[0] for r in ventas],
        "ledger_total": round(float(ledger_total), 2),
    }

def compare(actual: dict) -> list:
    errors = []

    # Compare ledger rows
    act_ledger = actual["ledger"]
    exp_ledger = EXPECTED_LEDGER
    if len(act_ledger) != len(exp_ledger):
        errors.append(f"ledger row count: expected {len(exp_ledger)}, got {len(act_ledger)}")
    else:
        for i, (exp_id, exp_oid, exp_tipo, exp_monto, exp_det) in enumerate(exp_ledger):
            act = act_ledger[i]
            if act[0] != exp_id:
                errors.append(f"row[{i}] id_transaccion: expected '{exp_id}', got '{act[0]}'")
            if act[1] != exp_oid:
                errors.append(f"row[{i}] id_orden: expected '{exp_oid}', got '{act[1]}'")
            if act[2] != exp_tipo:
                errors.append(f"row[{i}] tipo_movimiento: expected '{exp_tipo}', got '{act[2]}'")
            if float(act[3]) != exp_monto:
                errors.append(f"row[{i}] monto: expected {exp_monto}, got {float(act[3])}")
            if act[4] != exp_det:
                errors.append(f"row[{i}] detalle: expected '{exp_det}', got '{act[4]}'")

    # Compare total
    if actual["ledger_total"] != EXPECTED_TOTAL:
        errors.append(f"ledger_total: expected {EXPECTED_TOTAL}, got {actual['ledger_total']}")

    # Compare ventas
    if actual["ventas"] != EXPECTED_VENTAS:
        errors.append(f"ventas: expected {EXPECTED_VENTAS}, got {actual['ventas']}")

    return errors
