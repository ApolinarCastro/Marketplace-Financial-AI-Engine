def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_paris_m_code():
    base_query = "Paris_Finanzas_RAW"
    
    # --- 1. Paris_Fact_Ventas (Venta Bruta o GMV) ---
    m_ventas = f"""
let
    Fuente = {base_query},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "París")
in
    #"Agregar Marketplace"
"""

    # --- 2. Paris_Fact_Comisiones (Comisión Calculada) ---
    m_comisiones = f"""
let
    Fuente = {base_query},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [TIPO] = "Venta"),
    #"Calcular Monto Comisión" = Table.AddColumn(#"Filtrar Venta", "Monto_Comision", each [MONTO] * [COMISIÓN] / 100, type number),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Calcular Monto Comisión", {{"NÚMERO ORDEN", "FECHA", "SKU", "Monto_Comision"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"Monto_Comision", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "París")
in
    #"Agregar Marketplace"
"""

    # --- 3. Paris_Fact_DescuentoComercial ---
    m_descuento = f"""
let
    Fuente = {base_query},
    #"Filtrar Descuento" = Table.SelectRows(Fuente, each [TIPO] = "Venta" and [DESCUENTO COMERCIAL] <> 0 and [DESCUENTO COMERCIAL] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Descuento", {{"NÚMERO ORDEN", "FECHA", "SKU", "DESCUENTO COMERCIAL"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"DESCUENTO COMERCIAL", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Descuento Comercial"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "París")
in
    #"Agregar Marketplace"
"""

    # --- 4. Paris_Fact_Logistica (Despacho, Logística Inversa, Compensación) ---
    m_logistica = f"""
let
    Fuente = {base_query},
    #"Tipos Logísticos" = {{"Despacho", "Cobro por despacho", "Logística inversa", "Compensación logística"}},
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
"""

    # --- 5. Paris_Fact_OtrosCargos (Cargo, Cobro por Campaña, Rebate) ---
    m_otros_cargos = f"""
let
    Fuente = {base_query},
    #"Tipos Otros" = {{"Cargo", "Cobro por campaña", "Rebate"}},
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
"""
    
    output = "### París\n\n"
    output += get_m_code_template("Paris_Fact_Ventas", m_ventas)
    output += get_m_code_template("Paris_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("Paris_Fact_DescuentoComercial", m_descuento)
    output += get_m_code_template("Paris_Fact_Logistica", m_logistica)
    output += get_m_code_template("Paris_Fact_OtrosCargos", m_otros_cargos)
    
    with open("/home/ubuntu/paris_m_code.txt", "w", encoding="utf-8") as f:
        f.write(output)

def generate_ml_m_code():
    base_query = "ML_Facturacion_RAW"
    poscobro_query = "ML_Poscobro_RAW"
    
    # --- 1. ML_Fact_Ventas (Venta Bruta o GMV) ---
    m_ventas = f"""
let
    Fuente = {base_query},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor de la compra"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor de la compra", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 2. ML_Fact_Comisiones ---
    m_comisiones = f"""
let
    Fuente = {base_query},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por venta"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de venta", "Fecha del cargo", "Código ML", "Costo por categoría + ofrecer cuotas"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Costo por categoría + ofrecer cuotas", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 3. ML_Fact_Envios ---
    m_envios = f"""
let
    Fuente = {base_query},
    #"Tipos Envío" = {{"Cargo por Mercado Envíos", "Cargo por envíos de Mercado Libre"}},
    #"Filtrar Envío" = Table.SelectRows(Fuente, each List.Contains(#"Tipos Envío", [Detalle])),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Costo Envío"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 4. ML_Fact_Publicidad ---
    m_publicidad = f"""
let
    Fuente = {base_query},
    #"Filtrar Publicidad" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "publicidad", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Ads", Comparer.OrdinalIgnoreCase) or [Detalle] = "Cargo por publicación"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Publicidad", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Publicidad"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 5. ML_Fact_Asesoria ---
    m_asesoria = f"""
let
    Fuente = {base_query},
    #"Filtrar Asesoría" = Table.SelectRows(Fuente, each [Detalle] = "Cargo por Asesoría Comercial"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Asesoría", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Asesoría Comercial"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 6. ML_Fact_Fullfilment ---
    m_fullfilment = f"""
let
    Fuente = {base_query},
    #"Filtrar Full" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Full", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Full", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Costo Fullfilment"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 7. ML_Fact_Bonificaciones ---
    m_bonificaciones = f"""
let
    Fuente = {base_query},
    #"Filtrar Bonificación" = Table.SelectRows(Fuente, each Text.Contains([Detalle], "Bonificación", Comparer.OrdinalIgnoreCase) or Text.Contains([Detalle], "Anulación", Comparer.OrdinalIgnoreCase)),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Bonificación", {{"Número de venta", "Fecha del cargo", "Código ML", "Valor del cargo"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de venta", "ID_Transaccion"}, {"Fecha del cargo", "Fecha"}, {"Código ML", "SKU"}, {"Valor del cargo", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Bonificación"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""

    # --- 8. ML_Fact_Devoluciones (Poscobro) ---
    m_devoluciones = f"""
let
    Fuente = {poscobro_query},
    #"Seleccionar Columnas" = Table.SelectColumns(Fuente, {{"ID_TRANSACCION", "FECHA", "SKU", "MONTO_DEVOLUCION"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"ID_TRANSACCION", "ID_Transaccion"}, {"FECHA", "Fecha"}, {"MONTO_DEVOLUCION", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Devolución"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Mercado Libre")
in
    #"Agregar Marketplace"
"""
    
    output = "### Mercado Libre\n\n"
    output += get_m_code_template("ML_Fact_Ventas", m_ventas)
    output += get_m_code_template("ML_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("ML_Fact_Envios", m_envios)
    output += get_m_code_template("ML_Fact_Publicidad", m_publicidad)
    output += get_m_code_template("ML_Fact_Asesoria", m_asesoria)
    output += get_m_code_template("ML_Fact_Fullfilment", m_fullfilment)
    output += get_m_code_template("ML_Fact_Bonificaciones", m_bonificaciones)
    output += get_m_code_template("ML_Fact_Devoluciones", m_devoluciones)
    
    with open("/home/ubuntu/ml_m_code.txt", "w", encoding="utf-8") as f:
        f.write(output)

def generate_ripley_m_code():
    base_query_pedidos = "Ripley_Pedidos_RAW"
    base_query_ajustes = "Ripley_Ajustes_RAW"

    # --- 1. Ripley_Fact_Ventas ---
    m_ventas = f"""
let
    Fuente = {base_query_pedidos},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Estado] = "Entregado"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each "Venta"),
    #"Agregar Marketplace" = Table.AddColumn(#"Agregar Tipo", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"
