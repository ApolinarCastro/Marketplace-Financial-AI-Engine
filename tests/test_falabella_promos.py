"""tests/test_falabella_promos.py
TDD: Verifica que los nuevos conceptos de aportes promocionales de Falabella
se clasifiquen como costos comerciales en el cierre mensual.
"""
from __future__ import annotations

import unittest
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import (
    MarketplaceAuditorEngine,
)


class TestFalabellaPromosClassification(unittest.TestCase):
    """Valida la clasificación de cada concepto promocional nuevo de Falabella."""

    @classmethod
    def setUpClass(cls):
        DatabaseV4.reset()
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        DatabaseV4._instance = cls.db

        raw_data = [
            # Pago de aporte promocionales a cliente (Promo)
            {"marketplace": "FALABELLA", "id_transaccion": "TX_PAGO_PROMO", "id_orden": "O1",
             "fecha": "2026-03-01", "detalle": "Pago de aporte promocionales a cliente (Promo)",
             "monto": -15000.0, "tipo_movimiento": "debit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Descuento por aportes promocionales a clientes (Promo)
            {"marketplace": "FALABELLA", "id_transaccion": "TX_DESC_PROMO", "id_orden": "O2",
             "fecha": "2026-03-02", "detalle": "Descuento por aportes promocionales a clientes (Promo)",
             "monto": -5000.0, "tipo_movimiento": "debit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
        ]
        cls.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.conn.close()
        except Exception:
            pass
        DatabaseV4.reset()

    def test_promo_concepts_classified_correctly(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        
        res = self.db.query(
            "SELECT id_transaccion, clasificacion_operativa "
            "FROM marketplace_ledger_clasificado_v1 "
            "WHERE id_transaccion IN ('TX_PAGO_PROMO', 'TX_DESC_PROMO')"
        ).to_dict(orient="records")
        by_tx = {r["id_transaccion"]: r["clasificacion_operativa"] for r in res}

        self.assertEqual(by_tx["TX_PAGO_PROMO"], "Pago de aporte promocionales a cliente (Promo)")
        self.assertEqual(by_tx["TX_DESC_PROMO"], "Descuento por aportes promocionales a clientes (Promo)")

    def test_promo_concepts_consolidated_as_commercial_costs(self):
        # Insert a base sale so we have some positive revenue too
        sale_data = [
            {"marketplace": "FALABELLA", "id_transaccion": "TX_SALE", "id_orden": "O0",
             "fecha": "2026-03-10", "detalle": "Cobro por comisión por venta",
             "monto": 100000.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
        ]
        self.db.insert_df(pd.DataFrame(sale_data), "marketplace_ledger_v1")
        
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        
        close = auditor.run_financial_closing("FALABELLA", "2026-03-01", "2026-03-31")

        # The promos must be in commercial costs (costos_comerciales)
        # Expected: -15000 + -5000 + 100000 (commission sale) = 80000.0
        self.assertEqual(close["costos_com_net"] if "costos_com_net" in close else close["costos_com"], 80000.0)


if __name__ == "__main__":
    unittest.main()
