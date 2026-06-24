# EVENT_REGISTRY_V1.md — Universal Concept Catalog

**Date:** 2026-06-05  
**Scope:** ML, PARIS, RIPLEY, FALABELLA, SHOPIFY  
**Status:** BLUEPRINT (concepts identified, roles unassigned pending Shopify certification)

---

## Legend

| Field | Values | Description |
|-------|--------|-------------|
| `event_role` | `ROOT_EVENT` / `MECHANISM` / `MIXED` / `UNASSIGNED` | Role in the event model causality |
| `cash_role` | `REAL_CASH` / `ACCRUAL` / `MIRROR_ZERO` / `PASS_THROUGH` / `UNASSIGNED` | Cash equivalence |
| `pnl_role` | `INCLUDE` / `EXCLUDE_WHEN_PAIRED` / `EXCLUDE` / `UNASSIGNED` | Role in Resultado Neto |
| `audit_role` | `PRESERVE` / `TRACE_ONLY` / `SUPPRESS` | Role in audit trail |
| `financial_group` | 6 groups | P&L classification |

---

## ML — Mercado Libre (certified)

| Concept | event_role | cash_role | pnl_role | audit_role | financial_group |
|---------|-----------|-----------|----------|------------|----------------|
| Cargo por venta (Venta) | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Bonificación | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ingresos |
| Importe del pedido | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Pago | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Devolución de venta | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | devoluciones |
| Devolución de dinero | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | devoluciones |
| Cargo por envíos de ML | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cargo por Mercado Envíos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cargo por devolución | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Full storage/retiro/aging | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cargo diferencias medidas/peso | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Envío | ROOT_EVENT | PASS_THROUGH | INCLUDE | PRESERVE | costos_operacionales |
| Cargo por venta (Comisión) | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Anulación del cargo por venta | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Product Ads | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Brand Ads | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Display | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Asesoría Comercial | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Mantenimiento Mi página | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| **Ajuste por Talla/Garantía** | **ROOT_EVENT** | **REAL_CASH** | **INCLUDE** | **PRESERVE** | ajustes |
| **Ajuste por Arrepentimiento** | **ROOT_EVENT** | **REAL_CASH** | **INCLUDE** | **PRESERVE** | ajustes |
| Ajuste por Producto Dañado | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Diferencia Publicación | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Ítem Faltante | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Falta de Stock | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Retraso en Entrega | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Cambio de Dirección | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Falla en Entrega | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Ajuste por Disputa no Respondida | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Abono manual | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| **Ajuste por Compra Protegida (BPP)** | **MECHANISM** | **MIRROR_ZERO** | **EXCLUDE_WHEN_PAIRED** | **PRESERVE** | ajustes |
| **Ajuste Poscobro Conciliado** | **MECHANISM** | **MIRROR_ZERO** | **EXCLUDE_WHEN_PAIRED** | **PRESERVE** | ajustes |
| **Ajuste Poscobro General** | **MECHANISM** | **MIRROR_ZERO** | **EXCLUDE_WHEN_PAIRED** | **PRESERVE** | ajustes |
| Mediación | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| Cancelación de la mediación | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ajustes |
| cashback | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| cashback_cancel | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| reserve_for_dispute | MECHANISM | MIRROR_ZERO | EXCLUDE | TRACE_ONLY | ajustes |
| Reserva devolución envío BBP | MECHANISM | MIRROR_ZERO | EXCLUDE | TRACE_ONLY | ajustes |
| Ajuste histórico (pre-2026) | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Retiro de dinero | ROOT_EVENT | REAL_CASH | EXCLUDE | PRESERVE | tesoreria |

### ML — Certified Pairs (from RFC_EVENT_MODEL)

