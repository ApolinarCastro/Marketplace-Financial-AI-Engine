# MATRIZ MAESTRA DE REMEDIACIÓN — BASELINE V6

Generado: 2026-05-30
Fuentes: 8 auditorías forenses (Data, Reproducibilidad, XML, Dead Code, Performance, Seguridad, Observabilidad, Production Readiness)
Trust Score V1: 54.1/100 | Production Readiness: 18.75/100 | Audit Ready: NO

---

## RESUMEN EJECUTIVO

| Métrica | Hoy | Post-Fase A | Post-Fase D |
|---|---|---|---|
| Trust Score | 54.1/100 | ~78/100 | ~92/100 |
| Production Readiness | 18.75/100 | ~40/100 | ~85/100 |
| Audit Ready | NO | SÍ (condicional) | SÍ |
| $ con XML respaldo | 56% | ~85% | ~95%+ |
| Clasificación financiera | ~66% | ~95% | 100% |
| Riesgo de pérdida datos | ALTO | BAJO | MÍNIMO |

---

## 1. HALLAZGOS CONSOLIDADOS (45 únicos, deduplicados)

### Leyenda
- **ID**: Identificador único
- **Área**: DATA / REPRO / XML / DEAD / PERF / SEC / OBS / INFRA / TEST / DOCS
- **P**: P0-P3 (ver clasificación)
- **E**: Esfuerzo (XS/S/M/L/XL)
- **R**: Riesgo implementación (B/M/A)
- **Dep**: Dependencia (ID que debe resolverse antes)

