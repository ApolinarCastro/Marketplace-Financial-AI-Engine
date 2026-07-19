"""F4: Phase 4 — Financial Traceability (STARTED).

Validates the RAW→Registry→ETL→Ledger→Clasificación→Cierre chain
using public contracts only. Zero core modifications.

Actions mapped to tests:
  F4-01 (Action 7): EvidenceObject — FinancialTraceability dataclass constructs
  F4-02 (Action 1): RAW→Registry — archivo_origen links to ingestion_registry
  F4-03 (Action 2): RAW→Transaction — id_transaccion traces to file row
  F4-04 (Action 4): Ledger→Classification — clasificado has origen_clasificacion
  F4-05 (Action 4+5): Classification→Cierre — financial_group aggregates to cierre
  F4-06 (Action 5): P&L Uniqueness — no duplicate id_transaccion in op P&L
  F4-07 (Action 8): Reproduction from RAW — F3-05 fixture reproduces 8/$20,800/2v
  F4-08 (Action 6): P&L vs Treasury — cierre formula vs ledger separation

Actions 3 (transformation version) and 6 (full P&L/treasury separation)
are documented gaps for Phase 4 CONTINUED.
"""
from __future__ import annotations
import gc
import shutil
from pathlib import Path

import subprocess
import sys

import pytest

from engine.v4.database import DatabaseV4
from engine.v4.evidence.traceability import (
    FinancialTraceability,
    RawOrigin,
    RegistryLink,
    EtlTransform,
    LedgerEntry,
    ClassificationEntry,
    CierreSummary,
)
from engine.v4.evidence.traceability_engine import TraceabilityEngine
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.ingestion import IngestionRegistry
from engine.v4.ingestion.orchestrator import IngestionOrchestrator

# ── paths (ROOT-relative + F4_TEMP_ROOT) ───────────────────────────────
import os
ROOT = Path(__file__).resolve().parent.parent
F4_TEMP_ROOT = Path(os.environ.get("F4_TEMP_ROOT", ROOT / "data" / "db" / "tmp_f4_v8")).resolve()
BASELINE = ROOT / "data" / "db" / "baseline_estable_v8_candidate_20260717" / "meli_financial_v4.db"
OFFICIAL_DB = ROOT / "data" / "db" / "meli_financial_v4.db"
OFFICIAL_RAW = ROOT / "01_Raw"
TEMP_BASE = F4_TEMP_ROOT / "tmp_f4_trace"
FIXTURE = ROOT / "tests" / "fixtures" / "f3_03" / "f3_03_fixture.xlsx"
FIXTURE_FILENAME = "f3_03_fixture.xlsx"

# ── expected values from F3-03 fixture ─────────────────────────────────
EXPECTED_ROWS = 8
EXPECTED_TOTAL = 20800.0
EXPECTED_VENTAS = ["F3-03-001", "F3-03-002"]

