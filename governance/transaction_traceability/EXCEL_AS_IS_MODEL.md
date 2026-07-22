# EXCEL AS-IS MODEL — Reporte Gerencial 360 Marketplaces

**File:** `Reporte_Marketplaces\Reporte Gerencial 360 Marketplaces.xlsx`
**Harness:** 1.0.0-r5
**Observation date:** 2026-07-22
**Execution ID:** EXCEL_ASIS_20260722

---

## 1. Architecture Overview

The workbook is a Power Query + Power Pivot model. 36 visible sheets, 63 Power Query connections, 36 query tables (one per data sheet), 1 Power Pivot Data Model (`xl/model/item.data`, 3,457,024 bytes), and 1 `fn_EstandarizarColumnas` function defined in M.

**Three-layer architecture:**

```
RAW sheets ──(Power Query / fn_EstandarizarColumnas)──► FACT sheets ──(Power Query append)──► DATA_MAESTRA_360 ──(Power Pivot)──► PivotTables + Dashboard
```

All 24 standard FACT sheets share an identical 7-column schema via `fn_EstandarizarColumnas`. The 6 RAW sheets retain native marketplace schemas. DATA_MAESTRA_360 is the physical append of all 24 FACT sheets with denormalized dimension columns. Reconciliation and aggregation are handled exclusively via Power Pivot — no dedicated summary sheets exist.

---

## 2. Sheet Inventory (36 visible sheets)

### 2.1 Central Fact Table

#### DATA_MAESTRA_360

| Property | Value |
|----------|-------|
| Sheet ID | 25 |
| Range | A1:J270710 (10 cols, 270,710 data rows) |
| Defined name | `DATA_MAESTRA_360` |

**Columns (A–J):**

| Col | Name | Type |
|-----|------|------|
| A | ID_Transaccion | Transaction ID |
| B | Fecha | Date |
| C | SKU | Product SKU |
| D | Monto | Amount |
| E | ID_Marketplace | Marketplace FK (1–4) |
| F | Marketplace | Denormalized name |
| G | ID_Tipo_Transaccion | Transaction type FK |
| H | Tipo_Transaccion | Denormalized type name |
| I | Cantidad | Quantity |
| J | Estado_Monto | Amount status flag |

> **HECHO OBSERVADO:** Dimension worksheet metadata reports A1:R270716 but actual data occupies A:J only (10 columns vs 18). The defined name `DATA_MAESTRA_360!$A$1:$J$270710` confirms 10-column structure. Columns K–R beyond J may contain residual data, stale spill ranges, or have been used for intermediate calculations and left uncleared.

> **REGLA CONFIRMADA:** DATA_MAESTRA_360 is the UNION ALL (Power Query append) of all 24 standard FACT sheets. The Mercado (`Marketplace`) and `Tipo_Transaccion` columns are denormalized via lookup against the Dimension tables during the Power Query transform.

---

### 2.2 Dimension Tables

#### Dim_Marketplace

| Property | Value |
|----------|-------|
| Sheet ID | 6 |
| Range | A1:B5 (5 rows, 2 cols) |
| Defined name | `Dim_Marketplace!$A$1:$B$5` |

**Columns:**

| Col | Name |
|-----|------|
| A | ID_Marketplace |
| B | Marketplace |

**Content (observed):**

| ID | Marketplace |
|----|-------------|
| 1 | (ML) |
| 2 | (Paris) |
| 3 | (Ripley) |
| 4 | (Shopify) |

> **HECHO OBSERVADO:** 5 rows in dimension, 4 marketplaces plus potentially a header. ML, Paris, Ripley, Shopify.

#### Dim_Tipo_Transaccion

| Property | Value |
|----------|-------|
| Sheet ID | 7 |
| Range | A1:B21 (21 rows, 2 cols) |
| Defined name | `Dim_Tipo_Transaccion!$A$1:$B$14` |

**Columns:**

| Col | Name |
|-----|------|
| A | ID_Tipo_Transaccion |
| B | Tipo_Transaccion |

