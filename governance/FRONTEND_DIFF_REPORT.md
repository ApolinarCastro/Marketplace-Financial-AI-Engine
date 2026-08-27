# FRONTEND DIFF REPORT

### Comparación (BASELINE `0f71cc4` vs ACTUAL)

Al realizar el Diff Quirúrgico detectamos las siguientes funciones y endpoints modificados/rotos en el código regresivo:

1. **`templates/dashboard.html`**:
   - Múltiples funciones `render*` fueron mutiladas o eliminadas.
   - Fallbacks y Promesas de fetch sin catch correcto que inducían a un *Loading infinito*.
   - El Drawer Documental (`#inspector-modal`) y su controlador perdieron el mapeo original de `folio_xml`.

2. **`api/api.py`**:
   - Endpoint `/api/v4/electronic_certification/status/{transaction_id}` inyectado con un **error 409 (BACKEND_CONTRACT_INCOMPLETE) hardcodeado**, lo que forzaba intencionalmente el fallo de la certificación electrónica independientemente del estado real de DuckDB.
   - Mutación de respuestas en `/api/v4/ledger`, introduciendo desajustes en la estructura JSON esperada por la interfaz.

**Acción Correctiva**: Reversión aséptica y exclusiva de `api/api.py` y `templates/dashboard.html` hacia la versión del commit `0f71cc4`, eliminando la regresión de raíz.
