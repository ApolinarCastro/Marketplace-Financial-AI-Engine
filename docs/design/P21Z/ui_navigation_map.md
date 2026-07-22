# Mapa de Navegación UI (P21Z)

## Estructura Principal (Sidebar / Header)
1. **Executive Dashboard** (`/app`) - Visión Financiera Macro
2. **Documentary Dashboard** (`/app/documentary`) - Visión Documental y Certificación Electrónica
   - 2.1 Resumen Ejecutivo de Certificación
   - 2.2 Explorador de Documentos (GAPs y Match)
   - 2.3 **[NUEVO]** Validador de Certificación Electrónica (Drag & Drop XML)
3. **Knowledge Base** (`/app/knowledge`) - Obsidian Adapter

## Jerarquía de la Vista de Certificación
- **Nivel 1:** Resumen de Salud (Cobertura Documental Total vs GAPs)
- **Nivel 2:** Tabla de Gaps accionables (`DocumentGapEngine`)
- **Nivel 3:** Modal/Panel Lateral de Inspección de Evidencia (`EvidenceEngine`)
  - Permite ver el `Evidence Hash`, `Chain Type`, `Marketplace`.
- **Nivel 4:** Acción de Certificación Electrónica en crudo (Carga de XML y pipeline de validación).
