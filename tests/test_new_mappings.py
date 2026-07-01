"""tests/test_new_mappings.py
TDD RED: Verifica que los conceptos recién descubiertos
(fee_for_divergence_in_package_dimensions, Cancelación de la mediación,
cashback, cashback_cancel) se clasifiquen correctamente y se consoliden
en el cierre mensual de ventas.
"""
from __future__ import annotations

import unittest
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import (
    MarketplaceAuditorEngine,
)


class TestNewMappingsClassification(unittest.TestCase):
    """Valida la clasificación atómica de cada concepto nuevo."""

    @classmethod
    def setUpClass(cls):
        DatabaseV4.reset()
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        DatabaseV4._instance = cls.db

        raw_data = [
            # fee_for_divergence → Cargo por diferencias en las medidas y el peso del paquete (costos_operacionales)
            {"marketplace": "ML", "id_transaccion": "TX_DIVERG", "id_orden": "O1",
             "fecha": "2026-03-01", "detalle": "fee_for_divergence_in_package_dimensions",
             "monto": -72241.0, "tipo_movimiento": "debit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Cancelación de la mediación (variante con acentos)
            {"marketplace": "ML", "id_transaccion": "TX_MEDIACION", "id_orden": "O2",
             "fecha": "2026-03-02", "detalle": "Cancelación de la mediación",
             "monto": 18331.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Cancelacion de la mediacion (sin acentos)
            {"marketplace": "ML", "id_transaccion": "TX_MEDIACION_ACC", "id_orden": "O3",
             "fecha": "2026-03-03", "detalle": "Cancelacion de la mediacion",
             "monto": 18331.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Cancelacin de la mediacin (glitch de codificación detectado en DB real)
            {"marketplace": "ML", "id_transaccion": "TX_MEDIACION_GLITCH", "id_orden": "O3_G",
             "fecha": "2026-03-03", "detalle": "Cancelacin de la mediacin",
             "monto": 18331.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # cashback
            {"marketplace": "ML", "id_transaccion": "TX_CASHBACK", "id_orden": "O4",
             "fecha": "2026-03-04", "detalle": "cashback",
             "monto": 14855.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # cashback_cancel
            {"marketplace": "ML", "id_transaccion": "TX_CASHBACK_CANCEL", "id_orden": "O5",
             "fecha": "2026-03-05", "detalle": "cashback_cancel",
             "monto": -14855.0, "tipo_movimiento": "debit",
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

    def test_fee_divergence_classified_as_cargo_diferencias(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        res = self.db.query(
            "SELECT clasificacion_operativa FROM marketplace_ledger_clasificado_v1 "
            "WHERE id_transaccion = 'TX_DIVERG'"
        )
        self.assertEqual(
            res.iloc[0]["clasificacion_operativa"],
            "Cargo por diferencias en las medidas y el peso del paquete",
        )

    def test_cancelacion_mediacion_all_variants_classified(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        res = self.db.query(
            "SELECT id_transaccion, clasificacion_operativa "
            "FROM marketplace_ledger_clasificado_v1 "
            "WHERE id_transaccion IN ('TX_MEDIACION','TX_MEDIACION_ACC','TX_MEDIACION_GLITCH')"
        ).to_dict(orient="records")
        by_tx = {r["id_transaccion"]: r["clasificacion_operativa"] for r in res}

        self.assertEqual(by_tx["TX_MEDIACION"], "Cancelación de la mediación")
        self.assertEqual(by_tx["TX_MEDIACION_ACC"], "Cancelación de la mediación")
        self.assertEqual(by_tx["TX_MEDIACION_GLITCH"], "Cancelación de la mediación")

    def test_cashback_and_cancel_classified(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        res = self.db.query(
            "SELECT id_transaccion, clasificacion_operativa "
            "FROM marketplace_ledger_clasificado_v1 "
            "WHERE id_transaccion IN ('TX_CASHBACK','TX_CASHBACK_CANCEL')"
        ).to_dict(orient="records")
        by_tx = {r["id_transaccion"]: r["clasificacion_operativa"] for r in res}

        self.assertEqual(by_tx["TX_CASHBACK"], "cashback")
        self.assertEqual(by_tx["TX_CASHBACK_CANCEL"], "cashback_cancel")

    def test_no_unclassified_records(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        unclassified = self.db.query(
            "SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 "
            "WHERE clasificacion_operativa = 'NO_CLASIFICADO'"
        ).iloc[0]["n"]
        self.assertEqual(unclassified, 0, "Ningún registro debe quedar sin clasificar")


class TestNewMappingsFinancialClosing(unittest.TestCase):
    """Valida que el cierre mensual consolide correctamente los nuevos conceptos."""

    @classmethod
    def setUpClass(cls):
        DatabaseV4.reset()
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        DatabaseV4._instance = cls.db

        raw_data = [
            # Venta base (ingreso)
            {"marketplace": "ML", "id_transaccion": "TX_SALE", "id_orden": "O0",
             "fecha": "2026-03-10", "detalle": "Cargo por venta (Venta)",
             "monto": 1000000.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Costo operacional
            {"marketplace": "ML", "id_transaccion": "TX_DIVERG", "id_orden": "O1",
             "fecha": "2026-03-01", "detalle": "fee_for_divergence_in_package_dimensions",
             "monto": -72241.0, "tipo_movimiento": "debit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            # Ajustes
            {"marketplace": "ML", "id_transaccion": "TX_MED", "id_orden": "O2",
             "fecha": "2026-03-02", "detalle": "Cancelación de la mediación",
             "monto": 18331.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_CB", "id_orden": "O3",
             "fecha": "2026-03-04", "detalle": "cashback",
             "monto": 14855.0, "tipo_movimiento": "credit",
             "archivo_origen": "test.xlsx", "folio_xml": None, "estado_xml": None},
            {"marketplace": "ML", "id_transaccion": "TX_CBC", "id_orden": "O4",
             "fecha": "2026-03-05", "detalle": "cashback_cancel",
             "monto": -14855.0, "tipo_movimiento": "debit",
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

    def test_financial_closing_correct_totals(self):
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        close = auditor.run_financial_closing("ML", "2026-03-01", "2026-03-31")

        # ¿Cuánto vendí?
        self.assertEqual(close["ingresos"], 1000000.0)
        # ¿Qué me descontaron? (costos operacionales)
        self.assertEqual(close["costos_op"], -72241.0)
        # ¿Ajustes netos? (Cancelación de la mediación is excluded from op_pnl)
        self.assertEqual(close["ajustes"], 0.0)
        # ¿Cuánto gané? (1,000,000 - 72,241 + 0 = 927,759)
        self.assertEqual(close["neto"], 927759.0)


if __name__ == "__main__":
    unittest.main()
