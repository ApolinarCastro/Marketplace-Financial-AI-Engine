# CIERRE_FINANCIERO_MIGRATION_PLAN

## Read-Only SCOUT — Phase Governance 01 / S2 Survey  
**Date:** 2026-06-22  
**Status:** DRAFT — Not approved for execution

---

## 1. Migration Strategy: Dual-Write → Verify → Cutover

Given the depth and risk of the v1→v2 migration, the recommended strategy is a controlled dual-write pattern over 3 phases.

---

## 2. Phase Breakdown

### Phase M1 — Schema + Dual Write (HIGH RISK — ~4h)
**Goal:** Create v2 table, write to both v1 and v2, verify parity.

**Steps:**
1. [ ] Define `marketplace_cierre_financiero_v2` schema (see V2_SCHEMA.md)
2. [ ] Register v2 in `database.py` auto-create
3. [ ] Modify `MarketplaceAuditorEngine.run_financial_closing()`:
   - After writing to v1, compute and write to v2 (SIGNAL + ALL modes)
   - Use existing `marketplace_ledger_v1` classification + taxonomy filtering
4. [ ] Add snapshot before first dual-write
5. [ ] Execute `run_financial_closing()` for all MPs/periods
6. [ ] Verify: v2 ALL = v1 resultado_neto (Δ=0 per period per MP)
7. [ ] Verify: v2 SIGNAL = filtered canonical (documented delta)

**Files modified:**
- `engine/v4/database.py` (schema)
- `engine/v4/marketplace_auditor.py` (write path)
- `knowledge/taxonomy/*.json` (taxonomy loading — already exists)

**Files NOT modified (yet):**
- `api/api.py` — still reads from v1
- All engines — still read from v1

**Exit criteria:** Dual-write verified correct. v2 populated for all periods.

---

### Phase M2 — API Cutover (HIGH RISK — ~6h)
**Goal:** Replace v1 reads with v2 reads, parameterized by signal_mode.

**Steps:**
1. [ ] Modify `_resolve_period_range()` to query v2 instead of v1
2. [ ] Modify `/api/v4/exec/summary` to query v2 (with signal_mode='ALL' first, then signal_mode='SIGNAL')
3. [ ] Modify `/api/v4/periodos` to query v2
4. [ ] Modify `/api/v4/exec/ux12_summary` to query v2
5. [ ] Update `FinancialEngine.query_exec_summary()` YTD resolution
6. [ ] Update `ReconciliationEngine._level_1_internal()` to compare clasificado vs v2
7. [ ] Update `ReconciliationEngine._level_2_operational()` to compare op_pnl vs v2
8. [ ] Update `ExplainabilityEngine._compute_kpi('resultado_neto')` to query v2
9. [ ] Update `ScorecardEngine` to query v2
10. [ ] Add `signal_mode` parameter to relevant API endpoints

**Files modified:**
- `api/api.py` (6 endpoints)
- `engine/v4/domain/financial_engine.py` (YTD resolution)
- `engine/v4/reconciliation/reconciliation_engine.py` (2 level methods)
- `engine/v4/explainability/explainability_engine.py` (KPI compute)
- `engine/v4/scorecard/scorecard_engine.py` (score query)
- `tests/test_reconciliation_engine.py` (may need tolerance updates)

**Testing (CRITICAL):**
- All 273 tests must pass WITH v2
- Certification gate must be updated (v2 references)
- Snapshot before + revert path if tests fail

**Exit criteria:** All API endpoints + engines read from v2. 273 tests pass. Frontend matches.

---

### Phase M3 — v1 Deprecation (MEDIUM RISK — ~2h)
**Goal:** Stop writing to v1, mark as legacy, update documentation.

**Steps:**
1. [ ] Remove v1 write from `MarketplaceAuditorEngine.run_financial_closing()`
2. [ ] Add v1→v2 cross-check in certification gate (v1 ALL = v2 ALL Δ=0)
3. [ ] Update Governance docs (CLAUDE.md, certification reports)
4. [ ] Re-run all certifications
5. [ ] Add `_legacy` suffix to v1 references in documentation

**Files modified:**
- `engine/v4/marketplace_auditor.py` (remove v1 write)
- `tests/test_closing.py` (update dry-run check to v2)
- Governance docs

**Exit criteria:** v1 no longer written, all consumers use v2. v1 exists for rollback only.

---

## 3. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-----------|--------|------------|
| Certification contracts invalidated | HIGH | CRITICAL | Re-run all certifications; update contract values |
| Frontend shows different values | HIGH | HIGH | Signal_mode=ALL during M2; SIGNAL in separate release |
| Reconciliation engine fails | MEDIUM | HIGH | Update tolerances; verify new deltas are correct |
| 273 tests fail | MEDIUM | HIGH | Pre-snapshot; iterate on v2 values |
| v2 experimental table conflicts | LOW | MEDIUM | Drop experimental `cierre_financiero_v2` before creating official one |
| DEC-019 not properly reflected | MEDIUM | HIGH | Verify `op_pnl=1` filter applied identically in v2 |
| Period boundary changes | LOW | MEDIUM | v2 MAX(periodo_inicio) from SIGNAL mode may differ from v1 if SIGNAL periods are subset |

---

## 4. Rollback Plan

**If M1 fails:**
1. Restore from pre-M1 snapshot
2. Drop `marketplace_cierre_financiero_v2` table
3. Revert `database.py` and `marketplace_auditor.py`

**If M2 fails:**
1. Restore from pre-M2 snapshot
2. Revert all engine/API changes
3. Continue with v1-only reads; v2 writes continue

**If M3 fails:**
1. Re-enable v1 writes
2. Revert marketplace_auditor.py
3. v1 and v2 coexist indefinitely

---

## 5. Total Estimated Effort

| Phase | Hours | Risk | Dependencies |
|-------|-------|------|-------------|
| M1 — Schema + Dual Write | 4h | HIGH | Taxonomy files, closing engine |
| M2 — API Cutover | 6h | HIGH | M1 completed |
| M3 — v1 Deprecation | 2h | MEDIUM | M2 completed + 7 days burn-in |
| **Total** | **12h** | **HIGH** | |

**Recommendation:** Do NOT proceed with S2 until S3 (Executive Visibility) and S4 (Marketplace Governance) are complete. The API cutover alone will destabilize all existing certifications.
