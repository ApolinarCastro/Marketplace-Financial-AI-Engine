# FRONTEND CALL GRAPH BEFORE

## INVENTARIO ACTUAL DE FUNCIONES DE CARGA Y ORQUESTACIÓN

### 1. loadDashboard()
- **Llamada por:** <script> al final del documento (carga inicial), y por evento onchange en los selectores de Marketplace y Período, además de unAudit().
- **Acciones:**
  1. clearFinancialFilter() (que a su vez dispara un ciclo completo de llamadas HTTP y renderizado).
  2. etch('/api/v4/financial-structure')
  3. ApiClient.getSummary()
  4. etch('/api/v4/dte/certify')
  5. Asignaciones a window._financialStructure.
  6. etch('/api/v4/auditoria')
  7. enderCierre()
  8. loadAnalyticLayers() (que lanza otra cadena asíncrona pesada).
  9. etchLedgerFromServer()
- **Problema principal:** Se ejecuta a sí mismo pero antes dispara clearFinancialFilter, duplicando las llamadas 7, 8 y 9.

### 2. clearFinancialFilter()
- **Llamada por:** Botón "Limpiar filtro" en UI, y por loadDashboard().
- **Acciones:**
  1. Borra ctiveFinancialFilter.
  2. enderCierre()
  3. loadAnalyticLayers()
  4. etchLedgerFromServer()
- **Problema principal:** Al ser llamada desde loadDashboard, dispara un ciclo completo de red redundante antes de que loadDashboard haya obtenido la nueva Estructura Financiera.

### 3. pplyFinancialFilter(type, value, label)
- **Llamada por:** Clicks en las filas de la Estructura Financiera.
- **Acciones:**
  1. Setea ctiveFinancialFilter.
  2. enderCierre()
  3. etchLedgerFromServer()
- **Observación:** Provoca una recarga desde el servidor del Ledger, lo cual es correcto, pero no interfiere con Analytics.

### 4. loadAnalyticLayers()
- **Llamada por:** loadDashboard(), clearFinancialFilter().
- **Acciones:**
  1. etch('/api/v4/exec/summary') (Duplicado a nivel conceptual con el que hace loadDashboard).
  2. Síncronamente espera: wait Promise.all([ document-gap, risk-summary, coverage ])
  3. Bloque catch(e) global que destruye la UI si falla document-gap.
- **Problema principal:** Secuencialidad y acoplamiento rígido con endpoints lentos (document-gap).

### 5. enderCierre()
- **Llamada por:** loadDashboard(), clearFinancialFilter(), pplyFinancialFilter(), 	oggleMode().
- **Acciones:**
  1. Lee window._financialStructure.
  2. Si es null/undefined, pinta Skeleton "Sin datos" o "En Construcción".
  3. Si tiene datos, renderiza HTML de la Estructura Financiera.
- **Observación:** No hace llamadas de red, es pura renderización síncrona.

### 6. etchLedgerFromServer()
- **Llamada por:** loadDashboard(), clearFinancialFilter(), pplyFinancialFilter().
- **Acciones:**
  1. Muestra spinner en UI.
  2. etch(buildLedgerUrl(0))
  3. Guarda data en currentLedgerData y window._ledgerTotalCount.
  4. enderLedger()
- **Observación:** Al ser llamado 2 veces al inicio, lanza doble petición a /api/v4/ledger.

### 7. enderLedger()
- **Llamada por:** etchLedgerFromServer(), loadMoreLedger(), evento change del filtro local de detalles.
- **Acciones:**
  1. Renderiza currentLedgerData.
- **Observación:** Renderización síncrona segura.

---

## SECUENCIA DE EJECUCIÓN INICIAL (El Auto-DDoS)

1. Navegador carga HTML.
2. Invocación inicial de loadDashboard().
3. loadDashboard llama a clearFinancialFilter().
4. clearFinancialFilter() ejecuta simultáneamente:
   - enderCierre() (pinta Skeleton temporal porque window._financialStructure es null).
   - loadAnalyticLayers() (Lanza peticiones lentas: document-gap, isk-summary).
   - etchLedgerFromServer() (Lanza petición a ledger).
5. Inmediatamente después de lanzar (sin esperar a que terminen), loadDashboard() continúa su flujo síncrono:
   - etch('financial-structure') -> **QUEDA BLOQUEADO** porque Uvicorn está procesando document-gap (lanzado en paso 4).
   - etch('summary')
   - etch('certify')
   - etch('auditoria')
   - Vuelve a llamar a enderCierre() (aún con Skeleton).
   - Vuelve a llamar a loadAnalyticLayers() (Lanza 2da ronda de peticiones lentas).
   - Vuelve a llamar a etchLedgerFromServer() (Lanza 2da petición a ledger).

**Conclusión del Grafo Antes:**
La concurrencia descontrolada y la invocación cíclica ahogan el pool de conexiones del backend, detienen la renderización principal en un Skeleton, y un error en Analytics rompe el contrato visual ("BACKEND CONTRACT REQUIRED").

