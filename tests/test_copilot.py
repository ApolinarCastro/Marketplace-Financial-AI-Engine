"""Tests for Copilot (P39) — Financial Intelligence engine + dedicated page."""
from __future__ import annotations
import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)


class TestCopilotPage:
    def test_copilot_page_returns_200(self):
        r = client.get("/copilot")
        assert r.status_code == 200
        assert "Financial Copilot" in r.text

    def test_copilot_page_has_question_input(self):
        r = client.get("/copilot")
        assert "copilot-question" in r.text
        assert "askCopilot" in r.text

    def test_copilot_page_nav_links(self):
        r = client.get("/copilot")
        assert "/exec" in r.text
        assert "/app" in r.text


class TestCopilotHealthEndpoint:
    def test_health_endpoint_returns_200(self):
        r = client.get("/api/v4/financial-intelligence/health")
        assert r.status_code == 200

    def test_health_has_answer(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "answer" in data
        a = data["answer"]
        assert "summary" in a
        assert "is_profit" in a
        assert "delta" in a
        assert "delta_pct" in a

    def test_health_answer_has_mp_breakdown(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "breakdown" in data
        assert len(data["breakdown"]) > 0
        for mp in data["breakdown"]:
            assert "marketplace" in mp
            assert "rn" in mp
            assert "is_profit" in mp

    def test_health_has_explanation(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "explanation" in data
        assert "text" in data["explanation"]

    def test_health_has_evidence_chain(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "evidence" in data
        assert len(data["evidence"]) > 0
        for e in data["evidence"]:
            assert "marketplace" in e
            assert "source" in e
            assert "sql" in e
            assert "value" in e

    def test_health_evidence_has_components(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        for e in data["evidence"]:
            assert "components" in e
            assert len(e["components"]) >= 2

    def test_health_evidence_has_etl_info(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        for e in data["evidence"]:
            assert "etl" in e
            assert "pipeline" in e["etl"]
            assert e["etl"]["pipeline"] != ""

    def test_health_evidence_has_raw_sources(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        for e in data["evidence"]:
            assert "raw_sources" in e
            assert len(e["raw_sources"]) > 0

    def test_health_evidence_has_ledger_samples(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        for e in data["evidence"]:
            assert "ledger_samples" in e
            assert len(e["ledger_samples"]) > 0
            for s in e["ledger_samples"]:
                assert "id_transaccion" in s
                assert "monto" in s
                assert "detalle" in s

    def test_health_evidence_has_xml_info(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        for e in data["evidence"]:
            assert "xml" in e

    def test_health_has_period(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "period" in data

    def test_health_has_previous_period(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        assert "previous_period" in data

    def test_health_cross_mp_coverage(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        mps = {mp["marketplace"] for mp in data["breakdown"]}
        assert any(mp.lower() == "ml" for mp in mps), f"ML not in {mps}"

    def test_health_profit_consistent(self):
        r = client.get("/api/v4/financial-intelligence/health")
        data = r.json()
        total_rn = sum(mp["rn"] for mp in data["breakdown"])
        answer_profit = data["answer"]["is_profit"]
        assert answer_profit == (total_rn > 0)


class TestCopilotGolden:
    """Golden Test — captures deterministic health output for regression detection."""

    GOLDEN_DIR = Path(__file__).parent / "golden"
    KEY = "copilot_health"

    def test_golden_copilot_health_exists(self):
        path = self.GOLDEN_DIR / f"{self.KEY}.json"
        assert path.exists(), f"Golden file missing at {path}. Run with UPDATE_GOLDEN=1 to create."

    def test_golden_copilot_health_has_expected_keys(self):
        path = self.GOLDEN_DIR / f"{self.KEY}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        assert "answer" in golden
        assert "breakdown" in golden
        assert "explanation" in golden
        assert "evidence" in golden
        assert "period" in golden
        assert "previous_period" in golden
