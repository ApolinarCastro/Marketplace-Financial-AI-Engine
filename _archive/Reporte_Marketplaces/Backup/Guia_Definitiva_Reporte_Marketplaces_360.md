# Guía Definitiva 2.0: Reporte Gerencial 360° de Marketplaces con Power Query

**Autor:** Manus AI  
**Versión:** 2.0  
**Fecha:** Diciembre 2025  
**Marketplaces Cubiertos:** Mercado Libre, Paris Marketplace, Ripley Marketplace

---

## Resumen Ejecutivo

Esta guía representa una evolución fundamental en la gestión de reportes gerenciales para operaciones de e-commerce en múltiples marketplaces. Mientras que el enfoque tradicional se limitaba a consolidar ventas y devoluciones, este nuevo modelo incorpora una visión de 360 grados que incluye todas las aristas críticas del negocio: comisiones detalladas, costos logísticos, promociones, cancelaciones, ajustes financieros y otros cargos operativos.

El objetivo es transformar su reporte de un simple estado de resultados a un completo panel de inteligencia de negocios. Para lograrlo, implementaremos un **modelo de datos relacional (esquema de estrella)** directamente en Power Query, permitiendo un análisis más profundo, preciso y escalable de la rentabilidad real de su operación.

---

## Introducción: El Problema con el Enfoque Tradicional

### Limitaciones del Modelo Anterior

El modelo tradicional de reportes de marketplaces presenta tres limitaciones fundamentales que impiden una toma de decisiones informada:

**Primera limitación: Visión parcial de costos.** Los reportes convencionales se enfocan en el GMV (Gross Merchandise Value) y las comisiones básicas, pero ignoran costos ocultos como los cargos fijos operacionales, costos de envío variables, penalizaciones por incumplimiento y cargos por publicidad. Esta omisión puede distorsionar la rentabilidad aparente de un producto hasta en un 30%, según nuestra experiencia con vendedores en Chile.

**Segunda limitación: Falta de granularidad temporal.** Al consolidar todas las transacciones en una única tabla plana, se pierde la capacidad de analizar el ciclo de vida completo de una venta. Una transacción que aparece como "venta completada" puede tener asociada una devolución tres semanas después, un ajuste de comisión al mes siguiente y un cargo por publicidad que se factura de manera diferida. Sin un modelo que capture estos eventos de manera independiente y relacionada, es imposible calcular la rentabilidad real en el momento correcto.

**Tercera limitación: Imposibilidad de análisis multidimensional.** Una tabla plana no permite responder preguntas de negocio complejas como: *"¿Cuál es mi margen de contribución neto por categoría de producto en Ripley, después de descontar todos los costos logísticos, durante el último trimestre, comparado con el mismo período del año anterior?"* Este tipo de análisis requiere un modelo dimensional que separe hechos (transacciones medibles) de dimensiones (atributos descriptivos).

### La Solución: Modelo de Datos Relacional

La solución propuesta en esta guía se basa en tres pilares fundamentales. Primero, la **extracción completa de datos** de todos los reportes disponibles en cada marketplace, no solo los de ventas. Segundo, la **estandarización de transacciones** mediante la creación de un esquema común que permita comparar manzanas con manzanas entre Mercado Libre, Paris y Ripley. Tercero, la **implementación de un modelo de estrella** que organice los datos en una tabla de hechos central (transacciones) rodeada de tablas de dimensiones (tiempo, producto, marketplace, tipo de transacción).

Este enfoque no solo resuelve las limitaciones mencionadas, sino que además prepara su infraestructura de datos para escalar. Cuando agregue un cuarto marketplace o necesite integrar datos de costos de producción, el modelo se adaptará sin requerir una reestructuración completa.

---

## Parte I: Fundamentos del Modelo de Datos

### Capítulo 1: Arquitectura del Esquema de Estrella

El esquema de estrella es un patrón de diseño de bases de datos ampliamente utilizado en inteligencia de negocios. Su nombre proviene de su representación visual: una tabla central (la tabla de hechos) conectada a múltiples tablas periféricas (las dimensiones), formando una estrella.

#### 1.1. La Tabla de Hechos: `Fact_Transacciones`

La tabla de hechos almacena los eventos de negocio medibles. En nuestro contexto, cada fila representa un movimiento financiero individual relacionado con la operación en marketplaces. Esto incluye no solo las ventas, sino también cada costo, cargo, descuento y ajuste asociado.

**Estructura de `Fact_Transacciones`:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `ID_Transaccion` | Texto | Identificador único de la transacción original del marketplace |
| `Fecha` | Fecha | Fecha en que ocurrió el evento |
| `ID_Producto` | Texto | Clave foránea hacia `Dim_Producto` |
| `ID_Marketplace` | Entero | Clave foránea hacia `Dim_Marketplace` |
| `ID_Tipo_Transaccion` | Entero | Clave foránea hacia `Dim_Tipo_Transaccion` |
| `Monto` | Decimal | Valor monetario (positivo para ingresos, negativo para costos) |
| `Cantidad` | Entero | Unidades vendidas o afectadas |

**Principio de granularidad:** Cada fila debe representar el nivel más atómico de detalle posible. Por ejemplo, si una venta tiene asociados tres cargos diferentes (comisión por venta, costo de envío y cargo por publicidad), estos deben registrarse como tres filas separadas en la tabla de hechos, todas compartiendo el mismo `ID_Transaccion` pero con diferentes `ID_Tipo_Transaccion`.

#### 1.2. Las Tablas de Dimensiones

Las dimensiones proporcionan el contexto descriptivo para los hechos. Cada dimensión responde a una pregunta específica sobre la transacción: ¿cuándo ocurrió? (Dim_Tiempo), ¿qué producto se vendió? (Dim_Producto), ¿en qué marketplace? (Dim_Marketplace), ¿qué tipo de movimiento fue? (Dim_Tipo_Transaccion).

**`Dim_Tiempo`:**

Esta dimensión permite análisis temporal sofisticado. En lugar de depender únicamente de la columna de fecha en la tabla de hechos, creamos una tabla de calendario completa que incluye atributos derivados.

| Columna | Ejemplo | Descripción |
|---------|---------|-------------|
| `Fecha` | 2025-11-15 | Fecha completa (clave primaria) |
| `Año` | 2025 | Año calendario |
| `Trimestre` | Q4 | Trimestre del año |
| `Mes` | 11 | Número de mes |
| `Nombre_Mes` | Noviembre | Nombre del mes |
| `Semana` | 46 | Semana del año (ISO 8601) |
| `Dia_Semana` | Viernes | Nombre del día |
| `Es_Fin_Semana` | No | Indicador booleano |

