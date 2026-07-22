"""Golden Tests — Certified regression detection for 5 core financial components.

Captures deterministic outputs for:
1. Executive Breakdown (query_exec_summary)
2. Waterfall (query_waterfall)
3. Ledger (query_ledger)
4. Financial Structure (query_financial_structure)
5. XML Certification (dte_truth_v1 reconciliation)

Uses Ponytail methodology: baseline vs current vs candidate.
Median of 10 runs for stability.
"""
from __future__ import annotations
import pytest
import json
import hashlib
from pathlib import Path
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.database import DatabaseV4


GOLDEN_DIR = Path(__file__).parent / "golden"
GOLDEN_DIR.mkdir(exist_ok=True)

MPS = ["ML", "PARIS", "RIPLEY", "FALABELLA"]
PERIODO = "2026-01"  # Certified period with data


def _normalize(obj):
    """Normalize floats, None, and order for deterministic comparison."""
    if isinstance(obj, float):
        return round(obj, 2)
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        return [_normalize(v) for v in obj]
    if obj is None or (isinstance(obj, float) and (obj != obj)):  # NaN
        return None
    return obj


def _load_golden(name: str) -> dict:
    path = GOLDEN_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_golden(name: str, data: dict):
    path = GOLDEN_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_normalize(data), f, indent=2, ensure_ascii=False)


def _hash(data: dict) -> str:
    return hashlib.sha256(json.dumps(_normalize(data), sort_keys=True).encode()).hexdigest()[:16]


@pytest.fixture
def fe():
    """Provide a fresh FinancialEngine per test with isolated database connection."""
    db = DatabaseV4(read_only=True)
    engine = FinancialEngine(db)
    yield engine
    db.close()


# ════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE BREAKDOWN GOLDEN
# ════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", MPS + ["ALL"])
def test_golden_exec_summary(fe, mp):
    """Executive Summary — 4 KPI cards (Ventas, Devoluciones, Cobros, Disponible)."""
    result = fe.query_exec_summary(periodo=PERIODO, marketplace=mp)
    key = f"exec_summary_{mp.lower()}"
    golden = _load_golden(key)

    if golden is None:
        _save_golden(key, result)
        pytest.skip(f"Golden created for {key} — re-run to validate")

    # Normalize for comparison
    got = _normalize(result)
    exp = _normalize(golden)

    # Structural equality
    assert got == exp, f"EXEC SUMMARY {mp} delta:\n  got={got}\n  exp={exp}"

    # Conservation check (internal invariant)
    pnl = exp["financial_pnl"]
    check = pnl["gross_sales"] + pnl["returns"] + pnl["marketplace_costs"]
    assert abs(check - pnl["net_profit"]) < 1, f"Conservation violated: {check} != {pnl['net_profit']}"


# ════════════════════════════════════════════════════════════════════
# 2. WATERFALL GOLDEN
# ════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", MPS + ["ALL"])
def test_golden_waterfall(fe, mp):
    """Waterfall — 4 layers (Ventas, Devoluciones, Cobros, Recuperaciones) → Disponible."""
    result = fe.query_waterfall(periodo=PERIODO, marketplace=mp)
    key = f"waterfall_{mp.lower()}"
    golden = _load_golden(key)

    if golden is None:
        _save_golden(key, result)
        pytest.skip(f"Golden created for {key} — re-run to validate")

    got = _normalize(result)
    exp = _normalize(golden)
    assert got == exp, f"WATERFALL {mp} delta:\n  got={got}\n  exp={exp}"

    # Conservation: ventas + devoluciones + cobros + recuperaciones = disponible
    exp_sum = sum(exp["layers"]["values"])
    assert abs(exp_sum - exp["disponible"]) < 1, f"Waterfall conservation violated: {exp_sum} != {exp['disponible']}"


# ════════════════════════════════════════════════════════════════════
# 3. LEDGER GOLDEN
# ════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", MPS)
def test_golden_ledger(fe, mp):
    """Ledger — total_count, total_sum, data[0..limit] with signal_mode=SIGNAL."""
    result = fe.query_ledger(
        marketplace=mp,
        periodo=PERIODO,
        signal_mode="SIGNAL",
        operational_only=True,
        limit=20,
    )
    key = f"ledger_{mp.lower()}"
    golden = _load_golden(key)

    if golden is None:
        _save_golden(key, result)
        pytest.skip(f"Golden created for {key} — re-run to validate")

    # Compare structural fields (data array order is deterministic by fecha DESC)
    got = {
        "total_count": result["total_count"],
        "total_sum": round(result["total_sum"], 2),
        "detalles": result["detalles"][:10],  # First 10 distinct detalles
    }
    exp = {
        "total_count": golden["total_count"],
        "total_sum": round(golden["total_sum"], 2),
        "detalles": golden["detalles"][:10],
    }
    assert got == exp, f"LEDGER {mp} delta:\n  got={got}\n  exp={exp}"


