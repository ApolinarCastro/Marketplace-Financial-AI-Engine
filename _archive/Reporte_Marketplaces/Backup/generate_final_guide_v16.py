import re
import pandas as pd

def update_guide_content(old_guide_path, new_guide_path, audit_findings_path):
    """Carga el contenido de la guía V15.0, lo actualiza con los hallazgos y lo guarda como V16.0."""
    
    # 1. Cargar el contenido de la guía anterior
    with open(old_guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Cargar los hallazgos de auditoría
    with open(audit_findings_path, "r", encoding="utf-8") as f:
        audit_content = f.read()

    # 3. Actualizar la versión
    content = content.replace("V15.0", "V16.0")

    # 4. Insertar los hallazgos de auditoría como una nueva subsección
    # Buscamos el final del Capítulo 6 para insertar los hallazgos
    # El patrón busca el final del capítulo 6, antes del Anexo A
    pattern = r"(## Anexo A: Código M \(Power Query\).*)"
    
    new_section = f"""
### 6.3. Hallazgos del Radar de Auditoría y Propuestas de Mapeo

{audit_content}

"""
    
    # Reemplazo: el contenido existente + el nuevo capítulo
    replacement = new_section + r"\1"
    
    # Realizar la inserción
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 5. Guardar el nuevo contenido
    with open(new_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Guía Maestra Definitiva (V16.0) generada en {new_guide_path}")
    return new_guide_path

# Rutas de los archivos
old_path = "/home/ubuntu/Guia_Maestra_Definitiva_V15.0.md"
new_path = "/home/ubuntu/Guia_Maestra_Definitiva_V16.0.md"
audit_findings_path = "/home/ubuntu/hallazgos_y_propuestas.md"

# Ejecutar la actualización
update_guide_content(old_path, new_path, audit_findings_path)
