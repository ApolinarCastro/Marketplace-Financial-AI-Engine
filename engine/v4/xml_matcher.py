"""
Meli DTE Matcher — Automated XML Certification
Links marketplace_ledger_v1 with Facturacion/*.xml per marketplace
"""
import glob
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
from engine.v4.database import DatabaseV4

logger = logging.getLogger("meli.xml_matcher")

NAMESPACE = {"sii": "http://www.sii.cl/SiiDte"}

class MeliXMLMatcher:
    def __init__(self, marketplace='ML'):
        self.db = DatabaseV4.get()
        self.ns = NAMESPACE
        self.marketplace = marketplace.upper()
        if self.marketplace == 'ML':
            ml_raw = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\ML")
            doc_dir = ml_raw / "Documentos Recepcionados"
            fact_dir = ml_raw / "Facturacion"
            self.raw_dir = doc_dir if doc_dir.exists() else fact_dir
        elif self.marketplace == 'PARIS':
            self.raw_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\PARIS\Facturacion")
        else:
            raise ValueError(f"Unsupported marketplace: {marketplace}")

    def extract_dtes(self, base_path: str | Path | None = None) -> pd.DataFrame:
        """Parse all XML files in Facturacion and return a summary DataFrame."""
        if base_path is None:
            base_path = self.raw_dir
        
        files = glob.glob(str(base_path / "*.xml"))
        logger.info(f"Escaneando {len(files)} archivos XML para {self.marketplace}...")
        
        extracted = []
        for fpath in files:
            try:
                # Some files have encoding issues, latin-1 usually works for DTEs
                with open(fpath, "r", encoding="ISO-8859-1") as f:
                    xml_content = f.read()
                
                # Simple parsing
                root = ET.fromstring(xml_content)
                
                # Finding DTE tags
                for dte in root.findall(".//{http://www.sii.cl/SiiDte}DTE") or root.findall(".//DTE"):
                    id_doc = dte.find(".//{http://www.sii.cl/SiiDte}IdDoc") or dte.find(".//IdDoc")
                    totales = dte.find(".//{http://www.sii.cl/SiiDte}Totales") or dte.find(".//Totales")
                    emisor = dte.find(".//{http://www.sii.cl/SiiDte}Emisor") or dte.find(".//Emisor")
                    
                    if id_doc is not None and totales is not None:
                        folio = id_doc.findtext(".//{http://www.sii.cl/SiiDte}Folio") or id_doc.findtext("Folio")
                        fecha = id_doc.findtext(".//{http://www.sii.cl/SiiDte}FchEmis") or id_doc.findtext("FchEmis")
                        monto = totales.findtext(".//{http://www.sii.cl/SiiDte}MntTotal") or totales.findtext("MntTotal")
                        rut_emisor = emisor.findtext(".//{http://www.sii.cl/SiiDte}RUTEmisor") or emisor.findtext("RUTEmisor")
                        
                        extracted.append({
                            "folio": folio,
                            "fecha_emision": fecha,
                            "monto_total": float(monto or 0),
                            "rut_emisor": rut_emisor,
                            "archivo_xml": Path(fpath).name
                        })
            except Exception as e:
                logger.debug(f"Error parseando {Path(fpath).name}: {e}")
        
        return pd.DataFrame(extracted)

    def run_matching(self):
        """Link DTEs to Ledger for the specific marketplace."""
        dtes = self.extract_dtes()
        if dtes.empty:
            logger.warning(f"No se extrajeron DTEs de los archivos XML para {self.marketplace}.")
            return 0
        
        logger.info(f"DTEs extraídos: {len(dtes)}. Iniciando vinculación para {self.marketplace}...")
        
        matches_found = 0
        for idx, row in dtes.iterrows():
            folio = row['folio']
            monto = row['monto_total']
            fecha = row['fecha_emision']
            
            self.db.execute("""
                UPDATE marketplace_ledger_v1
                SET folio_xml = ?, estado_xml = 'CERTIFICADO'
                WHERE ABS(monto) = ? 
                  AND fecha BETWEEN CAST(? AS DATE) - INTERVAL 7 DAY AND CAST(? AS DATE) + INTERVAL 7 DAY
                  AND folio_xml IS NULL
                  AND marketplace = ?
            """, [folio, monto, fecha, fecha, self.marketplace])
            
        # Count total certificates at the end for this marketplace
        res = self.db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE estado_xml = 'CERTIFICADO' AND marketplace = ?", [self.marketplace])
        return int(res['n'].iloc[0])

if __name__ == "__main__":
    matcher = MeliXMLMatcher()
    n = matcher.run_matching()
    print(f"Certificadas {n} transacciones.")