"""
financial_structure_contract.py — Certified Pydantic models for the Financial Structure layer.

Maps to marketplace_ledger_clasificado_v1 rows and financial_group taxonomy.
"""
from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class FinancialStructureRow(BaseModel):
    marketplace: str
    id_transaccion: str
    id_orden: str | None = None
    fecha: date
    detalle: str
    monto: float
    tipo_movimiento: str
    archivo_origen: str | None = None
    financial_group: str | None = None
    clasificacion_operativa: str | None = None
    include_in_operational_pnl: bool = True


class FinancialGroupTotal(BaseModel):
    financial_group: str
    display_label: str
    total: float
    record_count: int
    sign_behavior: str = "mixed"


class FinancialStructureSummary(BaseModel):
    marketplace: str
    period_start: date
    period_end: date | None = None
    period_label: str
    total_records: int
    group_totals: list[FinancialGroupTotal]
    grand_total: float
    taxonomy_coverage: float = Field(ge=0, le=100)


class FinancialStructureQuery(BaseModel):
    marketplace: str
    periodo: str | None = None
    financial_group: str | None = None
    include_non_operational: bool = False
