# PARIS DUPLICATE FINANCIAL SIMULATION
**Date:** 2026-06-07
**Method:** Virtual dedup via `ROW_NUMBER() OVER (PARTITION BY id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen)` — KEEP 1, REMOVE N-1.

**No DELETE executed. No DB modified.**

---

## Global Impact

| Concepto | ACTUAL | SIMULADO | DELTA |
|---|---|---|---|
| **Ventas (ingresos)** | $484,161,942 | $457,933,042 | **-$26,228,900** |
| **Devoluciones** | -$121,458,109 | -$116,712,533 | **+$4,745,576** |
| **Cobro por despacho** | -$21,625,080 | -$21,509,080 | **+$116,000** |
| **Logística inversa** | -$3,088,120 | -$2,749,200 | **+$338,920** |
| **Otros costos operacionales** | -$1,947,438 | -$1,834,438 | **+$113,000** |
| **Total costos operacionales** | -$26,660,638 | -$26,092,718 | **+$567,920** |
| **Ajustes** | $1,375,357 | $1,051,803 | **-$323,554** |
| **Resultado Neto** | **$337,418,552** | **$316,179,594** | **-$21,238,958** |

**Delta Sum Check:** ing(-26,228,900) + dev(+4,745,576) + cop(+567,920) + aju(-323,554) = **RN(-21,238,958)** ✅

---

## Impact by Financial Group

| Financial Group | ACTUAL | SIMULADO | DELTA |
|---|---|---|---|
| ingresos | $484,161,942 | $457,933,042 | -$26,228,900 |
| devoluciones | -$121,458,109 | -$116,712,533 | +$4,745,576 |
| costos_operacionales | -$26,660,638 | -$26,092,718 | +$567,920 |
| ajustes | $1,375,357 | $1,051,803 | -$323,554 |
| **TOTAL** | **$337,418,552** | **$316,179,594** | **-$21,238,958** |

---

## Impact by Month

| Periodo | RN Actual | RN Simulado | Delta RN |
|---|---|---|---|
| 2025-01 | $9,746,025 | $8,773,070 | -$972,955 |
| 2025-02 | $7,605,672 | $6,954,111 | -$651,561 |
| 2025-03 | $21,906,600 | $19,916,635 | -$1,989,965 |
| 2025-04 | $17,972,977 | $16,653,691 | -$1,319,286 |
| 2025-05 | $20,866,723 | $19,759,564 | -$1,107,159 |
| 2025-06 | $38,651,771 | $36,967,006 | -$1,684,765 |
| 2025-07 | $25,959,233 | $24,156,293 | -$1,802,940 |
| 2025-08 | $8,995,620 | $8,412,192 | -$583,428 |
| 2025-09 | $14,885,894 | $14,179,411 | -$706,483 |
| 2025-10 | $38,673,811 | $36,043,496 | -$2,630,315 |
| 2025-11 | $37,475,230 | $35,548,774 | -$1,926,456 |
| 2025-12 | $21,910,994 | $20,930,001 | -$980,993 |
| 2026-01 | $5,446,503 | $4,820,831 | -$625,672 |
| 2026-02 | $7,426,410 | $7,025,333 | -$401,077 |
| 2026-03 | $16,242,892 | $15,088,880 | -$1,154,012 |
| 2026-04 | $17,731,313 | $16,628,512 | -$1,102,801 |
| 2026-05 | $8,262,738 | $7,598,936 | -$663,802 |
| 2026-06 | $17,658,146 | $16,722,858 | -$935,288 |

**Todos los 18 meses tienen delta negativo.** Ningún período se beneficia o perjudica desproporcionadamente.

---

## Impact by Concept (detalle)

| Detalle | Financial Group | ACTUAL | SIMULADO | DELTA |
|---|---|---|---|---|
| Venta | ingresos | $483,888,712 | $457,659,812 | -$26,228,900 |
| Devolución | devoluciones | -$121,458,109 | -$116,712,533 | +$4,745,576 |
| Cobro por despacho | costos_operacionales | -$21,625,080 | -$21,509,080 | +$116,000 |
| Logística inversa | costos_operacionales | -$3,088,120 | -$2,749,200 | +$338,920 |
| Retiro stock bodega Paris | costos_operacionales | -$1,630,800 | -$1,630,800 | $0 |
| Compensación logística | ajustes | $1,618,057 | $1,618,057 | $0 |
| Ajuste Inventario Activo | ajustes | $647,108 | $647,108 | $0 |
| Cargo | ajustes | -$646,295 | -$322,741 | +$323,554 |
| Cobro stock antiguo | costos_operacionales | -$316,638 | -$316,638 | $0 |
| Rebate | ingresos | $273,230 | $273,230 | $0 |
| Cobro por campaña | ajustes | -$260,504 | -$260,504 | $0 |
| Merma | ajustes | $16,991 | $16,991 | $0 |

*Nota: Los conceptos con $0 delta no tenían duplicados en sus grupos.*

---

## Verification Delta = -$21,238,958 ✅

**Fórmula:** `RN_delta = ing_delta + dev_delta + cop_delta + aju_delta`
`= (-26,228,900) + (+4,745,576) + (+567,920) + (-323,554) = -21,238,958`
