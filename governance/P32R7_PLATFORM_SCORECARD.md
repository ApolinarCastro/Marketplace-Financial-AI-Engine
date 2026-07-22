# P32R7 — Platform Scorecard

**Date:** 2026-07-07
**Scope:** Unified scorecard across all 7 audit dimensions

## Dimension Scores (0-100)

### 1. Regression Integrity: 50/100
| Criterion | Score | Details |
|-----------|-------|---------|
| Test pass rate | 60 | 265/278 (95.3%), was 268/278 |
| New regressions | 20 | 1 real regression (map_detalle_to_concept) |
| Environment stability | 70 | 4 tests blocked by DB lock |

### 2. Backend Health: 65/100
| Criterion | Score | Details |
|-----------|-------|---------|
| API availability | 60 | 1/11 endpoints crashes |
| Response time | 80 | Sub-100ms avg for tested endpoints |
| Memory efficiency | 70 | No leaks, modules loaded reasonably |

### 3. Frontend Health: 70/100
| Criterion | Score | Details |
|-----------|-------|---------|
| API contract compliance | 80 | All referenced endpoints exist |
| Zero frontend logic | 90 | No client-side financial calculations |
| No orphan endpoints | 60 | Some legacy references present |

### 4. End-to-End Traceability: 55/100
| Criterion | Score | Details |
|-----------|-------|---------|
| Ledger→Clasificado | 100 | $0 delta, perfect |
| Ledger→Cierre | 30 | $2.07B gap |
| RAW→Ledger | 60 | XMLs on disk not traced to ledger |
| Auditoria cross-ref | 30 | Schema mismatch prevents join |

### 5. Single Financial Truth: 30/100
| Criterion | Score | Details |
|-----------|-------|---------|
| Ledger==Clasificado | 100 | $0 delta ✅ |
| Ledger==Cierre | 0 | 4/4 MPs fail |
| Unclassified rows | 50 | 14,560 rows (3.6%) |

### 6. Traceability Consumption: 60/100
| Criterion | Score | Details |
|-----------|-------|---------|
| DTE Coverage display | 80 | 3/4 MPs covered |
| Executive Intelligence | 0 | Table does not exist |
| Audit display | 70 | 2/4 MPs covered |

### 7. Contract Matrices: 75/100
| Criterion | Score | Details |
|-----------|-------|---------|
| Endpoint existence | 90 | All referenced endpoints exist |
| Response shape match | 70 | Not fully verified due to crashes |
| Documentation alignment | 65 | Desglose table docs incorrect |

## Overall Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Regression | 20% | 50 | 10.0 |
| Backend Health | 15% | 65 | 9.75 |
| Frontend Health | 15% | 70 | 10.5 |
| Traceability | 15% | 55 | 8.25 |
| Single Financial Truth | 20% | 30 | 6.0 |
| Traceability Consumption | 5% | 60 | 3.0 |
| Contract Matrices | 10% | 75 | 7.5 |
| **TOTAL** | **100%** | — | **55.0/100** |

## Risk Heatmap

| Risk | Level | Impact | Likelihood |
|------|-------|--------|------------|
| RIPLEY data misrepresentation | 🔴 HIGH | Financial statements incorrect | HIGH ($1.78B gap) |
| Concept mapping broken | 🟠 MEDIUM | Cobros breakdown degraded | HIGH (test fails) |
| Summary endpoint crash | 🟠 MEDIUM | Executive dashboard broken | ALWAYS (ALL MP) |
| Executive Intelligence missing | 🟡 LOW | UX12 not functional | CERTAIN |
| FALABELLA cierre overstatement | 🟠 MEDIUM | $6M false surplus | KNOWN |

## Recommendation

**DO NOT DEPLOY to production.** Score 55/100 is below the 70/100 threshold. Three blocking issues:
1. Single Financial Truth broken ($2.07B gap)
2. Regression in concept mapping
3. Summary endpoint crashes for ALL marketplace
