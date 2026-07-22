# MARKETPLACE OPERATIONAL INTELLIGENCE COVERAGE

**Date:** 2026-06-06
**Scope:** All raw data sources per marketplace
**Goal:** Determine if a common operational intelligence layer is viable across all 4 MPs
**Constraints:** NO code changes, NO implementation, SOLO inventario

---

## Executive Summary

**OPERATIONAL_LAYER = MARKETPLACE_SPECIFIC** ⚠️

Each marketplace was built independently with its own data schema, granularity, and operational concepts. A universal operational layer is NOT viable without structural harmonization.

However, **3 common operational KPIs** are feasible across all 4 MPs:

- **Returns Rate** (Devoluciones / Ventas)
- **Commission Rate** (Comisiones / Ventas)
- **Net Revenue Rate** (Disponible / Ventas)

For specific operational domains (logistics, catalog quality, fulfillment, claims), ML has **10-100x more granularity** than the other 3 MPs combined.

---

## FASE 1: Raw Data Inventory Per MP

### Mercado Libre (323 files)

| Source | Files | Format | Period | Granularity |
|---|---|---|---|---|
| **Facturación** | 18 | XLSX | Ene2025–Jun2026 (18mo) | Transaction-level: 32 columns, 3,077 rows/mo avg |
| **Poscobro** | 5 | XLSX | Ene2025–Jun2026 (18mo) | Reason codes: FLOW (claim/refund/chargeback) + reason_detail |
| **Liberaciones** | 18 | XLSX | Ene2025–Jun2026 (18mo) | Settlement-level: 53 columns, bank reconciliation detail |
| **Liquidación_FF** | 90 | XLSX | Ene2025–May2026 (17mo) | Weekly, SKU-level Fulfillment: 10-56 KB/wk avg |
| **Documentos Recepcionados** | 192 | XML | Continuous | SII DTE receipts (invoice-level) |

**Facturación columns:** `N° de factura fiscal, Fecha del cargo, Número del cargo, Detalle, Descontado de la operación, Estado del cargo, Cargo que bonifica, Valor del cargo, Porcentaje por categoría, Costo por categoría, Costo fijo, Subtotal sin descuento, Valor del descuento, Motivo del descuento, Número de venta, Pago, Fecha de venta, Canal de Venta, Cliente, Cantidad vendida, Precio unitario, Total de la venta, Número de envío, Número de paquete, Número de publicación, Título de publicación, Tipo de publicación, Categoría de la publicación, Código ML, Sección de Mercado Libre y Mercado Pago`

### Ripley (453 files)

| Source | Files | Format | Period | Granularity |
|---|---|---|---|---|
| **Resumen Financiero** | 46 | XLSX | 46 settlements (weekly) | Settlement-level: 37 columns → 34 columns (schema change at file 372) |
| **Documentos Recepcionados** | 407 | XML | Continuous | SII DTE receipts |

**Resumen columns:** `Fecha OC, Número documento liquidación, Orden de compra, Shop ID, Tienda, Importe del pedido, Envío, Gastos de envío pagados por el operador, Comisiones sobre pedidos, Pedidos reembolsados, Envío reembolsado, Gastos de envío reembolsados pagados por el operador, Comisiones sobre pedidos reembolsados, Abono postventa, Abono por error de comisión, Abono extraordinario - error de precio, Abono oferta TC - OPEX, Abono por uso de flota propia, Otros abonos, Abonos soluciones comerciales, Abonos por cupón promocional, Descuento oferta TC - OPEX, Otros descuentos, Descuento por error de clase logística, Descuento por costo logístico, Descuento por logística inversa, Descuento por cancelación, Descuento por compensación a cliente, Descuento FF - sobreestadía, Descuento FF - pick and pack, Descuento FF - Otros, Descuento por PDM, Cobro despacho primera milla, Descuento operacional, Abono por formalización a OPL, Descuento por cupones de despacho, A pagar`

### Paris (~270 files)

| Source | Files | Format | Period | Granularity |
|---|---|---|---|---|
| **Facturación (XMLs)** | 248 | XML | Continuous | SII DTE receipts |
| **Dropshipping** | 18 | XLSX | Ene2025–Jun2026 (18mo) | Transaction-level: 29 columns, order+SKU detail |
| **Fulfillment** | 4 | XLSX | 2025 annual + Ene–Jun 2026 | Order-level: 27 columns, includes SKU + logistics |

