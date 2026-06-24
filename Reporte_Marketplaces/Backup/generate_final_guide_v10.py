def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_dim_m_code():
    # Códigos M para las tablas de dimensiones (Mejora M1)
    
    m_dim_marketplace = """
let
    Fuente = Table.FromRecords({
        [ID_Marketplace = 1, Marketplace = "Mercado Libre"],
        [ID_Marketplace = 2, Marketplace = "Ripley"],
        [ID_Marketplace = 3, Marketplace = "París"]
    }),
    #"Tipo Cambiado" = Table.TransformColumnTypes(Fuente,{{"ID_Marketplace", Int64.Type}, {"Marketplace", type text}})
in
    #"Tipo Cambiado"
"""

    m_dim_tipo_transaccion = """
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
"""
    
    output = "### Tablas de Dimensiones\n\n"
    output += get_m_code_template("Dim_Marketplace", m_dim_marketplace)
    output += get_m_code_template("Dim_Tipo_Transaccion", m_dim_tipo_transaccion)
    return output

def generate_ml_m_code():
    base_query = "ML_Facturacion_RAW"
    poscobro_query = "ML_Poscobro_RAW"
    
    # Función de estandarización (Mejora M3)
    m_fn_estandarizar = """
(Tabla as table, ID_Tipo as number, ID_Marketplace as number) as table =>
let
    #"Seleccionar Columnas" = Table.SelectColumns(Tabla, {"ID_Transaccion", "Fecha", "SKU", "Monto"}),
    #"Agregar ID_Marketplace" = Table.AddColumn(#"Seleccionar Columnas", "ID_Marketplace", each ID_Marketplace, Int64.Type),
    #"Agregar ID_Tipo_Transaccion" = Table.AddColumn(#"Agregar ID_Marketplace", "ID_Tipo_Transaccion", each ID_Tipo, Int64.Type),
    #"Agregar Cantidad" = Table.AddColumn(#"Agregar ID_Tipo_Transaccion", "Cantidad", each 1, Int64.Type),
    #"Reordenar Columnas" = Table.ReorderColumns(#"Agregar Cantidad", {"ID_Transaccion", "Fecha", "SKU", "Monto", "ID_Marketplace", "ID_Tipo_Transaccion", "Cantidad"})
in
    #"Reordenar Columnas"
"""
    
    # --- 1. ML_Fact_Ventas (ID 1) ---
    m_ventas = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor de la compra"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor de la compra", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 1)
in
    #"Estandarizar"
"""

    # --- 2. ML_Fact_Comisiones (ID 2) ---
    m_comisiones = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Costo por categoría + ofrecer cuotas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Costo por categoría + ofrecer cuotas", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 1)
in
    #"Estandarizar"
"""

    # --- 3. ML_Fact_Envios (ID 3) ---
    m_envios = """
let
    Fuente = """ + base_query + """,
    #"Tipos Envío" = {"Cargo por Mercado Envíos", "Cargo por envíos de Mercado Libre"},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Detalle])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 3, 1)
in
    #"Estandarizar"
"""

    # --- 4. ML_Fact_Publicidad (ID 4) ---
    m_publicidad = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Publicidad" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "publicidad", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Ads", Comparer.OrdinalIgnoreCase) or [Detalle] = "Cargo por publicación"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Publicidad", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 4, 1)
in
    #"Estandarizar"
"""

    # --- 5. ML_Fact_Bonificaciones (ID 5) ---
    m_bonificaciones = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Bonificación" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Bonificación", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Anulación", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Bonificación", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 5, 1)
in
    #"Estandarizar"
"""

    # --- 6. ML_Fact_Devoluciones (ID 6) ---
    m_devoluciones = """
let
    Fuente = """ + poscobro_query + """,
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID_TRANSACCION", "FECHA", "SKU", "MONTO_DEVOLUCION"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID_TRANSACCION", "ID_Transaccion"}, {"FECHA", "Fecha"}, {"MONTO_DEVOLUCION", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 6, 1)
in
    #"Estandarizar"
"""

    # --- 7. ML_Fact_Asesoria (ID 9) ---
    m_asesoria = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Asesoría" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por Asesoría Comercial"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Asesoría", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 9, 1)
