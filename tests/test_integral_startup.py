from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine


def test_scoped_classification_changes_only_requested_transaction(tmp_path):
    db = DatabaseV4(tmp_path / "scoped.duckdb", read_only=False)
    db.execute("INSERT INTO marketplace_ledger_v1 (marketplace,id_transaccion,id_orden,fecha,detalle,monto,tipo_movimiento,archivo_origen) VALUES ('ML','OLD','O0','2026-01-01','Cargo por venta (Venta)',1000,'INGRESO','old.xlsx')")
    db.execute("INSERT INTO marketplace_ledger_v1 (marketplace,id_transaccion,id_orden,fecha,detalle,monto,tipo_movimiento,archivo_origen) VALUES ('ML','TARGET','O1','2026-07-01',?,-3150,'CARGO','fixture.xlsx')", ['Cargo por env\u00edos de Mercado Libre'])
    db.execute("INSERT INTO marketplace_ledger_clasificado_v1 (marketplace,id_transaccion,id_orden,detalle,tipo_movimiento,monto,fecha,clasificacion_operativa,confianza_clasificacion,origen_clasificacion,include_in_operational_pnl,financial_group) VALUES ('ML','OLD','O0','Cargo por venta (Venta)','INGRESO',1000,'2026-01-01','Cargo por venta (Venta)',1,'atomic_match',true,'ingresos')")

    count = MarketplaceAuditorEngine(db=db).run_classification_for_transaction("TARGET")

    assert count == 1
    assert db.query("SELECT COUNT(*) n FROM marketplace_ledger_clasificado_v1 WHERE id_transaccion='OLD'").iloc[0].n == 1
    row = db.query("SELECT * FROM marketplace_ledger_clasificado_v1 WHERE id_transaccion='TARGET'").iloc[0]
    assert row.financial_group == "costos_operacionales"
    assert bool(row.include_in_operational_pnl) is True
    assert row.origen_clasificacion == "atomic_match"
    db.close()


def test_copilot_top_transactions_respects_explicit_period(tmp_path):
    from engine.v4.copilot.copilot_engine import CopilotEngine
    db = DatabaseV4(tmp_path / "copilot.duckdb", read_only=False)
    db.execute("INSERT INTO marketplace_ledger_v1 (marketplace,id_transaccion,id_orden,fecha,detalle,monto,tipo_movimiento,archivo_origen,financial_group,include_in_operational_pnl) VALUES ('ML','JULY','O1','2026-07-01','Cargo por envíos de Mercado Libre',-3150,'CARGO','fixture.xlsx','costos_operacionales',true)")
    db.execute("INSERT INTO marketplace_cierre_financiero_v1 (marketplace,periodo_inicio,periodo_fin,resultado_neto) VALUES ('ML','2026-06-01','2026-06-30',1)")
    result = CopilotEngine(db=db).ask("top_transactions", marketplace="ML", periodo="2026-07")
    assert result["breakdown"][0]["id_transaccion"] == "JULY"
    db.close()
