# CAP-001 CORRECTIVE REVIEW

**Fecha:** 2026-07-15  
**Fase:** FASE 0 — CONTENCIÓN Y ESTABILIZACIÓN  
**Tarea:** REVISIÓN CORRECTIVA DE CAP-001 (Upload Center E2E)  
**Responsable:** Codex (OpenCode executor)  
**Estado:** COMPLETADO — Remediación aplicada, listo para re-certificación

---

## 1. Resumen ejecutivo

**CAP-001 (Upload Center E2E)** fue reportado como `DONE`/`VALIDATED` en `execution_board.json`. La revisión correctiva revela:

| Criterio | Reportado | Realidad |
|----------|-----------|----------|
| Estado operacional | `DONE` | **IMPLEMENTED** |
| Estado de evidencia | `VALIDATED` | **PARTIAL** |
| Aislamiento de BD | No verificado | **NO — BD oficial contaminada** |
| Limpieza `data/uploads/` | No verificada | **NO — archivos残留** |
| Modelo de estado | No canónico | **INVÁLIDO** (`DONE`/`VALIDATED` no existen) |

**Veredicto:** CAP-001 **NO está `DONE`/`VALIDATED`**. Estado real: **`IMPLEMENTED` / `PARTIAL`**.

---

## 2. Hallazgos detallados

### 2.1 Violación de ruta protegida — `engine/v4/`

**Archivo:** `engine/v4/ingestion/__init__.py` (nuevo, untracked)

**Evidencia:**
- `git status` muestra `engine/v4/ingestion/__init__.py` como **untracked** (archivo nuevo)
- No existe en commit base `795124b` (baseline certificado)
- Contiene `IngestionRegistry` que escribe en `ingestion_registry` y `file_registry`

**Regla violada:** §8 Plan Maestro — "Todo cambio protegido requiere: bug reproducible, evidencia antes del cambio, RFC, análisis de impacto, plan de rollback, prueba negativa, implementación quirúrgica, regresión, recertificación proporcional"

**Ninguno de estos pasos se ejecutó.**

---

### 2.2 Contaminación de BD oficial

**BD:** `data/db/meli_financial_v4.db`

| Métrica | Certificada (post-B2.5C) | Actual | Estado |
|---------|--------------------------|--------|--------|
| SHA-256 | `3939ad54...` | `bf6ed7ae...` | **MISMATCH** |
| `ingestion_registry` rows | 0 | 15 | +15 |
| `file_registry` rows | 0 | 23 | +23 |

**Causa:** Tests originales de CAP-001 (`test_upload_center_e2e.py` versión original) ejecutaron contra BD oficial sin aislamiento.

---

### 2.3 Contaminación `data/uploads/`

**Archivos residuales:** 23+ archivos CSV/XLSX de tests

**Causa:** Endpoint `/api/v4/ingestion/upload` usa `UPLOAD_DIR = Path("data/uploads")` hardcodeado; tests no limpiaban.

---

### 2.4 Modelo de estado no canónico

**`execution_board.json` reportaba:**
```json
"operational_status": "DONE",
"evidence_status": "VALIDATED"
```

**Estados válidos (Plan Maestro §6):** `NOT_STARTED` → `IMPLEMENTED` → `VALIDATED` → `VERIFIED` → `CERTIFIED`

**Estados inválidos usados:** `DONE`, `VERIFY`, `DOING`, `BLOCKED`, `READY`, `BACKLOG`

---

### 2.5 `generate_execution_board.py` genera estados inválidos

**Archivo:** `tools/generate_execution_board.py`

**Lógica defectuosa (líneas 196-204):**
```python
if c1["evidence_status"] == "VALIDATED":
    c1["operational_status"] = "DONE"  # ❌ Estado inválido
else:
    c1["evidence_status"] = "IMPLEMENTED"
    c1["operational_status"] = "IMPLEMENTED"
```

---

## 3. Remediación ejecutada

### 3.1 Tests aislados — `tests/conftest.py` + `test_upload_center_e2e.py`

**Fixtures nuevas:**
| Fixture | Propósito |
|---------|-----------|
| `temp_db_path` | Path único por test para DuckDB temporal |
| `isolated_db` | Patch `DatabaseV4.get()` + schema init en temp DB |
| `isolated_uploads` | Temp dir para uploads con cleanup automático |
| `isolated_app` | `TestClient` con `monkeypatch` en `api_module.UPLOAD_DIR` y `pe_module.UPLOADS_DIR` |

**Resultado:** `test_upload_center_e2e.py` **10/10 PASS** con aislamiento completo.

---

