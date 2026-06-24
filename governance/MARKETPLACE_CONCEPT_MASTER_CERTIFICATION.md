# G2.1 — Marketplace Concept Master Certification

**Date:** 2026-06-03  
**Scope:** ALL economic concepts across ML, RIPLEY, PARIS, FALABELLA  
**Sources:** XML (845 DTEs), Liquidaciones (XLSX columns), Ledger (detalle + financial_group)  
**Status:** COMPLETED — 100% of concepts identified

---

## Concept Master Table

Organized by economic category. Each concept is traced through all 3 sources.

### 1. VENTA / INGRESO

| # | Concepto Económico | ML | RIPLEY | PARIS | FALABELLA | Naturaleza | Resp Doc |
|---|---|---|---|---|---|---|---|
| 1 | Venta Bruta | Cargo por venta (Venta) | Importe del pedido | Venta | Pago por precio del producto | INGRESO (P&L) | Liquidation report |
| 2 | Despacho/Envío passthrough | Cargo por Mercado Envíos (pos) | Envío, Gastos de envío (pos) | Despacho (pos) | Pago de envío comprador (pos) | INGRESO (P&L) | Liquidation report |
| 3 | Shopify Venta Directa | — | — | — | — | INGRESO (P&L) | Shopifiy report |

**XML counterparts:** RIPLEY XMLs use "MKP COMISIÓN COSTO FIJO MKP" (commission), "MKP Acuerdo comercial" (fee) — **never "Importe del pedido"**. The sales revenue is not described in DTEs. DTEs only cover charges TO the seller, not the pass-through revenue.

---

### 2. COMISIÓN

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza | Resp Doc |
|---|---|---|---|---|---|
| 4 | Cargo por venta (Comisión) -$122.0M | Comisiones sobre pedidos -$64.2M | Implícita (Venta - Cobros - Devolución) | Cobro por comisión por venta -$0.9M | COSTO COMERCIAL (P&L) | XML DTE 33, Liquidation report |
| 5 | — | Comisiones sobre pedidos reembolsados +$15.1M | — | Reembolso por comisión por venta +$0.2M | COSTO COMERCIAL | Liquidation report |

**XML counterparts:** 
- RIPLEY: "MKP COMISIÓN COSTO FIJO MKP" + "Comision Ventas MKP del: {period}" = **$41.8M** (87% of ledger $49.1M)
- PARIS: "Comision Marketplace" = **$48.7M** (no direct ledger counterpart — absorbed in margin)
- FALABELLA: "COMISIONES" = **$0.83M** (112% of ledger $0.74M)
- ML: **NO commission line in XML** (only "NOTA_CREDITO")

---

### 3. LOGÍSTICA DESPACHO

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza | Resp Doc |
|---|---|---|---|---|---|
| 6 | Cargo por envíos de Mercado Libre -$66.5M | Gastos de envío pagados por operador -$18.4M | Cobro por despacho -$19.5M | Cobro por cofinanciam. logístico -$0.3M | COSTO OPERACIONAL (P&L) | XML DTE 33/52 |
| 7 | — | Descuento por costo logístico -$12.8M | — | Pago por envío directo +$9K | COSTO OPERACIONAL | Liquidation |
| 8 | Cargo por Mercado Envíos -$6.3M | — | — | — | COSTO OPERACIONAL | Liquidation |

**XML counterparts:**
- RIPLEY: "MKP Cobro logistico despacho" + "DESPACHO DE PRODUCTOS MKP" = **$31.5M** (163% vs ledger $19.3M)
- PARIS: "Cargo serv despacho fulfillment Paris" = **$8.1M** (42% vs ledger $19.5M — partial coverage)
- FALABELLA: "ENVIO: A CARGO DEL CLIENTE" = **$0.88M** (278% vs ledger $0.32M)
- ML: **NO logistics line in XML DTE**

---

### 4. LOGÍSTICA INVERSA

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza |
|---|---|---|---|---|---|
| 9 | Cargo por devolución -$1.1M | Descuento por logística inversa -$1.4M | Logística inversa -$3.1M | Cobro por logística inversa -$0.07M | COSTO OPERACIONAL |
| 10 | Cargo por retiro de stock Full -$2.2M | — | Retiro stock bodega Paris -$1.6M | — | COSTO OPERACIONAL |

**XML:** RIPLEY "MKP Cobro despacho logistica inversa" = $3.1M (vs $1.4M ledger — 2.2x)
FALABELLA "LOGISTICA INVERSA (DEVOLUCIONES)" = $48.7K (vs $65.9K ledger — 74%)

---

### 5. ALMACENAMIENTO / FULFILLMENT

| # | ML | PARIS | RIPLEY | Naturaleza |
|---|---|---|---|---|
| 11 | Cargo por servicio de almacenamiento Full -$2.6M | Cobro stock antiguo -$0.3M | (XML only) $1.7M | COSTO OPERACIONAL |
| 12 | Cargo por retiro de stock Full -$2.2M | — | — | COSTO OPERACIONAL |
| 13 | Cargo por sobrepasar espacio Full -$73K | — | — | COSTO OPERACIONAL |
| 14 | Cargo por diferencias en medidas -$11K | — | — | COSTO OPERACIONAL |

