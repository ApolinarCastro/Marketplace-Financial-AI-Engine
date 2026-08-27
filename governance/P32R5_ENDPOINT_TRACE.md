# P32R5 ENDPOINT TRACE

## Traza de Endpoints

### 1. `/api/v4/documentary/coverage`
- **Firma:** `def get_documentary_coverage(marketplace: str | None = None, periodo: str | None = None)`
- **Validación:** Si `not periodo`, retorna diccionario con `"NO DISPONIBLE"`.
- **Propagación:** Pasa `periodo` a `engine._certify_*`.

### 2. `/api/v4/dte/document-gap`
- **Firma:** `def get_document_gaps(marketplace: str = None, periodo: str = None, limit: int = 500)`
- **Validación:** Si `not periodo`, retorna diccionario con contadores en `0` y arrays vacíos.
- **Propagación:** Pasa `marketplace` y `periodo` a `engine.get_document_gaps`.

### 3. `/api/v4/dte/risk-summary`
- **Firma:** `def get_risk_summary(marketplace: str = None, periodo: str = None)`
- **Validación:** Si `not periodo`, retorna diccionarios y arrays vacíos.
- **Propagación:** Pasa `marketplace` y `periodo` a `engine.get_risk_summary`.

### 4. `/api/v4/electronic_certification/status/{transaction_id}`
- **Firma:** `def get_electronic_certification_status(transaction_id: str, response, marketplace: str = None, periodo: str = None)`
- **Validación:** Si `not periodo`, retorna `"NO DISPONIBLE"`.
- **Propagación:** Construye parámetros `transaction_id` y fechas de `_resolve_period_range` e invoca consulta.
