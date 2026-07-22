# RIPLEY FINANCIAL CERTIFICATION V1

**Scope:** `scope = RIPLEY`
**Estado:** PRELIMINAR / EVIDENCE BASED

## 1. Executive Summary
Basado estrictamente en la evidencia cruda encontrada en la carpeta `01_Raw/RIPLEY/`, este documento define y certifica preliminarmente el modelo financiero de Ripley. La operación se divide en ciclos de liquidación ("Ciclos de facturación") y se desglosa operacionalmente en logística ("Fulfillment") y consolidación de pagos ("Seller XLSX"). El soporte tributario es electrónico (DTE XML). Se identifican con claridad las ventas brutas, comisiones, impuestos, un gran número de descuentos logísticos y el pago neto esperado. 

## 2. Financial Sources Hierarchy
* **Fuente Financiera Principal:** Reportes XLSX en `Resumen financiero/Seller` (contienen la consolidación final `A pagar` y número de liquidación).
* **Fuente Logística / Operacional Principal:** Reportes CSV en `Resumen financiero/Fulfillment` y `abonos_descuentos_` (contienen la granularidad a nivel de línea y los cargos por Fulfillment).
* **Fuente Documental Principal:** Archivos `dteproveedor_*.xml` en `Documentos Recepcionados` (Facturas electrónicas Tipo 33 emitidas por Ripley al Seller por concepto de servicios y comisiones).

## 3. Financial Flow
* **Qué vende RIPLEY:** El producto del Seller a un cliente final. Genera el ingreso inicial (`Importe del pedido` / `Precio total`).
* **Qué cobra RIPLEY (Ingreso para Ripley):** Comisiones (`Comisiones sobre pedidos` / `Commission (excluding taxes)`), más impuestos sobre dichas comisiones, y gastos asociados a envíos.
* **Qué descuenta RIPLEY (Cargos al Seller):** Cobros de Fulfillment (Sobreestadía, pick and pack, logística inversa, cancelaciones, PDM, despacho primera milla).
* **Qué paga RIPLEY (Egreso al Seller):** El neto final consolidado, representado por la columna `A pagar` (en reportes Seller) o `transfer_amount` (en reportes Fulfillment).

## 4. Documentary Flow
* **Documento que origina la venta:** La orden de compra (identificada como `Order number` o `Orden de compra`).
* **Documento que liquida:** El comprobante de ciclo o liquidación (identificado por el `Número documento liquidación` en los XLSX de Seller, que agrupa un período específico).
* **Documento que respalda tributariamente:** El XML DTE (Tipo 33), que representa la Factura Electrónica de cobro de comisiones y servicios logísticos de Ripley hacia el Seller.

## 5. Matching Candidates
Para garantizar la trazabilidad `RAW -> ETL -> SQL`, las siguientes llaves deberán utilizarse en el modelo de Matching:
1. **Transaccional / Orden:**
   - `Order number` (Ciclos de facturación)
   - `order_id` (Fulfillment)
   - `Orden de compra` (Seller)
2. **Liquidación:**
   - `Número documento liquidación` (Seller)
   - Posible relación con el período de fechas de los archivos CSV de ciclos.
3. **Tributario:**
   - `Número de factura` (Ciclos de facturación)
   - `<NroDTE>` (en XML).

## 6. Financial Components (Certificados por Evidencia)
* **Venta Bruta:** `Precio total (con impuestos)`, `Importe del pedido`.
* **Comisión Marketplace:** `Commission (excluding taxes)`, `Comisiones sobre pedidos`.
* **Costos Logísticos:** `Descuento FF - pick and pack`, `Gastos de envío`, `Cobro despacho primera milla`.
* **Descuentos / Penales:** `Descuento FF - sobreestadía`, `Descuento por logística inversa`, `Descuento por cancelación`.
* **Impuestos:** `Impuestos sobre la comisión`, `Impuestos sobre el precio total`.
* **Pago Neto:** `A pagar`, `transfer_amount`, `Amount transferred to tienda (including taxes)`.

## 7. Risks
* **Encoding (CSVs):** Nombres de columnas con caracteres especiales rotos (`Nmero de factura`, `artculos`, `comisin`) obligan a un parsing resistente.
* **Complejidad Logística:** Existen más de 20 tipos de abonos y descuentos operacionales en los archivos de FF y Seller que requerirán un mapeo taxonómico cuidadoso y exhaustivo.
* **Granularidad Asimétrica:** Los reportes del "Seller" parecen consolidados, mientras que "Fulfillment" y "Ciclos" tienen mayor nivel de línea (`Order line id`, `SKU`).

## 8. Preliminary Certification
Se certifica de manera preliminar que:
1. La información disponible es **suficiente** para construir un Ledger Financiero cerrado.
2. Existe trazabilidad entre la orden, la liquidación financiera y la facturación.
3. El estado de la documentación RAW permite avanzar a la siguiente fase bajo el modelo *Evidence First*.

---

## Recomendación de Siguiente Paso Óptimo
**Propuesta:** Construir el `RIPLEY_ETL_PIPELINE` enfocado exclusivamente en la ingesta (Loader) y normalización (Parser).

**Justificación:** Antes de construir tablas SQL definitivas o conciliaciones financieras complejas, necesitamos estandarizar el "Encoding" de las fuentes, aplanar los XML de manera tabular y homologar las diferentes llaves (`order_id`, `Orden de compra`) bajo una estructura RAW limpia y unificada en la base de datos (Ej: `ripley_raw_seller`, `ripley_raw_cycles`, `ripley_raw_ff`, `ripley_raw_dte`). Esto garantiza aislar Ripley sin modificar infraestructura global.
