"""FinancialTraceability — evidence data model for RAW→Ledger→Cierre chain.

Every field is read-only metadata from public contracts.
Zero financial logic. Zero SQL.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class RawOrigin:
    file_name: str
    file_path: str
    sha256: str
    file_size_bytes: int
    row_index: int | None = None


@dataclass
class RegistryLink:
    execution_id: str
    ingested_at: str
    user: str
    loader: str | None = None
    pipeline: str | None = None
    records_inserted: int = 0
    execution_time_seconds: float | None = None


@dataclass
class EtlTransform:
    loader_version: str | None = None
    harness_version: str | None = None
    taxonomy_version: str | None = None
    execution_commit: str | None = None


@dataclass
class LedgerEntry:
    id_transaccion: str
    id_orden: str
    marketplace: str
    monto: float
    tipo_movimiento: str
    detalle: str
    archivo_origen: str
    financial_group: str | None = None
    include_in_operational_pnl: bool = True
    periodo: str | None = None


@dataclass
class ClassificationEntry:
    financial_group: str | None = None
    financial_subgroup: str | None = None
    clasificacion_operativa: str | None = None
    origen_clasificacion: str | None = None
    confianza_clasificacion: float | None = None
    taxonomy_version: str | None = None


@dataclass
class CierreSummary:
    periodo_inicio: str
    periodo_fin: str
    total_ingresos: float
    total_costos_operacionales: float
    total_costos_comerciales: float
    total_ajustes: float
    resultado_neto: float


@dataclass
class FinancialTraceability:
    raw: RawOrigin | None = None
    registry: RegistryLink | None = None
    etl: EtlTransform | None = None
    ledger: LedgerEntry | None = None
    classification: ClassificationEntry | None = None
    cierre: CierreSummary | None = None
    errors: list[str] = field(default_factory=list)
    traced_at: str = field(default_factory=lambda: datetime.now().isoformat())
