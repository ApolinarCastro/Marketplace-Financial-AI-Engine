"""
ManagementClosingStatusService — single authority for closing status.
Derives from CertificationResultV3 + internal/external blockers only.
No direct RAW/ledger/XML queries.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ManagementClosingStatus:
    marketplace: str
    period: str
    certification_overall_status: str
    internal_actionable_alerts: int
    external_blockers: int
    closing_status: str
    closing_label: str
    closing_reason: str
    blocking_reasons: list
    next_actions: list
    contract_version: str = "ManagementClosingStatusV1"

class ManagementClosingStatusService:
    def derive(self, certification_overall_status: str, internal_actionable_alerts: int, external_blockers: int, marketplace: str, period: str) -> ManagementClosingStatus:
        # Normalize
        cert = certification_overall_status
        internal = internal_actionable_alerts or 0
        external = external_blockers or 0
        # CONFLICT
        if cert == "CONFLICT":
            return ManagementClosingStatus(
                marketplace=marketplace, period=period,
                certification_overall_status=cert,
                internal_actionable_alerts=internal, external_blockers=external,
                closing_status="CONFLICT", closing_label="CONFLICT",
                closing_reason="Material conflict in certification layers",
                blocking_reasons=["CONFLICT"], next_actions=["Resolve conflict"], contract_version="ManagementClosingStatusV1"
            )
        # INTERNAL ACTION overrides
        if internal > 0:
            return ManagementClosingStatus(
                marketplace=marketplace, period=period,
                certification_overall_status=cert,
                internal_actionable_alerts=internal, external_blockers=external,
                closing_status="OPEN_INTERNAL_ACTION", closing_label="OPEN_INTERNAL_ACTION",
                closing_reason=f"{internal} internal actionable alerts require correction",
                blocking_reasons=[f"{internal} internal alerts"], next_actions=["Resolve internal alerts"], contract_version="ManagementClosingStatusV1"
            )
        # EXTERNAL BLOCKER
        if external > 0:
            return ManagementClosingStatus(
                marketplace=marketplace, period=period,
                certification_overall_status=cert,
                internal_actionable_alerts=internal, external_blockers=external,
                closing_status="WAITING_EXTERNAL", closing_label="WAITING_EXTERNAL",
                closing_reason="Waiting for external dependency" + (" RIPLEY_FISCAL_SII_BRIDGE" if marketplace.upper()=="RIPLEY" else ""),
                blocking_reasons=["EXTERNAL_BLOCKER_RIPLEY_FISCAL_SII_BRIDGE" if marketplace.upper()=="RIPLEY" else "EXTERNAL_BLOCKER"],
                next_actions=["Wait for external source"], contract_version="ManagementClosingStatusV1"
            )
        # No blockers, derive from certification
        if cert == "FULLY_CERTIFIED":
            return ManagementClosingStatus(marketplace, period, cert, internal, external, "CLOSED_FULLY_CERTIFIED","CLOSED_FULLY_CERTIFIED","No blockers, fully certified",[],["Close period"], "ManagementClosingStatusV1")
        if cert == "PARTIALLY_CERTIFIED":
            return ManagementClosingStatus(marketplace, period, cert, internal, external, "CLOSED_PARTIALLY_CERTIFIED","CLOSED_PARTIALLY_CERTIFIED","Partially certified, no internal/external blockers",[],["Close with reservations"], "ManagementClosingStatusV1")
        if cert == "FINANCIAL_ONLY":
            return ManagementClosingStatus(marketplace, period, cert, internal, external, "CLOSED_FINANCIAL_ONLY","CLOSED_FINANCIAL_ONLY","Financial only",[],["Close financial"], "ManagementClosingStatusV1")
        if cert == "BLOCKED":
            return ManagementClosingStatus(marketplace, period, cert, internal, external, "BLOCKED","BLOCKED","Blocked",[],[], "ManagementClosingStatusV1")
        if cert == "NO_EVIDENCE":
            return ManagementClosingStatus(marketplace, period, cert, internal, external, "NOT_APPLICABLE","NOT_APPLICABLE","No evidence",[],[], "ManagementClosingStatusV1")
        return ManagementClosingStatus(marketplace, period, cert, internal, external, "NOT_APPLICABLE","NOT_APPLICABLE","Unknown",[],[], "ManagementClosingStatusV1")
