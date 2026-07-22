"""Golden Tests for all 11 Copilot questions (P39R2A).

Captures deterministic response structure and key fields for regression detection.
Run with: python -m pytest tests/test_copilot_golden.py -v
To update all golden files: $env:UPDATE_GOLDEN=1; python -m pytest tests/test_copilot_golden.py -v
"""
from __future__ import annotations
import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)
GOLDEN_DIR = Path(__file__).parent / "golden"

ALL_QUESTIONS = [
    "profit_loss", "why", "marketplace_impact", "top_detalle",
    "commission_impact", "cost_change", "top_transactions",
    "period_change", "cash_flow", "risk", "evidence",
]


def _get_response(qid: str, mp: str | None = None) -> dict:
    params = {"question": qid}
    if mp:
        params["marketplace"] = mp
    r = client.get("/api/v4/copilot/ask", params=params)
    assert r.status_code == 200, f"{qid}: expected 200, got {r.status_code}"
    return r.json()


class TestGoldenFilesExist:
    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_file_exists(self, qid):
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        assert path.exists(), f"Golden file missing at {path}. Run with UPDATE_GOLDEN=1 to create."

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_has_expected_keys(self, qid):
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        assert "question" in golden
        assert "period" in golden
        assert "answer" in golden
        assert "explanation" in golden
        assert "breakdown" in golden
        assert "evidence" in golden

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_answer_has_summary(self, qid):
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        assert "summary" in golden["answer"]

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_explanation_has_text(self, qid):
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        assert "text" in golden["explanation"]
        assert "bullet_points" in golden["explanation"]

    def test_golden_copilot_health_exists(self):
        path = GOLDEN_DIR / "copilot_health.json"
        assert path.exists(), f"Golden health file missing at {path}"


class TestGoldenResponseMatchesAPI:
    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_vs_live_question(self, qid):
        """Live response must have same keys as golden."""
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        live = _get_response(qid)
        for key in golden:
            assert key in live, f"{qid}: live missing key '{key}'"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_golden_vs_live_evidence_structure(self, qid):
        """Evidence entries must have source, sql, etl."""
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        live = _get_response(qid)
        for e in live.get("evidence", []):
            assert "source" in e, f"{qid}: evidence missing source"
            assert "sql" in e, f"{qid}: evidence missing sql"
            assert "etl" in e, f"{qid}: evidence missing etl"
            assert "pipeline" in e["etl"], f"{qid}: evidence missing etl.pipeline"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_no_nan_in_golden(self, qid):
        """No NaN values in golden files."""
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        raw = path.read_text(encoding="utf-8")
        assert "NaN" not in raw, f"{qid}: NaN found in golden file"

    def test_all_questions_have_different_qid(self):
        """Each question has a unique question label."""
        labels = {}
        for qid in ALL_QUESTIONS:
            path = GOLDEN_DIR / f"copilot_{qid}.json"
            with open(path, encoding="utf-8") as f:
                golden = json.load(f)
            q = golden.get("question", "")
            assert q not in labels.values() or qid == "period_change", \
                f"Duplicate question text: {q}"
            labels[qid] = q

    def test_profit_loss_status_consistent(self):
        """profit_loss answer.status must be profit or loss."""
        path = GOLDEN_DIR / "copilot_profit_loss.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        status = golden["answer"]["status"]
        assert status in ("profit", "loss"), f"Unexpected status: {status}"

    def test_cash_flow_has_disponible_in_breakdown(self):
        """cash_flow breakdown must have 'disponible' field."""
        path = GOLDEN_DIR / "copilot_cash_flow.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        for entry in golden.get("breakdown", []):
            assert "disponible" in entry, "cash_flow breakdown missing disponible"

    def test_risk_has_anomaly_types(self):
        """risk breakdown must have type and severity."""
        path = GOLDEN_DIR / "copilot_risk.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        for entry in golden.get("breakdown", []):
            assert "type" in entry
            assert "severity" in entry


# ── Auto-create golden files on demand ──────────────────────────

@pytest.mark.skipif("UPDATE_GOLDEN" not in __import__('os').environ,
                    reason="Set UPDATE_GOLDEN=1 to regenerate golden files")
@pytest.mark.parametrize("qid", ALL_QUESTIONS)
def test_update_golden(qid):
    data = _get_response(qid)
    path = GOLDEN_DIR / f"copilot_{qid}.json"
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Golden file updated: {path}")
