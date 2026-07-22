import unittest
import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

class TestRipleyClassification(unittest.TestCase):
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

    def test_ripley_taxonomy_mapped_correctly(self):
        ripley_details = [
            "Importe del envío del pedido",
            "Gastos de envío",
            "Importe de reembolso",
            "Importe del pedido reembolsado",
            "Importe del envío del pedido reembolsado",
            "Comisión de reembolso",
            "Impuesto sobre las comisiones",
            "Impuesto sobre la comisión de reembolso",
            "Impuesto de la factura manual",
            "Factura manual",
            "Recargo por precio mínimo"
        ]
        
        raw_data = []
        for i, detail in enumerate(ripley_details):
            raw_data.append({
                "marketplace": "RIPLEY",
                "id_transaccion": f"TX{i}",
                "id_orden": f"ORD{i}",
                "fecha": "2026-01-01",
                "detalle": detail,
                "monto": 1000.0,
                "tipo_movimiento": "Pago",
                "archivo_origen": "test.xlsx",
                "folio_xml": None,
                "estado_xml": None
            })
            
        self.db.insert_df(pd.DataFrame(raw_data), "marketplace_ledger_v1")
            
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        
        df = self.db.query("SELECT detalle, financial_group FROM marketplace_ledger_clasificado_v1")
        
        self.assertEqual(len(df), len(ripley_details), "Not all records were classified")
        
        for index, row in df.iterrows():
            print(f"Row: {row['detalle']} -> {row['financial_group']} (type: {type(row['financial_group'])})")
            self.assertIsNotNone(row['financial_group'])
            self.assertFalse(pd.isna(row['financial_group']))
            self.assertNotEqual(row['financial_group'], 'sin_clasificar')
            self.assertNotEqual(row['financial_group'], 'NULL')

if __name__ == "__main__":
    unittest.main()
