# KNOWLEDGE_REGISTRY_V1 — Certified Knowledge Registry

**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Propósito:** Registry consultable para skills, marketplaces, conceptos y reglas certificadas

---

## Entity: `knowledge_registry`

| Campo | Valor |
|-------|-------|
| marketplace | `mercadolibre` |
| certification_date | `2026-06-05` |
| certification_status | `CERTIFICADO` |
| knowledge_files | 10 |
| governance_references | 14 |

---

## Skills Certificadas

| Skill | Propósito | Aplica a |
|-------|-----------|----------|
| `conciliacion_fiscal` | Conciliar Facturación ML vs XML DTE | ML, PARIS, FALABELLA, SHOPIFY |
| `conciliacion_operativa` | Conciliar transacciones operacionales (órdenes, pagos, ajustes) | ALL |
| `conciliacion_caja` | Conciliar Liberaciones vs Ledger | ML (otros: PENDIENTE) |
| `cash_reality` | Certificar que números del ledger corresponden a caja real | ML (PASS), otros PENDIENTE |
| `event_model` | Asignar ROOT_EVENT vs MECHANISM por concepto | ALL (ML: CERTIFICADO) |
| `financial_structure` | Mantener taxonomía de 6 grupos P&L | ALL |
| `full_reconciliation` | Conciliar Full (logística) vs transaccional | ML only |
| `postcobro_analysis` | Analizar pipeline postventa | ML only |

---

## Marketplace Features

| Feature | ML | PARIS | RIPLEY | FALABELLA | SHOPIFY |
|---------|----|-------|--------|-----------|---------|
| factura (invoice) | ✅ | ✅ | ✅ | ✅ | ✅ (XML) |
| nota_credito (credit note) | ✅ | ❌ | ❌ | ❌ | ✅ (XML) |
| liberacion (cash settlement) | ✅ | ❌ | ✅ (A pagar) | ❌ | ❌ |
| poscobro (post-sale pipeline) | ✅ | ❌ | ❌ | ❌ | ❌ |
| full (fulfillment logistics) | ✅ | ❌ | ❌ | ❌ | ❌ |
| mediacion (mediation) | ✅ | ❌ | ❌ | ❌ | ❌ |
| bpp (purchase protection) | ✅ | ❌ | ❌ | ❌ | ❌ |
| reserve_for_dispute | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## Concept Registry (ML Certified)

### ROOT EVENTS (14)

| Concept | financial_group | cash_role | pnl_role |
|---------|----------------|-----------|----------|
| Talla/Garantía | ajustes | REAL_CASH | INCLUDE |
| Arrepentimiento | ajustes | REAL_CASH | INCLUDE |
| Producto Dañado/Vacío | ajustes | REAL_CASH | INCLUDE |
| Diferencia Publicación | ajustes | REAL_CASH | INCLUDE |
| Item Faltante | ajustes | REAL_CASH | INCLUDE |
| Falta de Stock | ajustes | REAL_CASH | INCLUDE |
| Retraso en Entrega | ajustes | REAL_CASH | INCLUDE |
| Cambio de Dirección | ajustes | REAL_CASH | INCLUDE |
| Falla en Entrega | ajustes | REAL_CASH | INCLUDE |
| Disputa no Respondida | ajustes | REAL_CASH | INCLUDE |
| Abono manual | ajustes | REAL_CASH | INCLUDE |
| Mediación | ajustes | REAL_CASH | INCLUDE |
| Cancelación de la mediación | ajustes | REAL_CASH | INCLUDE |
| cashback / cashback_cancel | ajustes | ACCRUAL | INCLUDE |

### EXECUTION MECHANISMS (3)

| Concept | financial_group | cash_role | pnl_role |
|---------|----------------|-----------|----------|
| BPP | ajustes | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED |
| Poscobro Conciliado | ajustes | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED |
| Poscobro General | ajustes | MIRROR_ZERO | EXCLUDE_WHEN_PAIRED |

### OTHER (financial concepts, not poscobro)

| Concept | financial_group | cash_role |
|---------|----------------|-----------|
| Cargo por venta (Venta) | ingresos | REAL_CASH |
| Bonificación | ingresos | ACCRUAL |
| Importe del pedido | ingresos | REAL_CASH |
| Pago | ingresos | REAL_CASH |
| Devolución de venta | devoluciones | REAL_CASH |
| Cargo por venta (Comisión) | costos_comerciales | ACCRUAL |
| Product Ads | costos_comerciales | ACCRUAL |
| Brand Ads | costos_comerciales | ACCRUAL |
| Display | costos_comerciales | ACCRUAL |
| Cargo Mercado Envíos | costos_operacionales | ACCRUAL |
| Full (almacenamiento/retiro) | costos_operacionales | ACCRUAL |
| Retiro de dinero | tesoreria | REAL_CASH |

---

## Certified Rules Registry

| Rule ID | Rule | Source |
|---------|------|--------|
| R001 | Facturación ML > Detalle Pagos > Liberaciones > Caja | ML_GOLDEN_REPORTS_V1 |
| R002 | Movimiento de dinero ≠ Evento económico | ML_CASH_REALITY_MODEL_V1 |
| R003 | Liberación ≠ Venta | ML_CASH_REALITY_MODEL_V1 |
| R004 | ROOT_EVENT + MECHANISM = solo ROOT_EVENT en RN | ML_FINANCIAL_EVENT_MODEL_V1 |
| R005 | Poscobro NO es devolución/caja/liberación | ML_POSTCOBRO_RULES_V1 |
| R006 | Venta en Full, ausente en Liquidaciones ≠ inexistente | ML_FULL_RULES_V1 |
| R007 | Prohibido mezclar dominios en conciliación | ML_CONCILIATION_DOMAIN_MODEL_V1 |
| R008 | NO depender exclusivamente de id_orden | ML_TRACEABILITY_MODEL_V1 |
| R009 | Cargo por venta (Venta) es fuente maestra de revenue | ML_GOLDEN_REPORTS_V1 |
| R010 | reserve_for_dispute NET = $0 (all-time) | ML_CASH_REALITY_MODEL_V1 |
