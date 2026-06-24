# Guía Práctica y Exhaustiva: Reporte Gerencial 360° de Marketplaces con Power Query

**Para Emprendedores: El Paso a Paso Detallado y Sin Omisiones**

---

## Introducción: El Reporte 360° y la Precisión

El objetivo de esta guía es crear un reporte que refleje la **Ganancia Real** de su operación en Marketplaces (Mercado Libre, Ripley y París). Para lograrlo, debemos aislar cada ingreso y cada costo (cada "arista") con **precisión quirúrgica**.

Esta versión de la guía se enfoca en el **detalle exacto** de cada paso en Power Query, asegurando que no haya omisiones en la selección de columnas o en la lógica de filtrado.

| Arista | Mercado Libre | Ripley | París |
| :--- | :--- | :--- | :--- |
| **Venta Bruta (GMV)** | ✅ | ✅ | ✅ |
| **Comisiones** | ✅ | ✅ | ✅ |
| **Costos de Envío** | ✅ | ✅ | ✅ |
| **Publicidad (Ads)** | ✅ | ❌ | ❌ |
| **Servicios Fullfilment** | ✅ | ❌ | ❌ |
| **Asesoría Comercial** | ✅ | ❌ | ❌ |
| **Devoluciones/Ajustes** | ✅ | ✅ | ✅ |

---

## Fase 1: La Preparación (Organización de Archivos)

La automatización de Power Query requiere que todos los archivos de un mismo tipo estén en una carpeta.

### Paso 1.1: Cree la Carpeta Maestra

1.  Cree una carpeta principal: `C:\Reporte_Marketplaces_360`.
2.  Cree las siguientes subcarpetas dentro de la carpeta principal:

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Pedidos (Ventas) | `Ripley_Pedidos` |
| **Ripley** | Reporte de Historial Financiero (Ajustes) | `Ripley_Ajustes` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |

### Paso 1.2: Carga Inicial en Power Query

1.  Abra un nuevo archivo de Excel.
2.  Vaya a la pestaña **Datos** > **Obtener Datos** > **De Archivos** > **De una Carpeta**.
3.  Seleccione la carpeta `ML_Facturacion`.
4.  Haga clic en **Combinar** > **Combinar y Transformar Datos**.
5.  Seleccione la hoja de datos (ej. "REPORT").
6.  En el Editor de Power Query, renombre la consulta a **`ML_Facturacion_RAW`**.
7.  Repita el proceso (Pasos 2 a 6) para las otras 4 carpetas, renombrando las consultas a: **`ML_Poscobro_RAW`**, **`Ripley_Pedidos_RAW`**, **`Ripley_Ajustes_RAW`**, y **`Paris_Finanzas_RAW`**.

---

## Fase 2: Mercado Libre - Desglose Exhaustivo (ML_Facturacion_RAW)

Duplicaremos la consulta **`ML_Facturacion_RAW`** 7 veces para aislar cada arista.

### 2.1. ML_Fact_Ventas (Venta Bruta o GMV)

*   **Objetivo:** Aislar el valor total de la venta.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por venta"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor de la compra`
    3.  **Renombrar Columnas:**
        *   `Número de venta` → **`ID_Transaccion`**
        *   `Fecha del cargo` → **`Fecha`**
        *   `Código ML` → **`SKU`**
        *   `Valor de la compra` → **`Monto`**
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.2. ML_Fact_Comisiones (Comisión por Venta)

*   **Objetivo:** Aislar el costo de la comisión.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por venta"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Costo por categoría + ofrecer cuotas`
    3.  **Renombrar Columnas:**
        *   `Número de venta` → **`ID_Transaccion`**
        *   `Fecha del cargo` → **`Fecha`**
        *   `Código ML` → **`SKU`**
        *   `Costo por categoría + ofrecer cuotas` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1** (para que sea un costo negativo).
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.3. ML_Fact_Envios (Costos Logísticos)

*   **Objetivo:** Aislar los costos de envío.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores **`"Cargo por Mercado Envíos"`** y **`"Cargo por envíos de Mercado Libre"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor del cargo`
    3.  **Renombrar Columnas:**
        *   `Número de venta` → **`ID_Transaccion`**
        *   `Fecha del cargo` → **`Fecha`**
        *   `Código ML` → **`SKU`**
        *   `Valor del cargo` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Costo Envío"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.4. ML_Fact_Publicidad (Ads)