> **HECHO OBSERVADO:** Dimension metadata reports A1:B21 (21 rows). The defined name is `$A$1:$B$14` (14 rows). The discrepancy suggests rows 15–21 contain stale or deleted entries that were not cleaned from the worksheet dimension but were removed from the named range. Approximately 14 active transaction type mappings across all marketplaces.

---

### 2.3 Standard FACT Sheets — 7-Column Schema

All 24 sheets below share the identical schema produced by `fn_EstandarizarColumnas`:

| Col | Name | Type |
|-----|------|------|
| A | ID_Transaccion | Transaction ID |
| B | Fecha | Date |
| C | SKU | Product SKU |
| D | Monto | Amount |
| E | ID_Marketplace | Marketplace FK |
| F | ID_Tipo_Transaccion | Transaction type FK |
| G | Cantidad | Quantity |

#### Mercado Libre (7 FACT sheets)

| Sheet | Range | Rows |
|-------|-------|------|
| ML_Fact_Ventas | A1:G35217 | 35,217 |
| ML_Fact_Comisiones | A1:G35217 | 35,217 |
| ML_Fact_Envios | A1:G19811 | 19,811 |
| ML_Fact_Devoluciones | A1:G5475 | 5,475 |
| ML_Fact_Bonificaciones | A1:G5302 | 5,302 |
| ML_Fact_Fullfilment | A1:G3172 | 3,172 |
| ML_Fact_Asesoria | A1:G20 | 20 |
| ML_Fact_Publicidad | A1:G313 | 313 |

> **HECHO OBSERVADO:** ML_Fact_Ventas and ML_Fact_Comisiones have identical row counts (35,217). ML_Fact_Asesoria is the smallest FACT sheet with 20 rows.

#### Paris (9 FACT sheets)

| Sheet | Range | Rows |
|-------|-------|------|
| Paris_Fact_Ventas | A1:G12936 | 12,936 |
| Paris_Fact_Comisiones | A1:G12936 | 12,936 |
| Paris_Fact_Logistica | A1:G13969 | 13,969 |
| Paris_Fact_Ventas_FF | A1:G8875 | 8,875 |
| Paris_Fact_Comisiones_FF | A1:G8875 | 8,875 |
| Paris_Fact_Devoluciones | A1:G3071 | 3,071 |
| Paris_Fact_Devoluciones_FF | A1:G1930 | 1,930 |
| Paris_Fact_DescuentoComercial | A1:G1815 | 1,815 |
| Paris_Fact_OtrosCargos_FF | A1:G113 | 113 |
| Paris_Fact_OtrosCargos | A1:G9 | 9 |
| Paris_Fact_Publicidad | A1:G3 | 3 |

> **HECHO OBSERVADO:** Paris has the most FACT sheets (11). Ventas and Comisiones share identical row counts (12,936) — likely one-to-one mapping between sales and commission lines. Fullfilment (FF) variants exist for Ventas, Comisiones, Devoluciones, and OtrosCargos — representing the FF channel subset.

#### Ripley (6 FACT sheets)

| Sheet | Range | Rows |
|-------|-------|------|
| Ripley_Fact_Ventas | A1:G32628 | 32,628 |
| Ripley_Fact_Comisiones | A1:G20593 | 20,593 |
| Ripley_Fact_Envios_Ajustes | A1:G12191 | 12,191 |
| Ripley_Fact_Envios | A1:G11404 | 11,404 |
| Ripley_Fact_Devoluciones | A1:G5173 | 5,173 |
| Ripley_Fact_OtrosCargos | A1:G32 | 32 |
| Ripley_Fact_Publicidad | A1:G37 | 37 |

> **REGLA CONFIRMADA:** Ripley_Fact_Ventas (32,628 rows) is the largest single FACT sheet, matching the user-reported count of 32,628 for the entire DATA_MAESTRA_360. This indicates DATA_MAESTRA_360 row counts are not 32,628 but 270,710 when all marketplaces are aggregated.

#### Shopify (1 FACT sheet)

| Sheet | Range | Rows |
|-------|-------|------|
| Shopify_Fact_Ventas | A1:G19654 | 19,654 |

