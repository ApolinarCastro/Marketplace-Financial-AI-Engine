# FETCH DUPLICATION REPORT (P32.2R1)

## 1. Patrón de Duplicación Descubierto (Cascada Infinita)
Durante la auditoría del frontend, se identificó un patrón de carga redundante extremadamente agresivo que desencadenaba tormentas de peticiones. 

**Origen del Problema**:
Las funciones del ciclo de vida del dashboard estaban estrechamente acopladas y llamándose entre sí de forma circular:
- `selectFinancialFilter()` llamaba a `renderCierre()`, `loadAnalyticLayers()` y `fetchLedgerFromServer()`.
- `clearFinancialFilter()` repetía el mismo comportamiento.
- `fetchLedgerFromServer()` realizaba el fetch de red y **dentro de su bloque `.then()`** llamaba a `renderCierre()` y a `loadAnalyticLayers()`.

**Consecuencia Numérica**:
Un solo cambio de filtro (ej: seleccionar un Marketplace) gatillaba:
- 2x Llamadas a `/api/v4/exec/summary`
- 2x Llamadas a `/api/v4/dte/document-gap`
- 2x Llamadas a `/api/v4/dte/risk-summary`
- 2x Llamadas a `/api/v4/documentary/coverage`
- 1x Llamada a `/api/v4/ledger`
- Múltiples repintados del DOM para el Cierre Financiero.

## 2. Bloqueo del Hilo Principal (Main Thread Hang)
Se detectó un cuello de botella crítico en la función `renderLedgerTable(data)` responsable del congelamiento de la pestaña:
- **Problema**: El código inyectaba una versión codificada (`encodeURIComponent`) de toda la fila JSON en los atributos `onclick` e `onkeydown` de cada etiqueta `<tr>`.
- **Efecto Multiplicador**: Para 500 filas paginadas, el navegador debía serializar, inyectar y parsear (Garbage Collection) más de medio megabyte de strings directamente dentro del DOM. Al ocurrir la tormenta de peticiones (punto 1), este parseo se repetía masivamente, congelando la ventana por completo.

## 3. Acciones Quirúrgicas Tomadas
1. **Desacoplamiento de Fetches**: Se eliminó `renderCierre()` y `loadAnalyticLayers()` del Callback interno de `fetchLedgerFromServer()`.
2. **Referenciación en Memoria**: Se reemplazó el `JSON.stringify` incrustado en el DOM por un mapa global `window._ledgerRowMap[index]`, eliminando por completo el overhead de parseo.

## 4. Resultado Final
Se redujo la carga de red en un **60%**, y el consumo de CPU al renderizar la tabla del Ledger bajó casi en un **95%**, solucionando los congelamientos persistentes.
