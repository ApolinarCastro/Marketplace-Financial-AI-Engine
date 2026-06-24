def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_dim_m_code():
    # Códigos M para las tablas de dimensiones (Actualización para Shopify)
    
    m_dim_marketplace = """
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
        [ID_Tipo_Transaccion = 13, Tipo_Transaccion = "Otros Cargos"],
        [ID_Tipo_Transaccion = 14, Tipo_Transaccion = "Venta Directa (Shopify)"] // NUEVO
    }),
    #"Tipo Cambiado" = Table.TransformColumnTypes(Fuente,{{"ID_Tipo_Transaccion", Int64.Type}, {"Tipo_Transaccion", type text}})
in
    #"Tipo Cambiado"
"""
    
    output = "### Tablas de Dimensiones\n\n"
    output += get_m_code_template("Dim_Marketplace", m_dim_marketplace)
    output += get_m_code_template("Dim_Tipo_Transaccion", m_dim_tipo_transaccion)
    return output

# --- Función de Estandarización (Necesaria para todos los códigos M) ---
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

def generate_ml_m_code():
    base_query = "ML_Facturacion_RAW"
    poscobro_query = "ML_Poscobro_RAW"
    
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

def generate_shopify_m_code():
    base_query = "Shopify_Ventas_RAW"
    
    # --- 1. Shopify_Fact_Ventas (ID 14) ---
    # Usamos ID 14 para diferenciar las ventas directas de las de Marketplace
    m_ventas = """
let
    Fuente = """ + base_query + """,
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID de la venta", "Mes", "Nombre del producto en el momento de la venta", "Ventas brutas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID de la venta", "ID_Transaccion"}, {"Mes", "Fecha"}, {"Nombre del producto en el momento de la venta", "SKU"}, {"Ventas brutas", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 14, 4)
in
    #"Estandarizar"
"""
    
    output = "### Shopify (Nicopoly.cl) (ID 4)\n\n"
    output += get_m_code_template("Shopify_Fact_Ventas", m_ventas)
    return output

def generate_paris_fulfillment_m_code():
    base_query = "Paris_Fulfillment_RAW"
    
    # --- 1. Paris_Fact_Ventas_Fulfillment (ID 1) ---
    # Usamos ID 1 para Venta, ya que es una venta directa al cliente, pero la separamos en la consulta
    m_ventas = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [tipo] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"número orden", "fecha", "sku", "monto"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"número orden", "ID_Transaccion"}, {"fecha", "Fecha"}, {"sku", "SKU"}, {"monto", "Monto"}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Renombrar Columnas", 1, 3) // Mismo ID de Marketplace que París
in
    #"Estandarizar"
"""

    # --- 2. Paris_Fact_Comisiones_Fulfillment (ID 2) ---
    m_comisiones = """
let
    Fuente = """ + base_query + """,
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [tipo] = "Venta"),
    #"Calcular Monto Comisión" = Table.AddColumn(#"Filtrar Venta", "Monto_Comision", each [monto] * [comisión] / 100, type number),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Calcular Monto Comisión", {{"número orden", "fecha", "sku", "Monto_Comision"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"número orden", "ID_Transaccion"}, {"Monto_Comision", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 2, 3)
in
    #"Estandarizar"
"""
    
    output = "### París Fulfillment (Integración)\n\n"
    output += get_m_code_template("Paris_Fact_Ventas_Fulfillment", m_ventas)
    output += get_m_code_template("Paris_Fact_Comisiones_Fulfillment", m_comisiones)
    return output

def generate_resumen_ejecutivo():
    resumen = """
# Resumen Ejecutivo Gerencial: Venta Bruta vs. Ganancia Neta (V11.0)

Este resumen está diseñado para responder directamente a las preguntas gerenciales: **"¿Cuánto vendemos?"** y **"¿Cuánto nos queda?"**.

## 1. La Métrica Clave: Venta Neta (Ganancia Real)

La métrica más importante es la **Venta Neta**, que representa la ganancia real después de restar **TODOS** los costos (comisiones, envíos, publicidad, fullfilment, etc.) de la Venta Bruta.

| Métrica | Fórmula DAX | Interpretación Gerencial |
| :--- | :--- | :--- |
| **Venta Bruta (GMV)** | `Venta Bruta = CALCULATE(SUM('DATA_MAESTRA_360'[Monto]), 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 1 || 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 14)` | **"Cuánto vendemos en total"** (antes de costos). |
| **Ganancia Neta** | `Ganancia Neta = SUM('DATA_MAESTRA_360'[Monto])` | **"Cuánto dinero real va a la caja"** (después de todos los costos). |
| **Margen Neto (%)** | `Margen Neto % = DIVIDE([Ganancia Neta], [Venta Bruta])` | **"Por cada $100 que vendemos, cuánto nos queda"**. |

