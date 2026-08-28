"""
TransactionCertificationResultV3 — Canonical transactional certification contract.
Complements CertificationResultV3 (global). One authority for drawer.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class TFinancialStatus(str, Enum):
    FINANCIAL_CERTIFIED = "FINANCIAL_CERTIFIED"
    FINANCIAL_PARTIAL = "FINANCIAL_PARTIAL"
    FINANCIAL_BLOCKED = "FINANCIAL_BLOCKED"
    FINANCIAL_CONFLICT = "FINANCIAL_CONFLICT"

class TSettlementStatus(str, Enum):
    SETTLEMENT_CERTIFIED = "SETTLEMENT_CERTIFIED"
    SETTLEMENT_NOT_APPLICABLE = "SETTLEMENT_NOT_APPLICABLE"
    SETTLEMENT_MISSING = "SETTLEMENT_MISSING"
    SETTLEMENT_CONFLICT = "SETTLEMENT_CONFLICT"

class TDocumentStatus(str, Enum):
    DOCUMENT_LINKED = "DOCUMENT_LINKED"
    DOCUMENT_REFERENCE_ONLY = "DOCUMENT_REFERENCE_ONLY"
    DOCUMENT_MISSING = "DOCUMENT_MISSING"
    DOCUMENT_CONFLICT = "DOCUMENT_CONFLICT"

class TXmlStatus(str, Enum):
    XML_CERTIFIED = "XML_CERTIFIED"
    XML_PRESENT_NOT_CERTIFIED = "XML_PRESENT_NOT_CERTIFIED"
    XML_INVALID = "XML_INVALID"
    XML_NOT_LINKED = "XML_NOT_LINKED"
    XML_NOT_APPLICABLE = "XML_NOT_APPLICABLE"

class TFiscalStatus(str, Enum):
    FISCAL_CERTIFIED = "FISCAL_CERTIFIED"
    INSUFFICIENT_FISCAL_EVIDENCE = "INSUFFICIENT_FISCAL_EVIDENCE"
    FISCAL_BLOCKED_EXTERNAL = "FISCAL_BLOCKED_EXTERNAL"
    FISCAL_CONFLICT = "FISCAL_CONFLICT"
    FISCAL_NOT_APPLICABLE = "FISCAL_NOT_APPLICABLE"

class TOverallStatus(str, Enum):
    FULLY_CERTIFIED = "FULLY_CERTIFIED"
    PARTIALLY_CERTIFIED = "PARTIALLY_CERTIFIED"
    FINANCIAL_ONLY = "FINANCIAL_ONLY"
    BLOCKED = "BLOCKED"
    CONFLICT = "CONFLICT"
    NO_EVIDENCE = "NO_EVIDENCE"

class PipelineStage(str, Enum):
    NOT_RUN = "NOT_RUN"
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"

@dataclass
class TransactionCertificationResultV3:
    contract_version: str = "TransactionCertificationResultV3"
    transaction_id: str = ""
    marketplace: str = ""
    period: str = ""
    financial_status: TFinancialStatus = TFinancialStatus.FINANCIAL_CERTIFIED
    settlement_status: TSettlementStatus = TSettlementStatus.SETTLEMENT_NOT_APPLICABLE
    document_status: TDocumentStatus = TDocumentStatus.DOCUMENT_MISSING
    xml_status: TXmlStatus = TXmlStatus.XML_NOT_LINKED
    fiscal_status: TFiscalStatus = TFiscalStatus.INSUFFICIENT_FISCAL_EVIDENCE
    overall_status: TOverallStatus = TOverallStatus.NO_EVIDENCE
    overall_label: str = ""
    overall_reason: str = ""
    chain_type: str = ""
    chain_reason: str = ""
    chain_evidence: dict = field(default_factory=dict)
    document: dict = field(default_factory=dict)
    xml: dict = field(default_factory=dict)
    pipeline: dict = field(default_factory=dict)
    evidence_level: str = ""
    evidence_hash: str = ""
    confidence: str = ""
    amount: dict = field(default_factory=dict)
    reason_codes: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "contract_version": self.contract_version,
            "transaction_id": self.transaction_id,
            "marketplace": self.marketplace,
            "period": self.period,
            "financial_status": self.financial_status.value,
            "settlement_status": self.settlement_status.value,
            "document_status": self.document_status.value,
            "xml_status": self.xml_status.value,
            "fiscal_status": self.fiscal_status.value,
            "overall_status": self.overall_status.value,
            "overall_label": self.overall_label,
            "overall_reason": self.overall_reason,
            "chain_type": self.chain_type,
            "chain_reason": self.chain_reason,
            "chain_evidence": self.chain_evidence,
            "document": self.document,
            "xml": self.xml,
            "pipeline": self.pipeline,
            "evidence_level": self.evidence_level,
            "evidence_hash": self.evidence_hash,
            "confidence": self.confidence,
            "amount": self.amount,
            "reason_codes": self.reason_codes,
            # legacy aliases for drawer compat (temporary)
            "estado": self.overall_status.value,
            "certification_scope": self.chain_type,
            "tipo_dte": self.document.get("type", "-"),
            "folio": self.document.get("folio", "-"),
            "evidencia": {"hash": self.evidence_hash, "confidence": self.confidence, "level": self.overall_status.value},
            "tx_id": self.transaction_id,
        }
