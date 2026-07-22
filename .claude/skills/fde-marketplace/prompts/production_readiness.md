# Production Readiness Checklist

**Required for Phase 9 (Production) gate. All items must PASS.**

---

## 1. RC1 Integrity (Non-Negotiable)

- [ ] `engine/rc1/` unmodified since BASELINE_V6 (SHA256: `e1e341ef`)
- [ ] No direct imports from `engine/rc1/` in new code
- [ ] RC1 public contracts only: `FinancialEngine`, `LedgerEngine`, `ReconciliationEngine`, `CertificationEngine`
- [ ] DEC-019 flag `include_in_operational_pnl` respected in all queries

## 2. Test Suite Health

- [ ] Full regression: **273+/273+ PASS, 0 new regressions**
- [ ] Certification Gate: **27/27 PASS** (`test_certification_gate.py`)
- [ ] FASE 1B Governance: **VERIFIED=YES** (59 unique tests, 105 aggregate)
- [ ] Copilot: **309/309 PASS** (19 page + 104 ask + 10 execute + 110 golden + 66 benchmark)
- [ ] Ingestion: **41/41 PASS**
- [ ] Evidence Orchestrator: **252/252 PASS**
- [ ] No flaky tests (3 consecutive clean runs)

## 3. Financial Truth Invariants

- [ ] **Single Financial Truth**: Ledger vs Cierre 69/69 periods $0 delta (Ingresos/Devoluciones)
- [ ] **DEC-019**: PosCobro paired (3,663 rows, $94.4M) excluded from operational P&L
- [ ] **Signal/Noise**: Taxonomy v1 active (RIPLEY 12/20, ML 70/1, PARIS 14/1, FALABELLA 15/1)
- [ ] **Case-insensitive SQL**: `LOWER(marketplace)`, `LOWER(financial_group)` in all 5 critical queries (DEC-035)
- [ ] **Period bug fixed**: `end=None` → open-ended (DEC-029/OBS-02 resolved)
- [ ] **Commission deduplication**: 0 shared transaction_ids (DEC-031)
- [ ] **Transaction exclusivity**: 0 cross-SIGNAL overlaps (DEC-032)

## 4. Data Freshness & Coverage

- [ ] Junio 2026 data ingested for all 4 MPs (or documented gap with Owner approval)
- [ ] PARIS/FALABELLA not >30 days stale (currently: FAIL - last Apr 2026)
- [ ] `file_registry` table populated (currently EMPTY - must be fixed)
- [ ] DTE coverage: PARIS 62 XMLs, FALABELLA 6 XMLs indexed (0 matched - heuristic limit documented)

## 5. Audit Trail Coverage

- [ ] ML audit rows > 0 (currently 0/22,401 — must be resolved)
- [ ] Ripley `cargo_sin_respaldo_legal`: 12,822 false positives structurally excluded (Phase 16F)
- [ ] FALABELLA $12K `movimientos_no_clasificados` documented & Owner-accepted
- [ ] Evidence chain: RAW → Registry → ETL → Ledger → Classification → Cierre → XML → Settlement → Bank → Dashboard

## 6. API Contract Stability

- [ ] Public contracts unchanged (FinancialEngine, LedgerEngine, ReconciliationEngine, CertificationEngine, EvidenceOrchestrator)
- [ ] New endpoints versioned under `/api/v4/`
- [ ] Backward compatibility: RFC-040R1 params (`folio_xml`, `archivo_origen`) optional
- [ ] No breaking changes to `/api/v4/exec/*`, `/api/v4/evidence/*`, `/api/v4/financial-structure`

## 7. Security & Performance

- [ ] Authentication on all endpoints (Sprint B1.1)
- [ ] Rate limiting active
- [ ] SQL injection prevention (parameterized queries only)
- [ ] HTTPS enforced in production config
- [ ] Dashboard authentication
- [ ] P95 latency < 500ms for `/api/v4/financial-structure`
- [ ] P95 latency < 200ms for `/api/v4/exec/summary`
- [ ] Memory < 512MB under load

## 8. Backup & Disaster Recovery

- [ ] Automated DB backup (DuckDB file copy + SHA256 manifest)
- [ ] Restore tested within last 30 days
- [ ] 19 snapshots available in `data/db/snapshot_*/`
- [ ] RPO < 1 hour, RTO < 4 hours documented

## 9. Secrets & Permissions

- [ ] No secrets in code (API keys, DB passwords)
- [ ] `.env` in `.gitignore`
- [ ] Production uses separate `.env.production`
- [ ] File permissions: DB read/write only for app user

## 10. Monitoring & Observability

- [ ] `/api/v4/health/financial` returns health score 0-100
- [ ] `/api/v4/health/metrics` returns 10 mandatory metrics
- [ ] Financial alerts engine active (Phase 7)
- [ ] Copilot query latency logged (benchmark median < 50ms)

## 11. Operational Runbooks

- [ ] Ingestion runbook: `docs/runbooks/ingestion.md`
- [ ] Classification runbook: `docs/runbooks/classification.md`
- [ ] Closing runbook: `docs/runbooks/closing.md`
- [ ] Audit runbook: `docs/runbooks/audit.md`
- [ ] Rollback runbook: `docs/runbooks/rollback.md`

## 12. Owner Sign-Off

- [ ] Apolinar Castro reviewed Phase 9 deliverables
- [ ] Priority questions certified (Copilot G1-G11 + new)
- [ ] Go/No-Go decision recorded in `governance/PHASE_9_GO_DECISION.md`

---

## Gate Verdict

| Category | Status |
|----------|--------|
| RC1 Integrity | ☐ PASS / ☐ FAIL |
| Test Suite | ☐ PASS / ☐ FAIL |
| Financial Truth | ☐ PASS / ☐ FAIL |
| Data Freshness | ☐ PASS / ☐ FAIL |
| Audit Trail | ☐ PASS / ☐ FAIL |
| API Contracts | ☐ PASS / ☐ FAIL |
| Security/Perf | ☐ PASS / ☐ FAIL |
| Backup/DR | ☐ PASS / ☐ FAIL |
| Secrets/Perms | ☐ PASS / ☐ FAIL |
| Monitoring | ☐ PASS / ☐ FAIL |
| Runbooks | ☐ PASS / ☐ FAIL |
| Owner Sign-Off | ☐ PASS / ☐ FAIL |

**Overall:** `GO` / `NO-GO` / `CONDITIONAL_GO`

**Conditions (if CONDITIONAL_GO):**

---

**Codex Signature:** ________________ **Date:** ________________

**Owner Signature:** ________________ **Date:** ________________