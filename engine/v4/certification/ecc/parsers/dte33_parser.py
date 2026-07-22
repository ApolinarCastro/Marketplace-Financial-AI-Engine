from .base_parser import BaseParser
from typing import Dict, Any

class DTE33Parser(BaseParser):
    """Parser for Factura Electrónica (33)"""
    def parse(self, root: Any) -> Dict[str, Any]:
        # Standard implementation applies perfectly to 33
        return super().parse(root)
