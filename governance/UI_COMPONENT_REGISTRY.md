---
id: UI_COMPONENT_REGISTRY_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: UX/UI Lead & Frontend Architect
ultima_revision: 2026-07-27
dependencias:
  - UI_ARCHITECTURE_MASTERPLAN_V1
---

# REGISTRO CANÓNICO DE COMPONENTES UI V1

## Inventario de Componentes Frontend Reutilizables

| ID Componente | Módulo | Archivo / Plantilla | Función Principal | Estado |
| :--- | :--- | :--- | :--- | :--- |
| `COMP-NAV-BAR` | Navegación | `templates/executive_dashboard.html` | Navegación gerencial entre `/exec`, `/app`, `/copilot` | CERTIFICADO |
| `COMP-KPI-CARD` | Resumen | `templates/executive_dashboard.html` | Tarjeta KPI monetaria con border color coding | CERTIFICADO |
| `COMP-WATERFALL-BAR` | Visualización | `templates/executive_dashboard.html` | Bar waterfall de deducciones por Marketplace | CERTIFICADO |
| `COMP-COPILOT-CHAT` | Copilot | `templates/copilot.html` | Chat UI determinista con 10 botones de sugerencia QF | CERTIFICADO |
| `COMP-FORMATTER-JS` | Shared Script | `frontend/shared/financial-formatter.js` | Formateador canónico monetario (CLP, USD, PCT) | CERTIFICADO |
| `COMP-AUDIT-TABLE` | Auditoría | `templates/dashboard.html` | Tabla de registros ledger con desglose modal | CERTIFICADO |
| `COMP-HEALTH-CARD` | Health | `templates/executive_dashboard.html` | Scorecard de distribución por Marketplace | CERTIFICADO |

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:UI_COMPONENT_REGISTRY_V1` (Tipo: `Registro_Componentes_UI`)

### Execution Graph Nodes
- `ExecNode:COMPONENTS_JS` (Static Script: `static/js/financial-formatter.js`)
