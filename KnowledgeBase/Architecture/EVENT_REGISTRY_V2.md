# EVENT_REGISTRY_V2 — Universal Event Role Registry

**Status:** CERTIFICADO (ML, PARIS, RIPLEY, FALABELLA) / PENDIENTE (SHOPIFY)
**Date:** 2026-06-06
**Scope:** Cross-marketplace event role assignments, rules, and causality pairs
**Source:** RFC_EVENT_MODEL_CERTIFICATION, RFC_EVENT_RULE_LOCATION, CONCEPT_REGISTRY_V2

---

## 1. Event Model Architecture

```
                    ROOT_EVENT (causa económica real)
                         │
                         │ paired by id_orden + amount
                         │
                    MECHANISM (representación ejecutora)
                         │
                         ├── PAIRED → MECHANISM excluded from P&L (cash=0)
                         └── STANDALONE → MECHANISM preserved (real cash event)

                    SETTLEMENT (tesorería, espejo del RN)
                         │
                         └── EXCLUDED from P&L (cash flow, not income/expense)
```

**Core Rule (RFC_EVENT_MODEL_CERTIFICATION):** When a ROOT_EVENT and its MECHANISM are paired (same id_orden, matching amount), the MECHANISM is excluded from Resultado Neto (RN). Unpaired STANDALONE mechanisms remain in P&L as real cash events.

**Decision DEC-002 (RFC_EVENT_RULE_LOCATION):** Event model lives in Option D — nueva capa conceptual entre clasificación y cierre. Not in loader, not in classification, not in API.

---

## 2. ROOT_EVENTS — All Marketplaces

### 2.1 Revenue Events (ingresos)

| Canonical Concept | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Venta de producto | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | 🟡 UNASSIGNED |
| Ingreso por despacho | — | ✅ ROOT_EVENT | — | — | — |
| Bonificación / Rebate | ✅ ROOT_EVENT | ✅ ROOT_EVENT | — | — | 🟡 UNASSIGNED |
| Ingreso por envío | — | — | ✅ ROOT_EVENT | — | — |
| ML Liquidación | — | — | — | — | 🟡 UNASSIGNED |

### 2.2 Return Events (devoluciones)

| Canonical Concept | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Devolución / Refund | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | 🟡 UNASSIGNED |

### 2.3 Operational Cost Events (costos_operacionales)

| Canonical Concept | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Envío / Despacho | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | 🟡 UNASSIGNED |
| Logística inversa | — | ✅ ROOT_EVENT | ✅ ROOT_EVENT | ✅ ROOT_EVENT | 🟡 UNASSIGNED |
| Almacenamiento Full | ✅ ROOT_EVENT | — | — | — | — |
| Diferencias medidas/peso | ✅ ROOT_EVENT | — | — | — | — |
| Promociones envío | — | — | — | ✅ ROOT_EVENT | 🟡 UNASSIGNED |

### 2.4 Commercial Cost Events (costos_comerciales)

| Canonical Concept | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Comisión por venta | ✅ ROOT_EVENT | *(implicit)* | ✅ ROOT_EVENT | ✅ ROOT_EVENT | 🟡 UNASSIGNED |
| Publicidad (Ads) | ✅ ROOT_EVENT | — | — | — | — |
| Asesoría Comercial | ✅ ROOT_EVENT | — | — | — | — |
| Aportes promocionales | — | — | — | ✅ ROOT_EVENT | — |
| MercadoPago fee | — | — | — | — | 🟡 UNASSIGNED |
| ML services | — | — | — | — | 🟡 UNASSIGNED |
| Falabella commissions | — | — | — | — | 🟡 UNASSIGNED |

### 2.5 Adjustment Events (ajustes)

| Canonical Concept | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Ajuste Talla/Garantía | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Arrepentimiento | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Producto Dañado | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Diferencia Publicación | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Ítem Faltante | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Falta de Stock | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Retraso Entrega | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Cambio Dirección | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Falla Entrega | ✅ ROOT_EVENT | — | — | — | — |
| Ajuste Disputa no Resp. | ✅ ROOT_EVENT | — | — | — | — |
| Abono manual | ✅ ROOT_EVENT | ✅ ROOT_EVENT | — | — | — |
| Mediación | ✅ ROOT_EVENT | — | — | — | — |
| cashback | ✅ ROOT_EVENT | — | — | — | — |
| Compensación logística | — | ✅ ROOT_EVENT | — | — | — |
| Ajuste Inventario Activo | — | ✅ ROOT_EVENT | — | — | — |
| Cobro por campaña | — | ✅ ROOT_EVENT | — | — | — |
| Merma | — | ✅ ROOT_EVENT | — | — | — |
| Multa / Multa por stock | — | ✅ ROOT_EVENT | — | — | — |
| Descuento por cancelación | — | — | ✅ ROOT_EVENT | — | — |
| Otros descuentos | — | — | ✅ ROOT_EVENT | — | — |
| Corrección envío directo | — | — | — | ✅ ROOT_EVENT | — |

---

## 3. MECHANISMS — ML Only

These concepts exist only in ML. No other marketplace (PARIS, RIPLEY, FALABELLA, SHOPIFY) has an adjustment cascade mechanism.

