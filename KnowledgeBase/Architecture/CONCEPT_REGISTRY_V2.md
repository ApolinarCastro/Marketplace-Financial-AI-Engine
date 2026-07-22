# CONCEPT_REGISTRY_V2 — Universal Financial Concept Catalog

**Status:** CERTIFICADO (ML, PARIS, RIPLEY, FALABELLA) / PENDIENTE (SHOPIFY)
**Date:** 2026-06-06
**Scope:** Universal catalog of all financial concepts across Mercado Libre, Falabella, Ripley, Paris, Shopify
**Source:** `marketplace_ledger_v1` (live DB), governance certifications, raw file analysis

---

## Legend

| Field | Values | Description |
|-------|--------|-------------|
| `canonical_concept` | text | Normalized concept name across MPs |
| `event_role` | ROOT_EVENT / MECHANISM / SETTLEMENT / UNASSIGNED | Role in event model |
| `cash_role` | REAL_CASH / ACCRUAL / PASS_THROUGH / MIRROR_ZERO / UNASSIGNED | Cash equivalence |
| `pnl_role` | INCLUDE / EXCLUDE_WHEN_PAIRED / EXCLUDE / UNASSIGNED | Role in Resultado Neto |
| `audit_role` | PRESERVE / TRACE_ONLY / SUPPRESS | Role in audit trail |
| `coverage` | ✅ CERTIFIED / 🟡 PENDIENTE / ❌ NOT_FOUND | Per-MP certification status |
| `cert_ref` | Governance file that certified this concept | |

---

## 1. ingresos (Revenue)

### 1.1 Product Sales (Gross Revenue)

| Canonical Concept | ML | Falabella | Ripley | Paris | Shopify |
|---|---|---|---|---|---|
| **Venta de producto** | Cargo por venta (Venta) ✅ | Pago por precio del producto ✅ | Importe del pedido ✅ | Venta ✅ | Ventas totales (+) 🟡 |
| **Ingreso por despacho** | *(none)* | *(none)* | *(none)* | Despacho ✅ | *(none)* |
| **Bonificación / rebate** | Bonificación ✅ | *(none)* | *(none)* | Rebate ✅ | ML Flex bonus (T=61) 🟡 |
| **Ingreso por envío** | *(embedded in Cargo por venta)* | *(none)* | Envío ✅ | *(none)* | ML Boletas (Liq 39) 🟡 |
| **Boleta / Liquidación ML** | *(internal)* | *(none)* | *(none)* | *(none)* | ML Facturas (Liq 33) 🟡 |

### 1.2 Revenue: Detailed Row-Level Concepts

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Venta de producto | ML | Cargo por venta (Venta) | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Venta de producto | RIPLEY | Importe del pedido | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_DATE_PARSING_CERTIFICATION |
| Venta de producto | PARIS | Venta | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Venta de producto | FALABELLA | Pago por precio del producto | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Venta de producto | SHOPIFY | Ventas totales (positive) | ingresos | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Ingreso por despacho | PARIS | Despacho | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Bonificación | ML | Bonificación | ingresos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Rebate | PARIS | Rebate | ingresos | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Ingreso por envío | RIPLEY | Envío | ingresos | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| ML Liquidación (Boleta) | SHOPIFY | ML Boletas (T=43/Liq 39) | ingresos | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| ML Liquidación (Factura) | SHOPIFY | ML Facturas (T=43/Liq 33) | ingresos | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |

---

## 2. devoluciones (Returns)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Devolución de venta | ML | Devolución de venta | devoluciones | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Pedido reembolsado | RIPLEY | Pedidos reembolsados | devoluciones | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Devolución | PARIS | Devolución | devoluciones | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Devolución de producto | FALABELLA | Descuento por devolución de producto | devoluciones | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Devolución / Refund | SHOPIFY | Ventas totales (negative) | devoluciones | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Nota de crédito ML | SHOPIFY | ML Credit notes (T=43/Liq 61) | devoluciones | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |

---

