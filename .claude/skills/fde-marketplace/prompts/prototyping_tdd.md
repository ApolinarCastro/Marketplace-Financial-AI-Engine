# Prototyping TDD Protocol

**Mandatory for all Phase 2+ technical work. No code before tests.**

---

## TDD Cycle (Red → Green → Refactor → Certify)

### 1. RED — Write Failing Test First

```python
# tests/test_<capability>_<specific>.py
def test_<capability>_<specific_behavior>():
    """
    GIVEN: <certified data state>
    WHEN:  <action under test>
    THEN:  <expected outcome with exact values>
    """
    # Arrange - Use certified fixtures only
    from tests.fixtures import certified_ledger, certified_cierre
    
    # Act
    result = engine_under_test.method(input_params)
    
    # Assert - Exact values from certification evidence
    assert result.metric == EXPECTED_VALUE  # From governance/*_CERTIFICATION.md
    assert result.delta == 0  # Single Financial Truth requirement
```

**Requirements:**
- Test file named `test_<capability>_<behavior>.py`
- Uses ONLY certified data fixtures (no mocks for financial logic)
- Asserts exact certified values (from governance certificates)
- Fails before implementation exists

### 2. GREEN — Minimal Implementation

- Write ONLY enough code to pass the test
- Use existing public contracts (FinancialEngine, LedgerEngine, etc.)
- No new SQL in orchestration layers (P40R2A rule)
- No financial calculations in frontend

### 3. REFACTOR — Clean Up

- Remove duplication
- Centralize constants in `engine/v4/copilot/constants.py`
- Extract SQL to `engine/v4/sql/copilot_queries.py`
- Ensure `LOWER()` for case-insensitive marketplace/financial_group (DEC-035)

### 4. CERTIFY — Evidence Generation

```bash
# Run full regression
python -m pytest tests/ -x -q
# Expected: 273+/273+ PASS, 0 new regressions

# Run certification gate
python -m pytest tests/test_certification_gate.py -v
# Expected: 27/27 PASS

# Run FASE 1B validation (if applicable)
python tools/validate_fase_1b.py --phase <X>
# Expected: VERIFIED=YES, summary.json generated
```

---

## Test Organization

| Layer | Test File Pattern | Purpose |
|-------|-------------------|---------|
| Unit (engine) | `tests/test_<engine>_<method>.py` | Public contract methods |
| Integration | `tests/test_<pipeline>_integration.py` | Multi-engine flows |
| Certification | `tests/test_certification_gate.py` | 27 invariant tests |
| FASE 1B | `tests/test_fase_1b_*.py` | Governance evidence |
| Golden | `tests/test_<copilot>_golden.py` | Question→answer exact match |
| Benchmark | `tests/test_<component>_benchmark.py` | Latency regression |

---

## Fixtures — Use Certified Data Only

```python
# tests/conftest.py (reference)
@pytest.fixture
def certified_ledger():
    """marketplace_ledger_v1 — 207,600 rows, $1.636B, 69/69 periods $0 delta"""
    return FinancialEngine().query_ledger(...)

@pytest.fixture
def certified_cierre():
    """marketplace_cierre_financiero_v1 — 109 rows, PARIS/RIPLEY $0, ML structural"""
    return FinancialEngine().query_cierre(...)

@pytest.fixture
def certified_taxonomy_ripley():
    """knowledge/taxonomy/ripley_v1.json — 12 SIGNAL / 20 NOISE"""
    return load_taxonomy("ripley_v1")
```

**NEVER** create synthetic financial data in tests. Use certified fixtures.

---

## Anti-Patterns (Auto-Reject)

| Anti-Pattern | Rejection Reason |
|--------------|------------------|
| `mock.patch` on FinancialEngine | Tests must use real certified data |
| Hardcoded expected values not in certificates | Single Financial Truth violation |
| Test creates DB tables | Use existing certified schema |
| Test modifies ledger data | Ledger is immutable evidence |
| Frontend calculation test | Backend decides; frontend consumes |
| New SQL in test file | SQL belongs in `engine/v4/sql/` |

---

## Example: Adding a New Copilot Question Handler

### Step 1: Write Golden Test FIRST

```python
# tests/test_copilot_golden.py
def test_copilot_question_12_ripley_dte_coverage():
    """G12: '¿Cuál es la cobertura DTE de Ripley por mes?'"""
    from engine.v4.copilot.copilot_engine import CopilotEngine
    
    engine = CopilotEngine()
    result = engine.ask("¿Cuál es la cobertura DTE de Ripley por mes?", period="2026-06")
    
    # Exact structure required
    assert result["question"] == "¿Cuál es la cobertura DTE de Ripley por mes?"
    assert result["period"] == "2026-06"
    assert "answer" in result
    assert "explanation" in result
    assert "breakdown" in result
    assert "evidence" in result
    
    # Evidence validation
    evidence = result["evidence"]
    assert evidence["ledger"]["verified"] == True
    assert evidence["raw"]["verified"] == False  # Ripley XML not certified
    assert evidence["certification_status"] == "PARTIALLY_VERIFIED"
```

### Step 2: Run — Confirm RED

```bash
python -m pytest tests/test_copilot_golden.py::test_copilot_question_12_ripley_dte_coverage -v
# FAILED (handler doesn't exist)
```

### Step 3: Implement Handler (Green)

```python
# engine/v4/copilot/handlers/g12_ripley_dte.py
class G12RipleyDTECoverageHandler:
    def handle(self, period: str) -> dict:
        # Use EvidenceOrchestrator public contract only
        from engine.v4.evidence import EvidenceOrchestrator
        orchestrator = EvidenceOrchestrator()
        dte_data = orchestrator.get_dte_coverage("RIPLEY", period)
        
        return self._response(period, dte_data)
```

### Step 4: Register in CopilotEngine

```python
# engine/v4/copilot/copilot_engine.py
QUESTION_HANDLERS = {
    # ...
    "ripley_dte_coverage": G12RipleyDTECoverageHandler(),
}
```

### Step 5: Run — Confirm GREEN

```bash
python -m pytest tests/test_copilot_golden.py::test_copilot_question_12_ripley_dte_coverage -v
# PASSED
```

### Step 6: Full Regression + Cert Gate

```bash
python -m pytest tests/ -x -q
python -m pytest tests/test_certification_gate.py -v
```

---

## Evidence Requirements for PR

Every PR must include:
1. **Test file(s)** — New tests written first (TDD)
2. **Implementation** — Minimal, uses public contracts
3. **Evidence** — `evidence/<phase>/<task_id>_<timestamp>.json` with:
   - `execution_id`, `commit`, `timestamp`, `harness_version`
   - `unique_tests`, `aggregate_executions`, `execution_groups`
   - `implementation_status`, `validation_status`, `certification_status`
4. **Regression proof** — Full suite PASS count (e.g., "273/273 PASS, 0 new regressions")
5. **Cert Gate proof** — "27/27 PASS"

---

## Quick Reference: Test Commands

```bash
# Unit tests for specific engine
python -m pytest tests/test_financial_engine.py -v

# Integration tests
python -m pytest tests/test_evidence_orchestrator.py -v

# Full regression (MUST PASS)
python -m pytest tests/ -x -q

# Certification gate (MUST PASS)
python -m pytest tests/test_certification_gate.py -v

# FASE 1B validation
python tools/validate_fase_1b.py --phase 1b

# Golden tests (Copilot)
python -m pytest tests/test_copilot_golden.py -v

# Benchmarks
python -m pytest tests/test_copilot_benchmarks.py -v
```