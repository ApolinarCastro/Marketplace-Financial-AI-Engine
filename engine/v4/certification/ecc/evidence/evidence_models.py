from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import hashlib
import json

@dataclass(frozen=True)
class EvidenceObject:
    evidence_level: str
    chain_type: str
    certification_status: str
    validation_trace: List[Dict[str, Any]] = field(default_factory=list)
    document_gaps: List[str] = field(default_factory=list)
    confidence: str = "DETERMINISTIC"
    evidence_schema_version: str = "1.0"
    evidence_hash: Optional[str] = field(default=None, init=False)

    def __post_init__(self):
        # We need a deterministic hash.
        # frozen=True prevents direct assignment, so we use object.__setattr__
        hash_dict = {
            "evidence_level": self.evidence_level,
            "chain_type": self.chain_type,
            "certification_status": self.certification_status,
            "validation_trace": self.validation_trace,
            "document_gaps": self.document_gaps,
            "confidence": self.confidence,
            "evidence_schema_version": self.evidence_schema_version
        }
        hash_str = json.dumps(hash_dict, sort_keys=True)
        sha256 = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()
        object.__setattr__(self, 'evidence_hash', sha256)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_level": self.evidence_level,
            "chain_type": self.chain_type,
            "certification_status": self.certification_status,
            "validation_trace": self.validation_trace,
            "document_gaps": self.document_gaps,
            "confidence": self.confidence,
            "evidence_schema_version": self.evidence_schema_version,
            "evidence_hash": self.evidence_hash
        }