| Concept | Raw Codes | Orders | Pair Partners | Standalone $ | Standalone % | Cash Source |
|---|---|---|---|---|---|---|
| **Ajuste por Compra Protegida (BPP)** | bpp_covered, bpp_refunded, partially_bpp_refunded, ppv_covered_melienvio, ppv_valid | 3,299 | Talla/Garantía, Arrepentimiento | $2,848,377 | 3.0% | Mediación |
| **Ajuste Poscobro Conciliado** | compensated, reconciled | 1,348 | Talla/Garantía, Arrepentimiento | $3,484,068 | 7.9% | Mediación |
| **Ajuste Poscobro General** | Ajuste Poscobro, CREDIT_NOT_PROCESSED, INVALID_AUTHORIZATION, by_admin, missing_invoice, not_reconciled, refund_account_money, refunded | 654 | Arrepentimiento | $2,447,511 | 67.8% | Mediación |
| **reserve_for_dispute** | *(derived)* | — | — | $0 | — | NET=$0 |
| **Reserva devolución envío BPP** | *(derived)* | — | — | $0 | — | NET=$0 |

**Certified Pairs (RFC_EVENT_MODEL_CERTIFICATION):**

| ROOT_EVENT | MECHANISM | Shared Orders | Exact Matches | Cash Proxy |
|---|---|---|---|---|
| Talla/Garantía | BPP | 1,902 | 1,751 ($52.4M) | Mediación |
| Talla/Garantía | Poscobro Conciliado | 746 | 637 ($22.3M) | Mediación |
| Arrepentimiento | Poscobro Conciliado | 342 | 297 ($10.1M) | Mediación |
| Arrepentimiento | Poscobro General | 12 | 11 ($0.4M) | Mediación |
| Arrepentimiento | BPP | 844 | — (shared) | Mediación |

**Standalone preservation rule:** $8,779,956 (6.2% of total $143.2M mechanisms) remains in P&L as real cash events (RFC_CASH_CERTIFICATION_BPP_POSCOBRO). These are unpaired mechanisms where no corresponding ROOT_EVENT was found.

---

## 4. SETTLEMENT — Treasury Events

| Concept | MP | Role | Cash Evidence | P&L Impact |
|---|---|---|---|---|
| **A pagar** | RIPLEY | SETTLEMENT | Mirror of monthly RN | $0 (50/50 = RN) |
| **Retiro de dinero** | ML | ROOT_EVENT (tesorería) | REAL_CASH | $0 (EXCLUDE from operational P&L) |

**RIPLEY "A pagar":** Financial_group=NULL by design. 11,683 rows, $206,946,843 total. Matches monthly RN 50/50 each month (verified in RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION). It is the settlement mirror — NOT an income or expense.

---

## 5. Event Model Application Per Marketplace

### ML (CERTIFICADO — 3 MECHANISMS)
- Full event model: 42 ROOT_EVENTS + 5 MECHANISMS
- Pairs detected, certified, cash-verified
- RN impact if applied: -$5,313,560 (standalone mechanisms preserved)

### PARIS (CERTIFICADO — 0 MECHANISMS)
- All 12 concepts = ROOT_EVENT
- Commission is implicit in product margin (no visible ledger concept)
- Event model degrades to: ALL concepts INCLUDE in P&L

### RIPLEY (CERTIFICADO — 0 MECHANISMS)
- All 14 concepts (excl. "A pagar") = ROOT_EVENT
- "A pagar" = SETTLEMENT (excluded from P&L)
- Event model degrades to: ALL financial_group concepts INCLUDE + SETTLEMENT EXCLUDE

### FALABELLA (CERTIFICADO — 0 MECHANISMS)
- All 13 concepts = ROOT_EVENT
- No adjustment cascade, no MECHANISMS
- Event model degrades to: ALL concepts INCLUDE in P&L

### SHOPIFY (PENDIENTE — 0 MECHANISMS HYPOTHESIS)
- All 14 candidate concepts = ROOT_EVENT (pending verification)
- Risk: ML Flex bonus + reversal pair needs validation
- Risk: CSV ↔ XML double counting needs resolution
- Event model likely degrades to: ALL concepts INCLUDE

---

## 6. Causality Rules

| Rule ID | Rule | Source | Applies To |
|---|---|---|---|
| R001 | ROOT_EVENT participates in P&L unconditionally | RFC_EVENT_MODEL_CERTIFICATION | ALL MPs |
| R002 | MECHANISM excluded from P&L when paired with ROOT_EVENT | RFC_EVENT_MODEL_CERTIFICATION | ML only |
| R003 | Standalone mechanism preserved in P&L (no pair found) | RFC_CASH_CERTIFICATION_BPP_POSCOBRO | ML only |
| R004 | reserve_for_dispute: EXCLUDE from P&L unconditionally (NET=$0) | RFC_CASH_CERTIFICATION_BPP_POSCOBRO | ML only |
| R005 | MARKETPLACE without cascading mechanisms → ALL concepts = ROOT_EVENT | RFC_EVENT_MODEL_CERTIFICATION | PARIS, RIPLEY, FALABELLA, SHOPIFY |
| R006 | SETTLEMENT concepts excluded from operational P&L | RIPLEY_PAYABLE_SEMANTICS | RIPLEY, ML (Retiro) |
| R007 | Event model lives in conceptual layer between classification and closing | RFC_EVENT_RULE_LOCATION | ALL MPs |
