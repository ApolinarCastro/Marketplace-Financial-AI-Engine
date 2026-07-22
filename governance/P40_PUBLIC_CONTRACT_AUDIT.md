# P40 FASE 2 — Public Contract Audit

> **Propósito**: Verificar que cada capacidad requerida por el Evidence Orchestrator esté disponible mediante **contratos públicos existentes** en FinancialEngine/LedgerEngine/ReconciliationEngine/CertificationEngine. Solo si es **imposible** mediante APIs públicas se abre un RFC.

**P37 R1**: El producto es la evidencia. Este documento no es una auditoría administrativa — es la verificación técnica previa a la implementación. Si un gap es diseño o documentación, se corrige en el código del Orchestrator sin RFC. Si un gap es REAL, se abre RFC mínimo.

---

## 1. Public Contract Matrix

### 1.1 EvidenceLinkRegistry

| # | Capacidad | Engine | Método Público | Status |
|---|-----------|--------|----------------|--------|
| L1 | Resolver por `id_orden` → registro completo con `id_transaccion`, `folio_xml`, `financial_group`, `detalle`, `monto`, `archivo_origen` | FinancialEngine | `query_ledger(order_id=id)` — `SELECT *` con filter por `id_transaccion OR id_orden` | ✅ **AVAILABLE** |
| L2 | Resolver por `id_transaccion` → mismo registro | FinancialEngine | `query_ledger(order_id=id)` — mismo param, busca en ambos campos | ✅ **AVAILABLE** |
| L3 | Resolver por `folio_xml` → registros que comparten ese folio | FinancialEngine | `query_ledger()` NO tiene parámetro `folio_xml`. El campo existe en `SELECT *` del response pero no es filterable. | ❌ **REAL GAP** |
| L4 | Resolver por `archivo_origen` | FinancialEngine | `query_ledger()` NO tiene parámetro `archivo_origen`. | ❌ **REAL GAP** |
| L5 | Resolver por `financial_group` | FinancialEngine | `query_ledger(financial_group=...)` | ✅ **AVAILABLE** |
| L6 | Resolver por `detalle` | FinancialEngine | `query_ledger(detalle=...)` | ✅ **AVAILABLE** |
| L7 | Resolver por `marketplace` + `periodo` | FinancialEngine | `query_ledger(marketplace=mp, periodo=p)` | ✅ **AVAILABLE** |
| L8 | Paginación de resultados (offset/limit) | FinancialEngine | `query_ledger(offset=N, limit=N)` | ✅ **AVAILABLE** |
| L9 | Total de registros + suma monetaria | FinancialEngine | `query_ledger()` → `total_count`, `total_sum` en response | ✅ **AVAILABLE** |
| L10 | Filtro SIGNAL/ALL/NOISE | FinancialEngine | `query_ledger(signal_mode=...)` | ✅ **AVAILABLE** |

### 1.2 ClosingContribution

| # | Capacidad | Engine | Método Público | Status |
|---|-----------|--------|----------------|--------|
| C1 | Obtener cierre de un periodo específico | FinancialEngine | `query_cierre(marketplace, periodo)` → dict con `resultado_neto`, `total_ingresos`, `batch_id`, etc. | ✅ **AVAILABLE** |
| C2 | Obtener último cierre disponible | FinancialEngine | `query_cierre(marketplace)` → LIMIT 1 DESC | ✅ **AVAILABLE** |
| C3 | Obtener todos los cierres | FinancialEngine | `query_cierre_all()` → lista completa | ✅ **AVAILABLE** |
| C4 | Determinar si una transacción participa en el cierre operacional | FinancialEngine | `query_ledger(operational_only=True)` → `include_in_operational_pnl` en response | ✅ **AVAILABLE** |
| C5 | Obtener reconciliación por marketplace + periodo | ReconciliationEngine | `validate_marketplace_consistency(marketplace, periodo)` → reconciliation delta, status, 5 levels | ✅ **AVAILABLE** |
| C6 | Obtener reconciliación de todos los marketplaces | ReconciliationEngine | `validate_all_marketplaces(periodo)` → dict por MP | ✅ **AVAILABLE** |
| C7 | Obtener certificación formal | CertificationEngine | `certify(marketplace, periodo)` → status, pass_rate, 6 claims | ✅ **AVAILABLE** |
| C8 | Verificar si financial structure está lista | FinancialEngine | `is_financial_structure_ready(marketplace, periodo)` → bool | ✅ **AVAILABLE** |
| C9 | Obtener periodos disponibles | FinancialEngine | `list_periods()` → lista `[{value, label}]` | ✅ **AVAILABLE** |
| C10 | Resolver rango de fechas de un periodo | FinancialEngine | `resolve_period_range(periodo)` → `(start, end, label)` | ✅ **AVAILABLE** |