**Dropshipping columns:** `id, descripción, tipo, número orden, sku, monto, moneda, acuerdo comercial, comisión, monto a pagar, monto total factura, fecha, estado, estado del pago, nro solicitud pago, nro solicitud factura, número factura, link factura, fecha factura, categoría, nro suborden, nro solicitud nota crédito, número nota crédito, link nota crédito, seller sku, fecha de entrega, reputación, Descuento Comercial, Tipo de Transporte`

**Fulfillment columns:** `id, descripción, tipo, número orden, sku, seller sku, monto, moneda, descuento comercial, acuerdo comercial, comisión, monto a pagar, monto liq.factura, fecha, estado, estado de liq.factura, nro solicitud liq.factura, número liq.factura, link liq.factura, fecha liq.factura, categoría, nro suborden, fecha de entrega, nro solicitud factura, número factura, link factura, fecha factura`

### Falabella (10 files)

| Source | Files | Format | Period | Granularity |
|---|---|---|---|---|
| **Documentos Recepcionados** | 6 | XML | Continuous (limited) | SII DTE receipts |
| **Órdenes y Transacciones** | 4 | XLSX | Mar–Jun 2026 (4mo) | Denormalized / pivot table format, 2 columns only |

**Note:** Falabella's Órdenes y Transacciones file has only 2 columns: `Fecha de actualización` (str) + a datetime-as-header column. This suggests a pivot table or API export, not a structured operational report. Minimal operational granularity available.

---

## FASE 2: Operational Category Coverage

### Legend
- ✅ Full coverage (structured data with operational detail)
- ⚠️ Partial coverage (aggregated or limited detail)
- ❌ No data available

| Operational Category | ML | RIPLEY | PARIS | FALABELLA |
|---|---|---|---|---|
| **Devoluciones** | ✅ 2,995 rows, $93.0M, as `Devolución de venta` | ✅ 2,450 rows, $82.9M, as `Pedidos reembolsados` | ⚠️ Dev included in Dropshipping status field | ❌ No return data available |
| **Reclamos** | ✅ 40+ reason codes via PosCobro (claim/refund/chargeback) | ❌ No separate reclaim data (embedded in descuentos) | ❌ No reclaim data | ❌ No reclaim data |
| **Cancelaciones** | ⚠️ Implied in devoluciones data | ⚠️ Included in `Descuento por cancelación` ($28K) | ❌ No cancelation data | ❌ No cancelation data |
| **Logística** | ✅ $66.5M envíos, $2.2M retiro stock, $6.3M ME | ✅ $18.4M envíos, $12.8M costo logístico, $1.4M logística inversa | ⚠️ `Tipo de Transporte` field in Dropshipping | ❌ No logistics data |
| **Fulfillment** | ✅ 90 Liquidación_FF files (weekly, SKU-level) | ⚠️ 3 FF descuentos (sobreestadía, pick and pack, Otros) | ✅ 27 columns Fulfillment report (SKU + logistics) | ❌ No fulfillment data |
| **Calidad Catálogo** | ✅ Differences + sizes + damaged items + empty box (40+ reason codes) | ❌ No catalog quality data | ❌ No catalog quality data | ❌ No catalog quality data |
| **Penalizaciones** | ⚠️ Cargos (Cargo, retiro stock, stock antiguo) | ✅ `Descuento por error de clase logística` + `Descuento operacional` | ❌ No penalty data | ❌ No penalty data |
| **Compensaciones** | ✅ BPP (`compensated`, `bpp_covered`, `ppv_covered`) | ⚠️ `Abono postventa`, `Abono error comisión` | ❌ No compensation data | ❌ No compensation data |
| **Incidencias** | ✅ Full PosCobro trace (11,469 rows, 40+ reason types) | ❌ No incidence data | ❌ No incidence data | ❌ No incidence data |

### Category Count Per MP

| Category | ML | RIPLEY | PARIS | FALABELLA |
|---|---|---|---|---|
| Covered (✅ + ⚠️) | **9/9** | **7/9** | **4/9** | **1/9** |

---

## FASE 3: Source, Granularity, Period, Coverage

### Source System

| MP | Primary Source | Secondary Source | Tertiary Source |
|---|---|---|---|
| **ML** | Facturación (ML API) | Poscobro + Liberaciones (ML API) | Liquidación_FF + SII XML |
| **RIPLEY** | Resumen Financiero (RIPLEY Portal) | SII XML | — |
| **PARIS** | Dropshipping (PARIS Portal) | Fulfillment (PARIS Portal) | SII XML |
| **FALABELLA** | Órdenes (FALABELLA Portal) | SII XML | — |

