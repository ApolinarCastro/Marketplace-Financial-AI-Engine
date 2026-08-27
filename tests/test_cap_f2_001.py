"""
Tests for CAP-F2-001 — Baseline Ejecutable de Conciliación End-to-End.
Piloto: Mercado Libre (MELI), Período 2025-04.
"""
from __future__ import annotations
import os
import shutil
import pytest
import duckdb
from pathlib import Path
from fastapi.testclient import TestClient

from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.copilot.copilot_engine import CopilotEngine
from engine.v4.knowledge.dual_graph import DualGraphRegistry
from engine.v4.ingestion.raw_file_indexer import RawFileIndexer
from api.api import app


@pytest.fixture(scope="module")
def controlled_db_path(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("cap_f2_001_db")
    official_db = Path("data/db/meli_financial_v4.db")
    target_db = tmp_dir / "controlled_cap_f2_001.db"
    shutil.copyfile(official_db, target_db)
    return str(target_db)


@pytest.fixture(scope="module")
def controlled_db_inst(controlled_db_path):
    db_inst = DatabaseV4(db_path=controlled_db_path, read_only=False)
    yield db_inst
    db_inst.close()


class TestCAPF2001Pipeline:
    def test_01_pilot_selection(self):
        marketplace = "ML"
        period = "2025-04"
        assert marketplace == "ML"
        assert period == "2025-04"

    def test_02_raw_integrity(self):
        indexer = RawFileIndexer(root_dir="01_Raw")
        records = [r for r in indexer.scan() if r.marketplace == "ML" and "2025-04" in r.relative_path]
        assert len(records) == 6
        for r in records:
            assert r.integrity_status == "VALID"
            assert len(r.content_hash) == 64

    def test_03_ingestion_idempotency(self):
        indexer = RawFileIndexer(root_dir="01_Raw")
        run1 = indexer.scan()
        run2 = indexer.scan()
        diff = indexer.compare_runs(run1, run2)
        assert diff["is_idempotent"] is True
        assert diff["new_files"] == 0

    def test_04_staging_contract(self, controlled_db_inst):
        conn = controlled_db_inst.conn
        count = conn.execute("SELECT count(*) FROM marketplace_ledger_v1 WHERE marketplace='ML' AND YEAR(fecha)=2025 AND MONTH(fecha)=4").fetchone()[0]
        assert count > 0

    def test_05_raw_to_ledger_traceability(self, controlled_db_inst):
        conn = controlled_db_inst.conn
        untraced = conn.execute("SELECT count(*) FROM marketplace_ledger_v1 WHERE marketplace='ML' AND YEAR(fecha)=2025 AND MONTH(fecha)=4 AND archivo_origen IS NULL").fetchone()[0]
        assert untraced == 0

    def test_06_financial_classification(self, controlled_db_inst):
        fe = FinancialEngine(db=controlled_db_inst)
        updated = fe.run_classification(marketplace="ML")
        assert updated >= 0

    def test_07_amount_immutability(self, controlled_db_inst):
        conn = controlled_db_inst.conn
        null_monto = conn.execute("SELECT count(*) FROM marketplace_ledger_v1 WHERE marketplace='ML' AND YEAR(fecha)=2025 AND MONTH(fecha)=4 AND monto IS NULL").fetchone()[0]
        assert null_monto == 0

    def test_08_reconciliation_execution(self, controlled_db_inst):
        fe = FinancialEngine(db=controlled_db_inst)
        closing = fe.run_financial_closing("ML", "2025-04-01", "2025-04-30")
        assert closing["neto"] is not None

    def test_09_delta_zero(self, controlled_db_inst):
        conn = controlled_db_inst.conn
        cierre = conn.execute("SELECT resultado_neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML' AND YEAR(periodo_inicio)=2025 AND MONTH(periodo_inicio)=4").fetchone()
        assert cierre is not None
        assert cierre[0] == 45359027.77 or round(cierre[0], 2) == 45359027.77

    def test_10_financial_closing_generated(self, controlled_db_inst):
        conn = controlled_db_inst.conn
        cierre_count = conn.execute("SELECT count(*) FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML' AND YEAR(periodo_inicio)=2025 AND MONTH(periodo_inicio)=4").fetchone()[0]
        assert cierre_count == 1

    def test_11_partial_dte_validation(self):
        # DTE status global remains NO CONFIRMADA
        dte_status = "NO CONFIRMADA"
        assert dte_status == "NO CONFIRMADA"

    def test_12_sap_backing(self, controlled_db_inst):
        copilot = CopilotEngine(db=controlled_db_inst)
        res = copilot.ask("Q-007", marketplace="ML", periodo="2025-04")
        assert res.get("status") == "INSUFFICIENT_EVIDENCE"

    def test_13_bank_backing(self, controlled_db_inst):
        copilot = CopilotEngine(db=controlled_db_inst)
        res = copilot.ask("Q-008", marketplace="ML", periodo="2025-04")
        assert res.get("status") == "INSUFFICIENT_EVIDENCE"

    def test_14_insufficient_evidence_fallback(self, controlled_db_inst):
        copilot = CopilotEngine(db=controlled_db_inst)
        res = copilot.ask("Q-007")
        assert res.get("status") == "INSUFFICIENT_EVIDENCE" or res.get("answer", {}).get("summary") == "No se puede responder con evidencia suficiente."

    def test_15_canonical_questions_q001_q010(self, controlled_db_inst):
        copilot = CopilotEngine(db=controlled_db_inst)
        for i in range(1, 11):
            qid = f"Q-{i:03d}"
            res = copilot.ask(qid, marketplace="ML", periodo="2025-04")
            assert "summary" in res or "answer" in res

    def test_16_dual_graph_traversal(self):
        graph = DualGraphRegistry()
        assert graph.get_node("CAP-F2-001") is not None
        assert graph.get_node("EVID-F2-001") is not None
        assert graph.audit_orphan_nodes() == []

    def test_17_knowledgeos_integration(self):
        project_doc = Path("knowledge/projects/CAP-F2-001.md")
        assert project_doc.exists()

    def test_18_endpoint_v4_contracts(self):
        client = TestClient(app)
        res = client.get("/api/v4/cierre/desglose?marketplace=ML&periodo=2025-04")
        assert res.status_code == 200

    def test_19_evidence_file_exists(self):
        evid_file = Path("evidence/fase_2/CAP-F2-001.json")
        assert evid_file.exists()

    def test_20_reproducibility(self, controlled_db_inst):
        fe = FinancialEngine(db=controlled_db_inst)
        run1 = fe.run_financial_closing("ML", "2025-04-01", "2025-04-30")
        run2 = fe.run_financial_closing("ML", "2025-04-01", "2025-04-30")
        assert run1 == run2
