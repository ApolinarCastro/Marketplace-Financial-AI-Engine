import glob
import xml.etree.ElementTree as ET
import pandas as pd
import logging
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from engine.v4.database import DatabaseV4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dte.matcher")

class DTEMatcher:
    def __init__(self):
        self.db = DatabaseV4.get()
        self.namespaces = {'ns0': 'http://www.sii.cl/SiiDte'}
        
    def load_dtes(self):
        xml_files = glob.glob(str(ROOT / '01_Raw/ML/Documentos Recepcionados/*.xml'))
        rows = []
        for f in xml_files:
            try:
                tree = ET.parse(f)
                root = tree.getroot()
                
                encabezado = root.find('.//ns0:Encabezado', self.namespaces)
                if encabezado is None:
                    continue
                    
                folio = encabezado.find('.//ns0:Folio', self.namespaces).text
                fecha = encabezado.find('.//ns0:FchEmis', self.namespaces).text
                
                emisor = encabezado.find('.//ns0:Emisor', self.namespaces)
                rut = emisor.find('ns0:RUTEmisor', self.namespaces).text if emisor is not None else None
                nombre = emisor.find('ns0:RznSoc', self.namespaces).text if emisor is not None else None
                
                totales = encabezado.find('.//ns0:Totales', self.namespaces)
                mnt_neto = float(totales.find('ns0:MntNeto', self.namespaces).text) if totales is not None and totales.find('ns0:MntNeto', self.namespaces) is not None else 0.0
                mnt_iva = float(totales.find('ns0:IVA', self.namespaces).text) if totales is not None and totales.find('ns0:IVA', self.namespaces) is not None else 0.0
                mnt_total = float(totales.find('ns0:MntTotal', self.namespaces).text) if totales is not None and totales.find('ns0:MntTotal', self.namespaces) is not None else 0.0
                
                rows.append({
                    'folio': folio,
                    'monto_neto': mnt_neto,
                    'monto_iva': mnt_iva,
                    'monto_total': mnt_total,
                    'fecha_emision': fecha,
                    'emisor_rut': rut,
                    'emisor_nombre': nombre
                })
            except Exception as e:
                logger.error(f"Error parsing {f}: {e}")
                
        if rows:
            df = pd.DataFrame(rows)
            df = df.drop_duplicates(subset=['folio'])
            self.db.execute("DELETE FROM dte_truth_v1")
            
            for _, r in df.iterrows():
                self.db.execute("""
                    INSERT INTO dte_truth_v1 (folio, monto_neto, monto_iva, monto_total, fecha_emision, emisor_rut, emisor_nombre)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [r['folio'], r['monto_neto'], r['monto_iva'], r['monto_total'], r['fecha_emision'], r['emisor_rut'], r['emisor_nombre']])
            
            logger.info(f"Loaded {len(df)} DTEs into dte_truth_v1.")
            
    def run_match(self):
        sql = '''
            SELECT l.folio_xml, c.monto, c.tipo_movimiento
            FROM marketplace_ledger_clasificado_v1 c
            JOIN marketplace_ledger_v1 l ON c.id_transaccion = l.id_transaccion
            WHERE c.marketplace='ML' 
            AND l.folio_xml IS NOT NULL
            AND c.tipo_movimiento NOT IN ('INGRESO_VENTA', 'DEVOLUCION', 'PAGO')
        '''
        ledger = self.db.query(sql)
        if ledger.empty:
            logger.warning("No folio_xml found in ledger.")
            return
            
        def extract_folio(f_str):
            if not f_str or '-' not in str(f_str): return None
            try:
                return str(int(str(f_str).split('-')[-1]))
            except:
                return None
                
        ledger['folio'] = ledger['folio_xml'].apply(extract_folio)
        ledger = ledger[ledger['folio'].notnull()]
        
        ledger_agg = ledger.groupby('folio')['monto'].sum().reset_index()
        ledger_agg['monto'] = ledger_agg['monto'].abs()
        
        dte = self.db.query("SELECT folio, monto_total FROM dte_truth_v1")
        if dte.empty:
            logger.warning("No DTEs found in DB.")
            return
            
        merged = pd.merge(ledger_agg, dte, on='folio', how='inner')
        merged['delta'] = merged['monto'] - merged['monto_total']
        
        merged['status'] = merged['delta'].apply(lambda d: 'MATCH' if abs(d) <= 2 else 'MISMATCH')
        
        matches = len(merged[merged['status'] == 'MATCH'])
        mismatches = len(merged[merged['status'] == 'MISMATCH'])
        logger.info(f"Matched: {matches}, Mismatched: {mismatches}")
        
        for _, r in merged.iterrows():
            if r['status'] == 'MISMATCH':
                self.db.execute("""
                    INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken)
                    VALUES (?, ?, ?, ?)
                """, ['ML', 'DTE_MATCH_CHECK', f"Folio {r['folio']}: Ledger={r['monto']} vs DTE={r['monto_total']} (Delta={r['delta']})", 'FLAG_FOR_REVIEW'])
        
        return merged

if __name__ == '__main__':
    matcher = DTEMatcher()
    matcher.load_dtes()
    res = matcher.run_match()
    if res is not None:
        print(res.head(20))
