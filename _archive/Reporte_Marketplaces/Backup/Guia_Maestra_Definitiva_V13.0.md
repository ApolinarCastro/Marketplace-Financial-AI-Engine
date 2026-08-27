# Guía Maestra Definitiva PRO: Reporte Gerencial 360° de Marketplaces y Venta Directa (V13.0)

**La Guía Final: Integración de Shopify y París Fulfillment, con Enfoque Gerencial**

---

## Capítulo 1: La Preparación y Carga Inicial (Actualización)

### 1.1: Organización de Carpetas (Actualizada)

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Historial Financiero | `Ripley_Finanzas` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |
| **París Fulfillment** | Reporte de Transacciones Fulfillment | `Paris_Fulfillment` | // NUEVO
| **Shopify** | Ventas Brutas por Pedido | `Shopify_Ventas` | // NUEVO

### 1.2: Carga de Datos en el Único Archivo de Excel

**Repita el proceso de carga para las 6 carpetas**, renombrando las consultas RAW:
*   `ML_Facturacion_RAW`
*   `ML_Poscobro_RAW`
*   `Ripley_Finanzas_RAW`
*   `Paris_Finanzas_RAW`
*   **`Paris_Fulfillment_RAW`** (NUEVO)
*   **`Shopify_Ventas_RAW`** (NUEVO)

---

## Capítulo 2: Modelado y Transformación Exhaustiva (Uso del Código M)

### 2.1: Creación de Tablas de Dimensiones (Actualizadas)

Utilice el Código M del **Anexo A** para actualizar `Dim_Marketplace` (ID 4 para Shopify) y `Dim_Tipo_Transaccion` (ID 14 para Venta Directa).

### 2.2: Creación de las Tablas de Hechos (23 Consultas)

Utilice el Código M del **Anexo A** para crear las nuevas consultas de hechos de Shopify y París Fulfillment.

| Marketplace | Consultas Adicionales |
| :--- | :--- |
| **Shopify** | `Shopify_Fact_Ventas` |
| **París** | `Paris_Fact_Ventas_Fulfillment`, `Paris_Fact_Comisiones_Fulfillment`, `Paris_Fact_Devoluciones` |

---

## Capítulo 3: Consolidación y Carga Final

### 3.1: Consolidación de la Tabla Maestra (Anexar Consultas)

Mueva **TODAS** las **23 consultas de hechos** a la lista de tablas a anexar para crear **`DATA_MAESTRA_360`**.

---

## Capítulo 4: Proceso de Actualización y Mantenimiento

(Contenido idéntico a la V10.0)

---

## Capítulo 5: Fórmulas DAX para el Análisis Gerencial

(Contenido idéntico a la V10.0, pero con la fórmula de Venta Bruta actualizada para incluir ID 14)

| Métrica | Fórmula DAX (Actualizada) |
| :--- | :--- |
| **Venta Bruta (GMV)** | `Venta Bruta = CALCULATE(SUM('DATA_MAESTRA_360'[Monto]), 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 1 || 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 14)` |
| **Ganancia Neta** | `Ganancia Neta = SUM('DATA_MAESTRA_360'[Monto])` |

---

## Anexo A: Código M (Power Query) para Consultas Personalizadas

### Tablas de Dimensiones

#### Dim_Marketplace
```m

let
    Fuente = Table.FromRecords({
        [ID_Marketplace = 1, Marketplace = "Mercado Libre"],
        [ID_Marketplace = 2, Marketplace = "Ripley"],
        [ID_Marketplace = 3, Marketplace = "París"],
        [ID_Marketplace = 4, Marketplace = "Shopify (Nicopoly.cl)"] // NUEVO
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
        [ID_Tipo_Transaccion = 13, Tipo_Transaccion = "Otros Cargos"],
        [ID_Tipo_Transaccion = 14, Tipo_Transaccion = "Venta Directa (Shopify)"] // NUEVO
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

#### Ripley_Fact_OtrosCargos
```m

let
    Fuente = Ripley_Finanzas_RAW,
    #"Tipos Otros Cargos" = {"Abono manual"},
    #"Filtrar Otros Cargos" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Otros Cargos", [Tipo])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Otros Cargos", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    // Abono manual es un ingreso, por lo que el signo se mantiene positivo.
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 13, 2)
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

#### Paris_Fact_Devoluciones
```m

let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Devolución" = Table.SelectRows(Fuente, each [TIPO] = "Devolución"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Devolución", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 6, 3)
in
    #"Estandarizar"

```


### Shopify (Nicopoly.cl) (ID 4)

#### Shopify_Fact_Ventas
```m

let
    Fuente = Shopify_Ventas_RAW,
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID de la venta", "Mes", "Nombre del producto en el momento de la venta", "Ventas brutas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID de la venta", "ID_Transaccion"}, {"Mes", "Fecha"}, {"Nombre del producto en el momento de la venta", "SKU"}, {"Ventas brutas", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 14, 4)
in
    #"Estandarizar"

```


### París Fulfillment (Integración)

#### Paris_Fact_Ventas_Fulfillment
```m

let
    Fuente = Paris_Fulfillment_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [tipo] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"número orden", "fecha", "sku", "monto"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"número orden", "ID_Transaccion"}, {"fecha", "Fecha"}, {"sku", "SKU"}, {"monto", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 3) // Mismo ID de Marketplace que París
in
    #"Estandarizar"

```

#### Paris_Fact_Comisiones_Fulfillment
```m

let
    Fuente = Paris_Fulfillment_RAW,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [tipo] = "Venta"),
    #"Calcular Monto Comisión" = Table.AddColumn(#"Filtrar Venta", "Monto_Comision", each [monto] * [comisión] / 100, type number),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Calcular Monto Comisión", {{"número orden", "fecha", "sku", "Monto_Comision"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"número orden", "ID_Transaccion"}, {"Monto_Comision", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 3)
in
    #"Estandarizar"

```




---

## Anexo B: Checklist de Implementación Final

(Contenido idéntico a la V10.0, con la actualización de 6 carpetas RAW y 23 consultas de hechos)

---

**Autor:** Manus AI  
**Versión:** 11.0 - Diciembre 2025  
**Nota:** Esta es la guía final que integra Marketplaces y Venta Directa, optimizada para la presentación gerencial.
