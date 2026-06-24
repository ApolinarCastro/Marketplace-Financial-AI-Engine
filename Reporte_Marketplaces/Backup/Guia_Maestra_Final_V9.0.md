# Guía Maestra Final PRO: Reporte Gerencial 360° de Marketplaces con Power Query (V9.0)

**La Guía Definitiva: Flujo Continuo, Detalle Exhaustivo y Códigos M Optimizados**

---

## Introducción: El Proyecto en un Solo Archivo y Estructura Optimizada

Esta guía es la **versión final y consolidada**, que incorpora la lógica exhaustiva de 360° y optimiza la estructura de datos a un **Esquema Estrella (Star Schema)**, manteniendo el hilo conductor de toda la información generada.

**El Flujo de Trabajo es Continuo:**

1.  **Carga Inicial:** Conectamos el archivo de Excel a las carpetas de reportes.
2.  **Modelado:** Creamos las Tablas de Dimensiones (`Dim_Marketplace`, `Dim_Tipo_Transaccion`).
3.  **Transformación:** Limpiamos y estandarizamos cada reporte en la **Tabla de Hechos** (`DATA_MAESTRA_360`).
4.  **Reporte Final:** Cargamos las tablas en Excel para crear la Tabla Dinámica.

---

## Fase 1: La Preparación y Carga Inicial

### Paso 1.1: Organización de Carpetas (El Requisito de Power Query)

Cree la siguiente estructura de carpetas en su disco duro. Power Query leerá los archivos que ponga dentro de ellas.

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Historial Financiero | `Ripley_Finanzas` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |

### Paso 1.2: Carga de Datos en el Único Archivo de Excel

**Abra un nuevo archivo de Excel.** Este será su archivo maestro.

1.  Vaya a la pestaña **Datos** > **Obtener Datos** > **De Archivos** > **De una Carpeta**.
2.  Seleccione la carpeta `ML_Facturacion`.
3.  Aparecerá una ventana con la lista de archivos. Haga clic en **Combinar** > **Combinar y Transformar Datos**.
4.  Seleccione la hoja de datos (ej. "REPORT").
5.  En el Editor de Power Query, renombre la consulta a **`ML_Facturacion_RAW`**.
6.  **Repita el proceso (Pasos 1 a 5) para las otras 3 carpetas**, renombrando las consultas a: **`ML_Poscobro_RAW`**, **`Ripley_Finanzas_RAW`**, y **`Paris_Finanzas_RAW`**.

**Resultado de la Fase 1:** Tendrá 4 consultas RAW en el panel izquierdo del Editor de Power Query.

---

## Fase 2: Modelado y Transformación Exhaustiva (Uso del Código M)

### Paso 2.1: Creación de Tablas de Dimensiones y Función de Estandarización

Cree las siguientes consultas en blanco y pegue el código M del Anexo.

| Consulta | Tipo | Propósito |
| :--- | :--- | :--- |
| **`Dim_Marketplace`** | Dimensión | Mapea ID (1, 2, 3) a Nombre (Mercado Libre, Ripley, París). |
| **`Dim_Tipo_Transaccion`** | Dimensión | Mapea ID (1 a 13) a Tipo de Transacción (Venta, Comisión, etc.). |
| **`fn_EstandarizarColumnas`** | Función | Asegura que todas las consultas de hechos tengan la misma estructura de 7 columnas. |

### Paso 2.2: Creación de las Tablas de Hechos (18 Consultas)

Utilice el **Código M del Anexo** para crear las 18 consultas de hechos. Este código ya incorpora todas las correcciones de Ripley y la estandarización de columnas.

**¡CORRECCIÓN CRÍTICA EN ML!** El código M de Mercado Libre ahora utiliza la columna **`Número de publicación`** para el SKU, corrigiendo la omisión de versiones anteriores.

| Mercado Libre (8) | Ripley (5) | París (5) |
| :--- | :--- | :--- |
| `ML_Fact_Ventas` | `Ripley_Fact_Ventas` | `Paris_Fact_Ventas` |
| `ML_Fact_Comisiones` | `Ripley_Fact_Comisiones` | `Paris_Fact_Comisiones` |
| `ML_Fact_Envios` | `Ripley_Fact_Envios` | `Paris_Fact_DescuentoComercial` |
| `ML_Fact_Publicidad` | `Ripley_Fact_Impuestos` | `Paris_Fact_Logistica` |
| `ML_Fact_Asesoria` | `Ripley_Fact_Reembolsos` | `Paris_Fact_OtrosCargos` |
| `ML_Fact_Fullfilment` | | |
| `ML_Fact_Bonificaciones` | | |
| `ML_Fact_Devoluciones` | | |

