# UX1.1 — Gerencial Gap Analysis

**Date:** 2026-06-04  
**Source:** `Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx`  
**Target:** `Executive Dashboard UX1.0`

---

## FASE 1 — Reverse Engineering: Reporte_Gerencial_Marketplaces

### 1.1 Hierarchical Structure

The report uses 4 high-level categories with a clear hierarchy:

```
Ventas (Ingresos Brutos)
    ↓
Devoluciones (Returns & Refunds)
    ↓
Cobros (Fees, Commissions, Charges)
    ↓
Disponible (Net Available = Ventas - Devoluciones - Cobros)
```

### 1.2 Dim_Tipo_Transaccion — 13 Concept Types

| ID | Gerencial Concept | Sign | Category |
|----|-------------------|------|----------|
| 1  | Ingreso por Venta (Marketplace) | + | **Ventas** |
| 13 | Ingreso por Venta (Canal Propio) | + | **Ventas** |
| 6  | Ajuste por Devolución | - | **Devoluciones** |
| 8  | Ajuste por Reembolso | - | **Devoluciones** |
| 2  | Comisión por Venta | - | **Cobros** |
| 3  | Costo de Transporte (Envío) | - | **Cobros** |
| 4  | Costo de Marketing en Plataforma | - | **Cobros** |
| 9  | Costo de Servicios Profesionales | - | **Cobros** |
| 10 | Costo de Gestión de Pedidos (Fulfillment) | - | **Cobros** |
| 11 | Ajuste por Descuento Comercial | - | **Cobros** |
| 12 | Tarifa de Procesamiento de Pago | ± | **Cobros** |
| 5  | Ajuste por Incentivo/Bonificación | + | **Cobros** (reduces Cobros) |
| 7  | Impuesto a la Transacción | - | **Devoluciones** (in report) |

### 1.3 KPIs

| KPI | Formula (DAX/Gerencial) | Business Question |
|-----|------------------------|-------------------|
| **Venta Bruta (GMV)** | `SUM(Monto) WHERE ID=1 OR ID=13` | "¿Cuánto vendimos?" |
| **Total Devoluciones** | `SUM(Monto) WHERE ID=6 OR ID=8` | "¿Cuánto nos devolvieron?" |
| **Total Cobros** | `SUM(Monto) WHERE ID IN (2,3,4,5,9,10,11,12)` | "¿Cuánto nos cobraron?" |
| **Disponible (Neto)** | `SUM(Monto) ALL` | "¿Cuánto quedó disponible?" |
| **Margen Neto %** | `Disponible / Venta Bruta` | "¿Qué % de cada venta nos queda?" |

### 1.4 Per-Marketplace Distribution

| Marketplace | ID | Raw Source | Has SKU? |
|------------|----|-----------|----------|
| Mercado Libre | 1 | ML_Facturacion + ML_Poscobro | Yes |
| Ripley | 2 | Ripley_Finanzas | Yes |
| París | 3 | Paris_Finanzas | Yes |
| Nicopoly (Shopify) | 4 | Shopify_Ventas | Yes (product name) |

### 1.5 Concept-Level Breakdown (Within Cobros)

The report breaks down Cobros into sub-concepts:
- **Comisiones** (ID 2) — Per-MP, % of sale
- **Logística/Envío** (ID 3) — Shipping costs
- **Publicidad/Marketing** (ID 4) — Product Ads, Display, etc.
- **Servicios** (ID 9) — Asesoría Comercial, Mi Página
- **Fulfillment** (ID 10) — Full storage & picking
- **Descuentos Comerciales** (ID 11) — Promotional discounts
- **Procesamiento de Pago** (ID 12) — Payment gateway fees
- **Bonificaciones/Incentivos** (ID 5) — Positive adjustments
- **Impuestos** (ID 7) — Transaction taxes

### 1.6 Business Questions the Report Answers

1. ¿Cuánto vendimos? → Venta Bruta
2. ¿Cuánto nos devolvieron? → Total Devoluciones
3. ¿Cuánto nos cobraron? → Total Cobros
4. ¿Cuánto quedó disponible? → Disponible
5. ¿Qué marketplace aporta más? → Per-MP breakdown
6. ¿Dónde se fue el dinero? → Concept breakdown (comisiones, logística, publicidad)
7. ¿Qué cambió respecto al período anterior? → Period comparison

### 1.7 Data Sources

- 6 RAW sheets, 25 fact tables, 1 consolidated table (`DATA_MAESTRA_360`)
- 251,651 rows across 4 marketplaces
- Classification via Power Query M code (filtering by detalle/TIPO column)

---

