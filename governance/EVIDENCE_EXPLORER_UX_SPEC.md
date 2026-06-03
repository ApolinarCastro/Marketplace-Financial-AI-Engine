# EVIDENCE EXPLORER UX SPEC

**Sprint**: B3
**Date**: 2026-05-30
**Regime**: ARQUITECTURA — READ ONLY

---

## TABLE OF CONTENTS

1. [Evidence Explorer Panel](#fase-1--evidence-explorer-panel)
2. [Explainability View](#fase-2--explainability-view)
3. [Evidence Badge System](#fase-3--evidence-badge-system)
4. [Confidence Visualization](#fase-4--confidence-visualization)
5. [Marketplace-Specific Evidence Flows](#fase-5--marketplace-specific-evidence-flows)
6. [Key UX Questions Answered](#key-ux-questions)

---

## FASE 1 — EVIDENCE EXPLORER PANEL

### Location

The Evidence Explorer replaces and extends the current Transaction Inspector modal (`#inspector-modal`).

**Trigger**: Click any row in the ledger table
**Behavior**: Opens as a slide-in panel from the right side (not a centered modal)

### Layout

```
┌───────────────────────────────────────────────────────────────────────┐
│  EVIDENCE EXPLORER                                       [✕] [—] [⛶] │
│  ─────────────────────────────────────────────────────────────────── │
│                                                                       │
│  ┌─── TRANSACTION HEADER ──────────────────────────────────────────┐ │
│  │  TX-2026-04-ML-000001                                 $1,000,000│ │
│  │  Cargo por venta (Venta) · 2026-04-15 · ML                      │ │
│  │                                                                  │ │
│  │  [🔵 CERTIFICADO ▼]   [Evidence Chain ▼]   [Explain ▼]          │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── TAB BAR ──────────────────────────────────────────────────────┐ │
│  │  [📋 Evidence Chain]  [📄 Source]  [📊 Impact]  [🔍 Audit]      │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── EVIDENCE CHAIN TAB (default) ────────────────────────────────┐ │
│  │                                                                   │ │
│  │  Each link is a horizontal card with:                             │ │
│  │  • Icon (file type / DB type)                                     │ │
│  │  • Label (file name / table name)                                 │ │
│  │  • Key metadata (rows, amount, date)                              │ │
│  │  • Confidence badge                                               │ │
│  │  • Click to expand / preview                                      │ │
│  │                                                                   │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ❶ MARKETPLACE                                               │  │ │
│  │  │   Mercado Libre (ML)                                        │  │ │
│  │  │   [ 🟢 100% ]                                               │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │       │                                                          │ │
│  │       ▼                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ❷ SOURCE FILE                    [📂 Preview ▼]            │  │ │
│  │  │   2026_04.xlsx · Fila 42                                    │  │ │
│  │  │   ML_Facturacion/2026_04.xlsx                               │  │ │
│  │  │   [ 🟢 100% ]                                               │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │       │                                                          │ │
│  │       ▼                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ❸ XML EVIDENCE                     [📄 View XML ▼]         │  │ │
│  │  │   Folio: 033-0013380337                                     │  │ │
│  │  │   DTE_762.xml · Monto: $1,000,000                           │  │ │
│  │  │   [ 🟢 CERTIFICADO ]   Estado: CERTIFICADO                  │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │       │                                                          │ │
│  │       ▼                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ④ CONCEPT                            [📊 Classification]   │  │ │
│  │  │   Cargo por venta (Venta)                                   │  │ │
│  │  │   → INGRESO_VENTA                                           │  │ │
│  │  │   [ 🟢 100% ]                                               │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │       │                                                          │ │
│  │       ▼                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ⑤ CLASSIFICATION                   [📊 Detail ▼]           │  │ │
│  │  │   clasificacion_operativa: "Cargo por venta (Venta)"        │  │ │
│  │  │   financial_group: "ingresos"                                │  │ │
│  │  │   include_in_operational_pnl: TRUE                           │  │ │
│  │  │   [ 🟢 100% ]                                               │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │       │                                                          │ │
│  │       ▼                                                          │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ ⑥ FINANCIAL CLOSE                  [📊 View Close ▼]       │  │ │
│  │  │   ML · 2026-04 · $927,759 neto                              │  │ │
│  │  │   Impact on: total_ingresos (+$1,000,000)                   │  │ │
│  │  │   [ 🟢 100% ]                                               │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── CONFIDENCE FOOTER ────────────────────────────────────────────┐ │
│  │  OVERALL CONFIDENCE:  ██████████░  96%                            │ │
│  │  Source: 100%  XML: 100%  Class: 100%  Aggregate: 100%          │ │
│  │  Status: ✅ All evidence links verified                            │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

### Panel States

| State | Trigger | Visual |
|---|---|---|
| **Loading** | Click row | Skeleton placeholder (3 pulse bars) |
| **Loaded** | Data received | Full chain view with all 6 links |
| **Partial** | Missing links | Dimmed nodes with "?" icon + explanation text |
| **Error** | API failure | Red banner with retry button |
| **Empty** | No data row | "No hay datos de evidencia" with explanation |

### Interaction Design

| Action | Behavior |
|---|---|
| Click row in ledger | Open Evidence Explorer (slide-in right) |
| Click a chain node | Expand inline with detail sub-panel |
| Click "Preview" on file node | Show file preview in split view (right 50%) |
| Click "View XML" on XML node | Show raw XML content in split view |
| Click "Classification" | Show classification mapping rule |
| Click "View Close" | Navigate to close detail for that period |
| Click chain arrow (→) | Animate scroll to next node |
| Click confidence bar | Show dimension breakdown popover |
| Click "Explain" button | Switch to Explainability View (FASE 2) |

### Responsive Behavior

| Screen | Behavior |
|---|---|
| >1200px | Slide-in panel at 600px width, ledger dims behind |
| 768-1200px | Slide-in at 90vw width |
| <768px | Full-screen drawer, swipe to close |

---

## FASE 2 — EXPLAINABILITY VIEW

### Overview

A separate tab/window that answers the 6-question Explainability Contract for any figure. Accessible from:
- The Evidence Explorer "Explain" button
- The cierre summary panel (click any figure)
- An auditoria finding (click "explain this alert")

### Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  EXPLAINABILITY REPORT                                  [Export PDF] │
│  ─────────────────────────────────────────────────────────────────── │
│                                                                       │
│  CIFRA: $927,759 CLP  ·  Resultado neto  ·  ML  ·  2026-04           │
│                                                                       │
│  ┌─── Q1: ¿QUÉ es? ───────────────────────────────────────────────┐ │
│  │  Resultado neto del cierre financiero de Mercado Libre para      │ │
│  │  abril 2026. Corresponde a la resta de ingresos ($1,000,000)     │ │
│  │  menos costos operacionales (-$72,241).                           │ │
│  │  No incluye: Mediación ($18,331) - excluido del P&L operacional. │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── Q2: ¿CUÁNTO es? ────────────────────────────────────────────┐ │
│  │  $927,759 CLP                                                     │ │
│  │                                                                   │ │
│  │  ┌──────────┬─────────────┬───────────┬─────────┐                │ │
│  │  │ Concepto │    Monto    │    %      │  Group  │                │ │
│  │  ├──────────┼─────────────┼───────────┼─────────┤                │ │
│  │  │ Ingresos │ $1,000,000  │  107.8%   │ ingresos│                │ │
│  │  │ Op.Costs │  -$72,241   │   -7.8%   │ costos  │                │ │
│  │  ├──────────┼─────────────┼───────────┼─────────┤                │ │
│  │  │ NETO     │  $927,759   │  100.0%   │    —    │                │ │
│  │  └──────────┴─────────────┴───────────┴─────────┘                │ │
│  │                                                                   │ │
│  │  Excluido del P&L operacional:                                    │ │
│  │  • Mediación: +$18,331 (include_in_operational_pnl = FALSE)      │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── Q3: ¿DE DÓNDE viene? ───────────────────────────────────────┐ │
│  │                                                                   │ │
│  │  Transacción primaria: TX-2026-04-ML-000001                       │ │
│  │                                                                   │ │
│  │  [2026_04.xlsx] → [Ledger Row] → [Classified] → [Close]          │ │
│  │       Fila 42        TX-000001      ingresos    2026-04           │ │
│  │                                                                   │ │
│  │  Documento soporte: 01_Raw/ML/ML_Facturacion/2026_04.xlsx        │ │
│  │  [📂 Open file location]                                          │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── Q4: ¿POR QUÉ existe? ───────────────────────────────────────┐ │
│  │  Venta de producto SKU-123456 a través de Mercado Libre           │ │
│  │                                                                   │ │
│  │  Clasificación: El detalle "Cargo por venta (Venta)" fue          │ │
│  │  mapeado a "ingresos" mediante regla establecida en               │ │
│  │  FINANCIAL_STRUCTURE.                                             │ │
│  │                                                                   │ │
│  │  Respaldo XML: Folio 033-0013380337 (DTE_762.xml)                 │ │
│  │  Estado: CERTIFICADO ✅                                            │ │
│  │  Monto DTE: $1,000,000 · Match: 100%                              │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── Q5: ¿DÓNDE impacta? ────────────────────────────────────────┐ │
│  │                                                                   │ │
│  │  Directo: marketplace_cierre_financiero_v1                        │ │
│  │    → total_ingresos: +$1,000,000                                   │ │
│  │    → resultado_neto: +$927,759 (net of costs)                     │ │
│  │                                                                   │ │
│  │  Dashboard: vw_dashboard_kpis → total_sales_internal              │ │
│  │  Auditoría: cargo_sin_respaldo_legal → PASSED ✅                  │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─── Q6: EVIDENCIA ──────────────────────────────────────────────┐ │
│  │                                                                   │ │
│  │  Fuentes primarias (2):                                           │ │
│  │  • 01_Raw/ML/ML_Facturacion/2026_04.xlsx (5,234 rows)           │ │
│  │  • 01_Raw/ML/Documentos Recepcionados/DTE_762.xml                │ │
│  │                                                                   │ │
│  │  Registros involucrados:                                          │ │
│  │  • 1 ledger row (marketplace_ledger_v1)                           │ │
│  │  • 1 classification row (marketplace_ledger_clasificado_v1)      │ │
│  │  • 1 close row (marketplace_cierre_financiero_v1)                 │ │
│  │  • 0 audit findings                                              │ │
│  │                                                                   │ │
│  │  Confianza general: 96%                                           │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

### Explainability States

| State | Description | Visual Indicator |
|---|---|---|
| **COMPLETE** | All 6 questions answered with data | Green header bar |
| **PARTIAL** | Some questions have gaps (e.g., no XML) | Amber header bar + gap list |
| **INFERRED** | All data comes from inference, no direct source | Blue header bar with "INFERIDO" badge |
| **BROKEN** | Key evidence missing (source file not found) | Red header bar with "CADENA ROTA" alert |

### Answer Quality Indicators

Each answer has a quality badge next to it:

| Badge | Meaning | Color |
|---|---|---|
| **DIRECTO** | Direct evidence from source | 🟢 Green |
| **INFERIDO** | Derived/inferred from other data | 🔵 Blue |
| **SIN DATOS** | No data available | ⚪ Gray |
| **NO APLICA** | Question not applicable to this figure | ⚪ Gray |

### Example: RIPLEY Partial Explainability

```
┌─── Q4: ¿POR QUÉ existe? ───────────────────────────────────────┐
│  Venta de producto a través de Ripley (Orden OC-2024-001234)     │
│                                                                   │
│  Clasificación: "Importe del pedido" → "ingresos" (regla directa) │
│                                                                   │
│  Respaldo XML: ⚠️ SIN EVIDENCIA LEGAL                             │
│  Folio liquidación: "312"                                         │
│  No existe XML en dte_truth_v1 para este folio.                   │
│  Estado: SIN_RECURSO_XML                                          │
│                                                                   │
│  Impacto en confianza: XML dimension = 0% (reduce overall from    │
│  95% to 71%)                                                      │
│                                                                   │
│  [🔍 Ver XMLs disponibles para este período]                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## FASE 3 — EVIDENCE BADGE SYSTEM

### Core Badge: Evidence Status

For each row in the ledger table, an evidence status badge:

```
┌─────────────────────────────────────────────────────────────┐
│  BADGE VARIANTS                                              │
│                                                              │
│  🟢 [CERTIFICADO]    — XML exists in dte_truth_v1           │
│                        Click → Evidence Explorer             │
│                                                              │
│  🟡 [BRIDGE]         — XML matched via bridge methodology   │
│                        (PARIS: Excel folio → XML folio)      │
│                        Click → shows bridge detail           │
│                                                              │
│  🔵 [MATCH HEUR]     — XML matched by amount + date window  │
│                        (xml_matcher.py algorithm)             │
│                        Click → shows match parameters        │
│                                                              │
│  ⚪ [SIN RECURSO]    — folio_xml present but NOT in XMLs    │
│                        Hover → "Folio X no encontrado en     │
│                                 dte_truth_v1 (920 XMLs)"    │
│                                                              │
│  ⚪ [SIN XML]        — No folio_xml value                    │
│                        Hover → "Sin vínculo a documento     │
│                                 tributario"                 │
│                                                              │
│  🔴 [NO CLASIFICADO] — detalle not in any classification    │
│                        Hover → "Concepto no clasificado"    │
│                        Click → classification suggestion     │
│                                                              │
│  ❓ [ORPHAN]         — Source file not found / not loaded   │
│                        (RIPLEY: 7 facturas $50.5M gap)      │
│                        Hover → "Documento fuente faltante"   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Badge in Ledger Table

```
┌──────┬────────────┬──────────────────────┬────────────┬──────────────┐
│ Fecha│ ID         │ Detalle              │ Monto      │ Evidencia    │
├──────┼────────────┼──────────────────────┼────────────┼──────────────┤
│04-15 │TX-000001   │Cargo por venta...    │ +$1,000,000│ [CERTIFICADO]│
│04-15 │TX-000002   │Comisión              │   -$178,000│ [CERTIFICADO]│
│04-16 │TX-000003   │Mediación             │    +$18,331│ [SIN XML]    │
│04-16 │TX-000004   │Fee divergencia       │   -$72,241│ [BRIDGE]     │
└──────┴────────────┴──────────────────────┴────────────┴──────────────┘
```

### Badge in Financial Close Summary

Each figure in the `cierre` panel shows a confidence badge:

```
┌────────────────────────────────────────────────┐
│  ESTRUCTURA FINANCIERA — ML · Abril 2026       │
│                                                 │
│  Ingresos          $1,000,000  🟢 100%         │
│  Costos Op.         -$72,241   🟢 100%         │
│  Costos Com.             $0    ⚪  71%         │
│  Ajustes             $18,331   🟡  85%         │
│  Devoluciones            $0    ⚪  71%         │
│  ───────────────────────────────────────       │
│  Resultado Neto     $927,759   🟢  96%         │
│                                                 │
│  Click any figure → Explainability Report       │
└────────────────────────────────────────────────┘
```

### Badge Sizing

| Context | Size | Format |
|---|---|---|
| Ledger table row | Small | `[CERTIFICADO]` (pill) |
| Cierre summary | Small | `🟢 100%` (dot + % inline) |
| Evidence Explorer node | Medium | Icon + label + detail |
| Full explainability | Large | Pill with description |
| Mobile | Compact | Dot only (no text on <480px) |

### Color Semantics

| Color | Meaning | Hex |
|---|---|---|
| 🟢 Green | Direct evidence, no gaps | `#059669` |
| 🟡 Amber | Indirect/bridge evidence | `#D97706` |
| 🔵 Blue | Heuristic/inferred match | `#2563EB` |
| ⚪ Gray | No evidence, no error | `#94A3B8` |
| 🔴 Red | Error/orphan/missing | `#DC2626` |

---

## FASE 4 — CONFIDENCE VISUALIZATION

### Confidence Bar Component

Used in: Evidence Explorer footer, Explainability report, Cierre summary

```
Variant 1: Compact (footer)
  OVERALL: ██████████░░  96%
  Source  ████████████ 100%
  XML     ████████████ 100%
  Class   ████████████ 100%
  Aggr    ████████████ 100%

Variant 2: Detailed (popover / expanded)
  ┌──────────────────────────────────────────────┐
  │  OVERALL CONFIDENCE                         │
  │  ████████████████████████████████░░░░  96%  │
  │                                              │
  │  Source File        100%  ████████████████   │
  │  XML Evidence       100%  ████████████████   │
  │  Classification     100%  ████████████████   │
  │  Aggregation        100%  ████████████████   │
  │                                              │
  │  Status: ✅ Todas las fuentes verificadas    │
  │  Missing: Ninguna                             │
  └──────────────────────────────────────────────┘

Variant 3: Gap Highlight (when confidence < 70%)
  ┌──────────────────────────────────────────────┐
  │  ⚠️ CONFIDENCE REDUCED                       │
  │  ██████████████░░░░░░░░░░░░░░░░░░░░  71%     │
  │                                              │
  │  Source File        100%  ████████████████   │
  │  XML Evidence         0%  ░░░░░░░░░░░░░░░░   │ ◄─── REDUCED
  │  Classification     100%  ████████████████   │
  │  Aggregation        100%  ████████████████   │
  │                                              │
  │  ⚠️ XML dimension at 0% — reduce overall     │
  │  from ~93% to 71%. Sin respaldo XML.         │
  │                                              │
  │  [🔍 Ver XMLs disponibles para este período] │
  └──────────────────────────────────────────────┘
```

### Confidence Thresholds

| Range | Color | Label | UX Treatment |
|---|---|---|---|
| 90-100% | 🟢 | Alta | Normal display |
| 70-89% | 🟡 | Media | Warning icon next to number |
| 40-69% | 🟠 | Baja | Warning banner, expand to show gap |
| 0-39% | 🔴 | Crítica | Red highlight, blocking gap explanation |

### Per-Dimension Icons

| Dimension | Icon | Tooltip |
|---|---|---|
| Source File | 📁 | "Archivo fuente procesado correctamente" |
| XML Evidence | 📄 | "Documento tributario verificado" |
| Classification | 🏷️ | "Clasificación financiera aplicada" |
| Aggregation | 🔢 | "Cálculo de agregación verificado" |

### Confidence History

Optional: show how confidence changed over time (snapshot comparison):

```
  CONFIDENCE OVER TIME
  ┌────────────────────────────────────────────┐
  │  Apr 2026  ████████████████████████░  96%  │
  │  Mar 2026  ██████████████████████░░  92%  │
  │  Feb 2026  ████████████████████░░░  88%  │
  │  Jan 2026  ██████████████████░░░░░  84%  │
  │                                            │
  │  Trend: ▲ +12% este trimestre             │
  └────────────────────────────────────────────┘
```

---

## FASE 5 — MARKETPLACE-SPECIFIC EVIDENCE FLOWS

### ML — Full Evidence Chain

```
  CHAIN: COMPLETE (6/6)

  Evidence Explorer shows ALL 6 nodes:
  ├── Marketplace: Mercado Libre
  ├── Source File: ML_Facturacion/2026_04.xlsx (Fila 42)
  ├── XML Evidence: DTE_762.xml (CERTIFICADO)
  ├── Concept: INGRESO_VENTA (Cargo por venta)
  ├── Classification: ingresos (100% confidence)
  └── Close: ML · 2026-04

  BADGE: [CERTIFICADO] — Green

  TYPICAL FLOW:
  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
  │ xlsx:      │ →  │ L1: Ledger │ →  │ L2: Class  │ →  │ L4: Close  │
  │ 2026_04    │    │ row: +$1M  │    │ ingresos   │    │ net: $927K │
  └────────────┘    └────────────┘    └────────────┘    └────────────┘
       │                  ↑                ↑
       ▼                  │                │
  ┌────────────┐          │                │
  │ XML: DTE   │ ─────────┘                │
  │ Folio 033  │  folio_xml match          │
  │ CERTIFICADO│                           │
  └────────────┘                           │
       │                                    │
       ▼                                    │
  ┌────────────┐                            │
  │ dte_truth  │ ───────────────────────────┘
  │ v1         │  estado_xml = CERTIFICADO
  └────────────┘

  UX NOTES:
  • Most rows show [CERTIFICADO] or [SIN XML]
  • 89.4% of rows have folio_xml
  • Click XML node → shows raw XML content + DTE amounts
  • Confidence typically 95-100%
```

### PARIS — Bridge Evidence Chain

```
  CHAIN: PARTIAL (5/6 — XML bridge)

  Evidence Explorer shows 6 nodes, but XML node shows "BRIDGE":
  ├── Marketplace: Paris
  ├── Source File: transactions_report_20260525.xlsx
  ├── XML Evidence: dteproveedor_5372.xml (BRIDGE)
  │     └── Matched via: "Número factura" column from Excel
  │         → "5372" → dteproveedor_5372.xml → Folio match
  ├── Concept: PAGO (Venta)
  ├── Classification: ingresos (90% confidence)
  └── Close: PARIS · 2026-04

  BADGE: [BRIDGE] — Amber

  BRIDGE DETAIL (click to expand):
  ┌────────────────────────────────────────────┐
  │  BRIDGE METHODOLOGY                        │
  │                                            │
  │  Excel column "Número factura" = "5372"    │
  │    → XML file: dteproveedor_5372.xml       │
  │    → XML <Folio>: 5372                     │
  │    → Match: EXACT (column → filename)      │
  │                                            │
  │  Confianza: 90% (indirecto)                │
  │  Estado: BRIDGE_ACTIVADO (Sprint A2)       │
  │                                            │
  │  📁 Excel: 01_Raw/PARIS/Transacciones/...  │
  │  📄 XML:   01_Raw/PARIS/Facturacion/...    │
  └────────────────────────────────────────────┘

  UX NOTES:
  • Bridge badge is AMBER (not green) to indicate indirect match
  • Bridge detail is ALWAYS visible — never hidden
  • 32/54 XMLs bridged (51.1% coverage)
  • Gaps show as [SIN XML] with note "XML exists but not bridged"
```

### RIPLEY — Broken Evidence Chain

```
  CHAIN: BROKEN (4/6 — XML evidence missing)

  Evidence Explorer shows 6 nodes, XML node shows "SIN RECURSO":
  ├── Marketplace: Ripley
  ├── Source File: 000312-2815.xlsx
  ├── XML Evidence: ⚠️ NO DISPONIBLE
  │     └── folio_xml = "312" (Número documento liquidación)
  │     └── No XML found in dte_truth_v1
  │     └── 100 XMLs exist but cover only Mar-May 2026 ($25.5M)
  │     └── This row is outside that range
  ├── Concept: INGRESO_VENTA (Importe del pedido)
  ├── Classification: ingresos (85% confidence)
  └── Close: RIPLEY · 2026-04

  BADGE: [SIN RECURSO] — Gray

  GAP DETAIL (auto-expanded):
  ┌────────────────────────────────────────────┐
  │  ⚠️ EVIDENCE GAP DETECTED                  │
  │                                            │
  │  XML dimension confidence: 0%              │
  │                                            │
  │  This reduces overall confidence from      │
  │  95% to 71%.                                │
  │                                            │
  │  Why no XML?                                │
  │  • 100 RIPLEY XMLs exist in                │
  │    01_Raw/RIPLEY/Documentos Recepcionados/ │
  │  • But they cover only Mar-May 2026        │
  │  • This transaction is from Apr 2026       │
  │  • 0% of RIPLEY ledger has estado_xml =    │
  │    CERTIFICADO                              │
  │                                            │
  │  Recommendation: Upload XMLs for this      │
  │  liquidation period (000312-2815)           │
  │                                            │
  │  [🔍 View available XMLs (100)]             │
  └────────────────────────────────────────────┘

  EXPLAINABILITY REPORT GAPS:
  Q4 (¿POR QUÉ existe?) shows:
  • ✅ Clasificación financiera: clara
  • ✅ Concepto de negocio: venta confirmada
  • ❌ Respaldo XML: SIN EVIDENCIA LEGAL
  • Impacto: Overall confianza reducida de 95% → 71%

  UX NOTES:
  • RIPLEY rows ALWAYS show reduced confidence
  • Gap detail is auto-expanded — never collapsed
  • "Recommendation" provides actionable next step
  • The system can still explain FINANCIAL ops clearly
  • The limitation is purely LEGAL evidence
```

### FALABELLA — Partial Evidence Chain

```
  CHAIN: PARTIAL (4/6 — shared XMLs, small volume)

  Evidence Explorer:
  ├── Marketplace: Falabella
  ├── Source File: Ordenes_y_Transacciones_Falabella_Mar2026.xlsx
  ├── XML Evidence: ⚠️ 4 XMLs (shared with ML)
  │     └── 4 XML files identical to ML/ counterparts
  │     └── 5 folio_xml values in ledger
  │     └── 0% CERTIFICADO
  ├── Concept: PAGO (Pago por precio del producto)
  ├── Classification: ingresos (80% confidence)
  └── Close: FALABELLA · 2026-05

  BADGE: [SIN XML] — Gray

  UNIQUE: DUPLICATE FILE WARNING:
  ┌────────────────────────────────────────────┐
  │  ⚠️ DUPLICATE SOURCE                       │
  │                                            │
  │  The XML file 033-0013380337.xml also      │
  │  exists in ML/ (sobreconteo documental).   │
  │                                            │
  │  Same file, different marketplace folders. │
  │  This does not affect evidence quality.    │
  └────────────────────────────────────────────┘

  UX NOTES:
  • Smallest marketplace (1,008 rows, $2.6M)
  • Duplicate file warning is informative, not blocking
  • Confidence typically 71-83% (no XML match)
```

---

## KEY UX QUESTIONS

### 1. ¿Cómo navega un auditor desde una cifra hasta la evidencia original?

**Path of 3 clicks:**

```
CLICK 1: En el panel de cierre, click en una cifra (ej. "Ingresos $1,000,000")
  → Filtra el ledger a esa categoría
  → Muestra todas las transacciones que componen esa cifra

CLICK 2: Click en una fila del ledger
  → Abre el Evidence Explorer
  → Muestra la cadena completa de 6 eslabones

CLICK 3: Click en cualquier nodo de evidencia (ej. "2026_04.xlsx")
  → Expande vista previa del archivo
  → Muestra fila exacta, columnas, valores

Desde la cifra hasta el archivo original: 3 clicks, <5 segundos.
```

**Keyboard shortcuts:**

| Shortcut | Action |
|---|---|
| `↑ ↓` | Navigate ledger rows |
| `Enter` | Open Evidence Explorer |
| `Escape` | Close panel / go back |
| `Tab` | Move between chain nodes |
| `Space` | Expand node detail |

### 2. ¿Cómo entiende la diferencia entre evidencia operacional y legal?

**Two separate indicators, always visible:**

```
  ┌──────────────────────────────────┐
  │  EVIDENCIA OPERATIVA             │
  │                                  │
  │  📁 Source File: 2026_04.xlsx   │ 🟢 100%
  │  🏷️ Classification: ingresos   │ 🟢 100%
  │  🔢 Aggregation: correcta       │ 🟢 100%
  │                                  │
  │  OPERATIONAL CONFIDENCE: 100%    │
  └──────────────────────────────────┘

  ┌──────────────────────────────────┐
  │  EVIDENCIA LEGAL                 │
  │                                  │
  │  📄 XML: Folio 033-0013380337   │ 🟢 100%
  │  📄 Estado: CERTIFICADO          │
  │                                  │
  │  LEGAL CONFIDENCE: 100%          │
  └──────────────────────────────────┘

  ┌──────────────────────────────────┐
  │  OVERALL: 96% (weighted)         │
  └──────────────────────────────────┘
```

**Visual separation:**
- Operational evidence = left column / top section (blue tint)
- Legal evidence = right column / bottom section (green tint)
- When legal is missing, the legal section turns gray with a clear "SIN EVIDENCIA LEGAL" badge
- Overall confidence shows BOTH dimensions separately before combining

**In the ledger table:**
- The badge reflects legal evidence status
- Clicking the badge shows a tooltip with operational confidence separately

### 3. ¿Cómo identifica gaps?

**Three gap detection mechanisms:**

```
MECHANISM 1: Badge Color
  [CERTIFICADO]   = No gaps
  [BRIDGE]        = Partial gap (indirect evidence)
  [SIN RECURSO]   = Gap: folio exists but no matching XML
  [SIN XML]       = Gap: no folio at all
  [NO CLASIFICADO]= Gap: concept not in any classification mapping
  [ORPHAN]        = Critical gap: source file missing

MECHANISM 2: Confidence Bars
  Any dimension < 100% is visually highlighted:
    XML Evidence       0%  ░░░░░░░░░░░░░░░░░░░░
    └── Dimension below threshold → click for explanation

MECHANISM 3: Gap Summary Strip
  Shown at the top of the Evidence Explorer when gaps exist:
  ┌────────────────────────────────────────────────────────────┐
  │  ⚠️ 3 GAPS DETECTED                                        │
  │  ┌──────────────────────────────────────────────────────┐  │
  │  │ ❶ XML: folio "312" no encontrado en dte_truth_v1    │  │
  │  │   (existen 100 XMLs, pero ninguno para este folio)   │  │
  │  │ ❷ Clasificación: confianza 85% (concepto genérico)  │  │
  │  │ ❸ Agregación: cifra inferida (A pagar = computed)   │  │
  │  └──────────────────────────────────────────────────────┘  │
  │  Impacto: Overall confidence reduced from 96% → 71%         │
  │  [🔍 View all gaps]  [📊 Recommendation report]              │
  └────────────────────────────────────────────────────────────┘

MECHANISM 4: Periodic Gap Dashboard
  Available from the main navigation:
  ┌────────────────────────────────────────────────────────────┐
  │  EVIDENCE QUALITY DASHBOARD                                │
  │                                                            │
  │  Marketplace  │ Rows │ XML%  │ Cert%  │ Conf  │ Audit     │
  │  ─────────────┼──────┼───────┼────────┼───────┼───────────│
  │  ML           │ 101K │ 89.4% │  5.8%  │  96%  │  3 alerts │
  │  RIPLEY       │ 269K │  0.0% │  0.0%  │  71%  │  7 alerts │
  │  PARIS        │  42K │ 51.1% │  0.0%  │  91%  │  1 alert  │
  │  FALABELLA    │   1K │  0.1% │  0.0%  │  83%  │  0 alerts │
  └────────────────────────────────────────────────────────────┘
```

### 4. ¿Cómo interpreta confidence?

**Rules for the user:**

```
1. HIGH (90-100%) → 🟢 "Todos los documentos verificados"
     • The figure is backed by source files + legal evidence
     • No manual verification needed
     • Example: ML row with CERTIFICADO badge

2. MEDIUM (70-89%) → 🟡 "Evidencia operacional completa, legal parcial"
     • The financial operation is clear and classifiable
     • Legal evidence is missing or indirect
     • Recommendation: Review XML coverage for this period
     • Example: RIPLEY row with SIN RECURSO badge

3. LOW (40-69%) → 🟠 "Evidencia incompleta"
     • Multiple gaps in the chain
     • Classification may be uncertain
     • Recommendation: Manual review required
     • Example: Unclassified concept (NO CLASIFICADO)

4. CRITICAL (0-39%) → 🔴 "Sin evidencia confiable"
     • Source files may be missing
     • No classification possible
     • Recommendation: Blocking — requires investigation
     • Example: 7 RIPLEY facturas no cargadas ($50.5M)

INTERPRETATION HELP:
  Each confidence bar is clickable → shows:
  • What this dimension measures
  • Why this score was assigned
  • What would improve it
  • Impact on overall confidence if improved
```

**Confidence as a product differentiator:**

```
  CONFIDENCE IS NOT "ACCURACY"
  It is "EVIDENCE QUALITY"

  A figure can be 100% financially accurate AND 0% legally confident.
  (Example: RIPLEY Importe del pedido — correct amount, no XML backing)

  The system NEVER hides the legal gap behind a high overall number.
  Both dimensions are always visible.
```

---

## ANNEX: Component Inventory

For implementation (future sprint), these UI components need to be built:

| Component | Used In | Priority |
|---|---|---|
| EvidenceChain | Explorer panel tab | P0 |
| ChainNode | Individual link in chain | P0 |
| EvidenceBadge | Ledger table, cierre, explorer | P0 |
| ConfidenceBar | Explorer footer, explainability | P0 |
| ConfidenceDimension | Per-dimension bar | P0 |
| GapSummary | Explorer top banner | P0 |
| GapDashboard | Main navigation page | P1 |
| ExplainabilityReport | Full report view | P0 |
| AnswerCard | Single Q&A section | P0 |
| AnswerBadge | Quality indicator per answer | P1 |
| FilePreview | Inline file content view | P1 |
| BridgeDetail | PARIS-specific metadata | P1 |
| DuplicateWarning | FALABELLA-specific alert | P2 |
| ConfidenceTimeline | Historical trend chart | P2 |
| RecommendationCard | Gap improvement suggestions | P1 |

---

**Document designed by**: Sprint B3 — Evidence UX Design
**Regime**: ARQUITECTURA — READ ONLY
**Status**: UX design complete — ready for frontend implementation planning
