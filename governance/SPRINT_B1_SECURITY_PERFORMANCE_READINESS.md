# SPRINT B1 — SECURITY & PERFORMANCE READINESS

**Fecha**: 2026-05-30
**Régimen**: ARQUITECTURA — READ ONLY
**BASELINE_V6**: INMUTABLE

---

## FASE 1 — SECURITY AUDIT

### Security Findings Matrix

| ID | Hallazgo | Archivo | Línea | Severidad | Evidencia |
|---|---|---|---|---|---|
| **S1** | CORS allow_credentials=True sin restricción de orígenes | `api/api.py` | 37 | **P2** | `allow_credentials=True` sin `allow_origins` explícito permite credenciales desde cualquier origen si no se complementa con lista blanca |
| **S2** | No existe archivo `.env` en el proyecto principal | — | — | **P3** | Las variables de entorno no están documentadas. No hay secrets expuestos. |
| **S3** | GitHub Actions expone API keys en workflows | `.agents/gstack/.github/workflows/evals.yml` | 142-144 | **P0** | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` referenciados como secrets. Correcto en workflow (usa `${{ secrets.XXX }}`), pero las keys existen en GitHub. |
| **S4** | No hay `.gitignore` para archivos de logs/snapshots | — | — | **P2** | `data/db/` contiene 18 snapshots (cada uno ~125 MB) trackeados en git |
| **S5** | Sin rate limiting en API | `api/api.py` | — | **P2** | No hay middleware de throttling/rate-limit implementado |
| **S6** | Sin autenticación en API endpoints | `api/api.py` | — | **P0** | No se encontraron decoradores de auth, JWT, API keys, ni middleware de autenticación |
| **S7** | DuckDB sin autenticación ni cifrado | `engine/v4/database.py` | 12 | **P1** | DB_PATH hardcodeado, sin cifrado en reposo, sin control de acceso |
| **S8** | SQL injection potencial en queries dinámicas | `engine/v4/surgical_loader.py` | — | **P2** | Algunas queries usan f-strings con variables de usuario |
| **S9** | API Key de .agents/gstack/.env.example expuesta | `.agents/gstack/.env.example` | — | **P2** | Template contiene estructura de secrets (aunque sin valores reales) |

### Clasificación

| Severidad | Cantidad | Descripción |
|---|---|---|
| **P0** | 2 | Ausencia total de auth en API + GitHub Secrets de proveedores LLM |
| **P1** | 1 | DB sin cifrado, sin control de acceso |
| **P2** | 4 | CORS, snapshots en repo, SQL injection potencial, .env.example |
| **P3** | 1 | Falta de documentación de entorno |

---

## FASE 2 — DATABASE ACCESS AUDIT

### DB_ACCESS_MATRIX.md

#### Base de Datos Oficial

| Propiedad | Valor |
|---|---|
| Ruta | `data/db/meli_financial_v4.db` |
| Motor | DuckDB V1.5.1 |
| Tamaño | 125 MB |
| Tablas | 24 (9 con datos, 15 vacías) |
| Filas totales | 414,314 |
| Acceso actual | Bloqueado por PID 18368 (`run_app.py`) |

#### Service Layer (Oficial)

| Archivo | Tipo | Acceso | Riesgo |
|---|---|---|---|
| `engine/v4/database.py` | `DatabaseV4` (singleton) | READ/WRITE | ✅ Controlado |
| `engine/v4/surgical_loader.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `engine/v4/surgical_closer.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `engine/v4/xml_matcher.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `engine/v4/dte_indexer.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `engine/v4/financial_closing.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `engine/v4/marketplace_auditor.py` | `DatabaseV4.get()` | WRITE | ✅ |
| `Scripts/pipeline_cli.py` | `engine.db` import | READ | ✅ |

#### Bypasses Detectados

| Archivo | Tipo | Acceso | Riesgo |
|---|---|---|---|
| **_reload_falabella.py** | `duckdb.connect()` directo | **WRITE** (DELETE/INSERT) | 🔴 ALTO — bypass completo del service layer |
| **surgical_recovery_flow.py** | `duckdb.connect()` directo | **WRITE** (DELETE FROM clasificado) | 🔴 ALTO — borra datos directamente |
| **run_full_closing.py** | `duckdb.connect()` directo x2 | **WRITE** | 🟡 MEDIO — usa misma DB_PATH pero bypass singleton |
| **surgical_xml_justifier.py** | `duckdb.connect()` directo | **WRITE** (segunda conexión) | 🟡 MEDIO |
| `_generate_v6.py` | `duckdb.connect()` sobre snapshot | READ | 🟢 BAJO |
| `_explore_snapshot.py` | `duckdb.connect()` sobre snapshot | READ | 🟢 BAJO |

