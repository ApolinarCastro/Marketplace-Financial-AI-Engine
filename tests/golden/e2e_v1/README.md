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

## ASSUMPTIONS
NONE

## KNOWN_LIMITATIONS
1. Single marketplace (ML) - does not test cross-marketplace reconciliation
2. Single document type (Facturacion) - does not test Poscobro, Liberaciones, or XML matching
3. No DTE/XML documents - document coverage will be 0% (below 95% threshold for CERTIFICADO)
4. Uses temporary directory monkey-patch pattern (same as f3_03 test)
5. Requires baseline DB copy for isolated execution