"""

    # --- 2. Ripley_Fact_Comisiones ---
    m_comisiones = f"""
let
    Fuente = {base_query_pedidos},
    #"Filtrar Venta" = Table.SelectRows(Fuente, each [Estado] = "Entregado"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Venta", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Comision (sin impuestos)"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Comision (sin impuestos)", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Agregar Tipo" = Table.AddColumn(#"Aplicar Signo", "Tipo_Transaccion", each "Comisión"),
    #"Agregar Marketplace" = Table.AddColumn(#"Aplicar Signo", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"
"""

    # --- 3. Ripley_Fact_Ajustes ---
    m_ajustes = f"""
let
    Fuente = {base_query_ajustes},
    #"Filtrar Ajustes" = Table.SelectRows(Fuente, each [Importe] <> 0 and [Importe] <> null),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Ajustes", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe", "Tipo de Ajuste"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Agregar Tipo" = Table.AddColumn(#"Renombrar Columnas", "Tipo_Transaccion", each [Tipo de Ajuste]),
    #"Eliminar Tipo Original" = Table.RemoveColumns(#"Agregar Tipo", {{"Tipo de Ajuste"}}),
    #"Agregar Marketplace" = Table.AddColumn(#"Eliminar Tipo Original", "Marketplace", each "Ripley")
in
    #"Agregar Marketplace"
"""
    
    output = "### Ripley\n\n"
    output += get_m_code_template("Ripley_Fact_Ventas", m_ventas)
    output += get_m_code_template("Ripley_Fact_Comisiones", m_comisiones)
    output += get_m_code_template("Ripley_Fact_Ajustes", m_ajustes)
    
    with open("/home/ubuntu/ripley_m_code.txt", "w", encoding="utf-8") as f:
        f.write(output)

def consolidate_m_code_and_create_guide():
    # Generar códigos M
    generate_paris_m_code()
    generate_ml_m_code()
    generate_ripley_m_code()

    with open("/home/ubuntu/ml_m_code.txt", "r", encoding="utf-8") as f:
        ml_code = f.read()
    with open("/home/ubuntu/ripley_m_code.txt", "r", encoding="utf-8") as f:
        ripley_code = f.read()
    with open("/home/ubuntu/paris_m_code.txt", "r", encoding="utf-8") as f:
        paris_code = f.read()

    m_code_content = f"""## Anexo: Código M (Power Query) para Consultas Personalizadas

{ml_code}
{ripley_code}
{paris_code}
"""
    
    guide_content = f"""# Guía Definitiva PRO: Reporte Gerencial 360° de Marketplaces con Power Query (Incluye Código M)

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

{m_code_content}

---

**Autor:** Manus AI  
**Versión:** 6.0 - Diciembre 2025  
**Nota:** Esta guía es la versión final, con un flujo continuo, detalle exhaustivo y la inclusión del código M para una implementación rápida y precisa.
"""
    
    final_guide_path = "/home/ubuntu/Guia_Didactica_Marketplaces_Pro_M_Code.md"
    with open(final_guide_path, "w", encoding="utf-8") as f:
        f.write(guide_content)

    print(f"Guía final con código M generada en {final_guide_path}")

# Ejecutar todas las funciones
consolidate_m_code_and_create_guide()