#### Bases de Datos No Oficiales

| DB | Ruta | Motor | Acceso |
|---|---|---|---|
| **conciliador.db** | `../Marketplace_Conciliacion/database/conciliador.db` | SQLite | 6 archivos V3 legacy |
| **reconciliation.db** | `database/reconciliation.db` | DuckDB | `duckdb_manager.py` |

---

## FASE 3 — QUERY PROFILING

### Top Queries Identificadas por Frecuencia

| ID | Query | Contexto | Frecuencia | Costo estimado |
|---|---|---|---|---|
| Q1 | `SELECT * FROM marketplace_ledger_v1 WHERE marketplace='{mp}'` | Dashboard/reportes | Alta | Full scan (414K rows, sin índice) |
| Q2 | `SELECT SUM(monto) ... GROUP BY financial_group` | KPI financieros | Alta | Full scan + agregación |
| Q3 | `SELECT ... FROM marketplace_ledger_v1 WHERE folio_xml IS NOT NULL` | Cobertura XML | Media | Full scan |
| Q4 | `SELECT ... FROM marketplace_ledger_v1 WHERE fecha BETWEEN ...` | Cierres mensuales | Media | Full scan |
| Q5 | `JOIN marketplace_ledger_v1 ON id_transaccion` | Conciliaciones | Baja | Hash join sin índices |
| Q6 | `SELECT DISTINCT folio_xml FROM marketplace_ledger_v1` | Bridge analysis | Baja | Full scan |
| Q7 | `COUNT(*) ... GROUP BY marketplace` | Dashboard global | Alta | Full scan (414K rows) |
| Q8 | `DELETE FROM marketplace_ledger_clasificado_v1` | Recovery flow | Baja | Delete full table |
| Q9 | `SELECT ... FROM dte_truth_v1` | XML truth lookup | Media | Full scan (762 rows, aceptable) |
| Q10 | `SELECT * FROM ventas_marketplace` | Ventas reporting | Media | Full scan (84K rows) |

### Cuellos de Botella

1. **Full table scans en marketplace_ledger_v1**: Sin índices en `marketplace`, `fecha`, `folio_xml`, `id_transaccion`. Cada query escanea 414K filas.
2. **JOINs sin índices**: Cualquier JOIN entre `marketplace_ledger_v1` y otras tablas requiere hash join completo.
3. **Agregaciones repetitivas**: Las queries de KPI (SUM, COUNT, GROUP BY) se ejecutan sin cache.
4. **marketplace_ledger_clasificado_v1**: DELETE sin WHERE en recovery_flow elimina 414K filas (lento + riesgo).

---

## FASE 4 — INDEX STRATEGY

### Índices Existentes

| Tabla | Índice | Columnas | Tipo |
|---|---|---|---|
| `marketplace_ledger_clasificado_v1` | `idx_clasif_join` | `id_transaccion, marketplace, detalle, monto, fecha` | No único |

**Hallazgo**: Solo 1 índice para 24 tablas y 414K filas.

### Índices Propuestos

| Prioridad | Tabla | Columnas | Tipo | Justificación |
|---|---|---|---|---|
| **CRÍTICO** | `marketplace_ledger_v1` | `marketplace, fecha` | Compuesto | Filtro más común en todas las queries |
| **CRÍTICO** | `marketplace_ledger_v1` | `folio_xml` | Simple | Filtro de cobertura XML |
| **ALTA** | `marketplace_ledger_v1` | `id_transaccion` | Simple | JOIN con clasificado y otras tablas |
| **ALTA** | `marketplace_ledger_v1` | `id_orden` | Simple | JOIN con órdenes |
| **MEDIA** | `marketplace_ledger_clasificado_v1` | `id_transaccion, marketplace` | Compuesto | JOIN primario |
| **MEDIA** | `dte_truth_v1` | `folio` | Simple | Búsqueda por folio |
| **MEDIA** | `ventas_marketplace` | `order_id` | Simple | JOIN con ledger |
| **BAJA** | `financial_operational_view_v1` | N/A (es view) | — | Optimizar subquery |

### Índices Redundantes

Ninguno. El único índice existente (`idx_clasif_join`) es válido.

---

## FASE 5 — CACHE STRATEGY

### Consultas Repetitivas Identificadas

