# CASH_ROLE_REGISTRY_V1 — Universal Cash Role Registry

**Status:** CERTIFICADO (ML only) / UNASSIGNED (PARIS, RIPLEY, FALABELLA, SHOPIFY)
**Date:** 2026-06-06
**Scope:** Cash equivalence assignments per concept across all 5 marketplaces
**Source:** G6_CASH_REALITY_CERTIFICATION, RFC_CASH_CERTIFICATION_BPP_POSCOBRO, CONCEPT_REGISTRY_V2

---

## 1. Cash Role Definitions

| Role | Meaning | P&L Treatment | Evidence Required |
|---|---|---|---|
| **REAL_CASH** | The amount represents actual cash movement. Bank account is debited or credited. | INCLUDE (or EXCLUDE if tesorería) | Bank statement, Liberaciones, settlement report |
| **ACCRUAL** | The amount represents an accrual or provision. Cash may move in a different period or amount. | INCLUDE | Accrual policy, historical cash reconciliation |
| **PASS_THROUGH** | The amount is collected from customer and passed to third party. Zero net P&L impact at group level. | INCLUDE (gross) / EXCLUDE (net) | Payment processor data |
| **MIRROR_ZERO** | The transaction mirrors a ROOT_EVENT on the same order. Net cash impact = $0 when paired. | EXCLUDE_WHEN_PAIRED | Pair analysis, reserve_for_dispute NET=$0 evidence |
| **UNASSIGNED** | Cash role not yet determined. Pending cash source identification. | INCLUDE (default) | — |

---

## 2. ML — Certified Cash Roles (42/42 concepts)

### 2.1 REAL_CASH (18 concepts)

Cash evidence: Liberaciones file (5,142 rows, $259.8M gross, $69.9M net). 3.9% delta vs DB RN ($67.2M). ALTA confidence.

| Concept | Financial Group | Cash Evidence | Delta | Confidence |
|---|---|---|---|---|
| Cargo por venta (Venta) | ingresos | Liberaciones | 3.9% | ALTA |
| Importe del pedido | ingresos | Liberaciones | 3.9% | ALTA |
| Pago | ingresos | Liberaciones | 3.9% | ALTA |
| Devolución de venta | devoluciones | Liberaciones | 3.9% | ALTA |
| Ajuste por Talla/Garantía | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Arrepentimiento | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Producto Dañado/Vacío | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Diferencia Publicación | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Ítem Faltante | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Falta de Stock | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Retraso en Entrega | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Cambio de Dirección | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Falla en Entrega | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Ajuste por Disputa no Respondida | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Abono manual | ajustes | Mediación + Liberaciones | Traced | ALTA |
| Mediación | ajustes | Mediación directa | $10.5M outflow | ALTA |
| Cancelación de la mediación | ajustes | Mediación directa | Traced | ALTA |
| Retiro de dinero | tesoreria | Liberaciones | Traced | ALTA |

### 2.2 ACCRUAL (19 concepts)

No direct cash evidence. These are contractual charges/credits that may or may not result in cash movement in the same period.

| Concept | Financial Group | Reason |
|---|---|---|
| Bonificación | ingresos | Marketing rebate, may be settled via credit note not cash |
| Cargo por venta (Comisión) | costos_comerciales | Commercial cost, netted against Liberaciones |
| Anulación del cargo por venta | costos_comerciales | Correction, no cash movement |
| Product Ads | costos_comerciales | Advertising cost, settled in batch |
| Brand Ads | costos_comerciales | Advertising cost, settled in batch |
| Display | costos_comerciales | Advertising cost, settled in batch |
| Asesoría Comercial | costos_comerciales | Service fee, settled in batch |
| Mantenimiento Mi página | costos_comerciales | Service fee, settled in batch |
| Cargo por envíos de ML | costos_operacionales | Logistics cost, netted against shipping revenue |
| Cargo por Mercado Envíos | costos_operacionales | Logistics cost |
| Cargo por devolución | costos_operacionales | Return logistics cost |
| Full (all types) | costos_operacionales | Fulfillment cost |
| Diferencias medidas/peso | costos_operacionales | Adjustment to logistics cost |
| Anulación envíos/devolución | costos_operacionales | Correction entries |
| cashback | ajustes | Promotional accrual, no direct cash |
| cashback_cancel | ajustes | Reversal of accrual |
| Ajuste histórico (pre-2026) | ajustes | Historical adjustment, cash already moved |

