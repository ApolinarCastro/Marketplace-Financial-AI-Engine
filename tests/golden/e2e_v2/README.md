# Golden Dataset E2E_V2

## DATASET_ID
E2E_V2

## MARKETPLACE
ML (MercadoLibre)

## WHY_SELECTED
- Same proven ML Facturacion path as E2E_V1 (FA-003/FA-004 certified).
- Extends E2E_V1 with the minimum additions for full-chain reconciliation:
  one treasury row + synthetic document matches via certified DocumentMatchWriter.
- E2E_V1 preserved untouched as FA-003/FA-004 historical evidence.

## SOURCE_TYPE
SYNTHETIC

## REAL_OR_SYNTHETIC
SYNTHETIC — manually created, not derived from production data. Folios are
`SYNTH-*` synthetic markers, never SII folios. Provenance fields state
`PFO_SYNTHETIC_GOLDEN` / `PFO_E2E_V2` explicitly.

## INPUT_FILES
```
tests/golden/e2e_v2/input/ML_Facturacion_E2E_V2.xlsx
```
6 rows: E2E_V1's 5 certified rows + treasury row
("E2E-TES", "Retiro de dinero", 20800.0, 0.0, "2026-06-20").

Loader contract (engine/v4/surgical_loader.py else-branch):
"Retiro de dinero" matches no cargo_venta/anulacion pattern →
`tipo_movimiento=CARGO`, `monto=-valor_cargo=-20800.0`, detalle preserved.

Classifier contract (engine/v4/marketplace_auditor.py):
"Retiro de dinero" ∈ FINANCIAL_STRUCTURE["tesoreria"] →
`financial_group='tesoreria'`, `include_in_operational_pnl=FALSE`
(ML mask + general exclusions).

## EXPECTED_FILES
```
tests/golden/e2e_v2/expected/expected_ledger.csv (9 rows, raw contract: empty financial_group)
tests/golden/e2e_v2/expected/expected_reconciliation.csv (5 rows, engine vocabulary)
tests/golden/e2e_v2/expected/expected_summary.json
tests/golden/e2e_v2/expected/expected_document_matches.csv (9 synthetic CONCILIATED matches)
```

## MANUAL_CALCULATION

Operational (op_pnl=TRUE, 8 rows):
`80000 - 15200 - 3500 - 50000 + 9500 = 20800`

Treasury (op_pnl=FALSE, 1 row): `-20800`

Mirror (Level 3 equation: operational + treasury ≈ 0):
`20800 + (-20800) = 0` → delta 0, PASS.

Document coverage: 9 CONCILIATED / 9 classified = 100.0 → delta 0, PASS.

Aggregate via `_determine_status` + reconciliation_rules.yaml:
delta 0 + taxonomy 100 + document 100 → CERTIFICADO.

Sign convention: **positivo = a favor del vendedor, negativo = costo/pérdida**.

## EXPECTED_RESULT

| Metric | Value |
|--------|-------|
| Expected ledger rows | 9 (8 operational + 1 treasury) |
| Operational net | 20800.0 |
| Treasury total | -20800.0 |
| Mirror delta | 0.0 |
| Document matches | 9/9 → 100.0 |
| Aggregate status | CERTIFICADO |

## FINANCIAL_RULE_REFERENCES
- `engine/v4/surgical_loader.py` LEDGER_COLS + else-branch (raw contract, no financial_group)
- `engine/v4/marketplace_auditor.py` FINANCIAL_STRUCTURE["tesoreria"], op_pnl exclusions, run_financial_closing (op_pnl=TRUE only)
- `engine/v4/reconciliation/reconciliation_engine.py` Levels 1-4 + _determine_status
- `engine/v4/reconciliation/reconciliation_rules.yaml` (CERTIFICADO thresholds)
- `engine/v4/matching/document_match_writer.py` (match persistence contract)

## ELECTRONIC_CERTIFICATION_BOUNDARY

```
XML_DTE_INGESTED = NO
DTE_TRUTH_POPULATED_FROM_XML = NO
DOCUMENT_MATCH_SOURCE = SYNTHETIC_GOLDEN_WRITER (DocumentMatchWriter, certified)
XML_ELECTRONIC_CERTIFICATION = NOT_TESTED
```

FA-005 PASS on E2E_V2 certifies reconciliation behavior, NOT electronic
fiscal certification. The mandatory follow-up is PFO-XML-DTE-E2E-001
(synthetic valid XML → ingestion → dte_truth_v1 → match decision → writer).

## ASSUMPTIONS
NONE beyond stated contracts.

## KNOWN_LIMITATIONS
1. Single marketplace (ML), single document type (Facturacion).
2. Document matches are synthetic fixture records, not SII DTE evidence.
3. Fresh TEMP_DB scope: engine sees only E2E_V2 rows for ML/2026-06.
