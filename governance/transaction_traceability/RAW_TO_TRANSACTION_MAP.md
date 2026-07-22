# RAW → FACT → Ledger Flow

## Documento de Trazabilidad de Transacciones

Version: 1.0

Estado: **IMPLEMENTADO** (basado en `surgical_loader.py` + `marketplace_auditor.py` + Excel Model)

---

## Estructura del Modelo

El sistema financiero opera en tres capas:

```
RAW → FACT → Ledger
```

- **RAW**: Archivos fuente originales (XLSX, CSV, XML) en `01_Raw/` o hojas RAW del Excel.
- **FACT**: Tablas normalizadas de 7 columnas en el modelo Excel (`*_Fact_*` sheets). Columnas: `ID_Transaccion`, `Fecha`, `SKU`, `Monto`, `ID_Marketplace`, `ID_Tipo_Transaccion`, `Cantidad`.
- **Ledger**: `marketplace_ledger_v1` en DuckDB — 9 columnas: `marketplace`, `id_transaccion`, `id_orden`, `fecha`, `detalle`, `monto`, `tipo_movimiento`, `archivo_origen`, `folio_xml`.

El Ledger se clasifica posteriormente en `marketplace_ledger_clasificado_v1` con `financial_group` y `clasificacion_operativa` mediante `MarketplaceAuditorEngine.run_classification()`.

---

## Marketplace: ML (Mercado Libre)

### HECHO OBSERVADO

- 8 hojas FACT en el Excel: `ML_Fact_Ventas`, `ML_Fact_Comisiones`, `ML_Fact_Envios`, `ML_Fact_Publicidad`, `ML_Fact_Bonificaciones`, `ML_Fact_Devoluciones`, `ML_Fact_Asesoria`, `ML_Fact_Fullfilment`. Todas con formato 7-columnas estándar.
- 1 hoja RAW: `ML_Facturacion_RAW` (31 columnas, 64,120 filas) — contiene detalle por cargo individual.
- 1 hoja RAW: `ML_Poscobro_RAW` (35 columnas, 11,815 filas) — ajustes post-cobro.
- En disco: `01_Raw/ML/Facturacion/` (archivos XLSX), `01_Raw/ML/Poscobro/`, `01_Raw/ML/Liberaciones/`, `01_Raw/ML/Documentos Recepcionados/` (DTE XMLs).
- `DATA_MAESTRA_360` consolida todas las FACT sheets en 270,716 filas.

### REGLA CONFIRMADA

| RAW Source | Campo Identificador | Tipo de Movimiento | Regla de Normalización | Destino FACT | Destino Ledger |
|---|---|---|---|---|---|
| `ML_Facturacion_RAW` / `01_Raw/ML/Facturacion/*.xlsx` | `Número de venta` (order_id) | `Cargo por venta` + no `Anulación` | `monto = +Total de la venta` (ingreso), `-Valor del cargo` (comisión) | `ML_Fact_Ventas` (ID_Tipo=1), `ML_Fact_Comisiones` (ID_Tipo=2) | `id_transaccion=SALE_{order_id}…`, monto=+total_venta, `tipo_movimiento=INGRESO_VENTA` + `COMM_{…}`, monto=-valor_cargo, `tipo_movimiento=EGRESO_COMISION` |
| `ML_Facturacion_RAW` / `01_Raw/ML/Facturacion/*.xlsx` | `Número de venta` (order_id) | `Anulación del cargo por venta` | `monto = -Total de la venta` (pérdida), `-Valor del cargo` (reversa comisión: -negativo=+positivo) | `ML_Fact_Devoluciones` (ID_Tipo=6) | `id_transaccion=REFUND_{…}`, monto=-total_venta, `tipo_movimiento=DEVOLUCION` + `REVCOMM_{…}`, monto=-valor_cargo, `tipo_movimiento=AJUSTE` |
| `ML_Facturacion_RAW` / `01_Raw/ML/Facturacion/*.xlsx` | `Número de venta` (order_id) | Otros cargos (envíos, publicidad, full, asesoría) | `monto = -Valor del cargo` (positivo en Excel = costo, se invierte signo) | `ML_Fact_Envios` (ID_Tipo=3), `ML_Fact_Publicidad` (ID_Tipo=4), `ML_Fact_Fullfilment` (ID_Tipo=10), `ML_Fact_Asesoria` (ID_Tipo=9) | `id_transaccion=CHG_{…}`, monto=-valor_cargo, `tipo_movimiento=CARGO` |
| `ML_Facturacion_RAW` / `01_Raw/ML/Facturacion/*.xlsx` | `Número de venta` (order_id) | `Bonificación` | `monto = -Valor del cargo` (bonificación reduce costo) | `ML_Fact_Bonificaciones` (ID_Tipo=5) | `id_transaccion=CHG_{…}`, monto=-valor_cargo, `tipo_movimiento=CARGO` |
| `ML_Poscobro_RAW` / `01_Raw/ML/Poscobro/*.xlsx` | `ID de la orden (order_id)` / `operation_id` | `reason_detail` (ej: `repentant_buyer`, `broken_item_fashion`) | `monto = MontoDevolucion * -1` (si hay devolución) o `Monto` directo. Datos deduplicados por `(operation_id, detalle)`. | No existe FACT directa | `id_transaccion=POS_{op_id}_{…}`, monto=val, `tipo_movimiento=PAGO`, `detalle=reason_detail` |
| `01_Raw/ML/Liberaciones/*.xlsx` | `ID DE OPERACIÓN EN MERCADO PAGO` | `Retiro de dinero` | `monto = MONTO NETO ACREDITADO - MONTO NETO DEBITADO`. Se excluyen `Dinero disponible inicial` y `Total`. | No existe FACT | `id_transaccion=PAYOUT_{…}`, `detalle="Retiro de dinero"`, `tipo_movimiento=ML_LIQUIDACION` |
| `ML_Poscobro_RAW` | `operation_external_reference` | FLOW = `claim` / `refund` / `chargeback` | 99.77% redundante con Facturación + Liberaciones. DEC-009: DELETE del modelo financiero. | N/A — pendiente de eliminación | `include_in_operational_pnl=0` (DEC-019: paired mechanisms) |