### 1.3 CashTrace

| # | Capacidad | Engine | Método Público | Status |
|---|-----------|--------|----------------|--------|
| T1 | Obtener settlement_id para una orden | Ninguno | No existe en DB. Datos no cargados. | ❌ **STRUCTURAL GAP** |
| T2 | Obtener monto liquidado | Ninguno | Liberaciones existe como archivo RAW pero no en DB. | ❌ **STRUCTURAL GAP** |
| T3 | Obtener pago real vs contable | Ninguno | Diferencia PosCobro vs Liberaciones documentada pero no en DB. | ❌ **STRUCTURAL GAP** |
| T4 | Obtener depósito bancario | Ninguno | No integrado. | ❌ **STRUCTURAL GAP** |
| T5 | Verificar estado de cobro | FinancialEngine | `query_cierre().resultado_neto` — RN = disponible según certificación DEC-001. Solución parcial. | ✅ **PARCIAL** |

### 1.4 CoverageAnalyzer

| # | Capacidad | Engine | Método Público | Status |
|---|-----------|--------|----------------|--------|
| V1 | Contar registros crudos en ledger | LedgerEngine | `get_ledger_records_count(marketplace, periodo)` → int | ✅ **AVAILABLE** |
| V2 | Contar registros clasificados | FinancialEngine | `get_financial_records_count(marketplace, periodo)` → int | ✅ **AVAILABLE** |
| V3 | Verificar cobertura 100% de clasificación | CertificationEngine | `certify().claims` → claim `CLASSIFICATION_COVERAGE` + PASS/FAIL | ✅ **AVAILABLE** |
| V4 | Obtener KPIs certificados por MP | FinancialEngine | `query_exec_summary(marketplace, periodo)` → gross, returns, costs, net | ✅ **AVAILABLE** |
| V5 | Obtener breakdown de cobros | FinancialEngine | `query_cobros_breakdown(marketplace, periodo)` → breakdown por concepto | ✅ **AVAILABLE** |
| V6 | Obtener waterfall completo | FinancialEngine | `query_waterfall(marketplace, periodo)` → ing+dev+cost+com+ajust+neto | ✅ **AVAILABLE** |
| V7 | Obtener inteligencia operacional | FinancialEngine | `query_operational_intelligence(marketplace, periodo)` → risk, opportunity, driver, anomaly | ✅ **AVAILABLE** |
| V8 | Obtener registros de auditoría | FinancialEngine | `query_audit(marketplace, check_name, offset, limit)` → alertas | ✅ **AVAILABLE** |
| V9 | Verificar reconciliation status | ReconciliationEngine | `validate_marketplace_consistency().metrics.certification_status` | ✅ **AVAILABLE** |
| V10 | Verificar taxonomy coverage % | ReconciliationEngine | `validate_marketplace_consistency().taxonomy_coverage` | ✅ **AVAILABLE** |
| V11 | Verificar document coverage % | ReconciliationEngine | `validate_marketplace_consistency().document_coverage` | ✅ **AVAILABLE** |
| V12 | Verificar orphan records | ReconciliationEngine | `validate_marketplace_consistency().orphan_records` | ✅ **AVAILABLE** |

### 1.5 GapAnalyzer

