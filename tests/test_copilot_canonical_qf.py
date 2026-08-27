"""Tests for Phase 1.b CAP-TD-006 — Canonical Normalization of Financial Copilot Questions."""
from __future__ import annotations
import pytest
from engine.v4.copilot.copilot_engine import CopilotEngine


@pytest.fixture
def copilot():
    return CopilotEngine()


CANONICAL_QUESTIONS = [f"Q-{i:03d}" for i in range(1, 11)]
CANONICAL_QF_ALIASES = [f"QF-{i:03d}" for i in range(1, 11)]
CANONICAL_INTENTS = [f"INT-QF-{i:03d}" for i in range(1, 11)]


class TestCanonicalQuestionResolution:
    @pytest.mark.parametrize("qid", CANONICAL_QUESTIONS)
    def test_resolve_canonical_q_ids(self, copilot, qid):
        assert copilot.resolve_question(qid) == qid

    @pytest.mark.parametrize("qf_alias, expected_qid", zip(CANONICAL_QF_ALIASES, CANONICAL_QUESTIONS))
    def test_resolve_qf_aliases(self, copilot, qf_alias, expected_qid):
        assert copilot.resolve_question(qf_alias) == expected_qid

    @pytest.mark.parametrize("intent_id, expected_qid", zip(CANONICAL_INTENTS, CANONICAL_QUESTIONS))
    def test_resolve_intent_ids(self, copilot, intent_id, expected_qid):
        assert copilot.resolve_question(intent_id) == expected_qid

    def test_non_overlapping_synonym_matrix(self, copilot):
        seen_synonyms = {}
        for synonym, qid in copilot.SYNONYMS.items():
            assert synonym not in seen_synonyms or seen_synonyms[synonym] == qid, f"Overlap detected for synonym: {synonym}"
            seen_synonyms[synonym] = qid


class TestCanonicalQuestionExecution:
    @pytest.mark.parametrize("qid", CANONICAL_QUESTIONS)
    def test_ask_returns_valid_structure(self, copilot, qid):
        res = copilot.ask(qid)
        assert "question_id" in res
        assert res["question_id"] == qid
        assert "intent_id" in res
        assert "answer" in res
        assert "summary" in res["answer"]

    def test_q007_sap_insufficient_evidence_fallback(self, copilot):
        res = copilot.ask("Q-007")
        assert res["status"] == "INSUFFICIENT_EVIDENCE"
        assert res["answer"]["summary"] == "No se puede responder con evidencia suficiente."
        assert res["confidence"] == 0.0

    def test_q008_bank_insufficient_evidence_fallback(self, copilot):
        res = copilot.ask("Q-008")
        assert res["status"] == "INSUFFICIENT_EVIDENCE"
        assert res["answer"]["summary"] == "No se puede responder con evidencia suficiente."
        assert res["confidence"] == 0.0

    @pytest.mark.parametrize("synonym, expected_qid", [
        ("qué vendí", "Q-001"),
        ("ventas brutas", "Q-001"),
        ("qué me cobraron", "Q-002"),
        ("comisiones", "Q-002"),
        ("qué me pagaron", "Q-003"),
        ("monto liquidado", "Q-003"),
        ("saldo pendiente", "Q-004"),
        ("devoluciones", "Q-005"),
        ("respaldo dte", "Q-006"),
        ("cargos no explicados", "Q-009"),
        ("margen financiero real", "Q-010"),
    ])
    def test_synonym_queries_resolve_and_execute(self, copilot, synonym, expected_qid):
        res = copilot.ask(synonym)
        assert res["question_id"] == expected_qid