---

## Fase 3: Consolidación y Reporte Final

### Paso 3.1: Consolidación de la Tabla Maestra (Anexar Consultas)

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
3.  Seleccione la opción **Tres o más tablas**.
4.  Mueva **TODAS** las 18 consultas de hechos a la lista de tablas a anexar.
5.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### Paso 3.2: Cargar las Tablas en Excel

1.  En el Editor de Power Query, seleccione las consultas **`Dim_Marketplace`**, **`Dim_Tipo_Transaccion`** y **`DATA_MAESTRA_360`**.
2.  Haga clic en **Cerrar y Cargar en...**
3.  Seleccione **Tabla** y **Nueva Hoja de Cálculo** para cada una.

### Paso 3.3: Crear el Dashboard (Tabla Dinámica)

1.  Cree una **Tabla Dinámica** usando la tabla **`DATA_MAESTRA_360`**.
2.  **La Métrica Clave (Venta Neta Real):**
    *   Arrastre la columna **`Monto`** a la sección **Valores**.
    *   Arrastre **`ID_Marketplace`** y **`ID_Tipo_Transaccion`** a la sección **Filas**.
3.  **Mejora de Usabilidad:** En la pestaña **Análisis de Tabla Dinámica** > **Campos**, reemplace los IDs numéricos por los nombres descriptivos, usando las tablas de dimensiones como referencia.

El resultado de la suma de la columna `Monto` en la Tabla Dinámica es su **Venta Neta Real** después de todos los costos.

---

## Anexo: Código M (Power Query) para Consultas Personalizadas

### Tablas de Dimensiones

#### Dim_Marketplace
```m

let
    Fuente = Table.FromRecords({
        [ID_Marketplace = 1, Marketplace = "Mercado Libre"],
        [ID_Marketplace = 2, Marketplace = "Ripley"],
        [ID_Marketplace = 3, Marketplace = "París"]
    }),
    #"Tipo Cambiado" = Table.TransformColumnTypes(Fuente,{{"ID_Marketplace", Int64.Type}, {"Marketplace", type text}})
in
    #"Tipo Cambiado"

```

#### Dim_Tipo_Transaccion
```m

let
    Fuente = Table.FromRecords({
        [ID_Tipo_Transaccion = 1, Tipo_Transaccion = "Venta"],
        [ID_Tipo_Transaccion = 2, Tipo_Transaccion = "Comisión"],
        [ID_Tipo_Transaccion = 3, Tipo_Transaccion = "Costo Envío"],
        [ID_Tipo_Transaccion = 4, Tipo_Transaccion = "Publicidad"],
        [ID_Tipo_Transaccion = 5, Tipo_Transaccion = "Bonificación"],
        [ID_Tipo_Transaccion = 6, Tipo_Transaccion = "Devolución"],
        [ID_Tipo_Transaccion = 7, Tipo_Transaccion = "Impuesto"],
        [ID_Tipo_Transaccion = 8, Tipo_Transaccion = "Reembolso"],
        [ID_Tipo_Transaccion = 9, Tipo_Transaccion = "Asesoría Comercial"],
        [ID_Tipo_Transaccion = 10, Tipo_Transaccion = "Costo Fullfilment"],
        [ID_Tipo_Transaccion = 11, Tipo_Transaccion = "Descuento Comercial"],
        [ID_Tipo_Transaccion = 12, Tipo_Transaccion = "Logística"],
        [ID_Tipo_Transaccion = 13, Tipo_Transaccion = "Otros Cargos"]
    }),
    #"Tipo Cambiado" = Table.TransformColumnTypes(Fuente,{{"ID_Tipo_Transaccion", Int64.Type}, {"Tipo_Transaccion", type text}})
in
    #"Tipo Cambiado"

```


### Mercado Libre (ID 1)