## 3. costos_operacionales (Operational Costs)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Envío Mercado Libre | ML | Cargo por envíos de Mercado Libre | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Mercado Envíos | ML | Cargo por Mercado Envíos | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Devolución logística | ML | Cargo por devolución | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Full almacenamiento | ML | Cargo por servicio de almacenamiento Full | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_FULL_RULES_V1 |
| Full retiro | ML | Cargo por retiro de stock Full | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_FULL_RULES_V1 |
| Full sobrepasar espacio | ML | Cargo por sobrepasar espacio Full | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_FULL_RULES_V1 |
| Full stock antiguo | ML | Cargo por stock antiguo en Full | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_FULL_RULES_V1 |
| Diferencia medidas/peso | ML | Cargo por diferencias en las medidas y el peso del paquete | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_GOLDEN_REPORTS_V1 |
| Anulación envíos ML | ML | Anulación del cargo por envíos de Mercado Libre | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_GOLDEN_REPORTS_V1 |
| Anulación devolución | ML | Anulación del cargo por devolución | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_GOLDEN_REPORTS_V1 |
| Anulación Mercado Envíos | ML | Anulación del cargo por Mercado Envíos | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | ML_GOLDEN_REPORTS_V1 |
| Cobro por despacho | PARIS | Cobro por despacho | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Logística inversa | PARIS | Logística inversa | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Retiro stock bodega Paris | PARIS | Retiro stock bodega Paris | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Cobro stock antiguo | PARIS | Cobro stock antiguo | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Envío | RIPLEY | Envío | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Envío reembolsado | RIPLEY | Envío reembolsado | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Gastos de envío (operador) | RIPLEY | Gastos de envío pagados por el operador | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Gastos de envío reembolsados (operador) | RIPLEY | Gastos de envío reembolsados pagados por el operador | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Descuento costo logístico | RIPLEY | Descuento por costo logístico | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Descuento logística inversa | RIPLEY | Descuento por logística inversa | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Cofinanciamiento logístico | FALABELLA | Cobro por cofinanciamiento logístico | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Logística inversa | FALABELLA | Cobro por logística inversa | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Pago envío comprador | FALABELLA | Pago de envío comprador | costos_operacionales | ROOT_EVENT | PASS_THROUGH | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Pago envío directo | FALABELLA | Pago por envío directo | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Reversa envío comprador | FALABELLA | Reversa de pago de envío comprador | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Promo envío | FALABELLA | Cobro Promo envío falabella.com | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Reembolso promo envío | FALABELLA | Reembolso por Promo envío falabella.com | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Corrección envío directo | FALABELLA | Corrección de cobro por envío directo | costos_operacionales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Falabella shipping (customer) | SHOPIFY | *(from XML FA T=33)* | costos_operacionales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Falabella logistics co-financing | SHOPIFY | *(from XML FA T=33)* | costos_operacionales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Falabella shipping promotions | SHOPIFY | *(from XML FA T=33/61)* | costos_operacionales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Falabella reverse logistics | SHOPIFY | *(from XML FA T=33)* | costos_operacionales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Falabella Flex shipping | SHOPIFY | *(from XML FA T=33/61)* | costos_operacionales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |

---