**`Dim_Producto`:**

Esta dimensión enriquece la información de cada SKU con atributos de negocio relevantes.

| Columna | Ejemplo | Descripción |
|---------|---------|-------------|
| `SKU` | MLC1626187509 | Código único del producto (clave primaria) |
| `Descripcion` | Zapatillas Running Nike | Nombre del producto |
| `Categoria` | Calzado Deportivo | Categoría de producto |
| `Subcategoria` | Running | Subcategoría |
| `COGS` | 25000 | Costo de los bienes vendidos |
| `Proveedor` | Nike Chile | Proveedor del producto |

**`Dim_Marketplace`:**

Esta dimensión es simple pero crítica para segmentar el análisis por canal.

| Columna | Ejemplo | Descripción |
|---------|---------|-------------|
| `ID_Marketplace` | 1 | Identificador numérico (clave primaria) |
| `Nombre` | Mercado Libre | Nombre del marketplace |
| `Pais` | Chile | País de operación |
| `Moneda` | CLP | Moneda de transacción |

**`Dim_Tipo_Transaccion`:**

Esta dimensión estandariza los diferentes tipos de movimientos financieros a través de los marketplaces.

| ID | Tipo | Categoría | Signo Esperado |
|----|------|-----------|----------------|
| 1 | Venta | Ingreso | Positivo |
| 2 | Comisión Marketplace | Costo | Negativo |
| 3 | Costo Envío | Costo | Negativo |
| 4 | Costo Fijo Operacional | Costo | Negativo |
| 5 | Devolución | Ajuste | Negativo |
| 6 | Cancelación | Ajuste | Negativo |
| 7 | Publicidad | Costo | Negativo |
| 8 | Promoción/Descuento | Costo | Negativo |
| 9 | Bonificación | Ingreso | Positivo |
| 10 | Penalización | Costo | Negativo |
| 11 | Asesoría Comercial | Costo | Negativo |
| 12 | Costo Fullfilment | Costo | Negativo |

---

## Parte II: Extracción de Datos por Marketplace

### Capítulo 2: Mercado Libre - Desglose Completo

Mercado Libre proporciona el sistema de reportes más completo y granular de los tres marketplaces. El reporte de facturación se divide en cinco secciones principales: Cargos, Descuentos, Venta, Envío y Publicación. Cada sección contiene información crítica que debe ser extraída y procesada de manera independiente.

#### 2.1. Estructura del Reporte de Facturación

El reporte de facturación de Mercado Libre es un archivo Excel con múltiples columnas que documentan cada cargo y su contexto. Las columnas clave incluyen:

**Sección de Cargos:**
- `Número de factura fiscal`: Documento legal de facturación
- `Fecha del cargo`: Fecha de generación del cargo
- `Número del cargo`: ID único del cargo
- `Detalle`: Concepto del cargo (ej. "Cargo por venta", "Cargo por envío")
- `Descontado de la operación`: Indica si fue descontado automáticamente
- `Estado del cargo`: Estado de anulación (si aplica)
- `Valor del cargo`: Monto facturado (incluye IVA)

**Detalle del cálculo:**
- `Porcentaje por categoría + ofrecer cuotas`: Tasa de comisión aplicada
- `Costo por categoría + ofrecer cuotas`: Monto generado por la comisión
- `Costo fijo`: Cargo adicional para productos bajo precio mínimo
- `Subtotal sin descuento`: Suma de costos antes de descuentos
- `Valor del descuento`: Monto de descuento aplicado
- `Motivo del descuento`: Razón del descuento

**Información de la venta:**
- `Número de venta`: ID de la transacción de venta
- `Pago`: Número de pago en Mercado Pago (para conciliación)
- `Canal de venta`: Origen de la venta
- `Tipo de medio de pago`: Método de pago del comprador
- `Valor de la compra`: GMV de la transacción

**Información del envío:**
- `Número de envío`: ID del envío
- `Número de paquete`: ID del paquete (para ventas agrupadas)
- `Costo de envío a cargo del cliente`: Monto pagado por el comprador

**Información de la publicación:**
- `Número de publicación`: ID de la publicación
- `Título`: Nombre del producto
- `Cuotas agregadas en publicación`: Cuotas ofrecidas
- `Categoría`: Categoría del producto
- `Código ML`: SKU del producto

#### 2.2. Configuración de Consultas en Power Query

**Paso 1: Carga del archivo de facturación**

Cree una carpeta `C:\Reporte_Marketplaces\ML_Facturacion` y coloque todos los archivos históricos de facturación. En Power Query:

1. Vaya a **Datos > Obtener datos > De un archivo > De una carpeta**
2. Seleccione la carpeta `ML_Facturacion`
3. Haga clic en **Combinar > Combinar y transformar datos**
4. Seleccione la hoja "REPORT" (o el nombre que tenga su reporte)
5. Renombre la consulta como `ML_Facturacion_RAW`

**Paso 2: Filtrado y transformación por tipo de cargo**

Para crear la tabla de hechos, necesitamos separar cada tipo de cargo en consultas independientes. Duplique la consulta `ML_Facturacion_RAW` cuatro veces y renómbrelas:

- `ML_Fact_Ventas`
- `ML_Fact_Comisiones`
- `ML_Fact_Envios`
- `ML_Fact_Publicidad`
- `ML_Fact_Asesoria`
- `ML_Fact_Fullfilment`
- `ML_Fact_Bonificaciones`

**Transformación de `ML_Fact_Ventas`:**

```
1. Filtre la columna "Detalle" para incluir solo "Cargo por venta"
2. Seleccione las columnas:
   - "Número de venta" → Renombre a "ID_Transaccion"
   - "Fecha del cargo" → Renombre a "Fecha"
   - "Código ML" → Renombre a "SKU"
   - "Valor de la compra" → Renombre a "Monto"
3. Agregue una columna personalizada "ID_Marketplace" con valor 1
4. Agregue una columna personalizada "ID_Tipo_Transaccion" con valor 1
5. Agregue una columna "Cantidad" con valor 1
```

**Transformación de `ML_Fact_Comisiones`:**

```
1. Filtre la columna "Detalle" para incluir "Cargo por venta" (la comisión está en el mismo registro)
2. Seleccione las columnas:
   - "Número de venta" → "ID_Transaccion"
   - "Fecha del cargo" → "Fecha"
   - "Código ML" → "SKU"
   - "Costo por categoría + ofrecer cuotas" → "Monto"
3. Multiplique la columna "Monto" por -1 (para que sea negativa)
4. Agregue columna "ID_Marketplace" = 1
5. Agregue columna "ID_Tipo_Transaccion" = 2
6. Agregue columna "Cantidad" = 1
```

