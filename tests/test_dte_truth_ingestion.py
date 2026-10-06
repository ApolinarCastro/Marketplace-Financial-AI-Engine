"""DTE truth ingestion metadata + fresh certified-table tests.

Covers PFO-XML-DTE-METADATA-DDL-001 PASO 5-10. All tests use isolated
tmp_path databases. Production DB and real 01_Raw/ are never touched.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from engine.v4.database import DatabaseV4

GOLDEN_XML = Path("tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000001.xml")
XML_SUBPATH = Path("01_Raw") / "ML" / "Documentos Recepcionados"


def _fresh_db(tmp_path: Path, name: str = "dte.db") -> DatabaseV4:
    return DatabaseV4(db_path=str(tmp_path / name), read_only=False)


def _stage_xml(tmp_path: Path) -> Path:
    dest = tmp_path / XML_SUBPATH
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(GOLDEN_XML, dest / GOLDEN_XML.name)
    return tmp_path


def test_fresh_db_has_dte_tables_empty(tmp_path: Path):
    db = _fresh_db(tmp_path)
    try:
        for tbl in ("dte_truth_v1", "dte_certified_match_v1", "document_match_v1"):
            n = db.query(f"SELECT COUNT(*) AS n FROM {tbl}")["n"].iloc[0]
            assert int(n) == 0, f"{tbl} not empty"
        cols = db.query(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'dte_certified_match_v1' ORDER BY ordinal_position"
        )["column_name"].tolist()
        assert cols == [
            "marketplace", "id_transaccion", "folio_xml", "dte_folio",
            "dte_monto", "dte_fecha", "emisor_nombre", "emisor_rut",
            "tipo_dte", "match_rule", "match_status", "match_source",
            "execution_id",
        ], f"certified schema mismatch: {cols}"
    finally:
        db.close()


def test_load_dtes_persists_tipo_dte_and_marketplace(tmp_path: Path):
    from engine.v4.dte_matcher import DTEMatcher

    root = _stage_xml(tmp_path)
    db = _fresh_db(tmp_path)
    orig_instance = DatabaseV4._instance
    DatabaseV4._instance = db
    try:
        DTEMatcher(db=db, marketplace="ML", root=root).load_dtes()
        rows = db.query("SELECT * FROM dte_truth_v1").to_dict(orient="records")
        assert len(rows) == 1
        r = rows[0]
        assert str(r["folio"]) == "90000001"
        assert str(r["tipo_dte"]) == "33", f"tipo_dte={r['tipo_dte']!r}"
        assert str(r["marketplace"]) == "ML", f"marketplace={r['marketplace']!r}"
        assert float(r["monto_neto"]) == 4789.0
        assert float(r["monto_iva"]) == 911.0
        assert float(r["monto_total"]) == 5700.0
        assert str(r["emisor_rut"]) == "76000000-0"
    finally:
        DatabaseV4._instance = orig_instance
        db.close()


def test_load_dtes_preserves_other_marketplaces(tmp_path: Path):
    from engine.v4.dte_matcher import DTEMatcher

    root = _stage_xml(tmp_path)
    db = _fresh_db(tmp_path)
    orig_instance = DatabaseV4._instance
    DatabaseV4._instance = db
    try:
        db.execute(
            "INSERT INTO dte_truth_v1 (folio, monto_total, marketplace, tipo_dte) "
            "VALUES ('TEST-PARIS-001', 1000.0, 'PARIS', '33')"
        )
        DTEMatcher(db=db, marketplace="ML", root=root).load_dtes()
        paris = db.query(
            "SELECT folio FROM dte_truth_v1 WHERE marketplace = 'PARIS'"
        )["folio"].tolist()
        assert paris == ["TEST-PARIS-001"], "PARIS row was wiped by ML load"
        ml = db.query(
            "SELECT folio FROM dte_truth_v1 WHERE marketplace = 'ML'"
        )["folio"].tolist()
        assert ml == ["90000001"]
    finally:
        DatabaseV4._instance = orig_instance
        db.close()


def test_ml_dte_visible_to_matcher_query(tmp_path: Path):
    from engine.v4.dte_matcher import DTEMatcher

    root = _stage_xml(tmp_path)
    db = _fresh_db(tmp_path)
    orig_instance = DatabaseV4._instance
    DatabaseV4._instance = db
    try:
        DTEMatcher(db=db, marketplace="ML", root=root).load_dtes()
        rows = db.query(
            "SELECT folio, monto_total, monto_neto, monto_iva, fecha_emision, "
            "emisor_rut, emisor_nombre, tipo_dte FROM dte_truth_v1 WHERE marketplace='ML'"
        ).to_dict(orient="records")
        assert len(rows) == 1
        assert str(rows[0]["folio"]) == "90000001"
        assert str(rows[0]["tipo_dte"]) == "33"
    finally:
        DatabaseV4._instance = orig_instance
        db.close()


def test_matcher_ensure_schema_compatible_with_fresh_ddl(tmp_path: Path):
    from engine.v4.matching.dte_ledger_matcher import DTELedgerMatcher

    db = _fresh_db(tmp_path)
    try:
        DTELedgerMatcher(db=db)._ensure_schema()
        DTELedgerMatcher(db=db)._ensure_schema()
        n = db.query("SELECT COUNT(*) AS n FROM dte_certified_match_v1")["n"].iloc[0]
        assert int(n) == 0
    finally:
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