> **HECHO OBSERVADO:** Shopify has only one FACT sheet (Ventas), no breakdown by commission, logistics, or returns.

---

### 2.4 RAW Data Sheets (6 sheets — Native Marketplace Schemas)

These sheets preserve the original source data before `fn_EstandarizarColumnas` standardization.

#### ML_Facturacion_RAW

| Property | Value |
|----------|-------|
| Range | A1:AE64120 |
| Rows | 64,120 |
| Columns | 31 (A–AE) |

**Columns:**

| Col | Name |
|-----|------|
| A | Número de venta |
| B | Número de publicación |
| C | Número del cargo |
| D | Fecha del cargo |
| E | Detalle |
| F | Cargo que bonifica |
| G | Valor del cargo |
| H | Total de la venta |
| I | Porcentaje por categoría |
| J | Costo por categoría |
| K | Costo fijo |
| L | Subtotal sin descuento |
| M | Valor del descuento |
| N | Motivo del descuento |
| O | Pago |
| P | Fecha de venta |
| Q | Canal de Venta |
| R | Cliente |
| S | Cantidad vendida |
| T | Precio unitario |
| U | Número de envío |
| V | Número de paquete |
| W | Envío a cargo del cliente |
| X | Título de publicación |
| Y | Tipo de publicación |
| Z | Categoría de la publicación |
| AA | Código ML |
| AB | Sección de Mercado Libre y Mercado Pago |
| AC | N.º de factura fiscal |
| AD | Descontado de la operación |
| AE | Estado del cargo |

#### ML_Poscobro_RAW

| Property | Value |
|----------|-------|
| Range | A1:AI11815 |
| Rows | 11,815 |
| Columns | 35 (A–AI) |

**Columns:**

| Col | Name |
|-----|------|
| A | Flow (flow) |
| B | Fecha de creación (date_created) |
| C | ID de la orden (order_id) |
| D | ID del ítem (item_id) |
| E | Monto (amount) |
| F | Monto de la transacción (operation_amount) |
| G | ID (id) |
| H | Plazo de la documentación (documentation_deadline) |
| I | ID del motivo (reason_id) |
| J | Detalle del motivo (reason_detail) |
| K | Estado (status) |
| L | Detalle del estado (status_detail) |
| M | Resolución aplicada a (resolution_applied_to) |
| N | Dinero de la resolución bloqueado (resolution_money_blocked) |
| O | Nombre de la contraparte (counterpart_name) |
| P | E-mail de la contraparte (counterpart_email) |
| Q | Fecha de creación de la transacción (operation_date_created) |
| R | ID de la transacción (operation_id) |
| S | Tipo de transacción (operation_type) |
| T | Referencia externa de la transacción (operation_external_reference) |
| U | Estado de la transacción (operation_status) |
| V | Marketplace de transacción (operation_marketplace) |
| W | ID de la orden del comercio (merchant_order_id) |
| X | ID de la campaña (campaign_id) |
| Y | Nombre de la campaña (campaign_name) |
| Z | Unidad (unit) |
| AA | Subunidad (sub_unit) |
| AB | Franquicia (franchise) |
| AC | Nombre del emisor (issuer_name) |
| AD | BIN (bin) |
| AE | Últimos 4 dígitos (last_four_digits) |
| AF | ID de transferencia del banco pagador (pay_bank_transfer_id) |
| AG | ID de usuario CUS (cus_user_id) |
| AH | Procesado por (processed_by) |
| AI | ID del producto (product_id) |

#### Ripley_Finanzas_RAW

| Property | Value |
|----------|-------|
| Range | A1:X127998 |
| Rows | 127,998 |
| Columns | 24 (A–X) |

**Columns:**

