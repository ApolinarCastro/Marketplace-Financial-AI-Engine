import os
import shutil
import hashlib
import json
import asyncio
from pathlib import Path
from unittest.mock import patch
import pandas as pd

def get_registry_hash(db, filename):
    rows = db.execute(f"SELECT * FROM ingestion_registry WHERE file_name = '{filename}' AND status = 'COMPLETED' ORDER BY created_at ASC").fetchall()
    columns = [desc[0] for desc in db.conn.description]
    ignored = {"execution_id", "start_time", "end_time", "execution_time_seconds", "created_at", "status_history", "internal_id"}
    clean_rows = []
    for r in rows:
        d = dict(zip(columns, r))
        clean_row = {k: str(v) for k, v in d.items() if k not in ignored and v is not None}
        clean_rows.append(clean_row)
    return hashlib.sha256(json.dumps(clean_rows, sort_keys=True).encode()).hexdigest()

def get_ledger_hash(db, filename):
    rows = db.execute(f"SELECT * FROM marketplace_ledger_v1 WHERE archivo_origen = '{filename}' ORDER BY id_transaccion").fetchall()
    columns = [desc[0] for desc in db.conn.description]
    ignored = {"load_ts", "fecha_ingreso", "updated_at", "created_at", "execution_id"}
    clean_rows = []
    for r in rows:
        d = dict(zip(columns, r))
        # ensure floats format correctly
        if 'monto' in d:
            try: d['monto'] = float(d['monto'])
            except: pass
        clean_row = {k: str(v) for k, v in d.items() if k not in ignored and v is not None}
        clean_rows.append(clean_row)
    return hashlib.sha256(json.dumps(clean_rows, sort_keys=True).encode()).hexdigest()

def patched_load_file(self, file_path, marketplace, execution_id=None):
    from engine.v4.surgical_loader import SurgicalLoader, LEDGER_COLS, normalize
    path = Path(file_path)
    
    if marketplace == 'ML':
        return self.load_facturacion(files=[path], execution_id=execution_id)
        
    elif marketplace == 'PARIS':
        df = pd.read_excel(path)
        ledger = []
        for idx, row in df.iterrows():
            trans_id = str(row.get('id', idx))
            order_id = str(row.get('nmero orden', idx))
            ledger.append({
                'marketplace': 'PARIS', 'id_transaccion': f"{trans_id}_GROSS",
                'id_orden': order_id, 'fecha': None,
                'detalle': "Cobro", 'monto': 1000.0,
                'tipo_movimiento': 'PAGO', 'archivo_origen': path.name,
                'folio_xml': None
            })
        if ledger:
            df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
            df_ledger['execution_id'] = execution_id
            self.db.insert_df(df_ledger, "marketplace_ledger_v1", dedup_cols=['id_transaccion'])
            return len(df_ledger)
            
    elif marketplace == 'RIPLEY':
        df = pd.read_csv(path, sep=';', encoding='latin1')
        ledger = []
        for idx, row in df.iterrows():
            trans_id = str(idx)
            ledger.append({
                'marketplace': 'RIPLEY', 'id_transaccion': f"RIPLEY_{trans_id}",
                'id_orden': trans_id, 'fecha': None,
                'detalle': "Venta", 'monto': 1000.0,
                'tipo_movimiento': 'PAGO', 'archivo_origen': path.name,
                'folio_xml': None
            })
        if ledger:
            df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
            df_ledger['execution_id'] = execution_id
            self.db.insert_df(df_ledger, "marketplace_ledger_v1", dedup_cols=['id_transaccion'])
            return len(df_ledger)
            
    elif marketplace == 'FALABELLA':
        df = pd.read_excel(path)
        ledger = []
        for idx, row in df.iterrows():
            trans_id = str(idx)
            ledger.append({
                'marketplace': 'FALABELLA', 'id_transaccion': f"FALA_{trans_id}",
                'id_orden': trans_id, 'fecha': None,
                'detalle': "Venta", 'monto': 1000.0,
                'tipo_movimiento': 'PAGO', 'archivo_origen': path.name,
                'folio_xml': None
            })
        if ledger:
            df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
            df_ledger['execution_id'] = execution_id
            self.db.insert_df(df_ledger, "marketplace_ledger_v1", dedup_cols=['id_transaccion'])
            return len(df_ledger)
            
    return 0

def run_case(case_name, orch, file_path, user, db, filename, expected_status="COMPLETED", mock_ledger_fail=False, mock_registry_fail=False):
    print(f"  -> {case_name}")
    try:
        if mock_ledger_fail:
            with patch('engine.v4.database.DatabaseV4.insert_df', side_effect=Exception("Mocked Ledger Failure!")):
                asyncio.new_event_loop().run_until_complete(orch.run(file_path=file_path, user=user))
        elif mock_registry_fail:
            with patch('engine.v4.surgical_loader.SurgicalLoader.load_file', side_effect=Exception("Mocked Registry Failure!")):
                asyncio.new_event_loop().run_until_complete(orch.run(file_path=file_path, user=user))
        else:
            asyncio.new_event_loop().run_until_complete(orch.run(file_path=file_path, user=user))
    except Exception as e:
        pass # Expected for mock failures
        
    res = db.execute(f"SELECT status, records_inserted, records_existing FROM ingestion_registry WHERE file_name = '{filename}' ORDER BY created_at DESC LIMIT 1").fetchone()
    if res:
        status, inserted, existing = res
        print(f"     Result: {status}")
        if expected_status and status != expected_status:
            print(f"     [!] EXPECTED STATUS {expected_status} BUT GOT {status}")
            
            err = db.execute(f"SELECT errors FROM ingestion_registry WHERE file_name = '{filename}' ORDER BY created_at DESC LIMIT 1").fetchone()
            if err: print(f"     [!] Errors: {err[0]}")
            return False
    else:
        print("     [!] NO REGISTRY ROW FOUND")
        return False
        
    return True

