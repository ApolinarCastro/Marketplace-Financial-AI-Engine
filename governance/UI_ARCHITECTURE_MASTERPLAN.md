---
id: UI_ARCHITECTURE_MASTERPLAN_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: UX/UI Lead & Solution Architect
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - ARCHITECTURE_REGISTRY_V1
---

# UI / UX ARCHITECTURE MASTERPLAN V1

## Propósito y Filosofía de Diseño
Establecer la especificación de arquitectura de la interfaz de usuario corporativa del **Marketplace Financial AI Engine**.
Define los 15 módulos visuales obligatorios, la separación estricta frontend/backend mediante servicios REST y el módulo unificado de formateo monetario `financial-formatter.js`.

---

## 1. Los 15 Módulos Visuales Obligatorios

1. **Upload Center**: Carga asistida y drag-and-drop de archivos RAW con validación pre-ingesta SHA-256.
2. **Dashboard Ejecutivo (`/exec`)**: 4 KPI cards con jerarquía gerencial (Ventas -> Devoluciones -> Cobros -> Disponible).
3. **Marketplace Health**: Puntuación de salud financiera y delta $0 por Marketplace.
4. **Ledger Explorer (`/app`)**: Visualización detallada de transacciones de doble entrada con filtros multi-dimensión.
5. **Reconciliación Engine UI**: Comparador tripartito D360 vs Auditor vs Liquidaciones.
6. **XML / DTE Viewer**: Visor de folios SII (33/43/52/61) y matcheo con ledger.
7. **SAP Explorer**: Visor de asientos contables ERP y BAPIs de conciliación.
8. **Banco / Cartola UI**: Conciliación de transferencias TEF contra cierres de disponibilidades.
9. **Financial Waterfall**: Gráfico en cascada interactivo de deducciones por marketplace.
10. **Evidencias & Compliance**: Visor de artefactos JSON de auditoría e imutabilidad hash.
11. **Financial Copilot (`/copilot`)**: Interfaz conversacional determinista con 10 preguntas estratégicas.
12. **Estado del Sistema**: Monitor en tiempo real de servicios API, DuckDB e integridad de DB.
13. **Alertas & Explicabilidad**: Desglose modal de inconsistencias y alertas de riesgo.
14. **Configuración & Conectores**: Gestión de reglas por Marketplace y parámetros del motor.
15. **KnowledgeOS Graph Browser**: Navegador del Grafo Dual (Knowledge + Execution) e índice de documentación.

---

## 2. Principios de Arquitectura Frontend

- **Aesthetics & Premium UI**: Tipografía moderna (Inter/Roboto), paletas tailoreadas HSL, modo oscuro glassmorphism y micro-animaciones CSS.
- **Formateo Único Canónico**: Todos los números y monedas deben pasar exclusivamente por `financial-formatter.js` (`formatCurrency`, `formatPercent`, `formatDelta`).
- **Desacople API**: Interacción backend 100% mediante FastAPI endpoints response models Pydantic v2.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:UI_ARCHITECTURE_MASTERPLAN_V1` (Tipo: `Masterplan_UI_UX`)

### Execution Graph Nodes
- `ExecNode:FINANCIAL_FORMATTER_JS` (Static Script: `static/js/financial-formatter.js`)
