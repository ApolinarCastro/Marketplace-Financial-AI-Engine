# Guía Práctica y Didáctica: Reporte Gerencial 360° de Marketplaces con Power Query

**Para Emprendedores sin Conocimientos Técnicos**

---

## Introducción: ¿Por qué un Reporte 360°?

Como emprendedor, usted necesita saber la **ganancia real** de cada venta, no solo el precio al que vendió. El error más común es confundir el **GMV** (Gross Merchandise Value o Venta Bruta) con la **Venta Neta** o, peor aún, con la **Ganancia Real**.

Su reporte anterior solo incluía ventas y devoluciones. El nuevo reporte 360° incluye todas las "aristas" (costos ocultos) que los Marketplaces le cobran:

| Costo Oculto | Mercado Libre | Ripley | París |
| :--- | :--- | :--- | :--- |
| **Comisiones** | ✅ | ✅ | ✅ |
| **Costos de Envío** | ✅ | ✅ | ✅ |
| **Publicidad (Ads)** | ✅ | ❌ | ❌ |
| **Servicios Fullfilment** | ✅ | ❌ | ❌ |
| **Asesoría Comercial** | ✅ | ❌ | ❌ |
| **Costo Fijo Operacional** | ✅ | ✅ | ❌ |
| **Anulaciones y Bonificaciones** | ✅ | ✅ | ✅ |

Esta guía le enseñará a usar **Power Query** (una herramienta gratuita de Excel) para automatizar la limpieza y consolidación de todos estos costos en un solo lugar, sin necesidad de fórmulas complejas.

---

## Fase 1: La Regla de Oro de la Automatización (Preparación)

La clave para que su reporte se actualice con un solo clic es la **organización de sus archivos**. Power Query es "inteligente" y puede leer todos los archivos que ponga en una carpeta.

### Paso 1.1: Cree la Carpeta Maestra

1.  Cree una carpeta principal en su disco duro, por ejemplo: `C:\Reporte_Marketplaces_360`.
2.  Dentro de esta carpeta, cree una subcarpeta para **cada tipo de reporte** que descargue de los Marketplaces.

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Pedidos (Ventas) | `Ripley_Pedidos` |
| **Ripley** | Reporte de Historial Financiero (Ajustes) | `Ripley_Ajustes` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |

### Paso 1.2: Cargue sus Archivos

*   Descargue todos sus reportes históricos (desde el mes que quiera analizar) y colóquelos en la subcarpeta correspondiente.
*   **Importante:** No cambie el nombre ni el formato de los archivos originales que descarga del Marketplace.

---

## Fase 2: La Magia de Power Query (Carga de Datos)

Ahora le enseñaremos a Excel a leer todas esas carpetas y a apilar los datos automáticamente.

### Paso 2.1: Conectar Excel a la Carpeta

1.  Abra un nuevo archivo de Excel.
2.  Vaya a la pestaña **Datos**.
3.  Haga clic en **Obtener Datos** > **De Archivos** > **De una Carpeta**.
4.  Seleccione la primera subcarpeta, por ejemplo: `C:\Reporte_Marketplaces_360\ML_Facturacion`.
5.  Aparecerá una ventana con la lista de archivos. Haga clic en **Combinar** > **Combinar y Transformar Datos**.
6.  En la ventana de combinación, seleccione la hoja de datos que contiene la información (ej. "REPORT" o la primera hoja). Power Query hará el resto.

### Paso 2.2: Limpiar y Renombrar (La Primera Transformación)

Una vez que se abra el **Editor de Power Query**, haga lo siguiente:

1.  **Renombre la Consulta:** En el panel derecho, cambie el nombre de la consulta a **`ML_Facturacion_RAW`**.
2.  **Repita el Proceso:** Repita los Pasos 2.1 y 2.2 para las otras 4 carpetas (`ML_Poscobro`, `Ripley_Pedidos`, `Ripley_Ajustes`, `Paris_Finanzas`). Al final, tendrá 5 consultas RAW.

---

## Fase 3: El Paso a Paso para el Reporte 360° (La Lógica de Filtrado)

Esta es la parte más importante. Vamos a duplicar la consulta `ML_Facturacion_RAW` para aislar cada tipo de costo.

### 3.1. Mercado Libre: Desglose de Costos (La Lógica 360°)

Duplique la consulta **`ML_Facturacion_RAW`** 6 veces y renómbrelas así:

1.  `ML_Fact_Ventas`
2.  `ML_Fact_Comisiones`
3.  `ML_Fact_Envios`
4.  `ML_Fact_Publicidad`
5.  `ML_Fact_Asesoria`
6.  `ML_Fact_Fullfilment`
7.  `ML_Fact_Bonificaciones`

