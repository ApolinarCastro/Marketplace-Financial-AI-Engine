# DTE Reactivation Report — Phase 14A

## Status: OPERATIONAL ✅

## Previous State

The `/api/v4/exec/summary` endpoint returned hardcoded zeros for all DTE metrics:
```json
{"xml_conciliados": 0, "xml_pendientes": 0, "total_dte": 0, "cobertura": 0}
```

The executive dashboard consumed this data, showing "—" for all DTE badges.

## Fix

Replaced hardcoded zeros with real queries from `marketplace_ledger_v1`:
- `xml_conciliados`: COUNT of rows where `folio_xml IS NOT NULL`
- `xml_pendientes`: total rows - xml_conciliados
- `total_dte`: total ledger rows matching period/marketplace
- `cobertura`: xml_conciliados / total_dte × 100

Data is now scoped by period and marketplace (respects `?periodo=` and `?marketplace=` parameters).

## Current Coverage (YTD 2026)

| Marketplace | Conciliados | Pendientes | Total | Cobertura |
|-------------|------------|-----------|-------|-----------|
| **FALABELLA** | 0 | 2,609 | 2,609 | **0.0%** |
| **ML** | 21,669 | 20,439 | 42,108 | **51.5%** |
| **PARIS** | 0 | 10,437 | 10,437 | **0.0%** |
| **RIPLEY** | 47,708 | 4,757 | 52,465 | **90.9%** |
| **TOTAL** | **69,377** | **38,242** | **107,619** | **64.5%** |

## Notes

- **RIPLEY** has highest coverage (90.9%) — 210,232 of 217,315 rows have `folio_xml` from XLSX source.
- **ML** has moderate coverage (51.3%) — 96,098 of 187,455 rows have `folio_xml`.
- **FALABELLA** and **PARIS** have 0% coverage because the DTEIndexer has NOT been executed. XML files exist on disk but are not ingested into the ledger.
- `estado_xml` column exists but is NOT maintained by the current pipeline (all FALABELLA/PARIS rows show "PENDIENTE"; ML/RIPLEY rows are NULL).

## Pending

- Execute DTEIndexer for PARIS (62 XMLs in `01_Raw/PARIS/Facturacion/`) and FALABELLA
- Populate `estado_xml` column from actual conciliation status
- Consider adding `asociacion_xml` validation

**Date:** 2026-06-17