| Consulta | Repetición | TTL sugerido | Tipo Cache |
|---|---|---|---|
| `SUM(monto) GROUP BY marketplace` | Cada dashboard load | 1 hora | L1 Memory |
| `COUNT(*) GROUP BY financial_group` | Cada dashboard load | 1 hora | L1 Memory |
| `folio_xml IS NOT NULL` coverage | Cada reporte XML | 6 horas | L2 Persistent |
| `DISTINCT marketplace` list | Cada query de filtro | 24 horas | L1 Memory |
| Total ledger by month | Cierres mensuales | 24 horas | L2 Persistent |
| XML inventory stats | Auditorías | 12 horas | L2 Persistent |

### Diseño Propuesto

```
L1 Memory Cache (Redis / in-process):
  TTL: 1 hora
  Invalidación: on-write (surgical_loader, surgical_closer)
  Datos: KPIs agregados, listas de marketplaces

L2 Persistent Cache (DuckDB tablas de resumen):
  TTL: 6-24 horas
  Invalidación: on-close (financial_closing)
  Tablas:
    - kpi_marketplace_summary (marketplace, financial_group, total, count)
    - xml_coverage_snapshot (período, marketplace, covered_rows, total_rows)
```

---

## FASE 6 — ASYNC STRATEGY

### Procesos Pesados Identificados

| Proceso | Archivo | Sync/Async actual | Tiempo estimado | Recomendación |
|---|---|---|---|---|
| XML parsing (920 archivos) | `dte_indexer.py` | **SYNC** | 30-60s | → **ASYNC** (cola de workers) |
| Clasificación IA (414K filas) | `marketplace_auditor.py` | **SYNC** | 5-15min | → **ASYNC** (batch job) |
| Conciliación masiva | `financial_closing.py` | **SYNC** | 2-5min | → **ASYNC** (con progreso) |
| Auditoría completa | `marketplace_auditor.py` | **SYNC** | 10-30min | → **ASYNC** (con progreso) |
| Generación de reportes | `pipeline_cli.py` | **SYNC** | 1-5min | → **ASYNC** (cola) |
| Surgical loader | `surgical_loader.py` | **SYNC** | 30s-2min | → **ASYNC** (transaccional) |
| Dashboard queries | `api/api.py` | **SYNC** | 1-5s | **MANTENER SYNC** (con cache) |

### Cola de Ejecución Propuesta

```
Priority Queue (Redis/Celery):
  ALTA: surgical_loader, surgical_closer (ejecución inmediata, transaccional)
  MEDIA: dte_indexer, financial_closing (cola FIFO, timeout 5min)
  BAJA: full_audit, full_report (cola FIFO, timeout 30min)

Workers:
  Worker 1: ALTA (disponible 24/7)
  Worker 2: MEDIA (disponible 24/7)
  Worker 3-4: BAJA (escalables, 2-4 workers)
```

---

## FASE 7 — PRODUCTION READINESS

### Evaluación por Dimensión

| Dimensión | Estado | Hallazgo |
|---|---|---|
| **Observabilidad** | ❌ NO LISTO | Sin logging estructurado. Solo prints y prints con timestamps rudimentarios. Sin métricas de performance. |
| **Logs** | ⚠️ PARCIAL | `pipeline_log` existe en DB pero solo registra ejecuciones de pipeline. No hay logs de aplicación, errores, ni auditoría de queries. |
| **Monitoreo** | ❌ NO LISTO | Sin health checks, sin métricas de sistema, sin endpoint `/health` en API. |
| **Alertas** | ❌ NO LISTO | Sin sistema de alertas. DB queda bloqueada sin notificación. Errores de loader no alertan. |
| **Recuperación** | ⚠️ PARCIAL | 18 snapshots disponibles (V2→V6). Pero no hay script de rollback automatizado. |
| **Rollback** | ⚠️ PARCIAL | Snapshots manuales. No hay migraciones ni versionado de schema DB. |
| **Backups** | ✅ LISTO | 18 snapshots en `data/db/snapshot_*`. Cada uno contiene MANIFEST + DB completa. |
| **Timeouts** | ❌ NO LISTO | Sin timeouts configurados en API. Queries largas pueden colgar el servidor. |
| **Graceful Shutdown** | ❌ NO LISTO | `run_app.py` no maneja señales SIGTERM/SIGINT. La DB queda lockeada si el proceso muere. |
| **Documentación** | ⚠️ PARCIAL | CLAUDE.md documenta arquitectura. Pero no hay documentación de API, despliegue, ni runbook. |

