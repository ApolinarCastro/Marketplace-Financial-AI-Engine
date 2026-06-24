import re

def get_m_code_template(code_name, code_body):
    """Genera el bloque de código M en formato Markdown."""
    return f"""#### {code_name}
```m
{code_body}
```

"""

def generate_auditoria_m_codes():
    """Genera los códigos M de auditoría para los 4 canales."""
    
    # Lógica de exclusión para Mercado Libre (basada en Detalle)
    ml_exclusion_terms = ["Cargo por venta", "Costo por categoría", "Mercado Envíos", "publicidad", "Full", "Asesoría", "Bonificación", "Devolución"]
    ml_code = f"""
let
    Fuente = ML_Facturacion_RAW,
    TerminosConocidos = {str(ml_exclusion_terms).replace("'", '"')},
    // Filtramos para que solo queden los DESCONOCIDOS (los que no contienen NINGÚN término conocido)
    #"Nuevos Cargos Detectados" = Table.SelectRows(Fuente, each not List.AnyTrue(List.Transform(TerminosConocidos, (t) => Text.Contains([Detalle], t, Comparer.OrdinalIgnoreCase)))),
    #"Solo Columnas Relevantes" = Table.SelectColumns(#"Nuevos Cargos Detectados", {{"Fecha del cargo", "Detalle", "Importe"}})
in
    #"Solo Columnas Relevantes"
"""

    # Lógica de exclusión para Ripley (basada en Tipo)
    ripley_exclusion_terms = ["Importe del pedido", "Comisiones", "Gastos de envío", "Impuesto sobre la comisión", "Importe de reembolso", "Abono manual", "Factura manual"]
    ripley_code = f"""
let
    Fuente = Ripley_Finanzas_RAW,
    TerminosConocidos = {str(ripley_exclusion_terms).replace("'", '"')},
    // Filtramos para que solo queden los DESCONOCIDOS (los que no coinciden exactamente con NINGÚN término conocido en la columna Tipo)
    #"Nuevos Cargos Detectados" = Table.SelectRows(Fuente, each not List.Contains(TerminosConocidos, [Tipo])),
    #"Solo Columnas Relevantes" = Table.SelectColumns(#"Nuevos Cargos Detectados", {{"Fecha de creación", "Tipo", "Descripción", "Importe"}})
in
    #"Solo Columnas Relevantes"
"""

    # Lógica de exclusión para París (basada en Tipo)
    paris_exclusion_terms = ["Venta", "Comisión", "Despacho", "Cobro por despacho", "Logística inversa", "Compensación logística", "Cargo", "Cobro por campaña", "Rebate", "Devolución"]
    paris_code = f"""
let
    Fuente = Paris_Finanzas_RAW,
    TerminosConocidos = {str(paris_exclusion_terms).replace("'", '"')},
    // Filtramos para que solo queden los DESCONOCIDOS (los que no coinciden exactamente con NINGÚN término conocido en la columna Tipo)
    #"Nuevos Cargos Detectados" = Table.SelectRows(Fuente, each not List.Contains(TerminosConocidos, [TIPO])),
    #"Solo Columnas Relevantes" = Table.SelectColumns(#"Nuevos Cargos Detectados", {{"FECHA", "TIPO", "MONTO"}})
in
    #"Solo Columnas Relevantes"
"""

    # Lógica de exclusión para Shopify (basada en Tipo de Transacción)
    shopify_exclusion_terms = ["Venta", "Devolución", "Ajuste", "Envío", "Impuesto"]
    shopify_code = f"""
let
    Fuente = Shopify_RAW,
    TerminosConocidos = {str(shopify_exclusion_terms).replace("'", '"')},
    // Filtramos para que solo queden los DESCONOCIDOS (los que no coinciden exactamente con NINGÚN término conocido en la columna Tipo de Transacción)
    #"Nuevos Cargos Detectados" = Table.SelectRows(Fuente, each not List.Contains(TerminosConocidos, [Tipo de Transacción])),
    #"Solo Columnas Relevantes" = Table.SelectColumns(#"Nuevos Cargos Detectados", {{"Fecha", "Tipo de Transacción", "Monto"}})
in
    #"Solo Columnas Relevantes"
"""

    auditoria_codes = (
        get_m_code_template("Auditoria_ML_NuevosCargos", ml_code) +
        get_m_code_template("Auditoria_Ripley_NuevosCargos", ripley_code) +
        get_m_code_template("Auditoria_Paris_NuevosCargos", paris_code) +
        get_m_code_template("Auditoria_Shopify_NuevosCargos", shopify_code)
    )
    
    return auditoria_codes

def update_guide_content(old_guide_path, new_guide_path):
    """Carga el contenido de la guía V14.0, lo actualiza y lo guarda como V15.0."""
    
    # 1. Cargar el contenido de la guía anterior
    with open(old_guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Actualizar la versión
    content = content.replace("V14.0", "V15.0")

    # 3. Crear el nuevo capítulo de Auditoría
    auditoria_chapter = """
## Capítulo 6: Auditoría de Integridad y Detección de Nuevos Cargos

Para asegurar que el reporte nunca quede obsoleto y que detecte automáticamente cualquier nuevo cargo o concepto que los Marketplaces introduzcan, implementaremos un sistema de **Consultas de Limbo o Auditoría**.

Estas consultas capturan todo lo que **NO** ha sido clasificado en las 25 consultas de hechos. Si estas tablas muestran datos, significa que hay un nuevo concepto que debe ser mapeado.

### 6.1. Creación de las Consultas de Auditoría

Se deben crear 4 nuevas consultas, una por cada canal, utilizando la lógica de **exclusión de términos conocidos**.

**Paso a Paso:**

1.  En Power Query, crea una nueva consulta en blanco.
2.  Copia el Código M correspondiente a continuación.
3.  Carga el resultado como una tabla en una hoja de Excel llamada `Auditoria`.

### 6.2. Códigos M de Auditoría

"""
    
    # 4. Insertar el nuevo capítulo y los códigos M
    auditoria_codes = generate_auditoria_m_codes()
    
    # Buscamos el final del Anexo B (Checklist) para insertar el nuevo capítulo
    pattern = r"(## Anexo B: Checklist de Implementación Final.*)"
    
    # Reemplazo: el contenido existente + el nuevo capítulo
    replacement = auditoria_chapter + auditoria_codes + r"\1"
    
    # Realizar la inserción
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 5. Guardar el nuevo contenido
    with open(new_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Guía Maestra Definitiva (V15.0) generada en {new_guide_path}")
    return new_guide_path

# La guía anterior se encuentra en /home/ubuntu/Guia_Maestra_Definitiva_V14.0.md
old_path = "/home/ubuntu/Guia_Maestra_Definitiva_V14.0.md"
new_path = "/home/ubuntu/Guia_Maestra_Definitiva_V15.0.md"

# Ejecutar la actualización
update_guide_content(old_path, new_path)
