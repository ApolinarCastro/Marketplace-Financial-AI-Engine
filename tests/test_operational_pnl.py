"""tests/test_operational_pnl.py
TDD: Verifica que se filtre correctamente el P&L operacional de Mercado Libre
de los eventos de riesgo/postventa/trazabilidad técnica sin afectar a otros marketplaces.
"""
from __future__ import annotations

import unittest
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine


class TestMarketplaceOperationalPNLFilter(unittest.TestCase):
    """Valida el comportamiento de la separación entre P&L operacional y de riesgo/postventa."""

    @classmethod
    def setUpClass(cls):
        DatabaseV4.reset()
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        DatabaseV4._instance = cls.db

        raw_data = [
            # Mercado Libre - Operacionales (Deben ser True)
            {"marketplace": "ML", "id_transaccion": "TX_ML_SALE", "id_orden": "O1",
             "fecha": "2026-05-01", "detalle": "Cargo por venta (Venta)",
             "monto": 120000.0, "tipo_movimiento": "credit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_ML_SHIPPING", "id_orden": "O1",
             "fecha": "2026-05-02", "detalle": "Cargo por envíos de Mercado Libre",
             "monto": -8500.0, "tipo_movimiento": "debit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_ML_ADS", "id_orden": "O1",
             "fecha": "2026-05-03", "detalle": "Cargo por campaña de publicidad - Product Ads",
             "monto": -3000.0, "tipo_movimiento": "debit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},

            # Mercado Libre - Exclusiones de Riesgo/Postventa (Deben ser False)
            {"marketplace": "ML", "id_transaccion": "TX_ML_DISPUTE", "id_orden": "O1",
             "fecha": "2026-05-04", "detalle": "reserve_for_dispute",
             "monto": -120000.0, "tipo_movimiento": "debit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_ML_MEDIACION", "id_orden": "O1",
             "fecha": "2026-05-05", "detalle": "Cancelación de la mediación",
             "monto": 15000.0, "tipo_movimiento": "credit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_ML_BPP", "id_orden": "O1",
             "fecha": "2026-05-06", "detalle": "bpp_refunded",
             "monto": -120000.0, "tipo_movimiento": "debit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_ML_REPENTANT", "id_orden": "O1",
             "fecha": "2026-05-07", "detalle": "repentant_buyer",
             "monto": -45000.0, "tipo_movimiento": "debit",
             "archivo_origen": "ml_test.xlsx", "folio_xml": None, "estado_xml": None},

            # París - Debe ser todo True (Sin importar si se clasifica como Ajuste, etc.)
            {"marketplace": "PARIS", "id_transaccion": "TX_PARIS_SALE", "id_orden": "OP1",
             "fecha": "2026-05-01", "detalle": "Venta",
             "monto": 80000.0, "tipo_movimiento": "credit",
             "archivo_origen": "p_test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "PARIS", "id_transaccion": "TX_PARIS_MERMA", "id_orden": "OP1",
             "fecha": "2026-05-02", "detalle": "Merma",
             "monto": -12000.0, "tipo_movimiento": "debit",
             "archivo_origen": "p_test.xlsx", "folio_xml": None, "estado_xml": None},
        ]
        cls.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.conn.close()
        except Exception:
            pass
        DatabaseV4.reset()

    def test_classification_assigns_operational_flag_correctly(self):
        """Verifica que el flag include_in_operational_pnl se asigne correctamente a cada registro."""
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()

        res = self.db.query(
            "SELECT id_transaccion, include_in_operational_pnl "
            "FROM marketplace_ledger_clasificado_v1"
        ).to_dict(orient="records")
        by_tx = {r["id_transaccion"]: bool(r["include_in_operational_pnl"]) for r in res}

        # ML Operacionales -> TRUE
        self.assertTrue(by_tx["TX_ML_SALE"])
        self.assertTrue(by_tx["TX_ML_SHIPPING"])
        self.assertTrue(by_tx["TX_ML_ADS"])

        # ML Exclusiones (Riesgo/Postventa/Mecanismos) -> FALSE
        self.assertFalse(by_tx["TX_ML_DISPUTE"])
        self.assertFalse(by_tx["TX_ML_MEDIACION"])
        self.assertFalse(by_tx["TX_ML_BPP"])

        # ML ROOT_EVENT real-cash -> FALSE (PHASE_16F: poscobro=operational traceability only)
        self.assertFalse(by_tx["TX_ML_REPENTANT"])

        # París -> Siempre TRUE (Sin importar la clasificación interna)
        self.assertTrue(by_tx["TX_PARIS_SALE"])
        self.assertTrue(by_tx["TX_PARIS_MERMA"])

    def test_database_views_are_created_and_filtered_properly(self):
        """Verifica que las vistas SQL operacionales y de riesgo existan y filtren correctamente."""
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()

        # Verificar vista operacional
        op_rows = self.db.query("SELECT id_transaccion FROM financial_operational_view_v1").to_dict(orient="records")
        op_ids = {r["id_transaccion"] for r in op_rows}
        
        self.assertIn("TX_ML_SALE", op_ids)
        self.assertIn("TX_ML_SHIPPING", op_ids)
        self.assertIn("TX_ML_ADS", op_ids)
        self.assertIn("TX_PARIS_SALE", op_ids)
        self.assertIn("TX_PARIS_MERMA", op_ids)

        # ML ROOT_EVENT real-cash now in risk view (PHASE_16F: poscobro=operational traceability only)
        self.assertNotIn("TX_ML_REPENTANT", op_ids)
        
        self.assertNotIn("TX_ML_DISPUTE", op_ids)
        self.assertNotIn("TX_ML_MEDIACION", op_ids)
        self.assertNotIn("TX_ML_BPP", op_ids)

        # Verificar vista de riesgo
        risk_rows = self.db.query("SELECT id_transaccion FROM risk_postsale_view_v1").to_dict(orient="records")
        risk_ids = {r["id_transaccion"] for r in risk_rows}

        self.assertIn("TX_ML_DISPUTE", risk_ids)
        self.assertIn("TX_ML_MEDIACION", risk_ids)
        self.assertIn("TX_ML_BPP", risk_ids)
        self.assertIn("TX_ML_REPENTANT", risk_ids)
        
        self.assertNotIn("TX_ML_SALE", risk_ids)
        self.assertNotIn("TX_PARIS_SALE", risk_ids)

    def test_financial_closing_aggregates_only_operational_pnl(self):
        """Verifica que el resultado neto del cierre mensual compute solo transacciones operacionales."""
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()

        close = auditor.run_financial_closing("ML", "2026-05-01", "2026-05-31")
        
        # Ingresos operacionales esperados: 120000.0 (Venta)
        # Costos operacionales esperados: -8500.0 (Envío)
        # Costos comerciales esperados: -3000.0 (Publicidad)
        # Resultado neto esperado (PHASE_16F: repentant_buyer excluded from operational P&L):
        # 120000.0 - 0.0 (devoluciones) - 8500.0 - 3000.0 + 0.0 (ajustes) = 108500.0
        self.assertEqual(close["ingresos"], 120000.0)
        self.assertEqual(close["costos_op"], -8500.0)
        self.assertEqual(close["costos_com"], -3000.0)
        self.assertEqual(close["ajustes"], 0.0)
        self.assertEqual(close["neto"], 108500.0)


if __name__ == "__main__":
    unittest.main()
