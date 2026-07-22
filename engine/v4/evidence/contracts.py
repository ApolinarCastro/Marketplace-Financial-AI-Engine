from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceLink:
    source_identifier: str
    source_type: str
    target_identifier: str
    target_type: str
    engine_used: str
    method_used: str
    confidence: str
    marketplace: str | None = None
    periodo: str | None = None
    financial_group: str | None = None
    detalle: str | None = None
    monto: float | None = None
    folio_xml: str | None = None
    archivo_origen: str | None = None


@dataclass
class ClosingContribution:
    participating: bool
    closing_batch: str | None = None
    closing_period: str | None = None
    financial_group: str | None = None
    operational_pnl: bool = True
    reconciliation_status: str = "NO_VERIFICADO"
    certification_status: str = "NO_VERIFICADO"


@dataclass
class CashTraceStatus:
    settlement_id: str | None = None
    settlement_amount: float | None = None
    settlement_date: str | None = None
    payment_id: str | None = None
    bank_deposit_id: str | None = None
    cash_status: str = "NO_DISPONIBLE"


@dataclass
class CoverageMetric:
    source: str
    target: str
    coverage_pct: float
    source_total: float
    matched: float
    method: str
    engine_used: str
    method_used: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class GapReport:
    gap_id: str
    marketplace: str
    description: str
    root_cause: str
    impact: str
    priority: str  # ALTA | MEDIA | BAJA
    status: str = "ABIERTO"


@dataclass
class EvidenceResult:
    marketplace: str
    periodo: str | None
    trace: list[EvidenceLink] = field(default_factory=list)
    closing: ClosingContribution | None = None
    coverage: list[CoverageMetric] = field(default_factory=list)
    gaps: list[GapReport] = field(default_factory=list)
    cash_trace: CashTraceStatus | None = None
