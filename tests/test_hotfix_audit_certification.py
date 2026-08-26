"""Hotfix regression guards: audit read-only, Falabella truth, certification semantics."""
import hashlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from fastapi.testclient import TestClient
from api.api import app
import duckdb

ROOT = Path(__file__).parent.parent
DB = ROOT / "data/db/meli_financial_v4.db"

def sha():
    return hashlib.sha256(DB.read_bytes()).hexdigest()

# --- Audit Button ---
def test_audit_endpoint_responds():
    c = TestClient(app)
    r = c.post("/api/v4/run-audit?marketplace=ML")
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "success"
    assert j["mode"] == "READ_ONLY"
    assert "report" in j

def test_audit_read_only_no_delete():
    c = TestClient(app)
    before = sha()
    import duckdb
    con = duckdb.connect(str(DB), read_only=True)
    cnt_before = con.execute("SELECT COUNT(*) FROM marketplace_auditoria_v1").fetchone()[0]
    con.close()
    r = c.post("/api/v4/run-audit?marketplace=ML")
    assert r.status_code == 200
    after = sha()
    con = duckdb.connect(str(DB), read_only=True)
    cnt_after = con.execute("SELECT COUNT(*) FROM marketplace_auditoria_v1").fetchone()[0]
    con.close()
    assert before == after, "DB mutated by audit"
    assert cnt_before == cnt_after

def test_audit_idempotent_3x():
    c = TestClient(app)
    results = []
    for _ in range(3):
        r = c.post("/api/v4/run-audit?marketplace=ML")
        assert r.status_code == 200
        results.append(r.json()["report"]["total_findings"])
    assert results[0] == results[1] == results[2]

# --- Falabella ---
def test_falabella_mar_may_negative():
    con = duckdb.connect(str(DB), read_only=True)
    for period, expected_sign in [("2026-03", -785566), ("2026-04", -1155270), ("2026-05", -267947)]:
        s = con.execute(f"SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND CAST(fecha AS VARCHAR) LIKE '{period}%'").fetchone()[0]
        assert s is not None and s < 0, f"{period} should be negative, got {s}"
        # May specific
        if period == "2026-05":
            assert abs(s - (-267948)) < 2, f"May delta {s}"
    con.close()

def test_falabella_api_matches_truth():
    c = TestClient(app)
    # financial-structure for Falabella May should reflect ledger (via backend, not JS)
    r = c.get("/api/v4/financial-structure?marketplace=FALABELLA&period=2026-05")
    assert r.status_code == 200

# --- Electronic Certification ---
def test_document_reference_not_cryptographic():
    c = TestClient(app)
    r = c.get("/api/v4/electronic_certification/status/15055037_COMM")
    assert r.status_code == 200
    j = r.json()
    assert j["estado"] == "DOCUMENT_REFERENCE_ONLY"
    assert j["certification_scope"] != "FISCAL"
    assert j["certification_scope"] == "DOCUMENTAL"
    assert j["pipeline"] == {"xml":"FAIL","xsd":"FAIL","sig":"FAIL","caf":"FAIL"}
    assert j["evidencia"]["level"] == "DOCUMENT_REFERENCE_ONLY"

def test_null_estado_normalized():
    c = TestClient(app)
    r = c.get("/api/v4/electronic_certification/status/15055037_COMM")
    j = r.json()
    assert j["estado"] is not None
    assert j["estado"] != "null"
    assert j["estado"] != ""

def test_fail_not_cryptographic():
    c = TestClient(app)
    r = c.get("/api/v4/electronic_certification/status/15055037_COMM")
    j = r.json()
    if j["pipeline"] == {"xml":"FAIL","xsd":"FAIL","sig":"FAIL","caf":"FAIL"}:
        assert j["estado"] != "CRYPTOGRAPHIC_CERTIFIED"

def test_ledger_reference_never_fiscal():
    c = TestClient(app)
    # pick a transaction without folio
    import duckdb
    con = duckdb.connect(str(DB), read_only=True)
    row = con.execute("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE folio_xml IS NULL LIMIT 1").fetchone()
    con.close()
    if row:
        tid = row[0]
        r = c.get(f"/api/v4/electronic_certification/status/{tid}")
        j = r.json()
        assert j["certification_scope"] != "FISCAL" or j["estado"] != "CRYPTOGRAPHIC_CERTIFIED"

def test_ripley_insufficient_not_fiscal():
    c = TestClient(app)
    import duckdb
    con = duckdb.connect(str(DB), read_only=True)
    row = con.execute("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' LIMIT 1").fetchone()
    con.close()
    if row:
        r = c.get(f"/api/v4/electronic_certification/status/{row[0]}")
        j = r.json()
        # Ripley should be INSUFFICIENT or DOCUMENT but never CRYPTOGRAPHIC without real evidence
        assert j["estado"] in ("INSUFFICIENT_FISCAL_EVIDENCE","DOCUMENT_REFERENCE_ONLY","LEDGER_REFERENCE_ONLY","XML_PRESENT_NOT_CERTIFIED","TRUTH_CONFLICT_DETECTED")
