# P33 — FINAL VERDICT

Basado en evidencia ejecutable recolectada el 2026-06-19.

---

## 1. ¿Qué debe conservarse?

| Componente | Evidencia |
|------------|-----------|
| **FinancialEngine** (1028 líneas) | WF = EB = LD $0 delta en 18 períodos × 4 MPs + ALL |
| **SurgicalLoader** (845 líneas) | Único ETL activo. Ingestiona 4/5 marketplaces correctamente |
| **marketplace_ledger_v1** (402K rows) | Datos financieros consistentes, 50 períodos, 7 grupos financieros |
| **marketplace_cierre_financiero_v1** (246 rows) | Cierre certificado por período/MP |
| **Certification Gate** (27 tests) | 19/19 PASS — salvaguarda contra regresiones |
| **ReconciliationEngine** (64 tests) | La suite de tests más grande del proyecto |
| **33 endpoints API** (28 GET, 5 POST) | 32/33 funcionales, respuesta ~24ms post-P32R10 |
| **3 dashboards** (Dashboard, Executive, Documentary) | Render correcto, sin lógica financiera client-side |

---

## 2. ¿Qué debe repararse?

| Prioridad | Issue | Acción |
|-----------|-------|--------|
| **P0** | `POST /api/v4/dte/certify` — ambos code paths rotos | Agregar `periodo` requerido; crear método `get_certification(marketplace)` o eliminarlo si no tiene consumidores |
| **P0** | `Scripts/pipeline_cli.py` importa `AntigravityEngineV4` inexistente | Eliminar archivo o crear el módulo faltante |
| **P1** | `GET /executive/insights` ignora `marketplace` param | Agregar `WHERE marketplace = ?` a la SQL |
| **P1** | 21 tablas vacías en DuckDB | Auditar cuáles deben poblarse vs cuáles eliminarse |
| **P2** | `test_regression_contracts.py` — loop body `continue` (nunca asevera) | Reemplazar `continue` con assert real |
| **P2** | `test_paris_classification.py` — asserts 2 rows, espera 0 | Corregir expectativa o implementar glob recursivo |
| **P2** | 3 imports muertos en `run_full_audit()` | Eliminar imports no utilizados |
| **P2** | `get_documentary_coverage()` descarta resultado | Eliminar llamada huérfana o usar el resultado |
| **P3** | Endpoint nombrado `/waterfall-v3` | Renombrar a `/waterfall` |

---

## 3. ¿Qué debe eliminarse?

| Archivo | Razón |
|---------|-------|
| `engine/data_loader_v3.py` (98 líneas) | Legacy — referencia proyecto externo, 0 imports |
| `engine/data_loader_v4.py` (119 líneas) | Legacy — mismo caso |
| `engine/data_loader_enhanced.py` (134 líneas) | Legacy — mismo caso |
| `templates/dashboard.html.bak` (1,408 líneas) | Backup — nunca servido |
| `templates/dashboard_utf8.html` (93KB, corrupto) | Corrupto — nunca servido |
| `templates/executive_dashboard.html.p16g_*` (804 líneas) | Backup — nunca servido |
| `frontend/shared/api_client.js` (101 líneas) | Standalone — nunca cargado por ningún template |
| `Scripts/pipeline_cli.py` (39 líneas) | Importa módulo inexistente |

**Total recuperable:** ~2,800 líneas de código, ~142KB de templates.

---

## 4. ¿Qué debe congelarse?

| Componente | Razón |
|------------|-------|
| **`certification/ecc/`** (23 archivos) | Subsistema ECC grande. Sin evidencia de consumo activo. Congelar hasta que se demuestre necesidad. |
| **`certification/electronic_certification/`** (9 archivos) | CAF, SII, XSD validators. No hay endpoint que los consuma desde el frontend. |
| **`certification/knowledge/`** (7 archivos) | Obsidian adapter, vault exporter. Sin integración activa. |
| **`engine/v4/contracts/`** (7 archivos) | Contract definitions no referenciados por el orquestador principal. |
| **`cierre_financiero_v2` tabla** (96 rows) | No hay claridad si reemplaza a v1. Congelar hasta decisión. |
| **357 archivos governance/** | Históricos. No modificar hasta que se defina política de archivo. |
| **129 archivos KnowledgeBase/** | Históricos. Congelar. |

---

## 5. ¿Cuál es el mayor riesgo técnico?

**DB principal sin respaldo automatizado ni réplica.**

- `data/db/meli_financial_v4.db` (125 MB) es el único storage primario
- 200+ tests dependen de que esta DB exista y esté íntegra
- No hay backup schedule automatizado (solo snapshots manuales)
- No hay read replica para consultas analíticas pesadas
- DuckDB no tiene replicación nativa

Riesgo: pérdida o corrupción de `meli_financial_v4.db` dejaría el sistema inoperable sin recovery inmediato.

---

## 6. ¿Qué impide avanzar?

1. **P0-1: `/api/v4/dte/certify` roto** — cualquier integración que consuma este endpoint fallará silenciosamente.
2. **P2-6: RipleyETL clase muerta** — las validaciones DTE/settlement definidas para RIPLEY no se ejecutan, pero nadie lo ha notado. Esto sugiere que el bus de integración no está monitorizado.
3. **21 tablas vacías** — no se sabe si son features incompletos o artefactos muertos. Sin esta claridad, cualquier nueva feature puede duplicar lógica existente.
4. **Sin orquestador de pipeline** — `SurgicalLoader.run()` es el único entry point. No hay scheduler, no hay retry, no hay alertas de falla.

---

## 7. ¿Puede iniciarse P33 sobre esta base?

| Condición | Estado |
|-----------|--------|
| Core financiero funcional | **SÍ** — WF = EB = LD verificado |
| API operativa | **SÍ** — 32/33 endpoints funcionales |
| Tests existentes | **SÍ** — 246 tests, 2 broken conocidos |
| DB íntegra | **SÍ** — 402K rows, 35 tablas |
| Principales riesgos identificados | **SÍ** — documentados arriba |
| Deuda P0 documentada | **SÍ** |
| Deuda P1 documentada | **SÍ** |
| Código muerto identificado | **SÍ** |
| Carga de documentación histórica | **ALTA** — 357 + 129 archivos |

### Veredicto

**SÍ, P33 puede iniciarse sobre esta base, con 2 condiciones:**

1. Reparar los 2 issues P0 antes de cualquier desarrollo nuevo.
2. No asumir que los subsistemas congelados (ECC, ElectronicCertification, Knowledge, Contracts) están operativos. Verificar cada uno antes de depender de ellos.

El core del sistema (ETL → Ledger → Close → API → Dashboard) es estable, rápido y está certificado. La deuda técnica acumulada es principalmente periférica (subsistemas no utilizados, documentación histórica, archivos muertos) y no afecta el funcionamiento del core financiero.
