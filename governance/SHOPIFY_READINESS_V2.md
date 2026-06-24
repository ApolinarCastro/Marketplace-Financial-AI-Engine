# SHOPIFY_READINESS_V2.md — Shopify Onboarding Analysis

**Date:** 2026-06-05  
**Scope:** Read-only analysis of `01_Raw/SHOPIFY/`  
**Status:** PENDIENTE (concepts identified, roles not assigned, no code changes)

---

## 1. Datasets Existentes

| Dataset | Path | Type | Rows | Size | Period |
|---------|------|------|------|------|--------|
| Ventas totales | `Ventas totales - 2025-01-01 - 2026-06-04.csv` | CSV (UTF-8) | 22,172 | 1.4 MB | 2025-01-01 → 2026-06-04 |
| Documentos Recepcionados | `Documentos Recepcionados/dteproveedor_*.xml` | XML (SII DTE) | 110 files | ~1.4 MB total | 2025-01-31 → 2026-05-31 |

### CSV: Columns

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| Día | DATE | Transaction date (YYYY-MM-DD) | No |
| ID de venta | TEXT | Transaction ID (numeric, 14 digits) | No |
| Nombre del pedido | TEXT | Order ID (e.g. `#10018`) | No |
| Nombre del producto | TEXT | Product name at sale time | Sí (32.6% empty) |
| Ventas totales | INTEGER | Amount in CLP | No |

### CSV: Key Stats