| ROOT_EVENT | MECHANISM | Shared Orders | Exact Matches | Cash Proxy |
|-----------|-----------|--------------|--------------|------------|
| Talla/Garantía | BPP | 1,902 | 1,751 ($52.4M) | Mediación |
| Talla/Garantía | Poscobro Conciliado | 746 | 637 ($22.3M) | Mediación |
| Arrepentimiento | Poscobro Conciliado | 342 | 297 ($10.1M) | Mediación |
| Arrepentimiento | Poscobro General | 12 | 11 ($0.4M) | Mediación |
| Arrepentimiento | BPP | 844 | — | Mediación |

**Standalone mechanisms preserved:** BPP $2.8M (3.0%), Poscobro Conciliado $3.5M (7.9%), Poscobro General $2.4M (67.8% by amount)

---

## PARIS (certified)

| Concept | event_role | cash_role | pnl_role | audit_role | financial_group |
|---------|-----------|-----------|----------|------------|----------------|
| Venta | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Despacho | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Rebate | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ingresos |
| Devolución | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | devoluciones |
| Cobro por despacho | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Logística inversa | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Retiro stock bodega Paris | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cobro stock antiguo | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Compensación logística | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Ajuste Inventario Activo | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Cobro por campaña | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Merma | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Multa | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Multa por stock | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |

### PARIS — Specific Notes

- **No MECHANISM concepts identified.** PARIS has no adjustment cascade equivalent to ML's BPP/Poscobro. Each row is a direct economic event.
- **Commission is implicit**, embedded in product margin ($48.7M estimated). No explicit commission concept in ledger.
- **Cash cross-check:** NOT performed (no Liberaciones equivalent available). All roles UNASSIGNED pending G6-equivalent certification.

---

## RIPLEY (certified)

| Concept | event_role | cash_role | pnl_role | audit_role | financial_group |
|---------|-----------|-----------|----------|------------|----------------|
| Importe del pedido | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Pedidos reembolsados | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | devoluciones |
| Gastos de envío pagados operador | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Gastos de envío reembolsados op. | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Descuento por costo logístico | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Descuento por logística inversa | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cobro despacho primera milla | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Descuento FF (Otros/pick/sobreestadía) | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Descuento operacional | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Descuento error clase logística | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Abono por uso de flota propia | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Envío reembolsado | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Comisiones sobre pedidos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Comisiones sobre pedidos reembolsados | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Abono oferta TC - OPEX | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Descuento oferta TC - OPEX | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Abonos por cupón promocional | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Descuento por cupones de despacho | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Abonos soluciones comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Descuento por PDM | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Descuento por cancelación | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Otros descuentos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Abono postventa | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Abono formalización a OPL | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Abono extraordinario error precio | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Abono por error de comisión | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Otros abonos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| Descuento por compensación cliente | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ajustes |
| **A pagar** | **SETTLEMENT** | **REAL_CASH** | **EXCLUDE** | **PRESERVE** | *(NULL — treasury)* |

### RIPLEY — Specific Notes

- **No MECHANISM concepts identified.** RIPLEY's $413.9M ledger has no adjustment cascade equivalent to ML BPP/Poscobro.
- **"A pagar"** is NOT a P&L concept. It is the settlement mirror of net P&L ($206.9M = 50/50 monthly). `financial_group=NULL` by design.
- **XML coverage:** 0% certified (407 XMLs discovered but DTEIndexer not executed).
- **Cash cross-check:** NOT performed (no Liberaciones equivalent).
- **Date parsing bug (RFC-001):** FULLY CLOSED (P0→P1, $0 permanent loss, $358M conserved).

---

## FALABELLA (certified)

| Concept | event_role | cash_role | pnl_role | audit_role | financial_group |
|---------|-----------|-----------|----------|------------|----------------|
| Pago por precio del producto | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Cobro por comisión por venta | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ingresos |
| Descuento por devolución producto | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | devoluciones |
| Cobro por cofinanciamiento logístico | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Reversa de pago de envío comprador | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Cobro por logística inversa | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Pago de envío comprador | ROOT_EVENT | PASS_THROUGH | INCLUDE | PRESERVE | costos_operacionales |
| Cobro Promo envío falabella.com | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Reembolso Promo envío falabella.com | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Corrección de cobro por envío directo | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_operacionales |
| Reembolso por comisión por venta | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Pago aporte promocionales (Promo) | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |
| Descuento aportes promocionales (Promo) | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | costos_comerciales |

