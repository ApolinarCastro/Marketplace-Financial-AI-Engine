"""
executive_contract.py — Certified Pydantic models for Executive Dashboard.

All KPIs are traceable to certified sources (cierre_financiero_v1, ledger_clasificado_v1).
"""
from __future__ import annotations
from pydantic import BaseModel, Field


class ExecutiveKpi(BaseModel):
    label: str
    value: float
    marketplace: str = "ALL"
    change_vs_previous: float | None = None
    source: str = Field(description="Certified source table/contract")
    tooltip: str = ""


class ExecutiveSummary(BaseModel):
    ventas_netas: float = 0.0
    devoluciones: float = 0.0
    cobros: float = 0.0
    disponible: float = 0.0
    marketplaces: list[ExecutiveKpi] = Field(default_factory=list)
    period: str = ""


class WaterfallStep(BaseModel):
    label: str
    value: float
    marketplace: str = "ALL"
    color: str = "#ccc"
    is_total: bool = False


class CobrosConcept(BaseModel):
    concepto: str
    total: float
    breakdown: dict[str, float] = Field(default_factory=dict)


class WaterfallResponse(BaseModel):
    steps: list[WaterfallStep]
    concepts: list[CobrosConcept] = Field(default_factory=list)


class ExecutiveQuery(BaseModel):
    periodo: str | None = None
    marketplace: str | None = None