## FASE 2 — UX1.0 vs Gerencial Report Comparison

### 2.1 Coverage Matrix

| Gerencial Feature | UX1.0 Status | Classification |
|-------------------|-------------|---------------|
| Venta Bruta (GMV) | ✅ Total Gross Revenue | **Ya existe** |
| Per-MP Gross Revenue | ✅ Scorecard shows gross | **Ya existe** |
| Total Devoluciones | ✅ In waterfall as "Devoluciones" | **Ya existe** |
| Total Cobros | ❌ Not as single metric | **Falta** |
| Disponible (Neto) | ✅ As "Resultado Neto" / "Net Revenue" | **Ya existe** (rename) |
| Margen Neto % | ✅ Scorecard shows net margin % | **Ya existe** |
| Ventas → Devoluciones → Cobros → Disponible hierarchy | ❌ Uses Ingresos → Devoluciones → Costos → Ajustes → Neto | **Mejorable** |
| Per-marketplace concept breakdown | ❌ Scorecard shows only gross/net, not concept-level | **Falta** |
| Concept-level drill (Comisiones, Logística, Publicidad) | ❌ Waterfall shows aggregated categories only | **Falta** |
| Period comparison | ❌ Single period only, no delta | **Falta** |
| Explicabilidad (what/why/how) | ❌ No tooltips or explanations | **Falta** |
| Simple waterfall (Ventas ↓ Devoluciones ↓ Cobros ↓ Disponible) | ❌ Uses 5-stage waterfall with financial_group names | **Mejorable** |
| Audit drill-down | ✅ Drill-down to Auditor exists | **Ya existe** |
| Gerencial language ("Disponible", "Cobros") | ❌ Uses "Resultado Neto", "Costos Operacionales" | **Mejorable** |

### 2.2 Summary

| Status | Count | Items |
|--------|-------|-------|
| **Ya existe** | 6 | Venta Bruta, Per-MP Gross, Devoluciones, Disponible, Margen Neto, Audit drill-down |
| **Falta** | 5 | Total Cobros, Per-MP concept breakdown, Concept drill, Period comparison, Explicabilidad |
| **Mejorable** | 3 | Waterfall hierarchy, Gerencial language, Waterfall simplicity |
| **No aplica** | 0 | Everything can be converged |

---

## FASE 3-7 — Convergence Design

### 3.1 New Hierarchy (Replace UX1.0 layout)

```
┌──────────────────────────────────────────────────────┐
│  Executive Dashboard  │  Period  │  Marketplaces      │
├──────────────────────────────────────────────────────┤
│  Disponible  │  Ventas  │  Devoluciones  │  Cobros    │  ← 4 KPI cards
├──────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐ ┌─────────────┐ │
│  │ Mercado Libre│  │    Ripley    │ │    París    │ │  ← Per-MP scorecard
│  │ $273.3M      │  │  $44.5M      │ │  $113.5M    │ │    (gerencial concepts)
│  │ Disponible   │  │  Disponible  │ │  Disponible │ │
│  └──────────────┘  └──────────────┘ └─────────────┘ │
├──────────────────────────────────────────────────────┤
│  Waterfall                                          │
│  Ventas          $563.6M  ██████████████████████     │
│  Devoluciones    -$58.3M  ██████░░░░░░░░░░░░░░░░     │  ← Simplified
│  Cobros          -$71.4M  ████████░░░░░░░░░░░░░░     │     3-step waterfall
│  Disponible      $433.8M  ██████████████████████     │
├──────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐│
│  │ Cobros Breakdown          │  ML     RIP   PAR  FA││  ← Per-concept
│  │ Comisiones                │ -66.8M  -10.2M ..  ..││     matrix
│  │ Logística                 │ -25.6M  -2.3M  ..  ..││
│  │ Publicidad                │ -12.5M  -2.1M  ..  ..││
│  │ Servicios                 │ -17.5M  -     ..  ..││
│  │ Ajustes                   │ +71.5M  -7K   ..  ..││
│  └──────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────┤
│  Drill-down → Auditor (existing UX1.0 component)    │
└──────────────────────────────────────────────────────┘
```

### 3.2 Terminology Mapping

| Gerencial Term | UX1.0 Term | Action |
|----------------|-----------|--------|
| **Ventas** | "Total Gross Revenue" / "Ingresos Brutos" | Rename to "Ventas" |
| **Devoluciones** | "Devoluciones" | Keep (same) |
| **Cobros** | "Costos Operacionales" + "Costos Comerciales" | **New concept** — group all fees |
| **Disponible** | "Resultado Neto" / "Net Revenue" | Rename to "Disponible" |
| **Comisiones** | Part of "Costos Comerciales" | Extract as sub-concept |
| **Logística** | Part of "Costos Operacionales" | Extract as sub-concept |
| **Publicidad** | Part of "Costos Comerciales" | Extract as sub-concept |
| **Servicios** | Asesoría Comercial (comerciales) | Extract as sub-concept |
| **Ajustes** | "Ajustes" financial group | Keep + rename |

