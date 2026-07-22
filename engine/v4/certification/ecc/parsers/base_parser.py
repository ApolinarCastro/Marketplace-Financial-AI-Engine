"""Base Parser for DTE Extraction"""
from typing import Dict, Any, List

class BaseParser:
    def __init__(self):
        self.sii_namespace = "http://www.sii.cl/SiiDte"
        self.nsmap = {'sii': self.sii_namespace}

    def _extract_text(self, root: Any, path: str, default: Any = None) -> Any:
        nodes = root.xpath(path, namespaces=self.nsmap)
        if not nodes:
            fallback_path = path.replace('sii:', '')
            nodes = root.xpath(f"//{fallback_path}")
            if not nodes:
                return default
        
        if hasattr(nodes[0], 'text'):
            return nodes[0].text.strip() if nodes[0].text else default
        
        if isinstance(nodes[0], str):
            return nodes[0].strip() if nodes[0] else default
            
        return default

    def _extract_common(self, root: Any) -> Dict[str, Any]:
        """
        Extracts fields common to all standard DTEs.
        """
        return {
            "document_type": self._extract_text(root, '//sii:Encabezado/sii:IdDoc/sii:TipoDTE'),
            "issuer_tax_id": self._extract_text(root, '//sii:Encabezado/sii:Emisor/sii:RUTEmisor'),
            "receiver_tax_id": self._extract_text(root, '//sii:Encabezado/sii:Receptor/sii:RUTRecep'),
            "folio": self._extract_text(root, '//sii:Encabezado/sii:IdDoc/sii:Folio'),
            "issue_date": self._extract_text(root, '//sii:Encabezado/sii:IdDoc/sii:FchEmis'),
            "net_amount": self._extract_text(root, '//sii:Encabezado/sii:Totales/sii:MntNeto'),
            "vat_amount": self._extract_text(root, '//sii:Encabezado/sii:Totales/sii:IVA'),
            "exempt_amount": self._extract_text(root, '//sii:Encabezado/sii:Totales/sii:MntExe'),
            "total_amount": self._extract_text(root, '//sii:Encabezado/sii:Totales/sii:MntTotal')
        }

    def _extract_items(self, root: Any) -> List[Dict[str, Any]]:
        items = []
        for detalle in root.xpath('//sii:Detalle', namespaces=self.nsmap) or root.xpath('//Detalle'):
            item = {
                "name": self._extract_text(detalle, 'sii:NmbItem') or self._extract_text(detalle, 'NmbItem'),
                "qty": self._extract_text(detalle, 'sii:QtyItem') or self._extract_text(detalle, 'QtyItem'),
                "price": self._extract_text(detalle, 'sii:PrcItem') or self._extract_text(detalle, 'PrcItem'),
                "amount": self._extract_text(detalle, 'sii:MontoItem') or self._extract_text(detalle, 'MontoItem')
            }
            items.append(item)
        return items

    def _extract_references(self, root: Any) -> List[Dict[str, Any]]:
        references = []
        for ref in root.xpath('//sii:Referencia', namespaces=self.nsmap) or root.xpath('//Referencia'):
            reference = {
                "type": self._extract_text(ref, 'sii:TpoDocRef') or self._extract_text(ref, 'TpoDocRef'),
                "folio": self._extract_text(ref, 'sii:FolioRef') or self._extract_text(ref, 'FolioRef'),
                "date": self._extract_text(ref, 'sii:FchRef') or self._extract_text(ref, 'FchRef'),
                "reason": self._extract_text(ref, 'sii:RazonRef') or self._extract_text(ref, 'RazonRef')
            }
            references.append(reference)
        return references

    def parse(self, root: Any) -> Dict[str, Any]:
        """
        Parses the document. To be overridden by specific types or used as fallback.
        """
        raw_data = self._extract_common(root)
        raw_data["items"] = self._extract_items(root)
        raw_data["references"] = self._extract_references(root)
        return raw_data