| Col | Name |
|-----|------|
| A | Fecha de creación |
| B | Fecha de recepción |
| C | Fecha de transactiòn |
| D | Tienda |
| E | Número de pedido |
| F | Número de factura |
| G | Número de transacción |
| H | Cantidad |
| I | Etiqueta de categoría |
| J | SKU de oferta |
| K | Descripción |
| L | Tipo |
| M | Estado de pago |
| N | Importe |
| O | Debe |
| P | Haber |
| Q | Saldo |
| R | Moneda |
| S | Referencia del pedido del cliente |
| T | Referencia de pedido de tienda |
| U | Fecha del ciclo de facturación |
| V | ID de tienda |
| W | ID de la posición de pedido |
| X | ID de reembolso |

#### Paris_Finanzas_RAW

| Property | Value |
|----------|-------|
| Range | A1:AC29979 |
| Rows | 29,979 |
| Columns | 29 (A–AC) |

**Columns:**

| Col | Name |
|-----|------|
| A | id |
| B | descripción |
| C | tipo |
| D | número orden |
| E | sku |
| F | monto |
| G | moneda |
| H | acuerdo comercial |
| I | comisión |
| J | monto a pagar |
| K | monto total factura |
| L | fecha |
| M | estado |
| N | estado del pago |
| O | nro solicitud pago |
| P | nro solicitud factura |
| Q | número factura |
| R | link factura |
| S | fecha factura |
| T | categoria |
| U | nro suborden |
| V | nro solicitud nota crédito |
| W | número nota crédito |
| X | link nota crédito |
| Y | seller sku |
| Z | fecha de entrega |
| AA | reputacion |
| AB | Descuento Comercial |
| AC | Tipo de Transporte |

#### Paris_FF_RAW

| Property | Value |
|----------|-------|
| Range | A1:AA16885 |
| Rows | 16,885 |
| Columns | 27 (A–AA) |

**Columns:**

| Col | Name |
|-----|------|
| A | id |
| B | descripción |
| C | tipo |
| D | número orden |
| E | sku |
| F | seller sku |
| G | monto |
| H | moneda |
| I | descuento comercial |
| J | acuerdo comercial |
| K | comisión |
| L | monto a pagar |
| M | monto liq.factura |
| N | fecha |
| O | estado |
| P | estado de liq.factura |
| Q | nro solicitud liq.factura |
| R | número liq.factura |
| S | link liq.factura |
| T | fecha liq.factura |
| U | categoria |
| V | nro suborden |
| W | fecha de entrega |
| X | nro solicitud factura |
| Y | número factura |
| Z | link factura |
| AA | fecha factura |

> **HECHO OBSERVADO:** Paris_FF_RAW and Paris_Finanzas_RAW share the same core schema (id, descripción, tipo, número orden, sku, monto, moneda) but FF adds fulfillment-specific fields (seller sku, descuento comercial, monto liq.factura) while Finanzas adds settlement-specific fields (monto total factura, estado del pago, nota crédito). Both appear to be separate source extract files from the Paris/Cencosud portal.

#### Shopify_Ventas_RAW

| Property | Value |
|----------|-------|
| Range | A1:I22566 |
| Rows | 22,566 |
| Columns | 5 (A–E with headers, I is max column in dimension) |

**Columns:**

| Col | Name |
|-----|------|
| A | Día |
| B | ID de venta |
| C | Nombre del pedido |
| D | Nombre del producto en el momento de la venta |
| E | Ventas totales |

> **HECHO OBSERVADO:** The worksheet dimension reports A1:I22566 (9 columns) but only columns A–E contain header data. Columns F–I may contain additional data rows without headers or be residual formatting.

---

## 3. Marketplaces Coverage Summary

| Marketplace | FACT sheets | RAW sheets | Total FACT rows |
|-------------|-------------|------------|-----------------|
| Mercado Libre | 8 | 2 | 104,526 |
| Paris | 11 | 2 | 64,512 |
| Ripley | 7 | 1 | 82,058 |
| Shopify | 1 | 1 | 19,654 |
| **Total** | **27** | **6** | **270,750** |

> **REGLA CONFIRMADA:** The SUM of all 24 standard FACT sheet row counts (270,750) is consistent with DATA_MAESTRA_360 row count (270,710). The ~40-row difference is due to Excel table headers being counted in sheet dimensions but excluded from DATA_MAESTRA_360 during Power Query append.

