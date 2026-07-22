from .base_parser import BaseParser
from typing import Dict, Any

class DTE52Parser(BaseParser):
    """Parser for Guía de Despacho Electrónica (52)"""
    def parse(self, root: Any) -> Dict[str, Any]:
        raw_data = super().parse(root)
        
        # Tipo 52 might have Transporte section
        patente = self._extract_text(root, '//sii:Encabezado/sii:Transporte/sii:Patente')
        rut_trans = self._extract_text(root, '//sii:Encabezado/sii:Transporte/sii:RUTTrans')
        
        if patente or rut_trans:
            trans_ref = {
                "type": "TRANSPORTE",
                "folio": patente or "N/A",
                "date": raw_data.get("issue_date"),
                "reason": f"RUTTrans:{rut_trans}"
            }
            raw_data["references"].append(trans_ref)

        return raw_data
