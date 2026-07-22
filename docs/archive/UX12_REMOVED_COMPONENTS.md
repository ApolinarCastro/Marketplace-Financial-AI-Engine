# UX12 REMOVED COMPONENTS (PHASE A)

This document tracks the legacy presentation elements disabled and archived during the UX12 Final Cleanup.

| File | Component | Reason Removed | Replacement Component |
| :--- | :--- | :--- | :--- |
| `templates/executive_dashboard.html` | `<section id="hierarchy-kpis">` | Legacy flat hierarchy merged P&L and Cash concepts (Ajustes & Retenciones). | UX12 Additive Section (Domains 1, 2, 3) |
| `templates/executive_dashboard.html` | KPI Cards JS logic (`let ventas`, `let devoluciones`, etc.) | Backend logic replaced by `ux12Data` structure processing. | UX12 DOM Population Logic (`ux12Data.financial_pnl`, etc.) |

All removed logic has been safely commented out (HTML `<!-- -->` and JS `/* */`) to ensure immediate rollback availability without deleting raw code. No database objects, views, or shared API logic have been removed.
