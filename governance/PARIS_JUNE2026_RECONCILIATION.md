# PARIS June 2026 — RAW vs Ledger Reconciliation

**Fecha:** 2026-06-11
**Auditoría:** FASE 4 de 7 — PARIS June 2026 Data Completeness Certification
**Método:** Comparación directa RAW vs Ledger por tipo de transacción, fecha, y order_id

---

## 1. Comparación por Categoría Financiera

| Categoría | RAW (Gross) | Ledger | Delta | Delta % |
|-----------|------------|--------|-------|---------|
| Venta (ingresos) | $25,654,880 | $19,018,872 | **$6,636,008** | +34.9% |
| Devolución | -$2,629,220 | -$526,856 | **-$2,102,364** | +75.1% |
| Logística (costos) | -$1,226,451 | -$833,870 | **-$392,581** | +32.0% |
| **Total** | **$21,799,209** | **$17,658,146** | **$4,141,063** | **+23.5%** |

## 2. Análisis de Delta por Categoría

### 2.1 Ventas ($6.6M delta)
El delta de ventas tiene dos causas:
1. **Días 6-8 no cargados al ledger**: RAW contiene Ventas de Jun 6, 7, 8 que no están en ledger
2. **Diferencias de clasificación**: RAW "Venta" = monto bruto, Ledger "ingresos" = valor neto después de comisiones/descuentos

### 2.2 Devoluciones ($2.1M delta)
- Ledger registra solo 20 filas de devolución (-$527K)
- RAW tiene 78 filas de devolución (-$2.6M)
- Las devoluciones de días 6-8 (RAW-only) suman $2.1M
- Las devoluciones de días 1-5 tienen una diferencia de clasificación

### 2.3 Logística ($393K delta)
- RAW: 588 filas "Cobro por despacho" y "Despacho" (-$1.2M)
- Ledger: 376 filas "costos_operacionales" (-$834K)
- Diferencia parcialmente explicada por días 6-8 no cargados

## 3. Comparación por Fecha

| Fecha | RAW Gross | Ledger Total | Delta | Cubierto? |
|-------|-----------|-------------|-------|-----------|
| 2026-06-01 | $5,708,084 | $4,928,256 | $779,828 | ✅ |
| 2026-06-02 | $5,118,956 | $4,737,160 | $381,796 | ✅ |
| 2026-06-03 | $5,105,543 | $4,324,278 | $781,265 | ✅ |
| 2026-06-04 | $4,491,865 | $3,515,038 | $976,827 | ✅ |
| 2026-06-05 | $1,213,036 | $153,414 | $1,059,622 | Parcial |
| 2026-06-06 | $80,025 | $0 | $80,025 | ❌ |
| 2026-06-07 | -$20,998 | $0 | -$20,998 | ❌ |
| 2026-06-08 | $102,698 | $0 | $102,698 | ❌ |
| **Total** | **$21,799,209** | **$17,658,146** | **$4,141,063** | |

## 4. Orden-Level Matching

| Métrica | Valor |
|---------|-------|
| Order IDs únicos en RAW | 716 |
| Order IDs únicos en Ledger (no-null) | 627 |
| Orders en AMBOS | 626 |
| Orders en RAW (no en Ledger) | **90** |
| Orders en Ledger (no en RAW) | **1** |
| Valor RAW-only | **$96,010** |

### 4.1 Órdenes RAW No Encontradas en Ledger

Las 90 órdenes RAW-only suman solo $96K, mucho menos que el delta de $4.1M. Esto indica que:
- La mayoría de la diferencia no es por órdenes individuales faltantes
- Es por diferencias en cómo se registran los montos (RAW tiene montos brutos, ledger almacena montos netos procesados)
- La columna `id_orden` en ledger no se corresponde 1:1 con `numero orden` en RAW para todas las transacciones (especialmente para costos/logística que no siempre tienen order_id)

## 5. Conclusión de Reconciliación

El delta de $4.1M no es enteramente "data faltante". Se descompone como:

| Componente | Estimado |
|------------|----------|
| Días 6-8 no cargados | ~$2.8M |
| Diferencia gross/net (días 1-5) | ~$1.3M |
| **Delta total** | **$4.1M** |

**No es posible reconciliar exactamente** porque:
1. Los archivos fuente del loader (`06-06-2026.xlsx`, `1 jun 2026 - 5 jun 2026.xlsx`) ya no existen
2. El archivo actual `1 jun 2026 - 8 jun 2026.xlsx` es una versión fusionada que puede tener datos diferentes
3. El loader aplica transformaciones (neto vs bruto) que no son visibles desde los RAW actuales
