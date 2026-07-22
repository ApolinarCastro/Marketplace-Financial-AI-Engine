# RISK_ASSESSMENT.md

## S2 (Canonical Close) — Phase Governance 01  
**Date:** 2026-06-22  
**Status:** READ ONLY — SCOUT Survey Complete

---

## 1. Overall Risk Rating: **CRITICAL** ⚠️

S2 has the highest risk profile of any remaining phase in Governance 01. The `cierre_financiero_v1` table is the most-referenced financial table in the system (36+ references across 12 files).

---

## 2. Risk Categories

### Risk A — Certification Invalidation (CERTAIN)
**Severity:** CRITICAL  
**Probability:** 100%  

Switching from v1 to v2 (even ALL mode) WILL change financial values because:
- `cierre_financiero_v1` uses formula: `ingresos + costos_operacionales + costos_comerciales + ajustes`  
  Note: **devoluciones are NOT a separate column** — they're embedded in `total_ajustes`
- v2 separates devoluciones explicitly
- v2 applies SIGNAL taxonomy (excludes NOISE rows)

**Impact:** ALL existing certifications invalidated. All governance documents referencing v1 values become stale.

### Risk B — Reconciliation Engine Breakage (HIGH)
**Severity:** HIGH  
**Probability:** 90%  

The `ReconciliationEngine` has 60 tests. Levels 1 (INTERNA) and 2 (OPERACIONAL) directly compare `clasificado` sums against `v1.resultado_neto`. Switching to v2 will:
- Change target totals for delta calculation
- Generate new alerts for previously PASSING periods
- Potentially reclassify certification status from CERTIFIED to PARCIAL

### Risk C — Frontend Value Shifts (HIGH)
**Severity:** HIGH  
**Probability:** 80%  

The `/api/v4/exec/summary` endpoint reads `resultado_neto` from v1. Switching to v2 changes ALL KPI card values. Even with `signal_mode=ALL`, devoluciones separation may cause small deltas. With `signal_mode=SIGNAL`, RIPLEY neto increases ~$236M.

**Without a coordinated frontend release, users will see different numbers with no explanation.**

### Risk D — Period Boundary Changes (MEDIUM)
**Severity:** MEDIUM  
**Probability:** 40%  

5 locations use `MAX(periodo_inicio) FROM v1 WHERE resultado_neto != 0` for YTD resolution. If v2 SIGNAL mode produces a different latest period than v1, YTD calculations shift.

### Risk E — Taxonomy Inconsistency (MEDIUM)
**Severity:** MEDIUM  
**Probability:** 30%  

The SIGNAL taxonomy was designed for RIPLEY only. ML, PARIS, and FALABELLA taxonomies have very few NOISE entries (1 each). The SIGNAL benefit is concentrated in RIPLEY. Applying SIGNAL universally has uneven impact:

| MP | SIGNAL coverage | Neto change | Justification |
|----|----------------|-------------|---------------|
| ML | 70/71 (98.6%) | +$0.5M | Minimal — 1 NOISE detail |
| PARIS | 14/15 (93.3%) | -$50M | 1 NOISE (Despacho=$0) |
| RIPLEY | 12/32 (37.5%) | +$236.5M | Major — 20 NOISE details excluded |
| FALABELLA | 15/16 (93.8%) | -$7M | Marginal |

### Risk F — Experimental v2 Table Collision (LOW)
**Severity:** LOW  
**Probability:** 100% (table exists)  

`cierre_financiero_v2` already exists in the database from Phase 16 experiments. Before creating the official v2, this table must be dropped or renamed. It has the wrong name and queries raw (not classified) ledger.

---

## 3. Dependency Heat Map

| Layer | Dependency Count | Avg Impact | Avg Risk | Recommendation |
|-------|-----------------|-----------|---------|---------------|
| **API endpoints** | 6 | HIGH | HIGH | Cut over last |
| **Engines** | 6 | HIGH | HIGH | Cut over carefully |
| **Tests** | 4 files (77 tests) | HIGH | HIGH | Update tolerances |
| **DB schema** | 1 | HIGH | LOW | Drop experiment first |
| **Governance docs** | 50+ | LOW | LOW | Update after code |
| **Temp/legacy files** | 19 | LOW | LOW | Can ignore |

---

## 4. Decision: EXECUTE S2, POSTPONE, OR CANCEL

### Option A — Execute S2 Now (NOT RECOMMENDED)
**Risk:** CRITICAL  
**Effort:** 12 hours  
**Justification:** The governance master plan scheduled S2 for a reason — the cierre table must eventually reflect SIGNAL taxonomy. However, the SCOUT reveals that the dependency depth (36+ references) and certification invalidation (100% probability) make this the wrong time.

### Option B — Postpone S2 After S3+S4 (RECOMMENDED ⭐)
**Risk:** MEDIUM (with prep)  
**Effort:** 0 hours now; 2h prep + 12h later  
**Justification:** 
1. The presentation layer (S1) is now fixed — backend controls all render data
2. S3 (Executive Visibility) surfaces orphan engines — zero cierre risk
3. S4 (Marketplace Governance) focuses on RIPLEY/SHOPIFY/ FALABELLA — minimal cierre risk
4. After S3+S4, the system has full visibility. THEN cut over to v2 with confidence
5. Additional burn-in time allows taxonomy refinement

**Prep work during S3/S4:**
- Create a `V2_COMPLIANCE_CHECK` script (read-only) that periodically compares v1 against a simulated v2 for drift detection
- Add S2 to the certification gate as NON-BLOCKING warning
- Document the expected v1→v2 delta per MP per period

### Option C — Cancel S2 (NOT RECOMMENDED)
**Risk:** HIGH (technical debt)  
**Justification:** The SIGNAL taxonomy is a certified truth. Not incorporating it into the canonical close means the system has two competing truths (v1 ALL-mode vs SIGNAL-filtered). This is acceptable short-term but unsustainable.

---

## 5. Recommendation

**POSTPONE S2.** Focus on S3 (Executive Visibility) and S4 (Marketplace Governance) first. The cierre table is working correctly for current needs. The SIGNAL taxonomy is already applied at the `financial-structure` endpoint (which is the primary data source for both dashboards post-S1). The v1 table only serves:
- Period boundary resolution (easily replaced)
- Reconciliation engine target (internal, not user-facing)
- Explainability engine reference (documents, not live values)
- Legacy `/api/v4/exec/summary` endpoint (kept for backward compat)

None of these are blocking deployment or user trust. S2 can wait.

### Go/No-Go Criteria for Future S2

Only proceed with S2 when:
1. [ ] S3 and S4 are both deployed and passing certification gate
2. [ ] `V2_COMPLIANCE_CHECK` has run for 7+ days with zero unexpected drift
3. [ ] All 273 tests pass with v2 values (tolerances updated)
4. [ ] Frontend has been tested with v2 SIGNAL values in staging
5. [ ] Governance docs updated with new v2 contract values
6. [ ] Executive approval obtained for certification value changes