**Clasificación a Financial Group** (vía `marketplace_auditor.py:RAW_TO_CLASSIFICATION_MAP` + `FINANCIAL_STRUCTURE`):

| Detalle RAW (normalizado) | Clasificación Operativa | Financial Group |
|---|---|---|
| `Cargo por venta (Venta)` | Cargo por venta (Venta) | `ingresos` |
| `Cargo por venta (Comisión)` | Cargo por venta (Comisión) | `costos_comerciales` |
| `Devolución de venta` / `Devolución de dinero` | Devolución de venta | `devoluciones` |
| `Cargo por Mercado Envíos` / `Cargo por envíos de Mercado Libre` | Cargo por Mercado Envíos | `costos_operacionales` |
| `Cargo por campaña de publicidad - Product Ads` / `- Brand Ads` | Cargo por campaña de publicidad | `costos_comerciales` |
| `Cargo por Asesoría Comercial` | Cargo por Asesoría Comercial | `costos_comerciales` |
| `Cargo por servicio de almacenamiento Full` / `retiro de stock Full` / etc. | Cargo por servicio de almacenamiento Full | `costos_operacionales` |
| `Bonificación` | Bonificación | `ingresos` |
| `Ajuste Poscobro` / `compensated` / `missing_invoice` | Cargo por devolución | `costos_operacionales` |
| `repentant_buyer` / `undelivered_repentant_buyer` / etc. | Ajuste por Arrepentimiento | `devoluciones` (excluido de P&L operacional) |
| `broken_item_fashion` / `empty_box` / `damaged_package_empty_box` | Ajuste por Producto Dañado/Vacío | `devoluciones` (excluido de P&L operacional) |
| `different_than_published` / `different_color_or_size_fashion` | Ajuste por Diferencia de Publicación | `devoluciones` (excluido de P&L operacional) |
| `out_of_stock` | Ajuste por Falta de Stock | `devoluciones` (excluido de P&L operacional) |
| `delivery_date_was_not_met` / `estimated_delivery_out_of_time` | Ajuste por Retraso en Entrega | `devoluciones` (excluido de P&L operacional) |
| `bpp_refunded` / `bpp_covered` / `partially_bpp_refunded` / `ppv_covered_melienvio` / `ppv_valid` | Ajuste por Compra Protegida (BPP) | `devoluciones` (excluido de P&L operacional) |
| `reconciled` | Recuperación por Pérdida de Inventario | `recuperaciones_y_bonificaciones` |
| `Abono manual` / `Cargo` | Abono manual | `ajustes` |
| `Retiro de dinero` / `reserve_for_dispute` / `withdraw` | Retiro de dinero | `tesoreria` |
| `Mediación` / `Cancelación de la mediación` | Mediación | `ajustes` |
| `cashback` / `cashback_cancel` | cashback | `ajustes` |
| `Pago` | Pago | `ajustes` |