| Metric | Value |
|--------|-------|
| Total sales (SUM) | $435,562,292 CLP |
| Positive rows (revenue) | 19,820 (89.4%) |
| Negative rows (returns) | 1,633 (7.4%) |
| Zero rows | 719 (3.2%) |
| Unique orders | 6,600+ (orders #10014 → #17239) |
| Min value | -32,990 CLP |
| Max value | 359,940 CLP |
| Avg value | 19,644 CLP |

### XML: Document Types

| DTE Type | Description | Count | Emitters |
|----------|-------------|-------|----------|
| 33 | Factura Electrónica (Invoice) | ~50 | Mercado Pago, MercadoLibre, Falabella |
| 43 | Liquidación-Factura (Liquidation) | ~30 | MercadoLibre |
| 61 | Nota de Crédito (Credit Note) | ~30 | Mercado Pago, MercadoLibre, Falabella |
| 56 | Nota de Débito (Debit Note) | ~4 | MercadoLibre |

### XML: Emitters

| RUT | Company | Concepts |
|-----|---------|----------|
| 76516950-K | Mercado Pago Operadora S.A. | Payment gateway fee + credits |
| 77398220-1 | MercadoLibre Chile LTDA | Listing fees, intermediation, Flex bonuses, sales summaries |
| 76212492-0 | Falabella.com SpA | Commissions, shipping, logistics, promotions |

### XML: Total Coverage

| Metric | Value |
|--------|-------|
| Total XML files | 110 |
| Earliest date | 2025-01-31 |
| Latest date | 2026-05-31 |
| Receptor (all) | IMPORTADORA Y COMERCIALIZADORA NANDA SPA (RUT 77898100-9) |

---

## 2. Eventos Financieros Existentes

| Event Type | Source | Frequency | Description |
|------------|--------|-----------|-------------|
| Venta | CSV | Daily | Product sale (positive Ventas totales) |
| Devolución | CSV | Daily | Product return (negative Ventas totales) |
| Pago comisión ML | XML (ML, T=33) | Bi-weekly/monthly | MercadoLibre listing & intermediation fees |
| Pago comisión MP | XML (MP, T=33) | Monthly | MercadoPago payment gateway fee |
| Comisión Falabella | XML (FA, T=33) | Monthly | Falabella commission charges |
| Costos logísticos | XML (FA, T=33) | Monthly | Shipping, reverse logistics, promotions |
| Bonos Flex | XML (ML, T=61) | Monthly | MercadoLibre Flex platform rebates |
| Reversa bonos Flex | XML (ML, T=56) | Monthly | Reversal of Flex rebates |
| Notas crédito MP | XML (MP, T=61) | Monthly | MercadoPago fee corrections |
| Liquidación ML | XML (ML, T=43) | Weekly | MercadoLibre sales summaries (Boletas + Facturas + Credit Notes) |

---

## 3. Equivalencia con Taxonomía Financiera

### → ingresos

| Concepto Shopify | Justificación | Riesgo |
|-----------------|---------------|--------|
| **Ventas totales** (positive) | Equivale a "Cargo por venta" o "Importe del pedido" en ML/RIPLEY | Bajo — es el revenue directo |
| **ML Boletas** (T=43/Liq 39) | Representa ventas resumidas por ML | Medio — puede solaparse con Ventas totales CSV |
| **ML Facturas** (T=43/Liq 33) | Representa ventas formales resumidas por ML | Medio — puede solaparse con Ventas totales CSV |

**⚠️ Riesgo de doble conteo:** Las Liquidaciones ML (T=43) resumen las ventas que ML procesó para Shopify. El CSV "Ventas totales" captura TODAS las ventas (incluyendo las no-ML). Hay que determinar si las Liquidaciones ML son SUBSET del CSV o si representan revenue adicional.

### → devoluciones

| Concepto Shopify | Justificación | Riesgo |
|-----------------|---------------|--------|
| **Ventas totales** (negative) | Valores negativos = devoluciones/refunds | Bajo — sign convention consistente |
| **ML Credit Notes** (T=43/Liq 61) | Notas de crédito en liquidaciones ML | Medio — puede solaparse con Ventas totales negativas |

### → costos_operacionales

| Concepto Shopify | Justificación | Riesgo |
|-----------------|---------------|--------|
| **Falabella shipping (customer-paid)** | Envíos a cargo del cliente | Medio — es pass-through, no costo real |
| **Falabella logistics co-financing** | Co-financiamiento logístico Falabella | Bajo |
| **Falabella shipping promotions** | Promociones de envío Falabella | Bajo |
| **Falabella reverse logistics** | Logística inversa (devoluciones) | Bajo |
| **Falabella Flex shipping** | Envío Falabella Directo/Flex | Bajo |

### → costos_comerciales

| Concepto Shopify | Justificación | Riesgo |
|-----------------|---------------|--------|
| **MercadoPago fee** (T=33) | Comisión por gateway de pago | Bajo — equivalente a "Cargo por venta (Comisión)" |
| **MercadoPago fee refund** (T=61) | Corrección de comisión MP | Bajo |
| **ML Listing/selling services** (T=33) | Servicios de publicación y venta ML | Bajo |
| **ML Intermediation** (T=33) | Gestión e intermediación ML | Bajo |
| **ML Flex bonus** (T=61) | Bonificación por uso Flex | Bajo — rebate que reduce costo neto |
| **ML Flex bonus reversal** (T=56) | Anulación de bonificación Flex | Bajo |
| **Falabella commissions** (T=33/61) | Comisiones Falabella | Bajo |

### → ajustes

| Concepto Shopify | Riesgo |
|-----------------|--------|
| **Ninguno identificado** | No existe concepto equivalente a ML BPP/Poscobro |

### → tesoreria

| Concepto Shopify | Riesgo |
|-----------------|--------|
| **No identificado** | No hay "A pagar" equivalente en datos Shopify |

---

## 4. ROOT_EVENT Candidates

Los siguientes conceptos Shopify son candidatos a ROOT_EVENT porque representan eventos económicos directos sin contraparte de mechanism:

| Concept | Evidence | Confianza |
|---------|----------|-----------|
| Ventas totales (positive) | Cada fila = una venta directa. Sin duplicación. | ALTA |
| Ventas totales (negative) | Cada fila = una devolución directa. | ALTA |
| MercadoPago fee | Es el costo directo del gateway de pago. | ALTA |
| ML listing/selling services | Es el costo directo de publicar en ML. | ALTA |
| ML intermediation | Es el costo directo de intermediación ML. | ALTA |
| Falabella commissions | Es la comisión directa de Falabella. | ALTA |
| Falabella logistics | Es el costo logístico directo. | ALTA |

**Total:** ~14 conceptos ROOT_EVENT candidate.

---

## 5. EXECUTION_MECHANISM Candidates

| Concept | Evidence | Confianza |
|---------|----------|-----------|
| **Ninguno identificado** | ML tiene BPP/Poscobro = mechanism porque el mismo evento (Talla) se representa dos veces. Shopify NO tiene este patrón: no hay dos filas con el mismo monto para la misma orden representando el mismo evento económico. | ALTA (negative) |

**Conclusión:** Shopify no tiene MECHANISM concepts. La regla ROOT_EVENT vs MECHANISM no aplica. Todos los conceptos son ROOT_EVENT.

**⚠️ Riesgo:** Esto debe validarse con analysis de órdenes (groupby id_orden) similar al RFC_EVENT_MODEL. Si alguna orden tiene tanto un costo (comisión) como un ingreso (venta) por el mismo monto, sería un mechanism.

---

## 6. Riesgos de Onboarding

| # | Riesgo | Severidad | Descripción | Mitigación |
|---|--------|-----------|-------------|------------|
| 1 | **Doble conteo CSV vs XML** | ALTA | Las Liquidaciones ML (T=43) pueden contener las mismas ventas que el CSV. Si se cargan ambos sin dedup, hay doble conteo de revenue. | Determinar relación: ¿CSV es el total absoluto y Liquidaciones ML son un subset? ¿O son fuentes complementarias? |
| 2 | **Sin cash source** | ALTA | No existe Liberaciones equivalente para Shopify. No se puede certificar cash reality. | Certificar como ACCRUAL-ONLY hasta obtener extractos bancarios. |
| 3 | **CLP como moneda única** | BAJA | Todos los montos están en CLP. El sistema actual solo maneja CLP. Shopify soporta múltiples monedas. | Por ahora CLP-only. Multi-moneda requiere RFC futuro. |
| 4 | **CSV sin ID de transacción único** | MEDIA | `ID de venta` existe pero no sabemos si es estable entre exports. | Validar consistencia del ID entre exports. |
| 5 | **Producto NULL en 32.6% de filas** | MEDIA | 7,231 filas sin nombre de producto. Pueden ser ajustes no-producto. | Verificar si estas filas corresponden a costos/gastos y no a ventas. |
| 6 | **Data gap entre CSV y XML** | ALTA | CSV captura ventas (gross revenue). XMLs capturan costos (comisiones, fees). No están linkeados por ID de orden. | Sin link, no se puede hacer reconciliación orden-por-orden. |
| 7 | **Múltiples emisores XML** | MEDIA | 3 emisores diferentes (MP, ML, Falabella) con formatos DTE distintos. | Cada emisor requiere su propio parsing XML y mapeo de conceptos. |
| 8 | **Sin historial de carga** | MEDIA | No existe loader para Shopify. Toda la infraestructura de ETL debe crearse desde cero. | Usar `marketplace-onboarding` skill + loader spec. |
| 9 | **Receptor común único** | BAJA | Todos los XMLs tienen el mismo receptor (NANDA SPA). La multiempresa requiere segregación por RUT. | Agregar tenant_id = RUT del receptor. |
| 10 | **Posible MECHANISM no detectado** | BAJA | ML Flex bonus (T=61) + ML Flex bonus reversal (T=56) podrían ser un par mechanism en una orden. | Verificar si existen órdenes con ambos conceptos y mismo monto. |

---

## 7. Recomendaciones de Onboarding

### Fase 1: Discovery (no code)
1. Confirmar relación CSV ↔ XML Liquidaciones ML (¿subset o complementario?)
2. Identificar si hay doble conteo entre CSV Ventas totales y ML Liquidaciones
3. Obtener bank statements o Liberaciones equivalente para cash cross-check
4. Validar si el `ID de venta` es estable entre exports

### Fase 2: Loader Spec
1. Definir loader para CSV (`load_shopify_ventas()`)
2. Definir loader para XML DTE (reutilizar `dte_indexer.py`)
3. Decidir estrategia de dedup: ¿CSV como source primario de revenue? ¿XMLs como source de costos?

### Fase 3: Classification
1. Mapear conceptos Shopify a `RAW_TO_CLASSIFICATION_MAP`
2. Asignar financial_group (ver sección 3)
3. Asignar event_role = ROOT_EVENT para todos (pending validación de pares)

### Fase 4: Event Model
1. Verificar groupby por `Nombre del pedido` (id_orden) para detectar posibles pares
2. Confirmar que NO existen MECHANISM concepts

### Fase 5: Certification
1. Cash reality certification (requiere cash source externo)
2. P&L certification (cierre de períodos)
3. Audit certification (XML evidence)
4. 14/14 regression
