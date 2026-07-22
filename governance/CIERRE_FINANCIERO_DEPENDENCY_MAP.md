# CIERRE_FINANCIERO_DEPENDENCY_MAP

## Read-Only SCOUT — Phase Governance 01 / S2 Survey
**Date:** 2026-06-22  
**Status:** READ ONLY — No modifications made

---

## 1. Summary

| Metric | Count |
|--------|-------|
| Unique files referencing `cierre_financiero_v1` | 12 production + 19 temp/legacy |
| API endpoints (production) | 6 distinct (9 SQL usages) |
| Engines (production) | 6 (Financial, Certification, Reconciliation, Explainability, Scorecard, Closing) |
| Tests referencing v1 | 4 test files (~77 indirect tests) |
| DB write paths | 1 (MarketplaceAuditorEngine.run_financial_closing) |
| DB read paths | 12+ (queries for results, period max, group totals) |
| `cierre_financiero_v2` experimental | Already exists in DB (24 periods × 4 MPs) |
| Total rows v1 | 124 rows |
| Total rows v2 | ~96 rows (24 × 4 MPs) |

---

## 2. Complete Reference Inventory

### 2A. API Endpoints (api.py)

| # | Endpoint | Line(s) | Usage | Impact | Risk |
|---|----------|---------|-------|--------|------|
| 1 | `/api/v4/exec/summary` | 498 | `SELECT total_ingresos, cobros, resultado_neto FROM marketplace_cierre_financiero_v1` | HIGH — KPI cards depend on these values | CRITICAL — direct financial values to frontend |
| 2 | `/api/v4/exec/summary` | 508-516 | Devuelve devoluciones from ledger (NOT from v1) | LOW — bypasses v1 | LOW |
| 3 | `/api/v4/exec/summary-v3` | 352 | `SELECT MAX(periodo_inicio) FROM v1 WHERE resultado_neto != 0` | MEDIUM — YTD period resolution | LOW — fallback exists |
| 4 | `/api/v4/exec/ux12_summary` | 1165 | `SELECT MAX(periodo_inicio) FROM v1 WHERE resultado_neto != 0` | MEDIUM — YTD period resolution | LOW — fallback exists |
| 5 | `/api/v4/periodos` | 1022-1027 | `SELECT DISTINCT periodo_inicio FROM v1 WHERE resultado_neto != 0` | MEDIUM — period selector | LOW — fallback to ledger periods |
| 6 | `/api/v4/certify` | 1089 | Via CertificationEngine.certify() → v1 queries | HIGH — certification contract | HIGH — changes certification status |
| 7 | `_resolve_period_range()` | 1001 | `SELECT MAX(periodo_inicio) FROM v1` | MEDIUM — YTD boundary | LOW — can default to 2024-01-01 |
| 8 | `get_financial_structure` (waterfall) | 802-841 | Pre-computed waterfall from ledger (NOT from v1) | NONE — Phase 12C already removed v1 dependency | NONE |
| 9 | `/api/v4/exec/waterfall` (legacy) | 844-882 | Direct ledger query (NOT from v1) | NONE — already decoupled | NONE |

### 2B. Engines

| # | Engine | File:Line | Usage | Impact | Risk |
|---|--------|-----------|---|--------|------|
| 1 | **FinancialEngine.query_exec_summary()** | financial_engine.py:629 | `SELECT MAX(periodo_inicio) FROM v1 WHERE resultado_neto != 0` | MEDIUM — YTD boundary | LOW — fallback to `start` |
| 2 | **CertificationEngine._certify_pnl_equivalence()** | certification_engine.py:206-215 | `SELECT resultado_neto FROM v1` (commented out — uses ledger directly) | NONE — already not using v1 for value | LOW |
| 3 | **ReconciliationEngine._level_1_internal()** | reconciliation_engine.py:253-280 | `SELECT total_ingresos, resultado_neto FROM v1` | HIGH — reconciliation delta calculation | CRITICAL — changes certification status |
| 4 | **ReconciliationEngine._level_2_operational()** | reconciliation_engine.py:377-389 | `SELECT resultado_neto FROM v1` | HIGH — operational delta calculation | CRITICAL — changes certification status |
| 5 | **ExplainabilityEngine._compute_kpi('resultado_neto')** | explainability_engine.py:163 | `SELECT SUM(resultado_neto) FROM v1 WHERE marketplace=?` | MEDIUM — KPI definition for "Disponible" | MEDIUM — affects explainability text |
| 6 | **ScorecardEngine** | scorecard_engine.py:96 | `SELECT SUM(resultado_neto) FROM v1 WHERE marketplace=?` | MEDIUM — scorecard KPIs | MEDIUM |
| 7 | **MarketplaceAuditorEngine.run_financial_closing()** | marketplace_auditor.py:632,668 | DELETEs + INSERTs into v1 | HIGH — ONLY write path to v1 | CRITICAL — data mutation |
| 8 | **ClosingEngine** | closing_engine.py:85-91 | Via CertificationEngine (no direct v1 access) | MEDIUM | MEDIUM |