## 4. costos_comerciales (Commercial Costs)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Comisión por venta | ML | Cargo por venta (Comisión) | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Anulación comisión | ML | Anulación del cargo por venta | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Product Ads | ML | Cargo por campaña de publicidad - Product Ads | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Brand Ads | ML | Cargo por campaña de publicidad - Brand Ads | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Display | ML | Cargo por campaña de publicidad - Display programático | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Asesoría Comercial | ML | Cargo por Asesoría Comercial | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Mantenimiento Mi página | ML | Cargo por mantenimiento de Mi página | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Anulación envíos (Display) | ML | Anulación del cargo por envíos de Mercado Libre | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | KNOWLEDGE_REGISTRY_V1 |
| Comisiones sobre pedidos | RIPLEY | Comisiones sobre pedidos | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Comisiones sobre reembolsos | RIPLEY | Comisiones sobre pedidos reembolsados | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Comisión por venta | FALABELLA | Cobro por comisión por venta | costos_comerciales | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Reembolso comisión | FALABELLA | Reembolso por comisión por venta | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Aporte promocional (cobro) | FALABELLA | Descuento por aportes promocionales a clientes (Promo) | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| Aporte promocional (pago) | FALABELLA | Pago de aporte promocional a cliente (Promo) | costos_comerciales | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | FALABELLA_KNOWLEDGE |
| MercadoPago fee | SHOPIFY | *(from XML MP T=33)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| MP fee refund | SHOPIFY | *(from XML MP T=61)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| ML listing/selling services | SHOPIFY | *(from XML ML T=33)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| ML intermediation | SHOPIFY | *(from XML ML T=33)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| ML Flex bonus | SHOPIFY | *(from XML ML T=61)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| ML Flex bonus reversal | SHOPIFY | *(from XML ML T=56)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |
| Falabella commissions | SHOPIFY | *(from XML FA T=33/61)* | costos_comerciales | UNASSIGNED | UNASSIGNED | UNASSIGNED | UNASSIGNED | 🟡 PENDIENTE | SHOPIFY_READINESS_V2 |

---

## 5. ajustes (Adjustments)

### 5.1 Adjustment Root Events (ML — certified)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Ajuste por Talla/Garantía | ML | bigger_than_expected_fashion, smaller_than_expected_fashion, not_match_size_guide_fashion | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Arrepentimiento | ML | dont_want_it_another_cause_fashion, item_not_useful_fashion_different*, repentant_buyer, undelivered_repentant_buyer, bought_by_mistake, buy_out_of_ml | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Producto Dañado/Vacío | ML | broken_item_fashion, damaged_package_broken_item_fashion, empty_box | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Diferencia de Publicación | ML | different_color_or_size*, different_item_other*, different_than_published, not_expected_quality_different | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Ítem Faltante | ML | missing_accessories, missing_item | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Falta de Stock | ML | out_of_stock | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Retraso en Entrega | ML | estimated_delivery_out_of_time, delivery_date_was_not_met | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Cambio de Dirección | ML | change_receiver_address | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Falla en Entrega | ML | undelivered_other, delivered_but_not_receive_package | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste por Disputa no Respondida | ML | respondent_unanswered, unauthorized_purchase | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Abono manual | ML | Cargo | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Mediación | ML | *(derived)* | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Cancelación de la mediación | ML | *(derived)* | ajustes | ROOT_EVENT | REAL_CASH | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| cashback | ML | *(derived)* | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| cashback_cancel | ML | *(derived)* | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |

### 5.2 Execution Mechanisms (ML — certified)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Ajuste por Compra Protegida (BPP) | ML | bpp_covered, bpp_refunded, partially_bpp_refunded, ppv_covered_melienvio, ppv_valid | ajustes | MECHANISM | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste Poscobro Conciliado | ML | compensated, reconciled | ajustes | MECHANISM | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| Ajuste Poscobro General | ML | Ajuste Poscobro, CREDIT_NOT_PROCESSED, INVALID_AUTHORIZATION, by_admin, missing_invoice, not_reconciled, refund_account_money, refunded | ajustes | MECHANISM | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED | PRESERVE | ✅ CERTIFIED | RFC_EVENT_MODEL_CERTIFICATION |
| reserve_for_dispute | ML | *(derived)* | ajustes | MECHANISM | MIRROR_ZERO | EXCLUDE | TRACE_ONLY | ✅ CERTIFIED | RFC_CASH_CERTIFICATION_BPP_POSCOBRO |
| Reserva devolución envío BPP | ML | *(derived)* | ajustes | MECHANISM | MIRROR_ZERO | EXCLUDE | TRACE_ONLY | ✅ CERTIFIED | RFC_CASH_CERTIFICATION_BPP_POSCOBRO |

