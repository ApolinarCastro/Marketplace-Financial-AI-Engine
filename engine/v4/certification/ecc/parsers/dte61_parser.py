from .base_parser import BaseParser
from typing import Dict, Any

class DTE61Parser(BaseParser):
    """Parser for Nota de Crédito Electrónica (61)"""
    def parse(self, root: Any) -> Dict[str, Any]:
        raw_data = super().parse(root)
        
        # Tipo 61 MUST have references (to the modified invoice). 
        # This is already extracted by base_parser's _extract_references.
        # We don't add heuristics here to invent logic, we just rely on standard extraction
        # but could flag if references are empty, though that's an ECC Validator role, not extractor.
        
        return raw_data
