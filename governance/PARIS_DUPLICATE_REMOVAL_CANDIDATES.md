# PARIS DUPLICATE REMOVAL CANDIDATES
**Date:** 2026-06-07
**Source:** PARIS_DUPLICATES_FORENSIC_REPORT.md

---

## Universe Definition

**Criteria:** `id_orden` + `fecha` + `monto` + `financial_group` + `detalle` + `clasificacion_operativa` + `archivo_origen`

**Grouping guarantee:** Every row in a group has identical values across ALL economic columns + same source file.

**Total candidate groups:** 1,573
**Total rows:** 3,625
**Rows to KEEP:** 1,573 (one per group)
**Rows to REMOVE:** 2,052

---

## Q1: ¿Todas las filas provienen realmente del mismo archivo origen?

**SI** — Todas las candidate groups tienen exactamente el mismo `archivo_origen` dentro de cada grupo. 22 archivos origen distintos contribuyen a los 1,573 grupos:

| Archivo Origen | Grupos | % |
|---|---|---|
| `1 ene 2025 - 31 dic 2025.xlsx` | 628 | 39.9% |
| `10-2025.xlsx` | 105 | 6.7% |
| `12-2025.xlsx` | 85 | 5.4% |
| `04-2026.xlsx` | 78 | 5.0% |
| `1 ene 2026 - 30 abr 2026.xlsx` | 74 | 4.7% |
| `03-2026.xlsx` | 64 | 4.1% |
| `08-2025.xlsx` | 60 | 3.8% |
| `05-2026.xlsx` | 56 | 3.6% |
| `11-2025.xlsx` | 53 | 3.4% |
| `04-2025.xlsx` | 43 | 2.7% |
| `01-2026.xlsx` | 41 | 2.6% |
| `06-2025.xlsx` | 41 | 2.6% |
| `01-2025.xlsx` | 40 | 2.5% |
| `07-2025.xlsx` | 39 | 2.5% |
| `02-2025.xlsx` | 34 | 2.2% |
| `06-06-2026.xlsx` | 33 | 2.1% |
| `09-2025.xlsx` | 27 | 1.7% |
| `02-2026.xlsx` | 26 | 1.7% |
| `05-2025.xlsx` | 24 | 1.5% |
| `03-2025.xlsx` | 10 | 0.6% |
| `1 may 2026 - 31 may 2026.xlsx` | 9 | 0.6% |
| `1 jun 2026 - 5 jun 2026.xlsx` | 3 | 0.2% |

---

## Q2: ¿Existe alguna fila donde el evento económico sea distinto?

**NO** — Dentro de cada candidate group, todas las filas tienen EXACTAMENTE el mismo `financial_group`, `detalle`, y `clasificacion_operativa`.

**Excepciones parciales (monto=0):** 6 grupos excepcionales donde la misma `(id_orden, fecha, monto=0, archivo_origen)` tiene DISTINTOS `financial_group`:

| id_orden | fecha | monto | FG_1 | FG_2 | Source |
|---|---|---|---|---|---|
| 303550238 | 2025-08-05 | $0 | ingresos | devoluciones | 08-2025.xlsx |
| 301112061 | 2025-05-19 | $0 | ingresos | devoluciones | 05-2025.xlsx |
| 300873000 | 2025-05-06 | $0 | ingresos | devoluciones | 05-2025.xlsx |
| 309759280 | 2026-04-10 | $0 | ingresos | devoluciones | 04-2026.xlsx |
| 300858485 | 2025-05-05 | $0 | ingresos | devoluciones | 05-2025.xlsx |
| 276949841 | 2025-01-16 | $0 | ingresos | devoluciones | 01-2025.xlsx |

**Todas las 6 excepciones tienen monto=$0.** El impacto financiero de cualquier decisión errónea contra estas filas es **$0**. No representan riesgo material.

---

## Distribución por Financial Group

| Financial Group | Grupos | Filas totales | Filas removibles | Monto removible |
|---|---|---|---|---|
| ingresos | 1,082 | 2,563 | 1,481 | $26,228,900 |
| devoluciones | 193 | 421 | 228 | -$4,745,576 |
| costos_operacionales | 294 | 633 | 339 | -$567,920 |
| ajustes | 4 | 8 | 4 | -$323,554 |
| **TOTAL** | **1,573** | **3,625** | **2,052** | **$21,238,958** |

