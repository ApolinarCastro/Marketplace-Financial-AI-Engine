# Guía Definitiva PRO: Reporte Gerencial 360° de Marketplaces con Power Query (Incluye Código M)

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

## Fase 2: Transformación y Desglose Exhaustivo (Uso del Código M)

En lugar de seguir el paso a paso manual, puede crear las consultas personalizadas de forma instantánea usando el **Código M** que se adjunta en el Anexo.

### Paso 2.1: Crear Consultas Personalizadas

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Nueva Consulta** > **Otras Fuentes** > **Consulta en Blanco**.
3.  Vaya al **Editor Avanzado** (pestaña Inicio).
4.  Copie y pegue el código M de la consulta que desea crear (ej. `ML_Fact_Ventas`) del Anexo y haga clic en **Listo**.
5.  Repita este proceso para **TODAS** las consultas de desglose (un total de 16 consultas).

**Consultas a Crear (Total 16):**

| Mercado Libre (8) | Ripley (3) | París (5) |
| :--- | :--- | :--- |
| `ML_Fact_Ventas` | `Ripley_Fact_Ventas` | `Paris_Fact_Ventas` |
| `ML_Fact_Comisiones` | `Ripley_Fact_Comisiones` | `Paris_Fact_Comisiones` |
| `ML_Fact_Envios` | `Ripley_Fact_Ajustes` | `Paris_Fact_DescuentoComercial` |
| `ML_Fact_Publicidad` | | `Paris_Fact_Logistica` |
| `ML_Fact_Asesoria` | | `Paris_Fact_OtrosCargos` |
| `ML_Fact_Fullfilment` | | |
| `ML_Fact_Bonificaciones` | | |
| `ML_Fact_Devoluciones` | | |

---

## Fase 3: Consolidación y Reporte Final

### Paso 3.1: Consolidación de la Tabla Maestra (Anexar Consultas)

**Asegúrese de que todas las 16 consultas de desglose tengan exactamente las mismas 6 columnas:** `ID_Transaccion`, `Fecha`, `SKU`, `Monto`, `Tipo_Transaccion`, `Marketplace`.

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
3.  Seleccione la opción **Tres o más tablas**.
4.  Mueva **TODAS** las 16 consultas de desglose a la lista de tablas a anexar.
5.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### Paso 3.2: Cargar la Tabla Maestra en Excel

1.  En la consulta **`DATA_MAESTRA_360`**, vaya a **Inicio** y haga clic en **Cerrar y Cargar en...**
2.  Seleccione **Tabla** y **Nueva Hoja de Cálculo**.

### Paso 3.3: Crear el Dashboard (Tabla Dinámica)

1.  Seleccione la tabla cargada y vaya a la pestaña **Insertar** > **Tabla Dinámica**.
2.  **La Métrica Clave (Venta Neta Real):**
    *   Arrastre la columna **`Monto`** a la sección **Valores**.
    *   Arrastre **`Marketplace`** y **`Tipo_Transaccion`** a la sección **Filas**.

El resultado de la suma de la columna `Monto` en la Tabla Dinámica es su **Venta Neta Real** después de todos los costos.

---

## Anexo: Código M (Power Query) para Consultas Personalizadas

### Mercado Libre

#### ML_Fact_Ventas
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor de la compra"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor de la compra", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Comisiones
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Código ML", "Costo por categoría + ofrecer cuotas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Costo por categoría + ofrecer cuotas", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Envios
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Tipos Envío" = {"Cargo por Mercado Envíos", "Cargo por envíos de Mercado Libre"},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Detalle])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Costo Envío"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Publicidad
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Publicidad" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "publicidad", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Ads", Comparer.OrdinalIgnoreCase) or [Detalle] = "Cargo por publicación"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Publicidad", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Publicidad"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Asesoria
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Asesoría" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por Asesoría Comercial"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Asesoría", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Asesoría Comercial"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Fullfilment
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Full" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Full", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Full", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Costo Fullfilment"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Bonificaciones
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Bonificación" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Bonificación", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Anulación", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Bonificación", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Bonificación"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```