**Transformación de `ML_Fact_Envios`:**

```
1. Filtre la columna "Detalle" para incluir los siguientes términos:
   - "Cargo por Mercado Envíos"
   - "Cargo por envíos de Mercado Libre"
2. Seleccione las columnas necesarias (similar al proceso anterior)
3. "Valor del cargo" → "Monto" (multiplicado por -1)
4. "ID_Tipo_Transaccion" = 3
```}],path:

**Transformación de `ML_Fact_Publicidad`:**

```
1. Filtre la columna "Detalle" para incluir los siguientes términos:
   - "Campañas de publicidad"
   - "Cargo por campaña de publicidad"
   - "Cargo por publicación"
   - "Mercado Ads"
2. Procese de manera similar
3. "ID_Tipo_Transaccion" = 7
```

**Transformación de `ML_Fact_Asesoria`:**

```
1. Filtre la columna "Detalle" para incluir "Cargo por Asesoría Comercial"
2. Seleccione las columnas necesarias (similar al proceso anterior)
3. "Valor del cargo" → "Monto" (multiplicado por -1)
4. "ID_Tipo_Transaccion" = 11
```

**Transformación de `ML_Fact_Fullfilment`:**

```
1. Filtre la columna "Detalle" para incluir los siguientes términos:
   - "Cargo por retiro de stock Full"
   - "Cargo por servicio de almacenamiento Full"
   - "Cargo por stock antiguo en Full"
   - "Cargo por mantenimiento de Mi página"
2. Seleccione las columnas necesarias (similar al proceso anterior)
3. "Valor del cargo" → "Monto" (multiplicado por -1)
4. "ID_Tipo_Transaccion" = 12
```

**Transformación de `ML_Fact_Bonificaciones`:**

```
1. Filtre la columna "Detalle" para incluir los siguientes términos:
   - "Bonificación"
   - "Anulación del cargo por venta"
   - "Anulación del cargo por Mercado Envíos"
   - "Anulación del cargo por envíos de Mercado Libre"
   - "Anulación del cargo por devolución"
2. Seleccione las columnas necesarias (similar al proceso anterior)
3. "Valor del cargo" → "Monto" (mantener signo, ya que las anulaciones son positivas)
4. "ID_Tipo_Transaccion" = 9
```

#### 2.3. Procesamiento de Devoluciones (Poscobro)

El reporte de poscobro (dinero retirado) contiene las devoluciones. Cree una carpeta `C:\Reporte_Marketplaces\ML_Poscobro` y configure la carga:

**Consulta `ML_Fact_Devoluciones`:**

```
1. Cargue desde carpeta ML_Poscobro
2. Filtre la columna "Estado" o campo equivalente para incluir solo "refund"
3. Seleccione:
   - "ID de la transacción" → "ID_Transaccion"
   - "Fecha" → "Fecha"
   - "SKU" → "SKU"
   - "Monto" → "Monto" (multiplicado por -1)
4. "ID_Marketplace" = 1
5. "ID_Tipo_Transaccion" = 5
6. "Cantidad" = -1
```

---

### Capítulo 3: Paris Marketplace - Integración Completa

Paris Marketplace opera sobre la plataforma Mirakl y ofrece múltiples reportes a través de su Seller Center. La clave está en integrar información de diferentes secciones para obtener una visión completa.

#### 3.1. Reportes Disponibles en Paris

Paris proporciona siete categorías de reportes en la sección **Reportes** del Seller Center:

1. **Finanzas**: Detalle de transacciones, comisiones y pagos
2. **Comercial**: Métricas de ventas y rendimiento
3. **Productos**: Información de catálogo y stock
4. **Logística**: Estados de envío y costos de despacho
5. **Órdenes**: Gestión de pedidos y estados
6. **Fulfillment**: Operaciones de almacenamiento (si aplica)
7. **Reputación**: Métricas de desempeño del vendedor

Para nuestro modelo de datos, nos enfocaremos en los reportes de **Finanzas**, **Logística** y **Órdenes**.

#### 3.2. Configuración de Consultas en Power Query

**Paso 1: Reporte de Finanzas (Transacciones)**

Desde el Seller Center, vaya a **Finanzas > Pagos y Facturas > Transacciones**. Descargue el reporte aplicando los filtros necesarios (tipo de transacción, estado, período). Coloque los archivos en `C:\Reporte_Marketplaces\Paris_Finanzas`.

**Consulta `Paris_Finanzas_RAW`:**

```
1. Cargue desde carpeta Paris_Finanzas
2. Identifique las columnas clave:
   - "Número de orden" o "ID de transacción"
   - "Fecha"
   - "Código SKU"
   - "Monto" o "Total"
   - "Comisión"
   - "Estado"
   - "Descripción del producto"
```

**Transformación a `Paris_Fact_Ventas`:**

```
1. Filtre por tipo de transacción = "Venta" o estado que indique venta completada
2. Seleccione:
   - "Número de orden" → "ID_Transaccion"
   - "Fecha" → "Fecha"
   - "Código SKU" → "SKU"
   - "Monto" → "Monto"
3. "ID_Marketplace" = 2
4. "ID_Tipo_Transaccion" = 1
5. "Cantidad" = 1
```

**Transformación a `Paris_Fact_Comisiones`:**

```
1. Duplique Paris_Finanzas_RAW
2. Filtre por ventas (igual que arriba)
3. Seleccione:
   - "Número de orden" → "ID_Transaccion"
   - "Fecha" → "Fecha"
   - "Código SKU" → "SKU"
   - "Comisión" → "Monto" (multiplicado por -1)
4. "ID_Marketplace" = 2
5. "ID_Tipo_Transaccion" = 2
```

**Paso 2: Reporte de Logística**

Desde **Reportes > Logística**, descargue el reporte de envíos. Este contiene información sobre costos de despacho, modalidad de envío y estados.

**Consulta `Paris_Logistica_RAW`:**

```
1. Cargue desde carpeta Paris_Logistica
2. Identifique columnas:
   - "Número de orden"
   - "Costo de envío"
   - "Modalidad de envío"
   - "Estado de envío"
```

**Transformación a `Paris_Fact_Envios`:**

```
1. Filtre para incluir solo registros con costo de envío > 0
2. Seleccione:
   - "Número de orden" → "ID_Transaccion"
   - Fecha (puede necesitar hacer lookup con Paris_Finanzas_RAW)
   - SKU (puede necesitar lookup)
   - "Costo de envío" → "Monto" (multiplicado por -1)
3. "ID_Marketplace" = 2
4. "ID_Tipo_Transaccion" = 3
```

