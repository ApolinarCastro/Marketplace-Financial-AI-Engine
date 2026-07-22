"""
reconciliation_contracts.py — Pydantic models for the Reconciliation Engine.

All outputs are validated, typed, and serialize to JSON for API consumption.
Zero financial logic. Zero database queries. Pure data contracts.
"""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field


CertificationStatus = Literal[
    "CERTIFICADO",
    "PARCIAL",
    "PENDIENTE",
    "ERROR",
    "FINANCIAL_INTEGRITY_BROKEN",
]


class ReconciliationAlert(BaseModel):
    marketplace: str
    period: str
    level: str
    rule: str
    impact_amount: float
    record_count: int
    sql_query: str
    evidence: str


class LevelResult(BaseModel):
    level: str = Field(description="Level name (INTERNA|OPERACIONAL|TESORERÍA|DOCUMENTAL)")
    status: str = Field(description="PASS|ALERTA|ERROR")
    delta: float = Field(description="Absolute difference between source and target")
    source_total: float = Field(description="Total from source A")
    target_total: float = Field(description="Total from source B")
    alerts: list[ReconciliationAlert] = Field(default_factory=list)


class ReconciliationMetrics(BaseModel):
    reconciliation_delta: float = 0.0
    taxonomy_coverage: float = 100.0
    document_coverage: float = 0.0
    orphan_records: int = 0
    certification_status: CertificationStatus = "PENDIENTE"


class ReconciliationResult(BaseModel):
    marketplace: str
    period: str
    certification_status: CertificationStatus
    delta: float
    operational_total: float
    settlement_total: float
    treasury_total: float
    taxonomy_coverage: float
    document_coverage: float
    orphan_records: int
    total_records: int
    alerts: list[ReconciliationAlert] = Field(default_factory=list)
    levels: dict[str, LevelResult] = Field(default_factory=dict)
    metrics: ReconciliationMetrics = Field(default_factory=ReconciliationMetrics)
    engine_version: str = "1.0.0"
