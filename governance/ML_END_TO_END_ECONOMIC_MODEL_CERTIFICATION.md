# CERTIFICACIÓN DEL MODELO ECONÓMICO END-TO-END MERCADO LIBRE
**Priority:** MÁXIMA
**Focus:** Documentary Truth, Evidence First, Zero Assumptions, Zero Heuristics.

---

## FASE 1: MAPA ECONÓMICO COMPLETO

La trazabilidad del ciclo de vida financiero de una transacción en Mercado Libre (ML) refleja la transición desde el reconocimiento del devengado hasta la disponibilidad real de fondos (Caja). 

1. **VENTA & ORDEN**
   - **Origen:** Compra del cliente final.
   - **Archivo:** `Facturacion/Reporte_Facturacion_MercadoLibre_*.xlsx`
   - **Tabla/Atributos:** `Nº de venta`, `Total de la venta`, `Precio unitario`, `Fecha de venta`.
   - **Impacto Económico:** Incremento bruto del GMV (No es caja real aún).

2. **PAGO CLIENTE**
   - **Origen:** Procesamiento del pago vía Mercado Pago.
   - **Archivo:** `Liberaciones/*.xlsx`
   - **Tabla/Atributos:** `MONTO BRUTO DE LA OPERACIÓN`, `ID DE OPERACIÓN EN MERCADO PAGO`.
   - **Impacto Económico:** Recaudo en fideicomiso o pasivo de pasarela.

3. **FACTURACIÓN (DEVENGADO)**
   - **Origen:** Emisión de los cargos y DTEs por parte de ML.
   - **Archivo:** `Facturacion/Reporte_Facturacion_MercadoLibre_*.xlsx` y `Documentos Recepcionados/dteproveedor_*.xml`.
   - **Tabla/Atributos:** `Valor del cargo`, `Porcentaje por categoría`, `Detalle`.
   - **Impacto Económico:** Reconocimiento de costos (Comisiones, Envíos).

4. **LIBERACIÓN (CAJA)**
   - **Origen:** Los fondos superan el periodo de retención y se acreditan en la cuenta de Mercado Pago del Seller.
   - **Archivo:** `Liberaciones/*.xlsx`
   - **Tabla/Atributos:** `TIPO DE REGISTRO` ("Dinero disponible"), `MONTO NETO ACREDITADO`.
   - **Impacto Económico:** Realización del ingreso operativo de caja.

5. **COMISIONES & PUBLICIDAD & FULLFILMENT**
   - **Origen:** Deducciones operativas según uso de servicios.
   - **Archivo:** `Facturacion/*.xlsx` (Desglose de servicios) y `Liquidacion_FF/*.xlsx` (para costos de Fulfillment).
   - **Tabla/Atributos:** `Costo fijo`, `Costo por categoría`, `Liquidación de Factura` (para Full).
   - **Impacto Económico:** Reducción del margen de contribución. Gasto Operativo.

6. **DEVOLUCIONES & RECLAMOS & POSCOBRO**
   - **Origen:** Cancelaciones o disputas posventa.
   - **Archivo:** `Poscobro/*.xlsx` y `Liberaciones/*.xlsx` (Reversiones).
   - **Tabla/Atributos:** `TIPO DE REGISTRO` ("Devolución", "Mediación"), `MONTO NETO DEBITADO`.
   - **Impacto Económico:** Reversión de Ingresos Brutos y posible recuperación de costos.

7. **AJUSTES & TRANSFERENCIA & ABONO BANCARIO**
   - **Origen:** Movimiento de fondos desde Mercado Pago a la cuenta bancaria del Seller.
   - **Archivo:** `Liberaciones/*.xlsx`
   - **Tabla/Atributos:** `TIPO DE REGISTRO` ("Retiro de dinero"), `CUENTA DE DESTINO DEL RETIRO`.
   - **Impacto Económico:** Flujo de Caja Financiero Final.

---

## FASE 2: TRUTH SOURCE ANALYSIS

**FACTURACIÓN:**
- **¿Qué representa?** Eventos **Devengados** y desglose unitario de cobros administrativos.
- **Representa:** El soporte tributario y el detalle unitario de ventas/pedidos, pero *no* la disponibilidad real del dinero.

**LIBERACIONES:**
- **¿Qué representa?** La verdadera **Caja** y flujo de fondos.
- **Representa:** Cobro efectivo, descuentos aplicados directo al saldo y transferencias (retiros). Es el extracto de cuenta corriente.

**POSCOBRO:**
- **¿Qué representa?** Es un archivo de resoluciones posteriores. Representa ajustes temporales, mediaciones o penalizaciones. 
- **Riesgo de Duplicidad:** Alto. Muchos de estos eventos impactan finalmente la cuenta de Liberaciones. Si se suma sin filtrar, duplica el gasto.

