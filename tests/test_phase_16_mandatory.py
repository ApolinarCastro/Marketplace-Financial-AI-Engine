"""
Mandatory Phase 16 Execution Verification Tests
ADJ_01 through ADJ_05 aligned with Single Financial Truth principles.
"""
import unittest
import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

class TestPhase16MandatoryAdjustments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._old_instance = DatabaseV4._instance
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        cls.db.is_read_only = False
        DatabaseV4._instance = cls.db
        cls.auditor = MarketplaceAuditorEngine()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.close()
        except Exception:
            pass
        DatabaseV4._instance = cls._old_instance

    def test_ripley_001_duplicate_order_detection(self):
        """
        TEST_RIPLEY_001: Duplicate order detection between Importe del pedido, Precio total and Subtotal.
        An order present simultaneously in all three must produce exactly one SIGNAL contributor.
        """
        # Insert raw duplicate rows for a single order
        raw_data = [
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_EXCEL_101", "id_orden": "ORD_DUP_999",
             "fecha": "2026-06-01", "detalle": "Importe del pedido", "monto": 50000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "rip_test.xlsx", "folio_xml": "L1"},
            # In cycles (starts with RIP_CSV_)
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_CSV_L1_ORD_DUP_999_1_precio", "id_orden": "ORD_DUP_999",
             "fecha": "2026-06-01", "detalle": "Precio total", "monto": 50000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "cycles.csv", "folio_xml": "L1"},
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_CSV_L1_ORD_DUP_999_2_subtotal", "id_orden": "ORD_DUP_999",
             "fecha": "2026-06-01", "detalle": "Subtotal", "monto": 50000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "cycles.csv", "folio_xml": "L1"},
        ]
        self.db.execute("DELETE FROM marketplace_ledger_v1")
        self.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

        self.auditor.run_classification()

        res = self.db.query(
            "SELECT id_transaccion, include_in_operational_pnl FROM marketplace_ledger_clasificado_v1"
        )
        # Check that exactly one row has include_in_operational_pnl = True
        op_rows = res[res['include_in_operational_pnl'] == True]
        self.assertEqual(len(op_rows), 1, "Must produce exactly one SIGNAL contributor when duplicates overlap")
        self.assertEqual(op_rows.iloc[0]['id_transaccion'], "RIP_EXCEL_101", "Canonical Excel Importe del pedido must be the operational signal")

    def test_ripley_002_structure_vs_ledger_delta_zero(self):
        """
        TEST_RIPLEY_002: Financial Structure vs Ledger delta must equal 0.
        Verify that monthly closing net result equals sum of operational rows in classified ledger.
        """
        # Insert varied Ripley rows
        raw_data = [
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_EX_1", "id_orden": "ORD_1",
             "fecha": "2026-06-02", "detalle": "Importe del pedido", "monto": 100000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "rip_test.xlsx", "folio_xml": "L2"},
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_EX_2", "id_orden": "ORD_1",
             "fecha": "2026-06-02", "detalle": "Comisiones sobre pedidos", "monto": -12000.0,
             "tipo_movimiento": "CARGO", "archivo_origen": "rip_test.xlsx", "folio_xml": "L2"},
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_EX_3", "id_orden": "ORD_1",
             "fecha": "2026-06-02", "detalle": "Gastos de envío pagados por el operador", "monto": -8000.0,
             "tipo_movimiento": "CARGO", "archivo_origen": "rip_test.xlsx", "folio_xml": "L2"},
            # Non-operational Cycle rows
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_CSV_L2_ORD_1_com", "id_orden": "ORD_1",
             "fecha": "2026-06-02", "detalle": "Comisiones sobre pedidos", "monto": -12000.0,
             "tipo_movimiento": "CARGO", "archivo_origen": "cycles.csv", "folio_xml": "L2"},
        ]
        self.db.execute("DELETE FROM marketplace_ledger_v1")
        self.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

        self.auditor.run_classification()
        close = self.auditor.run_financial_closing("RIPLEY", "2026-06-01", "2026-06-30")

        # Sum of operational P&L ledger rows
        op_sum = float(self.db.query(
            "SELECT COALESCE(SUM(monto), 0) as sm FROM marketplace_ledger_clasificado_v1 WHERE include_in_operational_pnl = TRUE"
        ).iloc[0]['sm'])

        delta = abs(close['neto'] - op_sum)
        self.assertAlmostEqual(delta, 0.0, places=2, msg="Financial Structure vs Ledger delta must equal 0")

    def test_ripley_003_cycles_present_in_db_but_absent_from_operational_pnl(self):
        """
        TEST_RIPLEY_003: Cycles present in DB but absent from operational PnL.
        CICLOS (RIP_CSV_) and TH (RIP_TH_) records must be preserved but marked include_in_operational_pnl = False.
        """
        raw_data = [
            # Cycle record
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_CSV_F123_O321_precio", "id_orden": "O321",
             "fecha": "2026-06-05", "detalle": "Precio total", "monto": 45000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "cycles.csv", "folio_xml": "F123"},
            # TH record
            {"marketplace": "RIPLEY", "id_transaccion": "RIP_TH_555_venta", "id_orden": "O321",
             "fecha": "2026-06-05", "detalle": "Comisión", "monto": -3500.0,
             "tipo_movimiento": "CARGO", "archivo_origen": "th.csv", "folio_xml": "F123"},
        ]
        self.db.execute("DELETE FROM marketplace_ledger_v1")
        self.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

        self.auditor.run_classification()

        classified = self.db.query("SELECT id_transaccion, include_in_operational_pnl FROM marketplace_ledger_clasificado_v1")
        self.assertEqual(len(classified), 2, "Records must be preserved in DB for treasury and audits")
        for _, r in classified.iterrows():
            self.assertFalse(r['include_in_operational_pnl'], f"Record {r['id_transaccion']} must be excluded from operational PnL")

    def test_paris_001_revenue_source_transaction_value(self):
        """
        TEST_PARIS_001: Revenue source must be transaction value, not settlement value.
        Gross revenue rows must capture the raw gross transaction value (before commission).
        """
        # Paris loader parses raw rows and splits gross/commission.
        # Let's insert a simulated gross record with _GROSS suffix and verify it.
        raw_data = [
            # Venta gross (originating from transaction amount)
            {"marketplace": "PARIS", "id_transaccion": "PARIS_TX_123_GROSS", "id_orden": "PO_456",
             "fecha": "2026-06-10", "detalle": "Venta", "monto": 120000.0,
             "tipo_movimiento": "PAGO", "archivo_origen": "paris_raw.xlsx", "folio_xml": None},
            # Commission (originating from difference)
            {"marketplace": "PARIS", "id_transaccion": "PARIS_TX_123_COMM", "id_orden": "PO_456",
             "fecha": "2026-06-10", "detalle": "Cargo por venta (Comisión)", "monto": -18000.0,
             "tipo_movimiento": "EGRESO_COMISION", "archivo_origen": "paris_raw.xlsx", "folio_xml": None},
        ]
        self.db.execute("DELETE FROM marketplace_ledger_v1")
        self.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

        self.auditor.run_classification()
        close = self.auditor.run_financial_closing("PARIS", "2026-06-01", "2026-06-30")

        # Revenue should equal exactly 120,000.0 (transaction amount before commission), NOT 102,000.0 (settlement amount)
        self.assertEqual(close["ingresos"], 120000.0, "Revenue must match transaction amount")
        self.assertEqual(close["costos_com"], -18000.0, "Commissions must match split value")
        self.assertEqual(close["neto"], 102000.0, "Net closing should combine gross and commission correctly")

if __name__ == "__main__":
    unittest.main()
