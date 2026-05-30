"""tests/test_ml_audit.py
TDD tests for the ML classification audit.
"""
import pandas as pd
import unittest
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor_ml import audit_ml_misclassifications

class TestMLAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DatabaseV4.reset()
        # Use an in‑memory DuckDB for isolation
        cls.db = DatabaseV4(db_path=":memory:", read_only=False)
        DatabaseV4._instance = cls.db
        # Insert sample data: some correctly classified, some not
        data = [
            # Correctly classified (detail maps to a valid class)
            {"marketplace": "ML", "id_transaccion": "ML001", "id_orden": "O1", "fecha": "2024-01-01", "detalle": "Cargo por venta (Venta)", "monto": 100.0, "tipo_movimiento": "debit", "archivo_origen": "file1.xlsx", "folio_xml": None, "estado_xml": None},
            # Mis‑classified (detail not in map)
            {"marketplace": "ML", "id_transaccion": "ML002", "id_orden": "O2", "fecha": "2024-01-02", "detalle": "Algo desconocido", "monto": 50.0, "tipo_movimiento": "credit", "archivo_origen": "file2.xlsx", "folio_xml": None, "estado_xml": None},
            # Generic adjustment (should be flagged)
            {"marketplace": "ML", "id_transaccion": "ML003", "id_orden": "O3", "fecha": "2024-01-03", "detalle": "Ajuste Poscobro General", "monto": 20.0, "tipo_movimiento": "debit", "archivo_origen": "file3.xlsx", "folio_xml": None, "estado_xml": None},
        ]
        df = pd.DataFrame(data)
        cls.db.insert_df(df, "marketplace_ledger_v1")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.conn.close()
        except:
            pass
        DatabaseV4.reset()

    def test_audit_detects_misclassifications(self):
        mis_df = audit_ml_misclassifications()
        # Expect two rows flagged (ML002 and ML003)
        self.assertEqual(len(mis_df), 2)
        self.assertIn("ML002", mis_df["id_transaccion"].values)
        self.assertIn("ML003", mis_df["id_transaccion"].values)
        # Verify that audit records were inserted
        audit_tbl = self.db.query("SELECT * FROM marketplace_auditoria_v1 WHERE marketplace='ML' AND check_name='MISCLASSIFIED'")
        self.assertEqual(len(audit_tbl), 2)

if __name__ == "__main__":
    unittest.main()
