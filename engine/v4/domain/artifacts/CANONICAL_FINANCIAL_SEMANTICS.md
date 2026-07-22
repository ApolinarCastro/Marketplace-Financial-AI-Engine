# Canonical Financial Semantics

Auto-generated from `engine/v4/domain/canonical_semantics.py`.
**Do not edit manually.** Run `python -m engine.v4.domain.generate_artifacts` to regenerate.

---

## Financial Groups

| Enum Value | Display Name | P&L Order | Amount Sign | Cash Role | Description |
|---|---|---|---|---|---|
| `ingresos` | Ingresos | 1 | POSITIVE | ACCRUAL | Ingresos por ventas brutas del marketplace |
| `devoluciones` | Devoluciones | 2 | NEGATIVE | ACCRUAL | Devoluciones, reembolsos y reversos |
| `costos_operacionales` | Costos Operacionales | 3 | NEGATIVE | ACCRUAL | Costos de logística, envío y operación |
| `costos_comerciales` | Costos Comerciales | 4 | NEGATIVE | ACCRUAL | Comisiones, publicidad y costos de venta |
| `recuperaciones_y_bonificaciones` | Recuperaciones y Bonificaciones | 5 | POSITIVE | ACCRUAL | Recuperaciones de inventario y bonificaciones logísticas |
| `ajustes` | Ajustes | 6 | VARIABLE | ACCRUAL | Ajustes, multas, compensaciones y cargos varios |
| `tesoreria` | Tesorería | 7 | VARIABLE | REAL_CASH | Movimientos de tesorería y settlement (no P&L) |
| `impuestos` | Impuestos | 8 | VARIABLE | ACCRUAL | Impuestos sobre comisiones |

---

## P&L Order

1. `ingresos`
2. `devoluciones`
3. `costos_operacionales`
4. `costos_comerciales`
5. `recuperaciones_y_bonificaciones`
6. `ajustes`
7. `tesoreria`
8. `impuestos`

---

## Marketplaces

| Marketplace | Display Name | Uniqueness Key | Rationale | Signal Taxonomy |
|---|---|---|---|---|
| `FALABELLA` | Falabella | `id_transaccion, detalle` | FALABELLA loader generates one row per concept per order. Grain = (id_transaccion, detalle). Cross-file check via archivo_origen. | Yes |
| `ML` | Mercado Libre | `id_transaccion` | ML loader generates unique id_transaccion per row. No cross-file overlaps. | Yes |
| `PARIS` | Paris | `id_transaccion, archivo_origen, detalle` | Full grain = (id_transaccion, archivo_origen, detalle). Cross-file pipeline overlaps (same detalle, different files) are differentiated by archivo_origen. Intra-file duplicates (test fixtures) by detalle. | Yes |
| `RIPLEY` | Ripley | `id_transaccion, archivo_origen` | Same order appears in parallel FF CSV files. (id_transaccion, archivo_origen) = real unique grain. | Yes |
| `SHOPIFY` | Shopify | `id_transaccion` | Not yet loaded. Default to id_transaccion. | No |

---

## Metric Registry

| Metric | Display Name | Source Table | Granularity | Formula Method | Version | Evidence |
|---|---|---|---|---|---|---|
| `costos_marketplace` | Costos Marketplace | `marketplace_ledger_v1` | period | `FinancialEngine.query_exec_summary().marketplace_costs` | 1.0.0 | PHASE_14_LEDGER_CATEGORY_RECONCILIATION |
| `devoluciones` | Devoluciones (Returns) | `marketplace_ledger_v1` | period | `FinancialEngine.query_exec_summary().returns` | 1.0.0 | PHASE_14_LEDGER_CATEGORY_RECONCILIATION |
| `disponible` | Disponible (Resultado Neto) | `marketplace_ledger_v1` | period | `FinancialEngine.query_waterfall().disponible` | 1.0.0 | PHASE_12C_WATERFALL_CERTIFICATION |
| `ganancia_final` | Ganancia Final | `N/A` | N/A | `GAP — No existe método certificado. No se asume equivalencia con disponible ni ningún otro KPI certificado.` | 1.0.0 | GAP — Sin evidencia de negocio que vincule Ganancia Final a KPIs certificados. |
| `margen` | Margen Neto | `marketplace_ledger_v1` | period | `DERIVED: (disponible / ventas) * 100` | 1.0.0 | G5.6_REVENUE_ENGINE_CERTIFICATION |
| `pendiente_cobro` | Pendiente de Cobro | `marketplace_ledger_v1` | period | `FinancialEngine.query_ledger(financial_group='tesoreria', detalle='A pagar')` | 1.0.0 | GAP_NOT_CERTIFIED — No dedicated endpoint. No settlement/bank linkage available. Uses treasury fallback only. |
| `tesoreria` | Tesorería | `marketplace_ledger_v1` | period | `FinancialEngine.query_ledger(financial_group='tesoreria')` | 1.0.0 | RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION |
| `ventas` | Ventas (Gross Sales) | `marketplace_ledger_v1` | period | `FinancialEngine.query_exec_summary().gross_sales` | 1.0.0 | PHASE_14_LEDGER_CATEGORY_RECONCILIATION |