### FALABELLA — Specific Notes

- **No MECHANISM concepts identified.** 1,008 rows, $2.6M total. No adjustment cascade exists.
- **XML coverage:** 0% certified (DTEs from Falabella.com SpA exist but DTEIndexer not executed).
- **Take rate:** 24.1% (highest of all 4 MPs, but smallest absolute volume).
- **Cash cross-check:** NOT performed.

---

## SHOPIFY (UNASSIGNED — pending onboarding certification)

| Concept | Source | event_role | cash_role | pnl_role | audit_role | financial_group |
|---------|--------|-----------|-----------|----------|------------|----------------|
| Ventas totales | CSV | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ ingresos** |
| MercadoPago fee (T=33) | XML (MP) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| MercadoPago fee refund (T=61) | XML (MP) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| ML Listing/selling services (T=33) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| ML Intermediation (T=33) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| ML Flex platform bonus (T=61) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| ML Flex bonus reversal (T=56) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| ML Boletas (T=43/Liq 39) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ ingresos** |
| ML Facturas (T=43/Liq 33) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ ingresos** |
| ML Credit notes (T=43/Liq 61) | XML (ML) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ devoluciones** |
| Falabella commissions (T=33) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| Falabella commissions (T=61) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_comerciales** |
| Falabella shipping customer (T=33) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_operacionales** |
| Falabella logistics co-financing (T=33) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_operacionales** |
| Falabella shipping promotions (T=33/61) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_operacionales** |
| Falabella reverse logistics (T=33) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_operacionales** |
| Falabella Flex shipping (T=33/61) | XML (FA) | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | *UNASSIGNED* | **→ costos_operacionales** |

### SHOPIFY — Proposed Financial Group Assignment

| Financial Group | Concepts |
|----------------|----------|
| ingresos | Ventas totales (CSV), ML Boletas (Liq 39), ML Facturas (Liq 33) |
| devoluciones | ML Credit notes (Liq 61), Negative Ventas totales rows |
| costos_operacionales | Falabella shipping (all variants), Falabella reverse logistics, Falabella logistics co-financing |
| costos_comerciales | MercadoPago fee, ML listing/selling, ML intermediation, ML Flex bonus (net), Falabella commissions |
| ajustes | *(none identified — SHOPIFY has no adjustment cascade equivalent to ML)* |

### SHOPIFY — ROOT_EVENT vs MECHANISM Hypothesis

**Candidates for ROOT_EVENT:**
- Ventas totales (each row is a direct sale → ROOT_EVENT)
- ML Boletas/Facturas (direct revenue → ROOT_EVENT)
- Falabella commissions (direct cost → ROOT_EVENT)

**Candidates for MECHANISM:**
- **None identified.** SHOPIFY has no concept equivalent to ML's BPP/Poscobro. No adjustment cascade, no paired entries by order.
- This suggests the event model for SHOPIFY is simpler: ALL concepts = ROOT_EVENT.

**Risks requiring validation:**
1. Negative Ventas totales: Are these ROOT_EVENT (direct return) or could they represent a MECHANISM pattern?
2. ML flexible bonus + reversal: Could these form a paired cycle (Bonificación → reversal)?
3. Need to verify no orders have both a cost concept AND a revenue concept for the same event.

### SHOPIFY — Cash Cross-Check Requirement

| Concept | Potential Cash Source | Status |
|---------|---------------------|--------|
| Ventas totales | Bank deposits | PENDIENTE |
| MercadoPago fee | Mercado Pago XML (T=33) | XML exists — need to reconcile |
| ML fees | ML XML (T=33/43) | XML exists — need to reconcile |
| Falabella fees | Falabella XML (T=33) | XML exists — need to reconcile |

**Critical gap:** No bank statement / Liberaciones equivalent available for Shopify. Cash reality certification requires external cash source.
