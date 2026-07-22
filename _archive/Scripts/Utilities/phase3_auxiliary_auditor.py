import os
import json
import time
from engine.v4.database import DatabaseV4
from engine.v4.certification.ecc.ecc_adapter import ECCAdapter
import pandas as pd

def run_phase3_audit():
    db = DatabaseV4.get()
    adapter = ECCAdapter()
    
    marketplaces = ["ML", "PARIS", "FALABELLA", "RIPLEY"]
    
    coverage_matrix = []
    traceability_matrix = []
    catalog = []
    
    for mp in marketplaces:
        print(f"Auditando {mp}...")
        
        # Solo auditar los que tienen XML indexado para poder verificar el SUCCESS real
        query = f"""
            SELECT id_transaccion, id_orden, folio_xml, marketplace, fecha, monto 
            FROM marketplace_ledger_v1
            WHERE marketplace = '{mp}' 
              AND folio_xml IS NOT NULL 
              AND folio_xml != 'None'
            LIMIT 10000
        """
        df_ledger = db.query(query)
        
        # In memory filtering for ML to handle 033-0000 padding
        valid_ledgers = []
        if not df_ledger.empty:
            df_truth = db.query(f"SELECT folio FROM dte_truth_v1 WHERE marketplace = '{mp}'")
            truth_folios = set(df_truth['folio'].astype(str))
            
            for _, r in df_ledger.iterrows():
                f = str(r['folio_xml'])
                f_clean = f
                if mp == 'ML' and '-' in f:
                    f_clean = f.split('-')[1].lstrip('0')
                if f_clean in truth_folios:
                    valid_ledgers.append(r)
                if len(valid_ledgers) == 100:
                    break
            df_ledger = pd.DataFrame(valid_ledgers)
            
        stats = {
            "Marketplace": mp,
            "Total_Muestreado": len(df_ledger),
            "XML": 0,
            "DTE": 0,
            "SUCCESS": 0,
            "FAIL": 0,
            "NOT_FOUND": 0,
            "Cobertura": "0.00%"
        }
        
        for _, row in df_ledger.iterrows():
            tx_id = str(row['id_transaccion'])
            order_id = str(row['id_orden'])
            folio = str(row['folio_xml']) if pd.notna(row['folio_xml']) and str(row['folio_xml']) != 'None' else None
            
            trace_entry = {
                "transaction_id": tx_id,
                "order_id": order_id,
                "folio_xml": folio,
                "file_path": None,
                "tipo_dte": None,
                "marketplace": mp,
                "status": "NOT_FOUND",
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
            if folio:
                stats["XML"] += 1
                # Try finding matching DTE
                # Depending on the system, Ripley folios might need some parsing, but let's test exact match first.
                folio_search = folio
                if mp == 'ML' and '-' in folio:
                    folio_search = folio.split('-')[1].lstrip('0')
                
                df_dte = db.query(f"SELECT file_path FROM dte_truth_v1 WHERE folio = '{folio_search}' AND marketplace = '{mp}' LIMIT 1")
                
                if not df_dte.empty and pd.notna(df_dte.iloc[0]['file_path']):
                    stats["DTE"] += 1
                    file_path = df_dte.iloc[0]['file_path']
                    trace_entry["file_path"] = file_path
                    
                    try:
                        from engine.v4.certification.electronic_certification.xml_reader import XMLReader
                        xml_content, _ = XMLReader.read_xml(file_path)
                            
                        payload = adapter.process(xml_content, marketplace=mp)
                        cert_status = payload.electronic_certificate.get("overall_status", "FAIL")
                        trace_entry["status"] = cert_status
                        trace_entry["tipo_dte"] = payload.document_type
                        
                        if cert_status == "PASS":
                            stats["SUCCESS"] += 1
                        else:
                            stats["FAIL"] += 1
                            
                    except Exception as e:
                        trace_entry["status"] = f"FAIL (Error: {str(e)})"
                        stats["FAIL"] += 1
                else:
                    stats["NOT_FOUND"] += 1
            else:
                stats["NOT_FOUND"] += 1
                
            traceability_matrix.append(trace_entry)
            if trace_entry["status"] == "PASS" and len(catalog) < 20: 
                catalog.append(trace_entry)
                
        if stats["Total_Muestreado"] > 0:
            stats["Cobertura"] = f"{(stats['SUCCESS'] / stats['Total_Muestreado']) * 100:.2f}%"
            
        coverage_matrix.append(stats)
        
    out_dir = "C:\\Users\\ASUS Zenbook\\.gemini\\antigravity-ide\\brain\\7e10ebb4-ac65-4d64-93b7-bfebef91fdc9"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "REAL_TRANSACTION_CATALOG.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)
        
    with open(os.path.join(out_dir, "MARKETPLACE_COVERAGE_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write("# Marketplace Coverage Matrix\n\n")
        f.write("| Marketplace | XML | DTE | SUCCESS | FAIL | NOT_FOUND | Cobertura |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for m in coverage_matrix:
            f.write(f"| {m['Marketplace']} | {m['XML']} | {m['DTE']} | {m['SUCCESS']} | {m['FAIL']} | {m['NOT_FOUND']} | {m['Cobertura']} |\n")
            
    with open(os.path.join(out_dir, "XML_TRACEABILITY_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write("# XML Traceability Matrix\n\n")
        f.write("| Timestamp | Marketplace | Transaction ID | Order ID | Folio XML | File Path | Status |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for t in traceability_matrix:
            f.write(f"| {t['timestamp']} | {t['marketplace']} | {t['transaction_id']} | {t['order_id']} | {t['folio_xml']} | {t['file_path']} | {t['status']} |\n")

    print("Auditoría generada exitosamente.")

if __name__ == "__main__":
    run_phase3_audit()