| ID | Hallazgo | Área | P | E | R | Dep | Trust Δ | Audit Δ | Prod Δ |
|---|---|---|---|---|---|---|---|---|---|
| H01 | 7 facturas RIPLEY no cargadas ($50.5M): 582603, 584269, 586105, 587807, 589546, 591235, 592974 | DATA | P0 | M | B | — | +3-5 | +5-8 | +2 |
| H02 | 13 tablas obsoletas en schema (54% dead schema) | DATA/DEAD | P2 | M | M | — | +2 | +2 | +1 |
| H03 | RIPLEY 8,413 rows ($142M) financial_group=NULL (100% no clasificado) | DATA | P0 | M | M | H06 | +8-12 | +10 | +5 |
| H04 | FALABELLA 1,008 rows financial_subgroup=NULL 100% | DATA | P1 | S | B | H05 | +2 | +3 | +2 |
| H05 | marketplace_auditor.py NUNCA escribe financial_subgroup (código definido pero no ejecutado) | DEAD | P1 | S | B | — | +2 | +2 | +2 |
| H06 | RIPLEY loader (load_ripley) MUERTO — glob *.xlsx encuentra 0 archivos | REPRO | P0 | L | M | — | +5-8 | +10-15 | +3 |
| H07 | ML DTEIndexer path roto: `ML/Facturacion/` no existe | REPRO | P1 | XS | B | — | +2 | +5 | +1 |
| H08 | No existe repositorio git — sin historial, sin rollback, sin branching | INFRA/REPRO | P0 | M | B | — | +5-8 | +15-20 | +10-15 |
| H09 | ~100 rutas absolutas hardcoded (10 activas en 7 módulos activos) | REPRO | P0 | L | M | H08 | +3-5 | +10 | +10 |
| H10 | Pipeline CI/CD (.github/workflows/ci.yml) FALLARÁ en CI — sin snapshot DB, rutas absolutas | INFRA/REPRO | P1 | M | B | H08, H09 | +1 | +5 | +10-15 |
| H11 | 3 módulos violan patrón singleton DB (xml_justifier, recovery_flow, run_full_closing) | REPRO/PERF | P1 | S | B | — | +1 | +3 | +5 |
| H12 | RIPLEY XML: 0% trazabilidad (100 XML ECCSA, sin soporte DTEIndexer, $25.5M) | XML | P0 | L | M | H06, H16 | +5-8 | +10 | +3 |
| H13 | PARIS XML: 0% HOY (154 XMLs 100% parseables, 78.8% potencial vía Excel bridge, $297.8M) | XML | P0 | M | B | H16 | +10-15 | +15-20 | +5 |
| H14 | ML XML: 89.4% folio_xml (88,323 CERTIFICADO), ~10.6% faltante (10,789 rows, ~$40-80M) | XML | P2 | M | B | H07, H16 | +3-5 | +5 | +2 |
| H15 | FALABELLA XML: 61.5% folio_xml, 0% CERTIFICADO (387 rows sin folio) | XML | P2 | S | B | H16 | +2 | +3 | +1 |
| H16 | DTEIndexer/XMLJustifier CONFIRMADO standalone — NO integrados al pipeline. Solo ML procesado manualmente | XML/REPRO | P0 | L | M | — | +10-15 | +20-25 | +5 |
| H17 | $663M de $1,508M (44%) NO tiene respaldo XML demostrable | XML | P0 | — | — | H12-H16 | — | — | — |
| H18 | financial_closing.py referencia tablas que NO EXISTEN (meli_ledger_v1, meli_payouts) — código legacy muerto | DEAD | P2 | S | B | — | +1 | +1 | +1 |
| H19 | 34 root _*.py + 137 scratch/*.py — código exploratorio sin integrar | DEAD | P3 | M | B | — | 0 | 0 | 0 |
| H20 | vw_dashboard_kpis no funcional — consulta order_reconciliation (0 rows) | DEAD | P2 | S | B | — | +1 | +1 | +1 |
| H21 | API version metadata = "3.5" (sistema es V6) | DEAD | P3 | XS | B | — | 0 | 0 | 0 |
| H22 | /api/v4/ledger: 3 queries por request (COUNT + SELECT + DISTINCT) — podría ser 1 con ventana | PERF | P2 | S | B | — | 0 | 0 | +2 |
| H23 | /api/v4/cierre/desglose: GROUP BY 4 dimensiones sobre 414K rows sin índice | PERF | P2 | S | B | — | 0 | 0 | +2 |
| H24 | run_classification(): UPDATE propagación JOIN 414K × 414K sin índice | PERF | P2 | S | B | — | 0 | 0 | +2 |
| H25 | surgical_closer.py: DELETE+INSERT loop 48 periodos, bloquea API 30-120s | PERF | P1 | M | B | H11 | 0 | 0 | +5 |
| H26 | POST /api/v4/run-audit síncrono — bloquea API por minutos | PERF | P1 | S | B | — | 0 | 0 | +5 |
| H27 | Fallback loop Python propagación (línea 501) = HORAS si se activa | PERF | P2 | M | B | — | 0 | 0 | +2 |
| H28 | Sin cache para resultados históricos inmutables (cierres, desgloses de meses anteriores) | PERF | P2 | M | B | — | 0 | 0 | +3 |
| H29 | Sin connection pooling — DuckDB single connection con lock | PERF/REPRO | P2 | S | B | — | 0 | 0 | +2 |
| H30 | SET temp_directory en cada request (~1-5ms desperdiciado) | PERF | P3 | XS | B | — | 0 | 0 | 0 |
| H31 | API SIN autenticación — cualquiera puede acceder a /api/v4/* | SEC | P1 | M | B | — | +2 | +3 | +10-15 |
| H32 | No HTTPS — solo localhost:8004 | SEC | P1 | S | B | — | 0 | +2 | +5 |
| H33 | Sin cifrado en reposo para DB | SEC | P2 | M | B | — | 0 | +2 | +3 |
| H34 | SQL injection vía POST /api/v4/query (SQL arbitrario) | SEC | P1 | M | B | — | +2 | +5 | +10 |
| H35 | Sin rate limiting | SEC | P2 | S | B | — | 0 | +1 | +3 |
| H36 | Sin configuración CORS visible | SEC | P2 | XS | B | — | 0 | 0 | +1 |
| H37 | Sin validación de input en POST endpoints | SEC | P2 | S | B | — | 0 | +1 | +3 |
| H38 | Sin métricas / health checks | OBS | P1 | M | B | — | 0 | +2 | +8 |
| H39 | Sin alertas / notificaciones | OBS | P2 | S | B | — | 0 | +1 | +5 |
| H40 | pipeline_log = 0 rows, auditoria_v1 = 1 row (logging framework no funcional) | OBS | P1 | S | B | — | +3 | +5 | +5 |
| H41 | Sin logging estructurado | OBS | P2 | S | B | — | 0 | +1 | +3 |
| H42 | Sin monitoreo para procesos ETL | OBS | P1 | M | B | — | 0 | +3 | +8 |
| H43 | Sin configuración de entornos (dev/staging/prod) | INFRA | P1 | M | M | H08, H09 | +1 | +5 | +10 |
| H44 | Sin plan de disaster recovery / backup strategy | INFRA | P1 | M | B | H08 | +3 | +10 | +10 |
| H45 | 5 documentos contradictorios: traceability_audit_report.txt (2-3x inflado), data_state_duckdb.json (194,944 rows error), DB_PROTECTION_AUDIT.txt (V5), README.md (V4), MANIFEST_V6.json (marketplaces vacío) | DOCS | P1 | S | B | — | +3 | +5 | +3 |
| H46 | 0 cobertura de tests para RIPLEY loader, DTEIndexer, XMLJustifier | TEST | P1 | L | B | H06, H16 | +3 | +10 | +5 |
| H47 | Sin SLA/SLO definidos | OBS/INFRA | P2 | S | B | — | 0 | +2 | +5 |

---

## 2. DEPENDENCIAS ENTRE HALLAZGOS

```
H06 (RIPLEY loader muerto) ──bloquea──► H03 (RIPLEY $142M sin clasificar)
                                        H12 (RIPLEY XML 0%)
                                        H46 (test RIPLEY loader)

H08 (No git) ──bloquea──► H09 (rutas hardcoded — migrar a relative requiere git mv)
                          H10 (CI/CD — necesita git para triggers)
                          H43 (entornos — necesita branching)
                          H44 (DR — necesita git para backup de código)

H09 (hardcoded paths) ──bloquea──► H10 (CI/CD — paths absolutos no existen en CI runner)
                                    H43 (entornos — rutas fijas a C:\Users\...)

H16 (DTEIndexer standalone) ──bloquea──► H12 (RIPLEY XML 0%)
                                          H13 (PARIS XML 0%)
                                          H14 (ML XML faltante)
                                          H15 (FALABELLA XML 0% CERTIFICADO)
                                          H46 (test DTEIndexer/XMLJustifier)

H05 (mkt_auditor no escribe financial_subgroup) ──causa──► H04 (FALABELLA 100% NULL)

H11 (3 módulos violan singleton) ──agrava──► H25 (surgical_closer bloquea)

H08 + H09 (no git + paths absolutos) ──bloquean──► TODO lo que requiera portabilidad
```

### Bloques de dependencia (resolver juntos)

| Bloque | Hallazgos | Enfoque | Esfuerzo total |
|---|---|---|---|
| **BLOQUE A**: Fundación | H08 (git) + H09 (paths) + H10 (CI/CD) + H43 (entornos) + H44 (DR) | Resolver en orden: H08 → H09 → H10/H43/H44 | L-XL |
| **BLOQUE B**: RIPLEY resurrección | H06 (loader) + H03 (classif) + H12 (XML) + parte H46 (tests) | Resolver en orden: H06 → H03 → H12 | L |
| **BLOQUE C**: XML pipeline | H16 (integrar DTEIndexer) + H13 (PARIS) + H14 (ML) + H15 (FALABELLA) + H46 (tests) | H16 resuelve H13/H14/H15 simultáneamente | L |
| **BLOQUE D**: Seguridad base | H31 (auth) + H32 (HTTPS) + H34 (SQL inj) + H35 (rate) | Independientes, pueden resolverse en paralelo | M |
| **BLOQUE E**: Observabilidad | H38 (health) + H39 (alerts) + H40 (logging) + H42 (monitoreo) | Independientes, pueden resolverse en paralelo | M |

---

## 3. CLASIFICACIÓN P0-P3

### P0 — Bloqueante Auditability (8 hallazgos)

| ID | Hallazgo | Trust Δ | Priority |
|---|---|---|---|
| H08 | No existe repositorio git | +5-8 | 1 |
| H16 | DTEIndexer/XMLJustifier standalone, no integrado | +10-15 | 2 |
| H06 | RIPLEY loader muerto | +5-8 | 3 |
| H13 | PARIS XML 0% HOY (78.8% potencial) | +10-15 | 4 |
| H12 | RIPLEY XML 0% | +5-8 | 5 |
| H01 | 7 facturas RIPLEY no cargadas ($50.5M) | +3-5 | 6 |
| H03 | RIPLEY $142M sin clasificar | +8-12 | 7 |
| H17 | $663M (44%) sin XML respaldo (métrica síntoma, no hallazgo independiente) | — | — |

### P1 — Bloqueante Production Ready (16 hallazgos)

| ID | Hallazgo | Prod Δ | Priority |
|---|---|---|---|
| H31 | API sin autenticación | +10-15 | 1 |
| H34 | SQL injection vía /api/v4/query | +10 | 2 |
| H09 | ~100 rutas absolutas hardcoded | +10 | 3 |
| H10 | CI/CD pipeline fallará en CI | +10-15 | 4 |
| H44 | Sin disaster recovery / backup | +10 | 5 |
| H43 | Sin configuración de entornos | +10 | 6 |
| H38 | Sin métricas / health checks | +8 | 7 |
| H42 | Sin monitoreo ETL | +8 | 8 |
| H25 | surgical_closer bloquea API 30-120s | +5 | 9 |
| H26 | run-audit síncrono bloquea minutos | +5 | 10 |
| H32 | No HTTPS | +5 | 11 |
| H40 | pipeline_log 0 rows, auditoria 1 row | +5 | 12 |
| H46 | 0 test coverage RIPLEY/DTEIndexer/XML | +5 | 13 |
| H45 | 5 documentos contradictorios | +3 | 14 |
| H04 | FALABELLA financial_subgroup 100% NULL | +2 | 15 |
| H05 | marketplace_auditor no escribe financial_subgroup | +2 | 16 |
| H11 | 3 módulos violan singleton DB | +5 | 17 |

### P2 — Deuda Técnica (14 hallazgos)

| ID | Hallazgo | Área |
|---|---|---|
| H02 | 13 tablas obsoletas en schema | DATA/DEAD |
| H07 | ML DTEIndexer path roto | REPRO |
| H14 | ML XML ~10.6% faltante | XML |
| H15 | FALABELLA XML 0% CERTIFICADO | XML |
| H18 | financial_closing.py legacy muerto | DEAD |
| H20 | vw_dashboard_kpis no funcional | DEAD |
| H22 | /api/v4/ledger 3 queries por request | PERF |
| H23 | /cierre/desglose GROUP BY sin índice | PERF |
| H24 | run_classification JOIN sin índice | PERF |
| H27 | Fallback loop Python HORAS | PERF |
| H28 | Sin cache histórica | PERF |
| H29 | Sin connection pooling | PERF |
| H33 | Sin cifrado en reposo | SEC |
| H35 | Sin rate limiting | SEC |
| H37 | Sin validación input POST | SEC |
| H41 | Sin logging estructurado | OBS |
| H47 | Sin SLA/SLO | OBS |

### P3 — Mejora (4 hallazgos)

| ID | Hallazgo | Área |
|---|---|---|
| H19 | 34 _*.py + 137 scratch/*.py | DEAD |
| H21 | API version = "3.5" en vez de V6 | DEAD |
| H30 | SET temp_directory repetido | PERF |
| H36 | Sin CORS config | SEC |

---

## 4. ROADMAP POR FASES

### FASE A — AUDIT READY (Prioridad: MÁXIMA)
*Objetivo: Pasar una auditoría externa. Trust Score → ~78. Trust Score ponderado XML → ~75.*
*Duración estimada: 6-8 semanas*

| Paso | Hallazgos | Acción | Esfuerzo | Dependencias |
|---|---|---|---|---|
| A1 | H08 | `git init`, commit inicial con V6 snapshot, .gitignore | S | — |
| A2 | H09 | Migrar 10 rutas activas a path relativo + config file | M | A1 |
| A3 | H16 | Integrar DTEIndexer al pipeline (hook post-load) | L | — |
| A4 | H13 | Ejecutar DTEIndexer para PARIS → 78.8% XML coverage | M | A3 |
| A5 | H12 | Extender DTEIndexer para ECCSA (RIPLEY XML) | L | A3 |
| A6 | H06 | Reparar load_ripley(): cambiar glob a *.csv + mapeo header | M | — |
| A7 | H03 | Reparar clasificación RIPLEY → $142M con financial_group | M | A6 |
| A8 | H01 | Cargar 7 facturas RIPLEY faltantes ($50.5M) | S | A6 |
| A9 | H45 | Corregir 5 documentos contaminados | S | — |
| A10 | H40 | Reparar pipeline_log + auditoria_v1 logging | S | — |

**Salida FASE A**: XML coverage: 56% → ~85%. RIPLEY clasificación: 0% → 100%. Sistema reproducible. Documentos consistentes. **AUDIT READY (condicional)**.

### FASE B — PRODUCTION READY
*Objetivo: Entorno productivo mínimo viable. Trust Score → ~85. Production Readiness → ~60.*
*Duración estimada: 4-6 semanas*

| Paso | Hallazgos | Acción | Esfuerzo |
|---|---|---|---|
| B1 | H31 | Implementar API Key + Bearer auth en FastAPI | M |
| B2 | H34 | Eliminar POST /api/v4/query o sanitizar con whitelist de queries | M |
| B3 | H10 | Reparar CI/CD: empaquetar DB snapshot, rutas relativas, test en CI | M |
| B4 | H43 | Configurar dev/staging/prod con archivos .env | M |
| B5 | H44 | Backup automático DB + git push diario | M |
| B6 | H38+H42 | Health check endpoint + monitoreo ETL (cron + notificación) | M |
| B7 | H32 | HTTPS con self-signed cert (dev) + Let's Encrypt (prod) | S |
| B8 | H11 | Refactorizar 3 módulos a singleton DB | S |
| B9 | H25+H26 | Hacer surgical_closer + run-audit asíncronos (BackgroundTasks) | M |
| B10 | H46 | Tests para RIPLEY loader, DTEIndexer, XMLJustifier | L |

**Salida FASE B**: API segura. CI/CD funcional. 3 entornos. Backup automático. Monitoreo activo. ETL asíncrono. **PRODUCTION READY**.

### FASE C — SCALABILITY
*Objetivo: Rendimiento predecible hasta 5M rows. Production Readiness → ~75.*
*Duración estimada: 4-6 semanas*

| Paso | Hallazgos | Acción | Esfuerzo |
|---|---|---|---|
| C1 | H22 | Consolidar 3 queries del ledger en 1 con window function | S |
| C2 | H23+H24 | Precalcular agregados por marketplace+periodo en tabla separada | M |
| C3 | H28 | Cache desglose de meses cerrados (TTL 24h / ∞) | M |
| C4 | H27 | Eliminar fallback loop Python (forzar ruta SQL) | M |
| C5 | H02 | Drop 13 tablas obsoletas (no afecta V6) | S |
| C6 | H18+H20+H21 | Limpiar dead code (financial_closing.py, vw_dashboard, version) | S |
| C7 | H29 | Connection pool para lectores concurrentes | M |
| C8 | H14+H15 | Completar XML ML (10.6%) + FALABELLA CERTIFICADO | M |

**Salida FASE C**: API response -70%. Concurrencia +300%. ETL -50% tiempo. XML coverage → ~95%. **RENDIMIENTO PREPRODUCCIÓN**.

### FASE D — COMMERCIAL READY
*Objetivo: Vendible, multi-cliente, SaaS-ready. Trust Score → ~92. Production Readiness → ~85.*
*Duración estimada: 8-12 semanas*

| Paso | Hallazgos | Acción | Esfuerzo |
|---|---|---|---|
| D1 | — | Multi-tenant: particionar DB por tenant_id | XL |
| D2 | H33 | Cifrado en reposo (DuckDB encryption extension) | M |
| D3 | H35+H37 | Rate limiting + validación input completa | M |
| D4 | — | Dashboard de KPIs en tiempo real (reemplazar vw_dashboard_kpis) | L |
| D5 | H39 | Sistema de alertas (email/Slack/webhook) | M |
| D6 | H41 | Migrar a logging estructurado (structlog) | M |
| D7 | H47 | Definir SLA/SLO + contrato de servicio | S |
| D8 | H19 | Archivar/eliminar scratch code | S |

**Salida FASE D**: Multi-tenant. Seguro. Observable. Con SLA. **COMMERCIAL READY**.

---

## 5. TOP 10 ACCIONES — MÁXIMA CONFIANZA CON MÍNIMO RIESGO

*Criterio: Impacto en Trust Score + Audit Readiness + Production Readiness, dividido por Riesgo de implementación x Esfuerzo.*

| Rank | Acción | Hallazgos | Trust Δ | Riesgo | Esfuerzo | Ratio Impacto/Riesgo |
|---|---|---|---|---|---|---|
| **1** | **git init + commit V6** | H08 | +5-8 | B | S | ★★★★★ |
| **2** | **Integrar DTEIndexer al pipeline** | H16, H13, H14, H15 | +10-15 | B | L | ★★★★☆ |
| **3** | **Corregir 5 documentos contaminados** | H45 | +3 | B | S | ★★★★☆ |
| **4** | **Reparar pipeline_log + auditoria_v1** | H40 | +3 | B | S | ★★★★☆ |
| **5** | **Reparar load_ripley() (glob *.xlsx → *.csv)** | H06, H03, H01 | +5-8 | M | M | ★★★★ |
| **6** | **Migrar 10 rutas activas a path relativo** | H09 | +3-5 | M | M | ★★★★ |
| **7** | **Implementar API Key + Bearer auth** | H31 | +2 | B | M | ★★★ |
| **8** | **Health check endpoint + monitoreo ETL** | H38, H42 | 0 → +8 Prod | B | M | ★★★ |
| **9** | **Ejecutar DTEIndexer para PARIS (trigger manual)** | H13 | +10-15 | B | S | ★★★★★ |
| **10** | **Reparar CI/CD (DB snapshot + rutas relativas)** | H10 | +1 Trust, +10-15 Prod | B | M | ★★★ |

### Top 10 — Análisis detallado

#### #1: git init + commit V6
- **Por qué**: Sin git no hay auditoría posible. No hay trazabilidad de cambios. No hay rollback. No hay CI/CD.
- **Esfuerzo**: Horas. `git init; git add -A; git commit -m "BASELINE V6"`
- **Riesgo**: Ninguno. READ-ONLY. No modifica código.
- **Impacto**: Desbloquea H09, H10, H43, H44. Base para TODO lo demás.

#### #2: Integrar DTEIndexer al pipeline
- **Por qué**: Es la acción individual que más impacto tiene en Trust Score (+10-15). Resuelve H13 (PARIS), H14 (ML faltante), H15 (FALABELLA) simultáneamente.
- **Esfuerzo**: Grande. Requiere entender flujo post-load, añadir hook, probar 3 MPs.
- **Riesgo**: Bajo. DTEIndexer ya existe y funciona (probado en ML). Solo falta integrarlo.
- **Impacto**: 78.8% PARIS coverage recuperado. ~10.6% ML faltante. FALABELLA CERTIFICADO.

#### #3: Corregir 5 documentos contaminados
- **Por qué**: Documentación contradictoria = fracaso de auditoría inmediato. Un auditor encuentra traceability_audit_report.txt con cifras 2-3x infladas y descarta todo el sistema.
- **Esfuerzo**: Pequeño. Editar 5 archivos con cifras correctas de V6.
- **Riesgo**: Ninguno. READ-ONLY.

#### #4: Reparar pipeline_log + auditoria_v1
- **Por qué**: Logging framework existe pero no funciona (0 rows, 1 row). Sin evidencia de ejecución, no hay auditoría.
- **Esfuerzo**: Pequeño. Debuggear por qué no se escriben registros.
- **Riesgo**: Ninguno.

#### #5: Reparar load_ripley()
- **Por qué**: RIPLEY es el marketplace más problemático (loader muerto, 0% XML, $142M sin clasificar). Reparar el loader desbloquea TODO lo demás de RIPLEY.
- **Esfuerzo**: Medio. Cambiar glob pattern, mapear headers de CSV a schema esperado.
- **Riesgo**: Medio. Podría romper el pipeline si el mapeo es incorrecto. Requiere test.

#### #6: Migrar 10 rutas activas a path relativo
- **Por qué**: Sin rutas relativas, el sistema solo corre en C:\Users\ASUS Zenbook\... de una laptop específica. Bloquea CI/CD, deployment, multi-tenant.
- **Esfuerzo**: Medio. Identificar las 10 rutas en 7 módulos, reemplazar con path relativo a REPO_ROOT, añadir config file.

#### #7: API Key + Bearer auth
- **Por qué**: API pública sin autenticación = riesgo de fuga de datos financieros. Bloqueante para producción.
- **Esfuerzo**: Medio. FastAPI has built-in support via `HTTPBearer` + `APIKeyHeader`.
- **Impacto**: Habilita producción. No afecta trust score directamente, pero es blocker para commercial.

#### #8: Health check + monitoreo ETL
- **Por qué**: Hoy no hay forma de saber si el pipeline está corriendo, falló, o completó. Ciego total.
- **Esfuerzo**: Medio. Endpoint `/health` + script de monitoreo con notificación.

#### #9: Ejecutar DTEIndexer para PARIS (trigger manual)
- **Por qué**: No requiere integración al pipeline. Solo ejecutar el script existente sobre PARIS. Recupera 78.8% de cobertura XML ($297.8M) de inmediato.
- **Esfuerzo**: Horas (un comando). Riesgo: Ninguno (DTEIndexer es READ-ONLY).
- **Paradoja**: Es la acción #9 porque tiene el mejor ratio impacto/esfuerzo/riesgo de toda la matriz, PERO requiere decisión del negocio (está en el área gris de "implementar" vs "ejecutar herramienta existente").

#### #10: Reparar CI/CD
- **Por qué**: CI/CD existe pero fallará. Sin CI/CD no hay despliegue repetible.
- **Esfuerzo**: Medio. Empaquetar DB snapshot + test en runner headless.
- **Riesgo**: Bajo.

---

## 6. MAPA DE CALOR — HALLAZGOS VS ÁREAS DE IMPACTO

```
                    Trust   Audit   Prod    Commercial
Hallazgo            Score   Ready   Ready   Ready
─────────────────────────────────────────────────────
H08 (no git)         ████    ██████  █████   ████
H16 (DTEIndexer)     ██████  ████████ ██      ██
H06 (RIPLEY loader)  ████    ██████  ██      ██
H13 (PARIS XML)      ██████  ████████ ██      ██
H09 (hardcoded)      ██      ████    ██████  ██████
H31 (no auth)        █       ██      ███████ ████████
H34 (SQL injection)  █       ██      ██████  ████████
H10 (CI/CD broken)   █       ██      ██████  ██████
H44 (no DR/backup)   ██      ████    ██████  ██████
H45 (docs contam)    ██      ████    ██      ██
H03 (RIPLEY classif) █████   ████    ██      ██
─────────────────────────────────────────────────────
Legend: █ = 1-2 pts, ██ = 3-5, ████ = 6-10, ██████ = 10-15, ████████ = 15-25
```

---

## 7. MÉTRICAS AGREGADAS POR FASE

| Métrica | Hoy | Fase A | Fase B | Fase C | Fase D |
|---|---|---|---|---|---|
| **Trust Score** | 54.1 | ~78 | ~85 | ~88 | ~92 |
| Trust Score XML ponderado | 49.7 | ~75 | ~80 | ~90 | ~95 |
| Trust Score Reproducibilidad | 61.8 | ~85 | ~90 | ~92 | ~95 |
| Trust Score Integridad | 87.1 | ~92 | ~95 | ~97 | ~98 |
| **Production Readiness** | 18.75 | ~30 | ~60 | ~75 | ~85 |
| **Audit Ready** | NO | SÍ* | SÍ | SÍ | SÍ |
| **XML coverage ($)** | 56% | ~85% | ~88% | ~95% | ~97% |
| **Clasificación financiera** | ~66% | ~95% | ~98% | 100% | 100% |
| **$ sin respaldo XML** | $663M | ~$226M | ~$181M | ~$75M | ~$45M |
| **Tests pasando** | 14/14 | 14/14 | 20+ | 25+ | 30+ |
| **Repositorio git** | NO | SÍ | SÍ | SÍ | SÍ |
| **CI/CD funcional** | NO | NO | SÍ | SÍ | SÍ |
| **Autenticación API** | NO | NO | SÍ | SÍ | SÍ |
| **Multi-tenant** | NO | NO | NO | NO | SÍ |

*\*Fase A: Audit Ready condicional — pasaría auditoría interna pero no necesariamente externa (falta seguridad y observabilidad).*

---

## 8. RIESGOS DE NO REMEDIAR

| Riesgo | Probabilidad | Impacto | Hallazgos relacionados |
|---|---|---|---|
| Pérdida de datos financieros por falta de backup | ALTA | CATASTRÓFICO ($1,508M) | H44 |
| Fuga de datos financieros por API sin auth | MEDIA | CRÍTICO (reputación + legal) | H31, H34 |
| Imposibilidad de responder a hallazgo de auditoría externa | ALTA | CRÍTICO (descalificación) | H08, H16, H17 |
| Corrupción de DB por 3 módulos con conexión directa | BAJA | ALTO (datos inconsistentes) | H11 |
| Falla en CI bloquea despliegue urgente | MEDIA | ALTO (productividad) | H10 |
| Incapacidad de escalar a nuevo marketplace | MEDIA | ALTO (crecimiento) | H06, H09, H16 |
| Fraude financiero no detectado por falta de monitoreo | BAJA | CATASTRÓFICO | H38, H40, H42 |
| $50.5M en facturas RIPLEY nunca contabilizadas | MEDIA | ALTO (estados financieros incorrectos) | H01 |

---

## 9. PREGUNTAS ABIERTAS PARA DECISIÓN

1. **Ejecutar DTEIndexer para PARIS ahora?** — Acción #9 del Top 10. READ-ONLY, riesgo mínimo, impacto inmediato. Solo requiere decisión: "corremos el script existente sobre PARIS?"

2. **RIPLEY: ¿reparar loader o reconstruir desde CSVs?** — Los 47 CSVs fuente existen. ¿Opción A (reparar load_ripley existente) vs Opción B (nuevo load_ripley_from_csv)?

3. **13 tablas obsoletas: ¿DROP o archivar?** — ¿Eliminación física (no recuperable) o mover a schema `_legacy`?

4. **Versión de API: ¿corregir a V6 o mantener 3.5?** — Metadata cosmética pero indicativa de desorden.

5. **Orden de Fases: ¿A→B→C→D secuencial o solapado?** — Por ejemplo, ¿empezar Fase B (security) en paralelo con Fase A?

---

*FIN DEL DOCUMENTO — BASELINE V6 PERMANECE INMUTABLE. NO IMPLEMENTAR. SÓLO MATRIZ.*
