# Especificación del Proceso ETL: Falabella y Ripley (Mirakl)

**Fecha:** 05 de Febrero de 2026

**Autor:** Manus AI

**Versión:** 1.0

## 1. Introducción

Este documento detalla el proceso de Extracción, Transformación y Carga (ETL) para automatizar la conciliación de transacciones de **Falabella.cl** y **Ripley.cl** con SAP Business One. Falabella utiliza un sistema propio (Seller Center) con ciclos de facturación mensuales, mientras que Ripley opera sobre la plataforma **Mirakl**, un estándar global para marketplaces con una estructura de datos muy robusta pero compleja.

## 2. Proceso de Extracción (Extract)

### 2.1. Fuente: Falabella Seller Center

-   **Liquidación Factura**: Reporte mensual que contiene el resumen de ventas, comisiones y cargos.
-   **Reporte Histórico de Ventas**: Detalle transaccional de cada orden.
-   **Columnas Clave**:
    -   `Order Number`: ID de la orden (clave de cruce).
    -   `Status`: Estado de la orden (Entregado, Devuelto).
    -   `Unit Price`: Precio de venta.
    -   `Commission`: Monto de la comisión cobrada por Falabella.
    -   `Shipping Fee`: Costo de envío (si aplica).
    -   `Net Amount`: Monto a liquidar.

### 2.2. Fuente: Ripley (Mirakl Platform)

-   **Orders Report**: Detalle comercial de las órdenes.
-   **Transaction History**: El reporte financiero más importante en Mirakl.
-   **Payment Statement**: Resumen del ciclo de pago.
-   **Columnas Clave**:
    -   `Order ID`: ID de la orden.
    -   `Transaction Type`: Tipo (ORDER_PAYMENT, REFUND, COMMISSION, SUBSCRIPTION_FEE).
    -   `Amount`: Monto de la transacción.
    -   `Debit/Credit`: Indicador de flujo de dinero.
    -   `Payment State`: Estado del pago (PAID, PENDING).

## 3. Proceso de Transformación (Transform)

### 3.1. Lógica para Falabella

1.  **Manejo de Ciclos Mensuales**: Falabella suele liquidar a mes vencido. El sistema debe agrupar las ventas por el `Periodo de Liquidación` informado por Falabella para que cuadre con el abono bancario.
2.  **Validación de IVA en Comisiones**: Falabella emite una factura por sus servicios. El sistema debe extraer el IVA de la comisión para registrarlo correctamente como crédito fiscal en SAP.
3.  **Fulfillment by Falabella (FBF)**: Si se usa FBF, los costos de almacenamiento y picking deben separarse de la venta del producto.

### 3.2. Lógica para Ripley (Mirakl)

1.  **Normalización de Transacciones Mirakl**: Mirakl desglosa cada orden en múltiples líneas (Venta, Comisión, IVA Comisión). El sistema debe consolidar estas líneas en un único `order_id_canonico`.
2.  **Tratamiento de Notas de Crédito**: Ripley/Mirakl genera reembolsos que deben cruzarse con las Notas de Crédito en SAP.
3.  **Suscripciones y Multas**: Mirakl permite cobrar suscripciones mensuales al vendedor. Estos cargos "huérfanos" (sin orden asociada) deben registrarse como gastos generales en SAP.

## 4. Motor de Conciliación (Reglas de Negocio)

### 4.1. Regla de Matching

-   **Falabella**: `Order Number` (Falabella) == `Referencia/NumAtCard` (SAP).
-   **Ripley**: `Order ID` (Ripley) == `Referencia/NumAtCard` (SAP).

### 4.2. Lógica de "Triple Conciliación" Aplicada

1.  **Venta**: Validar que el `Unit Price` de Falabella/Ripley coincida con el `DocTotal` de la factura en SAP (restando despacho si aplica).
2.  **Comisión**: Comparar la comisión retenida por el marketplace contra la factura de servicios recibida.
3.  **Banco**: Cruzar el `Net Amount` de la liquidación contra el abono en la cuenta corriente.

## 5. Mapeo al Modelo Canónico

-   **`fact_sales_orders`**: Captura el ingreso bruto.
-   **`fact_payments`**: Captura el flujo de caja neto y las retenciones.
-   **`fact_reconciliation`**: Genera las alertas de discrepancia.

## 6. Conclusión Técnica

Falabella y Ripley requieren un manejo estricto de los **periodos de corte**. A diferencia de Mercado Libre que es casi tiempo real, estos retailers funcionan por "ciclos". El sistema Chile-Sync Conciliador implementará una **"Capa de Periodos"** para asegurar que la conciliación financiera respete los cortes de caja de cada marketplace.