### 2.3 PASS_THROUGH (1 concept)

| Concept | Financial Group | Reason |
|---|---|---|
| Envío (customer-paid shipping) | costos_operacionales | Collected from customer, paid to carrier — zero net |

### 2.4 MIRROR_ZERO (5 concepts)

Cash evidence: reserve_for_dispute NET = $0 (all-time). BPP reserve = $4.57M pairwise zero. Poscobro reserve = $2.52M pairwise zero.

| Concept | Financial Group | Cash Evidence | Standalone $ | % |
|---|---|---|---|---|
| Ajuste por Compra Protegida (BPP) | ajustes | reserve_for_dispute NET=$0 | $2,848,377 | 3.0% |
| Ajuste Poscobro Conciliado | ajustes | reserve_for_dispute NET=$0 | $3,484,068 | 7.9% |
| Ajuste Poscobro General | ajustes | reserve_for_dispute NET=$0 | $2,447,511 | 67.8% |
| reserve_for_dispute | ajustes | reserve NET=$0 | $0 | 0% |
| Reserva devolución envío BPP | ajustes | reserve NET=$0 | $0 | 0% |

---

## 3. PARIS — UNASSIGNED (0/12 concepts)

| Concept | Financial Group | Cash Role | Gap |
|---|---|---|---|
| Venta | ingresos | 🟡 UNASSIGNED | No Liberaciones equivalent |
| Despacho | ingresos | 🟡 UNASSIGNED | No cash source |
| Rebate | ingresos | 🟡 UNASSIGNED | No cash source |
| Devolución | devoluciones | 🟡 UNASSIGNED | No cash source |
| Cobro por despacho | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Logística inversa | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Retiro stock bodega Paris | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Cobro stock antiguo | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Compensación logística | ajustes | 🟡 UNASSIGNED | No cash source |
| Ajuste Inventario Activo | ajustes | 🟡 UNASSIGNED | No cash source |
| Cobro por campaña | ajustes | 🟡 UNASSIGNED | No cash source |
| Merma | ajustes | 🟡 UNASSIGNED | No cash source |

**Observation:** PARIS has no Liberaciones, no bank statement integration, no settlement report. All cash roles will remain UNASSIGNED until an external cash source is identified.

---

## 4. RIPLEY — UNASSIGNED (0/15 concepts)

| Concept | Financial Group | Cash Role | Gap |
|---|---|---|---|
| Importe del pedido | ingresos | 🟡 UNASSIGNED | No Liberaciones equivalent |
| Pedidos reembolsados | devoluciones | 🟡 UNASSIGNED | No cash source |
| Gastos de envío (operador) | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Envío reembolsado | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Comisiones sobre pedidos | costos_comerciales | 🟡 UNASSIGNED | No cash source |
| Descuento por cancelación | ajustes | 🟡 UNASSIGNED | No cash source |
| Otros descuentos | ajustes | 🟡 UNASSIGNED | No cash source |
| **A pagar** | *(NULL)* | 🟡 UNASSIGNED | Is REAL_CASH but uncertified |

**Observation:** "A pagar" is structurally a SETTLEMENT (mirrors RN), so by definition it should be REAL_CASH. However, no external bank settlement report exists to confirm. All other concepts pending cash source.

---

## 5. FALABELLA — UNASSIGNED (0/13 concepts)

