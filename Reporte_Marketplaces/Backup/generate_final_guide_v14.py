import re

def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_ripley_publicidad_m_code():
    """Genera el código M para la nueva consulta Ripley_Fact_Publicidad."""
    m_publicidad = """
let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Factura Manual" = Table.SelectRows(Fuente, each [Tipo] = "Factura manual"),
    #"Palabras Clave Publicidad" = {"Google", "Facebook", "Product Ads", "AON", "Cyber"},
    #"Filtrar Publicidad" = Table.SelectRows(#"Filtrar Factura Manual", each List.AnyTrue(List.Transform(#"Palabras Clave Publicidad", each Text.Contains([Descripción], _, Comparer.OrdinalIgnoreCase)))),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Publicidad", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 4, 2)
in
    #"Estandarizar"
"""
    return get_m_code_template("Ripley_Fact_Publicidad", m_publicidad)

def generate_ripley_envios_ajustes_m_code():
    """Genera el código M para la nueva consulta Ripley_Fact_Envios_Ajustes."""
    m_envios_ajustes = """
let
    Fuente = Ripley_Finanzas_RAW,
    #"Filtrar Factura Manual" = Table.SelectRows(Fuente, each [Tipo] = "Factura manual"),
    #"Palabras Clave Envío" = {"Recargo por precio mínimo de producto", "Descuento por costo logístico", "Descuento por logistica inversa", "Descuento por cancelación"},
    #"Filtrar Envío" = Table.SelectRows(#"Filtrar Factura Manual", each List.AnyTrue(List.Transform(#"Palabras Clave Envío", each Text.Contains([Descripción], _, Comparer.OrdinalIgnoreCase)))),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Envío", {{"Número de pedido", "Fecha de creación", "SKU de oferta", "Importe"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"Número de pedido", "ID_Transaccion"}, {"Fecha de creación", "Fecha"}, {"SKU de oferta", "SKU"}, {"Importe", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 3, 2)
in
    #"Estandarizar"
"""
    return get_m_code_template("Ripley_Fact_Envios_Ajustes", m_envios_ajustes)

def update_guide_content(old_guide_path, new_guide_path):
    """Carga el contenido de la guía V13.0, lo actualiza y lo guarda como V14.0."""
    
    # 1. Cargar el contenido de la guía anterior
    with open(old_guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Actualizar la versión y el conteo de consultas (23 -> 25)
    content = content.replace("V13.0", "V14.0")
    content = content.replace("23 Consultas", "25 Consultas")
    content = content.replace("23 consultas", "25 consultas")

    # 3. Insertar las nuevas consultas en la sección de Ripley del Anexo A
    new_publicidad_code = generate_ripley_publicidad_m_code()
    new_envios_ajustes_code = generate_ripley_envios_ajustes_m_code()
    
    # Buscar la sección de Ripley en el Anexo A (justo después de Ripley_Fact_OtrosCargos)
    # Usaremos una expresión regular para encontrar el final de la sección de Ripley
    
    # Patrón para encontrar el final de la sección de Ripley (antes de París)
    # Buscamos el último código M de Ripley (Ripley_Fact_OtrosCargos) y lo insertamos después
    pattern = r"(#### Ripley_Fact_OtrosCargos\n```m\n.*?```\n\n)"
    
    # Reemplazo: el código existente + los dos nuevos códigos
    replacement = r"\1" + new_publicidad_code + new_envios_ajustes_code
    
    # Realizar la inserción
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 4. Guardar el nuevo contenido
    with open(new_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Guía Maestra Definitiva (V14.0) generada en {new_guide_path}")
    return new_guide_path

# La guía anterior se encuentra en /home/ubuntu/Guia_Maestra_Definitiva_V13.0.md
old_path = "/home/ubuntu/Guia_Maestra_Definitiva_V13.0.md"
new_path = "/home/ubuntu/Guia_Maestra_Definitiva_V14.0.md"

# Ejecutar la actualización
update_guide_content(old_path, new_path)