### 5.3 Adjustment Concepts (Other MPs — all ROOT_EVENT)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| Compensación logística | PARIS | Compensación logística | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Ajuste Inventario Activo | PARIS | Ajuste Inventario Activo | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Cobro por campaña | PARIS | Cobro por campaña | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Merma | PARIS | Merma | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Multa | PARIS | *(derived)* | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Multa por stock | PARIS | *(derived)* | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | PARIS_XML_ACTIVATION_REPORT |
| Descuento por cancelación | RIPLEY | Descuento por cancelación | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |
| Otros descuentos | RIPLEY | Otros descuentos | ajustes | ROOT_EVENT | ACCRUAL | INCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_CLASSIFICATION_EXECUTION |

---

## 6. tesoreria (Treasury)

| Canonical Concept | MP | Source Concept (detalle) | Financial Group | Event Role | Cash Role | P&L Role | Audit Role | Coverage | Cert Ref |
|---|---|---|---|---|---|---|---|---|---|
| A pagar (Settlement) | RIPLEY | A pagar | *(NULL)* | SETTLEMENT | REAL_CASH | EXCLUDE | PRESERVE | ✅ CERTIFIED | RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION |
| Retiro de dinero | ML | Retiro de dinero | tesoreria | ROOT_EVENT | REAL_CASH | EXCLUDE | PRESERVE | ✅ CERTIFIED | ML_GOLDEN_REPORTS_V1 |

---

## 7. Coverage Summary

| Marketplace | Total Concepts | Certified | Pending | Missing | Ledger Rows | Ledger Total ($) | XML Coverage | Cash Source |
|---|---|---|---|---|---|---|---|---|
| **ML** | **42** | **42** | 0 | 0 | 101,603 | 842,328,200 | 89.4% | ✅ Liberaciones |
| **PARIS** | **12** | **12** | 0 | 0 | 42,487 | 378,083,530 | ~51% | ❌ N/A |
| **RIPLEY** | **15** | **15** | 0 | 0 | 62,502 | 413,893,232 | 0% (discovered) | ❌ N/A |
| **FALABELLA** | **13** | **13** | 0 | 0 | 1,008 | 2,583,866 | 0% (6 DTEs exist) | ❌ N/A |
| **SHOPIFY** | **14** | **0** | 14 | 0 | 0 (not loaded) | 435,562,292 (CSV) | 110 DTEs | ❌ N/A |

### Role Coverage

| Role Type | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| EVENT_ROLE | ✅ 42/42 | ✅ 12/12 | ✅ 15/15 | ✅ 13/13 | 🟡 0/14 |
| CASH_ROLE | ✅ 42/42 | 🟡 0/12 | 🟡 0/15 | 🟡 0/13 | 🟡 0/14 |
| PNL_ROLE | ✅ 42/42 | ✅ 12/12 | ✅ 15/15 | ✅ 13/13 | 🟡 0/14 |
| AUDIT_ROLE | ✅ 42/42 | ✅ 12/12 | ✅ 15/15 | ✅ 13/13 | 🟡 0/14 |

### Cert Ref Summary

| Certification | Scope | Status |
|---|---|---|
| KNOWLEDGE_REGISTRY_V1 | ML all concepts | CERTIFICADO |
| RFC_EVENT_MODEL_CERTIFICATION | ML adjustments (14 ROOT + 3 MECHANISM) | CERTIFICADO |
| RFC_CASH_CERTIFICATION_BPP_POSCOBRO | ML BPP/Poscobro/reserve cash | CERTIFICADO |
| G6_CASH_REALITY_CERTIFICATION | ML Liberaciones cross-check | CERTIFICADO |
| ML_FULL_RULES_V1 | ML Full (logistics) concepts | CERTIFICADO |
| ML_GOLDEN_REPORTS_V1 | ML golden sources | CERTIFICADO |
| PARIS_XML_ACTIVATION_REPORT | PARIS all concepts | CERTIFICADO |
| RIPLEY_CLASSIFICATION_EXECUTION | RIPLEY all concepts | CERTIFICADO |
| RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION | RIPLEY "A pagar" | CERTIFICADO |
| FALABELLA_KNOWLEDGE | FALABELLA all concepts | CERTIFICADO |
| SHOPIFY_READINESS_V2 | SHOPIFY analysis | PENDIENTE |