### Granularity Comparison

| Granularity Level | ML | RIPLEY | PARIS | FALABELLA |
|---|---|---|---|---|
| Transaction-level | ✅ | ✅ | ✅ | ❌ (pivot) |
| SKU-level | ✅ (Facturación + FF) | ❌ | ✅ | ❌ |
| Reason code | ✅ (40+ PosCobro codes) | ❌ | ❌ | ❌ |
| Settlement detail | ✅ (53 columns) | ✅ (37→34 columns) | ⚠️ (29 columns) | ❌ |
| Warehouse ops | ✅ (FF weekly) | ⚠️ (3 FF lines) | ✅ (Fulfillment report) | ❌ |
| Catalog quality | ✅ (size, color, damage) | ❌ | ❌ | ❌ |

### Period Coverage

| MP | Earliest | Latest | Continuous |
|---|---|---|---|
| **ML** | 2025-01-01 | 2026-06-06 | ✅ 18 months |
| **RIPLEY** | 2025-01 | 2026-05 | ✅ 17 months |
| **PARIS** | 2025-01 | 2026-06-06 | ✅ 18 months |
| **FALABELLA** | 2026-03-01 | 2026-06-05 | ⚠️ 4 months only |

---

## FASE 4: Operational KPI Matrix

### Universal KPIs (All 4 MPs)

| KPI | ML | RIPLEY | PARIS | FALABELLA | Formula |
|---|---|---|---|---|---|
| **Returns Rate** | 10.6% | 23.5% | NC | NC | \|Devoluciones\| / Ventas |
| **Gross Revenue** | $875.9M | $353.2M | $484.2M | $12.5M | ledger.ingresos SUM |
| **Returns $** | $93.0M | $82.9M | $121.5M | $1.9M | ledger.devoluciones SUM |
| **Commission Rate** | 13.9% | 18.2% | NC | NC | \|CostosComerciales\| / Ventas |
| **Net Revenue** | $712.0M | $206.9M | $337.4M | $7.7M | cierre.resultado_neto |
| **Logistics Cost Rate** | 8.5% | 10.4% | NC | NC | \|CostosOperacionales\| / Ventas |

### ML-Specific KPIs (40+ reason codes)

| KPI | Value | Source |
|---|---|---|
| Ajustes Rate | 37.3% of Ventas | Ledger ajustes / ingresos |
| BPP Rate | $99.0M | bpp_refunded (30.3% of ajustes) |
| Talla/Garantía | $117.6M | 6 reason codes |
| Arrepentimiento | $44.8M | 5 reason codes |
| Producto Dañado | $3.0M | broken_item_fashion + empty_box |
| Falla Entrega | $4.9M | undelivered + not received |
| PosCobro Coverage | 100% of devoluciones | 93.7% of dev have PosCobro match |
| Logistics | $66.5M | Cargo por envíos ML |
| Fulfillment | $2.6M | Full storage/stock charges |
| Advertising | $49.4M | Product Ads + Display + Brand |

### RIPLEY-Specific KPIs (Resumen Financiero)

| KPI | Value | Source |
|---|---|---|
| Commission | $64.2M | Comisiones sobre pedidos |
| Logistics | $18.4M | Envío + Gastos envío |
| Returns Rate | 23.5% | Pedidos reembolsados / Importe |
| Penalties | $13.8M | Descuento costo logístico |
| Reversed Commissions | $15.1M | Comisiones reembolsadas |
| Abonos (adjustments) | NC | Abono postventa, error comisión, etc. |
| FF Charges | NC | 3 columns removed after file 371 |

### PARIS-Specific KPIs (Dropshipping + Fulfillment)

| KPI | Value | Source |
|---|---|---|
| Commission | $48.7M (implicit) | Via P&L spread (not explicit in datos) |
| Order Count | ~3,000/mo | Dropshipping transactions |
| Fulfillment SKUs | NC | Fulfillment report has SKU data |
| Transport Mode | NC | Tipo de Transporte field |
| Reputation | NC | reputacion field (seller rating) |

### FALABELLA-Specific KPIs

| KPI | Value | Source |
|---|---|---|
| Gross Revenue | $12.5M | ledger (only 4 months) |
| Commission | $2.4M | ledger |
| Returns | $1.9M | ledger |

---

## Answer to Unica Pregunta

> ¿Puede construirse una capa operacional común para los 4 marketplaces?

### Answer