### 2C. Database Schema

| # | File:Line | Usage | Impact | Risk |
|---|-----------|---|--------|------|
| 1 | database.py:134-135 | `CREATE TABLE IF NOT EXISTS marketplace_cierre_financiero_v1 (...)` | HIGH — schema definition | CRITICAL — creation + migration |
| 2 | **cierre_financiero_v2** (existing) | In DB (experimental) | Already has data from Phase 16 experiment | MEDIUM — exists but not referenced in production code |

### 2D. Tests

| # | Test File | Lines | Usage | Impact | Risk |
|---|-----------|-------|-------|--------|------|
| 1 | test_closing.py | 33, 35 | `SELECT COUNT(*) FROM v1` for dry-run validation | LOW — just count check | LOW |
| 2 | test_certification.py | 11 tests | Indirect via CertificationEngine.certify() | MEDIUM — status may change | MEDIUM |
| 3 | test_certification_gate.py | 27 tests | Gates 1-2 via exec/waterfall (ledger, NOT v1) | LOW — already decoupled | LOW |
| 4 | test_reconciliation_engine.py | 60 tests | Indirect via ReconciliationEngine.validate_marketplace_consistency() | HIGH — delta values change | CRITICAL — tests may fail |
| 5 | test_phase_16_mandatory.py | 145 lines | Indirect via run_financial_closing() which writes to v1 | MEDIUM | MEDIUM |

### 2E. Governance / Documentation Files

| # | File | References | Count |
|---|------|-----------|---|
| 1 | CLAUDE.md | 1 | 1 |
| 2 | governance/*.md files | Throughout | ~50+ references |
| 3 | knowledge/*.md files | 3 | 3 |
| 4 | discovery/*.md files | 3 | 3 |

---

## 3. Usage Pattern Analysis

### Pattern A: Period Boundary (MAX query)
Used to find the latest closed period for YTD calculations.

Files: `api.py:352,1001,1165`, `financial_engine.py:629`

**Replacement:** Query `MAX(periodo_inicio)` from v2 instead of v1, OR fallback to ledger `MAX(fecha)`.

### Pattern B: Certified KPI Values
Used to read `resultado_neto`, `total_ingresos`, etc. as the certified source of truth.

Files: `api.py:498`, `reconciliation_engine.py:260,379`, `explainability_engine.py:163`, `scorecard_engine.py:96`

**Replacement:** Read from v2 (with SIGNAL or ALL mode) instead of v1. Values WILL differ for RIPLEY, PARIS, and ML.

### Pattern C: Period Listing
Used to populate the period selector dropdown.

File: `api.py:1022-1027`

**Replacement:** Query periods from v2 or from ledger.

### Pattern D: Write Target
Only `MarketplaceAuditorEngine.run_financial_closing()` writes to v1.

File: `marketplace_auditor.py:632,668`

**Replacement:** Write to both v1 and v2 during migration, then exclusively v2.

---

## 4. Key Discovery: v1 vs v2 Financial Delta

Comparison of `v1.resultado_neto` vs `v2.resultado_neto` (SIGNAL mode) for matched periods:

| MP | v1 Neto | v2 Signal Neto | Delta | Sign |
|---|---------|---------------|-------|------|
| RIPLEY | $283.4M | $519.9M | **+$236.5M** | SIGNAL exclusion of negative NOISE rows INCREASES neto |
| PARIS | $193.3M | $337.2M | **+$143.9M** | Same pattern — NOISE rows are predominantly negative |
| ML | $582.4M | $583.0M | **+$0.5M** | Minimal — ML taxonomy has 70/71 SIGNAL (1 NOISE) |
| FALABELLA | $7.7M | $7.7M | **$0** | Identical — all rows are SIGNAL |

**Root cause:** v2 SIGNAL mode excludes NOISE rows (classified by taxonomy). Most NOISE rows are negative (devoluciones, costos, ajustes), so excluding them INCREASES the neto. This is the CORRECT financial behavior but creates a BREAK with existing certifications.

**Roadblock:** Switching to v2 SIGNAL mode will invalidate ALL existing certification contracts that use v1 values.

---

## 5. Experimental v2 Table (cierre_financiero_v2)

The Phase 16 experiment left a table `cierre_financiero_v2` in the database with:
- 24 periods per MP (all months with data)
- SIGNAL-filtered aggregates
- Per-period `resultado_neto` and `resultado_neto_full`
- DTE linked row counts

**Issues with experimental v2:**
1. Named `cierre_financiero_v2` (not `marketplace_cierre_financiero_v2`)
2. Queries `marketplace_ledger_v1` (raw) not `marketplace_ledger_clasificado_v1` (classified)
3. No `total_devoluciones` separation in the formula (only in the column)
4. Does not include ML paired mechanism exclusion (DEC-019)
5. Uses `include_in_operational_pnl = 1` filter already in v1
6. Not referenced by any production code