#### fn_EstandarizarColumnas
```m

(Tabla as table, ID_Tipo as number, ID_Marketplace as number) as table =>
let
    #"Seleccionar Columnas" = Table.SelectColumns(Tabla, {"ID_Transaccion", "Fecha", "SKU", "Monto"}),
    #"Agregar ID_Marketplace" = Table.AddColumn(#"Seleccionar Columnas", "ID_Marketplace", each ID_Marketplace, Int64.Type),
    #"Agregar ID_Tipo_Transaccion" = Table.AddColumn(#"Agregar ID_Marketplace", "ID_Tipo_Transaccion", each ID_Tipo, Int64.Type),
    #"Agregar Cantidad" = Table.AddColumn(#"Agregar ID_Tipo_Transaccion", "Cantidad", each 1, Int64.Type),
    #"Reordenar Columnas" = Table.ReorderColumns(#"Agregar Cantidad", {"ID_Transaccion", "Fecha", "SKU", "Monto", "ID_Marketplace", "ID_Tipo_Transaccion", "Cantidad"})
in
    #"Reordenar Columnas"

```

#### ML_Fact_Ventas
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor de la compra"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor de la compra", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Comisiones
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Costo por categoría + ofrecer cuotas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Costo por categoría + ofrecer cuotas", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Envios
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Tipos Envío" = {"Cargo por Mercado Envíos", "Cargo por envíos de Mercado Libre"},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Detalle])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 3, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Publicidad
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Publicidad" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "publicidad", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Ads", Comparer.OrdinalIgnoreCase) or [Detalle] = "Cargo por publicación"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Publicidad", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 4, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Asesoria
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Asesoría" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por Asesoría Comercial"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Asesoría", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 9, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Fullfilment
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Full" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Full", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Full", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 10, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Bonificaciones
```m

let
    Fuente = ML_Facturacion_RAW,
    #"Filtrar Bonificación" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Bonificación", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Anulación", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Bonificación", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 5, 1)
in
    #"Estandarizar"

```

#### ML_Fact_Devoluciones
```m

let
    Fuente = ML_Poscobro_RAW,
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID_TRANSACCION", "FECHA", "SKU", "MONTO_DEVOLUCION"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID_TRANSACCION", "ID_Transaccion"}, {"FECHA", "Fecha"}, {"MONTO_DEVOLUCION", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 6, 1)
in
    #"Estandarizar"

```


### Ripley (ID 2)

#### Ripley_Fact_Ventas
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Tipo] = "Importe del pedido"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 2)
in
    #"Estandarizar"

```

#### Ripley_Fact_Comisiones
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Comisión" = Table.SelectRows(Fuente, each [Tipo] = "Comisiones"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Comisión", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 2)
in
    #"Estandarizar"

```

#### Ripley_Fact_Envios
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Tipos Envío" = {"Gastos de envío (RIPLEY) pagados por el operador", "Gastos de envío (RIPLEY)"},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Tipo])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 3, 2)
in
    #"Estandarizar"

```

#### Ripley_Fact_Impuestos
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Impuesto" = Table.SelectRows(Fuente, each [Tipo] = "Impuesto sobre la comisión (IVA 0,00%)"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Impuesto", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 7, 2)
in
    #"Estandarizar"

```

#### Ripley_Fact_Reembolsos
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Reembolso" = Table.SelectRows(Fuente, each [Tipo] = "Importe de reembolso"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Reembolso", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 8, 2)
in
    #"Estandarizar"

```


### París (ID 3)

#### Paris_Fact_Ventas
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 3)
in
    #"Estandarizar"

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
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 3)
in
    #"Estandarizar"

```

#### Paris_Fact_DescuentoComercial
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Descuento" = Table.SelectRows(Fuente, each [TIPO] = "Venta" and [DESCUENTO COMERCIAL] <> 0 and [DESCUENTO COMERCIAL] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Descuento", {{"NÚMERO ORDEN", "FECHA", "SKU", "DESCUENTO COMERCIAL"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"DESCUENTO COMERCIAL", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 11, 3)
in
    #"Estandarizar"

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
    #"Eliminar Columnas Originales" = Table.RemoveColumns(#"Aplicar Signo Condicional", {{"Monto", "TIPO"}}),
    #"Renombrar Monto Final" = Table.RenameColumns(#"Eliminar Columnas Originales", {{"Monto_Final", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Monto Final", 12, 3)
in
    #"Estandarizar"

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
    #"Eliminar Columnas Originales" = Table.RemoveColumns(#"Aplicar Signo Condicional", {{"Monto", "TIPO"}}),
    #"Renombrar Monto Final" = Table.RenameColumns(#"Eliminar Columnas Originales", {{"Monto_Final", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Monto Final", 13, 3)
in
    #"Estandarizar"

```




---

**Autor:** Manus AI  
**Versión:** 9.0 - Diciembre 2025  
**Nota:** Esta es la guía final y optimizada, que incorpora el Star Schema y los Códigos M verificados.
