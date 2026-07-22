from .base_parser import BaseParser
from typing import Dict, Any

class DTE43Parser(BaseParser):
    """Parser for Liquidación Factura Electrónica (43)"""
    def parse(self, root: Any) -> Dict[str, Any]:
        raw_data = super().parse(root)
        
        # Tipo 43 usually contains Liquidacion and comisiones. 
        # For ECC normalization, we extract ValComNeto and ValComExe into references 
        # if they exist, or append them as a special item to be parsed later.
        
        # Extract comisiones
        val_com_neto = self._extract_text(root, '//sii:Encabezado/sii:Liquidacion/sii:ValComNeto')
        val_com_iva = self._extract_text(root, '//sii:Encabezado/sii:Liquidacion/sii:ValComIVA')
        val_com_exe = self._extract_text(root, '//sii:Encabezado/sii:Liquidacion/sii:ValComExe')
        
        # If comisiones exist, we append a specialized reference or metadata (mapped to references here)
        if val_com_neto or val_com_exe:
            comision_ref = {
                "type": "COMISION_LIQUIDACION",
                "folio": "N/A",
                "date": raw_data.get("issue_date"),
                "reason": f"Neto:{val_com_neto}|IVA:{val_com_iva}|Exe:{val_com_exe}"
            }
            raw_data["references"].append(comision_ref)

        return raw_data
