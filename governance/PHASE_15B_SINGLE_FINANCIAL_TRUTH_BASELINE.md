# Phase 15B — Single Financial Truth Baseline

**Date**: 2026-06-18
**Status**: CERTIFIED
**Tests**: 261/261 PASS (incl. 27 certification gate)
**Taxonomies**: 4/4 MPs covered (ripley_v1, ml_v1, paris_v1, falabella_v1)

## Immutable Truths

### Financial Structure ↔ Ledger Equivalence
| MP | FS Total = Ledger SUM | Cert |
|---|---|---|
| ML | $0 delta | ✅ |
| PARIS | $0 delta | ✅ |
| RIPLEY | $0 delta | ✅ |
| FALABELLA | $0 delta | ✅ |

### Waterfall Conservation (ing + dev + cob + rec = disp)
| MP | Conservation | Cert |
|---|---|---|
| ALL | $0 delta | ✅ |
| ML | $0 delta | ✅ |
| PARIS | $0 delta | ✅ |
| RIPLEY | $0 delta | ✅ |
| FALABELLA | $0 delta | ✅ |

### Exec Summary = Waterfall (net_profit = disponible)
| MP | Exec = Waterfall | Cert |
|---|---|---|
| ML | $0 delta | ✅ |
| PARIS | $0 delta | ✅ |
| RIPLEY | $0 delta | ✅ |
| FALABELLA | $0 delta | ✅ |

### Taxonomy Coverage
| MP | Detalles | Orphans | Groups Covered | Cert |
|---|---|---|---|---|
| ML | 71 | 0 | 7/7 | ✅ |
| PARIS | 15 | 0 | 4/4 | ✅ |
| RIPLEY | 32 | 0 | 6/6 | ✅ |
| FALABELLA | 16 | 0 | 5/5 | ✅ |

### DTE Coverage
| MP | Coverage | Cert |
|---|---|---|
| ML | ≥50% | ✅ |
| RIPLEY | ≥95% | ✅ |
| PARIS | 0% (known — XLSX source for folio_xml) | ⚠️ |
| FALABELLA | 0% (known — no XML source) | ⚠️ |

### API Contract (14/14 regression)
- INSERT/UPDATE/DELETE blocked on core tables
- No heuristics in endpoint responses
- No financial calculations in frontend
- All endpoints return certified data

## Phase 15B Artifacts
| File | Type |
|---|---|
| `knowledge/taxonomy/ml_v1.json` | ML taxonomy (71 detalles) |
| `knowledge/taxonomy/paris_v1.json` | PARIS taxonomy (15 detalles) |
| `knowledge/taxonomy/falabella_v1.json` | FALABELLA taxonomy (16 detalles) |
| `tests/test_certification_gate.py` | 27 automated gate tests |
| `governance/PHASE_15B_DTE_RECOVERY_CERTIFICATION.md` | DTE recovery cert |
| `governance/PHASE_15B_SIGNAL_TAXONOMY_CERTIFICATION.md` | Taxonomy cert |
| `governance/PHASE_15B_AUTOMATED_CERTIFICATION_GATE.md` | Gate cert |
| `governance/PHASE_15B_SINGLE_FINANCIAL_TRUTH_BASELINE.md` | This file |
| `governance/PHASE_15B_FINAL_AUDIT_READINESS_CERTIFICATION.md` | Final cert |

## Known Limitations
1. **PARIS/FALABELLA DTE coverage 0%** — DTEIndexer generó 68 records en `dte_truth_v1` pero XMLMatcher heuristic (monto+fecha ±7d) no vinculó al ledger. Se requiere matcher por order_id.
2. **RIPLEY/ML waterfall vs cierre delta** — RIPLEY ~$386M y ML ~$60M de diferencia entre waterfall (FINANCIAL_STRUCTURE) y cierre (CIERRE_FINANCIERO_V1). Es estructural: cierre fue calculado pre-Phase 13 (SIGNAL taxonomy) y pre-DEC-019.
3. **Dashboard rebuild pending** — Executive Dashboard still uses `/api/v4/exec/summary` + `/api/v4/exec/waterfall`. Future state: single `/api/v4/financial-structure` source.
4. **Data freshness** — No Junio 2026 data incorporated for any MP. PARIS/FALABELLA end Apr 2026.
