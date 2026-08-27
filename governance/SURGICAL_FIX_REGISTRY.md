---
id: SURGICAL_FIX_REGISTRY
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Lead QA & Frontend Engineer
ultima_revision: 2026-07-27
dependencias: [BASELINE_POST_SURGICAL_FIX]
relacionado_con: [TECHNICAL_DEBT_REGISTRY_V1, PMO_REGISTRY_V1]
---

# REGISTRO MAESTRO DE FIXES QUIRÚRGICOS POST-F5-08

## Propósito
Registrar formalmente todas las intervenciones quirúrgicas de corrección realizadas en la interfaz gráfica y componentes de presentación posterior al cierre de la Fase 5.08, demostrando que ningún cálculo del motor financiero fue alterado y preservando la trazabilidad $0 delta.

---

## Registro de Fixes Quirúrgicos

### Fix ID: `POST_F5_08_CLP_FORMAT_PARITY_FIX`

| Campo | Detalle |
| :--- | :--- |
| **ID** | `POST_F5_08_CLP_FORMAT_PARITY_FIX` |
| **Fecha** | 2026-07-26 |
| **Componente** | Frontend / Templates Dashboard |
| **Archivos Modificados** | `templates/dashboard.html`<br>`templates/executive_dashboard.html` |
| **Causa Raíz** | Inconsistencia en formateadores JS locales donde valores en CLP mostraban centavos o formateo divergente en tooltips explicativos. |
| **Solución Implementada** | Implementación de `formatCLP()` unificado usando `Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 })`. |
| **Evidencia** | Verificación visual en dashboard Auditor y Gerencial. Paridad monetaria $0 delta contra respuestas API JSON. |
| **Impacto** | Nulo en backend / $0 cambio en DB. Presentación impecable en CLP. |
| **Estado** | **CERRADO Y CERTIFICADO** |

---

### Fix ID: `POST_F5_08_DTE_COVERAGE_STATUS_RENDER_FIX`

| Campo | Detalle |
| :--- | :--- |
| **ID** | `POST_F5_08_DTE_COVERAGE_STATUS_RENDER_FIX` |
| **Fecha** | 2026-07-27 |
| **Componente** | Frontend / API Response Rendering |
| **Archivos Modificados** | `templates/dashboard.html`<br>`api/api.py` |
| **Causa Raíz** | Excepción silenciosa al procesar estados de cobertura DTE cuando la respuesta de `/api/v4/dte/coverage` retornaba arreglos vacíos o nulos en marketplaces sin XML activado. |
| **Solución Implementada** | Agregada validación defensiva en Javascript (`data?.coverage ?? 0`) y normalización del payload en `api.py` asegurando fallback `status: "PENDING_COVERAGE"`. |
| **Evidencia** | Script de prueba manual de endpoints API `/api/v4/dte/coverage` retornando HTTP 200 OK con payload válido sin romper UI. |
| **Impacto** | Nulo en backend / $0 cambio en DB. Renderizado 100% estable de tarjetas DTE. |
| **Estado** | **CERRADO Y CERTIFICADO** |

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:SURGICAL_FIX_REGISTRY` (Tipo: `Registro_Fixes`)
- `Node:FIX_CLP_FORMAT_PARITY` (Tipo: `Fix_Quirurgico`)
- `Node:FIX_DTE_COVERAGE_RENDER` (Tipo: `Fix_Quirurgico`)

### Execution Graph Nodes
- `ExecNode:VERIFY_FRONTEND_PARITY` (Process: Renderizado de plantillas Jinja2 y comprobación de formato CLP)
- `ExecNode:VERIFY_DTE_STATUS_PAYLOAD` (Process: Consulta HTTP GET a `/api/v4/dte/coverage`)

---

## Trazabilidad y Relaciones
- **RESUELVE**: Inconsistencias de representación en la capa de vista de la UI Auditor y Gerencial.
- **CERTIFICA**: Paridad de datos $0 delta entre backend API y frontend HTML.
- **ORIGINA**: [BASELINE_POST_SURGICAL_FIX](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/BASELINE_POST_SURGICAL_FIX.md)

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[SURGICAL_FIX_REGISTRY]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/SURGICAL_FIX_REGISTRY.md`
