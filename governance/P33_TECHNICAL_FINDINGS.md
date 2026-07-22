# P33 — TECHNICAL FINDINGS

## P0 — Debe repararse inmediatamente

### P0-1: `/api/v4/dte/certify` completamente roto

**Archivo:** `api/api.py:261-267`

**Causa:** El endpoint tiene 2 code paths, ambos rotos:
- `marketplace="ALL"`: llama `engine.get_all_certifications()` sin parámetro `periodo`. El método requiere `periodo` y lanza `ValueError` si no se provee.
- `marketplace != "ALL"`: llama `engine.get_certification(marketplace)` — método que **no existe** en `DocumentCertificationEngine`. Solo tiene `get_all_certifications(periodo)` y `get_coverage_summary(marketplace, periodo)`.

**Impacto:** Cualquier llamada a este endpoint produce HTTP 500.

### P0-2: `pipeline_cli.py` importa módulo inexistente

**Archivo:** `Scripts/pipeline_cli.py:4`

**Causa:** `from engine.v4.pipeline import AntigravityEngineV4` — el módulo `engine/v4/pipeline.py` **no existe**. `AntigravityEngineV4` nunca fue implementado.

**Impacto:** El script de CLI no puede ejecutarse.

---

## P1 — Debe repararse pronto

### P1-1: Aggregate ALL ≠ sum(per-MP) por SIGNAL/NOISE no documentado en código

**Archivo:** `engine/v4/domain/financial_engine.py:588`

**Causa:** La consulta agregada en `get_executive_breakdown()` aplica `COALESCE(include_in_operational_pnl,1)=1 AND financial_group IS NOT NULL` pero NO aplica signal filter para RIPLEY en el modo ALL. El desglose per-MP sí aplica signal filter para RIPLEY. Diferencia: ~$4.1M (13.8% del neto ALL).

**Impacto:** La sumatoria de per-MP ≠ ALL aggregate. Comportamiento esperado pero no documentado en el código.

### P1-2: Single 840-line api.py sin modularización

**Archivo:** `api/api.py` (840 lines)

**Causa:** Las 33 rutas están en un solo archivo sin usar `APIRouter`. Sin separación por dominio (ledger, cierre, dte, exec, intelligence).

**Impacto:** Dificulta mantenimiento. Cada endpoint que se agrega aumenta el tamaño del monolito.

### P1-3: 21 tablas vacías en DuckDB

**Archivo:** `data/db/meli_financial_v4.db`

**Causa:** 21 de 35 tablas tienen 0 filas. Muchas son artefactos de fases anteriores o features que nunca se implementaron completamente.

**Impacto:** Consultas contra estas tablas retornan 0 filas sin error. Riesgo de falsos negativos en lógica de negocio.

### P1-4: `executive/insights` ignora parámetro marketplace

**Archivo:** `api/api.py:514-521`

**Causa:** El endpoint acepta `marketplace` pero la SQL no lo usa: `SELECT * FROM marketplace_auditoria_v1 ORDER BY detected_at DESC LIMIT 10`.

**Impacto:** El filtro no funciona. El frontend muestra datos de todos los MPs aunque solicite uno específico.

---

## P2 — Debe repararse cuando sea posible

### P2-1: Test de regresión con assert roto

**Archivo:** `tests/test_regression_contracts.py:207-216`

**Causa:** `test_api_file_no_contains_startswith` itera `forbidden = ['.contains(', '.startswith(', 'catMap', 'FINANCIAL_STRUCTURE']` pero el cuerpo del loop es `continue` para 3 de 4 patrones. Solo verifica `FINANCIAL_STRUCTURE`.

**Impacto:** Los patrones `.contains(`, `.startswith(`, `catMap` pueden estar presentes en el frontend y el test no los detectará.

### P2-2: Test de PARIS espera valores incorrectos

**Archivo:** `tests/test_paris_classification.py:87-88`

**Causa:** `test_recursive_glob_ingests_from_subdirectories` comenta "should load 0 rows under current implementation" pero `assertEqual(count, 2)` espera 2 filas. La implementación actual carga 0 filas con glob no-recursivo.

**Impacto:** Test falla. Impide validar que la corrección de glob recursivo funciona.

### P2-3: 3 imports muertos en run_full_audit

**Archivo:** `api/api.py:661-663`

