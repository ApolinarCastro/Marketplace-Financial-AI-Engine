"""Deterministic XML to ECC mapping via Parser Registry"""
from typing import Dict, Any

from .parsers.parser_registry import ParserRegistry

class ECCMapping:
    def __init__(self):
        try:
            from lxml import etree
            self.etree = etree
            self.has_deps = True
        except ImportError:
            self.has_deps = False

        self.sii_namespace = "http://www.sii.cl/SiiDte"
        self.nsmap = {'sii': self.sii_namespace}
        self.registry = ParserRegistry()

    def _get_tipo_dte(self, root) -> str:
        nodes = root.xpath('//sii:Encabezado/sii:IdDoc/sii:TipoDTE', namespaces=self.nsmap)
        if not nodes:
            nodes = root.xpath('//Encabezado/IdDoc/TipoDTE')
            
        if nodes:
            if hasattr(nodes[0], 'text'):
                return nodes[0].text.strip() if nodes[0].text else None
            if isinstance(nodes[0], str):
                return nodes[0].strip()
        return None

    def extract(self, xml_content: str) -> Dict[str, Any]:
        """
        Executes deterministic XPath extractions based on the specific parser.
        """
        if not self.has_deps:
            return {}

        try:
            root = self.etree.fromstring(xml_content.encode('utf-8') if isinstance(xml_content, str) else xml_content)
        except Exception:
            return {}

        tipo_dte = self._get_tipo_dte(root)
        parser = self.registry.get_parser(tipo_dte)
        
        return parser.parse(root)
