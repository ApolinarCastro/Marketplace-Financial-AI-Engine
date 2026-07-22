"""
settlement_layer_contract.py — Certified Pydantic models for Settlement layer.

Groups with include_in_settlement=true from taxonomy.
"""
from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class SettlementGroupTotal(BaseModel):
    financial_group: str
    total: float
    record_count: int
    operational_contribution: float = 0.0


class SettlementSummary(BaseModel):
    marketplace: str
    period_label: str
    period_start: date
    period_end: date | None = None
    settlement_total: float
    group_totals: list[SettlementGroupTotal]
    total_records: int


class SettlementLayerQuery(BaseModel):
    marketplace: str
    periodo: str | None = None
