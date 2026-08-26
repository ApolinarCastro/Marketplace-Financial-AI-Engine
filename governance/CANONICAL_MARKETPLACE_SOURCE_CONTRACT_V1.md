# CANONICAL MARKETPLACE SOURCE CONTRACT V1
Fecha: 2026-08-26
Autoridad: evidence/raw_source_truth_v1/canonical_source_matrix.json

## Reglas permanentes
- RAW es READ-ONLY, 1313 archivos baseline.
- Solo GOLDEN_MANDATORY / GOLDEN_CONDITIONAL se ingieren para cierre certificado.
- SHOPIFY 243 archivos REJECTED (0 ledger rows, sin trazabilidad).
- RIPLEY fiscal BLOCKED hasta SII bridge.

## Fuentes por marketplace
- ML: Facturacion (GOLDEN_MANDATORY) + Documentos (SUPPORTING) -> ledger 109k rows
- PARIS: Facturacion + Documentos -> ledger 197k
- RIPLEY: Facturacion + Fulfillment + Mis extractos -> ledger 287k, DTE BLOCKED
- FALABELLA: Facturación (4 periodos) + Documentos (5 folios) -> ledger 3k
- SHOPIFY: REJECTED

Ver detalles en canonical_source_matrix.json y golden_report_evaluation.csv
