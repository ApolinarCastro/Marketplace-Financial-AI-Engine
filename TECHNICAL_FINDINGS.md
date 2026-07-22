# TECHNICAL_FINDINGS

## P0

### P0-1. Template activo con endpoint inexistente
- Archivo: [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:1464)
- Línea: `1464`
- Evidencia:
  - `fetch('/api/v4/upload/dte', {`
  - la ruta no existe en `app.routes`
- Dependencias:
  - depende de `api/api.py`
  - no tiene backend correspondiente
- Riesgo:
  - flujo documental del template no ejecutable

### P0-2. Script roto por import inexistente
- Archivo: [engine/v4/reprocess_audit.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/reprocess_audit.py:6)
- Línea: `6`
- Evidencia:
  - `from engine.v4.meli_auditor import MeliAuditorEngine`
  - import real falla con `ModuleNotFoundError`
- Dependencias:
  - depende de `engine.v4.meli_auditor`
  - ese módulo no existe en el árbol auditado
- Riesgo:
  - script muerto presentado como ejecutable

## P1

### P1-1. Servicio productivo mezcla lectura y mutación operativa
- Archivo: [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:610)
- Líneas:
  - `610`
  - `659`
  - `691`
  - `829`
- Evidencia:
  - `POST /api/v4/correcciones`
  - `POST /api/v4/run-audit`
  - `POST /api/v4/run-indexer`
  - `POST /api/v4/knowledge/export`
- Dependencias:
  - `MarketplaceAuditorEngine`
  - `DTEIndexer`
  - `ObsidianAdapter`
- Riesgo:
  - el mismo proceso que sirve dashboards expone escritura y ejecución pesada

### P1-2. Doble stack de base de datos
- Archivo A: [engine/v4/database.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/database.py:13)
- Archivo B: [database/duckdb_manager.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/database/duckdb_manager.py:7)
- Evidencia:
  - core vivo apunta a `data/db/meli_financial_v4.db`
  - stack legacy apunta a `database/reconciliation.db`
- Dependencias:
  - `run_app.py` usa `DatabaseV4`
  - no se observó consumidor productivo de `DuckDBManager`
- Riesgo:
  - coexistencia de dos fuentes técnicas de datos

### P1-3. Frontend activo duplica helper financiero
- Archivo A: [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:428)
- Archivo B: [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:720)
- Evidencia:
  - `function mapDetalleToConcept(detalle) {`
- Dependencias:
  - ambos templates
- Riesgo:
  - dos implementaciones activas de una misma transformación frontend

## P2

### P2-1. Helper compartido no consumido por templates activos
- Archivo: [frontend/shared/api_client.js](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/frontend/shared/api_client.js:6)
- Evidencia:
  - define `window.ApiClient`
  - templates activos redefinen `window.ApiClient` inline:
    - [templates/dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/dashboard.html:22)
    - [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:46)
    - [templates/documentary_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/documentary_dashboard.html:46)
- Dependencias:
  - sin consumidor productivo observable
- Riesgo:
  - código obsoleto o muerto coexistiendo con duplicados vivos

### P2-2. Engines completos sin consumidor productivo observable
- Archivos:
  - [engine/v4/lineage/lineage_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/lineage/lineage_engine.py:1)
  - [engine/v4/scorecard/scorecard_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/scorecard/scorecard_engine.py:1)
  - [engine/v4/data_quality/quality_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/data_quality/quality_engine.py:1)
  - [engine/v4/closing/closing_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/closing/closing_engine.py:1)
  - [engine/v4/production/production_checklist.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/production/production_checklist.py:1)
  - [engine/v4/explainability/explainability_engine.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/engine/v4/explainability/explainability_engine.py:1)
- Evidencia:
  - importan correctamente
  - están en tests recolectados
  - no aparecen como dependencia directa de rutas productivas usadas por `/app` o `/exec`
- Dependencias:
  - tests
- Riesgo:
  - superficie técnica mantenida sin consumo productivo observable

### P2-3. Endpoints sin consumidor visible en templates activos
- Rutas:
  - `/api/v4/executive/insights`
  - `/api/v4/dte/document/{transaction_id}`
  - `/api/v4/documentary/coverage`
  - `/api/v4/debug_audit`
  - `/api/v4/run-indexer`
- Evidencia:
  - existen en [api/api.py](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/api/api.py:58)
  - no se observaron llamadas desde `dashboard.html` ni `executive_dashboard.html`
- Dependencias:
  - API solamente
- Riesgo:
  - superficie expuesta sin consumidor productivo visible

## P3

### P3-1. Backups dentro del runtime
- Archivos:
  - `engine/v4/marketplace_auditor.py.backup`
  - `engine/v4/marketplace_auditor.py.pre_paris_patch`
  - `engine/v4/surgical_loader.py.bak`
  - `engine/v4/surgical_xml_justifier.py.backup`
  - `engine/v4/xml_matcher.py.backup`
- Evidencia:
  - presentes en árbol productivo `engine/v4`
- Dependencias:
  - no se observaron imports productivos
- Riesgo:
  - contaminación del perímetro vivo

### P3-2. Templates backup coexistiendo con templates activos
- Archivos:
  - [templates/dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/dashboard.html:1)
  - `templates/dashboard.html.bak`
  - [templates/executive_dashboard.html](/C:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/templates/executive_dashboard.html:1)
  - `templates/executive_dashboard.html.p16g_04e_backup_20260623_090844`
- Evidencia:
  - backups presentes en mismo directorio que los templates servidos por FastAPI
- Dependencias:
  - sin consumidor productivo observable
- Riesgo:
  - duplicación de artefactos frontend

### P3-3. Legacy loaders fuera del core vivo
- Archivos:
  - `engine/data_loader_v3.py`
  - `engine/data_loader_v4.py`
  - `engine/data_loader_enhanced.py`
- Evidencia:
  - existen fuera de `engine/v4`
  - no fueron observados como dependencia del runtime FastAPI actual
- Dependencias:
  - no observadas en `run_app.py` ni `api/api.py`
- Riesgo:
  - confusión entre loader vivo y loaders legacy
