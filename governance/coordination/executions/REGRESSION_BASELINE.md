# REGRESSION_BASELINE.md

**Fecha:** 2026-07-15  
**Fase:** FASE 0 — CONTENCIÓN Y ESTABILIZACIÓN  
**Ejecución:** `python -m pytest -v --tb=no -q` (724 tests recolectados)  
**Resultado:** **56 failed, 648 passed, 20 skipped** (121.74s)

---

## 1. Resumen por categoría

| Categoría | Fallos | % del total | Causa raíz |
|-----------|--------|-------------|------------|
| **Connection closed** | 31 | 55.4% | Tests usan BD oficial sin aislamiento; conexión se cierra entre tests |
| **NaN en certification** | 7 | 12.5% | `_certify_coverage` intenta `int(NaN)` cuando no hay datos clasificados |
| **Regresión contractual** | 3 | 5.4% | Deltas financieros no cero (ej. ML cargo venta diff $27.8M) |
| **Pipeline quirúrgico** | 2 | 3.6% | BD contaminada + conexión cerrada |
| **Inmutabilidad SQL** | 1 | 1.8% | Test bloqueo INSERT/UPDATE/DELETE espera error pero recibe 404 |
| **Inteligencia ejecutiva** | 1 | 1.8% | Driver insight retorna 0 drivers (datos no cargados) |
| **Otros** | 11 | 19.6% | Varios (clasificación París, pipelines, etc.) |

---

## 2. Detalle por archivo de test

| Archivo | Tests | Fallos | Categoría principal |
|---------|-------|--------|---------------------|
| `test_golden.py` | 48 | 31 | Connection closed (31) |
| `test_certification.py` | 11 | 7 | NaN en certification (7) |
| `test_closing.py` | 4 | 3 | Connection closed (3) |
| `test_v4_surgical_pipeline.py` | 1 | 1 | Connection closed (1) |
| `test_regression_contracts.py` | 14 | 3 | Regresión contractual (3) |
| `test_reconciliation_engine.py` | 78 | 1 | Regresión contractual (1) |
| `test_executive_intelligence.py` | 6 | 1 | Inteligencia ejecutiva (1) |
| `test_paris_classification.py` | 2 | 1 | Otros (1) |
| `test_v4_surgical_pipeline.py` | 1 | 1 | Pipeline quirúrgico (1) |

---

## 3. Análisis de causa raíz

### 3.1 Connection closed (31 fallos — 55.4%)

**Síntoma:** `_duckdb.ConnectionException: Connection already closed!`

**Causa:** Tests usan `DatabaseV4.get()` que retorna conexión a BD oficial (`data/db/meli_financial_v4.db`). La conexión se cierra implícitamente (context manager, timeout, o test anterior) y test siguiente falla.

**Tests afectados (ejemplos):**
- `test_golden.py::test_golden_exec_summary[ML]` through `[ALL]` (5 fallos)
- `test_golden.py::test_golden_waterfall[ML]` through `[ALL]` (5 fallos)
- `test_golden.py::test_golden_ledger[ML]` through `[ALL]` (5 fallos)
- `test_golden.py::test_golden_financial_structure[ML]` through `[ALL]` (5 fallos)
- `test_golden.py::test_stability_exec_summary[0-9]` (10 fallos)
- `test_golden.py::test_stability_waterfall[0-9]` (10 fallos)
- `test_closing.py` (3 fallos)
- `test_v4_surgical_pipeline.py` (1 fallo)

**Solución:** Tests deben usar fixtures aislados (`isolated_db`, `temp_db_path`) como en `test_upload_center_e2e.py` corregido.

---

### 3.2 NaN en certification (7 fallos — 12.5%)

**Síntoma:** `ValueError: cannot convert float NaN to integer` en `certification_engine.py:182`

**Código problemático:**
```python
classified = int(df.iloc[0]["classified"]) if not df.empty else 0
```

**Causa:** `_certify_coverage` consulta tabla `marketplace_ledger_clasificado_v1` para marketplace ML. Como BD oficial tiene datos pero tabla clasificada está vacía para ML (los datos ML no se clasifican correctamente), `df.iloc[0]["classified"]` retorna `NaN`.

**Tests afectados:**
- `test_certify_ml`
- `test_all_claims_have_evidence`
- `test_pass_rate_between_0_and_100`
- `test_ingresos_claim_present`
- `test_devoluciones_claim_present`
- `test_classification_coverage_claim_present`
- `test_operational_pnl_claim_present`

---

### 3.3 Regresión contractual (3 fallos — 5.4%)

| Test | Delta | Detalle |
|------|-------|---------|
| `test_ml_cargo_venta` | $27,882,800 | ALL-rows DIFF |
| `test_insert_update_delete_blocked` | 404 vs error esperado | SQL bloqueado debería dar error, retorna 404 |
| `test_level2_ml_source_total` | $12,029,600 | Source total = 0.0 vs target $12M |

---

### 3.4 Pipeline quirúrgico (2 fallos — 3.6%)

| Test | Error |
|------|-------|
| `test_full_pipeline_ingestion_classification_and_audit` | Connection already closed |
| `test_paris_classification.py::test_recursive_glob_ingests_from_subdirectories` | Connection already closed |

---

### 3.4 Inmutabilidad SQL (1 fallo — 1.8%)

**Test:** `test_insert_update_delete_blocked`

**Esperado:** SQL INSERT/UPDATE/DELETE → error 400/500  
**Real:** 404 Not Found (ruta no existe)

**Causa:** Endpoint de prueba no montado o ruta incorrecta en test.

---

### 3.5 Inteligencia ejecutiva (1 fallo — 1.8%)

**Test:** `test_driver_insight`

**Error:** `assert 0 >= 1` — driver insight retorna lista vacía.

**Causa:** Datos no cargados en BD de test (usa BD oficial vacía para ese contexto).

---

## 4. Baseline de comparación

| Métrica | Valor actual | Valor objetivo (post-remediación) |
|---------|--------------|-----------------------------------|
| Tests totales | 724 | 724 |
| Pasados | 648 | 724 |
| Fallados | 56 | 0 |
| Omitidos | 20 | 20 |
| Tiempo total | 121.74s | < 60s |

---

## 4. Plan de remediación por prioridad

| Prioridad | Acción | Tests afectados | Esfuerzo |
|-----------|--------|-----------------|----------|
| **P0** | Fixtures aislados para todos los tests que tocan BD | 31 (connection closed) | Alto |
| **P0** | Fix `_certify_coverage` NaN handling | 7 (certification) | Bajo |
| **P1** | Restaurar BD oficial desde snapshot certificado | 3 (regresión contractual) | Medio |
| **P1** | Fix endpoint SQL blocking test | 1 | Bajo |
| **P2** | Fix driver insight data loading | 1 | Medio |
| **P2** | Tests París classification | 1 | Medio |

---

## 5. Criterio de salida FASE 0

- [ ] BD oficial restaurada (hash `3939ad54...`)
- [ ] 724 tests PASS (0 fallos)
- [ ] CAP-001 reclasificado a `IMPLEMENTED`/`PARTIAL`
- [ ] `execution_board.json` con estados canónicos
- [ ] Documentación `PROTECTED_PATH_DIFF_REPORT.md`, `REGRESSION_BASELINE.md`, `CAP001_CORRECTIVE_REVIEW.md` completados
- [ ] RC1 verificado (N/A — no existe `engine/rc1/`)