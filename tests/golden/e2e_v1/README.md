# Golden Dataset E2E_V1

## DATASET_ID
E2E_V1

## MARKETPLACE
ML (MercadoLibre)

## WHY_SELECTED
- ML Facturacion ingestion path is the most stable and well-tested (used in f3_03 controlled ingestion test)
- SurgicalLoader handles ML Facturacion format with auto-header detection
- Sign convention is documented in surgical_loader.py docstring
- Existing synthetic fixture (f3_03) provides proven expected values

## SOURCE_TYPE
SYNTHETIC

## REAL_OR_SYNTHETIC
SYNTHETIC - Manually created, not derived from production data

## INPUT_FILES
```
tests/golden/e2e_v1/input/ML_Facturacion_E2E_V1.xlsx
```
Format: Excel (.xlsx) with columns: Venta, Detalle, Valor del cargo, Total de la venta, Fecha
5 rows representing:
1. E2E-001: Cargo por venta (9500 commission, 50000 gross)
2. E2E-002: Cargo por venta (5700 commission, 30000 gross)
3. E2E-001: Anulación del cargo por venta (-9500 commission reversal, 50000 gross refund)
4. E2E-003: Envío (1500 charge)
5. E2E-004: Publicidad (2000 charge)

## EXPECTED_FILES
```
tests/golden/e2e_v1/expected/expected_ledger.csv
tests/golden/e2e_v1/expected/expected_reconciliation.csv
tests/golden/e2e_v1/expected/expected_summary.json
```

## MANUAL_CALCULATION

Using ML sign convention from `engine/v4/surgical_loader.py`:

| Transaction | Type | Gross | Commission | Shipping/Ads | Net |
|-------------|------|-------|------------|--------------|-----|
| E2E-001 | Sale | +50000 | -9500 | 0 | +40500 |
| E2E-002 | Sale | +30000 | -5700 | 0 | +24300 |
| E2E-001 | Refund | -50000 | +9500 (reversal) | 0 | -40500 |
| E2E-003 | Shipping | 0 | 0 | -1500 | -1500 |
| E2E-004 | Advertising | 0 | 0 | -2000 | -2000 |
| **TOTAL** | | **+80000** | **-15200** | **-3500** | **+20800** |

Formula: `80000 - 15200 - 3500 - 50000 + 9500 = 20800`

Sign convention: **positivo = a favor del vendedor, negativo = costo/pérdida**

## EXPECTED_RESULT

| Metric | Value |
|--------|-------|
| Expected ledger rows | 8 |
| Expected reconciliation rows | 5 |
| Expected gross amount | 80000.0 |
| Expected charges | 18700.0 |
| Expected refunds | 50000.0 |
| Expected commission reversals | 9500.0 |
| Expected net result | 20800.0 |

## FINANCIAL_RULE_REFERENCES
- `engine/v4/surgical_loader.py` lines 64-79: ML sign convention documentation
- `engine/v4/surgical_loader.py` `read_excel_auto`: header detection logic
- `tests/fixtures/f3_03/f3_03_test.py`: proven expected ledger values for identical structure
- `engine/v4/reconciliation/reconciliation_engine.py` `_determine_status()` (lines 94-116): status logic
- `engine/v4/reconciliation/reconciliation_rules.yaml`: CERTIFICADO requires document_coverage >= 95
- `engine/v4/reconciliation/reconciliation_engine.py` line 578: LEVEL_4 delta = 100.0 - coverage

## RECONCILIATION_EXPECTATIONS

Per the real reconciliation contract, E2E_V1 (zero DTE/XML documents):

| Level | delta | taxonomy | document | status | Rationale |
|-------|-------|----------|----------|--------|-----------|
| LEVEL_1 | 0.0 | 100.0 | 0.0 | PENDIENTE | Internal ledger consistency holds; doc gate blocks CERTIFICADO |
| LEVEL_2 | 0.0 | 100.0 | 0.0 | PENDIENTE | Operational P&L consistent; doc gate blocks CERTIFICADO |
| LEVEL_3 | 0.0 | 100.0 | 0.0 | PENDIENTE | Treasury mirror out of scope (Facturacion-only dataset) |
| LEVEL_4 | 100.0 | 100.0 | 0.0 | PENDIENTE | delta = 100 - 0 coverage; 8 unmatched records |
| LEVEL_5 | 0.0 | 100.0 | 0.0 | PENDIENTE | Aggregate: financially consistent, pending documentary evidence |

Status derivation: `_determine_status()` returns PENDIENTE when `document_coverage (0.0) < 10`.
CERTIFICADO is unreachable without DTE/XML (requires document_coverage >= 95).

## FA-005 SCOPE

E2E_V1 CAN certify FA-003 (ingestion) and FA-004 (ledger internal consistency).
E2E_V1 CANNOT certify FA-005 to CERTIFICADO without DTE/XML evidence.
This is a KNOWN_NEXT_BLOCKER, not an active blocker until FA-003/FA-004 execute.

## ASSUMPTIONS
NONE

## KNOWN_LIMITATIONS
1. Single marketplace (ML) - does not test cross-marketplace reconciliation
2. Single document type (Facturacion) - does not test Poscobro, Liberaciones, or XML matching
3. No DTE/XML documents - document coverage will be 0% (below 95% threshold for CERTIFICADO)
4. Uses temporary directory monkey-patch pattern (same as f3_03 test)
5. Requires baseline DB copy for isolated execution