#### ML_Fact_Devoluciones
```m

let
    Fuente = ML_Poscobro_RAW,
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID_TRANSACCION", "FECHA", "SKU", "MONTO_DEVOLUCION"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID_TRANSACCION", "ID_Transaccion"}, {"FECHA", "Fecha"}, {"MONTO_DEVOLUCION", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Devolución"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"

```


### Ripley

#### Ripley_Fact_Ventas
```m

let
    Fuente = Ripley_Pedidos_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Estado] = "Entregado"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"

```

#### Ripley_Fact_Comisiones
```m

let
    Fuente = Ripley_Pedidos_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Estado] = "Entregado"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Comision (sin impuestos)"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Comision (sin impuestos)", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"

```

#### Ripley_Fact_Ajustes
```m

let
    Fuente = Ripley_Ajustes_RAW,
    #"Filtrar Ajustes" = Table.SelectRows(Fuente, each [Importe] <> 0 and [Importe] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Ajustes", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe", "Tipo de Ajuste"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each [Tipo de Ajuste]),
    #"Eliminar Tipo Original" = Table.RemoveColumns(#"Agregar Tipo", {{"Tipo de Ajuste"}}),
    #"Agregar Marketplace" = Table.AddColumn(#"Eliminar Tipo Original", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"

```


### París

#### Paris_Fact_Ventas
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "París")
in
    #"Agregar Marketplace"

```

#### Paris_Fact_Comisiones
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Calcular Monto Comisión" = Table.AddColumn(#"Filtrar Venta", "Monto_Comision", each [MONTO] * [COMISIÓN] / 100, type number),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Calcular Monto Comisión", {{"NÚMERO ORDEN", "FECHA", "SKU", "Monto_Comision"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"Monto_Comision", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "París")
in
    #"Agregar Marketplace"

```

#### Paris_Fact_DescuentoComercial
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Descuento" = Table.SelectRows(Fuente, each [TIPO] = "Venta" and [DESCUENTO COMERCIAL] <> 0 and [DESCUENTO COMERCIAL] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Descuento", {{"NÚMERO ORDEN", "FECHA", "SKU", "DESCUENTO COMERCIAL"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"DESCUENTO COMERCIAL", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Descuento Comercial"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "París")
in
    #"Agregar Marketplace"

```

#### Paris_Fact_Logistica
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Tipos Logísticos" = {"Despacho", "Cobro por despacho", "Logística inversa", "Compensación logística"},
    #"Filtrar Logística" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Logísticos", [TIPO])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Logística", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO", "TIPO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Aplicar Signo Condicional" = Table.AddColumn(#"Renombrar Columnas", "Monto_Final", each 
        if [TIPO] = "Compensación logística" then [Monto] 
        else -[Monto], type number),
    #"Eliminar Columnas Originales" = Table.RemoveColumns(#"Aplicar Signo Condicional", {{"MONTO", "TIPO"}}),
    #"Renombrar Monto Final" = Table.RenameColumns(#"Eliminar Columnas Originales", {{"Monto_Final", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Monto Final", "Tipo_Transaccion", each "Logística"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "París")
in
    #"Agregar Marketplace"

```

#### Paris_Fact_OtrosCargos
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Tipos Otros" = {"Cargo", "Cobro por campaña", "Rebate"},
    #"Filtrar Otros" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Otros", [TIPO])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Otros", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO", "TIPO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Aplicar Signo Condicional" = Table.AddColumn(#"Renombrar Columnas", "Monto_Final", each 
        if [TIPO] = "Rebate" then [Monto] 
        else -[Monto], type number),
    #"Eliminar Columnas Originales" = Table.RemoveColumns(#"Aplicar Signo Condicional", {{"MONTO", "TIPO"}}),
    #"Renombrar Monto Final" = Table.RenameColumns(#"Eliminar Columnas Originales", {{"Monto_Final", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Monto Final", "Tipo_Transaccion", each "Otros Cargos"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "París")
in
    #"Agregar Marketplace"

```




---

**Autor:** Manus AI  
**Versión:** 6.0 - Diciembre 2025  
**Nota:** Esta guía es la versión final, con un flujo continuo, detalle exhaustivo y la inclusión del código M para una implementación rápida y precisa.