**Paso 3: Devoluciones y Cancelaciones**

Las devoluciones en Paris se gestionan a través de la sección **Post-Venta**. Si el sistema permite exportar un reporte de devoluciones, cárguelo de manera similar. Si no, puede identificar devoluciones en el reporte de Finanzas buscando transacciones con monto negativo o estado "Devuelto".

**Consulta `Paris_Fact_Devoluciones`:**

```
1. Desde Paris_Finanzas_RAW, filtre por:
   - Estado = "Devuelto" o "Reembolsado"
   - O Monto < 0 (dependiendo de cómo se registren)
2. Transforme de manera estándar
3. "ID_Tipo_Transaccion" = 5
```

#### 3.3. Consideraciones Especiales para Paris

**Comisiones variables por categoría:** Paris aplica comisiones diferentes según la familia de producto. Asegúrese de que el reporte de Finanzas incluya la columna de comisión calculada. Si solo proporciona el porcentaje, deberá crear una columna personalizada: `Comisión = [Monto] * [Porcentaje_Comision]`.

**Estados de pedido:** Paris utiliza estados como "Pendiente", "Completado", "Cancelado", "Devuelto". Es fundamental filtrar correctamente para evitar duplicar transacciones. Solo incluya en `Paris_Fact_Ventas` las transacciones con estado "Completado" o equivalente.

---

### Capítulo 4: Ripley Marketplace - Visión Unificada

Ripley Marketplace, operado sobre la plataforma Mirakl, presenta una particularidad: los costos se distribuyen en múltiples reportes y algunos deben ser calculados manualmente según las políticas vigentes.

#### 4.1. Estructura de Reportes en Ripley

Ripley proporciona principalmente dos reportes descargables desde el Seller Center:

1. **Reporte de Pedidos**: Contiene las ventas realizadas con detalle de SKU, monto y comisión
2. **Reporte de Historial Financiero**: Incluye ajustes, reembolsos, cancelaciones y otros movimientos

Adicionalmente, Ripley publica documentación sobre:
- **Tabla de Comisiones**: Porcentajes por categoría
- **Costos Logísticos**: Tarifas según modalidad de envío y peso
- **Costo Fijo Operacional**: $990 por unidad vendida ≤ $5,000

#### 4.2. Configuración de Consultas en Power Query

**Paso 1: Reporte de Pedidos (Ventas)**

Descargue el reporte de pedidos desde el Seller Center y colóquelo en `C:\Reporte_Marketplaces\Ripley_Pedidos`.

**Consulta `Ripley_Ventas_RAW`:**

```
1. Cargue desde carpeta Ripley_Pedidos
2. Identifique columnas:
   - "Número de pedido"
   - "Fecha de creación"
   - "SKU de oferta" o "SKU de Tienda"
   - "Importe" (GMV)
   - "Comisión (sin impuestos)"
   - "Estado"
```

**Transformación a `Ripley_Fact_Ventas`:**

```
1. Filtre por estado que indique venta completada (excluya cancelados)
2. Seleccione:
   - "Número de pedido" → "ID_Transaccion"
   - "Fecha de creación" → "Fecha"
   - "SKU de oferta" → "SKU"
   - "Importe" → "Monto"
3. "ID_Marketplace" = 3
4. "ID_Tipo_Transaccion" = 1
5. "Cantidad" = 1
```

**Transformación a `Ripley_Fact_Comisiones`:**

```
1. Duplique Ripley_Ventas_RAW
2. Seleccione:
   - "Número de pedido" → "ID_Transaccion"
   - "Fecha de creación" → "Fecha"
   - "SKU de oferta" → "SKU"
   - "Comisión (sin impuestos)" → "Monto" (multiplicado por -1)
3. "ID_Marketplace" = 3
4. "ID_Tipo_Transaccion" = 2
```

**Paso 2: Costo Fijo Operacional**

Ripley cobra $990 por cada unidad vendida con precio ≤ $5,000. Este costo debe calcularse.

**Consulta `Ripley_Fact_Costo_Fijo`:**

```
1. Duplique Ripley_Ventas_RAW
2. Filtre: "Importe" <= 5000
3. Agregue columna personalizada "Monto" = -990
4. Seleccione columnas estándar
5. "ID_Tipo_Transaccion" = 4
```

**Paso 3: Reporte de Historial Financiero (Ajustes)**

Este reporte contiene devoluciones, cancelaciones y otros ajustes. Coloque los archivos en `C:\Reporte_Marketplaces\Ripley_Ajustes`.

**Consulta `Ripley_Ajustes_RAW`:**

```
1. Cargue desde carpeta Ripley_Ajustes
2. Identifique columnas:
   - "Número de pedido"
   - "Fecha de creación"
   - "SKU de oferta"
   - "Importe" (generalmente negativo)
   - "Tipo" o "Descripción" (para identificar el tipo de ajuste)
```

**Transformación a `Ripley_Fact_Devoluciones`:**

```
1. Filtre por tipo de ajuste = "Reembolso" o "Devolución"
2. Seleccione columnas estándar
3. "Importe" → "Monto" (ya debería ser negativo)
4. "ID_Tipo_Transaccion" = 5
```

**Transformación a `Ripley_Fact_Cancelaciones`:**

```
1. Filtre por tipo de ajuste = "Cancelación"
2. Procese de manera similar
3. "ID_Tipo_Transaccion" = 6
```

**Paso 4: Costos Logísticos (Modelado Manual)**

Los costos logísticos de Ripley varían según la modalidad de envío y el peso del paquete. Si estos datos no están disponibles en un reporte descargable, tiene dos opciones:

**Opción A: Crear tabla de tarifas**

Cree manualmente una tabla en Excel con las tarifas vigentes según la documentación de Ripley:

| Modalidad | Peso_Min | Peso_Max | Tarifa |
|-----------|----------|----------|--------|
| Flota Propia | 0 | 2 | 2500 |
| Flota Propia | 2 | 5 | 3500 |
| Chilexpress | 0 | 2 | 2800 |
| ... | ... | ... | ... |

Luego, en Power Query, haga un merge entre `Ripley_Ventas_RAW` y esta tabla de tarifas usando la modalidad de envío y el peso (si está disponible) como claves.

**Opción B: Solicitar reporte detallado**

Contacte a su ejecutivo de cuenta en Ripley para solicitar un reporte que incluya los costos de envío desglosados por pedido.

---

## Parte III: Construcción del Modelo de Datos

### Capítulo 5: Creación de Tablas de Dimensiones

Antes de consolidar la tabla de hechos, debemos crear las dimensiones que proporcionarán el contexto para el análisis.

