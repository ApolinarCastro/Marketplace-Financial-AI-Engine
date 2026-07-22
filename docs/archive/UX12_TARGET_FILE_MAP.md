# UX12 TARGET FILE MAP (STEP 1 INVENTORY)

This document provides the inventory of the endpoints and templates involved in the UX12 Semantic Truth Redesign.

## 1. Executive KPI Endpoints
*   **Path:** `api/api.py` (Endpoint: `/api/v4/exec/summary`)
*   **Responsibility:** Supplies the data for the main top-level KPI cards (Gross Revenue, Net Revenue, Returns, Cobros, Alerts).
*   **Data Consumed:** `marketplace_cierre_financiero_v1` (for totals), `marketplace_ledger_v1` (filtered for returns/operational items).
*   **Risk Level:** **HIGH** - Modifying this requires ensuring new domains (Cash vs P&L) perfectly match legacy numbers without double-counting.

## 2. Financial Waterfall Endpoints
*   **Path:** `api/api.py` (Endpoint: `/api/v4/exec/waterfall`)
*   **Responsibility:** Provides the categorized data points for the main waterfall visualization (Ingresos, Devoluciones, Costos Operacionales, Costos Comerciales, Ajustes, RN).
*   **Data Consumed:** `marketplace_ledger_v1` grouped by `financial_group` where `include_in_operational_pnl = 1`.
*   **Risk Level:** **HIGH** - The "Ajustes" bucket must be disassembled to separate Cash from P&L and Operational Intelligence without breaking the $0 Delta rule.

## 3. Dashboard API Endpoints (Breakdowns & Detail)
*   **Path:** `api/api.py` (Endpoints: `/api/v4/exec/cobros-breakdown`, `/api/v4/cierre/desglose`)
*   **Responsibility:** Feeds matrices and detailed breakdowns of costs and categories per marketplace.
*   **Data Consumed:** `marketplace_ledger_v1` mapped to specific concepts via `_map_detalle_to_concept()`.
*   **Risk Level:** **MEDIUM** - We will need to map or route specific `financial_group` or `concept` strings into their correct new UI domains (e.g., Chargebacks -> Operational & Financial partition).

## 4. Executive Templates
*   **Path:** `templates/executive_dashboard.html` (Served by `/exec`)
*   **Responsibility:** The primary UI structure for the C-level and finance teams.
*   **Data Consumed:** Executive summary API, Waterfall API, Cobros breakdown API.
*   **Risk Level:** **HIGH** - Requires heavy HTML/JS DOM restructuring to introduce the new tab/toggle (P&L vs Cash Flow) and the new Operational Intelligence section without breaking existing layout grids.

## 5. Dashboard Templates (Detailed View)
*   **Path:** `templates/dashboard.html` (Served by `/` and `/app`)
*   **Responsibility:** The technical detailed ledger and audit operations view.
*   **Data Consumed:** `/api/v4/ledger`, `/api/v4/cierre`, `/api/v4/auditoria`.
*   **Risk Level:** **LOW** - The detailed view already represents raw truth. We only need minor terminology alignment to match UX12, but the structural redesign is focused heavily on the Executive template.

## Summary of Planned Non-Destructive Interventions:
- In `api/api.py`, we will add new parameters or wrapper structures to `/api/v4/exec/summary` and `/api/v4/exec/waterfall` to return `financial_pnl`, `cash_flow`, and `operational_intelligence` arrays.
- In `templates/executive_dashboard.html`, we will **add** the DOM elements for the new tabs and cards, preserving the existing IDs for rollback validation purposes. Existing visual elements will only be removed in STEP 4 after certification.
