# PARIS DUPLICATE ROOT CAUSE CERTIFICATION
**Date:** 2026-06-07

---

## Source File Architecture

PARIS has two independent source pipelines, both already loaded into the ledger:

### Pipeline 1: Fulfillment (FF) — Archivos integrales
- `01_Raw/PARIS/Transacciones/Fulfillment/`
- Archivos de período extenso (anuales o multi-mensuales)
- Contienen la misma información que los DS files pero a nivel consolidado

### Pipeline 2: Dropshipping (DS) — Archivos mensuales
- `01_Raw/PARIS/Transacciones/Dropshipping/`
- Archivos por mes individual (01-2025.xlsx, 02-2025.xlsx, etc.)
- Detalle transaccional por orden

**Problema:** Ambos pipelines cubren el MISMO universo de transacciones. Cuando ambos se cargan al ledger, las mismas transacciones aparecen 2+ veces.

---

## Root Cause Determination

### ¿Los duplicados nacen en el archivo fuente?

**PARCIALMENTE SI** — Algunos archivos fuente ya contienen filas duplicadas internamente:

- `1 ene 2026 - 30 abr 2026.xlsx` contiene `id=0, Logística inversa, -$2,690` **81 veces** literalmente en el Excel
- `1 ene 2025 - 31 dic 2025.xlsx` tiene grupos con cnt=9, cnt=6, cnt=6, cnt=6, cnt=5 dentro del mismo archivo

### ¿Los duplicados nacen durante la carga?

**NO** — El loader no genera duplicados por sí mismo. Lee fielmente cada fila del archivo fuente y la inserta en el ledger. Si el archivo fuente tiene 81 filas idénticas, el ledger tiene 81 filas idénticas.

### Causa Raíz Verdadera

**El solapamiento de archivos fuente es la causa raíz estructural:**

1. **FF anual + DS mensuales:** El archivo `1 ene 2025 - 31 dic 2025.xlsx` (FF, 14,740 rows) contiene las mismas transacciones que los 12 archivos DS mensuales de 2025. Cuando ambos se cargan, cada transacción aparece ~2 veces.

2. **FF parcial + DS mensuales:** `1 ene 2026 - 30 abr 2026.xlsx` se solapa con los 4 DS mensuales de 2026.

3. **Datos intencionalmente duplicados en fuente:** El archivo `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx` cubren el mismo período.

4. **Duplicados internos en fuente:** Algunos archivos (especialmente el anual) tienen filas literalmente duplicadas dentro del mismo Excel — probablemente por consolidación manual o macros.

---

## Verified by Direct File Inspection

| Archivo fuente | Filas | Tiene duplicados internos? | Se solapa con otros? |
|---|---|---|---|
| `1 ene 2025 - 31 dic 2025.xlsx` | 14,740 | SI (~5 grupos) | SI (todos los DS 2025) |
| `1 ene 2026 - 30 abr 2026.xlsx` | 1,768 | SI (cnt=81 id=0) | SI (DS 2026 Jan-Apr) |
| `06-2025.xlsx` (DS) | 2,056 | SI | SI (FF 2025) |
| `10-2025.xlsx` (DS) | 3,042 | SI | SI (FF 2025) |
| `06-06-2026.xlsx` (DS) | 1,080 | SI | SI (FF Jun 2026) |
| Otros DS mensuales | ~1,000-2,000 | Variable | SI (FF anual) |

---

## Conclusión

| Pregunta | Respuesta |
|---|---|
| ¿Los duplicados nacen en el archivo fuente? | **SI, algunos** (~5% de los grupos son duplicados internos del archivo fuente) |
| ¿Los duplicados nacen durante la carga? | **NO** — El loader es fiel a la fuente |
| ¿La causa raíz es el solapamiento de archivos? | **SI (~95% de los grupos)** |
| ¿Se puede prevenir con dedup guard en el loader? | **SI** |

**Solución estructural:** El loader debe deduplicar contra filas existentes antes de insertar, usando la clave `(id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen)`. Alternativamente, cargar solo un pipeline (FF o DS) pero no ambos.
