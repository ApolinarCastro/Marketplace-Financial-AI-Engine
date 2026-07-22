from typing import Dict, Type
from .base_parser import BaseParser
from .dte33_parser import DTE33Parser
from .dte43_parser import DTE43Parser
from .dte52_parser import DTE52Parser
from .dte61_parser import DTE61Parser

class ParserRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseParser]] = {
            "33": DTE33Parser,
            "43": DTE43Parser,
            "52": DTE52Parser,
            "61": DTE61Parser
        }

    def get_parser(self, document_type: str) -> BaseParser:
        """
        Returns the specific parser for the DTE type, or the BaseParser as a fallback.
        """
        parser_class = self._registry.get(str(document_type), BaseParser)
        return parser_class()