*   **Objetivo:** Aislar los costos de publicidad.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Campañas de publicidad"`**, **`"Cargo por campaña de publicidad"`**, **`"Cargo por publicación"`**, **`"Mercado Ads"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor del cargo`
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Publicidad"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.5. ML_Fact_Asesoria (Asesoría Comercial)

*   **Objetivo:** Aislar el costo de Asesoría Comercial.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione solo el valor **`"Cargo por Asesoría Comercial"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor del cargo`
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Asesoría Comercial"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.6. ML_Fact_Fullfilment (Servicios Full)

*   **Objetivo:** Aislar los costos de almacenamiento y manejo de Fullfilment.
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Cargo por retiro de stock Full"`**, **`"Cargo por servicio de almacenamiento Full"`**, **`"Cargo por stock antiguo en Full"`**, **`"Cargo por mantenimiento de Mi página"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor del cargo`
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Costo Fullfilment"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

### 2.7. ML_Fact_Bonificaciones (Anulaciones y Bonos)

*   **Objetivo:** Aislar las devoluciones de cargos (ingresos positivos).
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Detalle`:** Seleccione los valores que **contengan** cualquiera de estos términos: **`"Bonificación"`**, **`"Anulación del cargo por venta"`**, **`"Anulación del cargo por Mercado Envíos"`**, **`"Anulación del cargo por envíos de Mercado Libre"`**, **`"Anulación del cargo por devolución"`**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de venta`
        *   `Fecha del cargo`
        *   `Código ML`
        *   `Valor del cargo`
    3.  **Renombrar Columnas:** (Misma lógica que 2.3).
    4.  **Transformación Crítica:** **NO** multiplique por -1. Las anulaciones ya vienen con signo positivo en el reporte de facturación.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Bonificación"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

---

## Fase 3: Mercado Libre - Devoluciones (ML_Poscobro_RAW)

### 3.1. ML_Fact_Devoluciones

*   **Consulta Fuente:** `ML_Poscobro_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `ENCONTRA`:** Seleccione solo el valor **`"refund"`** (si su reporte lo tiene). Si no, asuma que todas las filas son devoluciones.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `ID_TRANSACCION`
        *   `FECHA`
        *   `SKU`
        *   `MONTO_DEVOLUCION`
    3.  **Renombrar Columnas:**
        *   `MONTO_DEVOLUCION` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1** (la devolución es un costo).
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Devolución"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Mercado Libre"`**.

---

## Fase 4: Ripley - Desglose Exhaustivo

Duplicaremos la consulta **`Ripley_Pedidos_RAW`** y **`Ripley_Ajustes_RAW`**.

### 4.1. Ripley_Fact_Ventas (Venta Bruta o GMV)

*   **Consulta Fuente:** `Ripley_Pedidos_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Estado`:** Seleccione solo el estado de **venta completada** (ej. `"Entregado"` o similar).
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de pedido`
        *   `Fecha de creación`
        *   `SKU de oferta`
        *   `Importe`
    3.  **Renombrar Columnas:**
        *   `Número de pedido` → **`ID_Transaccion`**
        *   `Fecha de creación` → **`Fecha`**
        *   `SKU de oferta` → **`SKU`**
        *   `Importe` → **`Monto`**
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

### 4.2. Ripley_Fact_Comisiones (Comisión)

*   **Consulta Fuente:** `Ripley_Pedidos_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Estado`:** Seleccione solo el estado de **venta completada**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de pedido`
        *   `Fecha de creación`
        *   `SKU de oferta`
        *   `Comision (sin impuestos)`
    3.  **Renombrar Columnas:**
        *   `Número de pedido` → **`ID_Transaccion`**
        *   `Fecha de creación` → **`Fecha`**
        *   `SKU de oferta` → **`SKU`**
        *   `Comision (sin impuestos)` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

### 4.3. Ripley_Fact_Ajustes (Devoluciones, Cancelaciones y Penalizaciones)