| Concept | Financial Group | Cash Role | Gap |
|---|---|---|---|
| Pago por precio del producto | ingresos | 🟡 UNASSIGNED | No Liberaciones equivalent |
| Descuento por devolución producto | devoluciones | 🟡 UNASSIGNED | No cash source |
| Cobro por logística inversa | costos_operacionales | 🟡 UNASSIGNED | No cash source |
| Pago de envío comprador | costos_operacionales | 🟡 UNASSIGNED | Cash pass-through hypothesis |
| Cobro por comisión por venta | costos_comerciales | 🟡 UNASSIGNED | No cash source |
| Reembolso por comisión | costos_comerciales | 🟡 UNASSIGNED | No cash source |
| Aportes promocionales | costos_comerciales | 🟡 UNASSIGNED | No cash source |

**Observation:** "Pago de envío comprador" is a PASS_THROUGH candidate (customer pays → passed to carrier), but no cash evidence exists.

---

## 6. SHOPIFY — UNASSIGNED (0/14 concepts)

| Concept | Source | Financial Group | Cash Role | Gap |
|---|---|---|---|---|
| Ventas totales (positive) | CSV | ingresos | 🟡 UNASSIGNED | No bank statement |
| Ventas totales (negative) | CSV | devoluciones | 🟡 UNASSIGNED | No bank statement |
| MercadoPago fee | XML MP T=33 | costos_comerciales | 🟡 UNASSIGNED | No MP settlement report |
| ML listing/selling services | XML ML T=33 | costos_comerciales | 🟡 UNASSIGNED | No ML settlement report |
| ML intermediation | XML ML T=33 | costos_comerciales | 🟡 UNASSIGNED | No ML settlement report |
| ML Flex bonus/reversal | XML ML T=61/56 | costos_comerciales | 🟡 UNASSIGNED | No ML settlement report |
| Falabella commissions | XML FA T=33/61 | costos_comerciales | 🟡 UNASSIGNED | No FA settlement report |
| Falabella logistics (all) | XML FA T=33 | costos_operacionales | 🟡 UNASSIGNED | No FA settlement report |

**Observation:** 110 XML DTEs exist that could serve as cash evidence for MP/ML/FA fees. CSV "Ventas totales" requires external bank statement for REAL_CASH certification.

---

## 7. Cash Role Summary

| Cash Role | ML Count | PARIS | RIPLEY | FALABELLA | SHOPIFY | Total |
|---|---|---|---|---|---|---|
| REAL_CASH | 18 | 0 | 0 | 0 | 0 | 18 |
| ACCRUAL | 19 | 0 | 0 | 0 | 0 | 19 |
| PASS_THROUGH | 1 | 0 | 0 | 0 | 0 | 1 |
| MIRROR_ZERO | 5 | 0 | 0 | 0 | 0 | 5 |
| UNASSIGNED | 0 | 12 | 15 | 13 | 14 | 54 |
| **Total** | **42** | **12** | **15** | **13** | **14** | **96** |

## 8. Cash Certification Requirements

To certify a marketplace's cash roles:

| Requirement | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| Cash source identified | ✅ Liberaciones | ❌ | ❌ | ❌ | ❌ |
| Delta < 5% | ✅ 3.9% | ❌ | ❌ | ❌ | ❌ |
| reserve_for_dispute NET=$0 | ✅ Verified | N/A | N/A | N/A | N/A |
| Standalone mechanisms measured | ✅ $8.8M | N/A | N/A | N/A | N/A |
| Order-level trace (197 paired orders) | ✅ 97.5% | N/A | N/A | N/A | N/A |
| Bank statement / Liberaciones file | ✅ Available | ❌ | ❌ | ❌ | ❌ |
| Cash reality certification | ✅ G6 + RFC | ❌ | ❌ | ❌ | ❌ |

**Default rule:** Until cash source is identified, all concepts default to ACCRUAL for P&L purposes. This is conservative but may understate or overstate cash timing.
