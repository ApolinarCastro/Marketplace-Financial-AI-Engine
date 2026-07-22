# SYSTEM_HEALTH

Fecha de auditoría: `2026-07-09`

Modo:
- `READ ONLY`

Evidencia ejecutada:
- `python -m pytest --collect-only -q` -> `278 tests collected`
- `python -m pytest tests/test_api_smoke.py tests/test_regression_contracts.py tests/test_reconciliation_engine.py -q` -> `82 passed`
- `python -m compileall api engine/v4 tests` -> sin errores de sintaxis
- importación real de módulos críticos
- inspección de rutas FastAPI reales desde `app.routes`
- consultas read-only sobre `data/db/meli_financial_v4.db`

## 1. Core Productivo

Cadena productiva observada en código:

`RAW -> ETL -> Ledger -> Financial -> API -> Frontend`

### RAW
- Evidencia de dependencia con archivos raw desde ETL:
  - [engine/v4/surgical_loader.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/surgical_loader.py:1)

Estado: `AMARILLO`
- Funciona como componente de cadena.
- No se ejecutó sobre datos live por restricción de auditoría.
- Participa en runtime mutante, no en flujo read-only del dashboard.

### ETL
- Componente observado:
  - [engine/v4/surgical_loader.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/surgical_loader.py:81)
- Dependencias directas:
  - `DatabaseV4`
  - `MarketplaceAuditorEngine`

Estado: `AMARILLO`
- Está en la cadena.
- No forma parte del flujo read-only del dashboard.
- Su ejecución observable está expuesta solo por endpoint mutante `/api/v4/run-audit`.

### Ledger
- Componente observado:
  - [engine/v4/marketplace_auditor.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/marketplace_auditor.py:406)
  - [engine/v4/domain/ledger_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/domain/ledger_engine.py:7)
- Evidencia de uso en API:
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:71)
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:165)

Estado: `VERDE`
- `marketplace_ledger_v1` existe y responde.
- Conteo observado: `402105`
- Rutas consumidoras activas:
  - `/api/v4/ledger`
  - `/api/v4/cierre/desglose`

### Financial
- Componentes observados:
  - [engine/v4/domain/financial_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/domain/financial_engine.py:209)
  - [engine/v4/domain/ledger_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/domain/ledger_engine.py:16)
- Evidencia de uso en API:
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:397)
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:464)
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:499)

Estado: `VERDE`
- `82` tests críticos pasaron incluyendo contratos y reconciliación.
- Rutas consumidoras activas:
  - `/api/v4/exec/summary`
  - `/api/v4/financial-structure`
  - `/api/v4/exec/waterfall-v3`

### API
- Entry point:
  - [run_app.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/run_app.py:1)
- App principal:
  - [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:34)
- Rutas reales observadas:
  - `/app`
  - `/exec`
  - `/documentary-dashboard`
  - 29 rutas propias `/api/v4/...`

Estado: `AMARILLO`
- Funciona y expone el core vivo.
- Comparte el mismo proceso con endpoints mutantes:
  - `/api/v4/run-audit`
  - `/api/v4/run-indexer`
  - `/api/v4/correcciones`
  - `/api/v4/knowledge/export`

### Frontend
- Templates observados como activos por ruta:
  - [templates/dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/dashboard.html:1) -> `/app`
  - [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:1) -> `/exec` y `/executive-dashboard`
  - [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:1) -> `/documentary-dashboard`

Estado: `AMARILLO`
- Hay consumidores reales por ruta.
- Hay duplicación real de JS embebido.
- `documentary_dashboard.html` contiene llamada a endpoint inexistente.

## 2. Qué funciona

### Funciona con evidencia ejecutable
- DB oficial:
  - [engine/v4/database.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/database.py:13)
  - Path: `data/db/meli_financial_v4.db`
  - Existe en disco.
- API y contratos críticos:
  - `82 passed` en tests críticos.
- Módulos importables:
  - `engine.v4.lineage: OK`
  - `engine.v4.scorecard: OK`
  - `engine.v4.data_quality: OK`
  - `engine.v4.production: OK`
  - `engine.v4.explainability: OK`
  - `engine.v4.closing: OK`
- Sintaxis:
  - `compileall` sin errores.

## 3. Qué no funciona

### No funciona con evidencia ejecutable
- [engine/v4/reprocess_audit.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/reprocess_audit.py:6)
  - Import real falla:
  - `ModuleNotFoundError: No module named 'engine.v4.meli_auditor'`