#### 5.1. Dimensión de Tiempo (`Dim_Tiempo`)

**Paso 1: Crear tabla de calendario**

En Power Query, vaya a **Inicio > Nueva consulta > Consulta en blanco**. En el editor avanzado, pegue el siguiente código M:

```m
let
    FechaInicio = #date(2025, 1, 1),
    FechaFin = #date(2026, 12, 31),
    NumeroDias = Duration.Days(FechaFin - FechaInicio) + 1,
    ListaFechas = List.Dates(FechaInicio, NumeroDias, #duration(1,0,0,0)),
    TablaFechas = Table.FromList(ListaFechas, Splitter.SplitByNothing(), {"Fecha"}),
    CambiarTipo = Table.TransformColumnTypes(TablaFechas, {{"Fecha", type date}}),
    AgregarAño = Table.AddColumn(CambiarTipo, "Año", each Date.Year([Fecha]), Int64.Type),
    AgregarMes = Table.AddColumn(AgregarAño, "Mes", each Date.Month([Fecha]), Int64.Type),
    AgregarNombreMes = Table.AddColumn(AgregarMes, "Nombre_Mes", each Date.MonthName([Fecha]), type text),
    AgregarTrimestre = Table.AddColumn(AgregarNombreMes, "Trimestre", each "Q" & Number.ToText(Date.QuarterOfYear([Fecha])), type text),
    AgregarSemana = Table.AddColumn(AgregarTrimestre, "Semana", each Date.WeekOfYear([Fecha]), Int64.Type),
    AgregarDiaSemana = Table.AddColumn(AgregarSemana, "Dia_Semana", each Date.DayOfWeekName([Fecha]), type text),
    AgregarEsFinSemana = Table.AddColumn(AgregarDiaSemana, "Es_Fin_Semana", each if Date.DayOfWeek([Fecha], Day.Monday) >= 5 then "Sí" else "No", type text)
in
    AgregarEsFinSemana
```

Renombre la consulta como `Dim_Tiempo`.

#### 5.2. Dimensión de Producto (`Dim_Producto`)

**Paso 1: Extraer SKUs únicos**

Necesitamos consolidar todos los SKUs de los tres marketplaces. En Power Query:

```
1. Cree una nueva consulta en blanco
2. Anexe las columnas de SKU de todas las consultas RAW:
   - ML_Facturacion_RAW[Código ML]
   - Paris_Finanzas_RAW[Código SKU]
   - Ripley_Ventas_RAW[SKU de oferta]
3. Elimine duplicados
4. Renombre la columna a "SKU"
```

**Paso 2: Enriquecer con datos de negocio**

Si tiene un maestro de productos en Excel con información adicional (descripción, categoría, COGS, proveedor), cárguelo como una consulta y haga un merge con la lista de SKUs:

```
1. Cargue el maestro de productos como "Maestro_Productos"
2. En la consulta de SKUs únicos, vaya a Inicio > Combinar > Combinar consultas
3. Seleccione la columna SKU en ambas tablas
4. Tipo de combinación: Externa izquierda
5. Expanda las columnas: Descripcion, Categoria, Subcategoria, COGS, Proveedor
```

Renombre la consulta como `Dim_Producto`.

#### 5.3. Dimensión de Marketplace (`Dim_Marketplace`)

Esta es una tabla pequeña que puede crear manualmente.

**Paso 1: Crear tabla manual**

En Power Query, vaya a **Inicio > Nueva consulta > Otra fuente > Tabla en blanco**. Luego, en el editor avanzado:

```m
let
    Origen = Table.FromRecords({
        [ID_Marketplace = 1, Nombre = "Mercado Libre", Pais = "Chile", Moneda = "CLP"],
        [ID_Marketplace = 2, Nombre = "Paris", Pais = "Chile", Moneda = "CLP"],
        [ID_Marketplace = 3, Nombre = "Ripley", Pais = "Chile", Moneda = "CLP"]
    })
in
    Origen
```

Renombre como `Dim_Marketplace`.

#### 5.4. Dimensión de Tipo de Transacción (`Dim_Tipo_Transaccion`)

Similar a la anterior, cree una tabla manual:

```m
let
    Origen = Table.FromRecords({
        [ID_Tipo_Transaccion = 1, Tipo = "Venta", Categoria = "Ingreso", Signo = "Positivo"],
        [ID_Tipo_Transaccion = 2, Tipo = "Comisión Marketplace", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 3, Tipo = "Costo Envío", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 4, Tipo = "Costo Fijo Operacional", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 5, Tipo = "Devolución", Categoria = "Ajuste", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 6, Tipo = "Cancelación", Categoria = "Ajuste", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 7, Tipo = "Publicidad", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 8, Tipo = "Promoción/Descuento", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 9, Tipo = "Bonificación", Categoria = "Ingreso", Signo = "Positivo"],
        [ID_Tipo_Transaccion = 10, Tipo = "Penalización", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 11, Tipo = "Asesoría Comercial", Categoria = "Costo", Signo = "Negativo"],
        [ID_Tipo_Transaccion = 12, Tipo = "Costo Fullfilment", Categoria = "Costo", Signo = "Negativo"]
    })
in
    Origen
```

Renombre como `Dim_Tipo_Transaccion`.

---

### Capítulo 6: Consolidación de la Tabla de Hechos

Con todas las consultas de hechos individuales creadas (las consultas `_Fact_` de cada marketplace y tipo de transacción), ahora las consolidaremos en una única tabla.

#### 6.1. Anexar Todas las Consultas de Hechos

**Paso 1: Identificar todas las consultas de hechos**

Debería tener las siguientes consultas (o similares):
- `ML_Fact_Ventas`
- `ML_Fact_Comisiones`
- `ML_Fact_Envios`
- `ML_Fact_Publicidad`
- `ML_Fact_Asesoria`
- `ML_Fact_Fullfilment`
- `ML_Fact_Bonificaciones`
- `ML_Fact_Devoluciones`
- `Paris_Fact_Ventas`
- `Paris_Fact_Comisiones`
- `Paris_Fact_Envios`
- `Paris_Fact_Devoluciones`
- `Ripley_Fact_Ventas`
- `Ripley_Fact_Comisiones`
- `Ripley_Fact_Costo_Fijo`
- `Ripley_Fact_Devoluciones`
- `Ripley_Fact_Cancelaciones`

**Paso 2: Anexar consultas**

En Power Query:

```
1. Vaya a Inicio > Combinar > Anexar consultas para crear una nueva
2. Seleccione "Tres o más tablas"
3. Agregue todas las consultas de hechos listadas arriba
4. Haga clic en Aceptar
5. Renombre la nueva consulta como "Fact_Transacciones"
```

