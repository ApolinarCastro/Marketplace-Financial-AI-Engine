"""CanonicalFinancialSemantics — single typed contract for all financial domains.

This module is the SOLE source of truth for:
  - financial_group enumeration and metadata
  - cash_role enumeration
  - event_type enumeration
  - marketplace identifiers and per-MP uniqueness keys
  - amount_sign conventions
  - transaction grain definitions
  - business metric definitions (Ventas, Devoluciones, Costos, Margen, etc.)

Every metric is defined ONCE with canonical meaning, source, granularity,
and FinancialEngine reference. All consumers (API, Dashboard, Copilot,
Evidence) derive from this contract — never redefine.

Rule: DEFINE ONCE — USE EVERYWHERE.
Rule: DEC-019 is the sole truth of values.
Rule: No duplicated SQL. No frontend calculation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ═════════════════════════════════════════════════════════════════════════════
# Enums
# ═════════════════════════════════════════════════════════════════════════════

class FinancialGroup(str, Enum):
    """Eight certified financial groups. ORIGINAL SOURCE: marketplace_auditor.py:277-379."""
    INGRESOS = "ingresos"
    DEVOLUCIONES = "devoluciones"
    COSTOS_OPERACIONALES = "costos_operacionales"
    COSTOS_COMERCIALES = "costos_comerciales"
    RECUPERACIONES_Y_BONIFICACIONES = "recuperaciones_y_bonificaciones"
    AJUSTES = "ajustes"
    TESORERIA = "tesoreria"
    IMPUESTOS = "impuestos"


class CashRole(str, Enum):
    """Source: CASH_ROLE_REGISTRY_V1."""
    REAL_CASH = "REAL_CASH"
    ACCRUAL = "ACCRUAL"
    PASS_THROUGH = "PASS_THROUGH"
    MIRROR_ZERO = "MIRROR_ZERO"
    UNASSIGNED = "UNASSIGNED"


class EventType(str, Enum):
    """Source: EVENT_REGISTRY_V2."""
    ROOT_EVENT = "ROOT_EVENT"
    MECHANISM = "MECHANISM"
    SETTLEMENT = "SETTLEMENT"
    UNASSIGNED = "UNASSIGNED"


class Marketplace(str, Enum):
    """Five active marketplaces."""
    ML = "ML"
    PARIS = "PARIS"
    RIPLEY = "RIPLEY"
    FALABELLA = "FALABELLA"
    SHOPIFY = "SHOPIFY"


class AmountSign(str, Enum):
    """Sign convention for monto in financial_group context."""
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    VARIABLE = "VARIABLE"


# ═════════════════════════════════════════════════════════════════════════════
# Dataclasses
# ═════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class FinancialGroupMeta:
    """Metadata for a single financial group."""
    display_name: str
    pnl_order: int
    amount_sign: AmountSign
    canonical_cash_role: CashRole
    description: str = ""


@dataclass(frozen=True)
class UniquenessKey:
    """Defines the real uniqueness constraint for a table within a marketplace."""
    table: str
    key_fields: list[str]
    rationale: str = ""


@dataclass(frozen=True)
class MarketplaceMeta:
    """Metadata for a single marketplace."""
    name: str
    display_name: str
    ledger_uniqueness: UniquenessKey
    has_signal_taxonomy: bool = False


# ═════════════════════════════════════════════════════════════════════════════
# Registries (single source of truth)
# ═════════════════════════════════════════════════════════════════════════════

FINANCIAL_GROUP_META: dict[FinancialGroup, FinancialGroupMeta] = {
    FinancialGroup.INGRESOS: FinancialGroupMeta(
        display_name="Ingresos",
        pnl_order=1,
        amount_sign=AmountSign.POSITIVE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Ingresos por ventas brutas del marketplace",
    ),
    FinancialGroup.DEVOLUCIONES: FinancialGroupMeta(
        display_name="Devoluciones",
        pnl_order=2,
        amount_sign=AmountSign.NEGATIVE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Devoluciones, reembolsos y reversos",
    ),
    FinancialGroup.COSTOS_OPERACIONALES: FinancialGroupMeta(
        display_name="Costos Operacionales",
        pnl_order=3,
        amount_sign=AmountSign.NEGATIVE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Costos de logística, envío y operación",
    ),
    FinancialGroup.COSTOS_COMERCIALES: FinancialGroupMeta(
        display_name="Costos Comerciales",
        pnl_order=4,
        amount_sign=AmountSign.NEGATIVE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Comisiones, publicidad y costos de venta",
    ),
    FinancialGroup.RECUPERACIONES_Y_BONIFICACIONES: FinancialGroupMeta(
        display_name="Recuperaciones y Bonificaciones",
        pnl_order=5,
        amount_sign=AmountSign.POSITIVE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Recuperaciones de inventario y bonificaciones logísticas",
    ),
    FinancialGroup.AJUSTES: FinancialGroupMeta(
        display_name="Ajustes",
        pnl_order=6,
        amount_sign=AmountSign.VARIABLE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Ajustes, multas, compensaciones y cargos varios",
    ),
    FinancialGroup.TESORERIA: FinancialGroupMeta(
        display_name="Tesorería",
        pnl_order=7,
        amount_sign=AmountSign.VARIABLE,
        canonical_cash_role=CashRole.REAL_CASH,
        description="Movimientos de tesorería y settlement (no P&L)",
    ),
    FinancialGroup.IMPUESTOS: FinancialGroupMeta(
        display_name="Impuestos",
        pnl_order=8,
        amount_sign=AmountSign.VARIABLE,
        canonical_cash_role=CashRole.ACCRUAL,
        description="Impuestos sobre comisiones",
    ),
}

# Canonical P&L order (financial_group values in display order)
PNL_ORDER: list[str] = [
    "ingresos",
    "devoluciones",
    "costos_operacionales",
    "costos_comerciales",
    "recuperaciones_y_bonificaciones",
    "ajustes",
    "tesoreria",
    "impuestos",
]

# Per-marketplace ledger uniqueness keys
# Real ledger uniqueness = (id_transaccion, archivo_origen) for PARIS/RIPLEY
# because source files overlap at month boundaries.
# ML = id_transaccion alone (validated 0 duplicates).
# FALABELLA = id_transaccion alone (109 groups in same file — real data quality).
MARKETPLACE_META: dict[Marketplace, MarketplaceMeta] = {
    Marketplace.ML: MarketplaceMeta(
        name="ML",
        display_name="Mercado Libre",
        ledger_uniqueness=UniquenessKey(
            table="marketplace_ledger_v1",
            key_fields=["id_transaccion"],
            rationale="ML loader generates unique id_transaccion per row. No cross-file overlaps.",
        ),
        has_signal_taxonomy=True,
    ),
    Marketplace.PARIS: MarketplaceMeta(
        name="PARIS",
        display_name="Paris",
        ledger_uniqueness=UniquenessKey(
            table="marketplace_ledger_v1",
            key_fields=["id_transaccion", "archivo_origen", "detalle"],
            rationale="Full grain = (id_transaccion, archivo_origen, detalle). "
                      "Cross-file pipeline overlaps (same detalle, different files) are differentiated "
                      "by archivo_origen. Intra-file duplicates (test fixtures) by detalle.",
        ),
        has_signal_taxonomy=True,
    ),
    Marketplace.RIPLEY: MarketplaceMeta(
        name="RIPLEY",
        display_name="Ripley",
        ledger_uniqueness=UniquenessKey(
            table="marketplace_ledger_v1",
            key_fields=["id_transaccion", "archivo_origen"],
            rationale="Same order appears in parallel FF CSV files. "
                      "(id_transaccion, archivo_origen) = real unique grain.",
        ),
        has_signal_taxonomy=True,
    ),
    Marketplace.FALABELLA: MarketplaceMeta(
        name="FALABELLA",
        display_name="Falabella",
        ledger_uniqueness=UniquenessKey(
            table="marketplace_ledger_v1",
            key_fields=["id_transaccion", "detalle"],
            rationale="FALABELLA loader generates one row per concept per order. "
                      "Grain = (id_transaccion, detalle). Cross-file check via archivo_origen.",
        ),
        has_signal_taxonomy=True,
    ),
    Marketplace.SHOPIFY: MarketplaceMeta(
        name="SHOPIFY",
        display_name="Shopify",
        ledger_uniqueness=UniquenessKey(
            table="marketplace_ledger_v1",
            key_fields=["id_transaccion"],
            rationale="Not yet loaded. Default to id_transaccion.",
        ),
        has_signal_taxonomy=False,
    ),
}


def get_ledger_uniqueness_key(marketplace: str) -> list[str]:
    """Return the canonical uniqueness key fields for ledger transaction dedup."""
    mp = marketplace.upper() if marketplace else ""
    try:
        return list(MARKETPLACE_META[Marketplace(mp)].ledger_uniqueness.key_fields)
    except (KeyError, ValueError):
        return ["id_transaccion"]


def get_financial_group_meta(group: str) -> FinancialGroupMeta | None:
    """Return metadata for a financial group string."""
    try:
        return FINANCIAL_GROUP_META.get(FinancialGroup(group.lower()))
    except (KeyError, ValueError):
        return None


# ═════════════════════════════════════════════════════════════════════════════
# Metric definitions — DEFINE ONCE, USE EVERYWHERE
# ═════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class MetricDefinition:
    """Canonical definition of a single business metric.

    Every metric references a FinancialEngine method. No consumer
    (API/Dashboard/Copilot/Evidence) may redefine the formula.
    """
    name: str
    display_name: str
    description: str
    source_table: str
    granularity: str
    dimensions: list[str]
    exclusions: list[str]
    sign_convention: str
    formula_method: str
    formula_description: str
    version: str
    owner: str = "FinancialEngine"
    evidence: str = ""
    is_derived: bool = False


@dataclass(frozen=True)
class CanonicalMetric:
    """Runtime metric value with provenance."""
    name: str
    value: float
    period: str
    marketplace: str | None = None
    source_method: str = ""
    unit: str = "CLP"


METRIC_REGISTRY: dict[str, MetricDefinition] = {
    "ventas": MetricDefinition(
        name="ventas",
        display_name="Ventas (Gross Sales)",
        description="Suma de montos de ingresos operacionales del marketplace, neta de devoluciones de ingresos",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo", "financial_group"],
        exclusions=["Non-operational records (include_in_operational_pnl=0)", "NOISE detalle values"],
        sign_convention="POSITIVE",
        formula_method="FinancialEngine.query_exec_summary().gross_sales",
        formula_description="SUM(monto WHERE LOWER(financial_group)='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 [AND signal_filter])",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="PHASE_14_LEDGER_CATEGORY_RECONCILIATION",
    ),
    "devoluciones": MetricDefinition(
        name="devoluciones",
        display_name="Devoluciones (Returns)",
        description="Suma de montos de devoluciones, reembolsos y reversos operacionales",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo", "financial_group"],
        exclusions=["Non-operational records", "NOISE detalle values"],
        sign_convention="NEGATIVE",
        formula_method="FinancialEngine.query_exec_summary().returns",
        formula_description="SUM(monto WHERE LOWER(financial_group)='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 [AND signal_filter])",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="PHASE_14_LEDGER_CATEGORY_RECONCILIATION",
    ),
    "costos_marketplace": MetricDefinition(
        name="costos_marketplace",
        display_name="Costos Marketplace",
        description="Suma de todos los costos operacionales del marketplace: costos operacionales, comerciales, logisticos, comisiones, ajustes y recuperaciones",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo", "financial_group", "detalle"],
        exclusions=["Non-operational records", "NOISE detalle values", "Tesorería", "Impuestos"],
        sign_convention="NEGATIVE",
        formula_method="FinancialEngine.query_exec_summary().marketplace_costs",
        formula_description="SUM(monto WHERE LOWER(financial_group) IN ('costos_operacionales','costos_comerciales','costos_logisticos','comisiones','ajustes','recuperaciones_y_bonificaciones') AND COALESCE(include_in_operational_pnl,1)=1 [AND signal_filter])",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="PHASE_14_LEDGER_CATEGORY_RECONCILIATION",
    ),
    "disponible": MetricDefinition(
        name="disponible",
        display_name="Disponible (Resultado Neto)",
        description="Resultado neto operacional = ventas + devoluciones + costos + recuperaciones. También llamado Ganancia Final.",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo"],
        exclusions=["Non-operational records", "Tesorería", "Impuestos"],
        sign_convention="VARIABLE",
        formula_method="FinancialEngine.query_waterfall().disponible",
        formula_description="ventas + devoluciones + cobros + recuperaciones (post-computed from 4 CASE sums with op_pnl=1 and signal filter)",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="PHASE_12C_WATERFALL_CERTIFICATION",
    ),
    "margen": MetricDefinition(
        name="margen",
        display_name="Margen Neto",
        description="Porcentaje de Ganancia Final sobre Ventas Brutas. Margen = (disponible / ventas) * 100",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo"],
        exclusions=["No aplica — derived metric"],
        sign_convention="POSITIVE (percentage)",
        formula_method="DERIVED: (disponible / ventas) * 100",
        formula_description="(FinancialEngine.query_waterfall().disponible / FinancialEngine.query_exec_summary().gross_sales) * 100",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="G5.6_REVENUE_ENGINE_CERTIFICATION",
        is_derived=True,
    ),
    "tesoreria": MetricDefinition(
        name="tesoreria",
        display_name="Tesorería",
        description="Movimientos de tesorería y settlement. No forma parte del P&L operacional. Representa flujos de caja reales.",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo", "detalle"],
        exclusions=["Operational P&L records"],
        sign_convention="VARIABLE",
        formula_method="FinancialEngine.query_ledger(financial_group='tesoreria')",
        formula_description="SUM(monto WHERE LOWER(financial_group)='tesoreria')",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION",
    ),
    "pendiente_cobro": MetricDefinition(
        name="pendiente_cobro",
        display_name="Pendiente de Cobro",
        description="Montos registrados en tesorería pendientes de liquidación.",
        source_table="marketplace_ledger_v1",
        granularity="period",
        dimensions=["marketplace", "periodo", "detalle"],
        exclusions=["P&L records", "Settled amounts"],
        sign_convention="POSITIVE",
        formula_method="FinancialEngine.query_ledger(financial_group='tesoreria', detalle='A pagar')",
        formula_description="SUM(monto WHERE LOWER(financial_group)='tesoreria' AND LOWER(detalle) IN ('a pagar', 'pago pendiente'))",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="GAP_NOT_CERTIFIED — No dedicated endpoint. No settlement/bank linkage available. Uses treasury fallback only.",
    ),
    "ganancia_final": MetricDefinition(
        name="ganancia_final",
        display_name="Ganancia Final",
        description="GAP. Sin definición financiera certificada en este modelo. No hay evidencia normativa (DEC, reporte gerencial, KPI oficial) que lo vincule a Disponible/Resultado Neto. No confundir con Disponible (resultado neto operacional certificado).",
        source_table="N/A",
        granularity="N/A",
        dimensions=["N/A"],
        exclusions=[],
        sign_convention="N/A",
        formula_method="GAP — No existe método certificado. No se asume equivalencia con disponible ni ningún otro KPI certificado.",
        formula_description="GAP — Sin fórmula certificada. Requiere definición de negocio y evidencia normativa.",
        version="1.0.0",
        owner="FinancialEngine",
        evidence="GAP — Sin evidencia de negocio que vincule Ganancia Final a KPIs certificados.",
        is_derived=False,
    ),
}


METRIC_NAMES: list[str] = list(METRIC_REGISTRY.keys())


def get_metric_definition(name: str) -> MetricDefinition | None:
    """Return canonical metric definition by name."""
    return METRIC_REGISTRY.get(name.lower())


def get_metrics_by_source(table: str) -> list[MetricDefinition]:
    """Return all metrics sourced from a given table."""
    return [m for m in METRIC_REGISTRY.values() if m.source_table == table]


def get_metrics_by_granularity(granularity: str) -> list[MetricDefinition]:
    """Return all metrics with a given granularity."""
    return [m for m in METRIC_REGISTRY.values() if m.granularity == granularity]


# ═════════════════════════════════════════════════════════════════════════════
# Validator helpers
# ═════════════════════════════════════════════════════════════════════════════

def validate_financial_group(value: str | None) -> str | None:
    """Return the value if valid financial_group, None otherwise."""
    if value is None:
        return None
    try:
        FinancialGroup(value.lower())
        return value
    except (ValueError, AttributeError):
        return None


def validate_marketplace(value: str | None) -> str | None:
    """Return uppercase marketplace if valid, None otherwise."""
    if value is None:
        return None
    try:
        Marketplace(value.upper())
        return value.upper()
    except (ValueError, AttributeError):
        return None
