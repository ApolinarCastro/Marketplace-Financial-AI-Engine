# Criterios de Aceptación Visual

1. **Cero Regresiones Visuales:** El `Documentary Dashboard` existente no debe romperse al agregar la zona de carga XML. El diseño debe fluir naturalmente debajo o al lado de la tabla de GAPs.
2. **Feedback Inmediato:** El Pipeline de validación debe mostrar estados de carga visuales (spinners) mientras la API procesa el XML.
3. **Consistencia de Color (DEC-052):**
   - Verde (#10B981) para `CERTIFIED` y validaciones exitosas.
   - Rojo (#EF4444) para Firmas Inválidas o inconsistencias de IVA.
   - Amarillo (#F59E0B) para `XML_MISSING` o `SETTLEMENT_PENDING`.
4. **Accesibilidad:** Soporte para Drag & Drop visual (borde punteado que cambia al hacer hover con un archivo).
5. **Integración con Obsidian:** El botón "Abrir en Obsidian" debe tener el ícono característico (o similar púrpura) para denotar exportación al Knowledge Base.
