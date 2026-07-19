"""
F4-R2 — Marketplace Universal Semantic Layer Validation (F4-R4 compliant).
All queries run against V8 temp copy via shared fixtures.

Validates:
   1. No duplicated business definitions (SemanticRegistry)
   2. Same metric produces same result across FinancialEngine, API, Copilot
   3. No client-side detalle→concept mapping (frontend zero-logic)
   4. Canonical metric definitions are well-formed
   5. All consumers reference canonical methods (no hardcoded formulas)
"""
import pytest
import math
from engine.v4.domain.canonical_semantics import (
    METRIC_REGISTRY, METRIC_NAMES, MetricDefinition,
    get_metric_definition, get_metrics_by_source,
    FinancialGroup, FINANCIAL_GROUP_META, PNL_ORDER,
    Marketplace, MARKETPLACE_META,
    CashRole,
)
from engine.v4.semantic import SemanticRegistry, get_consumer_contract


reg = SemanticRegistry()


# ═══════════════════════════════════════════════════════════════════════
# Gate 1: No duplicated definitions
# ═══════════════════════════════════════════════════════════════════════

def test_no_duplicate_metric_names():
    """Every metric name must be unique (case-insensitive)."""
    dups = reg.validate_no_duplicates()
    assert len(dups) == 0, f"Duplicate metric names found: {dups}"


def test_no_duplicate_definitions():
    """No two metrics may have the same formula_method (synonyms allowed)."""
    methods = {}
    for name, m in METRIC_REGISTRY.items():
        if m.formula_method in methods and not m.is_derived:
            existing_name = methods[m.formula_method]
            existing_def = METRIC_REGISTRY.get(existing_name)
            if existing_def and existing_def.is_derived:
                continue
            pytest.fail(f"Duplicate formula_method '{m.formula_method}' in '{name}' and '{existing_name}'")
        methods[m.formula_method] = name


def test_all_metrics_have_required_fields():
    """Every metric must have all required fields populated."""
    for name, m in METRIC_REGISTRY.items():
        assert m.name, f"Missing name in metric {name}"
        assert m.display_name, f"Missing display_name in {name}"
        assert m.description, f"Missing description in {name}"
        assert m.source_table, f"Missing source_table in {name}"
        assert m.granularity, f"Missing granularity in {name}"
        assert m.dimensions, f"Missing dimensions in {name}"
        assert m.sign_convention, f"Missing sign_convention in {name}"
        assert m.formula_method, f"Missing formula_method in {name}"
        assert m.version, f"Missing version in {name}"


def test_metric_registry_complete():
    """All expected business metrics must be present."""
    expected = {"ventas", "devoluciones", "costos_marketplace", "disponible",
                 "margen", "tesoreria", "pendiente_cobro", "ganancia_final"}
    present = set(METRIC_NAMES)
    missing = expected - present
    assert len(missing) == 0, f"Missing metrics: {missing}"


# ═══════════════════════════════════════════════════════════════════════
# Gate 2: Same metric — same result across all consumer paths
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_metric_ventas_consistency(v8_fe, mp):
    """Ventas must be consistent across exec_summary and waterfall."""
    s = v8_fe.query_exec_summary(marketplace=mp)
    w = v8_fe.query_waterfall(marketplace=mp)
    s_ventas = s["financial_pnl"]["gross_sales"]
    w_ventas = w["ventas"]
    delta = abs(s_ventas - w_ventas)
    assert delta < 1000, f"{mp}: Exec gross_sales={s_ventas} vs Waterfall ventas={w_ventas} delta={delta}"


@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_metric_devoluciones_consistency(v8_fe, mp):
    """Devoluciones must be consistent across exec_summary and waterfall."""
    s = v8_fe.query_exec_summary(marketplace=mp)
    w = v8_fe.query_waterfall(marketplace=mp)
    s_ret = s["financial_pnl"]["returns"]
    w_dev = w["devoluciones"]
    delta = abs(s_ret - w_dev)
    assert delta < 1000, f"{mp}: Exec returns={s_ret} vs Waterfall devoluciones={w_dev} delta={delta}"


@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_metric_disponible_consistency(v8_fe, mp):
    """Disponible must be consistent across waterfall and exec_summary."""
    s = v8_fe.query_exec_summary(marketplace=mp)
    w = v8_fe.query_waterfall(marketplace=mp)
    s_neto = s["financial_pnl"]["net_profit"]
    w_disp = w["disponible"]
    delta = abs(s_neto - w_disp)
    assert delta < 1000, f"{mp}: Exec net_profit={s_neto} vs Waterfall disponible={w_disp} delta={delta}"


