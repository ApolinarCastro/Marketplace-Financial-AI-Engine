"""Phase 4 Classification Reconstruction — marketplace-scoped classification + mojibake normalization."""
import unittest
import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, _fix_mojibake
from taxonomy.taxonomy_loader import _fix_mojibake as _fix_mojibake_tl


class TestMojibakeNormalization(unittest.TestCase):
    def test_fix_acute_accent(self):
        self.assertEqual(_fix_mojibake("campaÃ±a"), "campaña")
        self.assertEqual(_fix_mojibake("DevoluciÃ³n"), "Devolución")
        self.assertEqual(_fix_mojibake("ComisiÃ³n"), "Comisión")

    def test_fix_multiple_accents(self):
        self.assertEqual(_fix_mojibake("LogÃ­stica inversa"), "Logística inversa")
        self.assertEqual(_fix_mojibake("CompensaciÃ³n logÃ­stica"), "Compensación logística")

    def test_clean_text_passthrough(self):
        self.assertEqual(_fix_mojibake("Devolución"), "Devolución")
        self.assertEqual(_fix_mojibake("Cargo por venta (Comisión)"), "Cargo por venta (Comisión)")

    def test_taxonomy_loader_replica(self):
        """Both _fix_mojibake implementations must produce identical results."""
        test_cases = ["campaÃ±a", "DevoluciÃ³n", "LogÃ­stica", "ComisiÃ³n", "Devolución", "clean text"]
        for tc in test_cases:
            self.assertEqual(_fix_mojibake(tc), _fix_mojibake_tl(tc))


class TestMarketplaceScopedClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._old_instance = DatabaseV4._instance
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        cls.db.is_read_only = False
        DatabaseV4._instance = cls.db

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.close()
        except Exception:
            pass
        DatabaseV4._instance = cls._old_instance

    def setUp(self):
        self.db.execute("DELETE FROM marketplace_ledger_v1")
        self.db.execute("DELETE FROM marketplace_ledger_clasificado_v1")

    def _insert_row(self, marketplace, detalle, monto=1000.0, id_tx=None):
        self.db.execute(
            "INSERT INTO marketplace_ledger_v1 (marketplace, id_transaccion, id_orden, fecha, detalle, monto, tipo_movimiento) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [marketplace, id_tx or f"TX_{marketplace}_{detalle[:10]}", f"ORD_{marketplace}", "2026-01-15", detalle, monto, "Pago"]
        )

    def test_classify_only_ml(self):
        self._insert_row("ML", "Cargo por venta (Venta)", 10000.0)
        self._insert_row("RIPLEY", "Importe del pedido", 5000.0)
        auditor = MarketplaceAuditorEngine()
        n = auditor.run_classification(marketplace="ML")
        self.assertEqual(n, 1)
        df = self.db.query("SELECT marketplace, financial_group FROM marketplace_ledger_clasificado_v1")
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["marketplace"], "ML")
        self.assertEqual(df.iloc[0]["financial_group"], "ingresos")

    def test_classify_only_ripley(self):
        self._insert_row("ML", "Cargo por venta (Venta)", 10000.0)
        self._insert_row("RIPLEY", "Importe del pedido", 5000.0)
        auditor = MarketplaceAuditorEngine()
        n = auditor.run_classification(marketplace="RIPLEY")
        self.assertEqual(n, 1)
        df = self.db.query("SELECT marketplace, financial_group FROM marketplace_ledger_clasificado_v1")
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["marketplace"], "RIPLEY")
        self.assertIsNotNone(df.iloc[0]["financial_group"])

    def test_classify_all_when_no_marketplace(self):
        self._insert_row("ML", "Cargo por venta (Venta)", 10000.0)
        self._insert_row("RIPLEY", "Importe del pedido", 5000.0)
        self._insert_row("PARIS", "Venta", 3000.0)
        auditor = MarketplaceAuditorEngine()
        n = auditor.run_classification()
        self.assertEqual(n, 3)

    def test_classify_paris_independently(self):
        self._insert_row("ML", "Cargo por venta (Venta)", 10000.0)
        self._insert_row("PARIS", "Venta", 3000.0)
        auditor = MarketplaceAuditorEngine()
        n = auditor.run_classification(marketplace="PARIS")
        self.assertEqual(n, 1)
        df = self.db.query("SELECT marketplace FROM marketplace_ledger_clasificado_v1")
        self.assertEqual(df.iloc[0]["marketplace"], "PARIS")

    def test_classification_propagates_to_ledger(self):
        self._insert_row("ML", "Cargo por venta (Venta)", 10000.0)
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification(marketplace="ML")
        row = self.db.query("SELECT clasificacion_operativa, financial_group, include_in_operational_pnl FROM marketplace_ledger_v1 WHERE marketplace='ML'").iloc[0]
        self.assertEqual(row["clasificacion_operativa"], "Cargo por venta (Venta)")
        self.assertEqual(row["financial_group"], "ingresos")
        self.assertTrue(row["include_in_operational_pnl"])

    def test_ripley_importe_mapped_correctly(self):
        self._insert_row("RIPLEY", "Importe del pedido", 5000.0)
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification(marketplace="RIPLEY")
        row = self.db.query("SELECT financial_group, clasificacion_operativa FROM marketplace_ledger_clasificado_v1").iloc[0]
        self.assertEqual(row["clasificacion_operativa"], "Importe del pedido")
        self.assertEqual(row["financial_group"], "ingresos")


if __name__ == "__main__":
    unittest.main()
