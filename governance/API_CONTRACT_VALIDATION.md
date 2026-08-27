# API CONTRACT VALIDATION (P32.2)

## Objetivo
Verificar y certificar que los contratos de los endpoints clave de la API en FastAPI coincidan exactamente con la estructura de consumo esperada por el Frontend, eliminando hardcodes y mockups falsos.

## Endpoints Validados

### 1. `/api/v4/financial-structure`
- **Estado**: VÁLIDO.
- **Correcciones**: Ninguna necesaria. El endpoint respeta la agrupación por `financial_group` e `items`, calculando los totales de `monto` de forma consistente. Filtra adecuadamente por `marketplace`, `periodo` y consideraciones de P&L operacional.

### 2. `/api/v4/ledger`
- **Estado**: CORREGIDO Y VÁLIDO.
- **Corrección Aplicada**: Se eliminó un comportamiento defectuoso donde al solicitar el marketplace `ALL`, la API literalmente filtraba por la cadena `"ALL"` en SQLite, devolviendo resultados vacíos. Ahora evalúa correctamente `ALL` y omite el filtro de marketplace, retornando la información consolidada.

### 3. `/api/v4/auditoria`
- **Estado**: CORREGIDO Y VÁLIDO.
- **Corrección Aplicada**: El endpoint original ignoraba el parámetro `periodo` y forzaba el marketplace `"ML"` o consultaba `"ALL"` como literal. Se actualizó para recibir opcionalmente `marketplace` y `periodo`, respetando los estándares de `_resolve_period_range` o manejando las consultas correctamente con fechas de inicio y fin de mes.

### 4. `/api/v4/cierre`
- **Estado**: CORREGIDO Y VÁLIDO.
- **Corrección Aplicada**: Al igual que `/api/v4/ledger`, ignoraba el estado "ALL", generando retornos vacíos o errores. Ahora procesa correctamente el filtro de marketplace condicional.

### 5. `/api/v4/electronic_certification/status/{transaction_id}`
- **Estado**: COMPLETAMENTE RECONSTRUIDO Y VÁLIDO.
- **Corrección Crítica Aplicada**: El endpoint antiguo retornaba un objeto incompatible desde `DocumentGapEngine()`. El frontend esperaba un contrato estricto con `tipo_dte`, `folio`, objeto `pipeline` (xml, xsd, sig, caf) y objeto `evidencia` (hash, confidence, level). 
- **Solución**: Reconstruido el endpoint para consultar directamente `marketplace_ledger_v1`, mapeando el valor real de `estado_xml` (CONCILIADO, DOCUMENTADO, etc.) y construyendo el objeto JSON idéntico a lo que exige el Drawer de certificación del dashboard.

## Conclusión
La consistencia entre Frontend y Backend ha sido restaurada sin introducir nuevos adaptadores. Ninguna regresión detectada.
