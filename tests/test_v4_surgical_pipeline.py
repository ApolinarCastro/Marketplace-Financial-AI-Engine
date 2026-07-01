from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.surgical_loader import SurgicalLoader


class V4SurgicalPipelineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        DatabaseV4.reset()
        self.temp_root = Path(__file__).resolve().parent / ".tmp" / f"pipeline_{uuid.uuid4().hex}"
        self.temp_root.mkdir(parents=True, exist_ok=True)
        
        # Patch ROOT inside surgical_loader
        import engine.v4.surgical_loader
        self.original_root = engine.v4.surgical_loader.ROOT
        self.original_dir_fact = engine.v4.surgical_loader.DIR_FACTURACION
        self.original_dir_poscobro = engine.v4.surgical_loader.DIR_POSCOBRO
        
        engine.v4.surgical_loader.ROOT = self.temp_root
        engine.v4.surgical_loader.DIR_FACTURACION = self.temp_root / "01_Raw" / "ML" / "ML_Facturacion"
        engine.v4.surgical_loader.DIR_POSCOBRO = self.temp_root / "01_Raw" / "ML" / "Poscobro"

        # Initialize test database
        self.db = DatabaseV4(self.temp_root / "test_pipeline.db", read_only=False)
        DatabaseV4._instance = self.db

    def tearDown(self) -> None:
        try:
            self.db.conn.close()
        except Exception:
            pass
        DatabaseV4.reset()
        
        # Restore patched ROOT
        import engine.v4.surgical_loader
        engine.v4.surgical_loader.ROOT = self.original_root
        engine.v4.surgical_loader.DIR_FACTURACION = self.original_dir_fact
        engine.v4.surgical_loader.DIR_POSCOBRO = self.original_dir_poscobro
        
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def write_xlsx(self, relative_path: str, rows: list[dict]) -> Path:
        path = self.temp_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_excel(path, index=False)
        return path

    def test_full_pipeline_ingestion_classification_and_audit(self) -> None:
        # 1. Write dummy facturacion file
        self.write_xlsx(
            "01_Raw/ML/ML_Facturacion/fact_test.xlsx",
            [
                {
                    "Número de venta": "2000000000000001",
                    "Publicación": "SKU-1",
                    "Total de la venta": 10000.0,
                    "Valor del cargo": 1500.0,
                    "Detalle": "Cargo por venta",
                    "Fecha del cargo": "2026-03-01",
                    "Factura fiscal": "F-100"
                },
                {
                    "Número de venta": "2000000000000002",
                    "Publicación": "SKU-2",
                    "Total de la venta": 20000.0,
                    "Valor del cargo": 3000.0,
                    "Detalle": "Cargo por envíos de Mercado Libre",
                    "Fecha del cargo": "2026-03-02",
                    "Factura fiscal": "F-101"
                }
            ]
        )

        # 2. Write dummy poscobro file
        self.write_xlsx(
            "01_Raw/ML/Poscobro/pos_test.xlsx",
            [
                {
                    "OrderId": "2000000000000001",
                    "OperationId": "123456",
                    "Monto": -500.0,
                    "ReasonDetail": "repentant_buyer",
                    "StatusDetail": "reconciled",
                    "DateCreated": "2026-03-03"
                }
            ]
        )

        # Run loader
        loader = SurgicalLoader()
        loader.load_facturacion()
        loader.load_poscobro()

        # Check raw row counts
        self.assertEqual(self.db.count("ventas_marketplace"), 1)
        # 2 sale entries + 2 comm entries + 1 shipping opex entry + 1 poscobro opex entry
        # Wait:
        # Row 1 (Cargo por venta): is_cargo_venta is true -> inserts SALE (10000) and COMM (-1500).
        # Row 2 (Cargo por envios): is_cargo_venta/is_anulacion_venta false -> inserts CHG (-3000).
        # Poscobro: inserts 1 POS row with repentant_buyer (-500).
        # Total in ledger: 2 + 1 + 1 = 4 rows.
        self.assertEqual(self.db.count("marketplace_ledger_v1"), 4)

        # Ensure all rows have marketplace = 'ML'
        ml_rows = self.db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace = 'ML'").iloc[0]['n']
        self.assertEqual(ml_rows, 4)

        # Run classification
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        
        # Verify classification
        class_count = self.db.count("marketplace_ledger_clasificado_v1")
        self.assertEqual(class_count, 4)

        # Check specific mapped classes
        classes = self.db.query("SELECT id_transaccion, clasificacion_operativa FROM marketplace_ledger_clasificado_v1").to_dict(orient="records")
        by_tx = {r["id_transaccion"]: r["clasificacion_operativa"] for r in classes}
        
        # We need to find key prefixes
        sale_tx = [k for k in by_tx.keys() if k.startswith("SALE_")][0]
        comm_tx = [k for k in by_tx.keys() if k.startswith("COMM_")][0]
        chg_tx = [k for k in by_tx.keys() if k.startswith("CHG_")][0]
        pos_tx = [k for k in by_tx.keys() if k.startswith("POS_")][0]

        self.assertEqual(by_tx[sale_tx], "Cargo por venta (Venta)")
        self.assertEqual(by_tx[comm_tx], "Cargo por venta (Comisión)")
        self.assertEqual(by_tx[chg_tx], "Cargo por envíos de Mercado Libre")
        self.assertEqual(by_tx[pos_tx], "Ajuste por Arrepentimiento")

        # Run financial closing
        close_res = auditor.run_financial_closing("ML", "2026-03-01", "2026-03-31")
        self.assertEqual(close_res["ingresos"], 10000.0)
        self.assertEqual(close_res["costos_op"], -3000.0)
        self.assertEqual(close_res["costos_com"], -1500.0)
        self.assertEqual(close_res["ajustes"], 0.0)
        # PHASE_16F: repentant_buyer excluded from operational P&L
        self.assertEqual(close_res["neto"], 5500.0)

        # Run audit
        auditor.run_audit()
        # Since we have no unclassified items and no 2026 legal XML issues (no folio mapping yet), audit should be 0 or small
        # Actually repentant_buyer does not have folio, but it's an opex/adjustment that doesn't require XML.
        # Let's verify no unclassified alerts.
        unclassified_alerts = self.db.query("SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE check_name = 'movimientos_no_clasificados'").iloc[0]['n']
        self.assertEqual(unclassified_alerts, 0)


if __name__ == "__main__":
    unittest.main()
