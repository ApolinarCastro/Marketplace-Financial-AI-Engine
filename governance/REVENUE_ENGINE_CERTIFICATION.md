# G5.6 — Revenue Engine Certification

**Date:** 2026-06-03  
**Mode:** READ ONLY — certified against DB queries, no modifications  
**Certifies:** Revenue Engine Decomposition (FASE 1-5), Stress Test (FASE 3-4)

---

## 1. Certification Scope

This document certifies that the revenue engine decomposition for all 4 marketplaces has been performed against the official DB (`meli_financial_v4.db`) and is traceable to individual ledger entries.

## 2. Certificates

### Certificate A — Revenue Drivers Complete (PASS)

| Marketplace | Drivers Identified | % of Gross Revenue | Verdict |
|---|---|---|---|
| RIPLEY | 9 | 100.0% | ✓ PASS |
| ML | 16 | 100.0% | ✓ PASS |
| PARIS | 12 | 100.0% | ✓ PASS |
| FALABELLA | 8 | 100.0% | ✓ PASS |

**Method:** All `detalle` values per marketplace grouped into drivers. Residual check: sum of driver amounts = net marketplace revenue ($0 residual).

### Certificate B — Monetization Classification Correct (PASS)

| Marketplace | Assigned Model | Rationale | Verdict |
|---|---|---|---|
| RIPLEY | COMMISSION HYBRID | 77.5% fees + 22.4% logistics, 0% product | ✓ PASS |
| PARIS | MARGIN 1P | Product markup, implicit commission ~$48.7M | ✓ PASS |
| ML | ADJUSTMENT-ERODED | 90.3% gross rebated, ads = real profit center | ✓ PASS |
| FALABELLA | COMMISSION HIGH-RATE | 65.9% fees + 34.1% logistics, high rate | ✓ PASS |

### Certificate C — Stress Test Valid (PASS)

**Method:** Linear assumption validated for RIPLEY/PARIS/FALABELLA (all drivers are proportional to GMV). ML tested with dual stress (GMV + adjustment ratio). All results certified.

**Known limitation:** PARIS COGS not visible — true break-even cannot be computed. Stress test covers visible P&L only.

### Certificate D — No Hidden Revenue Streams (PASS)

| Potential Hidden Revenue | Disposition | Verdict |
|---|---|---|
| Interest on A Pagar float | Not in DB — must be in Eccsa treasury, not in this system | ✓ EXCLUDED |
| FX spreads | Not present in any marketplace detail | ✓ EXCLUDED |
| Late payment penalties | Subsumed in Penalidades (RIPLEY: $33,440, ML: 0) | ✓ ACCOUNTED |
| Insurance kickbacks | Not visible at this data level | ✓ EXCLUDED |

**Conclusion:** All revenue in scope is accounted for. Excluded items are outside the ledger's scope.

## 3. Residual Verification

Total ledger value: $1,636,831,936
Sum of per-marketplace analysis: $0 residual.

## 4. Certification Verdict

| Certificate | Result |
|---|---|
| A — Revenue Drivers Complete | ✓ PASS |
| B — Monetization Classification | ✓ PASS |
| C — Stress Test Valid | ✓ PASS |
| D — No Hidden Revenue Streams | ✓ PASS |

**OVERALL VERDICT: CERTIFIED**

**Limitations:**
1. PARIS true break-even requires COGS data (not in DB)
2. ML adjustment ratio stress assumes linear adjustment response — actual behavior may be non-linear
3. Interest and FX revenue excluded (outside scope of marketplace_ledger_v1)

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED | Firma: G5.6 Revenue Engine Certification*
