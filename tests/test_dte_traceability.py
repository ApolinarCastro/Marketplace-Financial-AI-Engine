"""
F5-09 — Electronic Tax Traceability: read-only DTE->Ledger matching capability.

Verifies the certified DTELedgerMatcher is exposed read-only with correct
per-marketplace coverage, honest RIPLEY BLOCKED reporting, deterministic
results, and zero DB mutation.
"""
import sys
import os
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient  # noqa: E402

from api.api import app  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


# ── Module-level (DTELedgerMatcher.traceability) ────────────────────────

def _matcher():
    from engine.v4.matching.dte_ledger_matcher import DTELedgerMatcher
    return DTELedgerMatcher()


def test_traceability_all_marketplaces_present():
    m = _matcher()
    res = m.traceability()
    assert "marketplaces" in res
    assert {"ML", "PARIS", "FALABELLA", "RIPLEY"} <= set(res["marketplaces"].keys())
    assert res["_meta"]["read_only"] is True
    assert res["_meta"]["official_db_touched"] is False
    assert res["totals"]["official_db_touched"] is False


def test_traceability_ml_certified_counts():
    """ML DIRECT_MATCH must follow the certified rules (data-agnostic across DBs)."""
    m = _matcher()
    res = m.traceability(marketplace="ML")
    ml = res["marketplaces"]["ML"]
    assert ml["strategy"] == "DIRECT_MATCH"
    assert ml["status"] in ("CERTIFIED", "NO_CERTIFIED_MATCHES")
    assert ml["rows_linked"] >= 0
    assert ml["rows_eligible"] >= ml["rows_linked"]
    if ml["status"] == "CERTIFIED":
        assert ml["folios_certified"] >= 1
        assert ml["rows_linked"] >= 1


def test_traceability_paris_certified():
    m = _matcher()
    res = m.traceability(marketplace="PARIS")
    paris = res["marketplaces"]["PARIS"]
    assert paris["strategy"] == "DOCUMENT_CHAIN"
    assert paris["status"] == "CERTIFIED"
    assert paris["rows_linked"] >= 1


def test_traceability_falabella_certified():
    m = _matcher()
    res = m.traceability(marketplace="FALABELLA")
    fal = res["marketplaces"]["FALABELLA"]
    assert fal["strategy"] == "TRANSACTION_CHAIN"
    assert fal["status"] == "CERTIFIED"
    assert fal["rows_linked"] >= 1


def test_traceability_ripley_honest_blocked():
    """RIPLEY must NEVER be reported as traceable (no false fiscal inference)."""
    m = _matcher()
    res = m.traceability(marketplace="RIPLEY")
    rip = res["marketplaces"]["RIPLEY"]
    assert rip["strategy"] == "SETTLEMENT_CHAIN_V2"
    assert rip["status"] == "BLOCKED"
    assert "blocked_reasons" in rip


def test_traceability_invalid_marketplace_raises():
    m = _matcher()
    with pytest.raises(ValueError):
        m.traceability(marketplace="AMAZON")


def test_traceability_deterministic():
    """Same inputs -> same output (idempotent read)."""
    m = _matcher()
    a = m.traceability()
    b = m.traceability()
    assert a == b


def test_traceability_no_db_mutation():
    """Running traceability must not create/modify any table or view."""
    from engine.v4.database import DatabaseV4
    db = DatabaseV4.get()
    before = set(db.query("SELECT table_name FROM information_schema.tables")["table_name"])
    before_v = set(db.query("SELECT table_name FROM information_schema.views")["table_name"])
    m = _matcher()
    m.traceability()
    after = set(db.query("SELECT table_name FROM information_schema.tables")["table_name"])
    after_v = set(db.query("SELECT table_name FROM information_schema.views")["table_name"])
    assert before == after, "traceability created/dropped a table!"
    assert before_v == after_v, "traceability created/dropped a view!"


def test_transaction_trace_not_found():
    m = _matcher()
    res = m._trace_transaction("DOES_NOT_EXIST_XYZ")
    assert res["match_status"] == "NOT_FOUND"


def test_transaction_trace_ml_resolves():
    """A certified ML transaction must resolve to its DTE backing (data-agnostic)."""
    m = _matcher()
    ml_cert = m._build_certified_rows("ML", m._match_ml_direct())
    if ml_cert.empty:
        pytest.skip("no certified ML matches in test DB")
    tid = str(ml_cert.iloc[0]["id_transaccion"])
    res = m._trace_transaction(tid)
    assert res["match_status"] == "MATCHED_CERTIFIED"
    assert res["dte_folio"]
    assert res["tipo_dte"]


def test_traceability_total_conservation():
    """totals.total_dte_linked_rows must equal the sum of certified rows_linked."""
    m = _matcher()
    res = m.traceability()
    expected = sum(
        v["rows_linked"]
        for k, v in res["marketplaces"].items()
        if k != "RIPLEY" and "rows_linked" in v
    )
    assert res["totals"]["total_dte_linked_rows"] == expected


# ── API contract ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_route_exists(client):
    r = client.get("/api/v4/dte/traceability")
    assert r.status_code == 200, f"Unexpected status: {r.status_code} {r.text}"


def test_route_summary_shape(client):
    r = client.get("/api/v4/dte/traceability")
    data = r.json()
    assert "_meta" in data
    assert "marketplaces" in data
    assert "totals" in data
    for mp in ("ML", "PARIS", "FALABELLA", "RIPLEY"):
        assert mp in data["marketplaces"], f"missing {mp} in marketplaces"


def test_route_marketplace_filter(client):
    r = client.get("/api/v4/dte/traceability", params={"marketplace": "ML"})
    data = r.json()
    assert "ML" in data["marketplaces"]
    assert "PARIS" not in data["marketplaces"]


def test_route_invalid_marketplace_400(client):
    r = client.get("/api/v4/dte/traceability", params={"marketplace": "AMAZON"})
    assert r.status_code == 400


def test_route_transaction_lookup(client):
    r = client.get("/api/v4/dte/traceability", params={"transaction_id": "DOES_NOT_EXIST_XYZ"})
    assert r.status_code == 200
    data = r.json()
    assert "transaction" in data
    assert data["transaction"]["match_status"] == "NOT_FOUND"


def test_route_read_only(client):
    """GET traceability must not alter official DB tables/views."""
    from engine.v4.database import DatabaseV4
    db = DatabaseV4.get()
    before = set(db.query("SELECT table_name FROM information_schema.tables")["table_name"])
    r = client.get("/api/v4/dte/traceability")
    assert r.status_code == 200
    after = set(db.query("SELECT table_name FROM information_schema.tables")["table_name"])
    assert before == after


def test_route_no_frontend_logic():
    """DEC-014 — no financial/computation logic added to frontend for this feature."""
    templates_dir = ROOT / "templates"
    for tmpl in templates_dir.glob("*.html"):
        content = tmpl.read_text(encoding="utf-8")
        assert "traceability" not in content or "dte/traceability" not in content, (
            f"{tmpl.name} must not implement DTE traceability client-side"
        )