import os
import sys
import re

def verify_dashboard():
    dashboard_path = os.path.join('templates', 'dashboard.html')
    if not os.path.exists(dashboard_path):
        print("ERROR: dashboard.html not found.")
        sys.exit(1)
        
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    errors = []
    
    # 1. Existe contenedor Estructura Financiera
    if 'id="estructura-financiera-panel"' not in content:
        errors.append("Fallo: Contenedor 'Estructura Financiera' no encontrado (id='estructura-financiera-panel').")
        
    # 2. Existe Resultado Neto
    if 'Resultado Neto' not in content:
        errors.append("Fallo: 'Resultado Neto' no encontrado en el DOM.")
        
    # 3. Existe al menos un grupo financiero (Ingresos, Costos Operacionales, etc.)
    groups = ['ingresos', 'costos_operacionales', 'costos_comerciales', 'ajustes']
    found_groups = [g for g in groups if g in content.lower()]
    if not found_groups:
        errors.append("Fallo: No se encontraron grupos financieros fundamentales en el renderizado.")
        
    # 4. Existe al menos un subtotal financiero (fmtCLP)
    if 'fmtCLP' not in content:
        errors.append("Fallo: No se encontraron funciones de subtotal financiero (fmtCLP).")
        
    # 5. Ningún banner reemplaza el panel financiero (verificar que renderCierre no sobreescriba el panel principal con un banner cuando hay datos vacios de cierre pero ledger detectado)
    if 'ESTADO FINANCIERO CERTIFICADO PARCIAL' in content and 'container.innerHTML =' in content:
        # Check if the banner is injected inside the structure container
        # Since we moved it to 'estado-proceso-container', it should be fine.
        # But we must ensure it doesn't replace 'cierre-container' with a banner if !currentDesglose
        match = re.search(r'if \(!currentDesglose \|\| currentDesglose\.length === 0\)\s*\{\s*container\.innerHTML = `[^`]*CERTIFICADO PARCIAL', content, re.IGNORECASE)
        if match:
            errors.append("Fallo: El banner 'Certificado Parcial' sigue reemplazando la Estructura Financiera.")

    UI_PROTECTED_COMPONENTS_EXTENDED = [
        "Estructura Financiera",
        "Resultado Neto",
        "Capa Operacional y Transaccional",
        "Waterfall Operacional",
        "Capa Liquidaci", # Handle accents robustly
        "Waterfall Liquidaci",
        "Capa Tesorer",
        "Cobertura Documental",
        "Ledger Transaccional",
        "Compliance Tributario"
    ]
    
    for component in UI_PROTECTED_COMPONENTS_EXTENDED:
        if component not in content:
            errors.append(f"Fallo: Componente protegido '{component}' no encontrado en el DOM.")

    if errors:
        print("REGRESSION GUARD FAILED - DESPLIEGUE BLOQUEADO")
        for e in errors:
            print(" -", e)
        sys.exit(1)
        
    print("REGRESSION GUARD PASSED - UI COMPLIANT")
    sys.exit(0)

if __name__ == '__main__':
    verify_dashboard()