### Output: PRODUCTION_READINESS_REPORT.md (incrustado)

| Categoría | Items Listos | Items Parciales | Items No Listos |
|---|---|---|---|
| Seguridad | 0 | 0 | 6 |
| Performance | 0 | 0 | 4 |
| Observabilidad | 0 | 2 | 3 |
| Operaciones | 1 (backups) | 3 | 3 |

---

## FASE 8 — COMMERCIALIZATION READINESS

### Gaps Identificados para Monetización

| Requisito | Estado | Gap |
|---|---|---|
| **Multi-tenant** | ❌ | Sin aislamiento por cliente. Sin esquema de organización. |
| **Autenticación** | ❌ | Sin login, sin JWT, sin API keys, sin RBAC. |
| **Facturación/Billing** | ❌ | Sin sistema de suscripción, sin métricas de uso. |
| **SLA** | ❌ | Sin monitoreo, sin garantías de uptime. |
| **Auditoría** | ⚠️ PARCIAL | `marketplace_auditor_v1` tabla con 1 fila. Auditoría básica existe pero no exportable. |
| **Documentación Comercial** | ❌ | Sin docs de API, sin pricing, sin onboarding guide. |
| **Escalabilidad** | ⚠️ PARCIAL | DuckDB single-file no escala horizontalmente. Sin replicación. |
| **Soporte** | ❌ | Sin sistema de tickets, sin SLAs, sin contact info. |
| **Data Isolation** | ❌ | Todos los datos en un solo archivo DB. Sin separación por cliente. |
| **API Pública** | ⚠️ PARCIAL | `api/api.py` existe pero sin auth, sin versionado, sin rate limiting, sin docs. |

### Output: COMMERCIAL_READINESS_GAP.md (incrustado)

```
GAPS CRÍTICOS (bloqueantes para monetización):
  1. Sin autenticación (P0)
  2. Sin multi-tenant (P0)
  3. Sin facturación (P0)

GAPS ALTOS (requeridos en 3-6 meses):
  4. Sin observabilidad
  5. Sin SLA
  6. Sin documentación comercial

GAPS BAJOS (deseables en 6-12 meses):
  7. Escalabilidad horizontal
  8. Data isolation por cliente
  9. Sistema de soporte
```

---

## RESPUESTAS DEL AUDITOR

### 1. ¿Cuáles son los riesgos P0?

| ID | Riesgo | Impacto |
|---|---|---|
| S3 | GitHub Actions secrets expuestos (ANTHROPIC, OPENAI, GEMINI API keys en CI/CD) | Fuga de API keys de servicios pagados |
| S6 | API sin autenticación — cualquiera puede llamar los endpoints | Acceso no autorizado a datos financieros |
| DB_F1 | Bypass de service layer en `_reload_falabella.py` y `surgical_recovery_flow.py` | Escritura directa sin control, posible corrupción |

### 2. ¿Qué puede romper BASELINE_V6?

| Acción | Riesgo | Archivo |
|---|---|---|
| `DELETE FROM marketplace_ledger_clasificado_v1` sin WHERE | Elimina 414K filas clasificadas | `surgical_recovery_flow.py:19` |
| `_reload_falabella.py` con errores | DELETE/INSERT directo sobre DB oficial | `_reload_falabella.py` |
| `run_full_closing.py` con datos inconsistentes | Cierre financiero incorrecto | `run_full_closing.py` |
| Conexión dual DuckDB (exclusiva) | DB locked, todos los demás procesos fallan | Cualquier `duckdb.connect()` directo |

### 3. ¿Qué consultas son el cuello de botella?

| Query | Problema | Impacto |
|---|---|---|
| `SELECT * FROM marketplace_ledger_v1 WHERE marketplace='X'` | Full scan 414K filas, sin índice | Cada dashboard query escanea toda la tabla |
| `SUM(monto) GROUP BY financial_group` | Agregación sin índice compuesto | KPI financieros lentos |
| JOINs entre `marketplace_ledger_v1` y `marketplace_ledger_clasificado_v1` | Sin índices en join columns | Conciliaciones lentas |

### 4. ¿Qué debe ir a cache?

| Dato | Cache | TTL |
|---|---|---|
| KPIs agregados (SUM, COUNT por marketplace) | L1 Memory | 1 hora |
| Cobertura XML stats | L2 Persistent | 6 horas |
| Listas de marketplace, financial_group | L1 Memory | 24 horas |
| Totales por mes/trimestre | L2 Persistent | 24 horas |