*   **Consulta Fuente:** `Ripley_Ajustes_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `Importe`:** Seleccione solo valores **menores a 0** (negativos), ya que representan egresos.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `Número de pedido`
        *   `Fecha de creación`
        *   `SKU de oferta`
        *   `Importe`
    3.  **Renombrar Columnas:**
        *   `Número de pedido` → **`ID_Transaccion`**
        *   `Fecha de creación` → **`Fecha`**
        *   `SKU de oferta` → **`SKU`**
        *   `Importe` → **`Monto`**
    4.  **Transformación Crítica:** **NO** multiplique por -1. El importe ya viene con el signo correcto (negativo) para ser un costo.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Ajuste"`** (o puede usar una columna condicional si el reporte tiene un campo para distinguir entre Devolución, Cancelación o Penalización).
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"Ripley"`**.

---

## Fase 5: París - Desglose Exhaustivo

Duplicaremos la consulta **`Paris_Finanzas_RAW`**.

### 5.1. Paris_Fact_Ventas (Venta Bruta o GMV)

*   **Consulta Fuente:** `Paris_Finanzas_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `ESTADO`:** Seleccione solo el estado de **venta completada** (ej. `"Entregado"` o similar).
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `ID_TRANSACCION`
        *   `FECHA`
        *   `SKU`
        *   `GMV`
    3.  **Renombrar Columnas:**
        *   `GMV` → **`Monto`**
    4.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Venta"`**.
    5.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

### 5.2. Paris_Fact_Comisiones (Comisión)

*   **Consulta Fuente:** `Paris_Finanzas_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `ESTADO`:** Seleccione solo el estado de **venta completada**.
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `ID_TRANSACCION`
        *   `FECHA`
        *   `SKU`
        *   `COMISION`
    3.  **Renombrar Columnas:**
        *   `COMISION` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1**.
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Comisión"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

### 5.3. Paris_Fact_Ajustes (Devoluciones y Cancelaciones)

*   **Consulta Fuente:** `Paris_Finanzas_RAW`
*   **Instrucciones de Power Query:**
    1.  **Filtrar Columna `ESTADO`:** Seleccione los estados que representen egresos (ej. `"Devuelto"`, `"Cancelado"`, `"Reembolsado"`).
    2.  **Seleccionar Columnas:** Mantenga **únicamente** las siguientes 4 columnas:
        *   `ID_TRANSACCION`
        *   `FECHA`
        *   `SKU`
        *   `GMV` (o la columna que contenga el monto del reembolso)
    3.  **Renombrar Columnas:**
        *   `GMV` → **`Monto`**
    4.  **Transformación Crítica:** Seleccione la columna `Monto` y **Multiplique por -1** (si el monto de reembolso viene en positivo).
    5.  **Agregar Columna Personalizada `Tipo_Transaccion`:** Valor fijo **`"Ajuste"`**.
    6.  **Agregar Columna Personalizada `Marketplace`:** Valor fijo **`"París"`**.

---

## Fase 6: Unificación y Reporte Final

Una vez que todas las consultas de las Fases 2, 3, 4 y 5 estén limpias y estandarizadas (todas con las 5 columnas: `ID_Transaccion`, `Fecha`, `SKU`, `Monto`, `Tipo_Transaccion`, `Marketplace`), proceda a la unificación.

### Paso 6.1: Unificar la Tabla Maestra

1.  En el Editor de Power Query, vaya a **Inicio** > **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
2.  Mueva **TODAS** las consultas limpias (ej. `ML_Fact_Ventas`, `ML_Fact_Comisiones`, `Ripley_Fact_Ventas`, etc.) a la lista de tablas a anexar.
3.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### Paso 6.2: Cargar y Crear el Dashboard

1.  En la consulta **`DATA_MAESTRA_360`**, haga clic en **Cerrar y Cargar en...**
2.  Cree una **Tabla Dinámica** en Excel.
3.  **La Métrica Clave:** Arrastre la columna **`Monto`** a la sección **Valores**.
4.  **Análisis 360°:** Arrastre **`Marketplace`** y **`Tipo_Transaccion`** a la sección **Filas**.

El resultado de la suma de la columna `Monto` en la Tabla Dinámica será su **Venta Neta Real** después de todos los costos.

---

**Autor:** Manus AI  
**Versión:** 4.0 - Diciembre 2025  
**Nota:** Esta guía es la versión más detallada y exhaustiva, asegurando la correcta selección y transformación de cada columna.
