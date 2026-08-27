# Guía Definitiva: Reporte Gerencial 360° de Marketplaces con Power Query

**Flujo Continuo y Detallado en un Único Archivo de Excel**

---

## Introducción: El Proyecto en un Solo Archivo

El objetivo de este proyecto es crear un **único archivo de Excel** que contenga toda la lógica de Power Query para consolidar los datos de Mercado Libre, Ripley y París. Este archivo será su **Dashboard Maestro**.

**El Flujo de Trabajo es Continuo:**

1.  **Carga Inicial:** Conectamos el archivo de Excel a las carpetas de reportes.
2.  **Transformación:** Dentro del Editor de Power Query (en el mismo archivo), limpiamos y estandarizamos cada reporte.
3.  **Consolidación:** Unimos todas las consultas limpias en una sola tabla maestra.
4.  **Reporte Final:** Cargamos la tabla maestra en una hoja de Excel para crear la Tabla Dinámica.

---

## Fase 1: La Preparación y Carga Inicial

### Paso 1.1: Organización de Carpetas (El Requisito de Power Query)

Cree la siguiente estructura de carpetas en su disco duro. Power Query leerá los archivos que ponga dentro de ellas.

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Pedidos (Ventas) | `Ripley_Pedidos` |
| **Ripley** | Reporte de Historial Financiero (Ajustes) | `Ripley_Ajustes` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |

### Paso 1.2: Carga de Datos en el Único Archivo de Excel

**Abra un nuevo archivo de Excel.** Este será su archivo maestro.

1.  Vaya a la pestaña **Datos** > **Obtener Datos** > **De Archivos** > **De una Carpeta**.
2.  Seleccione la carpeta `ML_Facturacion`.
3.  Aparecerá una ventana con la lista de archivos. Haga clic en **Combinar** > **Combinar y Transformar Datos**.
4.  Seleccione la hoja de datos (ej. "REPORT").
5.  En el Editor de Power Query, renombre la consulta a **`ML_Facturacion_RAW`**.
6.  **Repita el proceso (Pasos 1 a 5) para las otras 4 carpetas**, renombrando las consultas a: **`ML_Poscobro_RAW`**, **`Ripley_Pedidos_RAW`**, **`Ripley_Ajustes_RAW`**, y **`Paris_Finanzas_RAW`**.

**Resultado de la Fase 1:** Tendrá 5 consultas RAW en el panel izquierdo del Editor de Power Query, todas dentro de su único archivo de Excel.

---

## Fase 2: Mercado Libre - Desglose Exhaustivo (Transformación)

**Objetivo:** Duplicar `ML_Facturacion_RAW` 7 veces para aislar cada arista de costo y venta.

### 2.1. ML_Fact_Ventas (Venta Bruta o GMV)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por venta"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor de la compra`.
    3.  **Renombrar Columnas:** `Número de venta` → **`ID_Transaccion`**, `Fecha del cargo` → **`Fecha`**, `Código ML` → **`SKU`**, `Valor de la compra` → **`Monto`**.
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.2. ML_Fact_Comisiones (Comisión por Venta)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por venta"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Costo por categoría + ofrecer cuotas`.
    3.  **Renombrar Columnas:** `Número de venta` → **`ID_Transaccion`**, `Fecha del cargo` → **`Fecha`**, `Código ML` → **`SKU`**, `Costo por categoría + ofrecer cuotas` → **`Monto`**.
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.3. ML_Fact_Envios (Costos Logísticos)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores **`"Cargo por Mercado Envíos"`** y **`"Cargo por envíos de Mercado Libre"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor del cargo`.
    3.  **Renombrar Columnas:** `Número de venta` → **`ID_Transaccion`**, `Fecha del cargo` → **`Fecha`**, `Código ML` → **`SKU`**, `Valor del cargo` → **`Monto`**.
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Costo Envío"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.4. ML_Fact_Publicidad (Ads)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Campañas de publicidad"`**, **`"Cargo por campaña de publicidad"`**, **`"Cargo por publicación"`**, **`"Mercado Ads"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor del cargo`.
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Publicidad"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.5. ML_Fact_Asesoria (Asesoría Comercial)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por Asesoría Comercial"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor del cargo`.
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Asesoría Comercial"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.6. ML_Fact_Fullfilment (Servicios Full)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Cargo por retiro de stock Full"`**, **`"Cargo por servicio de almacenamiento Full"`**, **`"Cargo por stock antiguo en Full"`**, **`"Cargo por mantenimiento de Mi página"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor del cargo`.
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Costo Fullfilment"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.7. ML_Fact_Bonificaciones (Anulaciones y Bonos)

*   **Consulta Fuente:** Duplicar `ML_Facturacion_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Bonificación"`**, **`"Anulación del cargo por venta"`**, **`"Anulación del cargo por Mercado Envíos"`**, **`"Anulación del cargo por envíos de Mercado Libre"`**, **`"Anulación del cargo por devolución"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de venta`, `Fecha del cargo`, `Código ML`, `Valor del cargo`.
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** **NO** multiplique por -1.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Bonificación"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.8. ML_Fact_Devoluciones (Poscobro)

*   **Consulta Fuente:** Duplicar `ML_Poscobro_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO_DEVOLUCION`.
    2.  **Renombrar Columnas:** `MONTO_DEVOLUCION` → **`Monto`**.
    3.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Devolución"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

---

## Fase 3: Ripley y París - Desglose Exhaustivo (Transformación)

### 3.1. Ripley_Fact_Ventas (Venta Bruta o GMV)

