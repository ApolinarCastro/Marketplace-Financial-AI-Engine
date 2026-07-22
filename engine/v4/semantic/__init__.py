"""Semantic Registry — canonical definitions for all financial business metrics.

DEFINE ONCE — USE EVERYWHERE.

Every metric is defined in canonical_semantics.METRIC_REGISTRY with:
  name, meaning, source, granularity, dimensions, exclusions, sign, version,
  owner, evidence.

All consumers (API, Dashboard, Copilot, Evidence) MUST call SemanticRegistry
to resolve metric definitions — never hardcode formulas.
"""
from __future__ import annotations
from typing import Any

from engine.v4.domain.canonical_semantics import (
    METRIC_REGISTRY, METRIC_NAMES, MetricDefinition, CanonicalMetric,
    get_metric_definition, get_metrics_by_source, get_metrics_by_granularity,
    FinancialGroup, FINANCIAL_GROUP_META, PNL_ORDER,
    Marketplace, MARKETPLACE_META,
    CashRole, AmountSign,
    get_financial_group_meta, get_ledger_uniqueness_key,
    validate_financial_group, validate_marketplace,
)


class SemanticRegistry:
    """Canonical registry for all financial business metrics.

    All consumers MUST use this registry to resolve metric definitions.
    No consumer may hardcode formula logic that duplicates these definitions.
    """

    def __init__(self):
        self._metrics: dict[str, MetricDefinition] = dict(METRIC_REGISTRY)

    def list_metrics(self) -> list[dict[str, Any]]:
        """Return all registered metrics as serializable dicts."""
        return [{
            "name": m.name,
            "display_name": m.display_name,
            "description": m.description,
            "source_table": m.source_table,
            "granularity": m.granularity,
            "dimensions": m.dimensions,
            "exclusions": m.exclusions,
            "sign_convention": m.sign_convention,
            "formula_method": m.formula_method,
            "version": m.version,
            "owner": m.owner,
            "evidence": m.evidence,
            "is_derived": m.is_derived,
        } for m in self._metrics.values()]

    def get_metric(self, name: str) -> MetricDefinition | None:
        """Return canonical definition for a metric by name."""
        return self._metrics.get(name.lower())

    def get_metric_or_raise(self, name: str) -> MetricDefinition:
        m = self.get_metric(name)
        if m is None:
            raise ValueError(f"Unknown metric '{name}'. Available: {', '.join(self._metrics)}")
        return m

    def validate_no_duplicates(self) -> list[str]:
        """Return list of duplicate definition warnings. Should be empty."""
        names = list(self._metrics.keys())
        duplicates = []
        seen = set()
        for n in names:
            lower = n.lower()
            if lower in seen:
                duplicates.append(f"Duplicate metric name: {n}")
            seen.add(lower)
        return duplicates

    def get_metric_names(self) -> list[str]:
        return list(self._metrics.keys())

    def get_metrics_by_domain(self, domain: str) -> list[MetricDefinition]:
        """Return metrics belonging to a domain (pnl, cash, derived)."""
        if domain == "pnl":
            return [m for m in self._metrics.values()
                    if m.name in ("ventas", "devoluciones", "costos_marketplace",
                                  "disponible", "ganancia_final")]
        if domain == "cash":
            return [m for m in self._metrics.values()
                    if m.name in ("tesoreria", "pendiente_cobro")]
        if domain == "derived":
            return [m for m in self._metrics.values() if m.is_derived]
        return []


def get_consumer_contract(consumer: str) -> dict[str, str]:
    """Return which metrics each consumer should expose and via which method.

    Validates the DEFINE ONCE principle: no consumer duplicates a formula.
    """
    contracts = {
        "financial_engine": {
            "role": "PROVIDER — single computation authority",
            "metrics": {m: METRIC_REGISTRY[m].formula_method for m in METRIC_NAMES},
        },
        "api": {
            "role": "PASS-THROUGH — calls FinancialEngine, no recalculation",
            "metrics": {m: f"FinancialEngine.{METRIC_REGISTRY[m].formula_method.split('.')[-1].split('(')[0]}" for m in METRIC_NAMES},
        },
        "dashboard": {
            "role": "CONSUMER — displays only, no calculation",
            "metrics": {m: "DISPLAY_ONLY" for m in METRIC_NAMES},
        },
        "copilot": {
            "role": "CONSUMER — explains via FinancialEngine, never recalculates",
            "metrics": {m: f"FinancialEngine.{METRIC_REGISTRY[m].formula_method.split('.')[-1].split('(')[0]}" for m in METRIC_NAMES},
        },
        "evidence_orchestrator": {
            "role": "CONSUMER — queries FinancialEngine public contracts, no own SQL",
            "metrics": {m: f"Fe.{METRIC_REGISTRY[m].formula_method.split('.')[-1].split('(')[0]}" for m in METRIC_NAMES},
        },
    }
    return contracts.get(consumer, {})


__all__ = [
    "SemanticRegistry",
    "get_consumer_contract",
    "METRIC_REGISTRY", "METRIC_NAMES", "MetricDefinition", "CanonicalMetric",
    "get_metric_definition", "get_metrics_by_source", "get_metrics_by_granularity",
    "FinancialGroup", "FINANCIAL_GROUP_META", "PNL_ORDER",
    "Marketplace", "MARKETPLACE_META",
    "CashRole", "AmountSign",
    "get_financial_group_meta", "get_ledger_uniqueness_key",
    "validate_financial_group", "validate_marketplace",
]
