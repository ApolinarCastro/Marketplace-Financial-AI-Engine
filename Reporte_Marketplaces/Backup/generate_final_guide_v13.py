import re

def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_ripley_otros_cargos_m_code():
    """Genera el código M para la nueva consulta Ripley_Fact_OtrosCargos."""
    m_otros_cargos = """
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
"""
    return get_m_code_template("Ripley_Fact_OtrosCargos", m_otros_cargos)

def update_guide_content(old_guide_path, new_guide_path):
    """Carga el contenido de la guía V12.0, lo actualiza y lo guarda como V13.0."""
    
    # 1. Cargar el contenido de la guía anterior
    with open(old_guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Actualizar la versión y el conteo de consultas (22 -> 23)
    content = content.replace("V12.0", "V13.0")
    content = content.replace("22 Consultas", "23 Consultas")
    content = content.replace("22 consultas", "23 consultas")

    # 3. Insertar la nueva consulta en la sección de Ripley del Anexo A
    new_otros_cargos_code = generate_ripley_otros_cargos_m_code()
    
    # Buscar la sección de Ripley en el Anexo A (justo después de Ripley_Fact_Reembolsos)
    # Usaremos una expresión regular para encontrar el final de la sección de Ripley
    
    # Patrón para encontrar el final de la sección de Ripley (antes de París)
    # Buscamos el último código M de Ripley (Ripley_Fact_Reembolsos) y lo insertamos después
    pattern = r"(#### Ripley_Fact_Reembolsos\n```m\n.*?```\n\n)"
    
    # Reemplazo: el código existente + el nuevo código de otros cargos
    replacement = r"\1" + new_otros_cargos_code
    
    # Realizar la inserción
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 4. Guardar el nuevo contenido
    with open(new_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Guía Maestra Definitiva (V13.0) generada en {new_guide_path}")
    return new_guide_path

# La guía anterior se encuentra en /home/ubuntu/Guia_Maestra_Definitiva_V12.0.md
old_path = "/home/ubuntu/Guia_Maestra_Definitiva_V12.0.md"
new_path = "/home/ubuntu/Guia_Maestra_Definitiva_V13.0.md"

# Ejecutar la actualización
update_guide_content(old_path, new_path)
