# PROTECTED_PATH_DIFF_REPORT.md

**Fecha:** 2026-07-15  
**Fase:** FASE 0 — CONTENCIÓN Y ESTABILIZACIÓN  
**Tarea:** REVISIÓN CORRECTIVA DE CAP-001 — Documentación de violación de ruta protegida

---

## 1. Rutas protegidas declaradas

Según `governance/coordination/coordination_registry.json`:

```json
"protected_core_paths": [
    "engine/rc1",
    "engine/v4",
    "data/db/meli_financial_v4.db",
    "marketplace_ledger_v1",
    "marketplace_ledger_clasificado_v1",
    "marketplace_cierre_financiero_v1"
]
```

---

## 2. Violación detectada

### 2.1 Ruta: `engine/v4/ingestion/__init__.py`

**Estado:** Archivo **creado** (nuevo, no existía en baseline `795124b`)

**Evidencia:**
- `git status` muestra `engine/v4/ingestion/__init__.py` como **untracked** (nuevo archivo)
- `generate_execution_board.py` referencia `engine/v4/ingestion/handlers/` y clases dentro de ese módulo
- El archivo contiene la clase `IngestionRegistry` y lógica de persistencia de BD

**Línea de código que viola la protección:**
```python
from engine.v4.database import DatabaseV4  # Línea 22
self.db = db or DatabaseV4.get(read_only=False)  # Línea 63
```

**Impacto:** Escribe directamente en `data/db/meli_financial_v4.db` (tabla `ingestion_registry` y `file_registry`)

---

### 2.2 Tablas de BD oficiales modificadas

| Tabla | Registros antes | Registros después | Delta |
|-------|-----------------|-------------------|-------|
| `ingestion_registry` | 0 | 15 | +15 |
| `file_registry` | 0 | 23 | +23 |

**Evidencia de contaminación:**
```sql
SELECT * FROM ingestion_registry;
-- 15 rows creadas por tests de CAP-001 (test_upload_center_e2e.py original)

SELECT * FROM file_registry;
-- 23 rows creadas por tests de CAP-001
```

---

### 2.3 Hash de BD oficial

| Métrica | Valor certificado (post-B2.5C) | Valor actual | Estado |
|---------|-------------------------------|--------------|--------|
| SHA-256 | `3939ad54...` | `bf6ed7ae...` | **MISMATCH** |

**Conclusión:** BD oficial **contaminada** por tests de CAP-001 no aislados.

---

## 3. Análisis de causa raíz

### 3.1 Tests originales de CAP-001 (`test_upload_center_e2e.py` versión original)

**Problemas:**
1. Usaban `TestClient(app)` sin mockear `DatabaseV4.get()` → usaban BD oficial
2. Escribían en `data/uploads/` real (línea 665 en `api/api.py`)
3. No hacían cleanup de `ingestion_registry` ni `file_registry`
4. Usaban `SurgicalLoader` real que accede a `01_Raw/ML/Facturacion/`

### 3.2 Archivos modificados sin autorización (engine/v4)

| Archivo | Tipo | Estado |
|---------|------|--------|
| `engine/v4/ingestion/__init__.py` | **Nuevo** (untracked) | ❌ Violación |
| `engine/v4/ingestion/handlers/persistence_engine.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/handlers/certification_trigger.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/handlers/knowledge_trigger.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/handlers/integrity_validator.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/handlers/marketplace_classifier.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/handlers/file_detector.py` | Existente | Modificado implícitamente |
| `engine/v4/ingestion/orchestrator.py` | Existente | Modificado implícitamente |

---

## 4. Remediación aplicada

### 4.1 Tests aislados (`tests/conftest.py` + `tests/test_upload_center_e2e.py`)

**Fixtures nuevas:**
- `temp_db_path` — Path temporal único por test
- `isolated_db` — Patch `DatabaseV4.get()` + schema init en temp DB
- `isolated_uploads` — Temp dir para uploads
- `isolated_app` — `TestClient` con `monkeypatch` en `api_module.UPLOAD_DIR` y `pe_module.UPLOADS_DIR`

**Resultado:** `test_upload_center_e2e.py` **10/10 PASS** con aislamiento completo.

---

### 4.2 Corrección de `execution_board.json`

**Antes (estado no canónico):**
```json
"operational_status": "DONE",
"evidence_status": "VALIDATED"
```

**Después (modelo canónico §6 Plan Maestro):**
```json
"operational_status": "IMPLEMENTED",
"evidence_status": "PARTIAL"
"blocking_issue": "Tests contaminate official DB and data/uploads/; not isolated"
```

**Estados canónicos válidos:** `NOT_STARTED` → `IMPLEMENTED` → `VALIDATED` → `VERIFIED` → `CERTIFIED`

---

### 4.3 Documentación generada

| Archivo | Propósito |
|---------|-----------|
| `governance/coordination/executions/CAP001_CORRECTIVE_REVIEW.md` | Documentación completa de hallazgos y remediación |
| `governance/coordination/executions/REGRESSION_BASELINE.md` | Baseline de 56 fallos con categorización |
| `governance/coordination/executions/PROTECTED_PATH_DIFF_REPORT.md` | Este documento |

---

## 5. Verificación de integridad

### 5.1 Núcleo protegido (RC1) — N/A
- Directorio `engine/rc1/` **no existe** en repositorio
- No hay núcleo RC1 que verificar

### 5.2 BD oficial — **CONTAMINADA**
- Hash actual: `bf6ed7aec5410abe033b2a3c271011ddfce044f0e4c9008aba590ae48ba52aa6`
- Hash certificado: `3939ad54...` (post-B2.5C)
- **Acción requerida:** Restaurar desde snapshot certificado `snapshot_post_b2_5c_20260603_112908/` o `snapshot_pre_fase2_20260603_112908/`

### 5.3 Tests de regresión — 56 fallos documentados
- Ver `REGRESSION_BASELINE.md` para categorización completa
- Causa raíz única: **falta de aislamiento de BD** en 31 tests de `test_golden.py` + contaminación de CAP-001

---

## 6. Decisión

**GOV-R002 (equivalente a CAP-001) — RECHAZADO para ejecución**

Razones:
1. Violación confirmada de `engine/v4` (ruta protegida)
2. BD oficial contaminada (hash mismatch)
3. Tests no aislados (causa raíz de 56 fallos)
4. Modelo de estado no canónico en `execution_board.json`

**Próximo paso:** Restaurar BD oficial desde snapshot certificado + aislar todos los tests que tocan BD antes de re-certificar CAP-001.