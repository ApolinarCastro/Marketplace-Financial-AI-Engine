# SOURCE INGESTION RECONCILIATION - EXECUTION REPORT
Fecha: 2026-08-26T17:20:34.119485
Precheck: DB 311c78e2 match, RAW 1313, ledger 598112, classification PASS
Inventario: raw_master_inventory 1313, duplicates 110 grupos, semantic 971 DTE
Registry: 1212 RAW_NOT_REGISTERED, handler coverage REVIEW
Falabella: 15 files, monthly -785k/-1.15M/-267k NEGATIVO, gate PASS
ML/PARIS/RIPLEY/SHOPIFY contracts definidos, SHOPIFY REJECTED
Golden V2: ML Facturacion MANDATORY, PARIS SUPPORTING, RIPLEY MANDATORY, SHOPIFY REJECTED
Controlled ingestion: copy SHA match, idempotency PASS 3x
RAW->Ledger: ML 341->109k, SHOPIFY 243->0 explicada
E2E: 4 marketplaces traceability PASS, financial truth 13 queries PASS, exception 8362, audit READ_ONLY PASS, regression 39 passed, idempotency 3x PASS, adversarial 0 critical, promotion NO_PROMOTION_REQUIRED
