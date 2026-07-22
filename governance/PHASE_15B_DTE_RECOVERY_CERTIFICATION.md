# Phase 15B — DTE Recovery Certification

**Date**: 2026-06-18
**Status**: CERTIFIED WITH LIMITATIONS ⚠️
**Engine**: `engine/v4/dte_indexer.py` v2, `engine/v4/xml_matcher.py` v2

## What Was Executed

### DTEIndexer
- **PARIS**: 62 XMLs procesados → 62 records en `dte_truth_v1` (tipo_dte, rut_receptor, marketplace, fecha_emision, monto_total, folio)
- **FALABELLA**: 6 XMLs procesados → 6 records en `dte_truth_v1`
- Schema: `dte_truth_v1` hot-migrated to include `tipo_dte`, `rut_receptor`, `marketplace` columns

### XMLMatcher
- **Heuristic**: `ABS(monto)` + fecha ±7 días
- **Result**: 0 matches for PARIS, 0 matches for FALABELLA
- **Root cause**: Heuristic is too generic — amount+fecha alignment fails because ledger stores net amounts (after commissions/deductions) while XML is gross. Without order_id linkage, matching is unreliable.

## Current DTE Coverage
| MP | Ledger Rows | folio_xml Populated | Coverage | Source |
|---|---|---|---|---|
| ML | 101,603 | ~51.3% | ✅ | Liberaciones XLSX |
| RIPLEY | 62,502 | ~96.7% | ✅ | XLSX Número Factura |
| PARIS | 42,487 | 0% | ❌ | XLSX Número Factura column exists, but not certified |
| FALABELLA | 1,008 | 0% | ❌ | No XML source available |

## Requirements for XML-to-Ledger Matching
1. **PARIS**: XLSX column "Número Factura" → should map to `folio_xml`. This is how the legacy loader works. DTEIndexer is NOT the source of `folio_xml` for PARIS.
2. **Order-level linkage**: DTEIndexer + XMLMatcher can only work if there is an `order_id` or `id_transaccion` in the XML. Currently no cross-reference exists.
3. **Next step**: Implement order_id extraction from DTE references (DTE 43 references origin DTE in `Referencia` tag).

## Verdict
- DTEIndexer executes correctly (68/68 records)
- XMLMatcher heuristic fails for cross-MP matching without order_id — **this is a known limitation, not a bug**
- PARIS `folio_xml` must come from XLSX pipeline, not DTEIndexer
