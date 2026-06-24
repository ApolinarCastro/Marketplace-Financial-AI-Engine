import re

def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_paris_devoluciones_m_code():
    """Genera el código M para la consulta Paris_Fact_Devoluciones."""
    m_devoluciones = """
let
    Fuente = Paris_Finanzas_RAW,
    #"Filtrar Devolución" = Table.SelectRows(Fuente, each [TIPO] = "Devolución"),
    #"Seleccionar Columnas" = Table.SelectColumns(#"Filtrar Devolución", {{"NÚMERO ORDEN", "FECHA", "SKU", "MONTO"}}),
    #"Renombrar Columnas" = Table.RenameColumns(#"Seleccionar Columnas", {{"NÚMERO ORDEN", "ID_Transaccion"}, {"MONTO", "Monto"}}),
    #"Aplicar Signo" = Table.TransformColumns(#"Renombrar Columnas", {{"Monto", each -_, type number}}),
    #"Estandarizar" = fn_EstandarizarColumnas(#"Aplicar Signo", 6, 3)
in
    #"Estandarizar"
"""
    return get_m_code_template("Paris_Fact_Devoluciones", m_devoluciones)

def update_guide_content(old_guide_path, new_guide_path):
    """Carga el contenido de la guía V11.0, lo actualiza y lo guarda como V12.0."""
    
    # 1. Cargar el contenido de la guía anterior
    with open(old_guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Actualizar la versión y el conteo de consultas (21 -> 22)
    content = content.replace("V11.0", "V12.0")
    content = content.replace("21 Consultas", "22 Consultas")
    content = content.replace("21 consultas", "22 consultas")

    # 3. Insertar la nueva consulta en la sección de París del Anexo A
    new_devoluciones_code = generate_paris_devoluciones_m_code()
    
    # Buscar la sección de París en el Anexo A (justo después de Paris_Fact_OtrosCargos)
    # Usaremos una expresión regular para encontrar el final de la sección de París
    
    # Patrón para encontrar el final de la sección de París (antes de Shopify)
    # Buscamos el último código M de París (Paris_Fact_OtrosCargos) y lo insertamos después
    pattern = r"(#### Paris_Fact_OtrosCargos\n```m\n.*?```\n\n)"
    
    # Reemplazo: el código existente + el nuevo código de devoluciones
    replacement = r"\1" + new_devoluciones_code
    
    # Realizar la inserción
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 4. Actualizar la tabla de consultas en el Capítulo 2 (21 -> 22)
    # Buscamos la tabla de consultas adicionales y la actualizamos
    
    # Patrón para encontrar la tabla de consultas adicionales
    table_pattern = r"\| Marketplace \| Consultas Adicionales \|\n\| :--- \| :--- \|\n\| \*\*Shopify\*\* \| `Shopify_Fact_Ventas` \|\n\| \*\*París\*\* \| `Paris_Fact_Ventas_Fulfillment`, `Paris_Fact_Comisiones_Fulfillment` \|"
    
    # Reemplazo: Añadir la nueva consulta de devoluciones
    table_replacement = r"| Marketplace | Consultas Adicionales |\n| :--- | :--- |\n| **Shopify** | `Shopify_Fact_Ventas` |\n| **París** | `Paris_Fact_Ventas_Fulfillment`, `Paris_Fact_Comisiones_Fulfillment`, `Paris_Fact_Devoluciones` |"
    
    content = re.sub(table_pattern, table_replacement, content, flags=re.DOTALL)
    
    # 5. Guardar el nuevo contenido
    with open(new_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Guía Maestra Definitiva (V12.0) generada en {new_guide_path}")
    return new_guide_path

# La guía anterior se encuentra en /home/ubuntu/Guia_Maestra_Definitiva_V11.0.md
old_path = "/home/ubuntu/Guia_Maestra_Definitiva_V11.0.md"
new_path = "/home/ubuntu/Guia_Maestra_Definitiva_V12.0.md"

# Ejecutar la actualización
update_guide_content(old_path, new_path)
