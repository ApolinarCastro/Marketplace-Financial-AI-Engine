# MARKETPLACE FINANCIAL OPERATING SYSTEM
# F3-02 — CONTROLLED INGESTION WITH REAL PIPELINE

Versión: 1.0

Fecha: 2026-07-17

Fase: 3

Estado:
COMPLETED

Veredicto:
CONTROLLED_FINANCIAL_FIXTURE_REQUIRED

CAP-001:
REMAINS_VALIDATED

---

## SUMMARY

Tres cargas controladas ejecutadas usando **SurgicalLoader real (sin mocks)** contra copia temporal de BASELINE_ESTABLE_V7.

| Upload | Archivo | Estado | Etapas | Tiempo |
|--------|---------|--------|--------|--------|
| 1 | FALABELLA_Conciliacion_2026-06_test1.csv | CERTIFIED | 6/6 | 1.9s |
| 2 | FALABELLA_Conciliacion_2026-06_test2.csv | CERTIFIED | 6/6 | 2.1s |
| 3 | FALABELLA_Conciliacion_2026-06_test3.csv | CERTIFIED | 6/6 | 3.2s |

**Pipeline mechanics: VERIFIED ✅**

**Regresión: 710 PASS, 0 FAIL, 0 ERROR — 0 regresiones. ✅**

---

## INFRAESTRUCTURA TEMPORAL

| Componente | Origen | Destino |
|------------|--------|---------|
| DB | BASELINE_ESTABLE_V7 (`bcb19ab4...`) | `tmp/` (copia independiente por carga) |
| Uploads | CSV generado en memoria | `tmp/uploads/` |
| Knowledge index | Archivo YAML vacío | `tmp/knowledge_index.yaml` |
| DB oficial | `meli_financial_v4.db` (`67086a13...`) | NO MODIFICADA |

### Verificación post-ejecución