## 2. Presentación Gerencial (UX/UI Sugerida)

Para que la información sea "entendible por todos los usuarios", se recomienda un dashboard con la siguiente estructura:

### A. Vista de Alto Nivel (KPIs)

*   **KPI 1:** **Ganancia Neta** (Valor total en grande).
*   **KPI 2:** **Margen Neto %** (Valor total en grande).
*   **KPI 3:** **Venta Bruta** (Valor total en grande).

### B. Desglose por Marketplace

*   **Gráfico de Barras:** Muestra la **Ganancia Neta** por cada Marketplace (Mercado Libre, Ripley, París, Shopify).
*   **Segmentador de Datos:** Un botón grande para filtrar por **Marketplace** y otro para **Fecha**.

### C. Estado de Cuenta Detallado (Matriz)

*   **Tabla Matriz:** Replicando la imagen que enviaste, pero con una mejora:
    *   **Filas:** `Marketplace` (Nivel 1) > `Tipo_Transaccion` (Nivel 2).
    *   **Valores:** `[Ganancia Neta]` (Muestra el valor final de cada arista).

**Ejemplo de Interpretación:**

Si el gerente selecciona **Mercado Libre** y ve:
*   **Venta:** $100.000
*   **Comisión:** -$15.000
*   **Envío:** -$5.000
*   **Ganancia Neta:** $80.000

El mensaje es claro: **"Vendimos $100.000, pero después de costos, nos quedan $80.000."**

## 3. Lógica de Integración (Para el Equipo Técnico)

*   **Shopify:** Se incorpora como un nuevo Marketplace (ID 4). Las ventas se clasifican como **Venta Directa (ID 14)** para diferenciarla de las ventas de Marketplace (ID 1).
*   **París Fulfillment:** Se integra en las consultas de París (ID 3), asegurando que las ventas y comisiones de Fulfillment se sumen a las ventas y comisiones totales de París.
"""
    return resumen

def consolidate_m_code_and_create_guide():
    # Generar códigos M
    dim_code = generate_dim_m_code()
    ml_code = generate_ml_m_code()
    ripley_code = generate_ripley_m_code()
    paris_code = generate_paris_m_code()
    shopify_code = generate_shopify_m_code()
    paris_fulfillment_code = generate_paris_fulfillment_m_code()

    m_code_content = f"""## Anexo A: Código M (Power Query) para Consultas Personalizadas

{dim_code}
{ml_code}
{ripley_code}
{paris_code}
{shopify_code}
{paris_fulfillment_code}
"""
    
    # Contenido de la Guía Maestra Definitiva (V10.0) (simplificado para la V11.0)
    guide_content = f"""# Guía Maestra Definitiva PRO: Reporte Gerencial 360° de Marketplaces y Venta Directa (V11.0)

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

### 2.2: Creación de las Tablas de Hechos (21 Consultas)

Utilice el Código M del **Anexo A** para crear las nuevas consultas de hechos de Shopify y París Fulfillment.

| Marketplace | Consultas Adicionales |
| :--- | :--- |
| **Shopify** | `Shopify_Fact_Ventas` |
| **París** | `Paris_Fact_Ventas_Fulfillment`, `Paris_Fact_Comisiones_Fulfillment` |

---

## Capítulo 3: Consolidación y Carga Final

### 3.1: Consolidación de la Tabla Maestra (Anexar Consultas)

Mueva **TODAS** las **21 consultas de hechos** a la lista de tablas a anexar para crear **`DATA_MAESTRA_360`**.

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

{m_code_content}

---

## Anexo B: Checklist de Implementación Final

(Contenido idéntico a la V10.0, con la actualización de 6 carpetas RAW y 21 consultas de hechos)

---

**Autor:** Manus AI  
**Versión:** 11.0 - Diciembre 2025  
**Nota:** Esta es la guía final que integra Marketplaces y Venta Directa, optimizada para la presentación gerencial.
"""
    
    final_guide_path = "/home/ubuntu/Guia_Maestra_Definitiva_V11.0.md"
    with open(final_guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)

    print(f"Guía Maestra Definitiva (V11.0) generada en {final_guide_path}")

    # Generar el resumen ejecutivo
    resumen_ejecutivo = generate_resumen_ejecutivo()
    resumen_path = "/home/ubuntu/Resumen_Ejecutivo_Gerencial.md"
    with open(resumen_path, "w", encoding="utf-8") as f:
        f.write(resumen_ejecutivo)
    
    print(f"Resumen Ejecutivo Gerencial generado en {resumen_path}")

    return final_guide_path, resumen_path

final_guide_path, resumen_path = consolidate_m_code_and_create_guide()