### 3.2 Corrección `execution_board.json`

**Archivos modificados:**
- `execution_board.json` — CAP-001 reclasificado
- `tools/generate_execution_board.py` — Lógica canónica

**Cambio en `execution_board.json` (CAP-001):**
```diff
- "operational_status": "DONE",
- "evidence_status": "VALIDATED",
+ "operational_status": "IMPLEMENTED",
+ "evidence_status": "PARTIAL",
+ "blocking_issue": "Tests contaminate official DB and data/uploads/; not isolated"
```

**Cambio en `generate_execution_board.py`:**
```python
# Solo estados canónicos
CANONICAL_OPERATIONAL = ["NOT_STARTED", "IMPLEMENTED", "VALIDATED", "VERIFIED", "CERTIFIED"]
CANONICAL_EVIDENCE = ["VALIDATED", "IMPLEMENTED", "PARTIAL", "NOT_STARTED"]

def _canonical_operational(status: str) -> str:
    mapping = {"DONE": "IMPLEMENTED", "VERIFY": "VALIDATED", "DOING": "IMPLEMENTED", 
               "BLOCKED": "IMPLEMENTED", "READY": "IMPLEMENTED", "BACKLOG": "NOT_STARTED"}
    return mapping.get(status, status if status in CANONICAL_OPERATIONAL else "IMPLEMENTED")
```

---

### 3.3 Documentación generada

| Archivo | Propósito |
|---------|-----------|
| `governance/coordination/executions/CAP001_CORRECTIVE_REVIEW.md` | Este documento |
| `governance/coordination/executions/REGRESSION_BASELINE.md` | Baseline 56 fallos categorizados |
| `governance/coordination/executions/PROTECTED_PATH_DIFF_REPORT.md` | Violación `engine/v4/` y contaminación BD |

---

## 4. Verificación post-remediación

### 4.1 Tests CAP-001 aislados
```
$ python -m pytest tests/test_upload_center_e2e.py -v
========================= 10 passed, 1 warning in 18.36s =========================
```

### 4.2 Estado `execution_board.json`
```json
{
  "cap_id": "CAP-001",
  "operational_status": "IMPLEMENTED",
  "evidence_status": "PARTIAL",
  "blocking_issue": "Tests contaminate official DB and data/uploads/; not isolated"
}
```

### 4.3 Generador canónico
```
$ python tools/generate_execution_board.py
Capabilities detected: 7
  IMPLEMENTED: 2
  VALIDATED: 1
  PARTIAL: 3
  NOT_STARTED: 1
```

---

## 5. Estado actual de CAP-001

| Criterio | Estado | Evidencia |
|----------|--------|-----------|
| Código implementado | ✅ IMPLEMENTED | `templates/upload_center.html`, `api/api.py` endpoints |
| Tests E2E pasan | ✅ 10/10 PASS | Con fixtures aislados |
| Aislamiento BD | ✅ IMPLEMENTED | Fixtures `isolated_db`, `isolated_uploads` |
| Limpieza uploads | ✅ IMPLEMENTED | Fixture `isolated_uploads` con cleanup |
| Estado operacional canónico | ✅ IMPLEMENTED | `execution_board.json` corregido |
| Estado evidencia canónico | ⚠️ PARTIAL | Tests pasan solo con aislamiento; BD oficial contaminada |
| 3 ejecuciones limpias | ❌ PENDIENTE | Requiere BD oficial restaurada |
| Ruta protegida `engine/v4/` | ❌ VIOLADA | `__init__.py` creado sin RFC |

---

## 6. Acciones pendientes para certificación

| # | Acción | Responsable | Deadline |
|---|--------|-------------|----------|
| 1 | Restaurar BD oficial desde snapshot `3939ad54` | Codex | Inmediato |
| 2 | Ejecutar 3 runs limpias consecutivas con BD restaurada | Codex | Post-restauración |
| 3 | Re-ejecutar suite completa (724 tests) | Codex | Post-restauración |
| 4 | Certificar CAP-001 si 3 runs limpias | Codex | Post-3-runs |

---

## 6. Conclusión

**CAP-001 está `IMPLEMENTED` / `PARTIAL` — NO `DONE` / `VALIDATED`.**

La remediación técnica (tests aislados, generador canónico, docs) está **completa**. Falta **restaurar BD oficial** y **3 ejecuciones limpias consecutivas** para alcanzar `VALIDATED` → `VERIFIED` → `CERTIFIED`.

**Recomendación:** Proceder con restauración de BD oficial (snapshots disponibles en `data/db/`). No avanzar a FASE 1 hasta certificación completa.