# PARIS June 2026 — Ledger Economic Universe

**Fecha:** 2026-06-11
**Auditoría:** FASE 3 de 7 — PARIS June 2026 Data Completeness Certification
**Fuente:** `data/db/meli_financial_v4.db` → `marketplace_ledger_v1`

---

## 1. Total PARIS en Ledger (Todo Período)

**$337,418,552**

## 2. Junio 2026 en Ledger

| Métrica | Valor |
|---------|-------|
| Filas | 1,090 |
| Total Monto | $17,658,146 |
| Ingresos | $19,018,872 |
| Devoluciones | -$526,856 |
| Costos Operacionales | -$833,870 |
| Ajustes | $0 |

## 3. Por Día

| Fecha | Filas | Ingresos | Devoluciones | Costos Op. |
|-------|-------|---------|-------------|------------|
| 2026-06-01 | 207 | $5,043,304 | -$103,288 | -$11,760 |
| 2026-06-02 | 240 | $4,973,632 | -$104,952 | -$117,720 |
| 2026-06-03 | 263 | $4,571,952 | -$52,064 | -$183,610 |
| 2026-06-04 | 301 | $4,040,304 | -$180,056 | -$269,210 |
| 2026-06-06 | 79 | $389,680 | -$86,496 | -$251,570 |
| **Total** | **1,090** | **$19,018,872** | **-$526,856** | **-$833,870** |

## 4. Por Detalle

| Detalle | Financial Group | Filas | Monto |
|---------|----------------|-------|-------|
| Venta | ingresos | 681 | $19,018,872 |
| Cobro por despacho | costos_operacionales | 376 | -$833,870 |
| Devolución | devoluciones | 20 | -$526,856 |
| Despacho | ingresos | 13 | $0 |

## 5. Archivos de Origen (Loader Trace)

| Archivo | Filas | Monto | Período |
|---------|-------|-------|---------|
| `06-06-2026.xlsx` | 1,002 | $16,409,208 | 2026-06-01 a 2026-06-05 |
| `1 jun 2026 - 5 jun 2026.xlsx` | 88 | $1,248,938 | 2026-06-01 a 2026-06-05 |

## 6. Hallazgos Críticos

### 6.1 Fechas Faltantes en Ledger

| Fecha | RAW | Ledger | Estado |
|-------|-----|--------|--------|
| 2026-06-01 | ✅ 214 filas | ✅ 207 filas | OK |
| 2026-06-02 | ✅ 200 filas | ✅ 240 filas | OK (RAW tiene menos?) |
| 2026-06-03 | ✅ 227 filas | ✅ 263 filas | OK |
| 2026-06-04 | ✅ 283 filas | ✅ 301 filas | OK |
| 2026-06-05 | ✅ 230 filas | ✅ 79 filas | Parcial |
| 2026-06-06 | ✅ 112 filas | ❌ 0 filas | **FALTANTE** |
| 2026-06-07 | ✅ 97 filas | ❌ 0 filas | **FALTANTE** |
| 2026-06-08 | ✅ 75 filas | ❌ 0 filas | **FALTANTE** |
| 2026-06-09 a 30 | ❌ No hay RAW | ❌ 0 filas | **SIN DATOS** |

### 6.2 Archivos Fuente No Rastreables

- El archivo `06-06-2026.xlsx` (1,002 filas, $16.4M) **NO EXISTE en disco**
- El archivo `1 jun 2026 - 5 jun 2026.xlsx` (88 filas, $1.2M) **NO EXISTE en disco**
- Ambos fueron renombrados/fusionados en `1 jun 2026 - 8 jun 2026.xlsx` (1,438 filas)

### 6.3 Período Cubierto vs Período Real

El ledger tiene data solo hasta **2026-06-05** (5 días). Junio tiene 30 días. **83% del mes está ausente** del ledger.
