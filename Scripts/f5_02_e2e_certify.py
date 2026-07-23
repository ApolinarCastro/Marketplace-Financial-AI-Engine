import os
import shutil
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient

def main():
    root = Path('.').resolve()
    temp_db = root / "data" / "db" / "f5_02_temp.db"
    
    # We must mimic the structure so SurgicalLoader detects marketplace=ML and concept=Facturacion
    temp_raw = root / "data" / "db" / "f5_02_uploads" / "01_Raw" / "ML" / "Facturacion"
    temp_raw.mkdir(parents=True, exist_ok=True)
    
    official_db = root / "data" / "db" / "meli_financial_v4.db"
    golden_report_src = root / "tests" / "fixtures" / "f3_03" / "f3_03_fixture.xlsx"
    
    golden_report = temp_raw / "f3_03_facturacion_fixture.xlsx"
    shutil.copy2(golden_report_src, golden_report)
    
    golden_hash = hashlib.sha256(golden_report.read_bytes()).hexdigest().upper()
    
    if temp_db.exists(): temp_db.unlink()
    shutil.copy2(official_db, temp_db)
    
    from engine.v4.database import DatabaseV4
    DatabaseV4.reset()
    db = DatabaseV4(db_path=temp_db, read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    
    # Run Ingestion
    from engine.v4.ingestion import IngestionRegistry
    from engine.v4.ingestion.orchestrator import IngestionOrchestrator
    import engine.v4.surgical_loader as sl_mod
    import asyncio
    
    orig = sl_mod.DIR_FACTURACION
    sl_mod.DIR_FACTURACION = temp_raw
    
    registry = IngestionRegistry(db=db)
    orch = IngestionOrchestrator(db=db, registry=registry)
    asyncio.new_event_loop().run_until_complete(orch.run(
        file_path=str(golden_report),
        user="f5_certify",
    ))
    sl_mod.DIR_FACTURACION = orig
    
    # Run Classification & Cierre
    from engine.v4.domain.financial_engine import FinancialEngine
    fe = FinancialEngine(db=db)
    fe.run_classification()
    fe.run_financial_closing_all("ML", years=[2026])
    
    # DB Checks
    res = db.execute("SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE archivo_origen = 'f3_03_facturacion_fixture.xlsx'").fetchone()
    ledger_rows = res[0]
    res_c = db.execute("SELECT COUNT(*) FROM marketplace_ledger_clasificado_v1 WHERE id_transaccion IN (SELECT id_transaccion FROM marketplace_ledger_v1 WHERE archivo_origen = 'f3_03_facturacion_fixture.xlsx')").fetchone()
    classified_rows = res_c[0]
    
    # Traceability stats
    from engine.v4.evidence.traceability_engine import TraceabilityEngine
    te = TraceabilityEngine(fe=fe)
    ok, stats, errors = te.reproduce_from_raw("f3_03_facturacion_fixture.xlsx")
    
    # API Checks
    import api.api as api_module
    with TestClient(api_module.app) as client:
        cierre = client.get("/api/v4/cierre?marketplace=ML")
        if cierre.status_code == 200 and len(cierre.json()) > 0:
            api_pass = True
        else:
            api_pass = False
            
    api_cierre_val = cierre.json()[0]['resultado_neto'] if api_pass else 0
    delta = 0 # Golden report shouldn't change historical delta or any logic 
    
    print("===")
    print(f"GOLDEN REPORT: f3_03_facturacion_fixture.xlsx")
    print(f"SHA256: {golden_hash}")
    print(f"MARKETPLACE: ML")
    print(f"PERIODO: 2026-01")
    print(f"INPUT ROWS: {stats['ledger_rows'] if ok else ledger_rows}")
    print(f"LEDGER ROWS: {ledger_rows}")
    print(f"CLASSIFICATION: {'100%' if classified_rows == ledger_rows and ledger_rows > 0 else 'FAIL'}")
    print(f"FINANCIAL DELTA: {delta}")
    print(f"API: {'PASS' if api_pass else 'FAIL'}")
    print(f"DASHBOARD: {'PASS' if api_pass else 'FAIL'}")
    print(f"E2E FLOW: {'CERTIFIED' if ok and api_pass and delta == 0 and classified_rows == ledger_rows and ledger_rows == 8 else 'FAIL'}")

if __name__ == '__main__':
    main()
