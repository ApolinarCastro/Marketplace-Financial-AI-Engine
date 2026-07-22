"""Tests for Traceability Engine."""
import pytest
import pandas as pd
import math
from engine.v4.traceability.traceability_engine import (
    trace_transaction,
    search_transactions,
    trace_by_order,
    evidence_chain,
    traceability_summary,
    sap_reconciliation,
    _clean
)


class TestClean:
    """_clean() utility."""

    def test_clean_float_nan(self):
        r = _clean({"a": float("nan")})
        assert r["a"] is None

    def test_clean_float_inf(self):
        r = _clean({"a": float("inf")})
        assert r["a"] is None

    def test_clean_float_neg_inf(self):
        r = _clean({"a": float("-inf")})
        assert r["a"] is None

    def test_clean_pd_na(self):
        r = _clean({"a": pd.NA})
        assert r["a"] is None

    def test_clean_iso_date(self):
        import datetime
        r = _clean({"a": datetime.date(2026, 1, 15)})
        assert r["a"] == "2026-01-15"

    def test_clean_keeps_normal(self):
        r = _clean({"a": 123, "b": "hello"})
        assert r == {"a": 123, "b": "hello"}

    def test_clean_keeps_none(self):
        r = _clean({"a": None})
        assert r["a"] is None


class TestTraceTransaction:
    """trace_transaction() — by id."""

    def test_returns_valid_structure(self):
        """Always returns data/total keys regardless of existence."""
        result = trace_transaction("ML", "__nonexistent__")
        assert "data" in result
        assert "total" in result
        assert result["total"] == 0


class TestSearchTransactions:
    """search_transactions() — filtered search."""

    def test_search_by_marketplace_returns_structure(self):
        result = search_transactions(marketplace="ML", limit=5)
        assert "data" in result
        assert "meta" in result
        assert len(result["data"]) <= 5

    def test_search_all_marketplaces_returns_structure(self):
        result = search_transactions(limit=10)
        assert "data" in result
        assert "meta" in result
        assert 0 <= len(result["data"]) <= 10

    def test_search_with_query_returns_structure(self):
        result = search_transactions(query="ML", limit=5)
        assert "data" in result

    def test_search_includes_pagination_meta(self):
        result = search_transactions(limit=5)
        m = result["meta"]
        assert "offset" in m
        assert "limit" in m
        assert "total" in m
        assert isinstance(m["total"], int)

    def test_search_with_filters_ingresos(self):
        result = search_transactions(financial_group="ingresos", limit=5)
        assert "data" in result


class TestTraceByOrder:
    """trace_by_order() — by order_id."""

    def test_trace_by_order_returns_structure(self):
        result = trace_by_order("ML", "__nonexistent__")
        assert "data" in result


class TestEvidenceChain:
    """evidence_chain() — full 8-step evidence."""

    def test_evidence_chain_nonexistent_returns_empty(self):
        result = evidence_chain("ML", "__nonexistent__")
        assert result["total"] == 0

    def test_evidence_chain_structure_for_known_tx(self):
        # Find a real transaction first
        search = search_transactions(marketplace="ML", financial_group="ingresos", limit=1)
        if search["data"]:
            tx = search["data"][0]
            result = evidence_chain(tx["marketplace"], tx["id_transaccion"])
            assert "data" in result
            data = result["data"]
            assert isinstance(data, dict)
            assert "evidence_chain" in data
            assert len(data["evidence_chain"]) == 8

    def test_evidence_chain_layers_order(self):
        search = search_transactions(marketplace="ML", limit=1)
        if search["data"]:
            tx = search["data"][0]
            result = evidence_chain(tx["marketplace"], tx["id_transaccion"])
            layers = [s["layer"] for s in result["data"]["evidence_chain"]]
            assert layers == [
                "RAW", "ETL", "LEDGER", "CLASSIFICATION",
                "CIERRE", "XML", "SETTLEMENT", "AUDIT"
            ]


class TestTraceabilitySummary:
    """traceability_summary() — aggregate."""

    def test_summary_returns_data(self):
        result = traceability_summary()
        assert "data" in result
        # Should have at least one marketplace
        assert any(d.get("marketplace") == "ML" for d in result["data"])

    def test_summary_counts_are_positive(self):
        result = traceability_summary()
        ml_rows = [d for d in result["data"] if d["marketplace"] == "ML"]
        for d in ml_rows:
            assert d["count"] is not None and d["count"] >= 0

    def test_summary_includes_trace_status(self):
        result = traceability_summary()
        for d in result["data"]:
            assert d["trace_status"] in ("TRACED", "UNTRACED")
            assert d["document_status"] in ("DTE_CERTIFIED", "HAS_FOLIO", "NO_DOCUMENT")


class TestSAPReconciliation:
    """sap_reconciliation() — baseline metrics."""

    def test_sap_all_periods(self):
        result = sap_reconciliation()
        assert "data" in result
        assert "meta" in result
        assert result["meta"]["period"] == "ALL"

    def test_sap_specific_period(self):
        result = sap_reconciliation(period="2026-01")
        assert "data" in result
        assert result["meta"]["period"] == "2026-01"

    def test_sap_returns_marketplace_metrics(self):
        result = sap_reconciliation()
        for d in result["data"]:
            assert "marketplace" in d
            assert "total_transactions" in d
            assert d["total_transactions"] is not None
