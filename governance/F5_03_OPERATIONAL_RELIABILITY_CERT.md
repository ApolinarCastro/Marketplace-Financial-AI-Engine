# F5-03 — OPERATIONAL RELIABILITY CERTIFICATION

## META
- **Execution Date:** 2026-07-23
- **Baseline:** V8 Certified
- **Status:** PASS
- **Execution Script:** scripts/f5_03_idempotency_certify.py
- **Scope:** ML, Paris, Ripley, Falabella

## OBJETIVO
Certificar que el sistema posee confiabilidad operacional (Idempotencia y Recuperación) frente a interrupciones y duplicados, garantizando que el estado final en ingestion_registry y marketplace_ledger_v1 sea idéntico (determinado mediante un HASH semántico, ignorando metadata temporal o volátil).

## RESULTADOS DE LOS CASOS DE PRUEBA

### MERCADO LIBRE (ml_golden.xlsx)
- **CASO 1 (First Load):** COMPLETED.
  - REGISTRY HASH: 3fafcef3f7e
  - LEDGER HASH: 228cbd9c1ebc
- **CASO 2 (Exact Duplicate):** SKIPPED_DUPLICATE. (Prevención de duplicados exitosa).
- **CASO 3 (Interrupted Before Ledger -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **CASO 4 (Interrupted After Registry -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **Status General:** PASS

### PARIS (paris_golden.xlsx)
- **CASO 1 (First Load):** COMPLETED.
  - REGISTRY HASH: 17fa834a0fa8
  - LEDGER HASH: 4f53cda18c2b
- **CASO 2 (Exact Duplicate):** SKIPPED_DUPLICATE.
- **CASO 3 (Interrupted Before Ledger -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **CASO 4 (Interrupted After Registry -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **Status General:** PASS

### RIPLEY (ripley_golden.csv)
- **CASO 1 (First Load):** COMPLETED.
  - REGISTRY HASH: 8c6bcd4c3b91
  - LEDGER HASH: 6c1c2bdbdc34
- **CASO 2 (Exact Duplicate):** SKIPPED_DUPLICATE.
- **CASO 3 (Interrupted Before Ledger -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **CASO 4 (Interrupted After Registry -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **Status General:** PASS

### FALABELLA (falabella_golden.xlsx)
- **CASO 1 (First Load):** COMPLETED.
  - REGISTRY HASH: 3cac3fe2795f
  - LEDGER HASH: 7e5fcaa6d1ec
- **CASO 2 (Exact Duplicate):** SKIPPED_DUPLICATE.
- **CASO 3 (Interrupted Before Ledger -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **CASO 4 (Interrupted After Registry -> Retry):** COMPLETED. (Hashes idénticos al Caso 1).
- **Status General:** PASS

## CONCLUSIÓN
La arquitectura de IngestionOrchestrator implementada en la versión v4 ha demostrado ser **100% idempotente y resiliente a fallos** para los cuatro marketplaces.
- **Deduplicación:** Archivos con el mismo SHA256 son omitidos correctamente sin duplicar impacto financiero.
- **Recuperación:** La persistencia se realiza bajo protección, y un rollback de ile_registry sobre ejecuciones fallidas permite la reingestión idéntica asegurando conservación de valor.

**F5-03 CERTIFICADO EXITOSAMENTE.**