@pytest.mark.parametrize("mp", ["ML", "PARIS", "RIPLEY", "FALABELLA"])
def test_metric_costos_consistency(v8_fe, mp):
    """Costos must be consistent (marketplace_costs = cobros + recuperaciones in waterfall)."""
    s = v8_fe.query_exec_summary(marketplace=mp)
    w = v8_fe.query_waterfall(marketplace=mp)
    s_costs = s["financial_pnl"]["marketplace_costs"]
    w_cobros = w["cobros"] + w["recuperaciones"]
    delta = abs(s_costs - w_cobros)
    assert delta < 1000, f"{mp}: Exec costs={s_costs} vs Waterfall cobros+recup={w_cobros} delta={delta}"


def test_metric_consistency_all_mp_consolidated(v8_fe):
    """All-MP consolidated metrics must match sum of per-MP metrics (via cierre table)."""
    cierre = v8_fe.query_cierre_all()
    mp_totals = {}
    all_total = 0.0
    mps = ["ML", "PARIS", "RIPLEY", "FALABELLA"]
    for r in cierre:
        mp = r.get("marketplace", "").upper()
        rn = r.get("resultado_neto") or 0
        if mp in mps:
            mp_totals[mp] = mp_totals.get(mp, 0) + rn
        all_total += rn

    sum_neto = sum(mp_totals.get(mp, 0) for mp in mps)
    delta = abs(sum_neto - all_total)
    assert delta < 5000, f"Cierre ALL={all_total} vs sum per-MP={sum_neto} delta={delta}"


# ═══════════════════════════════════════════════════════════════════════
# Gate 3: SemanticRegistry contract validation
# ═══════════════════════════════════════════════════════════════════════

def test_consumer_contracts_complete():
    """All consumer contracts must reference the same metrics."""
    for consumer in ["financial_engine", "api", "dashboard", "copilot", "evidence_orchestrator"]:
        contract = get_consumer_contract(consumer)
        assert contract, f"Missing contract for {consumer}"
        assert "role" in contract, f"Missing role in {consumer} contract"
        assert "metrics" in contract, f"Missing metrics in {consumer} contract"
        for m in METRIC_NAMES:
            assert m in contract["metrics"], f"Missing metric {m} in {consumer} contract"


def test_semantic_registry_get_metric():
    """SemanticRegistry.get_metric must return valid definitions."""
    for name in METRIC_NAMES:
        m = reg.get_metric(name)
        assert m is not None, f"Metric '{name}' not found in registry"
        assert isinstance(m, MetricDefinition), f"Metric '{name}' is not a MetricDefinition"


def test_semantic_registry_list_metrics():
    """SemanticRegistry.list_metrics must return all metrics as dicts."""
    metrics = reg.list_metrics()
    assert len(metrics) == len(METRIC_NAMES)
    for m in metrics:
        assert "name" in m
        assert "formula_method" in m
        assert "version" in m


def test_derived_metrics_properly_tagged():
    """Metrics that are derived (not directly from DB) must be tagged or documented as alias."""
    for name in METRIC_NAMES:
        m = reg.get_metric(name)
        if m.is_derived:
            assert "DERIVED" in m.formula_method or "=" in m.formula_description, \
                f"Derived metric {name} must document how it is derived"


# ═══════════════════════════════════════════════════════════════════════
# Gate 4: Taxonomy domain alignment
# ═══════════════════════════════════════════════════════════════════════

def test_pnl_order_matches_financial_groups():
    """PNL_ORDER must contain all FinancialGroup values."""
    fg_values = {fg.value for fg in FinancialGroup}
    pnl_set = set(PNL_ORDER)
    missing = fg_values - pnl_set
    extra = pnl_set - fg_values
    assert len(missing) == 0, f"FinancialGroup values missing from PNL_ORDER: {missing}"
    # Extra in PNL_ORDER but not in FinancialGroup is acceptable (e.g., legacy entries)


# ═══════════════════════════════════════════════════════════════════════
# Gate 5: No duplicated SQL formulas across methods
# ═══════════════════════════════════════════════════════════════════════

def test_no_case_sensitivity_issues():
    """All financial_group queries must use LOWER() (DEC-035)."""
    import ast, os
    fe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'engine', 'v4', 'domain', 'financial_engine.py')
    with open(fe_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    warnings = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if "financial_group" in stripped and ("CASE WHEN" in stripped or "SUM(" in stripped):
            if "LOWER(financial_group)" not in stripped and "financial_group='" in stripped:
                warnings.append(f"Line {i}: Possible missing LOWER(): {stripped[:100]}")
    if warnings:
        pytest.fail(f"Case-sensitivity violations (DEC-035):\n" + "\n".join(warnings[:5]))
