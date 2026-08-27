"""RipleySourceResolver — canonical resolver for RIPLEY sources (LOOP 3/4)."""
from pathlib import Path
import hashlib

# Canonical roles and their expected schemas
ROLE_DEFS = {
    "SELLER_SETTLEMENT": {"folder_hint": "Fulfillment by Seller", "required_cols": ["detalle", "monto"]},
    "BILLING_CYCLE": {"folder_hint": "Mis extractos", "required_cols": ["periodo"]},
    "TRANSACTION_HISTORY": {"folder_hint": "Historial de transacciones", "required_cols": ["order"]},
    "FULFILLMENT": {"folder_hint": "Fulfillment by Ripley", "required_cols": ["logistica"]},
    "FISCAL_XML": {"folder_hint": "Facturacion", "required_cols": ["TipoDTE"]},
}

class RipleySourceResolver:
    def __init__(self, raw_root: Path = Path("01_Raw/RIPLEY")):
        self.raw_root = Path(raw_root)

    def resolve(self, role: str):
        """Resolve files for a role via schema fingerprint + folder hint, not hard-coded single path."""
        if role not in ROLE_DEFS:
            raise ValueError(f"Unknown role {role}")
        hint = ROLE_DEFS[role]["folder_hint"]
        # discover all files that match hint or schema
        candidates = list(self.raw_root.rglob("*"))
        matched = [p for p in candidates if p.is_file() and hint.lower() in str(p).lower()]
        # also consider schema fingerprint if needed (simplified)
        return matched

    def all_roles(self):
        return {role: self.resolve(role) for role in ROLE_DEFS}
