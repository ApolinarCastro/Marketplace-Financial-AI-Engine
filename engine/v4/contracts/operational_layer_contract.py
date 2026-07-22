"""
operational_layer_contract.py — Certified Pydantic models for Operational P&L layer.

Tracks include_in_operational_pnl = 1 records and their contributions.
"""
from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class OperationalPnlRow(BaseModel):
    marketplace: str
    financial_group: str
    detalle: str
    monto: float
    tipo_movimiento: str
    clasificacion_operativa: str | None = None


class OperationalGroupTotal(BaseModel):
    financial_group: str
    total: float
    record_count: int
    sign_behavior: str = "mixed"


class OperationalPnlSummary(BaseModel):
    marketplace: str
    period_label: str
    period_start: date
    period_end: date | None = None
    operational_total: float
    resultado_neto: float | None = None
    delta: float
    group_totals: list[OperationalGroupTotal]
    total_records: int
    status: str = Field(description="CERTIFICADO|PARCIAL|ERROR")


class OperationalLayerQuery(BaseModel):
    marketplace: str
    periodo: str | None = None
    financial_group: str | None = None