*   **Consulta Fuente:** Duplicar `Ripley_Pedidos_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Estado`:** Seleccione solo el estado de **venta completada** (ej. `"Entregado"`).
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de pedido`, `Fecha de creación`, `SKU de oferta`, `Importe`.
    3.  **Renombrar Columnas:** `Número de pedido` → **`ID_Transaccion`**, `Fecha de creación` → **`Fecha`**, `SKU de oferta` → **`SKU`**, `Importe` → **`Monto`**.
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

### 3.2. Ripley_Fact_Comisiones (Comisión)

*   **Consulta Fuente:** Duplicar `Ripley_Pedidos_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Estado`:** Seleccione solo el estado de **venta completada**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de pedido`, `Fecha de creación`, `SKU de oferta`, `Comision (sin impuestos)`.
    3.  **Renombrar Columnas:** `Número de pedido` → **`ID_Transaccion`**, `Fecha de creación` → **`Fecha`**, `SKU de oferta` → **`SKU`**, `Comision (sin impuestos)` → **`Monto`**.
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

### 3.3. Ripley_Fact_Ajustes (Devoluciones, Cancelaciones y Penalizaciones)

*   **Consulta Fuente:** Duplicar `Ripley_Ajustes_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Importe`:** Seleccione solo valores **menores a 0** (negativos).
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `Número de pedido`, `Fecha de creación`, `SKU de oferta`, `Importe`.
    3.  **Renombrar Columnas:** `Número de pedido` → **`ID_Transaccion`**, `Fecha de creación` → **`Fecha`**, `SKU de oferta` → **`SKU`**, `Importe` → **`Monto`**.
    4.  **Transformación Crítica:** **NO** multiplique por -1. El importe ya viene con el signo correcto (negativo).
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Ajuste"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

### 3.4. Paris_Fact_Ventas (Venta Bruta o GMV)

*   **Consulta Fuente:** Duplicar `Paris_Finanzas_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `TIPO`:** Seleccione solo el valor **`"Venta"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO`.
    3.  **Renombrar Columnas:** `MONTO` → **`Monto`** (Asegúrese de que esta columna sea el GMV).
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

### 3.5. Paris_Fact_Comisiones (Comisión)

*   **Consulta Fuente:** Duplicar `Paris_Finanzas_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `TIPO`:** Seleccione solo el valor **`"Comisión"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO`.
    3.  **Renombrar Columnas:** `MONTO` → **`Monto`**.
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

### 3.6. Paris_Fact_Logistica (Despacho, Logística Inversa, Compensación)

*   **Consulta Fuente:** Duplicar `Paris_Finanzas_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `TIPO`:** Seleccione los valores **`"Despacho"`**, **`"Cobro por despacho"`**, **`"Logística inversa"`**, **`"Compensación logística"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO`.
    3.  **Renombrar Columnas:** `MONTO` → **`Monto`**.
    4.  **Transformación Crítica:**
        *   Para **`"Despacho"`**, **`"Cobro por despacho"`** y **`"Logística inversa"`**: Multiplique `Monto` por **-1** (son costos).
        *   Para **`"Compensación logística"`**: **NO** multiplique por -1 (es un ingreso/abono).
        *   *Sugerencia: Use una Columna Condicional para aplicar el signo.*
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Logística"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

### 3.7. Paris_Fact_OtrosCargos (Cargos, Cobro por Campaña, Rebate)

*   **Consulta Fuente:** Duplicar `Paris_Finanzas_RAW`.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `TIPO`:** Seleccione los valores **`"Cargo"`**, **`"Cobro por campaña"`**, **`"Rebate"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO`.
    3.  **Renombrar Columnas:** `MONTO` → **`Monto`**.
    4.  **Transformación Crítica:**
        *   Para **`"Cargo"`** y **`"Cobro por campaña"`**: Multiplique `Monto` por **-1** (son costos).
        *   Para **`"Rebate"`**: **NO** multiplique por -1 (es un ingreso/abono).
        *   *Sugerencia: Use una Columna Condicional para aplicar el signo.*
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Otros Cargos"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

---

## Fase 4: Consolidación y Reporte Final (En el Mismo Archivo de Excel)

### Paso 4.1: Consolidación de la Tabla Maestra (Anexar Consultas)

**Asegúrese de que todas las consultas de las Fases 2 y 3 tengan exactamente las mismas 6 columnas:** `ID_Transaccion`, `Fecha`, `SKU`, `Monto`, `Tipo_Transaccion`, `Marketplace`.

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
3.  Seleccione la opción **Tres o más tablas**.
4.  Mueva **TODAS** las consultas limpias (las que empiezan con `ML_Fact_`, `Ripley_Fact_` y `Paris_Fact_`) a la lista de tablas a anexar.
5.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### Paso 4.2: Cargar la Tabla Maestra en Excel

1.  En la consulta **`DATA_MAESTRA_360`**, vaya a **Inicio** y haga clic en **Cerrar y Cargar en...**
2.  Seleccione **Tabla** y **Nueva Hoja de Cálculo**.
3.  Power Query cargará la tabla consolidada en una nueva hoja de su archivo de Excel.

### Paso 4.3: Crear el Dashboard (Tabla Dinámica)

1.  Seleccione la tabla cargada y vaya a la pestaña **Insertar** > **Tabla Dinámica**.
2.  **La Métrica Clave (Venta Neta Real):**
    *   Arrastre la columna **`Monto`** a la sección **Valores**.
    *   Arrastre **`Marketplace`** y **`Tipo_Transaccion`** a la sección **Filas**.

El resultado de la suma de la columna `Monto` en la Tabla Dinámica es su **Venta Neta Real** después de todos los costos.

---

**Autor:** Manus AI  
**Versión:** 5.0 - Diciembre 2025  
**Nota:** Esta guía es la versión final, con un flujo continuo y el detalle exhaustivo de cada paso de filtrado y consolidación en un único archivo de Excel.
