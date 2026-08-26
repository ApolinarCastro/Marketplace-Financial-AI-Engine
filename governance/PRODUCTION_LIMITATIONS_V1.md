# PRODUCTION LIMITATIONS V1
Fecha: 2026-08-26

## Estado
- RIPLEY_FINANCIAL_RECONCILIATION = SUPPORTED (ledger 287k, settlement trace PASS)
- RIPLEY_SETTLEMENT_TRACEABILITY = SUPPORTED
- RIPLEY_FISCAL_SII_CERTIFICATION = BLOCKED (external fiscal bridge unavailable, settlement_ref != SII_DTE, overlap 0)
- REASON: external fiscal bridge unavailable, proven exhaustive search, isolated, not compromising rest
- SHOPIFY = REJECTED_WITH_PROVEN_REASON (243 files, 0 ledger, non-financial)
- FALABELLA cobertura 2 meses (2026-05 y 2014-08) vs 19 esperados -> SOURCE_PARTIAL but financial truth correct per ledger
