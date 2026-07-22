"""ECC Payload Definition"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ECCPayload:
    document_type: Optional[str] = None
    marketplace: Optional[str] = None
    issuer_tax_id: Optional[str] = None
    receiver_tax_id: Optional[str] = None
    folio: Optional[str] = None
    issue_date: Optional[str] = None
    currency: str = "CLP"
    net_amount: Optional[int] = None
    vat_amount: Optional[int] = None
    exempt_amount: Optional[int] = None
    total_amount: Optional[int] = None
    references: List[Dict[str, Any]] = field(default_factory=list)
    items: List[Dict[str, Any]] = field(default_factory=list)
    electronic_certificate: Optional[Dict[str, Any]] = None
    chain_type: Optional[str] = None
    marketplace_metadata: Dict[str, Any] = field(default_factory=dict)
    capability_matrix_version: str = "1.0"
    normalization_version: str = "1.0"
    evidence_object: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "marketplace": self.marketplace,
            "issuer_tax_id": self.issuer_tax_id,
            "receiver_tax_id": self.receiver_tax_id,
            "folio": self.folio,
            "issue_date": self.issue_date,
            "currency": self.currency,
            "net_amount": self.net_amount,
            "vat_amount": self.vat_amount,
            "exempt_amount": self.exempt_amount,
            "total_amount": self.total_amount,
            "references": self.references,
            "items": self.items,
            "electronic_certificate": self.electronic_certificate,
            "evidence_object": self.evidence_object,
            "chain_type": self.chain_type,
            "marketplace_metadata": self.marketplace_metadata,
            "capability_matrix_version": self.capability_matrix_version,
            "normalization_version": self.normalization_version
        }