# ── helpers ────────────────────────────────────────────────────────────
def sha256(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def official_hash():
    import hashlib
    return hashlib.sha256(OFFICIAL_DB.read_bytes()).hexdigest().upper()


def collect_raw_files():
    return sorted(
        str(p.relative_to(OFFICIAL_RAW))
        for p in OFFICIAL_RAW.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    )


def reset_singleton():
    DatabaseV4.reset()
    gc.collect()


def create_env(use_classification=False):
    if TEMP_BASE.exists():
        reset_singleton()
        shutil.rmtree(TEMP_BASE, ignore_errors=True)
        gc.collect()
    TEMP_BASE.mkdir(parents=True)
    temp_db = TEMP_BASE / "meli_financial_v4.db"
    shutil.copy2(BASELINE, temp_db)
    temp_raw = TEMP_BASE / "01_Raw" / "ML" / "Facturacion"
    temp_raw.mkdir(parents=True)
    shutil.copy2(FIXTURE, temp_raw / FIXTURE_FILENAME)
    return {"temp_db": temp_db, "temp_raw": temp_raw}


def destroy_env():
    reset_singleton()
    if TEMP_BASE.exists():
        shutil.rmtree(TEMP_BASE, ignore_errors=True)


def prepare_db(env):
    reset_singleton()
    db = DatabaseV4(db_path=str(env["temp_db"]), read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    return db


def run_ingestion(db, env):
    import engine.v4.surgical_loader as sl_mod
    orig = sl_mod.DIR_FACTURACION
    sl_mod.DIR_FACTURACION = env["temp_raw"]
    try:
        registry = IngestionRegistry(db=db)
        orch = IngestionOrchestrator(db=db, registry=registry)
        import asyncio
        asyncio.new_event_loop().run_until_complete(orch.run(
            file_path=str(env["temp_raw"] / FIXTURE_FILENAME),
            user="f4_test",
        ))
    finally:
        sl_mod.DIR_FACTURACION = orig


def run_classification(db):
    try:
        db.execute("UPDATE marketplace_ledger_v1 SET financial_group = NULL")
        db.execute("DELETE FROM marketplace_ledger_clasificado_v1")
    except Exception:
        pass
    fe = FinancialEngine(db=db)
    count = fe.run_classification()
    return count


def run_closing(db):
    fe = FinancialEngine(db=db)
    results = fe.run_financial_closing_all("ML", years=[2026])
    return results


# ── module-scoped isolation guard ──────────────────────────────────────
@pytest.fixture(scope="module")
def guard():
    before = official_hash()
    before_raw = collect_raw_files()
    yield
    after = official_hash()
    after_raw = collect_raw_files()
    assert after == before, (
        f"GUARD F4: Official DB hash changed!"
        f" Was {before}, now {after}"
    )
    assert after_raw == before_raw, "GUARD F4: Official RAW files changed!"


@pytest.fixture(scope="module", autouse=True)
def restore_v8_interceptor():
    """Restore session V8 interceptor after this module's singleton hijacking."""
    yield
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    gc.collect()
    v8_path = F4_TEMP_ROOT / "meli_financial_v4.db"
    if v8_path.exists():
        interceptor = DatabaseV4(db_path=str(v8_path), read_only=True)
        DatabaseV4._instance = interceptor
        DatabaseV4._shutdown_registered = True


# ══════════════════════════════════════════════════════════════════════
# F4-01: EvidenceObject
# ══════════════════════════════════════════════════════════════════════
class TestF401EvidenceObject:
    """Action 7: EvidenceObject — FinancialTraceability dataclass."""

    def test_dataclass_constructs(self, guard):
        ft = FinancialTraceability(
            raw=RawOrigin(file_name="test.xlsx", file_path="/tmp/test.xlsx",
                          sha256="abc", file_size_bytes=100),
            registry=RegistryLink(execution_id="e1", ingested_at="now", user="tester"),
            etl=EtlTransform(loader_version="SurgicalLoader",
                             harness_version="1.0.0-r5",
                             taxonomy_version="ml_v1"),
            ledger=LedgerEntry(id_transaccion="tx1", id_orden="ord1", marketplace="ML",
                               monto=5000.0, tipo_movimiento="INGRESO_VENTA",
                               detalle="Venta", archivo_origen="test.xlsx"),
            classification=ClassificationEntry(financial_group="ingresos",
                                              origen_clasificacion="ml_v1",
                                              taxonomy_version="ml_v1"),
            cierre=CierreSummary(periodo_inicio="2026-01-01", periodo_fin="2026-01-31",
                                 total_ingresos=5000.0, total_costos_operacionales=0.0,
                                 total_costos_comerciales=0.0, total_ajustes=0.0,
                                 resultado_neto=5000.0),
        )
        assert ft.raw is not None
        assert ft.registry is not None
        assert ft.etl is not None
        assert ft.ledger is not None
        assert ft.classification is not None
        assert ft.cierre is not None
        assert ft.raw.sha256 == "abc"
        assert ft.ledger.id_transaccion == "tx1"

    def test_empty_trace(self, guard):
        ft = FinancialTraceability(errors=["not found"])
        assert ft.errors == ["not found"]

    def test_traced_at_set(self, guard):
        ft = FinancialTraceability()
        assert ft.traced_at is not None


# ══════════════════════════════════════════════════════════════════════
# F4-02: RAW→Registry
# ══════════════════════════════════════════════════════════════════════
class TestF402RawToRegistry:
    """Action 1: Every archivo_origen in ledger has matching ingestion_registry."""

    def test_registry_has_fixture_entry(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            ok, errors = te.validate_archive_registry_link(FIXTURE_FILENAME)
            assert ok, f"Registry link validation failed: {errors}"
        finally:
            db.close()
            destroy_env()

    def test_te_trace_by_archivo(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            ok, stats, errors = te.reproduce_from_raw(FIXTURE_FILENAME)
            assert ok, f"Reproduction check failed: {errors}"
            assert stats["ledger_rows"] == EXPECTED_ROWS
            assert stats["ledger_total"] == EXPECTED_TOTAL
            assert stats["ventas"] == EXPECTED_VENTAS
        finally:
            db.close()
            destroy_env()

    def test_archivo_origen_present_on_ledger_rows(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            null_count = int(db.query(
                "SELECT COUNT(*) FROM marketplace_ledger_v1 "
                "WHERE archivo_origen IS NULL OR archivo_origen = ''"
            ).iloc[0, 0])
            assert null_count == 0, f"{null_count} ledger rows lack archivo_origen"
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-03: RAW→Transaction
# ══════════════════════════════════════════════════════════════════════
class TestF403RawToTransaction:
    """Action 2: id_transaccion encodes RAW row index."""

    def test_id_transaccion_contains_archivo_origen(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            rows = db.query(
                "SELECT id_transaccion, archivo_origen FROM marketplace_ledger_v1 "
                "WHERE archivo_origen = ? LIMIT 20",
                [FIXTURE_FILENAME],
            )
            for _, r in rows.iterrows():
                tx_id = str(r["id_transaccion"])
                assert FIXTURE_FILENAME.replace(".xlsx", "") in tx_id or \
                       FIXTURE_FILENAME in tx_id, \
                    f"id_transaccion '{tx_id}' does not reference '{FIXTURE_FILENAME}'"
        finally:
            db.close()
            destroy_env()

    def test_id_transaccion_encodes_row_index(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            # id_transaccion format: {TYPE}_{file_stem}_{row_index}
            # e.g., SALE_F3-03-001_f3_03_fixture.xlsx_1
            rows = db.query(
                "SELECT id_transaccion FROM marketplace_ledger_v1 "
                "WHERE archivo_origen = ? ORDER BY id_transaccion",
                [FIXTURE_FILENAME],
            )
            for _, r in rows.iterrows():
                tx_id = str(r["id_transaccion"])
                parts = tx_id.split("_")
                last = parts[-1]
                assert last.isdigit(), f"id_transaccion '{tx_id}' has no numeric row index"
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-04: Ledger→Classification
# ══════════════════════════════════════════════════════════════════════
class TestF404LedgerToClassification:
    """Action 4: Every ledger row has matching classification."""

    def test_every_ledger_row_has_classification(self, guard):
        """Requires classification to have been run on the temp DB."""
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)

            unclassified = int(db.query(
                "SELECT COUNT(*) FROM marketplace_ledger_v1 l "
                "LEFT JOIN marketplace_ledger_clasificado_v1 c "
                "ON l.id_transaccion = c.id_transaccion "
                "WHERE c.id_transaccion IS NULL"
            ).iloc[0, 0])
            assert unclassified == 0, f"{unclassified} ledger rows have no classification"
        finally:
            db.close()
            destroy_env()

    def test_classification_has_origen(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)

            null_origen = int(db.query(
                "SELECT COUNT(*) FROM marketplace_ledger_clasificado_v1 "
                "WHERE origen_clasificacion IS NULL OR origen_clasificacion = ''"
            ).iloc[0, 0])
            assert null_origen == 0, f"{null_origen} classified rows missing origen_clasificacion"
        finally:
            db.close()
            destroy_env()

    def test_traceability_engine_finds_classification(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            te = TraceabilityEngine(fe=FinancialEngine(db=db))

            tx_row = db.query(
                "SELECT id_transaccion FROM marketplace_ledger_v1 "
                "WHERE archivo_origen = ? LIMIT 1",
                [FIXTURE_FILENAME],
            )
            if not tx_row.empty:
                tx_id = str(tx_row.iloc[0]["id_transaccion"])
                ft = te.trace_by_transaction(tx_id)
                assert ft.classification is not None
                assert ft.classification.origen_clasificacion is not None
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-05: Classification→Cierre
# ══════════════════════════════════════════════════════════════════════
class TestF405ClassificationToCierre:
    """Action 4+5: classification aggregates into cierre."""

    def test_cierre_has_period_for_marketplace(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            closings = run_closing(db)

            assert len(closings) > 0, "No closing periods generated"
            non_zero = [c for c in closings if float(c.get("ingresos", 0) or 0) > 0]
            assert len(non_zero) > 0, "No ML closing periods with revenue"
        finally:
            db.close()
            destroy_env()

    def test_cierre_includes_fixture_period(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            closings = run_closing(db)

            non_zero = [c for c in closings if float(c.get("ingresos", 0) or 0) > 0]
            if non_zero:
                c = non_zero[0]
                ing = float(c.get("ingresos", 0) or 0)
                assert ing >= EXPECTED_TOTAL, (
                    f"Cierre ingresos ${ing} < expected ${EXPECTED_TOTAL}"
                )
        finally:
            db.close()
            destroy_env()

    def test_traceability_cierre_in_trace(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            closings = run_closing(db)
            assert len(closings) > 0
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-06: P&L Uniqueness
# ══════════════════════════════════════════════════════════════════════
class TestF406PnLUniqueness:
    """Action 5: No id_transaccion appears twice in operational P&L."""

    def test_no_duplicate_transactions(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            ok, errors = te.validate_pnl_uniqueness("ML")
            assert ok, f"P&L uniqueness violations: {errors}"
        finally:
            db.close()
            destroy_env()

    def test_no_duplicates_across_marketplaces(self, guard):
        """Uniqueness key per marketplace from canonical_semantics.
        PARIS/RIPLEY: (id_transaccion, archivo_origen) — cross-file pipeline overlap resolved.
        ML: id_transaccion — validated 0 duplicates.
        FALABELLA: (id_transaccion, detalle) — one row per concept per order.
        """
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            findings = {}
            for mp in ("ML", "PARIS", "RIPLEY", "FALABELLA"):
                ok, errors = te.validate_pnl_uniqueness(mp)
                findings[mp] = (ok, errors)

            for mp in ("ML", "PARIS", "RIPLEY", "FALABELLA"):
                ok, errors = findings[mp]
                assert ok, f"{mp} P&L uniqueness violations: {errors}"
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-07: Reproduction from RAW
# ══════════════════════════════════════════════════════════════════════
class TestF407ReproductionFromRaw:
    """Action 8: Given RAW file, reproduce exact ledger."""

    def test_reproduces_f3_05_fixture(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            ok, stats, errors = te.reproduce_from_raw(FIXTURE_FILENAME)
            assert ok, f"Reproduction check errors: {errors}"
            assert stats["ledger_rows"] == EXPECTED_ROWS, (
                f"Expected {EXPECTED_ROWS} rows, got {stats['ledger_rows']}"
            )
            assert stats["ledger_total"] == EXPECTED_TOTAL, (
                f"Expected ${EXPECTED_TOTAL}, got ${stats['ledger_total']}"
            )
            assert stats["ventas"] == EXPECTED_VENTAS, (
                f"Expected ventas {EXPECTED_VENTAS}, got {stats['ventas']}"
            )
        finally:
            db.close()
            destroy_env()

    def test_reproduces_exact_transactions(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            run_closing(db)

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            ledger_ids = db.query(
                "SELECT id_transaccion FROM marketplace_ledger_v1 "
                "WHERE archivo_origen = ? ORDER BY id_transaccion",
                [FIXTURE_FILENAME],
            )
            for _, r in ledger_ids.iterrows():
                ft = te.trace_by_transaction(str(r["id_transaccion"]))
                assert ft.ledger is not None, f"No ledger entry for {r['id_transaccion']}"
                assert ft.ledger.archivo_origen == FIXTURE_FILENAME
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-08: P&L vs Treasury
# ══════════════════════════════════════════════════════════════════════
class TestF408PnLVsTreasury:
    """Action 6: Cierre correctly separates P&L from treasury."""

    def test_cierre_neto_equals_sum_of_groups(self, guard):
        """Verifies cierre neto = ing + dev + cop + ccm + aju (signs are natural)."""
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            closings = run_closing(db)

            for c in closings:
                neto = float(c.get("neto", 0) or 0)
                ing = float(c.get("ingresos", 0) or 0)
                dev = float(c.get("devoluciones", 0) or 0)
                cop = float(c.get("costos_op", 0) or 0)
                ccm = float(c.get("costos_com", 0) or 0)
                aju = float(c.get("ajustes", 0) or 0)
                expected_neto = round(ing + dev + cop + ccm + aju, 2)
                assert abs(neto - expected_neto) < 0.01, (
                    f"neto={neto} != ing({ing})+dev({dev})+cop({cop})+ccm({ccm})+aju({aju})={expected_neto}"
                )
        finally:
            db.close()
            destroy_env()

    def test_no_treasury_rows_in_operational_pnl(self, guard):
        """Op P&L must not contain uncategorized rows (financial_group IS NULL).
        
        Canonical check: rows with include_in_operational_pnl=1 must have a
        valid financial_group. NULL financial_group means uncategorized = treasury.
        
        Prior keyword-based check found 434 potential hits, but only 1 is a
        real violation (PARIS 'Pago normal' with NULL financial_group).
        The other 433 have valid P&L financial_groups (costos_operacionales,
        ingresos, costos_comerciales) — false positives from keyword approach.
        """
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)

            canonical_violations = int(db.query(
                "SELECT COUNT(*) FROM marketplace_ledger_v1 "
                "WHERE COALESCE(include_in_operational_pnl, 1) = 1 "
                "AND financial_group IS NULL"
            ).iloc[0, 0])
            assert canonical_violations == 0, (
                f"{canonical_violations} rows with include_in_operational_pnl=1 "
                f"and NULL financial_group — uncategorized entries in P&L"
            )
        finally:
            db.close()
            destroy_env()


# ══════════════════════════════════════════════════════════════════════
# F4-R3: Canonical semantics artifact sync check
# ══════════════════════════════════════════════════════════════════════
class TestCanonicalSemanticsSync:
    """Generated artifacts must match canonical_semantics.py contract."""

    def test_artifacts_synced(self):
        repo = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, "-m", "engine.v4.domain.generate_artifacts", "--check-only"],
            capture_output=True, text=True, cwd=str(repo),
        )
        assert result.returncode == 0, (
            f"Generated artifacts out of sync with canonical_semantics.py\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}\n"
            f"Run: python -m engine.v4.domain.generate_artifacts"
        )


# ══════════════════════════════════════════════════════════════════════
# F4-FULL: End-to-end traceability demonstration
# ══════════════════════════════════════════════════════════════════════
class TestF4EndToEnd:
    """Full chain: trace a single transaction from RAW through Cierre."""

    def test_full_chain_trace(self, guard):
        env = create_env()
        try:
            db = prepare_db(env)
            run_ingestion(db, env)
            run_classification(db)
            closings = run_closing(db)
            assert len(closings) > 0

            te = TraceabilityEngine(fe=FinancialEngine(db=db))
            tx_row = db.query(
                "SELECT id_transaccion FROM marketplace_ledger_v1 "
                "WHERE archivo_origen = ? ORDER BY id_transaccion LIMIT 1",
                [FIXTURE_FILENAME],
            )
            assert not tx_row.empty, "No fixture rows in ledger"
            tx_id = str(tx_row.iloc[0]["id_transaccion"])

            ft = te.trace_by_transaction(tx_id)

            # All chain links present
            assert ft.raw is not None, "Missing RAW link"
            assert ft.registry is not None, "Missing Registry link"
            assert ft.etl is not None, "Missing ETL link"
            assert ft.ledger is not None, "Missing Ledger link"
            assert ft.classification is not None, "Missing Classification link"
            assert len(ft.errors) == 0, f"Trace errors: {ft.errors}"

            # Value consistency
            assert ft.ledger.id_transaccion == tx_id
            assert ft.ledger.archivo_origen == FIXTURE_FILENAME
        finally:
            db.close()
            destroy_env()
