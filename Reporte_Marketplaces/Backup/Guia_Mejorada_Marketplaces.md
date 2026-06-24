# Guía Definitiva 2.0: Reporte Gerencial 360° de Marketplaces con Power Query y Modelo de Datos

## Introducción

Esta guía representa la evolución del reporte gerencial, diseñada para proporcionar una visión de 360 grados de su operación en **Mercado Libre, Paris y Ripley**. A diferencia del enfoque anterior, que se centraba principalmente en ventas y devoluciones, este nuevo modelo incorpora todas las aristas críticas del negocio: costos logísticos, comisiones detalladas, promociones, cancelaciones y otros cargos operativos.

El objetivo es transformar su reporte de un simple estado de resultados a un completo panel de inteligencia de negocios. Para lograrlo, implementaremos un **modelo de datos relacional (esquema de estrella)** directamente en Power Query, permitiendo un análisis más profundo, preciso y escalable.

## Fase 1: El Nuevo Paradigma - Modelo de Datos Relacional

Abandonamos la idea de una única tabla "plana" y adoptamos un **esquema de estrella**. Este modelo organiza los datos en dos tipos de tablas, lo que optimiza la flexibilidad y el rendimiento del reporte:

- **Tabla de Hechos (Fact Table):** Contiene los eventos de negocio medibles. En nuestro caso, será una tabla llamada **`Fact_Transacciones`** que registrará cada movimiento individual: una venta, un costo de envío, una comisión, una devolución, etc.
- **Tablas de Dimensiones (Dimension Tables):** Describen los atributos de los hechos. Crearemos dimensiones para `Dim_Tiempo`, `Dim_Producto`, `Dim_Marketplace`, y `Dim_Tipo_Transaccion`.

Este enfoque nos permitirá responder preguntas complejas como: *"¿Cuál es la rentabilidad neta de un SKU específico en Ripley, considerando comisiones, costos de envío y devoluciones, durante el último trimestre?"*

## Fase 2: Extracción de Datos Ampliada (ETL 360°)

La clave de este nuevo modelo es extraer **toda** la información disponible. La estructura de carpetas propuesta en la guía anterior sigue siendo válida, pero ahora extraeremos más reportes y los procesaremos de manera diferente.

### 2.1. Mercado Libre: Desglose Total

Para Mercado Libre, no nos limitaremos a la facturación y el poscobro. Es crucial descargar y procesar todos los reportes disponibles en la sección **Facturación > Reportes de facturación**.

**Nuevas Consultas en Power Query:**

1.  **`ML_Facturacion_RAW`**: Del reporte "Detalle de facturación", extraeremos:
    - **Cargos por Venta**: Comisión, costo fijo, cuotas.
    - **Cargos por Envío**: Costos de Mercado Envíos.
    - **Cargos por Publicidad**: Costos de Mercado Ads.
    - **Bonificaciones y anulaciones**.

2.  **`ML_Poscobro_RAW`**: Del reporte de "Dinero retirado", para identificar devoluciones (`refund`).

3.  **`ML_Ventas_RAW`**: Del reporte de "Ventas", para obtener el detalle de cada operación.

### 2.2. Paris Marketplace: Integración Completa

Paris Marketplace, a través de su Seller Center, ofrece múltiples reportes. Debemos ir más allá del reporte básico de transacciones.

**Nuevas Consultas en Power Query:**

1.  **`Paris_Finanzas_RAW`**: Desde **Finanzas > Pagos y Facturas**, descargando el reporte de transacciones. Este será nuestro punto de partida.
2.  **`Paris_Logistica_RAW`**: Desde la sección **Reportes > Logística**, para obtener información sobre los costos y estados de envío.
3.  **`Paris_Devoluciones_RAW`**: La gestión de devoluciones se realiza en la sección de **Post-Venta**. Es fundamental exportar esta información para cruzarla con las ventas.

### 2.3. Ripley Marketplace: Visión Unificada

Ripley proporciona información a través de su plataforma Mirakl. Necesitamos consolidar los distintos cobros para tener una visión clara de la rentabilidad.

**Nuevas Consultas en Power Query:**

1.  **`Ripley_Ventas_RAW`**: Corresponde al reporte de pedidos, con el detalle de las ventas.
2.  **`Ripley_Ajustes_RAW`**: Reporte de historial financiero, que incluye devoluciones, cancelaciones y otros ajustes.
3.  **`Ripley_Comisiones_RAW`**: Descargar el detalle de comisiones vigentes y el costo fijo operacional para aplicarlos correctamente.
4.  **`Ripley_Costos_Logisticos_RAW`**: Documentación sobre los costos de envío según modalidad (Flota Propia, Chilexpress, etc.). Estos costos a menudo deben ser modelados o ingresados manualmente si no están en un reporte descargable.

## Fase 3: Construcción del Modelo de Datos en Power Query

Esta es la fase más crítica. En lugar de anexar todo en una tabla, transformaremos cada consulta RAW en un formato estándar y luego las uniremos en nuestra tabla de hechos.

