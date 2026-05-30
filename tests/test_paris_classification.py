from __future__ import annotations

import shutil
import unittest
import uuid
from pathlib import Path
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, FINANCIAL_STRUCTURE
from engine.v4.surgical_loader import SurgicalLoader

class ParisClassificationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        DatabaseV4.reset()
        self.temp_root = Path(__file__).resolve().parent / ".tmp" / f"paris_{uuid.uuid4().hex}"
        self.temp_root.mkdir(parents=True, exist_ok=True)
        
        # Patch ROOT inside surgical_loader to point to our temp_root
        import engine.v4.surgical_loader
        self.original_root = engine.v4.surgical_loader.ROOT
        self.original_dir_fact = engine.v4.surgical_loader.DIR_FACTURACION
        self.original_dir_poscobro = engine.v4.surgical_loader.DIR_POSCOBRO
        
        engine.v4.surgical_loader.ROOT = self.temp_root
        engine.v4.surgical_loader.DIR_FACTURACION = self.temp_root / "01_Raw" / "ML" / "ML_Facturacion"
        engine.v4.surgical_loader.DIR_POSCOBRO = self.temp_root / "01_Raw" / "ML" / "Poscobro"

        # Initialize test database
        self.db = DatabaseV4(self.temp_root / "test_v4.db", read_only=False)
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

    def test_recursive_glob_ingests_from_subdirectories(self) -> None:
        # Write dummy transaction files inside Dropshipping and Fulfillment folders
        self.write_xlsx(
            "01_Raw/PARIS/Transacciones/Dropshipping/report_drop.xlsx",
            [
                {
                    "ID": "TX-DROP-1",
                    "TIPO": "Pago normal",
                    "NÚMERO ORDEN": "ORD-DROP-1",
                    "MONTO A PAGAR": "15000",
                    "FECHA": "2026-04-10"
                }
            ]
        )
        self.write_xlsx(
            "01_Raw/PARIS/Transacciones/Fulfillment/report_full.xlsx",
            [
                {
                    "ID": "TX-FULL-1",
                    "TIPO": "Ajuste Inventario Activo",
                    "NÚMERO ORDEN": "ORD-FULL-1",
                    "MONTO A PAGAR": "20000",
                    "FECHA": "2026-04-15"
                }
            ]
        )

        loader = SurgicalLoader()
        # Under current implementation with non-recursive glob (*.xlsx), this should load 0 rows
        # because the excel files are located inside subfolders.
        # After the fix, it should find both files and load 2 rows.
        loader.load_paris()
        
        count = self.db.count("marketplace_ledger_v1")
        self.assertEqual(count, 2)

    def test_new_concepts_are_classified_correctly(self) -> None:
        # Seed the ledger with the new concepts
        ledger_rows = [
            # marketplace, id_transaccion, id_orden, fecha, detalle, monto, tipo_movimiento, archivo_origen, folio_xml
            ("PARIS", "TX-1", "ORD-1", "2026-04-17", "Ajuste Inventario Activo", 49283.0, "CARGO", "f.xlsx", None),
            ("PARIS", "TX-2", "ORD-2", "2026-04-30", "Retiro stock bodega Paris", -354300.0, "CARGO", "f.xlsx", None),
            ("PARIS", "TX-3", "ORD-3", "2026-04-16", "Merma", 16991.0, "CARGO", "f.xlsx", None),
            ("PARIS", "TX-4", "ORD-4", "2024-02-15", "Multa", -5000.0, "CARGO", "f.xlsx", None),
            ("PARIS", "TX-5", "ORD-5", "2024-08-10", "Multa por stock", -3000.0, "CARGO", "f.xlsx", None)
        ]
        
        for row in ledger_rows:
            self.db.execute("""
                INSERT INTO marketplace_ledger_v1 
                (marketplace, id_transaccion, id_orden, fecha, detalle, monto, tipo_movimiento, archivo_origen, folio_xml)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, list(row))
            
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        
        classified = self.db.query("SELECT id_transaccion, clasificacion_operativa FROM marketplace_ledger_clasificado_v1").to_dict(orient="records")
        by_tx = {row["id_transaccion"]: row["clasificacion_operativa"] for row in classified}
        
        # Verify specific operational classifications instead of NO_CLASIFICADO or historical fallbacks
        self.assertEqual(by_tx["TX-1"], "Ajuste Inventario Activo")
        self.assertEqual(by_tx["TX-2"], "Retiro stock bodega Paris")
        self.assertEqual(by_tx["TX-3"], "Merma")
        self.assertEqual(by_tx["TX-4"], "Multa")
        self.assertEqual(by_tx["TX-5"], "Multa por stock")
        
        # Verify financial structure categories
        self.assertIn("Ajuste Inventario Activo", FINANCIAL_STRUCTURE["ajustes"])
        self.assertIn("Retiro stock bodega Paris", FINANCIAL_STRUCTURE["costos_operacionales"])
        self.assertIn("Merma", FINANCIAL_STRUCTURE["ajustes"])
        self.assertIn("Multa", FINANCIAL_STRUCTURE["ajustes"])
        self.assertIn("Multa por stock", FINANCIAL_STRUCTURE["ajustes"])

if __name__ == "__main__":
    unittest.main()