**Signo en Ledger**: Positivo = ingreso a favor del vendedor. Negativo = costo/pérdida.
- `INGRESO_VENTA`: monto = +total_venta
- `EGRESO_COMISION`: monto = -valor_cargo
- `DEVOLUCION`: monto = -total_venta
- `CARGO` (envíos, publicidad, etc.): monto = -valor_cargo (valor_cargo es positivo en Excel)
- Anulaciones: `valor_cargo` negativo en Excel → `-(-x) = +x` → ajuste a favor

### PENDIENTE DE VALIDAR

- `ML_Poscobro_RAW` → `ML_Fact_Devoluciones` mapping no está documentado en el loader. Los reason_details de Poscobro (11,914 rows) se cargan directamente al Ledger sin pasar por FACT. Posible gap de trazabilidad.
- `Liquidacion_FF` (90 archivos, 15,521 filas) no es procesado por el pipeline V4. Certificado como ANALYTICAL_SOURCE — $0 información financiera exclusiva, pero requiere verificación periódica.
- Liberaciones tienen `id_orden` en float64. El match correcto requiere `float64 → int → str`.
- DTE XMLs en `Documentos Recepcionados/` (192 archivos) están indexados por `dte_indexer.py` pero NO vinculados al ledger por `folio_xml` para ML (solo 89.4% cobertura).

---

## Marketplace: PARIS

### HECHO OBSERVADO

- 12 hojas FACT en el Excel: `Paris_Fact_Ventas`, `Paris_Fact_Comisiones`, `Paris_Fact_Comisiones_FF`, `Paris_Fact_Logistica`, `Paris_Fact_Publicidad`, `Paris_Fact_Devoluciones`, `Paris_Fact_Devoluciones_FF`, `Paris_Fact_DescuentoComercial`, `Paris_Fact_OtrosCargos`, `Paris_Fact_OtrosCargos_FF`, `Paris_Fact_Ventas_FF`.
- 2 hojas RAW: `Paris_Finanzas_RAW` (29 columnas, 29,979 filas), `Paris_FF_RAW` (27 columnas, 16,885 filas).
- En disco: `01_Raw/PARIS/Transacciones/Dropshipping/` y `Fulfillment/`, `01_Raw/PARIS/Facturacion/` (62 DTE XMLs).
- PARIS es 3P Marketplace (DEC-023) — Cencosud es agente, 17 sellers son principales. Margen 15% = comisión marketplace.
- No existen costos comerciales separados en PARIS por diseño (3P).

### REGLA CONFIRMADA

| RAW Source | Campo Identificador | Tipo de Movimiento | Regla de Normalización | Destino FACT | Destino Ledger |
|---|---|---|---|---|---|
| `Paris_Finanzas_RAW` / `01_Raw/PARIS/Transacciones/Dropshipping/*.xlsx` | `id` | `Venta` (tipo="Venta") | `monto_bruto = monto`, `monto_neto = monto a pagar`. Comisión = neto - bruto. Venta bruta → Ingreso, Comisión → Costo. | `Paris_Fact_Ventas` (ID_Tipo=1), `Paris_Fact_Comisiones` (ID_Tipo=2) | `{id}_GROSS`, monto=monto_bruto, `tipo_movimiento=PAGO` + `{id}_COMM`, monto=comision, `tipo_movimiento=EGRESO_COMISION` |
| `Paris_Finanzas_RAW` / `01_Raw/PARIS/Transacciones/Dropshipping/*.xlsx` | `id` | `Devolución` | `monto_bruto = monto`, `monto_neto = monto a pagar`. Signo negativo conservado del RAW. | `Paris_Fact_Devoluciones` (ID_Tipo=6) | `{id}_GROSS`, monto=monto_bruto, `tipo_movimiento=PAGO` |
| `Paris_Finanzas_RAW` / `01_Raw/PARIS/Transacciones/Dropshipping/*.xlsx` | `id` | `Cobro por despacho` / `Logística inversa` / `Compensación logística` | `monto_neto` directo. | `Paris_Fact_Logistica` (ID_Tipo=3) | `{id}_GROSS`, monto=monto_bruto, `tipo_movimiento=CARGO` |
| `Paris_Finanzas_RAW` / `01_Raw/PARIS/Transacciones/Dropshipping/*.xlsx` | `id` | `Cobro por campaña` / `Rebate` | `monto_neto` directo. | `Paris_Fact_Publicidad` (ID_Tipo=4), `Paris_Fact_DescuentoComercial` (ID_Tipo=11) | `{id}_GROSS`, monto=monto_bruto, `tipo_movimiento=CARGO` |
| `Paris_FF_RAW` / `01_Raw/PARIS/Transacciones/Fulfillment/*.xlsx` | `id` | `Venta` / `Devolución` / `Cobro por despacho` / `Cobro stock antiguo` / `Merma` | Misma lógica que Finanzas RAW. | `Paris_Fact_Ventas_FF` (ID_Tipo=1), `Paris_Fact_Comisiones_FF` (ID_Tipo=2), `Paris_Fact_Devoluciones_FF` (ID_Tipo=6), `Paris_Fact_OtrosCargos_FF` (ID_Tipo=12) | `{id}_GROSS`, monto=monto_bruto |
| `01_Raw/PARIS/Facturacion/*.xml` | Folio DTE (SII) | DTE 33 / 43 / 52 / 61 | DTEIndexer procesa 62 XMLs → `dte_truth_v1`. Vinculación por `folio_xml` no implementada (0% coverage). | No existe FACT | `folio_xml` queda NULL en ledger |