- [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:1464)
  - consume `/api/v4/upload/dte`
  - la ruta no existe en `app.routes`

## 4. Qué nunca se ejecuta o no participa del core productivo

### Test-only
- Participan en tests, no en rutas productivas observables:
  - `engine/v4/lineage`
  - `engine/v4/scorecard`
  - `engine/v4/data_quality`
  - `engine/v4/closing`
  - `engine/v4/production`
  - `engine/v4/explainability`

Evidencia:
- Importables.
- Referenciados en `tests/`.
- Sin consumidor en `api/api.py`, `templates/dashboard.html`, `templates/executive_dashboard.html`.

### Fuera de cadena productiva actual
- [frontend/shared/api_client.js](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/frontend/shared/api_client.js:1)
  - existe como shared helper
  - los templates activos redefinen `window.ApiClient` inline
- [database/duckdb_manager.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/database/duckdb_manager.py:1)
  - usa `database/reconciliation.db`
  - no es usado por `run_app.py` ni por `api/api.py`

## 5. Legacy / Obsoleto / Backup

### LEGACY
- [database/duckdb_manager.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/database/duckdb_manager.py:7)
  - path alternativo de DB
- `engine/data_loader_v3.py`
- `engine/data_loader_v4.py`
- `engine/data_loader_enhanced.py`

### OBSOLETO
- [engine/v4/reprocess_audit.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/reprocess_audit.py:1)
  - import roto
- [frontend/shared/api_client.js](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/frontend/shared/api_client.js:1)
  - sin consumo productivo observable

### BACKUP
- `engine/v4/marketplace_auditor.py.backup`
- `engine/v4/marketplace_auditor.py.pre_paris_patch`
- `engine/v4/surgical_loader.py.bak`
- `engine/v4/surgical_xml_justifier.py.backup`
- `engine/v4/xml_matcher.py.backup`
- `templates/dashboard.html.bak`
- `templates/executive_dashboard.html.p16g_04e_backup_20260623_090844`

## 6. Duplicación real

### JS
- `window.ApiClient` duplicado en:
  - [frontend/shared/api_client.js](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/frontend/shared/api_client.js:6)
  - [templates/dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/dashboard.html:22)
  - [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:46)
  - [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:46)

### Helper financiero frontend
- `mapDetalleToConcept` duplicado en:
  - [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:428)
  - [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:720)

### HTML
- Template vivo + backup coexistiendo:
  - `templates/dashboard.html`
  - `templates/dashboard.html.bak`
  - `templates/executive_dashboard.html`
  - `templates/executive_dashboard.html.p16g_04e_backup_20260623_090844`

## 7. Estado de Salud

### Core Financiero: `VERDE`
- Evidencia:
  - `82 passed` en tests críticos
  - rutas `/api/v4/exec/summary`, `/api/v4/financial-structure`, `/api/v4/exec/waterfall-v3`

### ETL: `AMARILLO`
- Evidencia:
  - componente presente en cadena
  - no validado en ejecución live por restricción de auditoría
  - solo expuesto por endpoint mutante

### DuckDB: `VERDE`
- Evidencia:
  - DB oficial existe
  - tablas core responden
  - `engine/v4/database.py` es el manager usado por runtime

### API: `AMARILLO`
- Evidencia:
  - carga y sirve rutas productivas
  - mezcla lectura y mutación en el mismo servicio

### Frontend: `AMARILLO`
- Evidencia:
  - `/app` y `/exec` tienen templates activos
  - `documentary_dashboard.html` tiene un flujo roto
  - duplicación real de JS

### Tests: `VERDE`
- Evidencia:
  - `278 tests collected`
  - `82 passed` en suite crítica ejecutada

### Dashboard: `AMARILLO`
- Evidencia:
  - `dashboard.html` y `executive_dashboard.html` están conectados
  - `documentary_dashboard.html` tiene consumo a endpoint inexistente

### Trazabilidad: `AMARILLO`
- Evidencia:
  - existen `DocumentCertificationEngine` y `DocumentGapEngine`
  - el módulo `lineage` es test-only, sin consumidor productivo observable

### Single Source: `AMARILLO`
- Evidencia:
  - runtime usa `data/db/meli_financial_v4.db`
  - existe stack paralelo legacy en `database/duckdb_manager.py`

### Performance: `AMARILLO`
- Evidencia:
  - hay logs históricos con `500`, locks y conflictos de catálogo en [logs/backend.log](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/logs/backend.log:147)
  - la auditoría no ejecutó benchmark activo