**Causa:** `from engine.v4.run_initial_audit import load_marketplace_ledger_standalone`, `from engine.v4.surgical_loader import SurgicalLoader`, `from engine.v4.surgical_xml_justifier import XMLJustifier` — importados pero **nunca invocados**.

**Impacto:** 3 imports innecesarios que cargan módulos completos en memoria sin propósito.

### P2-4: `_DTE_LIMITATIONS` nunca usado

**Archivo:** `api/api.py:349-354`

**Causa:** Diccionario definido con información de cobertura DTE por marketplace. Nunca referenciado por ningún endpoint.

**Impacto:** Código muerto. La información podría ser valiosa pero no se expone.

### P2-5: Wasted API call en documentary/coverage

**Archivo:** `api/api.py:339`

**Causa:** `res = engine.get_all_certifications(periodo)` seguido inmediatamente por `doc_cov = "NO DISPONIBLE"`. El resultado de `get_all_certifications` se descarta.

**Impacto:** Llamada a DB desperdiciada (~3-8ms) en cada request.

### P2-6: RipleyETL clase nunca invocada por SurgicalLoader

**Archivo:** `engine/v4/etl/ripley_loader.py` vs `engine/v4/surgical_loader.py`

**Causa:** `SurgicalLoader.load_ripley()` tiene su propia lógica inline de parsing XLSX. La clase `RipleyETL` con sus transformaciones validación DTE no se usa.

**Impacto:** Toda la lógica de validación DTE/settlement en `RipleyETL` (transform_comision, transform_opex) no se ejecuta. Las reglas de negocio definidas en enero 2026 están inactivas.

---

## P3 — Debe monitorearse

### P3-1: 3 loaders legacy no utilizados

**Archivos:** `engine/data_loader_v3.py`, `engine/data_loader_v4.py`, `engine/data_loader_enhanced.py`

**Causa:** Heredados de versión anterior del proyecto. Referencian `Marketplace_Conciliacion/conciliador.db` (proyecto diferente).

**Impacto:** Clutter. 351 líneas de código muerto.

### P3-2: Frontend 100% CDN-dependiente

**Archivos:** templates/dashboard.html, executive_dashboard.html, documentary_dashboard.html

**Causa:** Tailwind CSS, Font Awesome y Google Fonts cargados desde CDN. Sin archivos locales ni bundle estático.

**Impacto:** Sin conexión a internet, los dashboards no renderizan correctamente.

### P3-3: ApiClient duplicado 4 veces

**Archivos:** dashboard.html, executive_dashboard.html, documentary_dashboard.html, `frontend/shared/api_client.js`

**Causa:** Mismo código de cliente API copiado textualmente en 3 templates + 1 archivo standalone. El standalone no se carga.

**Impacto:** Cambios en el cliente API requieren modificar 4 archivos. Riesgo de divergencia.

### P3-4: `cierre_financiero_v2` duplica a v1

**Tabla:** `cierre_financiero_v2` (96 rows, 24 periods)

**Causa:** Tabla creada con columnas adicionales (signal_mode, row_count, dte_linked_rows, resultado_neto_full). No hay documentación sobre si reemplaza o complementa a `marketplace_cierre_financiero_v1`.

**Impacto:** Ambigüedad sobre cuál tabla es la fuente oficial de verdad para cierre financiero.

### P3-5: endpoint nombrado como V3

**Endpoint:** `/api/v4/exec/waterfall-v3`

**Causa:** El endpoint lleva sufijo `-v3` que no corresponde a la versión actual de la API (v4). Es un artefacto de una migración anterior.

**Impacto:** Inconsistencia de nomenclatura.

### P3-6: Template backups (3 archivos, ~142KB total)

**Archivos:** `templates/dashboard.html.bak`, `templates/dashboard_utf8.html` (corrupto), `templates/executive_dashboard.html.p16g_04e_backup_*.html`

**Causa:** Backups manuales no limpiados. Uno de ellos (`dashboard_utf8.html`) está corrupto (mojibake).

**Impacto:** Clutter. Riesgo de confusión.

### P3-7: 357 governance/ + 129 KnowledgeBase/ archivos no ejecutables

**Causa:** Documentación histórica acumulada desde Sprint A1 (2026-05). Sin mantenimiento activo.

**Impacto:** La documentación puede divergir del estado actual del código.