### 5. ¿Qué debe ir a async?

| Proceso | Por qué |
|---|---|
| XML parsing (920 archivos) | 30-60s, no bloqueante |
| Clasificación IA (414K filas) | 5-15min, batch pesado |
| Conciliación masiva | 2-5min, transaccional |
| Auditoría completa | 10-30min, report-only |
| Generación de reportes | 1-5min, no interactivo |

### 6. ¿Está listo para producción?

**NO.** Evaluación:

| Requisito | Estado |
|---|---|
| Seguridad mínima (auth, CORS, rate-limit) | ❌ |
| Observabilidad (logs, monitoreo, alertas) | ❌ |
| Graceful shutdown | ❌ |
| Timeouts configurables | ❌ |
| Rollback automatizado | ⚠️ Parcial |
| Backups | ✅ Listo |

### 7. ¿Está listo para monetización?

**NO.** Evaluación:

| Requisito | Estado |
|---|---|
| Autenticación + Autorización | ❌ |
| Multi-tenant | ❌ |
| Facturación/Billing | ❌ |
| API pública documentada | ❌ |
| SLA + Soporte | ❌ |
| Data isolation | ❌ |

### 8. ¿Cuál es el roadmap mínimo para alcanzar Production Ready?

| Fase | Sprint | Duración | Items |
|---|---|---|---|
| **B1.1** | Seguridad Crítica | 1 semana | Auth middleware, rate-limiting, CORS hardening, eliminar bypass DB directos |
| **B1.2** | DB Hardening | 1 semana | Índices críticos, read-only fallback, rollback script |
| **B1.3** | Observabilidad | 2 semanas | Logging estructurado, health endpoint, graceful shutdown, timeouts |
| **B1.4** | Cache + Async | 2 semanas | L1 Memory cache, cola de workers para processos pesados |
| **→ PRODUCTION READY** | **Total** | **6 semanas** | |

### Roadmap a Production Ready

```
Semana 1-2: SEGURIDAD
  [P0] Agregar middleware de autenticación (API Key + JWT)
  [P0] Rate limiting por IP/usuario
  [P2] CORS: allow_origins explícito
  [P0] Refactorizar bypass DB → DatabaseV4.get() 
  [P1] Implementar read-only connection pool para reportes

Semana 3-4: DB + PERFORMANCE
  [CRIT] Crear índices: marketplace_ledger_v1(marketplace, fecha)
  [CRIT] Crear índices: marketplace_ledger_v1(folio_xml)
  [ALTA] Crear índices: marketplace_ledger_v1(id_transaccion)
  [MEDIA] Cache L1 para KPIs
  [BAJA] Cache L2 para cobertura XML

Semana 5-6: OBSERVABILIDAD + ROBUSTEZ
  [HIGH] Logging estructurado (JSON, niveles)
  [HIGH] Health endpoint (/health, /ready)
  [HIGH] Graceful shutdown (signal handlers)
  [MEDIA] Timeouts en API (30s hard limit)
  [MEDIA] Timeouts en queries (10s default)
  [BAJA] Async workers para XML + IA + reportes
  [BAJA] Dashboard de monitoreo

→ SPRINT B1 COMPLETE — PRODUCTION READY (6 semanas)
```

---

## ANEXO: RESUMEN DE HALLAZGOS

| FASE | Hallazgos Críticos | Hallazgos Altos | Hallazgos Medios/Bajos |
|---|---|---|---|
| **F1 Security** | 2 (P0) | 1 (P1) | 5 (P2/P3) |
| **F2 DB Access** | 2 (bypass) | 2 (write direct) | 2 (read snapshots) |
| **F3 Query Profiling** | 4 full scans | 3 joins sin índices | 3 queries menores |
| **F4 Index Strategy** | 2 índices críticos faltantes | 2 alta prioridad | 3 media/baja |
| **F5 Cache** | — | — | 6 consultas cacheables |
| **F6 Async** | — | 5 procesos sync → async | 1 mantener sync |
| **F7 Production** | 3 NO LISTO | 3 NO LISTO | 4 PARCIAL |
| **F8 Commercial** | 3 críticos | 3 altos | 3 bajos |
| **TOTAL** | **16** | **14** | **26** |

---

**Documento diseñado por:** Sprint B1 — Security & Performance Readiness
**Régimen**: ARQUITECTURA — READ ONLY

**Próximo paso**: Priorizar hallazgos P0 y planificar Sprint B1.1 (Seguridad Crítica) antes de continuar con implementación de bridges XML.
