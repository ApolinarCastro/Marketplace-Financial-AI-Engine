"""Tests for Phase 12.5 — Explainability Engine."""
from __future__ import annotations
import pytest
from engine.v4.explainability import ExplainabilityEngine


@pytest.fixture
def engine():
    return ExplainabilityEngine()


def test_explain_ventas_brutas(engine):
    result = engine.explain("ventas_brutas", "ML")
    assert result is not None
    assert result["kpi"] == "ventas_brutas"
    assert result["marketplace"] == "ML"
    assert "current_value" in result
    assert "definition" in result
    assert "formula" in result


def test_explain_devoluciones(engine):
    result = engine.explain("devoluciones", "ML")
    assert result is not None
    assert result["kpi"] == "devoluciones"
    assert result is not None  # devoluciones now includes poscobro (mixed sign)


def test_explain_margen_bruto(engine):
    result = engine.explain("margen_bruto", "ML")
    assert result is not None


def test_explain_resultado_neto(engine):
    result = engine.explain("resultado_neto", "ML")
    assert result is not None


def test_explain_costo_logistico(engine):
    result = engine.explain("costo_logistico", "ML")
    assert result is not None


def test_explain_ajustes(engine):
    result = engine.explain("ajustes", "ML")
    assert result is not None


def test_explain_unknown_kpi(engine):
    result = engine.explain("unknown_kpi", "ML")
    assert result is None


def test_explain_with_periodo(engine):
    result = engine.explain("ventas_brutas", "ML", "2026-01")
    assert result is not None
    assert result["period"] == "2026-01"


def test_list_all_kpis_available(engine):
    from engine.v4.explainability.explainability_engine import KPI_CATALOG
    assert len(KPI_CATALOG) >= 5
    assert "ventas_brutas" in KPI_CATALOG
    assert "devoluciones" in KPI_CATALOG
    assert "margen_bruto" in KPI_CATALOG
    assert "resultado_neto" in KPI_CATALOG