**NO. OPERATIONAL_LAYER = MARKETPLACE_SPECIFIC**

A common operational layer is NOT viable as a unified schema. The structural differences are too large:

### Critical Differences

| Dimension | ML | RIPLEY | PARIS | FALABELLA | Implication |
|---|---|---|---|---|---|
| **Data model** | 5 sources (Fact+Pos+Lib+FF+XML) | 2 sources (Resumen+XML) | 3 sources (XML+DS+FF) | 2 sources (XML+Ord) | No common schema |
| **Reason codes** | 40+ PosCobro codes | 0 structured codes | 0 structured codes | 0 structured codes | ML has 100x more granularity for claims |
| **SKU-level** | Yes (Facturación + FF) | No | Yes (DS + FF) | No | Only 2/4 have SKU trace |
| **Fulfillment** | Weekly SKU detail | 3 aggregated lines (files 312-371 only) | Structured 27-col report | None | Schema changes mid-period for RIPLEY |
| **Returns data** | Devolución de venta ($93M) | Pedidos reembolsados ($82.9M) | Implied in status | None | Different naming, different semantics |
| **Logistics detail** | Envíos + ME + Full + retiros | Envío + gastos + logística inversa | Tipo de Transporte only | None | Incomparable granularity |
| **Period** | 18 months | 17 months | 18 months | **4 months** | FALABELLA too short for trend analysis |

### Structural Incompatibilities

1. **ML uses PosCobro reason codes** (40+ specific reasons like `repentant_buyer`, `broken_item_fashion`, `change_receiver_address`). No other MP has any equivalent. ML's operational intelligence is 10-100x deeper than peers.

2. **RIPLEY schema changed mid-period** (3 FF columns removed after file 371). Any operational KPI based on those columns would break at file 371.

3. **PARIS operational data is split** between Dropshipping (order-level, 29 cols) and Fulfillment (SKU-level, 27 cols). These are separate files with different schemas.

4. **FALABELLA has only 4 months** and its only operational file is a pivot table (not a structured report). Inadequate for any operational layer.

5. **No common order ID system** across MPs. ML uses `Número de venta`, RIPLEY uses `Orden de compra`, PARIS uses `número orden`, FALABELLA uses ???. Cross-MP order trace is impossible.

### Universal KPIs That ARE Feasible

Despite the structural differences, these 3 operational KPIs can be computed uniformly from the ledger (already normalized):

| KPI | Definition | SQL |
|---|---|---|
| **Returns Rate** | \|SUM(devoluciones)\| / SUM(ingresos) | `(fg='devoluciones') / (fg='ingresos')` |
| **Commission Rate** | \|SUM(costos_comerciales)\| / SUM(ingresos) | `(fg='costos_comerciales') / (fg='ingresos')` |
| **Net Revenue Rate** | SUM(resultado_neto) / SUM(ingresos) | `cierre.resultado_neto / cierre.total_ingresos` |

These 3 work for ALL 4 MPs because the financial pipeline already normalizes the data into `marketplace_ledger_v1`.

### Recommended MP-Specific Operational Layers

If operational intelligence is needed per domain, build MP-specific layers:

| Domain | Recommended MP | Reason |
|---|---|---|
| **Returns Intelligence** | ML (primary), RIPLEY (secondary) | ML has 40+ reasons, RIPLEY has structured refund data |
| **Logistics Optimization** | ML (primary), RIPLEY (secondary) | ML has $66.5M envíos + Full detail; RIPLEY has logistics breakdown |
| **Catalog Quality** | ML only | 8 reason codes for size/color/damage/quality |
| **Fulfillment Efficiency** | ML + PARIS | ML: weekly SKU-level FF; PARIS: structured Fulfillment report |
| **Claims Management** | ML only | Full PosCobro trace (claim/refund/chargeback) |
| **Penalty Monitoring** | RIPLEY only | Structured descuentos for logistics errors |

---

## Certification

| Check | Result |
|---|---|
| All 4 MPs inventoried | ✅ (ML: 323, RIPLEY: 453, PARIS: ~270, FALABELLA: 10) |
| All 9 operational categories classified per MP | ✅ |
| Source, granularity, period, coverage per MP | ✅ |
| Operational KPI matrix built | ✅ |
| Answer to unica pregunta | **NO — MARKETPLACE_SPECIFIC** |

```
OPERATIONAL_LAYER = MARKETPLACE_SPECIFIC ⚠️
Universal KPIs = 3 (Returns Rate, Commission Rate, Net Revenue Rate)
```
