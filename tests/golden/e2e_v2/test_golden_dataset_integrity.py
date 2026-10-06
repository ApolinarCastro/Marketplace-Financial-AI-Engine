"""Golden Dataset E2E_V2 Integrity Test.

Validates structure, manual precomputations, and engine-vocabulary
consistency WITHOUT executing the pipeline or the reconciliation engine.
"""
import csv
import json
from pathlib import Path

import pytest


GOLDEN_DIR = Path(__file__).parent
INPUT_DIR = GOLDEN_DIR / "input"
EXPECTED_DIR = GOLDEN_DIR / "expected"

VALID_LEVEL_STATUSES = {"PASS", "ALERTA"}
VALID_AGGREGATE_STATUSES = {
    "CERTIFICADO", "PARCIAL", "PENDIENTE", "ERROR", "FINANCIAL_INTEGRITY_BROKEN",
}


class TestGoldenDatasetE2EV2Integrity:
    def test_input_file_exists(self):
        f = INPUT_DIR / "ML_Facturacion_E2E_V2.xlsx"
        assert f.exists() and f.stat().st_size > 0

    def test_input_has_six_rows_including_treasury(self):
        import openpyxl
        wb = openpyxl.load_workbook(INPUT_DIR / "ML_Facturacion_E2E_V2.xlsx")
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        assert rows[0] == ("Venta", "Detalle", "Valor del cargo", "Total de la venta", "Fecha")
        data = rows[1:]
        assert len(data) == 6
        tes = [r for r in data if r[0] == "E2E-TES"]
        assert len(tes) == 1
        assert tes[0][1] == "Retiro de dinero"
        assert float(tes[0][2]) == 20800.0

    def test_expected_files_exist(self):
        for fname in ("expected_ledger.csv", "expected_reconciliation.csv",
                      "expected_summary.json", "expected_document_matches.csv"):
            f = EXPECTED_DIR / fname
            assert f.exists(), fname
            assert f.stat().st_size > 0, fname

    def test_expected_ledger_nine_rows_and_manual_net(self):
        with open(EXPECTED_DIR / "expected_ledger.csv", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 9
        op = [r for r in rows if r["id_orden"] != "E2E-TES"]
        tes = [r for r in rows if r["id_orden"] == "E2E-TES"]
        assert len(op) == 8 and len(tes) == 1
        op_net = round(sum(float(r["monto"]) for r in op), 2)
        assert op_net == 20800.0, op_net
        assert round(float(tes[0]["monto"]), 2) == -20800.0
        assert tes[0]["tipo_movimiento"] == "CARGO"
        assert tes[0]["detalle"] == "Retiro de dinero"
        # Raw ledger contract: financial_group empty (classification assigns later)
        assert all(r["financial_group"] == "" for r in rows)
        # Mirror precomputation
        assert round(op_net + float(tes[0]["monto"]), 2) == 0.0

    def test_expected_reconciliation_uses_engine_vocabulary(self):
        with open(EXPECTED_DIR / "expected_reconciliation.csv", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 5
        by_level = {r["level"]: r for r in rows}
        assert set(by_level) == {"LEVEL_1", "LEVEL_2", "LEVEL_3", "LEVEL_4", "LEVEL_5"}
        for lvl in ("LEVEL_1", "LEVEL_2", "LEVEL_3", "LEVEL_4"):
            assert by_level[lvl]["status"] in VALID_LEVEL_STATUSES, lvl
            assert float(by_level[lvl]["delta"]) == 0.0, lvl
            assert float(by_level[lvl]["taxonomy_coverage"]) == 100.0, lvl
            assert float(by_level[lvl]["document_coverage"]) == 100.0, lvl
        assert by_level["LEVEL_5"]["status"] in VALID_AGGREGATE_STATUSES
        assert by_level["LEVEL_5"]["status"] == "CERTIFICADO"
        # No PENDIENTE anywhere: E2E_V2 targets full-chain parity
        assert all(r["status"] != "PENDIENTE" for r in rows)

    def test_expected_document_matches_nine_conciliated(self):
        with open(EXPECTED_DIR / "expected_document_matches.csv", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 9
        assert all(r["match_status"] == "CONCILIATED" for r in rows)
        assert all(r["marketplace"] == "ML" for r in rows)
        assert all("SYNTH" in (r["folio_xml"] or "") for r in rows)
        assert all(r["match_source"] == "PFO_SYNTHETIC_GOLDEN" for r in rows)
        # No real SII folios: synthetic markers only
        assert not any(r["folio_xml"].startswith("033-") for r in rows)
        # Every ledger id has exactly one match
        with open(EXPECTED_DIR / "expected_ledger.csv", newline="", encoding="utf-8") as f:
            ledger_ids = {r["id_transaccion"] for r in csv.DictReader(f)}
        assert {r["ledger_id"] for r in rows} == ledger_ids

    def test_expected_summary_consistent(self):
        summary = json.loads((EXPECTED_DIR / "expected_summary.json").read_text(encoding="utf-8"))
        assert summary["dataset_id"] == "E2E_V2"
        assert summary["expected_operational_net"] == 20800.0
        assert summary["expected_treasury_total"] == -20800.0
        assert summary["expected_mirror_delta"] == 0.0
        assert summary["expected_document_matches"] == 9
        assert summary["expected_document_coverage"] == 100.0
        assert summary["expected_aggregate_status"] == "CERTIFICADO"
        assert "NOT_TESTED" in summary["electronic_certification"]

    def test_no_production_paths_or_real_folios(self):
        for fname in ("expected_ledger.csv", "expected_reconciliation.csv",
                      "expected_summary.json", "expected_document_matches.csv"):
            content = (EXPECTED_DIR / fname).read_text(encoding="utf-8")
            for forbidden in ("data/db/meli_financial_v4.db", "01_Raw/", "production"):
                assert forbidden not in content, f"{forbidden} in {fname}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
