"""FileDetector — Stage 0 of ingestion pipeline.

Detects file properties: SHA256 hash, marketplace hint, document type, period, file size.
No DB writes. Pure file inspection.
"""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
from typing import Any


class FileDetector:

    MARKETPLACE_PATTERNS: list[tuple[str, str]] = [
        (r"(?i)(?:^|[\s_/\\-])ML(?:[\s_/\\-]|$)", "ML"),
        (r"(?i)(?:^|[\s_/\\-])MELI(?:[\s_/\\-]|$)", "ML"),
        (r"(?i)mercadolibre", "ML"),
        (r"(?i)mercado\s*libre", "ML"),
        (r"(?i)(?:^|[\s_/\\-])PARIS(?:[\s_/\\-]|$)", "PARIS"),
        (r"(?i)(?:^|[\s_/\\-])CENCOSUD(?:[\s_/\\-]|$)", "PARIS"),
        (r"(?i)(?:^|[\s_/\\-])RIPLEY(?:[\s_/\\-]|$)", "RIPLEY"),
        (r"(?i)(?:^|[\s_/\\-])FALABELLA(?:[\s_/\\-]|$)", "FALABELLA"),
        (r"(?i)(?:^|[\s_/\\-])SHOPIFY(?:[\s_/\\-]|$)", "SHOPIFY"),
    ]

    DOC_TYPE_PATTERNS: list[tuple[str, str]] = [
        (r"(?i)factura(cion)?", "facturacion"),
        (r"(?i)poscobro", "poscobro"),
        (r"(?i)liberacion(es)?", "liberaciones"),
        (r"(?i)liquidacion.*ff", "liquidacion_ff"),
        (r"(?i)liquidacion", "liquidacion"),
        (r"(?i)dte.*proveedor", "dte"),
        (r"(?i)recepcionado(s)?", "dte"),
        (r"(?i)\.xml$", "dte"),
        (r"(?i)dropshipping", "dropshipping"),
        (r"(?i)fulfillment", "fulfillment"),
        (r"(?i)pedido(s)?", "pedidos"),
        (r"(?i)ventas?\s*totales?", "ventas_totales"),
        (r"(?i)transaccion(es)?", "transacciones"),
        (r"(?i)orden(es)?", "ordenes"),
    ]

    MONTH_MAP = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    }

    # Each entry: (regex, year_group, month_group_or_name)
    # year_group=0 means use group(0) matched text for month extraction
    PERIOD_PATTERNS: list[tuple[str, int, int] | tuple[str, int, str]] = [
        (r"(?i)(\d{4})-(\d{2})", 1, 2),
        (r"(?i)(\d{1,2})\s*(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s*(\d{4})", 3, 2),
        (r"(?i)(\d{4})\s*(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)", 1, 2),
        (r"(?i)(\d{4})/(\d{2})", 1, 2),
    ]

    def detect(self, file_path: str | Path, original_filename: str | None = None) -> dict[str, Any]:
        path = Path(file_path)
        fname = original_filename or path.name
        result: dict[str, Any] = {
            "file_name": fname,
            "file_path": str(path.resolve()),
            "sha256": self._compute_sha256(path),
            "file_size_bytes": path.stat().st_size if path.exists() else 0,
            "extension": path.suffix.lower(),
            "marketplace": self._detect_marketplace(fname),
            "document_type": self._detect_document_type(fname),
            "period": self._detect_period(fname),
        }
        return result

    def _compute_sha256(self, path: Path) -> str:
        try:
            return hashlib.sha256(path.read_bytes()).hexdigest()
        except Exception:
            return ""

    def _detect_marketplace(self, fname: str) -> str | None:
        for pattern, mp in self.MARKETPLACE_PATTERNS:
            m = re.search(pattern, fname)
            if m:
                return mp
        return None

    def _detect_document_type(self, fname: str) -> str | None:
        for pattern, dt in self.DOC_TYPE_PATTERNS:
            if re.search(pattern, fname):
                return dt
        return None

    def _detect_period(self, fname: str) -> str | None:
        for pattern, year_grp, month_grp in self.PERIOD_PATTERNS:
            m = re.search(pattern, fname)
            if not m:
                continue
            try:
                month_val = m.group(month_grp)
                year = int(m.group(year_grp))
                if month_val.isdigit():
                    return f"{year}-{int(month_val):02d}"
                matched_text = m.group(0).lower()
                for name, num in self.MONTH_MAP.items():
                    if name in matched_text:
                        return f"{year}-{num:02d}"
            except (ValueError, IndexError):
                continue
        return None
