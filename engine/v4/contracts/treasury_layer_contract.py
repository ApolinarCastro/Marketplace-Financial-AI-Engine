"""
treasury_layer_contract.py — Certified Pydantic models for Treasury/Cash layer.

Maps to financial_group='tesoreria' records: cash movements, payouts, settlements.
"""
from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class TreasuryRow(BaseModel):
    marketplace: str
    id_transaccion: str
    fecha: date
    detalle: str
    monto: float
    tipo_movimiento: str


class TreasurySummary(BaseModel):
    marketplace: str
    period_label: str
    period_start: date
    period_end: date | None = None
    treasury_total: float
    operational_pnl_total: float
    mirror_delta: float = Field(description="|operational + treasury| = expected ~0")
    record_count: int
    status: str


class TreasuryLayerQuery(BaseModel):
    marketplace: str
    periodo: str | None = None