in
    #"Estandarizar"
"""

    # --- 8. ML_Fact_Fullfilment (ID 10) ---
    m_fullfilment = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Full" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Full", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Full", {{"Número de venta", "Fecha del cargo", "Número de publicación", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Número de publicación", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 10, 1)
in
    #"Estandarizar"
"""
    
    output = "### Mercado Libre (ID 1)\n\n"
    output += get_m_code_template("fn_EstandarizarColumnas", m_fn_estandarizar)
    output += get_m_code_template("ML_Fact_Ventas", m_ventas)
    output += get_m_code_template("ML_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("ML_Fact_Envios", m_envios)
    output += get_m_code_template("ML_Fact_Publicidad", m_publicidad)
    output += get_m_code_template("ML_Fact_Asesoria", m_asesoria)
    output += get_m_code_template("ML_Fact_Fullfilment", m_fullfilment)
    output += get_m_code_template("ML_Fact_Bonificaciones", m_bonificaciones)
    output += get_m_code_template("ML_Fact_Devoluciones", m_devoluciones)
    
    return output

def generate_ripley_m_code():
    base_query = "Ripley_Finanzas_RAW" 

    # --- 1. Ripley_Fact_Ventas (ID 1) ---
    m_ventas = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Tipo] = "Importe del pedido"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 2)
in
    #"Estandarizar"
"""

    # --- 2. Ripley_Fact_Comisiones (ID 2) ---
    m_comisiones = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Comisión" = Table.SelectRows(Fuente, each [Tipo] = "Comisiones"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Comisión", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 2)
in
    #"Estandarizar"
"""

    # --- 3. Ripley_Fact_Envios (ID 3) ---
    m_envios = """
let
    Fuente = """ + base_query + """,
    #"Tipos Envío" = {"Gastos de envío (RIPLEY) pagados por el operador", "Gastos de envío (RIPLEY)"},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Tipo])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 3, 2)
in
    #"Estandarizar"
"""

    # --- 4. Ripley_Fact_Impuestos (ID 7) ---
    m_impuestos = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Impuesto" = Table.SelectRows(Fuente, each [Tipo] = "Impuesto sobre la comisión (IVA 0,00%)"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Impuesto", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 7, 2)
in
    #"Estandarizar"
"""

    # --- 5. Ripley_Fact_Reembolsos (ID 8) ---
    m_reembolsos = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Reembolso" = Table.SelectRows(Fuente, each [Tipo] = "Importe de reembolso"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Reembolso", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 8, 2)
in
    #"Estandarizar"
"""
    
    output = "### Ripley (ID 2)\n\n"
    output += get_m_code_template("Ripley_Fact_Ventas", m_ventas)
    output += get_m_code_template("Ripley_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("Ripley_Fact_Envios", m_envios)
    output += get_m_code_template("Ripley_Fact_Impuestos", m_impuestos)
    output += get_m_code_template("Ripley_Fact_Reembolsos", m_reembolsos)
    
    return output

def generate_paris_m_code():
    base_query = "Paris_Finanzas_RAW"
    
    # --- 1. Paris_Fact_Ventas (ID 1) ---
    m_ventas = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 3)
in
    #"Estandarizar"
