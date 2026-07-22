# FDE Marketplace Financial Operating System Skill

> **Forward Deployed Engineering (FDE) methodology adapted for Marketplace Financial Operating System.**
> Production-grade methodology + tools that turn OpenCode into a forward-deployed engineer for financial reconciliation, evidence chains, and certified financial intelligence.

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-orange)](LICENSE)
[![Source: fde-consultants-protocoles@072f005](https://img.shields.io/badge/source-fde--consultants--protocoles%40072f005-blue)](https://github.com/selectess/fde-consultants-protocoles/tree/072f005e701b671d1e03a26dae2848e9b492fc32)

---

## What is FDE Marketplace?

**FDE Marketplace** encodes the Forward Deployed Engineering methodology — the discipline pioneered at Palantir (~2010) and now standard across enterprise AI engineering teams — specifically for the **Marketplace Financial Operating System** context.

In 2026, FDE postings grew **729% year-over-year**. This Skill adapts that workflow for a system that must:
- Demonstrate the complete journey of every transaction from RAW file → bank settlement
- Answer any financial question automatically with verifiable evidence chains
- Maintain a **Single Financial Truth** (DEC-019) across 4 marketplaces (ML, Paris, Falabella, Ripley)
- Operate at **zero monetary cost** (no paid APIs, no cloud dependencies)

---

## Core Adaptation: Marketplace Financial Operating System Context

This skill is **not** a generic FDE implementation. It is bound to:

### Governing Documents (Authority Order)
1. **FOUNDATION_RESET.md** — Mission, Vision, 10 Pillars, Golden Rules, Success Criteria
2. **MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md** — 23-phase execution model, roles, gates
3. **DEC-019** — Single Financial Truth (PosCobro paired = same event as Devolución, excluded from P&L)
4. **Marketplace Isolation** — Each MP (ML, Paris, Falabella, Ripley) has independent ingestion → ledger → closing
5. **Evidence First** — Every figure must trace: RAW → Registry → ETL → Ledger → Classification → Closing → XML → Settlement → Bank → Dashboard → Copilot
6. **Backend Decides; Frontend Consumes** — Zero financial logic in templates
7. **Zero Cost** — OpenCode executes; Ollama local; Python/DuckDB/FastAPI/pytest/Git
8. **OpenCode Executes; Codex Supervises & Certifies Evidence**
9. **Owner (Apolinar Castro) Retains Final Authority**

### Current System State (as of 2026-07-17)
- **273/273 tests PASS** (Phase 16F complete)
- **4 marketplaces** in certified ledger: ML ($842M), Paris ($378M), Ripley ($414M), Falabella ($2.6M)
- **69/69 period-MP combos** reconciled: Ingresos/Devoluciones $0 delta ✅
- **Ripley 54.1% NOISE eliminated** via SIGNAL/NOISE taxonomy (11/32 detalle values = SIGNAL)
- **PosCobro DELETED** from financial model (DEC-009): 99.77% redundant, $0 cash impact
- **Evidence Orchestrator** (P40 Phase 2) deployed — 5 API endpoints at `/api/v4/evidence/*`
- **Automatic Ingestion Platform** (Phase 1) certified — 41/41 tests PASS
- **Certification Gate** mandatory (`test_certification_gate.py` — 27 tests blocks deployment)

---

## The 6-Q Decomposition (Marketplace-Adapted)

**Before ANY technical package**, the FDE profile must answer:

| Q | Question | Marketplace Context |
|---|----------|---------------------|
| **Q1** | What **real process** is being corrected? | e.g., "Ripley XML folio linkage gap (0% certified)" |
| **Q2** | What **decision** must this enable? | e.g., "Certify Ripley DTE coverage for audit" |
| **Q3** | What **certified data** does it use? | e.g., "marketplace_ledger_v1 + dte_truth_v1 + RAW XMLs at 01_Raw/RIPLEY/Documentos Recepcionados/" |
| **Q4** | What is the **cost of error**? | e.g., "$186.7M Ripley XML coverage uncertified → audit finding risk" |
| **Q5** | What **exists currently**? | e.g., "407 XMLs discovered; DTEIndexer heuristic 0 matches; order_id matcher not built" |
| **Q6** | How will **success be demonstrated**? | e.g., "DTE coverage ≥ 80% per period; backtest delta $0 vs ledger" |

**No technical work begins until all 6-Q are answered in writing.**

---

## Operating Principles (Non-Negotiable) — Marketplace Edition

| # | Principle | Marketplace Enforcement |
|---|-----------|------------------------|
| 1 | **Scoping before coding** | 6-Q written → Codex approves → OpenCode executes single task |
| 2 | **Evals before claiming accuracy** | Every financial claim backed by `evidence/fase_1b/` JSON with `execution_id`, `commit`, `timestamp` |
| 3 | **No self-certification** | Certification Gate (27 tests) + 3 clean runs required for CERTIFIED |
| 4 | **Reproducible evidence** | `tools/validate_fase_1b.py` harness = only valid evidence producer |
| 5 | **Single Financial Truth** | All queries route through `FinancialEngine` / `LedgerEngine` public contracts; never raw SQL in frontend |
| 6 | **Marketplace isolation** | No cross-MP contamination; each MP has independent taxonomy, ledger, closing |
| 7 | **Evidence First** | Every number on dashboard/Copilot traces to `cierre_financiero_v1` → `marketplace_ledger_v1` → RAW |
| 8 | **Backend decides** | 0 financial calculations in `templates/*.html`; all via `/api/v4/*` endpoints |
| 9 | **Zero cost** | No paid APIs, no cloud, no SaaS; Ollama + local DuckDB only |
| 10 | **Owner authority** | Apolinar approves phase gates; Codex verifies evidence; OpenCode executes |
| 11 | **DEC-019 immutable** | PosCobro paired = same event as Devolución; `include_in_operational_pnl=0`; never re-run classification |
| 12 | **TimesFM isolated** | Forecasting DB separate (`data/forecasting/marketplace_forecasting_v1.duckdb`); never writes ledger |
| 13 | **Continuous learning** | Every ingestion → Knowledge Index update → Obsidian sync → Pattern Registry |
| 14 | **No parallel channels** | Coordination ONLY via `governance/coordination/` JSON files |

---

## Anti-Patterns (Never Produce) — Marketplace Edition

| Anti-Pattern | Marketplace Manifestation | Rejection |
|-------------|---------------------------|-----------|
| "Just use AI/ML" | "Let TimesFM predict revenue" without certified historical series | ❌ Reject: No certified series = no forecast |
| Trust me bro | "Dashboard shows correct net revenue" without `cierre_financiero_v1` trace | ❌ Reject: Show evidence chain |
| Magic number default | `take_rate = 0.179` hardcoded without driver decomposition (G5.6) | ❌ Reject: Use `REVENUE_ENGINE_DECOMPOSITION` drivers |
| Self-certification | "CERTIFIED" in markdown without `execution_id` + 3 clean runs | ❌ Reject: Only Certification Gate verdict counts |
| Buzzword inflation | "Agentic reconciliation" without `ReconciliationEngine` contract | ❌ Reject: Use public contracts only |
| Fake URLs | `https://marketplace-financial.ai/docs/...` that 404 | ❌ Reject: Only real repo paths |
| Scope creep | "Add forecasting" before Phase 2 Runtime Truth complete | ❌ Reject: Master Plan sequence mandatory |
| Raw dependency | Code reads `01_Raw/` directly after ingestion | ❌ Reject: Post-ingestion = DuckDB only |
| Financial logic in frontend | `mapDetalleToConcept()` in dashboard.html (removed Phase 14A) | ❌ Reject: Moved to `/api/v4/exec/cobros-breakdown` |
| Unverified claim | "Ripley net revenue = $206.9M" without `governance/RIPLEY_DASHBOARD_RECOVERY_CERTIFICATION.md` | ❌ Reject: Cite evidence file |

---

## 4-Stage Loop (Marketplace Execution Model)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SCOPING (Codex + Owner)                         │
│  • 6-Q decomposition written                                        │
│  • Gate: Owner approves objective → Codex authorizes ONE task       │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   PROTOTYPING (OpenCode)                            │
│  • Small, reversible changes                                        │
│  • Tests written FIRST (TDD)                                        │
│  • Evidence generated via `validate_fase_1b.py`                     │
│  • No financial logic in frontend                                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 PRODUCTION READINESS (Codex Review)                 │
│  • Diff reviewed against RC1 protected paths                        │
│  • Regression suite: 273/273 + new tests PASS                       │
│  • Certification Gate: 27/27 PASS                                   │
│  • Evidence JSON: execution_id, commit, timestamp, harness_version  │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FEEDBACK & LEARNING                            │
│  • Knowledge Index updated (Obsidian + knowledge_index.yaml)        │
│  • Pattern Registry updated                                         │
│  • Decision Registry updated                                        │
│  • Next 6-Q scoped                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

**One task at a time.** No parallel capabilities. Codex registers active task in `governance/coordination/coordination_state.json`.

---

## MCP Tools (Adapted — Zero External Dependencies)

The original FDE skill exposes 7 MCP tools via stdio. **This adaptation exposes ZERO MCP tools.** Instead, it provides **prompt templates** and **validation scripts** that OpenCode executes directly using the existing codebase.

### Available Validation Scripts (in repo)

| Script | Purpose | Marketplace Gate |
|--------|---------|-----------------|
| `tools/validate_fase_1b.py` | Official evidence harness (R5-compliant) | Phase 1B certification |
| `tools/evidence_consistency_check.py` | Cross-evidence consistency audit | C5 verification |
| `tests/test_certification_gate.py` | 27 tests blocking deployment | Every deployment |
| `engine/v4/closing/closing_engine.py` | Safe-mode period close orchestration | Phase 12.4 |
| `engine/v4/evidence/EvidenceOrchestrator` | Evidence chain via public contracts | P40 Phase 2 |

### Prompt Templates (in `prompts/`)

| Template | Use Case |
|----------|----------|
| `6q_decomposition.md` | Write 6-Q before any task |
| `scoping_checklist.md` | Codex pre-authorization checklist |
| `prototyping_tdd.md` | OpenCode TDD execution template |
| `evidence_requirements.md` | What evidence must be produced |
| `certification_gate.md` | Pre-deployment gate checklist |

---

## FDE Assurance Score (Marketplace Adaptation)

Every deliverable must self-assess and include in evidence:

| Component | Max | Marketplace Requirement |
|-----------|-----|------------------------|
| **Claim (falsifiable)** | 25 | Specific financial metric + period + MP + delta vs baseline |
| **Contradiction (known limits)** | 25 | Explicitly state: what could be wrong, coverage gaps, assumptions |
| **Evidence trail (file:line + SHA-256)** | 30 | Every number cites: `governance/*.md:line` + `evidence/fase_1b/*.json` + `execution_id` |
| **Anti-patterns (no buzzwords, no self-cert)** | 20 | Zero violations of Anti-Patterns table above |
| **TOTAL** | **100** | **≥ 85 = eligible for Certification Gate** |

**Certification requires:** FDE Assurance Score ≥ 85 **+** Certification Gate 27/27 PASS **+** 3 clean consecutive runs from controlled environment.

---

## Skill Structure

```
.claude/skills/fde-marketplace/
├── SKILL.md                    # This file
├── LICENSE                     # Apache-2.0 (copied from source)
├── prompts/
│   ├── 6q_decomposition.md
│   ├── scoping_checklist.md
│   ├── prototyping_tdd.md
│   ├── evidence_requirements.md
│   └── certification_gate.md
├── templates/
│   ├── evidence_template.json
│   ├── task_card.md
│   └── phase_gate_report.md
├── scripts/
│   └── validate_fde_score.py   # Local FDE Assurance Score calculator
└── references/
    ├── FOUNDATION_RESET.md     # Copied reference
    ├── MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md  # Copied reference
    └── DEC-019_SINGLE_FINANCIAL_TRUTH.md  # Copied reference
```

---

## Usage

### For Codex (Direction & Supervision)

1. **Receive objective from Owner** (Apolinar)
2. **Require 6-Q decomposition** — use `prompts/6q_decomposition.md`
3. **Run scoping checklist** — `prompts/scoping_checklist.md`
4. **Authorize ONE task** — register in `governance/coordination/coordination_state.json`
5. **Review OpenCode diff** — verify against RC1 protected paths, DEC-019, Single Financial Truth
6. **Run Certification Gate** — `python -m pytest tests/test_certification_gate.py -v`
7. **Verify evidence** — `python tools/evidence_consistency_check.py evidence/fase_1b/`
8. **Emit verdict** — APPROVED_TO_CONTINUE / REQUIRES_REMEDIATION / BLOCKED_BY_EVIDENCE / REJECTED / CERTIFIED
9. **Update Execution Board** — `tools/generate_execution_board.py`

### For OpenCode (Controlled Execution)

1. **Read coordination files first** — `governance/coordination/*.json`
2. **Read this SKILL.md** — understand constraints
3. **Execute ONLY authorized task** — no scope expansion
4. **Write tests FIRST** (TDD) — use `prompts/prototyping_tdd.md`
5. **Make small, reversible changes** — single file where possible
6. **Generate evidence** — `python tools/validate_fase_1b.py` for certification tasks
7. **Report all modified files** — in task completion message
8. **Stop on contradiction** — if FOUNDATION_RESET vs MASTER_PLAN vs DEC-019 conflict

### For Owner (Apolinar Castro)

- Approves Master Plan activation
- Defines business priorities
- Authorizes phase gates (Phase 0 → 1 → 2 → ...)
- Confirms economic meaning of rules
- Final GO/NO-GO for production

---

## TimesFM Architecture Reservation (Per PAUSA Controlada)

**TimesFM is NOT installed in the core.** This skill reserves the architecture for Phase 2 — Runtime Truth:

### Data Contract (Separate DB: `data/forecasting/marketplace_forecasting_v1.duckdb`)

```sql
-- forecast_series_v1: What series exist
CREATE TABLE forecast_series_v1 (
  series_id      TEXT PRIMARY KEY,      -- e.g., "ML::VENTAS::SKU_123"
  marketplace    TEXT NOT NULL,         -- ML, PARIS, FALABELLA, RIPLEY
  metric         TEXT NOT NULL,         -- VENTAS, DEVOLUCIONES, COSTOS, LIQUIDACIONES, BANCO
  granularity    TEXT NOT NULL,         -- DAILY, WEEKLY, MONTHLY
  sku            TEXT,                  -- NULL = aggregate
  start_date     DATE NOT NULL,
  end_date       DATE NOT NULL,
  n_observations INTEGER NOT NULL,
  certified_hash TEXT NOT NULL,         -- SHA-256 of financial baseline at series creation
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- forecast_runs_v1: Model executions
CREATE TABLE forecast_runs_v1 (
  run_id         TEXT PRIMARY KEY,      -- UUID
  series_id      TEXT REFERENCES forecast_series_v1(series_id),
  model          TEXT NOT NULL,         -- 'TimesFM-200M', 'LAST_VALUE', 'MOVING_AVG_4W', 'SEASONAL_NAIVE'
  model_version  TEXT NOT NULL,
  data_cutoff    DATE NOT NULL,         -- Last training date (NO future leakage)
  horizon        INTEGER NOT NULL,      -- Forecast horizon in periods
  hyperparams    TEXT,                  -- JSON
  status         TEXT NOT NULL,         -- RUNNING, COMPLETED, FAILED
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- forecast_predictions_v1: Point + quantile forecasts
CREATE TABLE forecast_predictions_v1 (
  prediction_id  TEXT PRIMARY KEY,
  run_id         TEXT REFERENCES forecast_runs_v1(run_id),
  target_date    DATE NOT NULL,
  point_estimate DOUBLE NOT NULL,
  q10            DOUBLE,
  q50            DOUBLE,
  q90            DOUBLE,
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- forecast_evaluations_v1: Backtest results (temporal split, no leakage)
CREATE TABLE forecast_evaluations_v1 (
  eval_id        TEXT PRIMARY KEY,
  series_id      TEXT REFERENCES forecast_series_v1(series_id),
  model          TEXT NOT NULL,
  model_version  TEXT NOT NULL,
  train_end      DATE NOT NULL,
  test_start     DATE NOT NULL,
  test_end       DATE NOT NULL,
  mae            DOUBLE,
  rmse           DOUBLE,
  mape           DOUBLE,
  coverage_q10_q90 DOUBLE,             -- % actuals within [q10, q90]
  baseline_mae   DOUBLE,                -- vs LAST_VALUE / MOVING_AVG / SEASONAL
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### TimesFM Isolation Rules (Enforced by this Skill)

| Rule | Enforcement |
|------|-------------|
| Never writes to `data/db/meli_financial_v4.db` | Separate DuckDB file; no shared connection |
| Never modifies `marketplace_ledger_v1` | No INSERT/UPDATE/DELETE on ledger tables |
| Never modifies classifications | Read-only access to `marketplace_ledger_clasificado_v1` |
| Never modifies closings | Read-only access to `marketplace_cierre_financiero_v1` |
| Never certifies reconciliations | Forecasts are **predictions**, not evidence |
| Never feeds Copilot as financial fact | Copilot queries `EvidenceOrchestrator` → `FinancialEngine` only |
| Always presented as **pronóstico** | UI label: "Pronóstico (TimesFM vX.Y) — no certificado" |
| Backtesting = temporal split only | `train_end < test_start` enforced in evaluation script |

### Phase 2 — Runtime Truth Prerequisites (Before TimesFM Pilot)

1. Identify certified historical series per MP/metric/SKU/granularity
2. Measure temporal coverage & quality (gaps, outliers, seasonality)
3. Define forecast contract (horizon, frequency, metrics)
4. Build local zero-cost experiment (Ollama + TimesFM or statistical baselines)
5. Backtest: TimesFM vs LAST_VALUE vs MOVING_AVG_4W vs SEASONAL_NAIVE
6. Only if TimesFM beats best baseline **consistently** → consider integration

---

## Validation: OpenCode Discovers & Loads fde-marketplace

Run this verification:

```bash
# 1. Skill directory exists
ls -la .claude/skills/fde-marketplace/

# 2. SKILL.md readable
head -50 .claude/skills/fde-marketplace/SKILL.md

# 3. Prompts accessible
ls .claude/skills/fde-marketplace/prompts/

# 4. Templates accessible
ls .claude/skills/fde-marketplace/templates/

# 5. References present
ls .claude/skills/fde-marketplace/references/
```

**Expected:** All directories exist, files readable, no import errors.

---

## Attribution & License

This skill adapts **FDE Consultants Protocoles** (commit `072f005e701b671d1e03a26dae2848e9b492fc32`) by **selectess**, licensed **Apache-2.0**.

- Source: https://github.com/selectess/fde-consultants-protocoles
- Original License: Apache-2.0 (skill/), MIT (modex/ core), BSL-1.1 (modex/ plugin)
- This adaptation: **Apache-2.0** (see LICENSE file)

**Excluded from this adaptation** (per PAUSA Controlada):
- Modex multi-agent runtime
- Modex Collective (8-agent)
- Frozen Arbiters
- Trust Registry (external)
- MCP Cloud / paid services
- Global installers / config modifications
- `install.sh` execution

---

## Version

**1.0.0-marketplace** — Aligned with:
- FOUNDATION_RESET.md v1.0 (APROBADO)
- MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md v1.0 (PROPUESTO PARA ACTIVACIÓN)
- DEC-019 (EJECUTADO, PASS)
- Phase 16F complete (273/273 tests PASS)
- P40 Phase 2 Evidence Orchestrator deployed
- Phase 1 Automatic Ingestion certified (41/41 tests PASS)
- FASE 1B-R5 Governance certified (59 unique tests, VERIFIED=YES, CERTIFIED=NO)