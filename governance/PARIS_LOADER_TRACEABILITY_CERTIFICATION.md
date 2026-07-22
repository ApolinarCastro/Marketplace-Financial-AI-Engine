# PARIS — Loader Traceability Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 2 de 6 — PARIS Forensic Reconciliation V2
**Objetivo:** Demostrar documentalmente el origen de `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx`

---

## 1. Evidencia en Ledger (`archivo_origen`)

El ledger registra exactamente 2 archivos de origen para PARIS Junio 2026:

| archivo_origen | Filas | Monto | Fecha Min | Fecha Max |
|---------------|-------|-------|-----------|-----------|
| `06-06-2026.xlsx` | 1,002 | $16,409,208 | 2026-06-01 | 2026-06-05 |
| `1 jun 2026 - 5 jun 2026.xlsx` | 88 | $1,248,938 | 2026-06-01 | 2026-06-05 |

## 2. Evidencia Física en Disco

Búsqueda completa en `01_Raw/PARIS/` (Facturacion, Transacciones/Dropshipping, Transacciones/Fulfillment):

| Archivo Buscado | Estado |
|-----------------|--------|
| `06-06-2026.xlsx` | **NO EXISTE** ❌ |
| `1 jun 2026 - 5 jun 2026.xlsx` | **NO EXISTE** ❌ |

## 3. Archivo Físico Existente Más Parecido

| Subdirectorio | Archivo | Tamaño | Fecha Modificación |
|--------------|---------|--------|-------------------|
| Transacciones/Dropshipping/ | `1 jun 2026 - 8 jun 2026.xlsx` | 187 KB | 2026-06-09 12:36:40 |
| Transacciones/Fulfillment/ | `1 jun 2026 - 8 jun 2026.xlsx` | 21 KB | 2026-06-09 12:37:58 |

## 4. Evidencia en Metadata

| Atributo | `06-06-2026.xlsx` (referenciado) | `1 jun 2026 - 8 jun 2026.xlsx` (actual) |
|----------|----------------------------------|----------------------------------------|
| Fecha modificación | Desconocida (archivo inexistente) | 2026-06-09 12:36:40 |
| ¿Renombrado? | Posible | — |

## 5. Evidencia en Pipeline Log

No existe tabla `pipeline_log` con trazabilidad de carga para PARIS Junio 2026.

## 6. Evidencia en Archivos RAW de Otros Meses

El patrón de nombres de archivos históricos confirma que el loader usa archivos de período fijo:
- `05-2026.xlsx` → Mayo 2026 (nomenclatura `MM-YYYY.xlsx`)
- `04-2026.xlsx` → Abril 2026
- El archivo `06-06-2026.xlsx` **NO sigue el patrón** de nomenclatura (`MM-YYYY.xlsx` o `1 [rango] [año].xlsx`)
- `1 jun 2026 - 5 jun 2026.xlsx` sí sigue el patrón de rango parcial (similar a `1 jun 2026 - 8 jun 2026.xlsx`)

## 7. Respuestas

### ¿Existe evidencia física?
**NO.** ❌ Ninguno de los dos archivos existe físicamente en `01_Raw/PARIS/` ni en ningún subdirectorio.

### ¿Existe evidencia en audit trail?
**NO.** ❌ No existe `pipeline_log` ni tabla de trazabilidad que documente la carga de estos archivos.

### ¿Existe evidencia en metadata?
**PARCIAL.** ⚠️ El archivo actual `1 jun 2026 - 8 jun 2026.xlsx` tiene fecha de modificación 2026-06-09 (posterior a la carga original 2026-05-30/06-05), sugiriendo que es una versión posterior a la que usó el loader.

### ¿Existe evidencia en tablas de origen?
**SÍ.** ✅ La columna `archivo_origen` en `marketplace_ledger_v1` registra que estos dos archivos fueron cargados. La evidencia es **testimonial indirecta**: el ledger dice que existieron, pero los archivos ya no están.

## 8. Conclusión

Los archivos `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx` **existieron en el momento de la carga** (evidencia en ledger), pero **ya no existen** en disco. El archivo actual `1 jun 2026 - 8 jun 2026.xlsx` es una versión posterior (modificado 2026-06-09) que **no necesariamente coincide** con los archivos originales de la carga.

**No es posible verificar** que `1 jun 2026 - 8 jun 2026.xlsx` contenga exactamente la misma data que los archivos cargados originalmente.
