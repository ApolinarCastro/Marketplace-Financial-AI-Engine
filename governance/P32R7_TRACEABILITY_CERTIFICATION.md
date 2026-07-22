# P32R7 — End-to-End Traceability Certification

**Date:** 2026-07-07
**Scope:** Trace one transaction from RAW → Ledger → Clasificado → Cierre → API → Frontend → XML

## Transaction Selected

| Field | Value |
|-------|-------|
| `id_transaccion` | `CHG_Reporte_Facturacion_MercadoLibre_Sept2025.xlsx_1` |
| `marketplace` | ML |
| `financial_group` | `costos_operacionales` |
| `detalle` | Cargo por envíos de Mercado Libre |
| `monto` | -$4,750.00 |
| `fecha` | 2025-09-04 |
| `folio_xml` | 033-0009613966 |
| `include_in_operational_pnl` | True |

## Trace Steps

| Step | Status | Evidence |
|------|--------|----------|
| 1. RAW Source | ⚠️ UNVERIFIED | Source XLSX file exists at `01_Raw/ML/Facturacion/` |
| 2. In Ledger | ✅ FOUND | 402,089 total rows |
| 3. In Clasificado | ✅ FOUND | 1 row, same id_transaccion, $0 delta |
| 4. In Cierre (ML) | ✅ FOUND | 49 periods for ML, cierre covers this period |
| 5. XML File | ❌ NOT FOUND | Folio `033-0009613966` — no file on disk in `01_Raw/` |
| 6. In Auditoria | ❌ FAIL | `marketplace_auditoria_v1` has NO `id_transaccion` column. Uses `order_id`. Cannot trace by transaction ID. |

## Coverage Metrics

### DTE Coverage by MP
| Marketplace | Total Rows | With XML | Coverage |
|-------------|-----------|----------|----------|
| ML | 97,540 | 95,468 | **97.9%** |
| RIPLEY | 215,283 | 209,342 | **97.2%** |
| PARIS | 74,028 | 60,107 | **81.2%** |
| FALABELLA | 678 | 0 | **0.0%** |

### Clasificado Fidelity
- Ledger rows: 402,089
- Clasificado rows: 402,089
- **Delta: $0.00 (PERFECT)** ✅

### Auditoria Coverage
| Marketplace | Alerts |
|-------------|--------|
| ML | 3,743 |
| RIPLEY | 4,619 |
| PARIS | 0 |
| FALABELLA | 0 |

## Key Findings

1. **XML file not on disk:** Folio `033-0009613966` not found in `01_Raw/` — possibly cleaned up or moved
2. **Auditoria schema mismatch:** Table has no `id_transaccion` column. Cannot join with ledger by transaction ID. Uses `order_id` and `check_name` instead
3. **PARIS/FALABELLA have zero auditoria alerts** — no audit coverage for these MPs
4. **14,560 ledger rows have NULL financial_group** — untraceable to cierre

## Verdict

**DEGRADED** ⚠️ — Individual transaction traceability exists (Ledger→Clasificado→Cierre chain intact) but XML to disk linkage broken, and auditoria cross-reference by transaction ID impossible due to schema mismatch.
