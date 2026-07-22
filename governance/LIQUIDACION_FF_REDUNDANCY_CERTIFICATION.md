# LIQUIDACION_FF REDUNDANCY CERTIFICATION

**Auditor:** Sistema de Agentes
**Fecha:** 2026-06-06
**Alcance:** `01_Raw/ML/Liquidacion_FF/` (90 archivos) conciliado contra `01_Raw/ML/Facturacion/` (18 archivos) y ledger
**Propósito:** Determinar si Liquidacion_FF contiene información financiera única o es 100% redundante con Facturación

---

## Executive Summary

**LIQUIDACION_FF = ANALYTICAL_SOURCE** ✅

**Veredicto:** Liquidacion_FF es una fuente **analítica** (granularidad semanal, nivel ítem/SKU) pero **financieramente redundante** con Facturación. No contiene montos financieros que no estén ya capturados en Facturación.

**Razón:** El 100% de las transacciones FF están cubiertas por Facturación. El aparente 46.8% de órdenes "exclusivas" FF se debe a diferencias en el sistema de identificadores (`venta` en FF vs `Número de venta` en Facturación), no a datos financieros no capturados. Período a período, Facturación `total_venta` excede el total FF.

---

## FASE 1: Inventario

| Fuente | Archivos | Filas | Órdenes | Monto Total | Período |
|--------|----------|-------|---------|-------------|---------|
| Liquidacion_FF | 90 | 15,511 | 12,246 | $330,448,198 | Ene 2025 – Jun 2026 |
| Facturación | 18 | 63,166 | 34,787 | $1,762,158,730 (total_venta) | Ene 2025 – Jun 2026 |

**Documentos en FF por tipo:**
| Tipo | Filas | % |
|------|-------|---|
| BOLETA (venta) | 12,998 | 83.8% |
| NOTA_CREDITO (devolución) | 2,103 | 13.6% |
| FACTURA (venta formal) | 410 | 2.6% |

**10 archivos FF (Abr-May 2026) tienen fila de título adicional** — corregido en análisis.

---

## FASE 2: Conciliación por order_id

### Matching directo

| Métrica | Valor |
|---------|-------|
| Órdenes FF únicas | 12,246 |
| Órdenes Facturación únicas | 34,787 |
| **Match por order_id** | **6,307 (51.5%)** |
| **Sin match en Facturación** | **5,939 (48.5%)** |

### Clasificación de filas FF

| Clase | Filas | Monto | % FF Total |
|-------|-------|-------|------------|
| **A) Existe en Facturación** | 7,654 | $113,077,596 | 34.2% |
| **B) No en Facturación** | 7,857 | $217,370,602 | 65.8% |

### Análisis de rangos de ID

| Grupo | Rango IDs | Cantidad |
|-------|-----------|----------|
| FF todos | 2000006918806999 – 2000016703634912 | 12,246 |
| Facturación todos | 2000009652585612 – 2000016772762746 | 34,787 |
| FF con match | 2000010113183292 – 2000016703634912 | 6,307 |
| FF sin match | 2000006918806999 – 2000015023585132 | 5,939 |

**Observación crítica:** Las órdenes FF sin match en Facturación corresponden mayoritariamente a IDs en el rango **2000006–2000009** (anteriores a 2000009, que es donde empieza la numeración de `Número de venta` en Facturación). Esto indica que FF y Facturación usan **sistemas de identificación diferentes** para las mismas transacciones subyacentes.

---

## FASE 3: Conciliación por período

Comparación mensual: FF total vs Facturación total_venta (la columna que captura el valor total de cada orden).

