# ML_CONCILIATION_DOMAIN_MODEL_V1 — Certified Domain Separation

**CERTIFICADO 002**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** MARKETPLACE_CHARGE_RECONCILIATION_V2, MARKETPLACE_ECONOMIC_TRUTH_CERTIFICATION

---

## Dominios de Conciliación

```
DOMAIN_OPERATIONAL (Eventos económicos reales)
├── Venta
├── Orden
├── Paquete
├── Devolución
├── Cargo por venta
├── Comisión
└── Ajuste

DOMAIN_FISCAL (Documentos tributarios)
├── Factura
├── Nota Crédito
├── Cargo (documento fiscal)
├── Bonificación
└── DTE (XML)

DOMAIN_CASH (Movimientos de caja)
├── Liberación
├── Movimiento Mercado Pago
├── Cobro
├── Retiro
├── reserve_for_dispute
└── Mediación
```

## Regla Fundamental

**PROHIBIDO mezclar dominios en una misma conciliación.**

| ❌ Incorrecto | ✅ Correcto |
|--------------|-------------|
| Conciliar Liberaciones vs Facturación | Liberaciones vs Caja |
| Conciliar Poscobro vs Devoluciones | Poscobro vs Facturación + Liberaciones |
| Usar DTE como source transaccional | DTE como evidencia fiscal |
| Conciliar Full contra revenue | Full contra logística |

## Mapeo de Fuentes a Dominios

| Source File | Dominio | Propósito |
|-------------|---------|-----------|
| ML_Facturacion/*.xlsx | OPERATIONAL + FISCAL | Transacciones y facturación |
| Todas_las_Transacciones/*.xlsx | OPERATIONAL | Detalle transaccional completo |
| Detalle_Pagos/*.xlsx | CASH | Pagos y movimientos MP |
| Liberaciones/*.xlsx | CASH | Flujo de caja real |
| DTE XMLs/*.xml | FISCAL | Documentos tributarios |
| Full/*.xlsx | OPERATIONAL (logística) | Operaciones logísticas |

## Reglas de Conciliación por Par

| Par | Dominios | Método |
|-----|----------|--------|
| Facturación ML ↔ Ledger | FISCAL ↔ OPERATIONAL | `folio_xml` match |
| Cargos ↔ Bonificaciones | FISCAL ↔ FISCAL | `cargo_que_bonifica` |
| Liberaciones ↔ Caja | CASH ↔ CASH | reserve_for_dispute NET = $0 |
| Poscobro ↔ Facturación + Liberaciones | OPERATIONAL + CASH | Triangulación 3-vías |

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/MARKETPLACE_CHARGE_RECONCILIATION_V2.md` | Método de conciliación por pares |
| `governance/MARKETPLACE_ECONOMIC_TRUTH_CERTIFICATION.md` | Verdad económica por dominio |
| `governance/MARKETPLACE_MONEY_FLOW_TRUTH.md` | Flujo de dinero (OPERATIONAL + CASH) |
| `governance/MARKETPLACE_WATERFALL_CERTIFICATION.md` | Waterfall cross-domain |

## Aplicación a otros marketplaces

| Marketplace | Operational | Fiscal | Cash |
|-------------|-------------|--------|------|
| RIPLEY | Resumen financiero XLSX | DTE (0%) | A pagar (settlement) |
| PARIS | Transacciones XLSX | DTE (51%) | N/A |
| FALABELLA | Órdenes XLSX | DTE (100%) | N/A |
| SHOPIFY | Ventas totales CSV | DTE (110 files) | N/A |