### 3.3 Cobros Breakdown (Concept-Level)

Since the DB uses `financial_group` for classification and `detalle` for concept name, the mapping from DB concepts to Gerencial sub-concepts is:

| Sub-Concept | DB financial_group | DB detalle (examples) |
|------------|-------------------|----------------------|
| **Comisiones** | costos_comerciales | Comisiones sobre pedidos, Cargo por venta (Comisión), Comisión por venta |
| **Logística** | costos_operacionales | Cargo por envíos, Gastos de envío, Despacho, Logística inversa |
| **Publicidad** | costos_comerciales | Product Ads, Cargo por publicidad, Cargo por publicación |
| **Servicios** | costos_comerciales | Cargo por Asesoría Comercial |
| **Fullfilment** | costos_operacionales | Full, Costo fullfilment, Almacenamiento |
| **Descuentos** | ajustes | Descuento comercial, Descuento por cancelación |
| **Bonificaciones** | ajustes (+ sign) | Bonificación, Incentivo, Compensación logística |
| **Procesamiento Pago** | costos_comerciales | Tarifa de procesamiento, Costo por cuotas |

### 3.4 Explicabilidad (FASE 7)

Each KPI must answer:
- **Qué es**: Definition in gerencial language
- **Cómo se calcula**: Formula from certified data
- **Qué incluye**: List of concepts included
- **Qué no incluye**: Exclusions

**Example — Cobros:**

> **¿Qué es?** Cobros representa el total de cargos, comisiones y costos que los marketplaces nos descuentan sobre las ventas.
>
> **¿Cómo se calcula?** Cobros = Comisiones + Logística + Publicidad + Servicios + Fullfilment + Descuentos + Ajustes Netos
>
> **¿Qué incluye?** Todo cargo de marketplace: comisiones por venta, costos de envío, publicidad, servicios profesionales, fullfilment, descuentos comerciales, bonificaciones e incentivos.
>
> **¿Qué no incluye?** No incluye devoluciones ni reembolsos (están en Devoluciones). No incluye IVA ni impuestos.

### 3.5 Key Formula

```
Disponible = Ventas - |Devoluciones| - |Cobros|
```

Where:
- `Ventas` = SUM(financial_group = 'ingresos')
- `Devoluciones` = SUM(financial_group = 'devoluciones') (already negative)
- `Cobros` = SUM(financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes'))
- `Disponible` = resultado_neto from marketplace_cierre_financiero_v1 (certified)

### 3.6 Data Flow

```
marketplace_cierre_financiero_v1 (certified)
    → /api/v4/exec/summary + /api/v4/exec/waterfall
    → Frontend JS mapping → Gerencial taxonomy
    → Render hierarchy: Ventas → Devoluciones → Cobros → Disponible

marketplace_ledger_v1 (certified)
    → /api/v4/cierre/desglose
    → Frontend per-detalle mapping → Concept breakdown
    → Render Cobros sub-concepts matrix

marketplace_auditoria_v1 (certified)
    → /api/v4/exec/audit-drilldown
    → Frontend render (unchanged)
```

**No new endpoints required. No DB queries. No financial logic duplicated.**

### 3.7 Success Criteria

| Question | How the converged dashboard answers it |
|----------|--------------------------------------|
| 1. ¿Cuánto vendimos? | **Ventas** KPI card shows total gross revenue |
| 2. ¿Cuánto nos devolvieron? | **Devoluciones** KPI card shows total returns |
| 3. ¿Cuánto nos cobraron? | **Cobros** KPI card shows total fees + costs |
| 4. ¿Cuánto quedó disponible? | **Disponible** KPI card shows net = Ventas - Devoluciones - Cobros |
| 5. ¿Qué marketplace aporta más? | Scorecard shows per-MP Disponible sorted descending |
| 6. ¿Dónde se fue el dinero? | Cobros Breakdown matrix shows Comisiones, Logística, Publicidad, etc. |
| 7. ¿Qué cambió respecto al período anterior? | Period comparison in KPI cards (delta arrows) |

---

**Documento generado:** 2026-06-04  
**Status:** READ ONLY — Guía de convergencia para Executive Dashboard UX1.1