**Clasificación a Financial Group**:

| Detalle RAW (normalizado) | Clasificación Operativa | Financial Group |
|---|---|---|
| `Venta` | Venta | `ingresos` |
| `Cargo por venta (Comisión)` | Cargo por venta (Comisión) | `costos_comerciales` |
| `Devolución` | Devolución | `devoluciones` |
| `Cobro por despacho` | Cobro por despacho | `costos_operacionales` |
| `Logística inversa` | Logística inversa | `costos_operacionales` |
| `Compensación logística` | Compensación logística | `ajustes` |
| `Despacho` | Despacho | `ingresos` |
| `Cobro por campaña` | Cobro por campaña | `ajustes` |
| `Rebate` | Rebate | `ingresos` |
| `Cobro stock antiguo` | Cobro stock antiguo | `costos_operacionales` |
| `Ajuste Inventario Activo` | Ajuste Inventario Activo | `ajustes` |
| `Retiro stock bodega Paris` | Retiro stock bodega Paris | `costos_operacionales` |
| `Merma` | Merma | `ajustes` |
| `Multa` / `Multa por stock` | Multa | `ajustes` |

**Signo en Ledger**: El loader PARIS preserva signos del RAW. `tipo_movimiento` se asigna como "PAGO" si el detalle contiene "pago", "CARGO" en caso contrario. La clasificación posterior determina el financial_group.

### PENDIENTE DE VALIDAR

- No existe `costos_comerciales` separado en PARIS por diseño 3P (DEC-023). Las "comisiones" son implícitas en el spread bruto/neto. Esto debe validarse contra cada contrato de seller.
- `Paris_Fact_Devoluciones` tiene 127,998 filas (la más grande) pero usa 24 columnas no estándar. El mapping detallado no está en el loader — se procesa como cualquier otra fila Paris con `monto_neto`.
- DTE coverage 0% (62 XMLs indexados, 0 vinculados a ledger). Requiere `order_id` matcher (PENDIENTE).
- `Paris_Finanzas_RAW` contiene columna `reputacion` — no está mapeada al ledger.
- Los conceptos `Cargo` (RAW) y `0` / `21430632` (FF_RAW tipo) no tienen clasificación definida.

---

## Marketplace: RIPLEY

### HECHO OBSERVADO

- 7 hojas FACT en el Excel: `Ripley_Fact_Ventas`, `Ripley_Fact_Comisiones`, `Ripley_Fact_Envios`, `Ripley_Fact_Publicidad`, `Ripley_Fact_Devoluciones`, `Ripley_Fact_Envios_Ajustes`, `Ripley_Fact_OtrosCargos`. Formato 7-columnas estándar.
- 1 hoja RAW: `Ripley_Finanzas_RAW` (24 columnas, 127,998 filas) — detalles granulares por transacción.
- En disco: `01_Raw/RIPLEY/` — archivos XLSX con columnas como `Fecha OC`, `Número documento liquidación`, `Orden de compra`, `A pagar`, `Importe del pedido`. Subdirectorios: `CICLOS/` (CSV), `TH/` (Transaction History CSV), `FF/` (Fulfillment CSV).
- El `surgical_loader.py` procesa RIPLEY en 4 flujos: (1) XLSX directos, (2) CSV CICLOS, (3) CSV TH (historial), (4) CSV FF.
- RIPLEY usa UPPERCASE en `financial_group` (INGRESOS, DEVOLUCIONES) — todos los queries deben usar `LOWER()`.
- 32 `detalle` valores → 11 SIGNAL / 21 NOISE (Phase 13 taxonomy).

### REGLA CONFIRMADA

