# PARIS June 2026 — RAW Economic Universe

**Fecha:** 2026-06-11
**Auditoría:** FASE 2 de 7 — PARIS June 2026 Data Completeness Certification
**Fuente:** `01_Raw/PARIS/Transacciones/Dropshipping/1 jun 2026 - 8 jun 2026.xlsx` + `01_Raw/PARIS/Transacciones/Fulfillment/1 jun 2026 - 8 jun 2026.xlsx`

---

## 1. Universo Combinado (DS + FF)

| Métrica | Dropshipping | Fulfillment | Total |
|---------|-------------|-------------|-------|
| Filas | 1,329 | 109 | **1,438** |
| Monto (Gross) | $20,638,719 | $1,160,490 | **$21,799,209** |
| Comisión Explícita | $13,992 | $1,008 | **$15,000** |
| Monto a Pagar (Net) | $17,114,498 | $962,344 | **$18,076,842** |
| Margen Implícito (Gross-Net) | $3,524,221 | $198,146 | **$3,722,367** |
| Margen % | 17.1% | 17.1% | **17.1%** |

## 2. Por Tipo de Transacción (DS)

| Tipo | Filas | Monto | Net |
|------|-------|-------|-----|
| Venta | 717 | $24,149,230 | $20,285,640 |
| Cobro por despacho | 528 | -$1,148,411 | -$1,186,950 |
| Devolución | 70 | -$2,362,100 | -$1,984,192 |
| Despacho | 14 | $0 | $0 |

## 3. Por Tipo de Transacción (FF)

| Tipo | Filas | Monto | Net |
|------|-------|-------|-----|
| Venta | 55 | $1,505,650 | $1,264,768 |
| Cobro por despacho | 46 | -$78,040 | -$78,040 |
| Devolución | 8 | -$267,120 | -$224,384 |

## 4. Por Día (DS + FF Combinado)

| Fecha | DS Filas | FF Filas | Gross | Net |
|-------|---------|---------|-------|-----|
| 2026-06-01 | 202 | 12 | $5,708,084 | $4,808,212 |
| 2026-06-02 | 189 | 11 | $5,118,956 | $4,218,576 |
| 2026-06-03 | 210 | 17 | $5,105,543 | $4,288,074 |
| 2026-06-04 | 262 | 21 | $4,491,865 | $3,721,476 |
| 2026-06-05 | 209 | 21 | $1,213,036 | $703,696 |
| 2026-06-06 | 101 | 11 | $80,025 | $119,368 |
| 2026-06-07 | 90 | 7 | -$20,998 | $67,800 |
| 2026-06-08 | 66 | 9 | $102,698 | $149,640 |
| **Total** | **1,329** | **109** | **$21,799,209** | **$18,076,842** |

## 5. Comisión Explícita

La comisión explícita es **$15,000 total** (DS: $13,992, FF: $1,008), que representa apenas el **0.07%** del gross. Consistente con hallazgos previos de que PARIS opera sin comisión marketplace explícita (modelo 1P dropshipping).

## 6. Observaciones

- **Gross total**: $21.8M para 8 días → promedio diario $2.7M/día
- **Net total**: $18.1M para 8 días → promedio diario $2.3M/día
- **Take rate implícito**: 17.1% (margen entre gross y net)
- **Los días 6-8** tienen montos significativamente menores que 1-5, indicando rezago en la fuente de datos (transacciones no liquidadas)
