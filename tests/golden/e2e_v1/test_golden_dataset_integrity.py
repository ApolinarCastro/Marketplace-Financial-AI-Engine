"""Golden Dataset E2E_V1 Integrity Test.

Validates the synthetic dataset structure and manual expected values
WITHOUT executing the pipeline.
"""
import csv
import json
from pathlib import Path

import pytest


GOLDEN_DIR = Path(__file__).parent
INPUT_DIR = GOLDEN_DIR / "input"
EXPECTED_DIR = GOLDEN_DIR / "expected"


class TestGoldenDatasetIntegrity:
    """Validate Golden Dataset E2E_V1 structure and internal consistency."""

    def test_input_directory_exists(self):
        assert INPUT_DIR.exists(), f"Input directory not found: {INPUT_DIR}"

    def test_expected_directory_exists(self):
        assert EXPECTED_DIR.exists(), f"Expected directory not found: {EXPECTED_DIR}"

    def test_input_files_exist(self):
        expected_input = INPUT_DIR / "ML_Facturacion_E2E_V1.xlsx"
        assert expected_input.exists(), f"Input file not found: {expected_input}"
        assert expected_input.stat().st_size > 0, "Input file is empty"

    def test_expected_files_exist(self):
        expected_files = [
            "expected_ledger.csv",
            "expected_reconciliation.csv",
            "expected_summary.json",
        ]
        for fname in expected_files:
            fpath = EXPECTED_DIR / fname
            assert fpath.exists(), f"Expected file not found: {fpath}"
            assert fpath.stat().st_size > 0, f"Expected file is empty: {fpath}"

    def test_expected_ledger_structure(self):
        """Validate expected_ledger.csv has correct columns and 8 rows."""
        ledger_path = EXPECTED_DIR / "expected_ledger.csv"
        with open(ledger_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 8, f"Expected 8 ledger rows, got {len(rows)}"

        required_columns = {
            "id_transaccion", "id_orden", "tipo_movimiento", "monto",
            "detalle", "financial_group", "marketplace", "fecha", "archivo_origen"
        }
        assert set(rows[0].keys()) == required_columns, f"Columns mismatch: {set(rows[0].keys())}"

        # Verify all rows have ML marketplace
        for row in rows:
            assert row["marketplace"] == "ML", f"Non-ML marketplace: {row}"

        # Verify tipos_movimiento match expected set
        tipos = {row["tipo_movimiento"] for row in rows}
        expected_tipos = {"INGRESO_VENTA", "EGRESO_COMISION", "CARGO", "DEVOLUCION", "AJUSTE"}
        assert tipos == expected_tipos, f"Tipos mismatch: {tipos} vs {expected_tipos}"

        # Verify monto sums to expected total
        total = sum(float(row["monto"]) for row in rows)
        assert abs(total - 20800.0) < 0.01, f"Ledger total mismatch: {total} != 20800.0"

    def test_expected_reconciliation_structure(self):
        """Validate expected_reconciliation.csv has 5 levels all CERTIFICADO."""
        recon_path = EXPECTED_DIR / "expected_reconciliation.csv"
        with open(recon_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 5, f"Expected 5 reconciliation rows, got {len(rows)}"

        for row in rows:
            assert row["marketplace"] == "ML"
            assert row["status"] == "CERTIFICADO", f"Non-CERTIFICADO status: {row}"
            assert float(row["delta"]) == 0.0, f"Non-zero delta: {row}"
            assert float(row["taxonomy_coverage"]) == 100.0
            assert float(row["document_coverage"]) == 100.0

    def test_expected_summary_structure(self):
        """Validate expected_summary.json has required fields and consistent values."""
        summary_path = EXPECTED_DIR / "expected_summary.json"
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)

        required_keys = {
            "dataset_id", "marketplace", "period", "source_type",
            "input_files", "expected_ledger_rows", "expected_reconciliation_rows",
            "expected_gross_amount", "expected_charges", "expected_refunds",
            "expected_commission_reversals", "expected_net_result",
            "expected_ledger_total", "financial_breakdown", "sign_convention",
            "manual_calculation"
        }
        assert set(summary.keys()) == required_keys, f"Keys mismatch: {set(summary.keys())}"

        assert summary["dataset_id"] == "E2E_V1"
        assert summary["marketplace"] == "ML"
        assert summary["source_type"] == "SYNTHETIC"
        assert summary["expected_ledger_rows"] == 8
        assert summary["expected_reconciliation_rows"] == 5
        assert summary["expected_net_result"] == 20800.0
        assert summary["expected_ledger_total"] == 20800.0

        # Verify financial breakdown sums to net result
        fb = summary["financial_breakdown"]
        calc_total = (
            fb["ingresos_venta"]
            + fb["egreso_comision"]
            + fb["cargos_operacionales"]
            + fb["devoluciones"]
            + fb["reversa_comision"]
        )
        assert abs(calc_total - summary["expected_net_result"]) < 0.01

    def test_no_production_paths_referenced(self):
        """Ensure no production database or RAW paths in expected files."""
        forbidden_paths = [
            "data/db/meli_financial_v4.db",
            "01_Raw/",
            "production",
            "meli_financial_v4.db",
        ]

        for fname in ["expected_ledger.csv", "expected_reconciliation.csv", "expected_summary.json"]:
            fpath = EXPECTED_DIR / fname
            content = fpath.read_text(encoding="utf-8")
            for forbidden in forbidden_paths:
                assert forbidden not in content, f"Forbidden path '{forbidden}' found in {fname}"

    def test_no_sensitive_data(self):
        """Ensure no real customer IDs, credentials, or sensitive identifiers."""
        sensitive_patterns = [
            "20000149",  # Real ML order IDs pattern
            "real_customer",
            "password",
            "token",
            "secret",
            "credential",
        ]

        for fname in ["expected_ledger.csv", "expected_reconciliation.csv", "expected_summary.json"]:
            fpath = EXPECTED_DIR / fname
            content = fpath.read_text(encoding="utf-8").lower()
            for pattern in sensitive_patterns:
                assert pattern.lower() not in content, f"Sensitive pattern '{pattern}' found in {fname}"

    def test_manual_calculation_consistency(self):
        """Verify the manual calculation in summary matches ledger total."""
        summary_path = EXPECTED_DIR / "expected_summary.json"
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)

        ledger_path = EXPECTED_DIR / "expected_ledger.csv"
        with open(ledger_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            ledger_total = sum(float(row["monto"]) for row in reader)

        assert abs(ledger_total - summary["expected_ledger_total"]) < 0.01
        assert abs(ledger_total - summary["expected_net_result"]) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])