"""
Phase 15B — Automated Certification Gate (F4-R4 compliant).
All queries run against V8 temp copy. DTE coverage computed inline.
"""
import re
import pytest
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_DIR = ROOT / "KnowledgeBase" / "Marketplace" / "Taxonomy"


def fix_mojibake(s):
    """Fix UTF-8 mojibake where bytes 0xC3 0xB3 (ó) are stored as Ã (U+00C3) + ³ (U+00B3)."""
    try:
        encoded = s.encode("latin-1")
        fixed = encoded.decode("utf-8")
        return fixed if fixed != s else s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def _load_taxonomy(mp):
    path = TAXONOMY_DIR / f"{mp.lower()}_v1.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _taxonomy_detalles(taxonomy):
    """Extract all canonical detalles (lowercased) from taxonomy structure."""
    detalles = set()
    for group in taxonomy.get("canonical_groups", {}).values():
        for d in group.get("detalles", []):
            detalles.add(d.lower())
    for d in taxonomy.get("detalle_classification", {}):
        detalles.add(d.lower())
    return detalles


def _taxonomy_groups(taxonomy):
    """Extract all canonical group names from taxonomy."""
    return set(taxonomy.get("canonical_groups", {}).keys())


def _norm_detalle(raw):
    """Normalize ledger detalle for comparison: mojibake fix + lowercase."""
    return fix_mojibake(raw).lower()


# ═════════════════════════════════════════════════════════════════════════
# Gate 1: Executive Summary vs Waterfall Consistency
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_gate_exec_summary_vs_waterfall(v8_fe, mp):
    """Exec summary net_profit must match waterfall disponible."""
    s = v8_fe.query_exec_summary(marketplace=mp)
    w = v8_fe.query_waterfall(marketplace=mp)
    pnl = s["financial_pnl"]
    net = pnl["net_profit"]
    disp = w["disponible"]
    delta = abs(net - disp)
    assert delta < 1000, f"{mp}: Exec net={net} vs Waterfall disp={disp}, delta={delta}"


# ═════════════════════════════════════════════════════════════════════════
# Gate 2: Waterfall Conservation
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_gate_waterfall_conservation(v8_fe, mp):
    """ventas + devoluciones + cobros + recuperaciones ≈ disponible."""
    w = v8_fe.query_waterfall(marketplace=mp)
    ing = w.get("ventas", 0) or 0
    dev = w.get("devoluciones", 0) or 0
    cob = w.get("cobros", 0) or 0
    rec = w.get("recuperaciones", 0) or 0
    disp = w.get("disponible", 0) or 0
    calc = ing + dev + cob + rec
    assert abs(calc - disp) < 0.01, (
        f"{mp}: ing({ing}) + dev({dev}) + cob({cob}) + rec({rec}) = {calc} "
        f"!= disponible({disp})"
    )


# ═════════════════════════════════════════════════════════════════════════
# Gate 3: DTE Coverage Thresholds (inline from V8 temp DB)
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp,threshold", [("ML", 50.0), ("RIPLEY", 95.0), ("PARIS", 0.0), ("FALABELLA", 0.0)])
def test_gate_dte_coverage(v8_db, mp, threshold):
    """DTE coverage must meet minimum threshold per marketplace (all rows)."""
    df = v8_db.query(
        "SELECT COUNT(*) as total, COUNT(folio_xml) as with_xml "
        "FROM marketplace_ledger_v1 WHERE LOWER(marketplace) = LOWER(?)",
        [mp]
    )
    total = df.iloc[0]["total"]
    with_xml = df.iloc[0]["with_xml"]
    cov = (with_xml / total * 100) if total > 0 else 0.0
    assert cov >= threshold, f"{mp}: DTE coverage {cov:.1f}% < {threshold}% (total={total}, with_xml={with_xml})"


# ═════════════════════════════════════════════════════════════════════════
# Gate 4: Taxonomy Coverage (no orphan detalles)
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_gate_taxonomy_has_no_orphans(v8_db, mp):
    """Every ledger detalle must be in taxonomy (no orphans, mojibake-tolerant)."""
    taxonomy = _load_taxonomy(mp)
    if taxonomy is None:
        pytest.skip(f"Taxonomy for {mp} not found")
    known = _taxonomy_detalles(taxonomy)
    rows = v8_db.query(
        "SELECT DISTINCT detalle FROM marketplace_ledger_v1 "
        "WHERE marketplace = ? AND detalle IS NOT NULL",
        [mp]
    )
    orphans = []
    for _, r in rows.iterrows():
        normed = _norm_detalle(r["detalle"])
        if normed not in known:
            orphans.append(r["detalle"])
    assert not orphans, f"{mp}: orphan detalles not in taxonomy: {orphans}"


