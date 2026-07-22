content = '''# Tareas E01 - E10 (Emergency Hardening)

- [x] Crear el endpoint GET /api/v4/electronic_certification/status/{transaction_id} en pi/api.py (FASE E03.5).
- [x] Eliminar toda lógica falsa (hardcodes, setTimeout, Math.random) del drawer JS en 	emplates/dashboard.html.
- [x] Actualizar el JS en el drawer para consumir GET /api/v4/electronic_certification/status/{transaction_id} al abrirlo.
- [x] Implementar el estado "BLOCKED — BACKEND CONTRACT REQUIRED" visualmente si el backend devuelve 409 o falla (FASE E04).
- [x] Eliminar los textos falsos ("Factura Electrónica 33", "123456", "PENDING", recomendaciones) y reemplazarlos por mapeo al JSON del backend (FASES E05, E06, E07, E08, E09).
- [x] Verificar con Select-String (grep equivalente en PS) que no queden coincidencias de simulaciones en el código (FASE E10).
- [x] Generar artefactos solicitados (ake_code_removed.json, ackend_contract_matrix.json, rontend_render_matrix.json, zero_fake_data_report.json, egression_report.json, emergency_fix_report.md).
'''
with open(r'c:\Users\ASUS Zenbook\.gemini\antigravity-ide\brain\eaf5b8eb-5faa-421a-a378-c671d38ad5bd\task.md', 'w', encoding='utf-8') as f:
    f.write(content)