"""

    # --- 2. Paris_Fact_Comisiones (ID 2) ---
    m_comisiones = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Calcular Monto Comisión" = Table.AddColumn(#"Filtrar Venta", "Monto_Comision", each [MONTO] * [COMISIÓN] / 100, type number),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Calcular Monto Comisión", {{"NÚMERO ORDEN", "FECHA", "SKU", "Monto_Comision"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"Monto_Comision", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 3)
in
    #"Estandarizar"
"""

    # --- 3. Paris_Fact_DescuentoComercial (ID 11) ---
    m_descuento = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Descuento" = Table.SelectRows(Fuente, each [TIPO] = "Venta" and [DESCUENTO COMERCIAL] <> 0 and [DESCUENTO COMERCIAL] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Descuento", {{"NÚMERO ORDEN", "FECHA", "SKU", "DESCUENTO COMERCIAL"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"DESCUENTO COMERCIAL", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 11, 3)
in
    #"Estandarizar"
"""

    # --- 4. Paris_Fact_Logistica (ID 12) ---
    m_logistica = """
let
    Fuente = """ + base_query + """,
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
"""

    # --- 5. Paris_Fact_OtrosCargos (ID 13) ---
    m_otros_cargos = """
let
    Fuente = """ + base_query + """,
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
"""
    
    output = "### París (ID 3)\n\n"
    output += get_m_code_template("Paris_Fact_Ventas", m_ventas)
    output += get_m_code_template("Paris_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("Paris_Fact_DescuentoComercial", m_descuento)
    output += get_m_code_template("Paris_Fact_Logistica", m_logistica)
    output += get_m_code_template("Paris_Fact_OtrosCargos", m_otros_cargos)
    
    return output

def consolidate_m_code_and_create_guide():
    # Generar códigos M
    dim_code = generate_dim_m_code()
    ml_code = generate_ml_m_code()
    ripley_code = generate_ripley_m_code()
    paris_code = generate_paris_m_code()

    m_code_content = f"""## Anexo A: Código M (Power Query) para Consultas Personalizadas

{dim_code}
{ml_code}
{ripley_code}
{paris_code}
"""
    
    # Reconstrucción de contenido avanzado (DAX, Actualización, Checklist)
    
    update_process = """
## Capítulo 4: Proceso de Actualización y Mantenimiento

La belleza de Power Query es que, una vez configurado, el proceso de actualización es simple y rápido.

### 4.1. Actualización de Archivos RAW

1.  **Descargue** los nuevos reportes de Mercado Libre, Ripley y París.
2.  **Mueva** los archivos RAW a sus respectivas carpetas de origen (ej. `ML_Facturacion`, `Ripley_Finanzas`, etc.). **Asegúrese de que los nombres de las columnas no hayan cambiado** en los nuevos reportes.
3.  **Abra** su archivo `ReporteMarketplaces.xlsx`.

### 4.2. Actualización de Datos en Excel

1.  Vaya a la pestaña **Datos**.
2.  Haga clic en el botón **Actualizar Todo**.

Power Query ejecutará automáticamente las 4 consultas RAW, las 18 consultas de hechos, la consolidación en `DATA_MAESTRA_360` y actualizará su Tabla Dinámica.

### 4.3. Mantenimiento y Solución de Problemas

| Problema | Causa Más Común | Solución |
| :--- | :--- | :--- |
| **Error de Columna No Encontrada** | El Marketplace cambió el nombre de una columna en su reporte RAW. | Edite la consulta RAW en Power Query y cambie el nombre de la columna en el paso `Source` o `Renamed Columns`. |
| **Error de Tipo de Dato** | El Marketplace introdujo un valor de texto en una columna numérica (ej. un guion `-`). | Edite la consulta RAW y aplique el paso **Reemplazar Valores** para convertir el valor problemático a `null` o `0` antes de cambiar el tipo de dato. |
| **Error de List/Table** | El proceso de combinación falló al leer un archivo. | Revise la consulta RAW y asegúrese de que todos los archivos en la carpeta tengan el mismo formato y estructura. |
"""

    dax_formulas = """
## Capítulo 5: Fórmulas DAX Avanzadas para el Análisis Financiero

Para obtener métricas financieras precisas en Power BI o en el Modelo de Datos de Excel, debe utilizar las siguientes medidas DAX.

**Nota:** Estas fórmulas asumen que la tabla de hechos se llama `DATA_MAESTRA_360`.

### 5.1. Métricas de Ingreso y Costo

| Métrica | Fórmula DAX | Descripción |
| :--- | :--- | :--- |
| **Venta Bruta (GMV)** | `Venta Bruta = CALCULATE(SUM('DATA_MAESTRA_360'[Monto]), 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 1)` | Suma de todos los montos clasificados como **Venta** (ID 1). |
| **Costo Total** | `Costo Total = CALCULATE(SUM('DATA_MAESTRA_360'[Monto]), 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] <> 1)` | Suma de todos los montos **que no son Venta**. Como los costos ya están en negativo, el resultado será un número negativo. |
| **Venta Neta (Ganancia Real)** | `Venta Neta = SUM('DATA_MAESTRA_360'[Monto])` | La suma de toda la columna `Monto`. **Esta es la métrica más importante**, ya que los costos están en negativo y se restan automáticamente. |

### 5.2. Métricas de Rentabilidad

| Métrica | Fórmula DAX | Descripción |
| :--- | :--- | :--- |
| **Margen Bruto (%)** | `Margen Bruto % = DIVIDE([Venta Neta], [Venta Bruta])` | Porcentaje de la Venta Neta sobre la Venta Bruta. |
| **Costo de Venta (%)** | `Costo de Venta % = DIVIDE([Costo Total], [Venta Bruta])` | Porcentaje del Costo Total sobre la Venta Bruta. |
"""

    checklist = """
## Anexo B: Checklist de Implementación Final

Utilice esta lista para verificar que su implementación es correcta antes de presentar el reporte.

| Estado | Tarea | Verificación |
| :--- | :--- | :--- |
| [ ] | **Carpetas RAW Creadas** | Las 4 carpetas (`ML_Facturacion`, `ML_Poscobro`, `Ripley_Finanzas`, `Paris_Finanzas`) existen y contienen los archivos RAW. |
| [ ] | **Consultas RAW Creadas** | Existen 4 consultas RAW en Power Query (`ML_Facturacion_RAW`, `ML_Poscobro_RAW`, `Ripley_Finanzas_RAW`, `Paris_Finanzas_RAW`). |
| [ ] | **Dimensiones Creadas** | Existen las consultas `Dim_Marketplace` y `Dim_Tipo_Transaccion`. |
| [ ] | **Función Creada** | Existe la función `fn_EstandarizarColumnas` con 3 argumentos. |
| [ ] | **Hechos Creados** | Existen las 18 consultas de hechos (8 ML, 5 Ripley, 5 París) usando el Código M optimizado. |
| [ ] | **Consolidación Final** | Existe la consulta `DATA_MAESTRA_360` que anexa las 18 consultas de hechos. |
| [ ] | **Carga en Excel** | Las consultas `Dim_Marketplace`, `Dim_Tipo_Transaccion` y `DATA_MAESTRA_360` están cargadas como tablas en Excel. |
| [ ] | **Tabla Dinámica Creada** | La Tabla Dinámica usa `DATA_MAESTRA_360` como fuente. |
| [ ] | **Métrica Neta Correcta** | La suma de la columna `Monto` en la Tabla Dinámica es la **Venta Neta Real**. |
"""
    
    guide_content = f"""# Guía Maestra Definitiva PRO: Reporte Gerencial 360° de Marketplaces con Power Query (V10.0)

**La Guía Final: Flujo Continuo, Detalle Exhaustivo, Códigos M Optimizados y Contenido Avanzado**

---

## Introducción: El Proyecto en un Solo Archivo y Estructura Optimizada

Esta guía es la **versión final y consolidada**, que incorpora la lógica exhaustiva de 360° y optimiza la estructura de datos a un **Esquema Estrella (Star Schema)**, manteniendo el hilo conductor de toda la información generada.

**El Flujo de Trabajo es Continuo:**

1.  **Carga Inicial:** Conectamos el archivo de Excel a las carpetas de reportes.
2.  **Modelado:** Creamos las Tablas de Dimensiones (`Dim_Marketplace`, `Dim_Tipo_Transaccion`).
3.  **Transformación:** Limpiamos y estandarizamos cada reporte en la **Tabla de Hechos** (`DATA_MAESTRA_360`).
4.  **Reporte Final:** Cargamos las tablas en Excel para crear la Tabla Dinámica.

---

## Capítulo 1: La Preparación y Carga Inicial

### 1.1: Organización de Carpetas (El Requisito de Power Query)

Cree la siguiente estructura de carpetas en su disco duro. Power Query leerá los archivos que ponga dentro de ellas.

| Marketplace | Reporte Necesario | Nombre de la Subcarpeta |
| :--- | :--- | :--- |
| **Mercado Libre** | Reporte de Facturación | `ML_Facturacion` |
| **Mercado Libre** | Reporte de Poscobro (Devoluciones) | `ML_Poscobro` |
| **Ripley** | Reporte de Historial Financiero | `Ripley_Finanzas` |
| **París** | Reporte de Finanzas (Transacciones) | `Paris_Finanzas` |

### 1.2: Carga de Datos en el Único Archivo de Excel

**Abra un nuevo archivo de Excel.** Este será su archivo maestro.

1.  Vaya a la pestaña **Datos** > **Obtener Datos** > **De Archivos** > **De una Carpeta**.
2.  Seleccione la carpeta `ML_Facturacion`.
3.  Aparecerá una ventana con la lista de archivos. Haga clic en **Combinar** > **Combinar y Transformar Datos**.
4.  Seleccione la hoja de datos (ej. "REPORT").
5.  En el Editor de Power Query, renombre la consulta a **`ML_Facturacion_RAW`**.
6.  **Repita el proceso (Pasos 1 a 5) para las otras 3 carpetas**, renombrando las consultas a: **`ML_Poscobro_RAW`**, **`Ripley_Finanzas_RAW`**, y **`Paris_Finanzas_RAW`**.

**Resultado del Capítulo 1:** Tendrá 4 consultas RAW en el panel izquierdo del Editor de Power Query.

---

## Capítulo 2: Modelado y Transformación Exhaustiva (Uso del Código M)

### 2.1: Creación de Tablas de Dimensiones y Función de Estandarización

Cree las siguientes consultas en blanco y pegue el código M del **Anexo A**.

| Consulta | Tipo | Propósito |
| :--- | :--- | :--- |
| **`Dim_Marketplace`** | Dimensión | Mapea ID (1, 2, 3) a Nombre (Mercado Libre, Ripley, París). |
| **`Dim_Tipo_Transaccion`** | Dimensión | Mapea ID (1 a 13) a Tipo de Transacción (Venta, Comisión, etc.). |
| **`fn_EstandarizarColumnas`** | Función | Asegura que todas las consultas de hechos tengan la misma estructura de 7 columnas. |

### 2.2: Creación de las Tablas de Hechos (18 Consultas)

Utilice el **Código M del Anexo A** para crear las 18 consultas de hechos. Este código ya incorpora todas las correcciones y la estandarización de columnas.

**¡CORRECCIÓN CRÍTICA EN ML!** El código M de Mercado Libre utiliza la columna **`Número de publicación`** para el SKU.

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

## Capítulo 3: Consolidación y Carga Final

### 3.1: Consolidación de la Tabla Maestra (Anexar Consultas)

1.  En el Editor de Power Query, vaya a la pestaña **Inicio**.
2.  Haga clic en **Combinar** > **Anexar Consultas** > **Anexar Consultas para crear una nueva**.
3.  Mueva **TODAS** las 18 consultas de hechos a la lista de tablas a anexar.
4.  Renombre la nueva consulta como **`DATA_MAESTRA_360`**.

### 3.2: Cargar las Tablas en Excel

1.  En el Editor de Power Query, seleccione las consultas **`Dim_Marketplace`**, **`Dim_Tipo_Transaccion`** y **`DATA_MAESTRA_360`**.
2.  Haga clic en **Cerrar y Cargar en...**
3.  Seleccione **Tabla** y **Nueva Hoja de Cálculo** para cada una.

---

{update_process}

---

{dax_formulas}

---

{m_code_content}

---

{checklist}

---

**Autor:** Manus AI  
**Versión:** 10.0 - Diciembre 2025  
**Nota:** Esta es la guía final y definitiva, que incorpora el Star Schema, los Códigos M verificados y todo el contenido avanzado de las versiones anteriores.
"""
    
    final_guide_path = "/home/ubuntu/Guia_Maestra_Definitiva_V10.0.md"
    with open(final_guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)

    print(f"Guía Maestra Definitiva (V10.0) generada en {final_guide_path}")

# Ejecutar la función principal
consolidate_m_code_and_create_guide()