**LIQUIDACION_FF:**
- **¿Qué representa?** Es un detalle complementario (Complemento) sobre facturación de logística (Full). 
- **Representa:** Redundancia operativa a nivel financiero, útil solo para auditoría de costos logísticos, pero el descuento del saldo se evidencia en Liberaciones/Facturación.

---

## FASE 3: MARKETPLACE_STATEMENT

Análisis del archivo de salida `marketplace_statement_data.json` / `detail_rows.csv`:

1. **¿Qué modelo financiero utiliza?** Utiliza un modelo híbrido basado en la concatenación de la facturación y la estructura del statement contable, mapeando `raw_type` a `line_item`.
2. **¿Qué universo representa?** El universo de conciliación del Marketplace (Ingresos vs Descuentos reconocidos en documentos).
3. **¿Qué fuente considera verdad?** Considera predominantemente `Facturación` (como se observa en el campo `source: Facturacion`), utilizándola para soportes analíticos.
4. **¿Qué excluye?** Excluye frecuentemente los movimientos puros de caja (retiros bancarios) y las retenciones de fondos temporales.
5. **¿Qué incluye?** Cargos por venta, devoluciones reconocidas, cobros logísticos.
6. **¿Qué eventos ignora?** Ignora los tiempos de tránsito del dinero ("Dinero en cuenta vs Dinero liberado").

---

## FASE 4: COMPARACIÓN DE MODELOS

**MODELO ACTUAL:** `Ventas - Devoluciones - Logística - Comisiones + Ajustes = RN`
- **Fortalezas:** Visibilidad analítica del P&L a nivel unitario (Order-level economics).
- **Debilidades:** Mezcla principios de devengado con caja. No concilia con extracto bancario exacto porque los tiempos de corte de caja difieren de los de facturación.
- **Duplicidades:** Potencial duplicación entre Facturación y Poscobros.

**MODELO MARKETPLACE STATEMENT:** `Ingresos acreditados - Cobros - Devoluciones = Saldo`
- **Fortalezas:** Refleja la cuenta de compensación exacta de la billetera virtual (Mercado Pago). 
- **Omisiones:** Pierde el desglose de los Unit Economics de la venta original, agregando los costos al momento de la liquidación.

---

## FASE 5: ECONOMIC SUBSTANCE TEST

- **VENTA:** `ECONOMIC_EVENT` (Ingreso Bruto Devengado)
- **COMISIÓN:** `ECONOMIC_EVENT` (Costo de Venta Directo)
- **ENVÍO:** `ECONOMIC_EVENT` (Costo de Distribución)
- **PUBLICIDAD:** `ECONOMIC_EVENT` (Gasto de Marketing)
- **DEVOLUCIÓN:** `ECONOMIC_EVENT` (Reversión de Venta / Contra-ingreso)
- **MEDIACIÓN:** `ECONOMIC_EVENT` (Gasto Extraordinario o Recupero)
- **POSCOBRO:** `NON_ECONOMIC_EVENT` (Excepto cuando se cruza como débito en liberación, per se es un evento de seguimiento).
- **CHARGEBACK:** `ECONOMIC_EVENT` (Pérdida por fraude)
- **CASHBACK:** `NON_ECONOMIC_EVENT` (Impacto en pasarela, el seller recibe monto full si es absorbido por ML; si lo asume el seller, es `ECONOMIC_EVENT`).
- **RESERVE_FOR_DISPUTE:** `NON_ECONOMIC_EVENT` (Movimiento patrimonial restrictivo, no afecta el P&L, afecta temporalmente el Cash Flow).
- **FULL (ALMACENAMIENTO):** `ECONOMIC_EVENT` (Costo de Almacenaje / Opex).
- **TRANSFERENCIA (ABONO):** `NON_ECONOMIC_EVENT` (Movimiento de balance: Disminución de Cuentas por Cobrar a aumento de Efectivo. No afecta P&L).

---

## FASE 6: SELLER P&L TRUTH

La arquitectura definitiva de la realidad del Seller **no** es la facturación de la plataforma, sino la **Estructura Híbrida de Caja-Devengado (Seller-Centric)**:

**I. GROSS REVENUE (Ventas Oficiales Devengadas)**
*(Basado en Facturación - Total de la venta)*

**II. REVENUE ADJUSTMENTS (Deducciones a Ingresos)**
- (-) Devoluciones (Cancelaciones completas)
- (-) Descuentos a cargo del Seller
**= NET REVENUE**

**III. COST OF GOODS SOLD (COGS / COSTOS DIRECTOS ML)**
- (-) Comisiones por Venta (Categoría y Costo Fijo)
- (-) Costos de Envío (Propios del pedido)
**= GROSS MARGIN**

