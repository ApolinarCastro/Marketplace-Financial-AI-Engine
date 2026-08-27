"""
CertificationResultV3 — Canonical public certification contract.

This is the EXTERNAL CONTRACT for certification status.
Internal engines (CertificationEngine, DocumentCertificationEngine) use their own states.
This adapter translates internal states to the canonical public contract.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class FinancialStatus(str, Enum):
    FINANCIAL_CERTIFIED = "FINANCIAL_CERTIFIED"
    FINANCIAL_PARTIAL = "FINANCIAL_PARTIAL"
    FINANCIAL_BLOCKED = "FINANCIAL_BLOCKED"
    FINANCIAL_CONFLICT = "FINANCIAL_CONFLICT"


class SettlementStatus(str, Enum):
    SETTLEMENT_CERTIFIED = "SETTLEMENT_CERTIFIED"
    SETTLEMENT_NOT_APPLICABLE = "SETTLEMENT_NOT_APPLICABLE"
    SETTLEMENT_MISSING = "SETTLEMENT_MISSING"
    SETTLEMENT_CONFLICT = "SETTLEMENT_CONFLICT"


class DocumentStatus(str, Enum):
    DOCUMENT_LINKED = "DOCUMENT_LINKED"
    DOCUMENT_REFERENCE_ONLY = "DOCUMENT_REFERENCE_ONLY"
    DOCUMENT_MISSING = "DOCUMENT_MISSING"
    DOCUMENT_CONFLICT = "DOCUMENT_CONFLICT"


class XmlStatus(str, Enum):
    XML_CERTIFIED = "XML_CERTIFIED"
    XML_PRESENT_NOT_CERTIFIED = "XML_PRESENT_NOT_CERTIFIED"
    XML_INVALID = "XML_INVALID"
    XML_NOT_LINKED = "XML_NOT_LINKED"
    XML_NOT_APPLICABLE = "XML_NOT_APPLICABLE"


class FiscalStatus(str, Enum):
    FISCAL_CERTIFIED = "FISCAL_CERTIFIED"
    INSUFFICIENT_FISCAL_EVIDENCE = "INSUFFICIENT_FISCAL_EVIDENCE"
    FISCAL_BLOCKED_EXTERNAL = "FISCAL_BLOCKED_EXTERNAL"
    FISCAL_CONFLICT = "FISCAL_CONFLICT"
    FISCAL_NOT_APPLICABLE = "FISCAL_NOT_APPLICABLE"


class OverallStatus(str, Enum):
    FULLY_CERTIFIED = "FULLY_CERTIFIED"
    PARTIALLY_CERTIFIED = "PARTIALLY_CERTIFIED"
    FINANCIAL_ONLY = "FINANCIAL_ONLY"
    BLOCKED = "BLOCKED"
    CONFLICT = "CONFLICT"
    NO_EVIDENCE = "NO_EVIDENCE"


@dataclass
class CertificationResultV3:
    """Canonical public certification result."""

    marketplace: str
    period: str

    # Layer statuses
    financial_status: FinancialStatus
    settlement_status: SettlementStatus
    document_status: DocumentStatus
    xml_status: XmlStatus
    fiscal_status: FiscalStatus

    # Overall derived status
    overall_status: OverallStatus
    overall_label: str
    overall_reason: str

    # Chain type for traceability
    chain_type: str

    # Evidence details
    evidence: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
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
            "evidence": self.evidence
        }


def derive_financial_status(cert_result, marketplace: str) -> FinancialStatus:
    """Derive financial status from CertificationEngine results.
    
    Reconciliation delta is a known structural issue that does not invalidate
    the core financial truth (ingresos, devoluciones, PNL equivalence).
    Per canonical contract: financial valid + fiscal evidence absent = PARTIALLY_CERTIFIED.
    """
    if not cert_result:
        return FinancialStatus.FINANCIAL_BLOCKED

    # Core financial truth checks: ingresos, devoluciones, PNL equivalence
    # These are the canonical financial truth indicators
    ingresos_claim = next((c for c in cert_result.claims if c.kpi == "INGRESOS"), None)
    dev_claim = next((c for c in cert_result.claims if c.kpi == "DEVOLUCIONES"), None)
    pnl_claim = next((c for c in cert_result.claims if c.kpi == "PNL_EQUIVALENCE"), None)
    op_pnl_claim = next((c for c in cert_result.claims if c.kpi == "OPERATIONAL_PNL"), None)

    ingresos_ok = ingresos_claim and ingresos_claim.status == "PASS"
    dev_ok = dev_claim and dev_claim.status == "PASS"
    pnl_ok = pnl_claim and pnl_claim.status == "PASS"
    op_pnl_ok = op_pnl_claim and op_pnl_claim.status == "PASS"

    # Core financial truth is certified if ingresos, devoluciones, and PNL equivalence are PASS
    # Reconciliation delta is a separate structural issue, not a core financial truth failure
    if ingresos_ok and dev_ok and pnl_ok:
        return FinancialStatus.FINANCIAL_CERTIFIED

    # Operational PNL also certified adds confidence
    if op_pnl_ok:
        return FinancialStatus.FINANCIAL_CERTIFIED

    # Check for partial financial data
    coverage_claim = next((c for c in cert_result.claims if c.kpi == "CLASSIFICATION_COVERAGE"), None)
    coverage_ok = coverage_claim and coverage_claim.status in ("PASS", "WARNING")

    if coverage_ok and (ingresos_ok or dev_ok):
        return FinancialStatus.FINANCIAL_PARTIAL

    return FinancialStatus.FINANCIAL_BLOCKED


def derive_settlement_status(doc_cert: dict, marketplace: str) -> SettlementStatus:
    """Derive settlement status from document certification."""
    if not doc_cert:
        return SettlementStatus.SETTLEMENT_NOT_APPLICABLE

    estado_legal = doc_cert.get("estado_legal", "")
    nivel_evidencia = doc_cert.get("nivel_evidencia", "")

    if "SETTLEMENT" in estado_legal or "SETTLEMENT" in nivel_evidencia:
        return SettlementStatus.SETTLEMENT_CERTIFIED

    # For marketplaces without settlement chain (ML, PARIS, FALABELLA)
    return SettlementStatus.SETTLEMENT_NOT_APPLICABLE


def derive_document_status(doc_cert: dict, marketplace: str) -> DocumentStatus:
    """Derive document status from document certification."""
    if not doc_cert:
        return DocumentStatus.DOCUMENT_MISSING

    estado_legal = doc_cert.get("estado_legal", "")
    cobertura = doc_cert.get("cobertura", 0)

    if "CERTIFIED" in estado_legal and cobertura >= 80:
        return DocumentStatus.DOCUMENT_LINKED
    elif "CERTIFIED" in estado_legal or "REFERENCE" in estado_legal:
        return DocumentStatus.DOCUMENT_REFERENCE_ONLY
    elif cobertura == 0:
        return DocumentStatus.DOCUMENT_MISSING
    else:
        return DocumentStatus.DOCUMENT_REFERENCE_ONLY


def derive_xml_status(doc_cert: dict, marketplace: str) -> XmlStatus:
    """Derive XML status from document certification."""
    if not doc_cert:
        return XmlStatus.XML_NOT_APPLICABLE

    cobertura = doc_cert.get("cobertura", 0)
    monto_elegible = doc_cert.get("monto_elegible", 0)
    estado_legal = doc_cert.get("estado_legal", "")

    if monto_elegible == 0:
        return XmlStatus.XML_NOT_APPLICABLE

    if "NOT_RUN" in estado_legal:
        return XmlStatus.XML_NOT_APPLICABLE

    if cobertura == 100:
        return XmlStatus.XML_CERTIFIED
    elif cobertura > 0:
        return XmlStatus.XML_PRESENT_NOT_CERTIFIED
    else:
        return XmlStatus.XML_NOT_LINKED


def derive_fiscal_status(doc_cert: dict, marketplace: str) -> FiscalStatus:
    """Derive fiscal status from document certification."""
    if not doc_cert:
        return FiscalStatus.FISCAL_NOT_APPLICABLE

    estado_legal = doc_cert.get("estado_legal", "")
    nivel_evidencia = doc_cert.get("nivel_evidencia", "")
    cobertura = doc_cert.get("cobertura", 0)
    monto_elegible = doc_cert.get("monto_elegible", 0)

    # RIPLEY: settlement chain exists but no SII DTE
    if "SETTLEMENT" in estado_legal and "SII" not in estado_legal and "DTE" not in estado_legal:
        return FiscalStatus.FISCAL_BLOCKED_EXTERNAL

    # ML/PARIS/FALABELLA with DTE coverage
    if "LEGAL_DOCUMENT" in estado_legal or "DOCUMENT_CHAIN" in estado_legal or "TRANSACTION_CHAIN" in estado_legal:
        if cobertura >= 80:
            return FiscalStatus.FISCAL_CERTIFIED
        elif cobertura > 0:
            return FiscalStatus.INSUFFICIENT_FISCAL_EVIDENCE
        else:
            return FiscalStatus.FISCAL_BLOCKED_EXTERNAL

    return FiscalStatus.INSUFFICIENT_FISCAL_EVIDENCE


def derive_overall_status(
    financial: FinancialStatus,
    settlement: SettlementStatus,
    document: DocumentStatus,
    xml: XmlStatus,
    fiscal: FiscalStatus
) -> tuple[OverallStatus, str, str]:
    """Derive overall status from layer statuses using canonical precedence.

    CRITICAL RULE: financial valid + fiscal evidence absent/incomplete = PARTIALLY_CERTIFIED (NOT FAILED/BLOCKED)
    """

    # CONFLICT takes highest precedence
    if (financial == FinancialStatus.FINANCIAL_CONFLICT or
        settlement == SettlementStatus.SETTLEMENT_CONFLICT or
        document == DocumentStatus.DOCUMENT_CONFLICT or
        xml == XmlStatus.XML_INVALID or
        fiscal == FiscalStatus.FISCAL_CONFLICT):
        return (OverallStatus.CONFLICT,
                "CONFLICT",
                "Material conflict detected in certification layers")

    # BLOCKED - process cannot complete (financial completely blocked)
    if financial == FinancialStatus.FINANCIAL_BLOCKED:
        return (OverallStatus.BLOCKED,
                "BLOCKED",
                "Certification process blocked: no financial truth established")

    # FISCAL_BLOCKED_EXTERNAL with certified financial = PARTIALLY_CERTIFIED (not BLOCKED)
    # This is the critical rule: financial truth exists but fiscal evidence is structurally unavailable
    if fiscal == FiscalStatus.FISCAL_BLOCKED_EXTERNAL and financial == FinancialStatus.FINANCIAL_CERTIFIED:
        return (OverallStatus.PARTIALLY_CERTIFIED,
                "PARTIALLY_CERTIFIED",
                "Financial truth certified; fiscal evidence blocked externally (e.g., settlement chain without SII DTE)")

    # FULLY_CERTIFIED - all required layers certified
    if (financial == FinancialStatus.FINANCIAL_CERTIFIED and
        document == DocumentStatus.DOCUMENT_LINKED and
        fiscal in (FiscalStatus.FISCAL_CERTIFIED, FiscalStatus.FISCAL_NOT_APPLICABLE)):
        return (OverallStatus.FULLY_CERTIFIED,
                "FULLY_CERTIFIED",
                "All certification layers complete and certified")

    # FINANCIAL_ONLY - financial certified but document/fiscal incomplete
    if (financial == FinancialStatus.FINANCIAL_CERTIFIED and
        (document != DocumentStatus.DOCUMENT_LINKED or
         fiscal == FiscalStatus.INSUFFICIENT_FISCAL_EVIDENCE)):
        return (OverallStatus.FINANCIAL_ONLY,
                "FINANCIAL_ONLY",
                "Financial truth certified; documentary/fiscal layers incomplete")

    # PARTIALLY_CERTIFIED - valid financial truth with partial documentary/fiscal
    if financial in (FinancialStatus.FINANCIAL_CERTIFIED, FinancialStatus.FINANCIAL_PARTIAL):
        return (OverallStatus.PARTIALLY_CERTIFIED,
                "PARTIALLY_CERTIFIED",
                "Financial truth valid; documentary/fiscal certification partial or blocked externally")

    # NO_EVIDENCE - nothing certified
    return (OverallStatus.NO_EVIDENCE,
            "NO_EVIDENCE",
            "Insufficient evidence for any certification layer")


def build_certification_result_v3(
    marketplace: str,
    period: str,
    cert_result,  # MarketplacesCertification from CertificationEngine
    doc_cert: dict,  # Document certification result
    chain_type: str
) -> CertificationResultV3:
    """Build canonical CertificationResultV3 from internal engine results."""

    financial = derive_financial_status(cert_result, marketplace)
    settlement = derive_settlement_status(doc_cert, marketplace)
    document = derive_document_status(doc_cert, marketplace)
    xml = derive_xml_status(doc_cert, marketplace)
    fiscal = derive_fiscal_status(doc_cert, marketplace)

    overall, label, reason = derive_overall_status(financial, settlement, document, xml, fiscal)

    evidence = {
        "financial": {
            "pass_rate": cert_result.pass_rate if cert_result else 0,
            "total_delta": cert_result.total_delta if cert_result else 0,
            "claims": [
                {"kpi": c.kpi, "status": c.status, "delta": c.delta}
                for c in cert_result.claims
            ] if cert_result else []
        },
        "document": doc_cert,
        "chain_type": chain_type
    }

    return CertificationResultV3(
        marketplace=marketplace,
        period=period,
        financial_status=financial,
        settlement_status=settlement,
        document_status=document,
        xml_status=xml,
        fiscal_status=fiscal,
        overall_status=overall,
        overall_label=label,
        overall_reason=reason,
        chain_type=chain_type,
        evidence=evidence
    )