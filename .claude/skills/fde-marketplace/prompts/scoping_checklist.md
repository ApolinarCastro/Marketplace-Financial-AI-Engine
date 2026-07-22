# Scoping Checklist — Codex Pre-Authorization

**Run this checklist BEFORE registering a task in coordination_state.json**

---

## 1. Governance Alignment

- [ ] Objective maps to a specific Phase in MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md
- [ ] Phase gate entry criteria met (previous phase CERTIFIED)
- [ ] No conflict with FOUNDATION_RESET.md 10 Pillars or Golden Rules
- [ ] No conflict with DEC-019 (Single Financial Truth, PosCobro exclusion)
- [ ] No conflict with Marketplace Isolation (each MP independent)
- [ ] No conflict with Evidence First (RAW → ... → Dashboard chain)

## 2. Scope Discipline

- [ ] **Single task only** — no "while we're at it" additions
- [ ] Scope fits in **one OpenCode session** (small, reversible changes)
- [ ] No financial logic modifications without RFC
- [ ] No RC1 protected path modifications (`engine/rc1/`, `engine/v4/` core engines)
- [ ] No new API contracts without public contract audit (P40 pattern)
- [ ] No frontend financial calculations (backend decides)

## 3. Evidence Requirements Defined

- [ ] Evidence type identified: `validate_fase_1b.py` / `test_certification_gate.py` / custom
- [ ] Expected `execution_id` format understood
- [ ] Required fields: `execution_id`, `commit`, `timestamp`, `harness_version`, `status`
- [ ] Evidence output path: `evidence/fase_1b/` or `evidence/fase_2/` etc.

## 4. Test Strategy

- [ ] Tests written FIRST (TDD) — `prompts/prototyping_tdd.md`
- [ ] Regression suite identified: `python -m pytest tests/ -x -q` (must stay 273/273+ PASS)
- [ ] New tests added to appropriate test file
- [ ] Certification Gate impact assessed: `tests/test_certification_gate.py` (27 tests)

## 5. Resource & Cost Check

- [ ] Zero monetary cost (no paid APIs, cloud, SaaS)
- [ ] Uses existing stack: Python, DuckDB, FastAPI, pytest, Ollama, Git
- [ ] No global config modifications (`~/.codex`, `~/.claude`, etc.)

## 6. Coordination Protocol

- [ ] Task will be registered in `governance/coordination/coordination_state.json`
- [ ] Only ONE active task at a time
- [ ] OpenCode will report ALL modified files
- [ ] Codex will review diff before verdict
- [ ] Execution Board will be regenerated: `python tools/generate_execution_board.py`

## 7. TimesFM Isolation (if forecasting related)

- [ ] Uses separate DB: `data/forecasting/marketplace_forecasting_v1.duckdb`
- [ ] Never writes to `data/db/meli_financial_v4.db`
- [ ] Never modifies ledger/classification/closing tables
- [ ] Forecasts labeled "Pronóstico — no certificado"
- [ ] Backtesting uses temporal splits only (no future leakage)

---

## Authorization Decision

| Check | Status |
|-------|--------|
| Governance Alignment | ☐ PASS / ☐ FAIL |
| Scope Discipline | ☐ PASS / ☐ FAIL |
| Evidence Requirements | ☐ PASS / ☐ FAIL |
| Test Strategy | ☐ PASS / ☐ FAIL |
| Resource & Cost | ☐ PASS / ☐ FAIL |
| Coordination Protocol | ☐ PASS / ☐ FAIL |
| TimesFM Isolation | ☐ PASS / ☐ FAIL / ☐ N/A |

**Overall:** `AUTHORIZED` / `REQUIRES_REMEDIATION` / `BLOCKED`

**Codex Signature:** ________________ **Date:** ________________

**Task ID Registered:** `TASK-XXXX` in `coordination_state.json`