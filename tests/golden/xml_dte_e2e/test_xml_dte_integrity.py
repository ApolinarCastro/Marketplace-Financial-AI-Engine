"""XML_DTE_E2E fixture integrity test (no engine execution).

Validates the synthetic XML parses with the SII namespace, carries the
expected fields, and matches the precomputed expected JSON.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


GOLDEN_DIR = Path(__file__).parent
INPUT_DIR = GOLDEN_DIR / "input"
EXPECTED_DIR = GOLDEN_DIR / "expected"
NS = {"ns0": "http://www.sii.cl/SiiDte"}


def _parse(xml_path: Path) -> dict:
    root = ET.parse(str(xml_path)).getroot()
    enc = root.find(".//ns0:Encabezado", NS)
    assert enc is not None, f"no Encabezado in {xml_path.name}"
    folio = enc.find(".//ns0:Folio", NS).text
    tipo = enc.find(".//ns0:IdDoc/ns0:TipoDTE", NS)
    if tipo is None:
        tipo = enc.find(".//ns0:TipoDTE", NS)
    fecha = enc.find(".//ns0:FchEmis", NS).text
    emisor = enc.find(".//ns0:Emisor", NS)
    tot = enc.find(".//ns0:Totales", NS)
    return {
        "folio": folio,
        "tipo_dte": tipo.text if tipo is not None else None,
        "fecha": fecha,
        "rut": emisor.find("ns0:RUTEmisor", NS).text,
        "nombre": emisor.find("ns0:RznSoc", NS).text,
        "neto": float(tot.find("ns0:MntNeto", NS).text),
        "iva": float(tot.find("ns0:IVA", NS).text),
        "total": float(tot.find("ns0:MntTotal", NS).text),
    }


def test_positive_xml_parses_with_expected_fields():
    v = _parse(INPUT_DIR / "PFO_SYNTH_DTE_90000001.xml")
    assert v["folio"] == "90000001"
    assert v["tipo_dte"] == "33"
    assert v["neto"] == 4789.0
    assert v["iva"] == 911.0
    assert v["total"] == 5700.0
    assert v["fecha"] == "2026-06-02"
    assert v["rut"] == "76000000-0"


def test_negative_xml_differs_by_two_pesos():
    v = _parse(INPUT_DIR / "PFO_SYNTH_DTE_90000002_NEG.xml")
    assert v["folio"] == "90000002"
    assert v["total"] == 5702.0
    assert abs(v["total"] - 5700.0) == 2.0


def test_expected_json_matches_fixture():
    exp = json.loads((EXPECTED_DIR / "expected_xml_dte.json").read_text(encoding="utf-8"))
    v = _parse(INPUT_DIR / "PFO_SYNTH_DTE_90000001.xml")
    assert exp["xml_expected_fields"]["folio"] == v["folio"]
    assert exp["xml_expected_fields"]["monto_total"] == v["total"]
    assert exp["match_expected"]["tolerance_clp"] == 1.0


def test_no_real_sii_markers():
    for f in INPUT_DIR.glob("*.xml"):
        text = f.read_text(encoding="utf-8", errors="replace")
        assert "90000001" in text or "90000002" in text
        assert "PFO SYNTHETIC" in text
        assert "76000000-0" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