| # | Capacidad | Engine | Método Público | Status |
|---|-----------|--------|----------------|--------|
| G1 | Listar gaps activos por marketplace | CoverageAnalyzer | CoverageAnalyzer.run() → #V# metrics + comparación contra cadena ideal | ✅ **DESIGN** |
| G2 | Obtener alertas de auditoría | FinancialEngine | `query_audit(marketplace)` → lista de alertas activas | ✅ **AVAILABLE** |
| G3 | Verificar certificación actual | CertificationEngine | `certify(marketplace, periodo)` → status, pass_rate | ✅ **AVAILABLE** |
| G4 | Verificar reconciliation actual | ReconciliationEngine | `validate_marketplace_consistency().metrics.reconciliation_delta` | ✅ **AVAILABLE** |
| G5 | Detectar periodos faltantes | FinancialEngine | `list_periods()` + `query_cierre(marketplace)` — periodos sin cierre | ✅ **AVAILABLE** |
| G6 | Detectar marketplaces sin datos | FinancialEngine | `is_financial_structure_ready(marketplace)` → bool | ✅ **AVAILABLE** |
| G7 | Calcular cobertura DTE (#V#) | CoverageAnalyzer | `query_ledger()` contiene `folio_xml` en cada row — count con/sin folio | ✅ **DESIGN** |
| G8 | Detectar si existe evidencia (Ledger + RAW + XML) | FinancialEngine | `get_financial_records_count()` + `query_ledger(archivo_origen=...)` — NO hay método para RAW/XML | ❌ **DESIGN GAP** |

---

## 2. Gap Classification

### 2.1 Gaps identificados

| ID | Capacidad faltante | Tipo | Explicación |
|----|-------------------|------|-------------|
| FG-1 | `folio_xml` no es filterable en `query_ledger()` | **REAL GAP** | `query_ledger()` retorna `folio_xml` en `SELECT *` pero no tiene parámetro `folio_xml` para filtrar. Para buscar por folio, el Orchestrator debería descargar todas las filas del marketplace+periodo y filtrar en memoria — no escala (ML = 101K rows). |
| FG-2 | `archivo_origen` no es filterable en `query_ledger()` | **REAL GAP** | Misma situación que FG-1. `archivo_origen` está en la respuesta pero no como filtro. Necesario para RAW→ETL tracing. |
| FG-3 | CashTrace — no existe settlement/pago/banco en DB | **STRUCTURAL GAP** | No es un gap de contrato público. Es un gap de datos. Ningún método público puede resolverlo porque los datos no existen. CashTrace queda como diseño. |
| FG-4 | Validación de evidencia RAW/XML no expuesta | **DESIGN GAP** | El Orchestrator puede medir cobertura usando datos existentes (get_financial_records_count, get_ledger_records_count, folio_xml coverage desde query_ledger). La validación de existencia de archivos RAW en disco es operacional, no financiera. El Orchestrator NO necesita verificar archivos RAW directamente — usa cobertura documental desde ReconciliationEngine. |
| FG-5 | No existe método `get_dte_info(folios)` | **DESIGN GAP** | El Orchestrator no necesita DTE info (tipo_dte, monto_total, emisor) para su función principal de traceo. La columna `folio_xml` en el ledger es suficiente para responder "¿este folio existe en el ledger?". DTE info detallado pertenece a DTEIndexer, no al Evidence Orchestrator. |

### 2.2 Gaps REALES (requieren RFC)

| RFC | Gap | Capacidad requerida | Solución propuesta (mínima) |
|-----|-----|---------------------|----------------------------|
| RFC-040 | FG-1 | Filtrar ledger por `folio_xml` | Agregar parámetro `folio_xml: str | None` a `FinancialEngine.query_ledger()` — 1 línea de lógica |
| RFC-040 | FG-2 | Filtrar ledger por `archivo_origen` | Agregar parámetro `archivo_origen: str | None` a `FinancialEngine.query_ledger()` — 1 línea de lógica |

### 2.3 Gaps DESIGN (no requieren RFC)

| Gap | Razón | Cómo lo resuelve el Orchestrator |
|-----|-------|----------------------------------|
| FG-3 CashTrace | Los datos no existen en DB. Ningún contrato puede resolverlo. | CashTrace queda como contratos vacíos — retorna `NO_DISPONIBLE` para todos los campos de cash. El gap está documentado. |
| FG-4 Validación evidencia | El Orchestrator no necesita verificar archivos RAW en disco. La cobertura documental existe via `ReconciliationEngine.validate_marketplace_consistency().document_coverage`. | CoverageAnalyzer usa `document_coverage` + `get_financial_records_count()` + `get_ledger_records_count()` + `certify().claims[CLASSIFICATION_COVERAGE]` |
| FG-5 DTE info detallado | El Orchestrator solo necesita saber si un `folio_xml` existe en el ledger. No necesita `tipo_dte`, `emisor`, etc. | `query_ledger()` retorna `folio_xml` en cada registro. CoverageAnalyzer puede calcular `% con folio_xml vs sin folio_xml`. |

### 2.4 Gaps DOCUMENTATION (no requieren RFC)

Ninguno detectado. Todos los parámetros documentados de `query_ledger()` coinciden con su implementación real.

---

## 3. RFC-040 — Scope mínimo

### Qué cambia

**FinancialEngine.query_ledger()** — agregar 2 parámetros opcionales:

```python
def query_ledger(
    self,
    marketplace: str = "ML",
    periodo: str | None = None,
    financial_group: str | None = None,
    clasificacion_operativa: str | None = None,
    detalle: str | None = None,
    order_id: str | None = None,
    folio_xml: str | None = None,        # NUEVO
    archivo_origen: str | None = None,   # NUEVO
    offset: int = 0,
    limit: int = 200,
    filter_zero: bool = True,
    operational_only: bool = True,
    signal_mode: str = "ALL",
) -> dict[str, Any]:
```

**Lógica a agregar** (después de línea 391, antes de `if operational_only:`):

```python
if folio_xml:
    conditions.append("folio_xml = ?")
    params.append(folio_xml)

if archivo_origen:
    conditions.append("archivo_origen = ?")
    params.append(archivo_origen)
```

### Qué NO cambia

- `query_ledger()` response: igual (`SELECT *` con `folio_xml` y `archivo_origen` ya incluidos)
- Otros métodos de FinancialEngine: **0 cambios**
- LedgerEngine: **0 cambios**
- ReconciliationEngine: **0 cambios**
- CertificationEngine: **0 cambios**
- DEC-019: **preservada** (folio_xml y archivo_origen son columnas existentes, no afectan `include_in_operational_pnl`)
- Single Financial Truth: **preservada**
- API endpoints: **0 cambios** (el Orchestrator consume FinancialEngine directamente)

### Líneas totales

- 2 parámetros agregados
- 6 líneas de lógica condicional
- **Total: ~8 líneas en 1 archivo**

---

## 4. Conclusión

| Tipo | Cantidad |
|------|----------|
| Capacidades disponibles mediante contratos públicos | **30/35 (85.7%)** |
| Gaps REALES (requieren RFC) | **2** (FG-1, FG-2) |
| Gaps DESIGN (no requieren RFC) | **3** (FG-3, FG-4, FG-5) |
| Gaps DOCUMENTATION | **0** |
| RFCs necesarios | **1** (RFC-040: 2 parámetros en FinancialEngine.query_ledger()) |

**Veredicto**: P40 FASE 2 puede implementarse con **1 RFC mínimo** de ~8 líneas. El 85.7% de las capacidades ya están disponibles mediante contratos públicos existentes. CashTrace queda como diseño (structural gap). Evidence validation se resuelve con datos existentes sin nuevo código.

Sin RFC-040, el Orchestrator puede funcionar pero NO podrá trazar por `folio_xml` ni `archivo_origen`. El traceo solo funcionaría desde `id_orden`/`id_transaccion`. Esto es suficiente para el MVP del Orchestrator.