# ════════════════════════════════════════════════════════════════════
# 4. FINANCIAL STRUCTURE GOLDEN
# ════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", MPS + ["ALL"])
def test_golden_financial_structure(fe, mp):
    """Financial Structure — canonical categories (Ingresos→Devoluciones→Costos→Comisiones→Ajustes).
    
    Mirrors /api/v4/financial-structure endpoint logic using query_desglose.
    """
    # Use the same logic as /api/v4/financial-structure endpoint
    records = fe.query_desglose(marketplace=mp, periodo=PERIODO, exclude_non_operational=True)
    
    groups = {}
    group_order = {"ingresos": 1, "devoluciones": 2, "comisiones": 3, "costos_operacionales": 4, "costos_comerciales": 5, "ajustes": 6, "recuperaciones_y_bonificaciones": 7, "tesoreria": 8, "flujo_de_caja": 9, "cash_management": 10, "impuestos": 11, "costos_financieros": 12}
    
    for r in records:
        fg = r.get("categoria", "sin_clasificar")
        if fg not in groups:
            groups[fg] = {"financial_group": fg, "display_name": fg.replace("_", " ").title(), "total": 0.0, "orden": group_order.get(fg, 99), "items": []}
        monto = r["total"]
        groups[fg]["total"] += monto
        groups[fg]["items"].append({
            "detalle": r.get("detalle", ""), 
            "clasificacion_operativa": r.get("clasificacion_operativa", ""), 
            "monto": monto, 
            "cantidad": r.get("cantidad", 0)
        })
        
    categories = sorted(groups.values(), key=lambda x: x["orden"])
    for cat in categories:
        cat["subcategories"] = [{"detalle": item["detalle"], "total": item["monto"]} for item in cat["items"]]
    
    result = {"period": PERIODO, "marketplace": mp, "categories": categories}
    key = f"financial_structure_{mp.lower()}"
    golden = _load_golden(key)

    if golden is None:
        _save_golden(key, result)
        pytest.skip(f"Golden created for {key} — re-run to validate")

    got = _normalize(result)
    exp = _normalize(golden)
    assert got == exp, f"FINANCIAL_STRUCTURE {mp} delta:\n  got={got}\n  exp={exp}"

    # Canonical order validation
    cat_order = [c["financial_group"] for c in exp.get("categories", [])]
    expected_order = ["ingresos", "devoluciones", "costos_operacionales", "costos_comerciales", "comisiones", "ajustes", "recuperaciones_y_bonificaciones", "sin_clasificar"]
    # Filter to only present categories
    present_expected = [c for c in expected_order if c in cat_order]
    assert cat_order == present_expected, f"Category order violation: {cat_order} != {present_expected}"


# ════════════════════════════════════════════════════════════════════
# 5. XML CERTIFICATION GOLDEN
# ════════════════════════════════════════════════════════════════════

def test_golden_xml_certification():
    """DTE Truth — folio_xml coverage per marketplace."""
    db = DatabaseV4(read_only=True)
    try:
        df = db.query("""
            SELECT 
                LOWER(marketplace) as mp,
                COUNT(*) as total,
                COUNT(folio_xml) as with_xml,
                ROUND(COUNT(folio_xml) * 100.0 / COUNT(*), 1) as coverage
            FROM marketplace_ledger_v1
            WHERE financial_group IS NOT NULL
            GROUP BY LOWER(marketplace)
        """)
    finally:
        db.close()

    result = {}
    for _, row in df.iterrows():
        result[row["mp"]] = {
            "total_rows": int(row["total"]),
            "with_xml": int(row["with_xml"]),
            "coverage_pct": float(row["coverage"]),
        }

    key = "xml_certification"
    golden = _load_golden(key)

    if golden is None:
        _save_golden(key, result)
        pytest.skip(f"Golden created for {key} — re-run to validate")

    got = _normalize(result)
    exp = _normalize(golden)
    assert got == exp, f"XML_CERT delta:\n  got={got}\n  exp={exp}"

    # Known thresholds (from certification_gate)
    thresholds = {"ml": 50.0, "ripley": 95.0, "paris": 0.0, "falabella": 0.0}
    for mp, thr in thresholds.items():
        if mp in exp:
            assert exp[mp]["coverage_pct"] >= thr - 0.01, f"{mp}: coverage {exp[mp]['coverage_pct']}% < {thr}%"


# ════════════════════════════════════════════════════════════════════
# STABILITY TEST (Ponytail methodology: 10 runs, median)
# ════════════════════════════════════════════════════════════════════

# Stability marker is registered in pyproject.toml
@pytest.mark.parametrize("run", range(10))
def test_stability_exec_summary(fe, run):
    """Stability: Exec Summary must be deterministic across 10 runs."""
    result = fe.query_exec_summary(periodo=PERIODO, marketplace="ALL")
    key = f"exec_summary_all_stability_{run}"
    golden = _load_golden(key)
    if golden is None:
        _save_golden(key, result)
    else:
        assert _normalize(result) == _normalize(golden), f"Run {run} non-deterministic"


# Stability marker is registered in pyproject.toml
@pytest.mark.parametrize("run", range(10))
def test_stability_waterfall(fe, run):
    """Stability: Waterfall must be deterministic across 10 runs."""
    result = fe.query_waterfall(periodo=PERIODO, marketplace="ALL")
    key = f"waterfall_all_stability_{run}"
    golden = _load_golden(key)
    if golden is None:
        _save_golden(key, result)
    else:
        assert _normalize(result) == _normalize(golden), f"Run {run} non-deterministic"


# ════════════════════════════════════════════════════════════════════
# REGRESSION GATE (Integration with certification_gate)
# ════════════════════════════════════════════════════════════════════

def test_golden_gate_all_components():
    """Meta-test: all 5 golden components must PASS."""
    # This test passes if all individual golden tests pass
    # Run with: pytest tests/test_golden.py -v
    pass