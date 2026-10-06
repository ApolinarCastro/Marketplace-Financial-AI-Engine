"""Reconciliation Level 1 vs Level 3 treasury scope contract (ML).

Regression test for PFO-FA005-L1-TREASURY-RCA-001.

A financially valid treasury row (financial_group='tesoreria',
include_in_operational_pnl=FALSE, mirroring operational P&L) must NOT
raise UNEXPECTED_GROUP:tesoreria in Level 1, while Level 3 mirror holds.

All tests use isolated tmp_path databases. No production state touched.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.v4.database import DatabaseV4
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine


def _seed(db: DatabaseV4, treasury_monto: float) -> None:
    """Seed operational P&L (+20800) + one treasury row + operational cierre."""
    db.execute(
        "INSERT INTO marketplace_ledger_clasificado_v1 (marketplace, "
        "id_transaccion, id_orden, detalle, tipo_movimiento, monto, fecha, "
        "clasificacion_operativa, include_in_operational_pnl, financial_group) VALUES "
        "('ML', 'T1', 'O1', 'Cargo por venta (Venta)', 'INGRESO_VENTA', 80000.0, "
        "'2026-06-01', 'Cargo por venta (Venta)', TRUE, 'ingresos'),"
        "('ML', 'T2', 'O1', 'Cargo por venta (Comisión)', 'EGRESO_COMISION', -15200.0, "
        "'2026-06-01', 'Cargo por venta (Comisión)', TRUE, 'costos_comerciales'),"
        "('ML', 'T3', 'O1', 'Devolución de venta', 'DEVOLUCION', -50000.0, "
        "'2026-06-15', 'Devolución de venta', TRUE, 'devoluciones'),"
        "('ML', 'T4', 'O1', 'Anulación del cargo por venta', 'AJUSTE', 9500.0, "
        "'2026-06-15', 'Anulación del cargo por venta', TRUE, 'ajustes'),"
        "('ML', 'T5', 'O2', 'Envío', 'CARGO', -1500.0, "
        "'2026-06-03', 'Envío', TRUE, 'costos_operacionales'),"
        "('ML', 'T6', 'O2', 'Publicidad', 'CARGO', -2000.0, "
        "'2026-06-04', 'Publicidad', TRUE, 'costos_operacionales'),"
        f"('ML', 'T7', 'TES-001', 'Retiro de dinero', 'CARGO', {treasury_monto}, "
        "'2026-06-20', 'Retiro de dinero', FALSE, 'tesoreria')"
    )
    db.execute(
        "INSERT INTO marketplace_cierre_financiero_v1 (marketplace, periodo_inicio, "
        "periodo_fin, total_ingresos, total_costos_operacionales, "
        "total_costos_comerciales, total_ajustes, resultado_neto) VALUES "
        "('ML', '2026-06-01', '2026-06-30', 80000.0, -3500.0, -15200.0, -40500.0, 20800.0)"
    )


def _fresh_engine(tmp_path: Path, treasury_monto: float) -> ReconciliationEngine:
    db = DatabaseV4(db_path=str(tmp_path / "rca.db"), read_only=False)
    _seed(db, treasury_monto)
    return ReconciliationEngine(db=db)


def test_level1_passes_with_valid_treasury_mirror(tmp_path: Path):
    """Operational +20800 with treasury -20800: L1 PASS/delta 0, L3 PASS/delta 0."""
    eng = _fresh_engine(tmp_path, -20800.0)
    try:
        l1 = eng._level_1_internal("ML", "2026-06-01", "2026-06-30", "Jun 2026")
        assert l1.status == "PASS", f"alerts: {[(a.rule, a.impact_amount) for a in l1.alerts]}"
        assert l1.delta == 0.0
        assert l1.alerts == []
        assert not any("tesoreria" in a.rule for a in l1.alerts)

        l2 = eng._level_2_operational("ML", "2026-06-01", "2026-06-30", "Jun 2026")
        assert l2.status == "PASS"
        l3 = eng._level_3_treasury(
            "ML", "2026-06-01", "2026-06-30", "Jun 2026", l2.source_total)
        assert l3.status == "PASS"
        assert l3.delta == 0.0
    finally:
        eng.db.close()


def test_level3_alerts_on_broken_treasury_mirror(tmp_path: Path):
    """Operational +20800 with treasury -15000: L3 ALERTA/delta 5800; L1 still PASS."""
    eng = _fresh_engine(tmp_path, -15000.0)
    try:
        l1 = eng._level_1_internal("ML", "2026-06-01", "2026-06-30", "Jun 2026")
        assert l1.status == "PASS", f"alerts: {[(a.rule, a.impact_amount) for a in l1.alerts]}"

        l2 = eng._level_2_operational("ML", "2026-06-01", "2026-06-30", "Jun 2026")
        l3 = eng._level_3_treasury(
            "ML", "2026-06-01", "2026-06-30", "Jun 2026", l2.source_total)
        assert l3.status == "ALERTA"
        assert l3.delta == 5800.0
    finally:
        eng.db.close()
