import re
import duckdb
from pathlib import Path
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("surgical.xml")

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"

class XMLJustifier:
    def __init__(self, marketplace='ML'):
        self.conn = duckdb.connect(str(DB_PATH))
        self.marketplace = marketplace.upper()
        if self.marketplace == 'ML':
            ml_raw = ROOT / "01_Raw" / "ML"
            doc_dir = ml_raw / "Documentos Recepcionados"
            fact_dir = ml_raw / "Facturacion"
            self.XML_DIR = doc_dir if doc_dir.exists() else fact_dir
            self.auditor_marketplace = 'ML'
        elif self.marketplace == 'PARIS':
            self.XML_DIR = ROOT / "01_Raw" / "PARIS" / "Facturacion"
            self.auditor_marketplace = 'PARIS'
        else:
            raise ValueError(f"Unsupported marketplace: {marketplace}")

    def run(self):
        logger.info(f"Deep scanning XML files content for indexing for marketplace: {self.marketplace}...")
        xml_index = {} # folio -> status
        
        all_xmls = list(self.XML_DIR.glob("*.xml"))
        logger.info(f"Indexing {len(all_xmls)} XML files for {self.marketplace}...")
        
        for xp in all_xmls:
            try:
                # Read first 1000 bytes to find folio quickly or parse
                with open(xp, "r", encoding="latin-1") as f:
                    content = f.read(2048) # Enough to find Folio tag usually
                
                folio_match = re.search(r"<Folio>(\d+)</Folio>", content)
                tipo_match = re.search(r"<TipoDTE>(\d+)</TipoDTE>", content)
                
                if folio_match:
                    f = folio_match.group(1)
                    xml_index[f] = xp.name
                    if tipo_match:
                        # Preserve legacy composite key support like 033-0010762179
                        t = tipo_match.group(1).zfill(3)
                        composite_key = f"{t}-{f.zfill(10)}"
                        xml_index[composite_key] = xp.name
            except Exception as e:
                logger.warning(f"Error indexing {xp.name}: {e}")
        
        logger.info(f"Index built: {len(xml_index)} folios found in XML files for {self.marketplace}.")
        
        # Now match with ledger
        logger.info(f"Matching ledger folios with XML index for {self.marketplace}...")
        ledger_res = self.conn.execute("SELECT DISTINCT folio_xml FROM marketplace_ledger_v1 WHERE folio_xml IS NOT NULL AND marketplace = ?", [self.marketplace]).df()
        
        count_valid = 0
        for l_folio in ledger_res['folio_xml'].tolist():
            if l_folio in xml_index:
                # Update ledger
                self.conn.execute("""
                    UPDATE marketplace_ledger_v1 
                    SET estado_xml = 'CERTIFICADO',
                        asociacion_xml = ?
                    WHERE folio_xml = ?
                """, [xml_index[l_folio], l_folio])
                count_valid += 1
            else:
                self.conn.execute("""
                    UPDATE marketplace_ledger_v1 
                    SET estado_xml = 'SIN_RECURSO_XML' 
                    WHERE folio_xml = ?
                """, [l_folio])
        
        logger.info(f"Justification complete: {count_valid} transactions certified with XML evidence for {self.marketplace}.")
        
        # Move certified results to auditor view
        self.conn.execute("""
            INSERT INTO marketplace_auditoria_v1 (marketplace, check_name, condition_detected, action_taken)
            VALUES (?, 'justificacion_xml', 'Certificados ' || ? || ' folios fiscales', 'vincular evidencia legal')
        """, [self.auditor_marketplace, count_valid])
        
        self.conn.close()

if __name__ == "__main__":
    justifier = XMLJustifier()
    justifier.run()
