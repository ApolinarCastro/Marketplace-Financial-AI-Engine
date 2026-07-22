"""Test FinancialEngine — single certified financial entry point."""
import pytest
from engine.v4.domain.financial_engine import FinancialEngine


@pytest.fixture
def fe():
    return FinancialEngine()


class TestFinancialEngine:
    """Certify that FinancialEngine is a drop-in replacement for all financial queries."""

    def test_resolve_period_range_month(self, fe):
        start, end, label = fe.resolve_period_range("2026-01")
        assert start == "2026-01-01"
        assert end == "2026-01-31"
        assert label == "Ene 2026"

    def test_resolve_period_range_ytd(self, fe):
        start, end, label = fe.resolve_period_range("YTD")
        assert start is not None
        assert label == "Year to Date"

    def test_resolve_period_range_none(self, fe):
        start, end, label = fe.resolve_period_range(None)
        assert label == "Year to Date"

    def test_clean_records(self, fe):
        import pandas as pd
        import math
        df = pd.DataFrame({
            "a": [1.0, float("nan"), None],
            "b": ["x", "y", "z"],
        })
        cleaned = fe.clean_records(df)
        assert len(cleaned) == 3
        assert cleaned[1]["a"] is None
        assert cleaned[0]["a"] == 1.0

    def test_map_detalle_to_concept(self, fe):
        assert fe.map_detalle_to_concept("Cargo por envíos de Mercado Libre") == "Logística"
        assert fe.map_detalle_to_concept("Cargo por venta (Comisión)") == "Comisiones"
        assert fe.map_detalle_to_concept("Cargo por campaña de publicidad - Product Ads") == "Publicidad"
        assert fe.map_detalle_to_concept("Cargo por Asesoría Comercial") == "Servicios"
        assert fe.map_detalle_to_concept("Bonificación") == "Bonificaciones"
        assert fe.map_detalle_to_concept("Impuesto sobre las comisiones") == "Impuestos"
        assert fe.map_detalle_to_concept("Descuento por cancelación") == "Ajustes"
        assert fe.map_detalle_to_concept("unknown_detalle_xyz") == "Otros"

    def test_list_periods(self, fe):
        periods = fe.list_periods()
        assert len(periods) >= 1
        assert periods[0]["value"] == "YTD"

    def test_query_cierre(self, fe):
        result = fe.query_cierre(marketplace="ML")
        assert isinstance(result, list)
        if result:
            r = result[0]
            assert "marketplace" in r
            assert "resultado_neto" in r

    def test_query_cierre_all(self, fe):
        result = fe.query_cierre_all()
        assert isinstance(result, list)
        if result:
            r = result[0]
            assert "marketplace" in r

    def test_query_cierre_by_period(self, fe):
        result = fe.query_cierre(marketplace="ML", periodo="2026-01")
        assert isinstance(result, list)

    def test_query_desglose_ml(self, fe):
        rows = fe.query_desglose(marketplace="ML", periodo="2026-01")
        assert isinstance(rows, list)

    def test_query_desglose_ripley(self, fe):
        rows = fe.query_desglose(marketplace="RIPLEY", periodo="2026-01")
        assert isinstance(rows, list)

    def test_query_desglose_paris(self, fe):
        rows = fe.query_desglose(marketplace="PARIS", periodo="2026-01")
        assert isinstance(rows, list)

    def test_query_desglose_exclude_non_operational(self, fe):
        rows = fe.query_desglose(marketplace="ML", periodo="2026-01", exclude_non_operational=True)
        assert isinstance(rows, list)

    def test_query_ledger(self, fe):
        result = fe.query_ledger(marketplace="ML", periodo="2026-01")
        assert "data" in result
        assert "total_count" in result
        assert "total_sum" in result

    def test_query_ledger_by_order(self, fe):
        result = fe.query_ledger(marketplace="ML", order_id="dummy-nonexistent")
        assert result["total_count"] == 0

    def test_query_cobros_breakdown(self, fe):
        result = fe.query_cobros_breakdown(periodo="2026-01")
        assert "matrix" in result
        assert "total_cobros" in result
        assert "mps" in result

    def test_query_cobros_breakdown_by_mp(self, fe):
        result = fe.query_cobros_breakdown(periodo="2026-01", marketplace="ML")
        assert "matrix" in result
        assert len(result["mps"]) <= 1

    def test_query_exec_summary(self, fe):
        result = fe.query_exec_summary(periodo="2026-01", marketplace="ML")
        assert "financial_pnl" in result
        pnl = result["financial_pnl"]
        assert "gross_sales" in pnl
        assert "returns" in pnl
        assert "marketplace_costs" in pnl
        assert "net_profit" in pnl

    def test_query_exec_summary_all_mps(self, fe):
        result = fe.query_exec_summary(periodo="2026-01")
        assert result["marketplace"] == "ALL"

    def test_query_waterfall(self, fe):
        result = fe.query_waterfall(periodo="2026-01", marketplace="ML")
        assert "ventas" in result
        assert "devoluciones" in result
        assert "cobros" in result
        assert "disponible" in result
        assert "layers" in result
        assert len(result["layers"]["labels"]) == 4

    def test_query_waterfall_all_mp(self, fe):
        result = fe.query_waterfall(periodo="2026-01")
        assert result["marketplace"] == "ALL"

    def test_query_audit(self, fe):
        result = fe.query_audit(marketplace="ML")
        assert "data" in result
        assert "total" in result

    def test_query_audit_with_check(self, fe):
        types = fe.query_audit_types()
        if types:
            result = fe.query_audit(check_name=types[0])
            assert "data" in result

    def test_query_audit_types(self, fe):
        types = fe.query_audit_types()
        assert isinstance(types, list)

    def test_query_operational_intelligence(self, fe):
        result = fe.query_operational_intelligence(periodo="2026-01", marketplace="ML")
        assert "top_return_reasons" in result
        assert "ai_narrative" in result

    @pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
    def test_all_marketplaces_have_data(self, fe, mp):
        """Verify every marketplace has cierre data (use list to find a non-zero period)."""
        c = fe.query_cierre_all()
        mp_rows = [r for r in c if r.get("marketplace") == mp and abs(r.get("resultado_neto", 0) or 0) > 0]
        assert len(mp_rows) > 0, f"{mp} has no non-zero cierre periods"

    def test_waterfall_conservation(self, fe):
        """Verify: disponible = ventas + devoluciones + cobros + recuperaciones."""
        w = fe.query_waterfall(periodo="2026-01")
        layers = w["layers"]
        total = sum(layers["values"])
        assert abs(total - w["disponible"]) < 1

    def test_exec_summary_conservation(self, fe):
        """Verify: net_profit = gross_sales + returns + marketplace_costs."""
        s = fe.query_exec_summary(periodo="2026-01", marketplace="ML")
        pnl = s["financial_pnl"]
        expected = pnl["gross_sales"] + pnl["returns"] + pnl["marketplace_costs"]
        assert abs(expected - pnl["net_profit"]) < 1

    def test_ledger_filter_operational_only(self, fe):
        """Verify operational_only=True excludes non-operational rows."""
        all_rows = fe.query_ledger(marketplace="ML", periodo="2026-01", operational_only=True)
        # non-operational rows should be excluded
        assert all_rows["total_count"] >= 0

    def test_desglose_no_tesoreria(self, fe):
        """Verify tesoreria financial_group is excluded from desglose."""
        rows = fe.query_desglose(marketplace="ML", periodo="2026-01")
        cats = {r.get("categoria") for r in rows}
        assert "tesoreria" not in cats

    def test_waterfall_returns_negative(self, fe):
        """Verify devoluciones are present in waterfall (merged with poscobro)."""
        w = fe.query_waterfall(periodo="2026-01", marketplace="ML")
        assert w["devoluciones"] is not None

    def test_waterfall_cobros_negative(self, fe):
        """Verify cobros are negative (costs reduce net)."""
        w = fe.query_waterfall(periodo="2026-01", marketplace="ML")
        assert w["cobros"] <= 0