@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_gate_taxonomy_groups_cover_financial_groups(v8_db, mp):
    """Taxonomy canonical_groups must cover all financial_groups used by this MP."""
    taxonomy = _load_taxonomy(mp)
    if taxonomy is None:
        pytest.skip(f"Taxonomy for {mp} not found")
    covered_groups = _taxonomy_groups(taxonomy)
    rows = v8_db.query(
        "SELECT DISTINCT financial_group FROM marketplace_ledger_v1 "
        "WHERE marketplace = ? AND financial_group IS NOT NULL",
        [mp]
    )
    missing = [r["financial_group"] for _, r in rows.iterrows() if r["financial_group"] not in covered_groups]
    assert not missing, f"{mp}: financial_groups missing from taxonomy: {missing}"


# ═════════════════════════════════════════════════════════════════════════
# Gate 5: Ledger SIGNAL Internal Consistency
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_gate_ledger_has_data(v8_db, mp):
    """Each marketplace must have ledger data."""
    count = int(v8_db.query(
        "SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp]
    ).iloc[0, 0])
    assert count > 0, f"{mp}: ledger has 0 rows"


def test_gate_all_mps_have_waterfall(v8_fe):
    """All 4 MPs must return valid waterfall structure."""
    for mp in ("ML", "PARIS", "RIPLEY", "FALABELLA"):
        w = v8_fe.query_waterfall(marketplace=mp)
        assert "disponible" in w, f"{mp}: waterfall missing 'disponible'"
        assert "ventas" in w, f"{mp}: waterfall missing 'ventas'"


# ═════════════════════════════════════════════════════════════════════════
# Gate 6: No Frontend Financial Computations
# ═════════════════════════════════════════════════════════════════════════

def test_gate_no_frontend_financial_computations():
    """Verify templates don't contain financial calculation logic."""
    templates_dir = Path("templates")
    forbidden_patterns = [
        "query_waterfall", "query_exec_summary", "FinancialEngine",
        "disponible =", "net_profit =", "cobros =", "ingresos +",
    ]
    errors = []
    for tmpl in templates_dir.glob("*.html"):
        content = tmpl.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in content:
                errors.append(f"{tmpl.name}: contains '{pattern}'")
    assert not errors, "Frontend financial computations detected:\n" + "\n".join(errors)


# ═════════════════════════════════════════════════════════════════════════
# Gate 7: Mutation Protection (INSERT/UPDATE/DELETE blocked on core tables)
# ═════════════════════════════════════════════════════════════════════════

def test_gate_insert_update_delete_blocked(v8_db):
    """Core financial tables must reject mutations in read-only mode."""
    import duckdb
    core_tables = ["marketplace_ledger_v1", "marketplace_ledger_clasificado_v1", "marketplace_cierre_financiero_v1"]
    for table in core_tables:
        with pytest.raises((duckdb.CatalogException, duckdb.IOException, Exception)):
            v8_db.execute(f"DELETE FROM {table} WHERE 1=0")


# ═════════════════════════════════════════════════════════════════════════
# Gate 8: API v4/ledger endpoint returns correct structure
# ═════════════════════════════════════════════════════════════════════════

def test_gate_api_v4_ledger_endpoint():
    """GET /api/v4/ledger must return correct structure.
    v8_interceptor already redirects DatabaseV4 singleton to V8 temp."""
    from fastapi.testclient import TestClient
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from api.api import app

    # No override needed — v8_interceptor already redirects DatabaseV4 singleton
    client = TestClient(app)

    # Test basic ledger query
    resp = client.get("/api/v4/ledger", params={"marketplace": "ML", "limit": 5})
    assert resp.status_code == 200, f"GET /api/v4/ledger failed: {resp.text}"
    data = resp.json()
    assert "data" in data, "Response missing 'data'"
    assert "total_count" in data, "Response missing 'total_count'"
    assert isinstance(data["data"], list), "data must be list"
    assert data["total_count"] >= 0, "total_count must be non-negative"

    # Test signal_mode parameter
    resp = client.get("/api/v4/ledger", params={"marketplace": "RIPLEY", "signal_mode": "SIGNAL", "limit": 10})
    assert resp.status_code == 200, f"signal_mode test failed: {resp.text}"

    # Test detalle filter
    resp = client.get("/api/v4/ledger", params={"marketplace": "ML", "detalle": "Cargo por venta (Venta)", "limit": 1})
    assert resp.status_code == 200
    data = resp.json()
    for row in data["data"]:
        assert "Cargo por venta" in row.get("detalle", ""), "detalle filter not working"


# ═════════════════════════════════════════════════════════════════════════
# Session guard: Official DB must remain unchanged
# ═════════════════════════════════════════════════════════════════════════

def sha256(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def test_official_db_integrity():
    """Verify official DB was NOT modified during test session."""
    official_db = Path("data/db/meli_financial_v4.db")
    expected = "4EFCAA8AA950AA6731A1F0D16624E3A62F3831B7CAAF521E31218DEAF8155709"
    actual = sha256(official_db)
    assert actual == expected, (
        f"OFFICIAL DB MUTATED!\n"
        f"  Expected: {expected}\n"
        f"  Actual:   {actual}\n"
    )