#### A. `ML_Fact_Ventas` (Venta Bruta o GMV)

*   **Objetivo:** Aislar el valor total de la venta.
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que sea **igual a** `"Cargo por venta"`.
    2.  Seleccione la columna **`Valor de la compra`** (este es el GMV).
    3.  Renombre las columnas clave: `Número de venta` a **`ID_Transaccion`**, `Fecha del cargo` a **`Fecha`**, `Código ML` a **`SKU`**, y `Valor de la compra` a **`Monto`**.
    4.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Venta"`.

#### B. `ML_Fact_Comisiones` (Comisión por Venta)

*   **Objetivo:** Aislar el costo de la comisión.
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que sea **igual a** `"Cargo por venta"`.
    2.  Seleccione la columna **`Costo por categoría + ofrecer cuotas`** (este es el valor de la comisión).
    3.  Renombre las columnas clave (igual que en A).
    4.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1** (para que sea un costo negativo).
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Comisión"`.

#### C. `ML_Fact_Envios` (Costos Logísticos)

*   **Objetivo:** Aislar los costos de envío.
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que **contenga** cualquiera de estos términos: `"Cargo por Mercado Envíos"` **O** `"Cargo por envíos de Mercado Libre"`.
    2.  Seleccione la columna **`Valor del cargo`**.
    3.  Renombre las columnas clave.
    4.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1**.
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Costo Envío"`.

#### D. `ML_Fact_Publicidad` (Ads)

*   **Objetivo:** Aislar los costos de publicidad (Ads).
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que **contenga** cualquiera de estos términos: `"Campañas de publicidad"` **O** `"Cargo por campaña de publicidad"` **O** `"Cargo por publicación"` **O** `"Mercado Ads"`.
    2.  Seleccione la columna **`Valor del cargo`**.
    3.  Renombre las columnas clave.
    4.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1**.
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Publicidad"`.

#### E. `ML_Fact_Asesoria` (Asesoría Comercial)

*   **Objetivo:** Aislar el costo de Asesoría Comercial.
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que sea **igual a** `"Cargo por Asesoría Comercial"`.
    2.  Seleccione la columna **`Valor del cargo`**.
    3.  Renombre las columnas clave.
    4.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1**.
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Asesoría Comercial"`.

#### F. `ML_Fact_Fullfilment` (Servicios Full)

*   **Objetivo:** Aislar los costos de almacenamiento y manejo de Fullfilment.
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que **contenga** cualquiera de estos términos: `"Cargo por retiro de stock Full"` **O** `"Cargo por servicio de almacenamiento Full"` **O** `"Cargo por stock antiguo en Full"` **O** `"Cargo por mantenimiento de Mi página"`.
    2.  Seleccione la columna **`Valor del cargo`**.
    3.  Renombre las columnas clave.
    4.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1**.
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Costo Fullfilment"`.

#### G. `ML_Fact_Bonificaciones` (Anulaciones y Bonos)

*   **Objetivo:** Aislar las devoluciones de cargos (ingresos positivos).
*   **Acción:**
    1.  Filtre la columna **`Detalle`** para que **contenga** cualquiera de estos términos: `"Bonificación"` **O** `"Anulación del cargo por venta"` **O** `"Anulación del cargo por Mercado Envíos"` **O** `"Anulación del cargo por devolución"`.
    2.  Seleccione la columna **`Valor del cargo`**.
    3.  Renombre las columnas clave.
    4.  **Transformación Crítica:** **NO** multiplique por -1. Las anulaciones ya vienen con signo positivo en el reporte de facturación.
    5.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Bonificación"`.

### 3.2. Mercado Libre: Devoluciones (Poscobro)

*   **Consulta Fuente:** `ML_Poscobro_RAW`
*   **Acción:**
    1.  Seleccione las columnas: `ID_TRANSACCION`, `FECHA`, `SKU`, `MONTO_DEVOLUCION`.
    2.  Renombre `MONTO_DEVOLUCION` a **`Monto`**.
    3.  **Transformación Crítica:** Multiplique la columna **`Monto`** por **-1** (la devolución es un costo).
    4.  Agregue una columna personalizada llamada **`Tipo_Transaccion`** con el valor `"Devolución"`.
    5.  Agregue una columna **`Marketplace`** con el valor `"Mercado Libre"`.

### 3.3. Ripley: Ventas y Ajustes