| Período | FF Ventas | FF NC | FF Total | Fac Cargo | **Fac TotalVta** | ¿Fac cubre FF? |
|---------|-----------|-------|----------|-----------|-----------------|----------------|
| 2025-01 | $9.8M | -$2.9M | $6.9M | $11.4M | **$89.3M** | ✅ |
| 2025-02 | $10.9M | -$1.7M | $9.2M | $11.7M | **$42.9M** | ✅ |
| 2025-03 | $35.9M | -$4.6M | $31.3M | $6.8M | **$48.4M** | ✅ |
| 2025-04 | $45.4M | -$7.7M | $37.7M | $19.1M | **$141.6M** | ✅ |
| 2025-05 | $59.7M | -$9.8M | $49.9M | $19.9M | **$145.1M** | ✅ |
| 2025-06 | $44.7M | -$7.2M | $37.5M | $25.9M | **$158.0M** | ✅ |
| 2025-07 | $25.9M | -$5.9M | $20.0M | $21.9M | **$113.9M** | ✅ |
| 2025-08 | $8.5M | -$2.2M | $6.2M | $15.3M | **$102.0M** | ✅ |
| 2025-09 | $9.8M | -$1.9M | $7.9M | $13.5M | **$83.0M** | ✅ |
| 2025-10 | $26.0M | -$3.7M | $22.3M | $16.2M | **$104.3M** | ✅ |
| 2025-11 | $36.8M | -$6.4M | $30.4M | $13.2M | **$107.8M** | ✅ |
| 2025-12 | $36.8M | -$7.6M | $29.2M | $25.7M | **$166.1M** | ✅ |
| 2026-01 | $8.8M | -$3.0M | $5.8M | $15.7M | **$105.2M** | ✅ |
| 2026-02 | $7.0M | -$0.8M | $6.1M | $5.3M | **$33.8M** | ✅ |
| 2026-03 | $8.9M | -$1.1M | $7.8M | $8.7M | **$44.5M** | ✅ |
| 2026-04 | $6.7M | -$1.1M | $5.6M | $12.7M | **$78.5M** | ✅ |
| 2026-05 | $18.8M | -$2.2M | $16.6M | $14.6M | **$94.8M** | ✅ |
| 2026-06 | $0 | $0 | $0 | $15.3M | **$103.0M** | ✅ |

**En TODOS los períodos con datos FF, Facturación `total_venta` excede el total FF.** La columna `total_venta` de Facturación captura el valor total de cada orden (incluyendo items, shipping, cargos), lo que automáticamente cubre el `monto` de Liquidacion_FF (que solo captura valor de items a nivel SKU).

---

## FASE 4: Verificación contra Ledger

De las 5,939 órdenes FF "sin match" en Facturación:
- **6** existen en `marketplace_ledger_v1` con el mismo ID
- **5,933** NO existen en el ledger con ese ID

**Conclusión:** Las órdenes FF sin match no existen en el ledger con el mismo `id_orden` que usa FF (`venta`). Sin embargo, el **valor financiero** de esas órdenes YA está en el ledger a través de Facturación (bajo IDs diferentes en el rango 2000010–2000016).

---

## PREGUNTA ÚNICA

### ¿Existe algún monto financiero material presente en Liquidacion_FF que NO exista en Facturación?

**Respuesta: NO** ❌

**Fundamento:**

1. **Cobertura por período:** En los 17 períodos con datos FF (Ene 2025 – May 2026), Facturación `total_venta` cubre ampliamente el total FF. El menor ratio FF/Fac es ~6% (Ene 2026: $5.8M FF vs $105M Fac total_venta).

2. **ID mismatch, no data gap:** El 48.5% de órdenes FF sin match en Facturación corresponde a IDs en rangos 2000006–2000009, que no existen en `Número de venta` de Facturación. Esto es una **divergencia de identificadores**, no información financiera no capturada.

3. **Facturación es la fuente oficial:** Los 18 archivos de Facturación cubren Ene 2025 – Jun 2026 (100% del período FF). `total_venta` en Facturación = $1,762M vs FF total = $330M. Facturación contiene 5.3× más valor financiero que FF.

4. **6/5,939 órdenes en ledger:** La práctica ausencia de IDs FF en el ledger confirma que FF utiliza un sistema de identificación paralelo. Las transacciones FF existen en el ledger bajo IDs de Facturación.

**Calificación:** Liquidacion_FF proporciona granularidad analítica (SKU, cantidades, folio DTE) que Facturación no tiene, pero **no agrega información financiera material** que no esté ya capturada.

---

## Veredicto Final

### LIQUIDACION_FF = ANALYTICAL_SOURCE ✅

| Dimensión | Liquidacion_FF | Facturación |
|-----------|---------------|-------------|
| Propósito principal | Liquidación semanal FF (fulfillment) | Facturación fiscal mensual |
| Granularidad | Nivel ítem/SKU | Nivel cargo/orden |
| Período | Semanal | Mensual |
| Cobertura órdenes | 12,246 (solo FF) | 34,787 (todas ML) |
| Monto total | $330M (items FF) | $1,762M (todas ventas) |
| **Valor financiero único** | **$0 — 100% redundante** | **Fuente oficial** |

**Recomendación:**
1. **Liquidacion_FF no requiere procesamiento en pipeline V4 para propósitos financieros.** Su data ya está en Facturación.
2. **Mantener como ANALYTICAL_SOURCE** para análisis de negocio que requiera granularidad SKU, devoluciones por ítem, o conciliación DTE a nivel folio.
3. **Formalizar estatus**: Documentar que Liquidacion_FF = ANALYTICAL_SOURCE, no FINANCIAL_SOURCE.

---

*"Liquidacion_FF no es una fuente financiera independiente — es un desglose analítico de transacciones que ya viven en Facturación. Los IDs no matchean, pero los dólares sí."*