| RAW Source | Campo Identificador | Tipo de Movimiento | Regla de Normalización | Destino FACT | Destino Ledger |
|---|---|---|---|---|---|
| `01_Raw/RIPLEY/*.xlsx` (hojas XLSX) | `Orden de compra` | `Importe del pedido` (A pagar > 0) | `monto` = valor de la columna. `tipo_movimiento=PAGO` si contiene "importe del pedido", "abono", "a pagar". | `Ripley_Fact_Ventas` (ID_Tipo=1) si Importe; `Ripley_Fact_Comisiones` (ID_Tipo=2) si Comisión | `id_transaccion=RIP_{liq}_{order}_{detail}`, monto=directo, `folio_xml=liq_doc` |
| `01_Raw/RIPLEY/*.xlsx` | `Orden de compra` | `Comisiones sobre pedidos` / `Gastos de envío` / etc. | `monto` = valor de la columna. Signo preservado del Excel. | `Ripley_Fact_Comisiones` (ID_Tipo=2), `Ripley_Fact_Envios` (ID_Tipo=3), `Ripley_Fact_Envios_Ajustes` (ID_Tipo=3) | `id_transaccion=RIP_{…}`, monto=directo, `tipo_movimiento=CARGO` |
| `01_Raw/RIPLEY/*.xlsx` | `Orden de compra` | `Devolución` / `Importe del pedido reembolsado` | `monto` preservado. | `Ripley_Fact_Devoluciones` (ID_Tipo=6) | `id_transaccion=RIP_{…}`, monto=directo |
| `01_Raw/RIPLEY/*.xlsx` | `Orden de compra` | `Descuento por cancelación` / `Otros descuentos` | Monto directo. | `Ripley_Fact_OtrosCargos` (ID_Tipo=12) | `id_transaccion=RIP_{…}`, monto=directo |
| `01_Raw/RIPLEY/*.xlsx` | — | Tiene columna `A pagar` | Se usa como total neto. `Importe del pedido` como gross. | `ventas_marketplace` usa Importe del pedido | Ledger usa todas las columnas como `detalle` via melt |
| `01_Raw/RIPLEY/CICLOS/*.csv` | `order number` | CSV con detalle por orden | `monto` parseado con `str.replace(',', '.')`. `folio_xml` = `numero de factura`. | No existe FACT directa | `id_transaccion=RIP_CSV_{…}`, `tipo_movimiento=PAGO` o `CARGO` |
| `01_Raw/RIPLEY/TH/*.csv` | `numero de pedido` | Transaction History | `monto` con signo preservado. Positivo = PAGO, negativo = CARGO. | No existe FACT directa | `id_transaccion=RIP_TH_{…}`. Excluido de P&L operacional (ADJ_01) |
| `01_Raw/RIPLEY/FF/*.csv` | `order_id` | Fulfillment | Columnas financieras detectadas por关键词: amount, fee, descuento, devolución, otros. | No existe FACT directa | `id_transaccion=RIP_FF_{…}` |

**Clasificación a Financial Group** (RIPLEY 11 SIGNAL details):

| Detalle RAW | Clasificación Operativa | Financial Group | Signal/Noise |
|---|---|---|---|
| `Importe del pedido` | Importe del pedido | `ingresos` | SIGNAL |
| `Comisiones sobre pedidos` | Comisiones sobre pedidos | `costos_comerciales` | SIGNAL |
| `Gastos de envío pagados por el operador` | Gastos de envío pagados por el operador | `costos_operacionales` | SIGNAL |
| `Gastos de envío reembolsados pagados por el operador` | Gastos de envío reembolsados pagados por el operador | `costos_operacionales` | SIGNAL |
| `Pedidos reembolsados` | Pedidos reembolsados | `devoluciones` | SIGNAL |
| `Importe del pedido reembolsado` | Importe del pedido reembolsado | `devoluciones` | SIGNAL |
| `Comisiones sobre pedidos reembolsados` | Comisiones sobre pedidos reembolsados | `costos_comerciales` | SIGNAL |
| `Comisión de reembolso` | Comisión de reembolso | `costos_comerciales` | SIGNAL |
| `Envío reembolsado` | Envío reembolsado | `costos_operacionales` | SIGNAL |
| `Importe del envío del pedido` | Importe del envío del pedido | `ingresos` | SIGNAL |
| `Importe del envío del pedido reembolsado` | Importe del envío del pedido reembolsado | `devoluciones` | SIGNAL |
| `A pagar` | A pagar | `tesoreria` | NOISE (treasury) |
| `Otros descuentos` / `Otros abonos` / etc. | (varios) | `ajustes` o `costos_comerciales` | NOISE |

