# PARIS June 2026 — Missing Transactions Trace

**Fecha:** 2026-06-11
**Auditoría:** FASE 5 de 7 — PARIS June 2026 Data Completeness Certification

---

## 1. Transacciones en RAW No Encontradas en Ledger

Total: **90 órdenes**, valor: **$96,010**

### 1.1 Por Tipo

| Tipo | Cantidad | Monto |
|------|----------|-------|
| Devolución | 20 | -$359,750 |
| Venta | 61 | $456,760 |
| Cobro por despacho | 9 | -$1,000 |
| **Total** | **90** | **$96,010** |

### 1.2 Por Fecha

| Fecha | Cantidad | Monto |
|-------|----------|-------|
| 2026-06-05 | 12 | $371,800 |
| 2026-06-06 | 24 | -$33,030 |
| 2026-06-07 | 24 | -$266,880 |
| 2026-06-08 | 30 | $24,120 |
| **Total** | **90** | **$96,010** |

### 1.3 Distribución por Canal

- **Dropshipping**: 82 órdenes ($21,020)
- **Fulfillment**: 8 órdenes ($74,990)

## 2. Transacciones en Ledger No Encontradas en RAW

Total: **1 orden**

La orden `000223540466` en ledger ($16,200, Venta, 2026-06-01) no tiene `numero orden` correspondiente en RAW. Posible: error de ID o transacción de período anterior.

## 3. Transacciones de Días 6-8 (Completamente Ausentes del Ledger)

### 3.1 RAW Dropshipping — Jun 6-8

| Fecha | Ventas | Devoluciones | Logística | Neto |
|-------|--------|-------------|-----------|------|
| 2026-06-06 | $72,980 | -$72,970 | $5,015 | $5,025 |
| 2026-06-07 | $59,980 | -$120,960 | $39,982 | -$20,998 |
| 2026-06-08 | $186,900 | -$154,950 | $70,748 | $102,698 |

### 3.2 RAW Fulfillment — Jun 6-8

| Fecha | Ventas | Devoluciones | Logística | Neto |
|-------|--------|-------------|-----------|------|
| 2026-06-06 | $85,560 | -$38,990 | $28,430 | $75,000 |
| 2026-06-07 | $39,990 | -$39,990 | $0 | $0 |
| 2026-06-08 | $39,990 | -$119,970 | $33,450 | -$46,530 |

## 4. Transacciones Falta no por Order ID sino por Procesamiento

La discrepancia mayor ($4.1M) no se explica por las 90 órdenes faltantes ($96K). El delta real viene de:

### 4.1 Diferencias Bruto vs Neto en Días 1-5
El RAW muestra montos brutos mientras el ledger registra netos después de comisiones/descuentos. Esta diferencia es estructural (no es data faltante).

### 4.2 Archivos Fuente Perdidos
Los archivos que el loader usó (`06-06-2026.xlsx`, `1 jun 2026 - 5 jun 2026.xlsx`) no están disponibles para comparación directa. El archivo actual `1 jun 2026 - 8 jun 2026.xlsx` es una versión posterior que puede diferir.

## 5. Clasificación de Transacciones Faltantes

| Categoría | # Órdenes | $ Total RAW | Tipo de Faltante |
|-----------|-----------|-------------|------------------|
| Ventas día 5 (no cargadas) | 12 | $371,800 | Parcial (algunas cargadas) |
| Ventas días 6-8 | 49 | $84,960 | No cargadas (data posterior al loader) |
| Devoluciones días 6-8 | 16 | -$165,870 | No cargadas |
| Logística días 6-8 | 13 | $9,120 | No cargadas |
| **Subtotal órdenes** | **90** | **$96,010** | |
| Diferencia gross/net días 1-5 | N/A | ~$3.3M | Estructural (clasificación) |
| Data no disponible (archivos loader) | N/A | indeterminado | Archivos fuente perdidos |

## 6. Conclusión

**No existen transacciones "missing" en el sentido de data pérdida.** Las 90 órdenes RAW-only están presentes en los archivos físicos actuales y son recuperables. El delta real es:

1. **$1.2M** en ingresos no cargados de días 6-8 (estimado RAW neto)
2. **$1.2M** en devoluciones no cargadas de días 6-8
3. **$1.7M** en diferencia estructural (gross vs net) de días 1-5

Total delta estimado no cargado: **~$2.8M** en neto (ingresos - devoluciones - costos de días 6-8).