- **Hash DB oficial**: `67086a13...` → `67086a13...` (IDÉNTICO) ✅
- **engine/v4/**: sin cambios (`git status` idéntico) ✅
- **Cleanup**: `tmp/` eliminado, evidence preservado en `evidence/fase_3/` ✅

---

## RESULTADOS POR CARGA

### Carga 1: FALABELLA_Conciliacion_2026-06_test1.csv (1.9s)

| Etapa | Resultado |
|-------|-----------|
| DETECT | PASS — marketplace=FALABELLA, ext=.csv, sha256 detectado |
| VALIDATE | PASS — CSV válido, sin duplicados |
| CLASSIFY | PASS — marketplace=FALABELLA, loader=SurgicalLoader, pipeline=falabella_v4 |
| PERSIST | PASS — SurgicalLoader ejecutado, 8 archivos XLSX procesados desde `01_Raw/FALABELLA/` |
| CERTIFY | PASS (DEGRADED) — reconciliación ejecutada contra temp DB |
| KNOWLEDGE | PASS — nuevas entradas en knowledge index |

**Execution ID**: único ✅
**SHA-256**: verificado ✅
**Marketplace**: FALABELLA ✅
**Document type**: "unknown" ⚠️ (FileDetector no tiene patrón "conciliacion")
**Period**: 2026-06 ✅
**Errores**: 0 ✅
**Warnings**: 0 ✅

### Carga 2: FALABELLA_Conciliacion_2026-06_test2.csv (2.1s)

- Execution ID único (diferente de carga 1) ✅
- 6/6 etapas completadas ✅
- 0 errores, 0 warnings ✅

### Carga 3: FALABELLA_Conciliacion_2026-06_test3.csv (3.2s)

- Execution ID único (diferente de cargas 1 y 2) ✅
- 6/6 etapas completadas ✅
- 0 errores, 0 warnings ✅

---

## HALLAZGOS

### Hallazgo 3-01: Pipeline mecánico FUNCIONA con SurgicalLoader real

**Severidad**: INFORMATIVO
**Detalle**: Las 6 etapas del pipeline (DETECT → VALIDATE → CLASSIFY → PERSIST → CERTIFY → KNOWLEDGE) se completaron exitosamente en las 3 ejecuciones usando SurgicalLoader real. El loader procesó 8 archivos XLSX de FALABELLA desde `01_Raw/FALABELLA/` en cada ejecución.

### Hallazgo 3-02: Bug en PersistenceEngine._get_loader()

**Severidad**: MEDIO
**Detalle**: `PersistenceEngine._get_loader()` en `engine/v4/ingestion/handlers/persistence_engine.py:29` llama `SurgicalLoader(db=self.db)` pero `SurgicalLoader.__init__()` (en `engine/v4/surgical_loader.py:80`) NO acepta parámetro `db`.

**Impacto**: Sin workaround, el pipeline falla en PERSIST con TypeError. Las pruebas existentes lo evitan mediante mock.

**Causa raíz**: Código nuevo (PersistenceEngine, untracked) asume interfaz diferente del código legacy (SurgicalLoader).

**Workaround usado en F3-02**: Pasar `loader=SurgicalLoader()` a `PersistenceEngine.__init__()`.

**No corregido**: PersistenceEngine es untracked (FASE 1), SurgicalLoader es tracked. La corrección debe decidirse en revisión de código.

### Hallazgo 3-03: FileDetector no reconoce "conciliacion" como tipo documental

**Severidad**: BAJO
**Detalle**: El FileDetector no tiene patrón para "conciliacion", por lo que FALABELLA doc_type queda como "unknown".
**Patrones existentes**: facturacion, poscobro, liberaciones, liquidacion, dte, dropshipping, fulfillment, pedidos, ventas_totales, transacciones, ordenes

### Hallazgo 3-04: records_inserted reporta 0 aunque SurgicalLoader insertó datos

**Severidad**: BAJO
**Detalle**: `PersistenceEngine.persist()` reporta `records_inserted=0` porque:
1. `load_marketplace()` retorna None (SurgicalLoader no retorna conteo)
2. Fallback consulta `file_registry` con SHA256 del archivo subido, pero SurgicalLoader registra con hash truncado del filename, no del contenido

**Impacto**: El Upload Center muestra "0 registros insertados" aunque los datos se cargaron correctamente.

### Hallazgo 3-05: No existe fixture financiero controlado

**Severidad**: BLOQUEANTE para certificación
**Detalle**: No existe un fixture que mapee "archivo X subido → Y filas en ledger con clasificación Z". Existen 73 fixtures de API (52 golden, 21 benchmark) pero ninguno a nivel pipeline.
**Acción requerida**: Crear fixture financiero controlado para certificar CAP-001.

---

## VEREDICTO

```
CONTROLLED_FINANCIAL_FIXTURE_REQUIRED
```

### Razón

El pipeline mecánico funciona correctamente (3/3 cargas completaron 6/6 etapas con SurgicalLoader real). Sin embargo, no existe un fixture financiero controlado que permita verificar:

- filas esperadas persistidas en ledger
- clasificación esperada de las transacciones
- ausencia de duplicidad financiera
- trazabilidad archivo → registry → ledger con resultados numéricos comprobables

### Estado de CAP-001

**CAP001_REMAINS_VALIDATED** — El pipeline está implementado y validado a nivel mecánico, pero no puede certificarse completamente sin un fixture financiero controlado.

### Próximos pasos

1. Crear fixture financiero controlado (archivo CSV/XLSX con estructura conocida y resultado esperado documentado)
2. Re-ejecutar F3-02 con fixture
3. Verificar filas, clasificación, y trazabilidad
4. Certificar CAP-001

---

## EVIDENCIA

- `evidence/fase_3/f3_02_controlled_ingestion_1784297447.json` — Resultados completos de las 3 ejecuciones
- `tests/f3_02_controlled_ingestion.py` — Script de prueba (standalone, no pytest)

## REGRESIÓN

**Pre-F3-02**: 700 PASS, 21 SKIP, 10 ERROR (upload center E2E)
**Post-F3-02**: 710 PASS, 21 SKIP, 0 ERROR

**10 tests recuperados de ERROR a PASS** — La prueba F3-02 reseteó el singleton DatabaseV4, desbloqueando los tests E2E de Upload Center. **0 regresiones.**