**Deduplicación**: RIPLEY tiene duplicación estructural documentada. `Importe del pedido` + `Precio total` + `Subtotal` pueden coexistir para la misma orden. `ADJ_03` gate: solo 1 de 3 contribuye al P&L operacional. Filas `RIP_CSV_` y `RIP_TH_` excluidas de P&L operacional (ADJ_01).

### PENDIENTE DE VALIDAR

- Los XLSX RIPLEY se procesan con `pd.melt()` que convierte todas las columnas (excepto liq, ord, fecha) en filas `detalle`/`monto`. Esto significa que NO hay una correspondencia 1:1 con las FACT sheets del Excel. Las FACT sheets parecen ser agregaciones pre-calculadas, no el origen directo.
- 407 XMLs descubiertos en `01_Raw/RIPLEY/Documentos Recepcionados/` — NO procesados por DTEIndexer. Cobertura XML = 0%.
- Las 12,822 alertas `cargo_sin_respaldo_legal` son falsos positivos certificados (P16F-04) — los números de referencia XLSX vs folios SII son sistemas diferentes.
- `Ripley_Finanzas_RAW` (127,998 filas, 24 columnas) es la hoja más grande del Excel pero NO es consumida directamente por el loader. Su relación con los XLSX en disco no está documentada.

---

## Marketplace: FALABELLA

### HECHO OBSERVADO

- No existen hojas FACT dedicadas en el Excel para FALABELLA.
- En disco: `01_Raw/FALABELLA/` — archivos XLSX con columnas: `Fecha de Transaccion`, `N de orden`, `Tipo de Transaccion`, `Monto con IVA`, `Falabella-Id`, `SKU vendedor`, `Documento Tributario`.
- 1,008 filas en ledger (el marketplace más pequeño: $2.6M total).
- 1 fila NO_CLASIFICADO conocida ($12,099, "Cobro por comisión por cancelación").

### REGLA CONFIRMADA

| RAW Source | Campo Identificador | Tipo de Movimiento | Regla de Normalización | Destino FACT | Destino Ledger |
|---|---|---|---|---|---|
| `01_Raw/FALABELLA/*.xlsx` | `N de orden` | `Precio del producto` | `monto` directo. `tipo_movimiento=PAGO` si contiene "pago" o "precio del producto". | No existe FACT en Excel | `id_transaccion=FAL_{id}_{idx}`, monto=directo |
| `01_Raw/FALABELLA/*.xlsx` | `N de orden` | `Cobro por comisión por venta` / `Cobro por cofinanciamiento logístico` / etc. | `monto` directo. `tipo_movimiento=CARGO`. | No existe FACT en Excel | `id_transaccion=FAL_{…}` |
| `01_Raw/FALABELLA/*.xlsx` | `N de orden` | `Reversa de pago de envío comprador` / `Reembolso por comisión por venta` | `monto` directo (negativo en origen). | No existe FACT en Excel | `id_transaccion=FAL_{…}` |
| `01_Raw/FALABELLA/*.xlsx` | `N de orden` | `Cobro por logística inversa` | `monto` directo. | No existe FACT en Excel | `id_transaccion=FAL_{…}` |
| `01_Raw/FALABELLA/*.xlsx` | `Documento Tributario` | Folio DTE SII | Se extrae como `folio_xml`. DTEIndexer procesó 6 XMLs → 0 matches. | No existe FACT | `folio_xml` en ledger (0% coverage) |

**Clasificación a Financial Group**:

| Detalle RAW | Clasificación Operativa | Financial Group |
|---|---|---|
| `Pago por precio del producto` | Pago por precio del producto | `ingresos` |
| `Cobro por comisión por venta` | Cobro por comisión por venta | `costos_comerciales` |
| `Cobro por cofinanciamiento logístico` | Cobro por cofinanciamiento logístico | `costos_operacionales` |
| `Reversa de pago de envío comprador` | Reversa de pago de envío comprador | `costos_operacionales` |
| `Cobro Promo envío falabella.com` | Cobro Promo envío falabella.com | `costos_operacionales` |
| `Reembolso por Promo envío falabella.com` | Reembolso por Promo envío falabella.com | `costos_operacionales` |
| `Reembolso por comisión por venta` | Reembolso por comisión por venta | `costos_comerciales` |
| `Cobro por logística inversa` | Cobro por logística inversa | `costos_operacionales` |
| `Descuento por devolución de producto` | Descuento por devolución de producto | `devoluciones` |
| `Pago de envío comprador` | Pago de envío comprador | `costos_operacionales` |
| `Corrección de cobro por envío directo` | Corrección de cobro por envío directo | `ajustes` |
| `Pago de aporte promocionales a cliente (Promo)` | Pago de aporte promocionales | `costos_comerciales` |
| `Descuento por aportes promocionales a clientes (Promo)` | Descuento por aportes promocionales | `costos_comerciales` |
| `Cobro por comisión por cancelación` | NO_CLASIFICADO | `sin_clasificar` (1 fila, $12,099) |