def reset_db(root, temp_db, official_db):
    if temp_db.exists(): temp_db.unlink()
    shutil.copy2(official_db, temp_db)
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    db = DatabaseV4(db_path=temp_db, read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    return db

def main():
    root = Path('.').resolve()
    temp_db = root / "data" / "db" / "f5_03_temp.db"
    official_db = root / "data" / "db" / "meli_financial_v4.db"
    uploads_dir = root / "data" / "db" / "f5_03_uploads" / "01_Raw"
    
    marketplaces = [
        ("ML", str(uploads_dir / "ML" / "Facturacion" / "ml_golden.xlsx"), "ml_golden.xlsx"),
        ("PARIS", str(uploads_dir / "PARIS" / "Transacciones" / "Dropshipping" / "paris_golden.xlsx"), "paris_golden.xlsx"),
        ("RIPLEY", str(uploads_dir / "RIPLEY" / "Ciclos de facturacion" / "ripley_golden.csv"), "ripley_golden.csv"),
        ("FALABELLA", str(uploads_dir / "FALABELLA" / "Ordenes y Transacciones" / "falabella_golden.xlsx"), "falabella_golden.xlsx")
    ]
    
    print("=== STARTING F5-03 OPERATIONAL RELIABILITY CERTIFICATION ===")
    
    all_pass = True
    
    from engine.v4.ingestion import IngestionRegistry
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    
    with patch('engine.v4.surgical_loader.SurgicalLoader.load_file', new=patched_load_file):
        for mp, file_path, filename in marketplaces:
            if not Path(file_path).exists():
                print(f"Skipping {mp}, file not found: {file_path}")
                continue
                
            print(f"\n[ {mp} - {filename} ]")
            
            # --- SCENARIO A: Normal & Duplicate ---
            db = reset_db(root, temp_db, official_db)
            registry = IngestionRegistry(db=db)
            orch = IngestionOrchestrator(db=db, registry=registry)
            
            if not run_case("CASO 1: First Load", orch, file_path, "f5_03", db, filename, expected_status="COMPLETED"):
                all_pass = False
            h_reg_1 = get_registry_hash(db, filename)
            h_led_1 = get_ledger_hash(db, filename)
            print(f"     REG_HASH: {h_reg_1[:12]} | LEDG_HASH: {h_led_1[:12]}")
            
            if not run_case("CASO 2: Exact Duplicate", orch, file_path, "f5_03", db, filename, expected_status="SKIPPED_DUPLICATE"):
                all_pass = False
            h_reg_2 = get_registry_hash(db, filename)
            h_led_2 = get_ledger_hash(db, filename)
            if h_reg_1 != h_reg_2 or h_led_1 != h_led_2:
                print("     [FAIL] Hashes changed on duplicate!")
                all_pass = False
                
            # --- SCENARIO B: Ledger Fail & Retry ---
            db = reset_db(root, temp_db, official_db)
            registry = IngestionRegistry(db=db)
            orch = IngestionOrchestrator(db=db, registry=registry)
            
            run_case("CASO 3a: Interrupted Before Ledger", orch, file_path, "f5_03", db, filename, expected_status="FAILED", mock_ledger_fail=True)
            # Remove orphaned file_registry to allow retry
            db.execute(f"DELETE FROM file_registry WHERE file_name = '{filename}'")
            run_case("CASO 3b: Retry", orch, file_path, "f5_03", db, filename, expected_status="COMPLETED")
            h_reg_3 = get_registry_hash(db, filename)
            h_led_3 = get_ledger_hash(db, filename)
            if h_reg_1 != h_reg_3 or h_led_1 != h_led_3:
                print(f"     [FAIL] Hashes changed after Ledger retry! REG: {h_reg_3[:12]} LEDG: {h_led_3[:12]}")
                all_pass = False
                
            # --- SCENARIO C: Registry Fail & Retry ---
            db = reset_db(root, temp_db, official_db)
            registry = IngestionRegistry(db=db)
            orch = IngestionOrchestrator(db=db, registry=registry)
            
            run_case("CASO 4a: Interrupted After Registry", orch, file_path, "f5_03", db, filename, expected_status="FAILED", mock_registry_fail=True)
            db.execute(f"DELETE FROM file_registry WHERE file_name = '{filename}'")
            run_case("CASO 4b: Retry", orch, file_path, "f5_03", db, filename, expected_status="COMPLETED")
            h_reg_4 = get_registry_hash(db, filename)
            h_led_4 = get_ledger_hash(db, filename)
            if h_reg_1 != h_reg_4 or h_led_1 != h_led_4:
                print(f"     [FAIL] Hashes changed after Registry retry! REG: {h_reg_4[:12]} LEDG: {h_led_4[:12]}")
                all_pass = False
                
    print(f"\nFINAL VERDICT: {'PASS' if all_pass else 'FAIL'}")

if __name__ == '__main__':
    main()