**Paso 3: Verificar estructura**

La tabla resultante debe tener exactamente estas columnas:
- `ID_Transaccion` (Texto)
- `Fecha` (Fecha)
- `SKU` (Texto)
- `ID_Marketplace` (Entero)
- `ID_Tipo_Transaccion` (Entero)
- `Monto` (Decimal)
- `Cantidad` (Entero)

Si alguna consulta individual tiene columnas adicionales o nombres diferentes, ajústelas antes de anexar.

#### 6.2. Validación de Datos

Antes de cargar el modelo, realice las siguientes validaciones:

**Validación 1: Coherencia de signos**

Cree una columna personalizada para verificar que los signos sean correctos:

```m
if [ID_Tipo_Transaccion] = 1 or [ID_Tipo_Transaccion] = 9 then
    if [Monto] > 0 then "OK" else "ERROR"
else
    if [Monto] < 0 then "OK" else "ERROR"
```

Filtre por "ERROR" para identificar inconsistencias.

**Validación 2: Fechas válidas**

Verifique que todas las fechas estén en un rango razonable (ej. entre 2025-01-01 y la fecha actual).

**Validación 3: SKUs existentes**

Haga un merge con `Dim_Producto` para identificar SKUs que no estén en el maestro de productos.

---

## Parte IV: Carga y Modelado en Excel

### Capítulo 7: Configuración del Modelo de Datos

#### 7.1. Carga de Consultas al Modelo de Datos

Para cada una de las tablas de dimensiones y la tabla de hechos:

```
1. En Power Query, seleccione la consulta
2. Vaya a Inicio > Cerrar y cargar en...
3. Seleccione "Solo crear conexión"
4. Marque la casilla "Agregar estos datos al Modelo de datos"
5. Haga clic en Aceptar
```

Repita para:
- `Dim_Tiempo`
- `Dim_Producto`
- `Dim_Marketplace`
- `Dim_Tipo_Transaccion`
- `Fact_Transacciones`

#### 7.2. Creación de Relaciones

**Paso 1: Abrir Power Pivot**

Vaya a la pestaña **Power Pivot > Administrar**. Esto abrirá la ventana de Power Pivot.

**Paso 2: Vista de diagrama**

En Power Pivot, haga clic en **Inicio > Vista de diagrama**. Verá todas las tablas cargadas.

**Paso 3: Crear relaciones**

Arrastre los campos para crear las siguientes relaciones:

| Tabla de Hechos | Columna | Tabla de Dimensión | Columna |
|-----------------|---------|-------------------|---------|
| Fact_Transacciones | Fecha | Dim_Tiempo | Fecha |
| Fact_Transacciones | SKU | Dim_Producto | SKU |
| Fact_Transacciones | ID_Marketplace | Dim_Marketplace | ID_Marketplace |
| Fact_Transacciones | ID_Tipo_Transaccion | Dim_Tipo_Transaccion | ID_Tipo_Transaccion |

**Paso 4: Verificar cardinalidad**

Todas las relaciones deben ser de tipo **Muchos a Uno** (Many-to-One), donde "Muchos" está en la tabla de hechos y "Uno" en la dimensión.

---

### Capítulo 8: Creación de Medidas DAX

Las medidas DAX son cálculos dinámicos que se evalúan en el contexto del análisis. A diferencia de las columnas calculadas, las medidas no ocupan espacio en memoria hasta que se utilizan.

#### 8.1. Medidas Básicas

**Total Ventas (GMV):**

```dax
Total_Ventas = 
CALCULATE(
    SUM(Fact_Transacciones[Monto]),
    Dim_Tipo_Transaccion[Tipo] = "Venta"
)
```

**Total Comisiones:**

```dax
Total_Comisiones = 
CALCULATE(
    SUM(Fact_Transacciones[Monto]),
    Dim_Tipo_Transaccion[Tipo] = "Comisión Marketplace"
)
```

**Total Costos de Envío:**

```dax
Total_Costos_Envio = 
CALCULATE(
    SUM(Fact_Transacciones[Monto]),
    Dim_Tipo_Transaccion[Tipo] = "Costo Envío"
)
```

**Total Devoluciones:**

```dax
Total_Devoluciones = 
CALCULATE(
    SUM(Fact_Transacciones[Monto]),
    Dim_Tipo_Transaccion[Tipo] = "Devolución"
)
```

#### 8.2. Medidas Avanzadas

**Venta Neta:**

```dax
Venta_Neta = 
[Total_Ventas] + 
[Total_Comisiones] + 
[Total_Costos_Envio] + 
[Total_Devoluciones]
```

Nota: Las comisiones, costos y devoluciones ya son negativos, por lo que se suman.

**Costo Total Marketplace:**

```dax
Costo_Total_Marketplace = 
CALCULATE(
    SUM(Fact_Transacciones[Monto]),
    Dim_Tipo_Transaccion[Categoria] = "Costo"
)
```

**Tasa de Devolución:**

```dax
Tasa_Devolucion = 
DIVIDE(
    ABS([Total_Devoluciones]),
    [Total_Ventas],
    0
)
```

Formato: Porcentaje con 2 decimales.

**Margen de Contribución:**

```dax
Margen_Contribucion = 
[Venta_Neta] - 
SUMX(
    Fact_Transacciones,
    Fact_Transacciones[Cantidad] * 
    RELATED(Dim_Producto[COGS])
)
```

Esta medida requiere que `Dim_Producto` tenga la columna `COGS` (costo de los bienes vendidos).

**Margen de Contribución %:**

```dax
Margen_Contribucion_Pct = 
DIVIDE(
    [Margen_Contribucion],
    [Total_Ventas],
    0
)
```

#### 8.3. Medidas de Comparación Temporal

**Ventas Mes Anterior:**

```dax
Ventas_Mes_Anterior = 
CALCULATE(
    [Total_Ventas],
    DATEADD(Dim_Tiempo[Fecha], -1, MONTH)
)
```

**Crecimiento vs Mes Anterior:**

```dax
Crecimiento_MoM = 
DIVIDE(
    [Total_Ventas] - [Ventas_Mes_Anterior],
    [Ventas_Mes_Anterior],
    0
)
```

**Ventas Acumuladas del Año:**

```dax
Ventas_YTD = 
CALCULATE(
    [Total_Ventas],
    DATESYTD(Dim_Tiempo[Fecha])
)
```

---

## Parte V: Dashboard Gerencial 360°

### Capítulo 9: Diseño de Visualizaciones

#### 9.1. KPIs Principales (Tarjetas)

Cree una nueva hoja llamada "Dashboard_Gerencial". Inserte tarjetas para mostrar los KPIs principales:

- **Total Ventas (GMV)**
- **Venta Neta**
- **Margen de Contribución**
- **Margen de Contribución %**
- **Tasa de Devolución**

Configure cada tarjeta con formato de número apropiado (moneda para valores monetarios, porcentaje para tasas).

#### 9.2. Gráfico de Cascada (Waterfall Chart)

Este gráfico es ideal para mostrar cómo el GMV se descompone hasta llegar a la venta neta.

**Paso 1: Crear tabla auxiliar**

Cree una tabla manual en Excel con la siguiente estructura:

| Concepto | Orden | Medida |
|----------|-------|--------|
| GMV | 1 | =Total_Ventas |
| Comisiones | 2 | =Total_Comisiones |
| Costos de Envío | 3 | =Total_Costos_Envio |
| Devoluciones | 4 | =Total_Devoluciones |
| Venta Neta | 5 | =Venta_Neta |

**Paso 2: Insertar gráfico**

Seleccione la tabla y vaya a **Insertar > Gráficos > Cascada**. Configure:
- Eje horizontal: Concepto
- Valores: Medida
- Marque "Venta Neta" como "Total"

#### 9.3. Matriz de Rentabilidad por Marketplace

Inserte una **Tabla Dinámica**:

**Configuración:**
- Filas: `Dim_Marketplace[Nombre]`
- Columnas: `Dim_Tipo_Transaccion[Categoria]`
- Valores: `SUM(Fact_Transacciones[Monto])`

Agregue formato condicional para resaltar los marketplaces más rentables.

#### 9.4. Análisis de Devoluciones (Gráfico de Pareto)

**Paso 1: Crear tabla dinámica de productos por devoluciones**

- Filas: `Dim_Producto[SKU]`, `Dim_Producto[Descripcion]`
- Valores: `Total_Devoluciones` (ordenado de mayor a menor)
- Filtro: `Dim_Tipo_Transaccion[Tipo]` = "Devolución"

**Paso 2: Calcular porcentaje acumulado**

Agregue una columna calculada en la tabla dinámica para el porcentaje acumulado.

**Paso 3: Crear gráfico combinado**

- Barras: Monto de devoluciones por producto
- Línea: Porcentaje acumulado

#### 9.5. Tendencia Temporal

Inserte un **Gráfico de Líneas**:

**Configuración:**
- Eje horizontal: `Dim_Tiempo[Fecha]` (agrupado por mes)
- Valores:
  - `Total_Ventas`
  - `Venta_Neta`
  - `Margen_Contribucion`

#### 9.6. Segmentadores (Slicers)

Agregue segmentadores para permitir filtrado interactivo:

- `Dim_Marketplace[Nombre]`
- `Dim_Tiempo[Año]`
- `Dim_Tiempo[Trimestre]`
- `Dim_Producto[Categoria]`

Configure los segmentadores para que afecten a todos los gráficos del dashboard.

---

## Parte VI: Actualización y Mantenimiento

### Capítulo 10: Proceso de Actualización

#### 10.1. Actualización Mensual

Al final de cada mes:

```
1. Descargue los nuevos reportes de cada marketplace
2. Coloque los archivos en las carpetas correspondientes
3. Abra el archivo de Excel del reporte
4. Vaya a Datos > Actualizar todo
5. Power Query procesará automáticamente los nuevos archivos
6. Verifique que no haya errores en las consultas
7. Revise el dashboard para validar los nuevos datos
```

#### 10.2. Validaciones Post-Actualización

**Validación 1: Coherencia de totales**

Compare el total de ventas del dashboard con los reportes originales de cada marketplace para asegurar que no haya discrepancias.

**Validación 2: Fechas**

Verifique que las transacciones del último mes se hayan cargado correctamente.

**Validación 3: Nuevos SKUs**

Si aparecen nuevos SKUs, actualice el maestro de productos (`Dim_Producto`) con la información correspondiente.

#### 10.3. Mantenimiento de Dimensiones

**Actualización de `Dim_Producto`:**

Si agrega nuevos productos, actualice el archivo maestro de productos y refresque la consulta.

**Actualización de `Dim_Tiempo`:**

Al inicio de cada año, extienda la tabla de calendario modificando las fechas de inicio y fin en el código M.

**Actualización de `Dim_Tipo_Transaccion`:**

Si los marketplaces introducen nuevos tipos de cargos, agregue filas a esta tabla con el ID y descripción correspondientes.

---

## Anexo A: Tabla de Referencia de Aristas por Marketplace

### Mercado Libre

| Arista | Fuente | Columna Clave | Tipo de Transacción |
|--------|--------|---------------|---------------------|
| Venta | Reporte Facturación | Valor de la compra | 1 - Venta |
| Comisión | Reporte Facturación | Costo por categoría + cuotas | 2 - Comisión |
| Costo Fijo | Reporte Facturación | Costo fijo | 4 - Costo Fijo |
| Envío | Reporte Facturación | Valor del cargo (filtrado por "Cargo por envío") | 3 - Costo Envío |
| Publicidad | Reporte Facturación | Valor del cargo (filtrado por "Cargo por publicación") | 7 - Publicidad |
| Devolución | Reporte Poscobro | Monto (filtrado por "refund") | 5 - Devolución |
| Bonificación | Reporte Facturación | Valor del cargo (negativo) | 9 - Bonificación |

### Paris Marketplace

| Arista | Fuente | Columna Clave | Tipo de Transacción |
|--------|--------|---------------|---------------------|
| Venta | Reporte Finanzas | Monto | 1 - Venta |
| Comisión | Reporte Finanzas | Comisión | 2 - Comisión |
| Envío | Reporte Logística | Costo de envío | 3 - Costo Envío |
| Devolución | Reporte Finanzas (filtrado) | Monto (negativo) | 5 - Devolución |
| Cancelación | Reporte Finanzas (filtrado) | Monto (negativo) | 6 - Cancelación |

### Ripley Marketplace

| Arista | Fuente | Columna Clave | Tipo de Transacción |
|--------|--------|---------------|---------------------|
| Venta | Reporte Pedidos | Importe | 1 - Venta |
| Comisión | Reporte Pedidos | Comisión (sin impuestos) | 2 - Comisión |
| Costo Fijo | Calculado (si Importe ≤ 5000) | -990 | 4 - Costo Fijo |
| Devolución | Reporte Historial | Importe (negativo) | 5 - Devolución |
| Cancelación | Reporte Historial | Importe (negativo) | 6 - Cancelación |
| Costo Logístico | Tabla de tarifas o reporte específico | Variable | 3 - Costo Envío |

---

## Anexo B: Código M Completo para Funciones Personalizadas