**Signo**: Preservado del origen. FALABELLA es el único MP donde `tipo_movimiento` no invierte signos.

### PENDIENTE DE VALIDAR

- No existen FACT sheets en el Excel para FALABELLA. Las 7-columnas FACT no se generan. Gap documentado — posiblemente porque FALABELLA se incorporó después del diseño del modelo Excel.
- Cobertura DTE = 0% (6 XMLs procesados, 0 vinculados). Requiere `order_id` matcher.
- La fila NO_CLASIFICADO persiste desde Phase 14 — pendiente de clasificación manual o regla.
- El loader FALABELLA busca columna `Falabella-Id` como transacción ID, pero no todas las filas la tienen — fallback a `FAL_{f.name}_{idx}`.

---

## Marketplace: SHOPIFY

### HECHO OBSERVADO

- 1 hoja FACT: `Shopify_Fact_Ventas` (19,654 rows, 7-columnas estándar, ID_Tipo_Transaccion=1).
- 1 hoja RAW: `Shopify_Ventas_RAW` (22,566 rows, 9 columnas).
- No hay loader implementado en `surgical_loader.py` para SHOPIFY. El `MarketplaceClassifier` lo mapea a `SurgicalLoader` pero `load_marketplace()` solo soporta ML, PARIS, RIPLEY, FALABELLA.

### REGLA CONFIRMADA

| RAW Source | Campo Identificador | Tipo de Movimiento | Regla de Normalización | Destino FACT | Destino Ledger |
|---|---|---|---|---|---|
| `Shopify_Ventas_RAW` | `ID de venta` | Ventas totales | No hay loader — pendiente de implementación. | `Shopify_Fact_Ventas` (ID_Tipo=1) | No implementado |

**Clasificación**: Sin clasificación — no hay filas en ledger.

### PENDIENTE DE VALIDAR

- **NO IMPLEMENTADO**: El loader no soporta SHOPIFY. `SurgicalLoader.load_marketplace()` no tiene branch para SHOPIFY. Las FACT sheets existen en el Excel pero no hay código que las consuma.
- Se requiere implementar `load_shopify()` en `surgical_loader.py` y registrar en `load_marketplace()`.
- `Shopify_Ventas_RAW` tiene columnas: `Día`, `ID de venta`, `Nombre del pedido`, `Nombre del producto`, `Ventas totales` — estructura no estándar.

---

## SAP

### HECHO OBSERVADO

- No existe en el modelo Excel actual.
- No existe loader implementado.
- No hay filas en ledger.

### PENDIENTE DE VALIDAR

- **NO IMPLEMENTADO**: Se requiere integración externa completa.
- Debe generar archivos SAP desde conciliaciones certificadas (FASE 6 del Plan Maestro).
- Flujo propuesto: Conciliación certificada → Selección → Preview → Validación → Aprobación humana → Exportación → Manifiesto.
- No guardar salidas en `01_Raw`. Usar carpeta `exports/`. No hardcodear cuentas SAP.

---

## Dimensión de Tipos de Transacción (Dim_Tipo_Transaccion)

El Excel define 13 tipos de transacción más 4 categorías contables:

| ID | Tipo | Categoría |
|---|---|---|
| 1 | Ingreso por Venta (Marketplace) | Ingresos |
| 2 | Comisión por Venta | Cobros |
| 3 | Costo de Transporte (Envío) | Cobros |
| 4 | Costo de Marketing en Plataforma | Cobros |
| 5 | Ajuste por Incentivo/Bonificación | Ingresos |
| 6 | Ajuste por Devolución | Devoluciones |
| 7 | Impuesto a la Transacción | Cobros |
| 8 | Ajuste por Reembolso | Devoluciones |
| 9 | Costo de Servicios Profesionales | Cobros |
| 10 | Costo de Gestión de Pedidos (Fulfillment) | Cobros |
| 11 | Ajuste por Descuento Comercial | Ingresos |
| 12 | Tarifa de Procesamiento de Pago | Cobros |
| 13 | Ingreso por Venta (Canal Propio) | Ingresos |

