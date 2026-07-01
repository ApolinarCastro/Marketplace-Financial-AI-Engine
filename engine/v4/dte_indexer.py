import xml.etree.ElementTree as ET
from pathlib import Path
import logging
import pandas as pd
from engine.v4.database import DatabaseV4

logger = logging.getLogger("meli.dte_indexer")

class DTEIndexer:
    def __init__(self, marketplace='ML'):
        self.db = DatabaseV4.get()
        if marketplace.upper() == 'ML':
            self.raw_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\ML\Documentos Recepcionados")
        elif marketplace.upper() == 'PARIS':
            self.raw_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\PARIS\Facturacion")
        elif marketplace.upper() == 'FALABELLA':
            self.raw_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Documentos Recepcionados")
        elif marketplace.upper() == 'RIPLEY':
            self.raw_dir = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\RIPLEY\XML")
        else:
            raise ValueError(f"Unsupported marketplace: {marketplace}")
        self.marketplace = marketplace.upper()

    def parse_xml(self, xml_path):
        """Parses a single DTE XML and returns a dict with its header data."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Helper to find tag ignoring namespace
            def find_tag(element, tag_name):
                for child in element.iter():
                    if child.tag.endswith(tag_name):
                        return child.text
                return None
            
            folio = find_tag(root, 'Folio')
            if not folio:
                return None
                
            tipo_dte = find_tag(root, 'TipoDTE')
            rut_emisor = find_tag(root, 'RUTEmisor')
            nombre_emisor = find_tag(root, 'RznSoc')
            fecha_emision = find_tag(root, 'FchEmis')
            rut_receptor = find_tag(root, 'RUTRecep')
            
            # Montos
            neto = find_tag(root, 'MntNeto')
            iva = find_tag(root, 'IVA')
            if not iva:
                iva = find_tag(root, 'MntIVA')
            total = find_tag(root, 'MntTotal')
            
            return {
                'folio': folio,
                'monto_neto': float(neto) if neto else 0.0,
                'monto_iva': float(iva) if iva else 0.0,
                'monto_total': float(total) if total else 0.0,
                'fecha_emision': fecha_emision,
                'emisor_rut': rut_emisor,
                'emisor_nombre': nombre_emisor,
                'tipo_dte': tipo_dte,
                'rut_receptor': rut_receptor,
                'marketplace': self.marketplace
            }
        except Exception as e:
            logger.error(f"Error parsing XML {xml_path.name}: {e}")
            return None
    
    def run(self):
        logger.info(f"Starting DTE Indexing process for marketplace: {self.marketplace}...")
        xml_files = list(self.raw_dir.glob("*.xml"))
        
        records = []
        for f in xml_files:
            data = self.parse_xml(f)
            if data:
                records.append(data)
        
        if not records:
            logger.info("No valid XML records found to index.")
            return 0
        
        df = pd.DataFrame(records)
        df = df.drop_duplicates(subset=['folio'])
        
        n = self.db.insert_df(df, "dte_truth_v1", dedup_cols=['folio'])
        logger.info(f"DTE Indexing completed for {self.marketplace}. {n} new legal records registered.")
        return n

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer_paris = DTEIndexer(marketplace='PARIS')
    indexer_paris.run()