# UX12 NUMERIC CONSISTENCY + NAVIGATION AUDIT

**STATUS: CRITICAL / VERDICT_D**
**DATE:** 2026-06-08

This document details the exact observations, calculations, and traceability paths that explain the discrepancies identified in the UX12 Executive Dashboard and routing.

---

# PART 1 — NAVIGATION AUDIT

## Objective
Determine whether the navigation correctly segregates the UX12 Executive view from the Legacy Auditor view.

## Mandatory Validation

**Button: "Gerencial"**
→ **Route:** `/exec`
→ **Template:** `executive_dashboard.html`
→ **API Source:** `/api/v4/exec/summary`, `/api/v4/exec/ux12_summary`, `/api/v4/exec/waterfall`, etc.
→ **Expected Output:** Executive Dashboard (UX12)

**Button: "Auditor"**
→ **Route:** `/app`
→ **Template:** `executive_dashboard.html`
→ **API Source:** Same as `/exec`
→ **Expected Output:** Executive Dashboard (UX12)

## Navigation Failure Analysis
When clicking "Auditor" (which links to `/app`), the system loads `executive_dashboard.html`. This occurs because Phase 1 of the UX12 Primary Routing Activation explicitly re-routed `/app` to `executive_dashboard.html` to prevent users from defaulting to the legacy view. However, the `<a href="/app">Auditor</a>` button inside `executive_dashboard.html` was not updated to point to `/legacy`.
**Result:** Both buttons loop back to the same UX12 template.

**NAVIGATION_AUDIT = FAIL**

---

# PART 2 — NUMERIC CONSISTENCY AUDIT

## Marketplace Card Validation (The 2.8M Delta)

**Observed Values:**
* Ventas: $27.646.200
* Devoluciones: -$4.971.696
* Cobros: -$1.427.364
* Disponible (Neto): $24.101.868

**Visual Math:** $27.646.200 - 4.971.696 - 1.427.364 = **$21.247.140**
**Visible "Disponible":** **$24.101.868**
**Visual Delta:** **$2.854.728**

**Root Cause:**
The UI code for the Marketplace Cards (`templates/executive_dashboard.html` lines 428-442) enforces a negative display sign for "Cobros", regardless of the mathematical reality:
```javascript
const cob = Math.abs(mpItem.cobros || 0); // Strips actual sign
...
<span class="text-sm font-bold text-amber-600">${fmtCLP(-cob)}</span> // Forces negative rendering
```
In the backend (`/api/v4/exec/summary`), `cobros` is calculated as `net - gross - devoluciones`.
For this specific marketplace, the `cobros` sum was mathematically a **positive $1.427.364** (e.g., net positive adjustments or seller subsidies). Because the UI applied `Math.abs()` and then hardcoded a minus sign, it visually inverted a $1.4M gain into a $1.4M loss, creating exactly a $2.8M optical delta against the actual Net Profit ("Disponible").

---

## Composition Validation (+3.1M vs -3.1M)

**Observed Values:**
* Waterfall "Cobros": +$3.186.636
* Composition "Total Cobros": -$3.186.636

**Root Cause (Sign Inversion between APIs):**
1. **Waterfall (`/api/v4/exec/waterfall`):**
   The API applies an explicit inversion to display costs as positive magnitudes in the waterfall structure: `cobros = -(costos_op + costos_com + ajustes)`. Thus, a negative ledger expense of -3.1M becomes **+3.1M**.
2. **Composition (`/api/v4/exec/cobros-breakdown`):**
   The API fetches the raw `SUM(monto)` from the ledger. Since costs are negative in the ledger, it returns **-3.1M**.
3. **UI Rendering:** The Composition UI (`templates/executive_dashboard.html`) renders the exact value from the Breakdown API (negative), while the Waterfall renders the exact value from the Waterfall API (positive).

---

# PART 3 — CROSS-VIEW CONSISTENCY

| Component | Source API | Sign Logic | Structural Integrity |
| :--- | :--- | :--- | :--- |
| **Marketplace Cards** | `/exec/summary` | Hardcoded `fmtCLP(-cob)` | **FAIL** (Breaks math if cobros is positive) |
| **Waterfall** | `/exec/waterfall` | Inverted `-(costos)` | **FAIL** (Displays expenses as positive numbers) |
| **Composition** | `/exec/cobros-breakdown` | Raw Ledger (Negative) | **PASS** (True to ledger) |
| **Ledger (Truth)** | Database | Negative = Expense | **PASS** |

---

# PART 4 — DATA FLOW TRACE

**Database:** `marketplace_ledger_v1` (Expenses = Negative)
↓
**API Level:**
*   `/exec/summary`: Computes `cobros` dynamically. Retains original sign (can be positive).
*   `/exec/waterfall`: Inverts sign intentionally `-(...)`. Becomes positive.
*   `/exec/cobros-breakdown`: Raw `SUM()`. Remains negative.
↓
**ViewModel (UI JS):**
*   **Cards:** Intercepts `cobros`, applies `Math.abs()`, forces negative.
*   **Waterfall:** Passes positive value directly.
*   **Composition:** Passes negative value directly.

**Data Flow Diagnosis:** The API layer lacks a unified contract for financial signs, and the UI layer attempts to heuristically correct signs using `Math.abs()`, resulting in mathematical contradictions.

---

# FINAL VERDICT

### **VERDICT_D: NAVIGATION + NUMERIC ISSUES**

**Recommended Fixes:**
1. **Navigation:** Update the `href="/app"` links in `executive_dashboard.html` to point to `/legacy`.
2. **Numeric (API Contract):** Standardize all API endpoints to return raw Ledger truth (Expenses = Negative). Remove the inversion logic `-(costos_op...)` from the Waterfall API.
3. **Numeric (UI Presentation):** Remove `Math.abs()` and hardcoded negative signs from the JavaScript templates. Allow the data payload to dictate the mathematical sign natively.