Esta dimensión NO es consumida directamente por el ledger. El ledger usa `financial_group` (8 valores: ingresos, devoluciones, costos_operacionales, costos_comerciales, recuperaciones_y_bonificaciones, ajustes, tesoreria, impuestos).

---

## Flujo de Clasificación (Ledger → Clasificado → Cierre)

El flujo completo después de la carga al Ledger es:

1. **`run_classification()`** (`marketplace_auditor.py:410`):
   - Toma `marketplace_ledger_v1` sin clasificar.
   - Aplica `normalize_detail()` (lowercase, sin acentos, sin caracteres especiales).
   - Mapea via `RAW_TO_CLASSIFICATION_MAP` (272 entradas) → `clasificacion_operativa`.
   - No-match: prueba regla dinámica de tesorería, luego regla histórica (pre-2026), luego `NO_CLASIFICADO`.
   - Asigna `include_in_operational_pnl` (DEC-019: paired mechanisms = False).
   - Mapea `clasificacion_operativa` → `financial_group` via `CLASIFICACION_TO_FINANCIAL_GROUP`.
   - Escribe en `marketplace_ledger_clasificado_v1`.

2. **`run_financial_closing()`** (`marketplace_auditor.py`):
   - Agrega por `financial_group` por período.
   - Calcula: `resultado_neto = ingresos + devoluciones + costos_operacionales + costos_comerciales + recuperaciones_y_bonificaciones + ajustes`.
   - Escribe en `marketplace_cierre_financiero_v1`.

3. **Propagación** (`marketplace_auditor.py:581-603`):
   - `clasificacion_operativa`, `include_in_operational_pnl`, `financial_group` se propagan de vuelta a `marketplace_ledger_v1`.

---

## Resumen de Cobertura

| Marketplace | Filas Ledger | FACT sheets en Excel | Loader implementado | DTE/XML coverage | Clasificación |
|---|---|---|---|---|---|
| ML | 101,603 | 8 (7-col estándar) | `load_facturacion()`, `load_poscobro()`, `load_liberaciones()` | 89.4% (Facturación) | 100% |
| PARIS | 42,487 | 10 (7-col estándar) + 2 RAW | `load_paris()` | 0% (62 XMLs indexados) | 100% |
| RIPLEY | 62,502 | 7 (7-col estándar) + 1 RAW | `load_ripley()` (4 sub-flujos) | 0% (407 XMLs descubiertos) | 100% |
| FALABELLA | 1,008 | 0 | `load_falabella()` | 0% (6 XMLs) | 99.9% (1 NO_CLASIFICADO) |
| SHOPIFY | 0 | 1 (7-col) + 1 RAW | **NO IMPLEMENTADO** | 0% | N/A |
| SAP | 0 | 0 | **NO IMPLEMENTADO** | 0% | N/A |

---

## Glosario de Columnas Ledger

| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| `marketplace` | TEXT | `ML`, `PARIS`, `RIPLEY`, `FALABELLA` | Hardcodeado por loader |
| `id_transaccion` | TEXT | ID único de la transacción | Generado por loader: `SALE_{order}_{file}_{idx}`, `RIP_{liq}_{order}_{detail}`, etc. |
| `id_orden` | TEXT | ID de la orden/venta | Columna orden en RAW |
| `fecha` | DATE | Fecha de la transacción | Columna fecha en RAW. RIPLEY usa `dayfirst=True`. |
| `detalle` | TEXT | Descripción del concepto | Columna detalle/tipo en RAW, preservado textual |
| `monto` | DOUBLE | Valor monetario con signo | Calculado por loader según reglas de signo |
| `tipo_movimiento` | TEXT | `INGRESO_VENTA`, `EGRESO_COMISION`, `DEVOLUCION`, `CARGO`, `PAGO`, `AJUSTE`, `ML_LIQUIDACION` | Asignado por loader según lógica de cargo |
| `archivo_origen` | TEXT | Nombre del archivo fuente | `f.name` del archivo procesado |
| `folio_xml` | TEXT | Folio del DTE/SII asociado | Columna factura fiscal en RAW |
| `clasificacion_operativa` | TEXT | Clasificación contable normalizada | `run_classification()` → `RAW_TO_CLASSIFICATION_MAP` |
| `financial_group` | TEXT | Grupo contable: `ingresos`, `devoluciones`, `costos_operacionales`, `costos_comerciales`, `recuperaciones_y_bonificaciones`, `ajustes`, `tesoreria`, `impuestos` | `CLASIFICACION_TO_FINANCIAL_GROUP` map |
| `include_in_operational_pnl` | BOOLEAN | Si la fila participa en P&L operacional | Reglas DEC-019 (paired mechanisms excluded) |
