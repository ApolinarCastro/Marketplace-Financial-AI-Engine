# FRONTEND CALL GRAPH AFTER

## INVENTARIO ACTUALIZADO DE FUNCIONES DE CARGA Y ORQUESTACIÓN

### 1. initializeDashboard()
- **Llamada por:** <script> al final del documento, selectores onchange, unAudit().
- **Acciones:**
  1. Verifica window._dashboardLoading. Si es 	rue, aborta (Prevención de duplicidad / Mutex).
  2. Cancela peticiones previas mediante window.dashboardAbortController.abort().
  3. Ejecuta orchestrateDashboard(signal).

### 2. orchestrateDashboard(signal)
- **Llamada por:** initializeDashboard().
- **Acciones:**
  1. Reinicia alertas y UI (Pinta el Skeleton explícito Cargando Estructura Financiera).
  2. Ejecuta Promise.all con las **Llamadas Críticas** (con signal):
     - inancial-structure
     - summary
     - dte/certify
     - uditoria
  3. Espera resolución.
  4. Llama a enderCierre() (Render síncrono del HTML).
  5. Inicia peticiones asíncronas no bloqueantes:
     - etchLedgerFromServer(signal)
     - loadAnalyticLayers()

### 3. clearFinancialFilter()
- **Llamada por:** Botón "Limpiar filtro" en la UI.
- **Acciones:**
  1. Borra filtro activo.
  2. enderCierre() (síncrono, con datos en memoria).
  3. etchLedgerFromServer()
- **Cambio crítico:** Ya no invoca loadAnalyticLayers() ni orquesta todo el Dashboard de nuevo.

### 4. loadAnalyticLayers(mp, periodo)
- **Llamada por:** orchestrateDashboard().
- **Acciones:**
  1. Ejecuta etch('/api/v4/dte/document-gap') (Con AbortSignal.timeout(8000)).
  2. Ejecuta etch('/api/v4/dte/risk-summary') de forma concurrente, sin depender de Gap.
  3. Ejecuta etch('/api/v4/documentary/coverage').
  4. Actualiza independientemente cada Widget (Render aislado por Widget).
- **Cambio crítico:** document-gap ya no bloquea el dashboard ni genera cascada de errores.

### 5. etchLedgerFromServer(signal)
- **Llamada por:** orchestrateDashboard(), clearFinancialFilter(), pplyFinancialFilter().
- **Acciones:**
  1. Pinta spinner de carga en el panel de Ledger.
  2. Invoca /api/v4/ledger con el AbortSignal.
  3. enderLedger().

---

## NUEVA SECUENCIA DE EJECUCIÓN (Flujo Único Controlado)

1. Navegador carga HTML.
2. Invocación de initializeDashboard().
3. orchestrateDashboard inicia las llamadas críticas en paralelo (Mutex activado).
4. Mientras se espera, se pinta la UI de Carga Crítica.
5. Terminan las llamadas críticas -> Se pinta la Estructura Financiera.
6. Se dispara la petición del Ledger y se pinta un Spinner temporal en su contenedor.
7. Se disparan las capas analíticas en segundo plano (Analytics Loaders independientes).
8. document-gap tarda 85 segundos. A los 8 segundos, el Frontend dispara el TimeoutError, atrapado localmente por el Widget Documental, pintando "Analizando en segundo plano...".
9. isk-summary termina en milisegundos y pinta la tabla de Riesgo Tributario exitosamente.
10. ledger termina y pinta su tabla.

**Conclusión del Grafo Después:**
Un flujo orquestado, asíncrono y resiliente a cuellos de botella del backend, sin duplicidad, y con estados de UI precisos.
