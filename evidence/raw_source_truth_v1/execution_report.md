# RAW SOURCE TRUTH V1 - EXECUTION REPORT
Fecha: 2026-08-26T17:09:48.476364
Inventario: 1313 archivos (RIPLEY 623, ML 341, SHOPIFY 243, PARIS 91, FALABELLA 15) 116MB 971 XML 236 XLSX 99 CSV
Duplicados: 110 grupos SHA (268 archivos, 20%), caso Falabella marzo-abril ya no duplicado (SHA distinto)
Temporal: RIPLEY 24 meses, PARIS 19, ML 19, FALABELLA 2, SHOPIFY 3 (incompleto)
Schema: 38 estables, 11 evolucionados
Semantica: DTE 971, Fulfillment 91, Settlement 52, Commission 42
File Registry: 157 registrados, 1212 no registrados (92%)
Ingestion: 933 no ingeridos, SHOPIFY 243 con 0 ledger rows -> REJECTED
RAW->Ledger: ML 341->109k, PARIS 91->197k, RIPLEY 623->287k, FALABELLA 15->3k, SHOPIFY 243->0
Ventas omitidas: Falabella raw 12 no registrados, ledger 369 ordenes; SHOPIFY omission total
Causa raiz: 1212 UNKNOWN/NOT_REGISTERED, PATH_MISMATCH, HANDLER_MISSING
Golden: ML Facturacion MANDATORY, PARIS Facturacion SUPPORTING, RIPLEY Fulfillment+Mis extractos MANDATORY, FALABELLA Facturacion MANDATORY, SHOPIFY REJECTED
Source gate: PARTIAL_WITH_BLOCKER (Falabella cobertura 2 meses, Ripley fiscal)
Remediation: registrar 316 ML, actualizar Falabella handler, decidir SHOPIFY
E2E: ledger API ok 4/4 MPs con datos (SHOPIFY 0), DTE trace 88k rows, cadena RAW->API demuestra trazabilidad con pérdida explicada
