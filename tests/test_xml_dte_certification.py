"""
Unit tests for XML/DTE SII Certification & Contract Validation (CTR-003 & LIN-003).
"""
import json
import pytest
from pathlib import Path
from tools.execute_xml_dte_certification import parse_dte_xml

ROOT = Path("c:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine")

class TestXmlDteCertification:
    def test_xml_certification_summary_exists(self):
        summary_path = ROOT / "evidence" / "xml_dte_certification" / "summary.json"
        assert summary_path.exists()
        data = json.loads(summary_path.read_text(encoding="utf-8"))
        assert data["total_xml_files"] == 971
        assert data["valid_xml_files"] == 971
        assert data["error_xml_files"] == 0
        assert data["contract_ctr_003_status"] == "CERTIFIED"
        assert data["official_verdict"] == "XML_DTE_CERTIFIED"

    def test_parse_sample_raw_xml(self):
        sample_xml = list((ROOT / "01_Raw").rglob("*.xml"))[0]
        rec = parse_dte_xml(sample_xml)
        assert rec["status"] == "VALID"
        assert "tipo_dte" in rec
        assert "folio" in rec
