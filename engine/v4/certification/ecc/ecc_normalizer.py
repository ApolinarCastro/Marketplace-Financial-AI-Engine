"""Deterministic Normalization of ECC Data"""
from typing import Dict, Any

class ECCNormalizer:
    def _safe_int(self, value: Any, default: int = 0) -> int:
        if not value:
            return default
        try:
            return int(round(float(value)))
        except ValueError:
            return default
            
    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            return default

    def _clean_rut(self, rut: str) -> str:
        if not rut:
            return ""
        return rut.strip().upper()
        
    def _clean_date(self, date_str: str) -> str:
        if not date_str:
            return ""
        return date_str.strip()

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes and type-casts raw string data from XML into strict types.
        """
        normalized = {
            "document_type": raw_data.get("document_type", ""),
            "issuer_tax_id": self._clean_rut(raw_data.get("issuer_tax_id", "")),
            "receiver_tax_id": self._clean_rut(raw_data.get("receiver_tax_id", "")),
            "folio": raw_data.get("folio", ""),
            "issue_date": self._clean_date(raw_data.get("issue_date", "")),
            "net_amount": self._safe_int(raw_data.get("net_amount")),
            "vat_amount": self._safe_int(raw_data.get("vat_amount")),
            "exempt_amount": self._safe_int(raw_data.get("exempt_amount")),
            "total_amount": self._safe_int(raw_data.get("total_amount")),
        }

        # Normalize items
        norm_items = []
        for item in raw_data.get("items", []):
            norm_items.append({
                "name": (item.get("name") or "").strip(),
                "qty": self._safe_float(item.get("qty")),
                "price": self._safe_float(item.get("price")),
                "amount": self._safe_int(item.get("amount"))
            })
        normalized["items"] = norm_items

        # Normalize references
        norm_refs = []
        for ref in raw_data.get("references", []):
            norm_refs.append({
                "type": (ref.get("type") or "").strip(),
                "folio": (ref.get("folio") or "").strip(),
                "date": self._clean_date(ref.get("date", "")),
                "reason": (ref.get("reason") or "").strip()
            })
        normalized["references"] = norm_refs

        return normalized