---

## Top 30 Groups by Amount

| id_orden | fecha | monto | financial_group | detalle | source | cnt |
|---|---|---|---|---|---|---|
| 0 | 2025-04-14 | $141,874 | ajustes | Ajuste Inventario Activo | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 0 | 2025-04-14 | $113,486 | ajustes | Ajuste Inventario Activo | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300531991 | 2025-04-17 | $64,491 | ingresos | Venta | 04-2025.xlsx | 2 |
| 309468787 | 2026-03-31 | $60,472 | ingresos | Venta | 03-2026.xlsx | 2 |
| 300598166 | 2025-04-22 | $60,191 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 302599596 | 2025-06-18 | $54,392 | ingresos | Venta | 06-2025.xlsx | 3 |
| 302599596 | 2025-06-26 | -$54,392 | devoluciones | Devolución | 06-2025.xlsx | 3 |
| 300655542 | 2025-04-26 | $51,591 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 3 |
| 300883513 | 2025-05-06 | $51,591 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 303125876 | 2025-07-15 | $50,992 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 3 |
| 301302606 | 2025-05-26 | $50,992 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 0 | 2026-04-17 | $49,283 | ajustes | Ajuste Inventario Activo | 1 ene 2026 - 30 abr 2026.xlsx | 2 |
| 300164854 | 2025-03-30 | $48,366 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 3 |
| 278013616 | 2025-03-26 | $48,366 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300712093 | 2025-04-29 | $48,151 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 4 |
| 311826879 | 2026-06-04 | $47,032 | ingresos | Venta | 06-06-2026.xlsx | 2 |
| 311724155 | 2026-06-04 | $47,032 | ingresos | Venta | 06-06-2026.xlsx | 2 |
| 277484094 | 2025-02-18 | $46,431 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300301509 | 2025-04-07 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300110979 | 2025-03-27 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300170152 | 2025-03-30 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300131965 | 2025-03-29 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300100540 | 2025-03-27 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 300344021 | 2025-04-07 | $45,141 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx | 2 |
| 309453745 | 2026-03-31 | $44,512 | ingresos | Venta | 03-2026.xlsx | 2 |
| 303862684 | 2025-08-20 | $43,991 | ingresos | Venta | 08-2025.xlsx | 2 |
| 303845608 | 2025-08-19 | $43,991 | ingresos | Venta | 08-2025.xlsx | 2 |
| 303856377 | 2025-08-20 | $43,991 | ingresos | Venta | 08-2025.xlsx | 2 |
| 309279361 | 2026-03-25 | $43,672 | ingresos | Venta | 1 ene 2026 - 30 abr 2026.xlsx | 2 |
| 310881534 | 2026-05-26 | $43,672 | ingresos | Venta | 1 may 2026 - 31 may 2026.xlsx | 2 |

---

## Largest Groups by Count

| cnt | id_orden | monto | financial_group | detalle | source |
|---|---|---|---|---|---|
| **81** | 0 | -$2,690 | costos_operacionales | Logística inversa | 1 ene 2026 - 30 abr 2026.xlsx |
| 17 | 302998803 | $29,742 | ingresos | Venta | 07-2025.xlsx |
| 9 | 300164854 | $0 | ingresos | Venta | 1 ene 2025 - 31 dic 2025.xlsx |
| 8 | 309896134 | $10,192 | ingresos | Venta | 04-2026.xlsx |
| 7 | 308180755 | $8,492 | ingresos | Venta | 01-2026.xlsx |

---

## Conclusión FASE 1

**1,573 grupos candidatos con 100% de homogeneidad económica dentro de cada grupo.**

- 0% riesgo de eliminar eventos económicos distintos
- 6 excepciones con monto=$0 (riesgo $0)
- 22 archivos fuente distintos, cada grupo homogéneo por archivo
- Eliminación = KEEP 1, REMOVE N-1 por grupo
