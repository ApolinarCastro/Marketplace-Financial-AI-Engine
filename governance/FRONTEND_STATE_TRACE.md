# FRONTEND STATE TRACE (P32.1 - Paso 1)

## Flujo de Eventos Actual
1. **Selector Marketplace / Período**: El usuario cambia el valor del select, lo que dispara el evento `onchange="loadDashboard()"`.
2. **loadDashboard() Inicio**:
   - `window._hasAuditAlerts = false;` (Reset de estado).
   - Llama a `clearFinancialFilter()`.
3. **Divergencia 1: Ejecución asíncrona descontrolada en clearFinancialFilter**:
   - `clearFinancialFilter()` limpia el filtro activo (`activeFinancialFilter = null`), oculta el banner.
   - **ERROR CRÍTICO**: Llama a `renderCierre()`, `loadAnalyticLayers()` y `fetchLedgerFromServer()`.
   - `fetchLedgerFromServer()` construye la URL leyendo el NUEVO valor del selector y dispara el `fetch`.
   - **El problema**: `clearFinancialFilter()` no es `async`, retorna inmediatamente. `loadDashboard()` continúa.
4. **loadDashboard() Continuación**:
   - Lee `mp` y `periodo` de los selectores.
   - Construye `mkQuery` y hace `await ApiClient.safeFetch('/api/v4/financial-structure' + mkQuery)`.
   - **Race Condition**: Mientras espera la respuesta de `financial-structure`, la llamada asíncrona de `fetchLedgerFromServer()` (disparada en el paso 3) puede retornar y sobrescribir `currentLedgerData` y llamar a `renderLedger()`.
   - `loadDashboard()` recibe `fsData`, hace `await ApiClient.getSummary()`.
   - Actualiza `window._financialStructure` con la data NUEVA.
   - Llama a `await ApiClient.safeFetch('/api/v4/auditoria' + mkQuery)`.
   - Llama *NUEVAMENTE* a `renderCierre()` y `loadAnalyticLayers()`.
   - Renderiza las alertas automáticamente inyectando HTML en `alerts-content` de forma destructiva, sobreescribiendo el DOM cada vez.
   - Llama a `fetchLedgerFromServer()` por SEGUNDA vez (redundante y destructivo).

## Identificación de la Primera Divergencia
La **primera divergencia** que rompe el flujo asíncrono y corrompe el estado ocurre en la función **`clearFinancialFilter()`**.
En lugar de limitarse a limpiar variables de estado, esta función dispara mutaciones del DOM y peticiones de red asíncronas de alto costo (`renderCierre`, `loadAnalyticLayers`, `fetchLedgerFromServer`), las cuales colisionan con el flujo orquestador principal (`loadDashboard`). 

Esto provoca que las vistas se rendericen con datos desincronizados (ej. `renderCierre()` se ejecuta usando un `window._financialStructure` obsoleto antes de que `loadDashboard` lo actualice) y produce múltiples llamadas a la API duplicadas que bloquean la coherencia visual.

## Conclusión (Paso 1 Completado)
La divergencia ha sido identificada exactamente. Se procederá al **Paso 2** para eliminar estas llamadas de `clearFinancialFilter` e imponer un orden de renderizado estricto y secuencial en `loadDashboard()`.
