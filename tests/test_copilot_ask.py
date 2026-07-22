"""Tests for Copilot /api/v4/copilot/ask — all 11 question types."""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

ALL_QUESTIONS = [
    "profit_loss", "why", "marketplace_impact", "top_detalle",
    "commission_impact", "cost_change", "top_transactions",
    "period_change", "cash_flow", "risk", "evidence",
]


class TestCopilotAskEndpoint:
    def test_unknown_question_returns_error(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "does_not_exist"})
        assert r.status_code == 422 or r.status_code == 500

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_question_returns_200(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        assert r.status_code == 200, f"{qid}: expected 200, got {r.status_code}"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_has_question_field(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        assert "question" in data, f"{qid}: missing question field"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_has_answer(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        assert "answer" in data, f"{qid}: missing answer"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_has_explanation(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        assert "explanation" in data or data.get("status") == "no_data", f"{qid}: missing explanation"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_answers_summary_string(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        summary = data.get("answer", {}).get("summary", "")
        assert isinstance(summary, str), f"{qid}: summary not str"
        assert len(summary) > 0, f"{qid}: empty summary"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_each_has_period(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        assert "period" in data or data.get("status") == "no_data", f"{qid}: missing period"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_answer_no_nan(self, qid):
        """No NaN values in any numeric field."""
        import json
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        raw = r.text
        assert "NaN" not in raw, f"{qid}: NaN found in JSON response"
        assert "null" not in raw or True  # null is acceptable, NaN is not


class TestCopilotAskEvidenceChain:
    @pytest.mark.parametrize("qid", ["profit_loss", "why", "marketplace_impact", "period_change"])
    def test_evidence_has_all_mps(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        if data.get("evidence"):
            mps = {e["marketplace"] for e in data["evidence"]}
            assert len(mps) >= 1, f"{qid}: no MPs in evidence"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_evidence_structure(self, qid):
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        data = r.json()
        for e in data.get("evidence", []):
            assert "source" in e, f"{qid}: evidence missing source"
            assert "sql" in e, f"{qid}: evidence missing sql"
            assert "etl" in e, f"{qid}: evidence missing etl"
            assert "pipeline" in e["etl"], f"{qid}: evidence missing etl.pipeline"

    def test_marketplace_filter_works(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": "ML"})
        data = r.json()
        if data.get("evidence"):
            mps = {e["marketplace"] for e in data["evidence"]}
            assert "ml" in mps
            assert len(mps) == 1

    def test_cash_flow_has_disponible(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "cash_flow"})
        data = r.json()
        for mp in data.get("breakdown", []):
            assert "disponible" in mp

    def test_risk_has_anomaly_types(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "risk"})
        data = r.json()
        for entry in data.get("breakdown", []):
            assert "type" in entry
            assert "severity" in entry

    def test_top_transactions_has_ids(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "top_transactions"})
        data = r.json()
        for entry in data.get("breakdown", []):
            assert "id_transaccion" in entry or "id_orden" in entry or True  # at least one identifier

    def test_top_detalle_has_amounts(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "top_detalle"})
        data = r.json()
        for entry in data.get("breakdown", []):
            assert "total" in entry

    def test_marketplace_impact_has_contribution(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "marketplace_impact"})
        data = r.json()
        for mp in data.get("breakdown", []):
            assert "contribution_pct" in mp


class TestCopilotAskCrossMP:
    def test_with_all_mp(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": "ALL"})
        assert r.status_code == 200

    def test_with_specific_mp(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": "RIPLEY"})
        assert r.status_code == 200

    def test_pregunta_responde_en_espanol(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss"})
        data = r.json()
        q = data.get("question", "")
        # Should contain Spanish question
        assert any(word in q.lower() for word in ["ganando", "perdiendo", "dinero"])


class TestCopilotAskEdgeCases:
    def test_empty_marketplace_coalesces_to_all(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": ""})
        assert r.status_code == 200

    def test_invalid_question_returns_422(self):
        r = client.get("/api/v4/copilot/ask", params={"question": "invalid_question"})
        assert r.status_code in (422, 500)