### 3.1. Creación de las Tablas de Dimensiones

1.  **`Dim_Producto`**: Cree una consulta a partir de las columnas de SKU y descripción de todas las tablas de ventas. Elimine duplicados. Puede enriquecerla con datos de su maestro de productos (categoría, COGS, etc.).
2.  **`Dim_Marketplace`**: Cree una tabla manualmente o desde una consulta que contenga los IDs y nombres de los marketplaces (1-Mercado Libre, 2-Paris, 3-Ripley).
3.  **`Dim_Tiempo`**: Cree una tabla de calendario en Power Query para poder analizar por día, mes, trimestre, año, etc.
4.  **`Dim_Tipo_Transaccion`**: Cree una tabla que estandarice los tipos de movimiento: Venta, Comisión, Costo Envío, Devolución, Publicidad, Ajuste, etc.

### 3.2. Estandarización de Consultas y Creación de la Tabla de Hechos

Para cada consulta RAW (ej. `ML_Facturacion_RAW`), el objetivo es transformarla para que tenga un formato estándar con las siguientes columnas:

- `ID_Transaccion_Original`
- `Fecha`
- `SKU`
- `ID_Marketplace`
- `ID_Tipo_Transaccion`
- `Monto` (positivo para ingresos, negativo para costos/egresos)

**Ejemplo de Transformación para `ML_Facturacion_RAW`:**

- Duplique la consulta `ML_Facturacion_RAW` varias veces, una por cada tipo de cargo que quiera registrar (venta, comisión, envío).
- En la consulta de "comisiones", filtre por los detalles correspondientes, seleccione las columnas `ID_Transaccion`, `Fecha`, `SKU`, y `Valor del cargo`. Añada una columna para `ID_Marketplace` (1) y `ID_Tipo_Transaccion` (ej. 2 para Comisión). Renombre `Valor del cargo` a `Monto` y asegúrese de que sea negativo.
- Repita este proceso para cada tipo de transacción de cada marketplace.

### 3.3. Anexar a la Tabla de Hechos

Una vez que todas las consultas de transacciones individuales estén estandarizadas, anéxelas en una única tabla: **`Fact_Transacciones`**.

- Vaya a **Inicio > Combinar > Anexar consultas para crear una nueva**.
- Seleccione todas las tablas de transacciones estandarizadas.

## Fase 4: Carga del Modelo y Creación del Dashboard Avanzado

### 4.1. Cargar el Modelo de Datos

- En Power Query, para cada una de las tablas de **Dimensiones** y la tabla de **Hechos**, seleccione **Cerrar y cargar en...**
- Elija **Solo crear conexión** y marque la casilla **Agregar estos datos al Modelo de datos**.

### 4.2. Relaciones y Jerarquías

- Vaya a la pestaña **Power Pivot > Administrar**.
- En la **Vista de diagrama**, arrastre los campos clave para crear las relaciones entre la tabla de hechos y las dimensiones (ej. `Fact_Transacciones[SKU]` con `Dim_Producto[SKU]`).

### 4.3. KPIs y Dashboard Gerencial 360°

Con el modelo de datos relacional, ahora puede crear métricas (medidas DAX) y visualizaciones mucho más potentes:

**Nuevas Medidas DAX:**

- **Venta Neta Total**: `SUM(Fact_Transacciones[Monto])`
- **Tasa de Devolución**: `CALCULATE(SUM(Fact_Transacciones[Monto]), Dim_Tipo_Transaccion[Tipo] = "Devolución") / CALCULATE(SUM(Fact_Transacciones[Monto]), Dim_Tipo_Transaccion[Tipo] = "Venta")`
- **Costo Total Marketplace**: `CALCULATE(SUM(Fact_Transacciones[Monto]), Dim_Tipo_Transaccion[Tipo] IN {"Comisión", "Costo Envío", "Publicidad"})`
- **Margen de Contribución**: `[Venta Neta Total] - [Costo Total Marketplace] - (Costo del Producto)`

**Visualizaciones Recomendadas:**

- **Gráfico de cascada (Waterfall Chart)** para mostrar cómo se descompone el ingreso bruto (GMV) hasta llegar a la rentabilidad neta, mostrando cada costo (comisión, envío, etc.) como una barra negativa.
- **Matriz de Rentabilidad** con Marketplace en las filas y `Venta Neta`, `Costo Total Marketplace` y `Margen de Contribución` como valores.
- **Gráfico de Pareto** para identificar los productos que generan el 80% de las devoluciones.
- **Mapa de calor** para visualizar la rentabilidad por categoría de producto y marketplace.

## Conclusión

Este nuevo enfoque requiere una configuración inicial más detallada, pero los beneficios son inmensos. Pasará de un reporte estático a un ecosistema de análisis dinámico que le permitirá tomar decisiones estratégicas basadas en una comprensión total de la rentabilidad de su operación en marketplaces. La automatización de Power Query asegura que, una vez configurado, el modelo se actualice con un solo clic, dándole más tiempo para el análisis y menos para la preparación de datos.
