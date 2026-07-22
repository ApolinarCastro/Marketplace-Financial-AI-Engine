# Phase 15A — DTE Certification

## Summary

Documentary traceability certification for all 4 marketplaces. Verifies `folio_xml` coverage in `marketplace_ledger_v1`.

## DTE Coverage per Marketplace

| Marketplace | Total Rows | With folio_xml | Coverage | Status |
|---|---|---|---|---|
| RIPLEY | 217,315 | 210,232 | **96.7%** | ✅ CERTIFIED |
| ML | 187,455 | 96,098 | **51.3%** | ⚠️ PARTIAL |
| PARIS | 45,756 | 0 | **0.0%** | ❌ FAIL |
| FALABELLA | 2,609 | 0 | **0.0%** | ❌ FAIL |

## Detail

### RIPLEY (96.7% — CERTIFIED)
- 210,232 of 217,315 rows have `folio_xml` populated
- Source: XLSX files ingested during Sprint B2.5C
- 7,083 rows without folio_xml correspond to treasury entries (LIQUIDACION group — expected)

### ML (51.3% — PARTIAL)
- 96,098 of 187,455 rows have `folio_xml` populated
- 91,357 rows without folio_xml include Poscobro entries (excluded by design per DEC-009) and entries where XML was not available at ingestion time

### PARIS (0.0% — FAIL)
- 62 DTE XML files exist in `01_Raw/PARIS/Facturacion/` but were never processed by the DTEIndexer
- The original 154 XMLs were reduced to 54 during Phase A2 recertification; the Facturacion directory has 62 files covering DTE types 33/43
- **RFC-PARIS-DTE-INDEXER**: Pending — DTEIndexer execution blocked by constraint

### FALABELLA (0.0% — FAIL)
- No XML files have been processed for FALABELLA
- Source data comes from XLSX files only; `folio_xml` was never populated

## DTE per Financial Group (RIPLEY)

| Financial Group | Total Rows | With folio_xml | Coverage |
|---|---|---|---|
| INGRESOS | 73,249 | 73,249 | 100% |
| DEVOLUCIONES | 10,206 | 10,206 | 100% |
| COSTOS_LOGISTICOS | 36,217 | 36,217 | 100% |
| COMISIONES | 53,336 | 53,336 | 100% |
| AJUSTES | 12,361 | 12,361 | 100% |
| LIQUIDACION | 31,946 | 24,863 | 77.8% |

## Verdict

**DTE CERTIFICATION: PARTIAL** ⚠️

| Marketplace | Status | Action Required |
|---|---|---|
| RIPLEY | ✅ CERTIFIED (96.7%) | None |
| ML | ⚠️ PARTIAL (51.3%) | Document non-XML sources |
| PARIS | ❌ FAIL (0.0%) | Execute DTEIndexer |
| FALABELLA | ❌ FAIL (0.0%) | Source XML ingestion needed |