*   **Consulta Fuente:** `Ripley_Pedidos_RAW` (Ventas) y `Ripley_Ajustes_RAW` (Ajustes)
*   **Acción (Ripley Ventas):**
    1.  Duplique `Ripley_Pedidos_RAW` y filtre por estado de venta completada.
    2.  Renombre `Importe` a **`Monto`**.
    3.  Agregue una columna **`Tipo_Transaccion`** con el valor `"Venta"`.
    4.  Agregue una columna **`Marketplace`** con el valor `"Ripley"`.
*   **Acción (Ripley Comisiones):**
    1.  Duplique `Ripley_Pedidos_RAW`.
    2.  Renombre `Comision` a **`Monto`**.
    3.  **Transformación Crítica:** Multiplique **`Monto`** por **-1**.
    4.  Agregue una columna **`Tipo_Transaccion`** con el valor `"Comisión"`.
*   **Acción (Ripley Ajustes/Devoluciones):**
    1.  Duplique `Ripley_Ajustes_RAW`.
    2.  Filtre la columna **`Importe`** para incluir solo valores negativos (reembolsos).
    3.  Renombre `Importe` a **`Monto`**.
    4.  Agregue una columna **`Tipo_Transaccion`** con el valor `"Devolución"` (o `"Ajuste"` si no puede distinguir).
    5.  Agregue una columna **`Marketplace`** con el valor `"Ripley"`.

### 3.4. París: Ventas y Comisiones

*   **Consulta Fuente:** `Paris_Finanzas_RAW`
*   **Acción (París Ventas):**
    1.  Duplique `Paris_Finanzas_RAW` y filtre por estado de venta completada.
    2.  Renombre `GMV` a **`Monto`**.
    3.  Agregue una columna **`Tipo_Transaccion`** con el valor `"Venta"`.
    4.  Agregue una columna **`Marketplace`** con el valor `"París"`.
*   **Acción (París Comisiones):**
    1.  Duplique `Paris_Finanzas_RAW`.
    2.  Renombre `COMISION` a **`Monto`**.
    3.  **Transformación Crítica:** Multiplique **`Monto`** por **-1**.
    4.  Agregue una columna **`Tipo_Transaccion`** con el valor `"Comisión"`.

---

## Fase 4: Unificación y Reporte Final

Una vez que haya limpiado y estandarizado todas las consultas (A, B, C, D, E, F, G de ML, más ML Poscobro, Ripley Ventas/Comisiones/Ajustes y París Ventas/Comisiones), todas deben tener las mismas 5 columnas:

1.  `ID_Transaccion`
2.  `Fecha`
3.  `SKU`
4.  `Monto`
5.  `Tipo_Transaccion`
6.  `Marketplace`

### Paso 4.1: Unificar la Tabla Maestra

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
3.  Seleccione la opción **Tres o más tablas**.
4.  Mueva todas las consultas limpias y estandarizadas (las que tienen el prefijo `ML_Fact_`, `ML_Poscobro`, `Ripley_` y `Paris_`) a la lista de tablas a anexar.
5.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### Paso 4.2: Cargar y Crear el Dashboard

1.  En la consulta **`DATA_MAESTRA_360`**, vaya a **Inicio** y haga clic en **Cerrar y Cargar en...**
2.  Seleccione **Tabla** y **Nueva Hoja de Cálculo**.
3.  Una vez cargada la tabla en Excel, vaya a la pestaña **Insertar** y haga clic en **Tabla Dinámica**.
4.  **Cree su Dashboard 360°:**
    *   **Filas:** Arrastre la columna **`Marketplace`** y luego **`Tipo_Transaccion`**.
    *   **Valores:** Arrastre la columna **`Monto`**.
    *   **Filtros:** Arrastre la columna **`Fecha`** y **`SKU`**.

### Paso 4.3: La Métrica Clave (Venta Neta)

La **Venta Neta** es simplemente la suma de la columna **`Monto`** en su Tabla Dinámica. Como los costos están en negativo y los ingresos en positivo, la suma le dará automáticamente la rentabilidad real después de todos los costos de Marketplace.

---

## Conclusión: Actualización en un Clic

¡Felicidades! Ha creado un reporte gerencial robusto.

Para actualizarlo el próximo mes, solo siga estos dos pasos:

1.  Descargue los nuevos reportes de los Marketplaces y colóquelos en las carpetas correctas (Paso 1.2).
2.  Abra su archivo de Excel y vaya a **Datos** > **Actualizar Todo**.

Power Query hará todo el trabajo de limpieza, filtrado y consolidación por usted. Ahora tiene la información completa para tomar decisiones estratégicas.

---

**Autor:** Manus AI  
**Versión:** 3.0 - Diciembre 2025  
**Nota:** Esta guía utiliza la lógica de filtrado exhaustiva de Mercado Libre, incluyendo todos los cargos de publicidad, Fullfilment y Asesoría Comercial.
