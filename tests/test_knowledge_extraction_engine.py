"""
Tests for KnowledgeExtractionEngine (System Brain Layer & Governance Audit Framework).
"""
from __future__ import annotations
import json
import pytest
from pathlib import Path
from engine.v4.knowledge.knowledge_extraction_engine import KnowledgeExtractionEngine


class TestKnowledgeExtractionEngine:
    def test_extract_from_evidence_creates_entity(self, tmp_path):
        extractor = KnowledgeExtractionEngine(root_dir=tmp_path)
        sample_evidence = {
            "cap_id": "CAP-F2-001",
            "execution_id": "EXEC-CAP-F2-001-20260727",
            "status": "PASS",
            "marketplace": "ML",
            "periodo": "2025-04",
            "reconciliation": {"delta": 0.0},
            "canonical_questions": {
                "Q-001": "PASS",
                "Q-002": "PASS",
                "Q-007": "FALLBACK_INSUFFICIENT_EVIDENCE"
            }
        }
        entity_path = extractor.extract_from_evidence(sample_evidence)
        assert entity_path.exists()
        content = entity_path.read_text(encoding="utf-8")
        assert "entity_id: execution:CAP-F2-001:EXEC-CAP-F2-001-20260727" in content
        assert "CAP-F2-001" in content
        assert "EXEC-CAP-F2-001-20260727" in content

    def test_idempotency_verification(self, tmp_path):
        extractor = KnowledgeExtractionEngine(root_dir=tmp_path)
        sample_evidence = {
            "cap_id": "CAP-TD-008",
            "execution_id": "EXEC-CAP-TD-008-20260727",
            "status": "PASS"
        }
        path1 = extractor.extract_from_evidence(sample_evidence)
        hash1 = extractor.compute_hash(path1.read_text(encoding="utf-8"))

        path2 = extractor.extract_from_evidence(sample_evidence)
        hash2 = extractor.compute_hash(path2.read_text(encoding="utf-8"))

        assert hash1 == hash2
        assert path1 == path2

    def test_wikilink_integrity_validation(self, tmp_path):
        extractor = KnowledgeExtractionEngine(root_dir=tmp_path)
        sample_evidence = {
            "cap_id": "CAP-TD-001",
            "execution_id": "EXEC-CAP-TD-001-20260727",
            "status": "PASS"
        }
        extractor.extract_from_evidence(sample_evidence)
        wl_report = extractor.validate_wikilinks()
        assert wl_report["broken_links"] == 0
        assert wl_report["duplicate_entities"] == 0

    def test_query_system_brain_retrieves_entity(self, tmp_path):
        extractor = KnowledgeExtractionEngine(root_dir=tmp_path)
        sample_evidence = {
            "cap_id": "CAP-TD-008",
            "execution_id": "EXEC-CAP-TD-008-20260727",
            "status": "PASS"
        }
        extractor.extract_from_evidence(sample_evidence)

        res = extractor.query_system_brain("CAP-TD-008")
        assert res["found"] is True
        assert res["cap_id"] == "CAP-TD-008"
        assert res["status"] == "PASS"

    def test_generate_full_evidence_suite(self, tmp_path):
        extractor = KnowledgeExtractionEngine(root_dir=tmp_path)
        sample_evidence = {
            "cap_id": "CAP-F2-001",
            "execution_id": "EXEC-CAP-F2-001-20260727",
            "status": "PASS"
        }
        extractor.extract_from_evidence(sample_evidence)
        suite = extractor.generate_full_evidence_suite()
        assert len(suite) == 11
        for name, p in suite.items():
            assert p.exists()

        summary_json = json.loads(suite["summary"].read_text(encoding="utf-8"))
        assert summary_json["decision_id"] == "KNOWLEDGEOS_AS_SYSTEM_BRAIN_V1"
        assert summary_json["implementation_status"] == "IMPLEMENTED"
        assert summary_json["certification_status"] == "PENDING"
        assert summary_json["final_verdict"] == "PARTIALLY_IMPLEMENTED_NOT_CERTIFIED"