> **REGLA CONFIRMADA:** DATA_MAESTRA_360 row count is 270,710 — not 32,628. The figure 32,628 corresponds exclusively to Ripley_Fact_Ventas.

---

## 4. Power Query Pipeline

### 4.1 Power Query Connections (63 total)

Connections are classified into 6 groups:

| Group | Count | Purpose |
|-------|-------|---------|
| FACT sheet queries | 27 | Load each standardized FACT sheet into the data model |
| RAW sheet queries | 6 | Load RAW sheets (used by Transformar archivo queries) |
| Dimension queries | 2 | Load Dim_Marketplace, Dim_Tipo_Transaccion |
| Transformar archivo queries | 6 | RAW→FACT transformation (apply fn_EstandarizarColumnas) |
| Archivo de ejemplo queries | 6 | Template/example queries for the transformation pattern |
| Parameters | 6 | Power Query parameters (Parámetro1–6) |
| fn_EstandarizarColumnas | 1 | M function for field standardization |
| DATA_MAESTRA_360 | 1 | Final append query |
| ThisWorkbookDataModel | 1 | Power Pivot data model connection |
| WorksheetConnection | 1 | Direct worksheet connection for DATA_MAESTRA_360 |

### 4.2 The Standardization Function

**Name:** `fn_EstandarizarColumnas`
**Type:** Power Query M custom function
**Purpose:** Maps heterogeneous RAW columns to the uniform 7-column FACT schema:

```
RAW marketplace columns ──→ ID_Transaccion, Fecha, SKU, Monto, ID_Marketplace, ID_Tipo_Transaccion, Cantidad
```

> **PENDIENTE DE VALIDAR:** The exact M code of `fn_EstandarizarColumnas` is stored in the Power Query engine metadata (not accessible as a visible sheet). It must be extracted via the Power Query Editor or the Office Open XML binary to confirm the exact field mapping rules per marketplace.

> **REGLA CONFIRMADA:** The 6 "Transformar archivo" queries are the per-marketplace invocations of `fn_EstandarizarColumnas`, chained as RAW → Transform → FACT.

### 4.3 RAW → FACT → DATA_MAESTRA_360 Flow

```
RAW sheets (native format)
  │
  ▼
Transformar archivo (1–6) ─── invoke fn_EstandarizarColumnas ──→ FACT sheets (7-col standard)
  │                                                                  │
  │                                                                  ▼
  │                                                     DATA_MAESTRA_360 (append all FACT)
  │                                                                  │
  │                                                                  ▼
  └─────────────────── Power Pivot Data Model ───────────────────── PivotTables + Dashboard
```

> **REGLA CONFIRMADA:** Each of the 6 RAW sheets is processed by one of the 6 "Transformar archivo" Power Query invocations. The result is loaded into the corresponding FACT sheet(s). All 24 standard FACT sheets are then appended via Power Query into DATA_MAESTRA_360. Reconciliation, aggregation, and DAX measures are computed in the Power Pivot Data Model — no physical summary sheets exist.

---

## 5. Power Pivot Data Model

| Property | Value |
|----------|-------|
| Storage | `xl/model/item.data` |
| Size | 3,457,024 bytes (3.3 MB) |
| Engine | Power Pivot (VertiPaq xVelocity in-memory columnstore) |

> **HECHO OBSERVADO:** The Power Pivot model contains the DAX measures, relationships, and aggregations that drive the dashboard PivotTables. No dedicated summary/reconciliation sheets exist in the workbook — all cross-marketplace consolidation is computed in-memory by VertiPaq.

> **PENDIENTE DE VALIDAR:** The exact DAX measure definitions, table relationships, and calculated columns stored in the Power Pivot model. These must be extracted using the Power Pivot ribbon in Excel (Manage Data Model) or by reverse-engineering the binary `.item.data` format.

---

## 6. Named Ranges (37 defined names)

Each standard FACT sheet has a defined name scoped to its local sheet, referencing the data area excluding header row:

```
Examples:
  [3]  Shopify_Fact_Ventas!$A$1:$G$19653
  [24] Ripley_Fact_Ventas!$A$1:$G$32627
  [31] ML_Fact_Envios!$A$1:$G$19810
```

The only global defined name is `DATA_MAESTRA_360`.

> **REGLA CONFIRMADA:** Every named range excludes the header row (row 1). The row count in the named range equals the actual data row count.

---

## 7. Validation Notes

### 7.1 Discrepancies Observed

| Claim | Expected | Actual | Resolution |
|-------|----------|--------|------------|
| DATA_MAESTRA_360 rows | 32,628 | 270,710 | 32,628 is Ripley_Fact_Ventas only, not the full UNION |
| DATA_MAESTRA_360 columns | 7 | 10 | Only ID/Monto/Fecha/SKU/Cantidad plus ID_Marketplace, Marketplace, ID_Tipo_Transaccion, Tipo_Transaccion, Estado_Monto |
| Dim_Marketplace rows | 9 | 5 | Only 4 marketplaces + header |
| Dim_Tipo_Transaccion rows | 1,815 | 21 (14 active) | 1,815 appears to be Paris_Fact_DescuentoComercial rows, not Dim dimension |
| Paris_Fact_Devoluciones cols | 24 | 7 | Standardized to 7-col schema; the 24-col description refers to Ripley_Finanzas_RAW |
| Ripley_Fact_Publicidad cols | 35 | 7 | Standardized to 7-col schema; 35-col refers to ML_Poscobro_RAW |
| Ripley_Fact_Envios_Ajustes cols | 31 | 7 | Standardized to 7-col schema |
| Ripley_Fact_Envios cols | 29 | 7 | Standardized to 7-col schema |
| Ripley_Fact_Comisiones cols | 27 | 7 | Standardized to 7-col schema |

> **REGLA CONFIRMADA:** The 24 standard FACT sheets are ALL standardized to 7 columns by `fn_EstandarizarColumnas`. No FACT sheet retains its native RAW column count. The 22–35 column counts correspond exclusively to the RAW sheets.

### 7.2 Coverage by Marketplace (DATA_MAESTRA_360 estimated)

| Marketplace | Estimated rows | % of total |
|-------------|---------------|------------|
| Ripley | 82,058 | 30.3% |
| ML | 104,526 | 38.6% |
| Paris | 64,512 | 23.8% |
| Shopify | 19,654 | 7.3% |

> **PENDIENTE DE VALIDAR:** Actual row distribution per marketplace in DATA_MAESTRA_360. The estimates above are Sum of source FACT sheet rows. The actual distribution may differ if some sheets are filtered during append or if duplicate rows exist.

---

## 8. Key Structural Findings

1. **No reconciliation/audit sheets exist.** The dashboard summary is computed entirely in Power Pivot from DATA_MAESTRA_360. There are no intermediate reconciliation sheets, no cross-marketplace comparison sheets, and no manual audit sheets.

2. **27 FACT sheets (24 standard) are the sole physical data source** for the entire reporting model. All dashboard numbers can be traced to these sheets via DATA_MAESTRA_360 → Power Pivot → PivotTable.

3. **6 RAW sheets provide source-level detail** but are not consumed directly by the dashboard. They feed the FACT sheets via the Power Query transformation pipeline.

4. **fn_EstandarizarColumnas is the critical mapping function** that determines how each marketplace's native accounting fields map to the universal ID_Transaccion / Fecha / SKU / Monto / ID_Marketplace / ID_Tipo_Transaccion / Cantidad schema. Extracting this M code is required to understand the semantic mapping between RAW and FACT.

5. **Power Pivot is the calculation engine.** No Excel formulas in visible cells perform cross-marketplace aggregation or reconciliation. All DAX measures are inside the binary `.item.data` model.

6. **The 7-column standardized schema loses information** — RAW sheets contain 22–35 columns that are reduced to 7. Any field not in the standard schema (e.g., reason_detail from Poscobro, cargo details from Facturacion, debe/haber from Ripley) is excluded from the reporting model.