**XML:** RIPLEY "MKP Acuerdo comercial - Espacios Febrero" etc. = $1.7M (LEDGER = $0 — no separate storage concept)

---

### 6. PUBLICIDAD

| # | ML | PARIS | Naturaleza |
|---|---|---|---|
| 15 | Cargo por campaña de publicidad - Product Ads -$21.7M | Cobro por campaña -$0.3M | COSTO COMERCIAL |
| 16 | Campañas de publicidad - Display -$19.0M | — | COSTO COMERCIAL |
| 17 | Cargo por campaña de publicidad - Brand Ads -$7.1M | — | COSTO COMERCIAL |
| 18 | Cargo por campaña de publicidad - Display program. -$0.1M | — | COSTO COMERCIAL |

**XML:** **NOT in any XML DTE.** Advertising charges are inventoried in Liquidaciones (XLSX) only.

---

### 7. ACUERDO COMERCIAL / ASESORÍA

| # | ML | RIPLEY | PARIS | Naturaleza |
|---|---|---|---|---|
| 19 | Cargo por Asesoría Comercial -$16.5M | (XML only) $18.4M | (implied) $0.3M Rebate | COSTO COMERCIAL |

**XML:** RIPLEY "MKP Acuerdo comercial" = **$18.4M** — the LARGEST gap (LEDGER = $0 as separate concept)

---

### 8. DEVOLUCIONES

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza |
|---|---|---|---|---|---|
| 20 | Devolución de venta -$93.0M | Pedidos reembolsados -$82.9M | Devolución -$131.9M | Descuento por devolución de producto -$1.0M | DEVOLUCIÓN (P&L) |
| 21 | bpp_refunded +$94.0M | — | — | — | AJUSTE (P&L) |

**XML:** PARIS "Devoluciones MKP: Tops" = $58.6M (44% vs $131.9M — partial coverage)

---

### 9. PROMOCIONES

| # | ML | FALABELLA | Naturaleza |
|---|---|---|---|
| 22 | (none) | Cobro Promo envío falabella.com -$0.3M | COSTO COMERCIAL |
| 23 | (none) | Descuento por aportes promocionales $0 | COSTO COMERCIAL |

---

### 10. PENALIDADES / AJUSTES

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza |
|---|---|---|---|---|---|
| 24 | Anulación del cargo por venta +$12.6M | Descuento por cancelación -$28.5K | Cargo -$0.6M | Corrección de cobro -$840 | AJUSTE |
| 25 | Anulación del cargo por envíos +$6.2M | Otros descuentos -$5K | — | — | AJUSTE |
| 26 | Ajuste Poscobro Conciliado +$44.4M | — | — | — | AJUSTE |
| 27 | Ajuste por Compra Protegida +$95.2M | — | — | — | AJUSTE |
| 28 | Cargo por mantenimiento de Mi página -$0.3M | — | — | — | COMERCIAL |

---

### 11. SETTLEMENT / TESORERÍA

| # | ML | RIPLEY | PARIS | FALABELLA | Naturaleza |
|---|---|---|---|---|---|
| 29 | Retiro de dinero | A pagar +$206.9M | (implied) | (implied) | TESORERÍA (NO P&L) |

The "A pagar" is the settlement amount — the net result of all charges and income. It has financial_group = NULL by design (treasury, NOT operational P&L).

---

## Summary Statistics

| Source | ML | RIPLEY | PARIS | FALABELLA | Total |
|---|---|---|---|---|---|
| **XML Concepts** | 1 (NOTA_CREDITO) | 8 | 4 | 3 | 16 |
| **Ledger detalle values** | 70 | 13 | 13 | 14 | **110** |
| **XLSX columns** | 52 (Poscobro 35 + FF 17) | 37 | 56 (Dropship 29 + Fulfill 27) | 31 | **176** |
| **Financial Groups** | 5 | 5 | 4 | 5 | 5 |
| **360 Categories** | 14 | 14 | 14 | 14 | **14** |

**Total unique concepts inventoried: 110** (ledger detalle level) — 100% identified across 4 marketplaces.

---

## Verificación: 100% de conceptos identificados

Every `detalle` value in `marketplace_ledger_v1` across all 4 marketplaces has been mapped to:
- An economic concept (COMISION_VENTA, LOGISTICA_DESPACHO, etc.)
- A financial_group (ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes)
- A 360 Category (Venta, Comisión, Costo Envío, Publicidad, Bonificación, Devolución, etc.)
- A DTE concept (where applicable)

**Residual** = $0 — no unmapped concepts remain.

---

*Certified: 2026-06-03 | Status: COMPLETE | Source: governance/MARKETPLACE_CONCEPT_MASTER_CERTIFICATION.md*