**IV. OPERATING EXPENSES (OPEX ML)**
- (-) Almacenamiento Full / Liquidacion FF
- (-) Publicidad (Product Ads)
- (-) Penalizaciones / Ajustes Poscobro Materializados
**= MARKETPLACE OPERATING PROFIT**

**V. CASH FLOW RECONCILIATION (Balance Sheet)**
- (+/-) Variación de Retenciones Temporales (Reservas)
- (=) Dinero Liberado en Mercado Pago (Soporte: Liberaciones)
- (-) Transferencias a Banco Local
**= SALDO EN MERCADO PAGO**

---

## RESPUESTAS OBLIGATORIAS

1. **¿Cuál es el evento raíz del modelo financiero?**
   El evento raíz es la confirmación de la orden en Mercado Libre (que desencadena la pasarela de pago). Desde una óptica de P&L de Seller, la **Liberación (Acreditación del fondo)** debe regir la caja, pero la **Facturación** rige la venta. Financieramente el origen causal (raíz) es la *Orden cobrada*.

2. **¿Cuál es la fuente de verdad oficial?**
   - **Para Cash-Flow / Conciliación Bancaria:** `Liberaciones`.
   - **Para P&L y Unit Economics:** `Facturación`.
   (Si se debe elegir una fuente inmutable que garantiza el dinero, es **Liberaciones**).

3. **¿Qué archivos son redundantes?**
   `Liquidacion_FF` es redundante a nivel financiero total (ya que el cobro final decanta en Facturación y Liberaciones), aunque da el desglose operativo. `Poscobro` a menudo repite ajustes que terminan impactando en `Liberaciones` bajo otro registro.

4. **¿Qué archivos son obligatorios?**
   - `Liberaciones` (El extracto de cuenta y verdad de caja).
   - `Facturación` (El desglose unitario, comisiones e impuestos tributarios).
   - `Documentos Recepcionados` (La validación fiscal final).

5. **¿Qué eventos deben eliminarse del modelo financiero (del P&L)?**
   - `Transferencias / Retiros bancarios` (Son movimientos de cuenta patrimonial, no ganancias ni pérdidas).
   - `Reservas o Retenciones temporales` (Solo afectan el flujo de caja, no el estado de resultados).

6. **¿Qué eventos deben mantenerse obligatoriamente?**
   - Ventas Netas, Devoluciones reales, Cargos por Comisión, Gastos de Envío, Gastos de Publicidad y Ajustes/Mediaciones Falladas.

7. **¿Qué diferencias existen entre marketplace_statement y el sistema actual?**
   `marketplace_statement` está anclado a Facturación (como revela la columna source), buscando catalogar line_items. El sistema actual puro intenta calcular un Net Revenue a través de una cascada que ignora el momento de caja. El statement provee el desglose documental, pero la realidad económica de fondos está en Liberaciones. 

8. **¿Qué arquitectura financiera recomendarías si hoy se reconstruyera el proyecto desde cero?**
   **Architecture: "Dual-Ledger Subledger System"**
   Crear un Ledger de Devengado (basado en Facturación para rentabilidad de SKUs/Órdenes) y un Ledger de Caja (basado en Liberaciones). Ambos cruzan mediante el `ID de Orden` o `Payment ID`. Toda diferencia entre el Devengado y la Caja se clasifica como *Cuentas por Cobrar Mercado Libre* o *Diferencia de Cambio/Ajuste*.

---

## SALIDA FINAL

```json
EVENT_ROOT = "ORDER_CREATION / PAYMENT_APPROVAL"
SINGLE_SOURCE_OF_TRUTH = "LIBERACIONES (FOR CASH) / FACTURACION (FOR P&L DEVENGADO)"
SELLER_PNL_MODEL = "GROSS REVENUE -> NET REVENUE -> GROSS MARGIN -> MARKETPLACE OPERATING PROFIT"
REDUNDANT_SOURCES = ["LIQUIDACION_FF", "POSCOBRO (parcialmente)"]
MANDATORY_SOURCES = ["LIBERACIONES", "FACTURACION", "DOCUMENTOS RECEPCIONADOS (XML)"]
REMOVE = ["TRANSFERENCIAS BANCARIAS", "RESERVE_FOR_DISPUTE (del P&L)"]
KEEP = ["VENTA", "COMISION", "ENVIO", "DEVOLUCION", "PUBLICIDAD"]
REBUILD_RECOMMENDATION = "DUAL-LEDGER SYSTEM (UNIT ECONOMICS LEDGER + CASH SETTLEMENT LEDGER) JOINED BY ORDER_ID"
```