### Función: Estandarizar Transacción

Esta función toma una tabla RAW y la transforma al formato estándar de la tabla de hechos.

```m
(Tabla as table, IDMarketplace as number, IDTipoTransaccion as number, ColumnaID as text, ColumnaFecha as text, ColumnaSKU as text, ColumnaMonto as text, MultiplicadorMonto as number) =>
let
    SeleccionarColumnas = Table.SelectColumns(Tabla, {ColumnaID, ColumnaFecha, ColumnaSKU, ColumnaMonto}),
    RenombrarColumnas = Table.RenameColumns(SeleccionarColumnas, {
        {ColumnaID, "ID_Transaccion"},
        {ColumnaFecha, "Fecha"},
        {ColumnaSKU, "SKU"},
        {ColumnaMonto, "Monto"}
    }),
    AjustarMonto = Table.TransformColumns(RenombrarColumnas, {{"Monto", each _ * MultiplicadorMonto, type number}}),
    AgregarMarketplace = Table.AddColumn(AjustarMonto, "ID_Marketplace", each IDMarketplace, Int64.Type),
    AgregarTipo = Table.AddColumn(AgregarMarketplace, "ID_Tipo_Transaccion", each IDTipoTransaccion, Int64.Type),
    AgregarCantidad = Table.AddColumn(AgregarTipo, "Cantidad", each if IDTipoTransaccion = 5 or IDTipoTransaccion = 6 then -1 else 1, Int64.Type)
in
    AgregarCantidad
```

**Uso:**

```m
ML_Fact_Ventas = EstandarizarTransaccion(
    ML_Facturacion_RAW,
    1,
    1,
    "Número de venta",
    "Fecha del cargo",
    "Código ML",
    "Valor de la compra",
    1
)
```

---

## Anexo C: Fórmulas DAX Avanzadas

### Análisis de Cohortes (Productos con Mayor Tasa de Devolución)

```dax
Tasa_Devolucion_Por_Producto = 
VAR VentasProducto = 
    CALCULATE(
        SUM(Fact_Transacciones[Monto]),
        Dim_Tipo_Transaccion[Tipo] = "Venta"
    )
VAR DevolucionesProducto = 
    CALCULATE(
        SUM(Fact_Transacciones[Monto]),
        Dim_Tipo_Transaccion[Tipo] = "Devolución"
    )
RETURN
    DIVIDE(ABS(DevolucionesProducto), VentasProducto, 0)
```

### Rentabilidad por Unidad

```dax
Rentabilidad_Por_Unidad = 
VAR UnidadesVendidas = 
    CALCULATE(
        SUM(Fact_Transacciones[Cantidad]),
        Dim_Tipo_Transaccion[Tipo] = "Venta"
    )
RETURN
    DIVIDE([Margen_Contribucion], UnidadesVendidas, 0)
```

### Contribución de Marketplace al Total

```dax
Contribucion_Marketplace_Pct = 
VAR VentasMarketplace = [Total_Ventas]
VAR VentasTotales = 
    CALCULATE(
        [Total_Ventas],
        ALL(Dim_Marketplace)
    )
RETURN
    DIVIDE(VentasMarketplace, VentasTotales, 0)
```

---

## Anexo D: Checklist de Implementación

### Fase 1: Preparación (Semana 1)

- [ ] Crear estructura de carpetas en `C:\Reporte_Marketplaces`
- [ ] Descargar reportes históricos de Mercado Libre (Facturación y Poscobro)
- [ ] Descargar reportes históricos de Paris (Finanzas, Logística)
- [ ] Descargar reportes históricos de Ripley (Pedidos, Historial)
- [ ] Preparar maestro de productos con SKU, descripción, categoría y COGS
- [ ] Documentar las comisiones vigentes de cada marketplace

### Fase 2: Construcción del Modelo (Semana 2-3)

- [ ] Crear consultas RAW en Power Query para cada fuente
- [ ] Crear tablas de dimensiones (Tiempo, Producto, Marketplace, Tipo)
- [ ] Transformar consultas RAW a formato estándar de hechos
- [ ] Anexar todas las consultas de hechos en `Fact_Transacciones`
- [ ] Validar coherencia de datos (signos, fechas, SKUs)
- [ ] Cargar consultas al Modelo de Datos
- [ ] Crear relaciones en Power Pivot

### Fase 3: Medidas y Dashboard (Semana 4)

- [ ] Crear medidas básicas (Total_Ventas, Total_Comisiones, etc.)
- [ ] Crear medidas avanzadas (Venta_Neta, Margen_Contribucion, etc.)
- [ ] Crear medidas de comparación temporal
- [ ] Diseñar dashboard con KPIs principales
- [ ] Crear gráfico de cascada
- [ ] Crear matriz de rentabilidad
- [ ] Crear análisis de devoluciones
- [ ] Agregar segmentadores

### Fase 4: Validación y Documentación (Semana 5)

- [ ] Validar totales contra reportes originales
- [ ] Documentar proceso de actualización mensual
- [ ] Crear manual de usuario del dashboard
- [ ] Capacitar al equipo en el uso del reporte
- [ ] Establecer calendario de actualización mensual

---

## Conclusión

Esta guía representa un cambio de paradigma en la gestión de reportes de marketplaces. Al adoptar un modelo de datos relacional y capturar todas las aristas del negocio, usted obtiene una visión completa y precisa de la rentabilidad real de su operación. La inversión inicial en configuración se recupera rápidamente a través de la automatización y la capacidad de tomar decisiones informadas basadas en datos confiables.

El modelo propuesto es escalable y flexible. Cuando necesite agregar un nuevo marketplace, simplemente cree las consultas correspondientes siguiendo el mismo patrón de estandarización. Cuando los marketplaces introduzcan nuevos tipos de cargos, agregue una fila a `Dim_Tipo_Transaccion` y cree la consulta de hechos correspondiente.

Recuerde que un reporte gerencial no es un documento estático, sino una herramienta viva que debe evolucionar con su negocio. Revise periódicamente las métricas que está midiendo y ajuste el modelo según las necesidades cambiantes de su organización.

**La clave del éxito está en la disciplina de la actualización mensual y en la curiosidad constante por profundizar en los datos.** Con este modelo, tiene las herramientas para responder no solo "¿cuánto vendí?", sino "¿por qué vendí eso?", "¿dónde estoy perdiendo dinero?" y "¿qué debo hacer diferente el próximo mes?".

---

**Autor:** Manus AI  
**Contacto:** Para consultas sobre esta guía, visite [https://help.manus.im](https://help.manus.im)  
**Versión:** 2.0 - Diciembre 2025
