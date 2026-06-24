# FINANCIAL EVIDENCE CHAIN DESIGN

**Sprint**: B2
**Date**: 2026-05-30
**Regime**: ARQUITECTURA — READ ONLY

---

## TABLE OF CONTENTS

1. [Traceability Model](#fase-1--traceability-model)
2. [Evidence Nodes](#fase-2--evidence-nodes)
3. [Explainability Contract](#fase-3--explainability-contract)
4. [RIPLEY Pilot](#fase-4--ripley-pilot)
5. [Visual Flow](#fase-5--visual-flow)
6. [Confidence Model](#fase-6--confidence-model)
7. [Product Value](#fase-7--product-value)

---

## FASE 1 — TRACEABILITY MODEL

### Standard Chain

```
  NIVEL 1              NIVEL 2              NIVEL 3              NIVEL 4              NIVEL 5              NIVEL 6
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  MARKETPLACE │ →  │   ARCHIVO    │ →  │ LIQUIDACIÓN/ │ →  │   CONCEPTO   │ →  │    LEDGER    │ →  │    CIERRE    │
│              │    │   FUENTE     │    │   FACTURA    │    │  FINANCIERO  │    │              │    │  FINANCIERO  │
│  ML          │    │  .xlsx / .csv│    │  .xml / folio│    │  detalle     │    │  monto       │    │  resultado   │
│  RIPLEY      │    │  .xlsx       │    │  liquidación │    │  tipo_mov    │    │  group       │    │  neto        │
│  PARIS       │    │  .xlsx       │    │  .xml / folio│    │  detalle     │    │  group       │    │  neto        │
│  FALABELLA   │    │  .xlsx       │    │  .xml / folio│    │  detalle     │    │  group       │    │  neto        │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### ML — Traceability Variant

```
ML (Mercado Libre)
  │
  ├── ML_Facturacion/2026_04.xlsx
  │     │
  │     ├── Fila: Cargo por venta (Venta)
  │     │     → id_transaccion = "TX-2026-04-ML-000001"
  │     │     → monto = +$1,000,000.00  (INGRESO_VENTA)
  │     │     → monto = -$178,000.00    (EGRESO_COMISION)
  │     │     → folio_xml = "033-0013380337"
  │     │     → archivo_origen = "2026_04.xlsx"
  │     │
  │     └── XML: 01_Raw/ML/Documentos Recepcionados/DTE_762.xml
  │           → <Folio>0013380337</Folio>
  │           → <TipoDTE>033</TipoDTE>
  │           → <MontoTotal>1,000,000</MontoTotal>
  │           → dte_truth_v1.folio = "0013380337"
  │
  ├── Poscobro/release_2026_04.xlsx
  │     └── PAGO: liberación de fondos (sin folio_xml)
  │
  └── Documentos Recepcionados/ (762 XML files)
        → dte_indexer.py → dte_truth_v1
        → xml_matcher.py → ledger.folio_xml
        → surgical_xml_justifier.py → estado_xml = 'CERTIFICADO' | 'SIN_RECURSO_XML'

  CHAIN LENGTH: 6/6 links  →  COMPLETE
  COVERAGE: 89.4% folio_xml, 5.8% CERTIFICADO
  GAP: $307M (96.3% within XML date range, only $11.2M future noise)
```

### RIPLEY — Traceability Variant

```
RIPLEY
  │
  ├── Resumen financiero/000312-2815.xlsx
  │     │
  │     ├── Columna: Importe del pedido  →  $X  (INGRESO_VENTA)
  │     ├── Columna: Comisión             →  -$Y  (EGRESO_COMISION)
  │     ├── Columna: Pedidos reembolsados →  -$Z  (DEVOLUCION)
  │     └── Columna: A pagar              →  neto
  │
  │     → folio_xml = "312" (Número documento liquidación)
  │     → NO existe XML matching (0% CERTIFICADO, 0% folio_xml en dte_truth)
  │
  └── Documentos Recepcionados/ (100 XML files, Mar-May 2026 only)
        → Cubren solo $25.5M de $284.9M (8.9% coverage)
        → 91.1% del ledger NO tiene respaldo XML

  CHAIN LENGTH: 3/6 links  →  BROKEN (XML evidence gap)
  COVERAGE: 0% CERTIFICADO, $142M sin clasificar
  BARRIERS: 6/7 activas (loader exists, source exists, but legal evidence missing)
```

### PARIS — Traceability Variant

```
PARIS
  │
  ├── Transacciones/Dropshipping/transactions_report_*.xlsx
  │     └── PAGO: "Venta" + monto
  │     └── CARGO: "Devolucion" + monto
  │     → folio_xml = "5372" (de columna "Número factura")
  │
  ├── Transacciones/Fulfillment/1 ene 2026 - 30 abr 2026.xlsx
  │     └── PAGO/CARGO similar
  │
  └── Facturacion/dteproveedor_5372.xml (54 files)
        → Bridge methodology: 32/32 folios matched
        → folio_xml poblado en LIVE DB (Sprint A2)

  CHAIN LENGTH: 5/6 links  →  PARTIAL (XML bridge complete, but 22 unmatched)
  COVERAGE: ~51.1% (32 of 54 XMLs bridged, covering $193.3M of $378.1M)
```

### FALABELLA — Traceability Variant

```
FALABELLA
  │
  ├── Órdenes y Transacciones/Ordenes_y_Transacciones_Falabella_Mar2026.xlsx
  │     └── PAGO/CARGO
  │     → folio_xml = "E001" (de columna "Documento Tributario")
  │
  └── Documentos Recepcionados/ (4 XML files, identical to ML/ shared)

  CHAIN LENGTH: 4/6 links  →  PARTIAL (4 XMLs shared with ML)
  COVERAGE: 5 folio_xml values, 0% CERTIFICADO
  VOLUME: 1,008 rows, $2.6M (smallest marketplace)
```

### Chain Comparison

| Link | ML | RIPLEY | PARIS | FALABELLA |
|---|---|---|---|---|
| N1: Marketplace | ✅ | ✅ | ✅ | ✅ |
| N2: Source file | ✅ (XLSX) | ✅ (XLSX) | ✅ (XLSX) | ✅ (XLSX) |
| N3: XML evidence | ✅ (762 files) | ⚠️ (100 files, 8.9%) | ✅ (54 files) | ⚠️ (4 files, shared) |
| N4: Concept | ✅ | ✅ | ✅ | ✅ |
| N5: Ledger | ✅ (101,603 rows) | ✅ (269,216 rows) | ✅ (~42K rows) | ✅ (1,008 rows) |
| N6: Financial Close | ✅ | ✅ (partial) | ✅ | ✅ |

---

## FASE 2 — EVIDENCE NODES

### Node Types

```
EVIDENCE NODE TYPES:

  CSV     Raw transaction dump from marketplace
          → RIPLEY: 47 files (Archivos de pedido BK) — NOT loaded by ETL
          → Backup/archive only, no pipeline consumption

  XLSX    Structured financial report from marketplace
          → ML: 41 files (ML_Facturacion) + 7 files (Poscobro) + 29 files (Liberaciones)
          → RIPLEY: 46 files (Resumen financiero)
          → PARIS: 29 files (Dropshipping) + 2 files (Fulfillment)
          → FALABELLA: 2 files (Órdenes y Transacciones)
          → TOTAL: 156 XLSX source files

  XML     Legal DTE (Documento Tributario Electrónico)
          → ML: 762 files (Documentos Recepcionados)
          → RIPLEY: 100 files (Documentos Recepcionados)
          → PARIS: 54 files (Facturacion)
          → FALABELLA: 4 files (Documentos Recepcionados, shared with ML)
          → TOTAL: 920 XML files

  LEDGER  Standardized financial record (marketplace_ledger_v1)
          → 414,314 rows, $1.5B total
          → Columns: marketplace, id_transaccion, id_orden, fecha, detalle, monto,
                      tipo_movimiento, archivo_origen, folio_xml, estado_xml

  CLASS   Classified ledger (marketplace_ledger_clasificado_v1)
          → 414,314 rows (same cardinality)
          → Adds: clasificacion_operativa, financial_group, include_in_operational_pnl
          → The bridge between raw data and financial meaning

  CLOSE   Financial closing (marketplace_cierre_financiero_v1)
          → Period-level aggregation
          → Columns: marketplace, periodo_inicio, periodo_fin,
                      total_ingresos, total_costos_operacionales,
                      total_costos_comerciales, total_ajustes, resultado_neto
```

### Evidence Node Schema

```typescript
interface EvidenceNode {
  /** Unique node identifier: {marketplace}-{type}-{id} */
  node_id: string;
  
  /** Node type */
  type: 'csv' | 'xlsx' | 'xml' | 'ledger' | 'classification' | 'financial_close' | 'audit';
  
  /** Marketplace */
  marketplace: 'ML' | 'RIPLEY' | 'PARIS' | 'FALABELLA';
  
  /** File path (for source files) or table name (for DB records) */
  location: string;
  
  /** Timestamp or period */
  timestamp: string;
  
  /** Number of rows/records */
  row_count: number;
  
  /** Total monetary value (if applicable) */
  total_value: number | null;
  
  /** Hash/checksum (for file integrity) */
  fingerprint: string | null;
  
  /** Child evidence nodes (forward links) */
  children: string[];
  
  /** Parent evidence nodes (backward links) */
  parents: string[];
  
  /** Link to next node in chain */
  next_node_id: string | null;
  
  /** Link to previous node in chain */
  prev_node_id: string | null;
  
  /** Confidence that this node is correctly linked */
  confidence: 0 | 0.25 | 0.5 | 0.75 | 0.9 | 1.0;
}
```

### Node Relationships

```
FILE NODES (CSV/XLSX/XML)
  │
  │  parent: null
  │  child:  ledger_entry
  │  confidence: 1.0 (file exists and was parsed)
  │
  ▼
LEDGER NODE (marketplace_ledger_v1 row)
  │
  │  parent: source_file
  │  child:  classification
  │  confidence: 1.0 (record exists)
  │
  ▼
CLASSIFICATION NODE (marketplace_ledger_clasificado_v1 row)
  │
  │  parent: ledger_entry
  │  child:  financial_close
  │  confidence: 0.5-1.0 (depends on mapping certainty)
  │
  ▼
FINANCIAL CLOSE NODE (marketplace_cierre_financiero_v1 row)
  │
  │  parent: classification
  │  child:  null (terminal node)
  │  confidence: 1.0 (aggregation is deterministic)
  │
```

### Additional Links

```
XML → DTE TRUTH (dte_truth_v1)
  │
  │  link_type: "legal_evidence"
  │  confidence: 1.0 (parsed from XML file)
  │  relation: folio → folio_xml
  │
  ▼
LEDGER ↔ DTE TRUTH
  │
  │  link_type: "xml_certification"
  │  confidence: 1.0 if folio_xml matches dte_truth
  │              0.0 if folio_xml NOT in dte_truth (SIN_RECURSO_XML)
  │  relation: ledger.folio_xml ↔ dte_truth.folio
```

---

## FASE 3 — EXPLAINABILITY CONTRACT

### Standard Response Schema

For any financial figure, the system must answer 6 questions. The response format:

```json
{
  "figure": {
    "value": 927759.0,
    "currency": "CLP",
    "marketplace": "ML",
    "period": "2026-04"
  },
  "explanations": {
    "what": {
      "answer": "Resultado neto del cierre financiero de Mercado Libre para abril 2026",
      "category": "resultado_neto",
      "subcategory": "operational_pnl"
    },
    "how_much": {
      "answer": "$927,759 CLP",
      "components": [
        {"name": "Ingresos", "value": 1000000.0, "percentage": 107.8},
        {"name": "Costos operacionales", "value": -72241.0, "percentage": -7.8}
      ],
      "excluded": [
        {"name": "Ajustes (mediación)", "value": 18331.0, "reason": "include_in_operational_pnl = FALSE"},
        {"name": "Ajustes (cashback)", "value": 0.0, "reason": "include_in_operational_pnl = FALSE"}
      ]
    },
    "from_where": {
      "answer": "Transacci\u00f3n TX-2026-04-ML-000001",
      "path": [
        {"node": "2026_04.xlsx", "type": "xlsx", "row": 42},
        {"node": "Cargo por venta (Venta)", "type": "concept", "confidence": 1.0},
        {"node": "marketplace_ledger_v1", "type": "ledger", "row_id": "TX-2026-04-ML-000001"},
        {"node": "marketplace_ledger_clasificado_v1", "type": "classification", "financial_group": "ingresos"},
        {"node": "marketplace_cierre_financiero_v1", "type": "close", "period": "2026-04"}
      ]
    },
    "why": {
      "answer": "Venta de producto SKU-123456 a trav\u00e9s de Mercado Libre",
      "driver": "transaccion_venta",
      "classification_basis": "Raw detail 'Cargo por venta (Venta)' matched to 'ingresos' via FINANCIAL_STRUCTURE mapping",
      "xml_evidence": {
        "folio": "033-0013380337",
        "status": "CERTIFICADO",
        "xml_file": "DTE_762.xml",
        "dte_amount": 1000000.0,
        "match_confidence": 1.0
      }
    },
    "where_impacts": {
      "answer": "Cierre financiero ML abril 2026",
      "downstream": [
        {"table": "marketplace_cierre_financiero_v1", "field": "total_ingresos", "impacted_value": 1000000.0},
        {"table": "vw_dashboard_kpis", "field": "total_sales_internal"},
        {"table": "marketplace_auditoria_v1", "check": "cargo_sin_respaldo_legal", "status": "PASSED"}
      ]
    },
    "evidence": {
      "sources": [
        {"type": "xlsx", "path": "01_Raw/ML/ML_Facturacion/2026_04.xlsx", "rows": 5234},
        {"type": "xml", "path": "01_Raw/ML/Documentos Recepcionados/DTE_762.xml", "folio": "033-0013380337"},
        {"type": "csv", "path": null, "note": "No CSV sources for ML"}
      ],
      "ledger_rows": 1,
      "classification_rows": 1,
      "close_rows": 1,
      "audit_findings": 0,
      "overall_confidence": 1.0
    }
  }
}
```

### Mandatory Questions

| # | Question | Meaning | Required Fields |
|---|---|---|---|
| 1 | **¿QUÉ es?** | Nature of the figure | category, subcategory, description |
| 2 | **¿CUÁNTO es?** | Monetary value + components | value, components, excluded |
| 3 | **¿DE DÓNDE viene?** | Source trace (file → ledger) | path nodes, origin |
| 4 | **¿POR QUÉ existe?** | Business reason + classification basis | driver, classification_basis, xml_evidence |
| 5 | **¿DÓNDE impacta?** | Downstream effect (close, audit) | downstream tables, impacted fields |
| 6 | **¿Qué evidencia lo respalda?** | All source files + confidence | sources, overall_confidence |

### Contract Rules

1. **Every figure must answer all 6 questions.** Partial answers are not allowed.
2. **Null/unknown answers must be explicit.** "Sin evidencia XML" > omitting the field.
3. **Confidence must be reported at every link level.** Not just overall.
4. **Excluded components must be visible.** Not hidden from the user.
5. **Source files must be linkable.** Full path + row number when possible.
6. **The contract is read-only.** Explanations do not modify data.

---

## FASE 4 — RIPLEY PILOT

### Example 1: "Importe del pedido" (Ingreso)

```
CIFRA: $1,234,567 CLP — Importe del pedido
PERIODO: 2026-04
LIQUIDACIÓN: 000312-2815

CHAIN:
  ┌─ RIPLEY
  │
  ├── Resumen financiero/000312-2815.xlsx
  │     ├── Fila 15: Orden de compra = "OC-2024-001234"
  │     ├── Columna: Importe del pedido = $1,234,567
  │     └── Columna: A pagar = $987,654
  │
  ├── Número documento liquidación = "312"
  │     → ledger.folio_xml = "312"
  │     → Estado XML: SIN_RECURSO_XML (no hay XML para este folio en dte_truth_v1)
  │
  ├── marketplace_ledger_v1
  │     → id_transaccion = "RIPLEY-2026-04-000312-001234"
  │     → detalle = "Importe del pedido"
  │     → monto = +$1,234,567
  │     → tipo_movimiento = "INGRESO_VENTA"
  │
  ├── marketplace_ledger_clasificado_v1
  │     → clasificacion_operativa = "Venta" (mapped via RAW_TO_CLASSIFICATION_MAP)
  │     → financial_group = "ingresos"
  │     → include_in_operational_pnl = TRUE
  │     → confianza_clasificacion = 0.95
  │
  └── marketplace_cierre_financiero_v1
        → periodo = 2026-04
        → total_ingresos = includes this $1,234,567

CONFIDENCE: 0.85
  - Source file: 1.0 (file exists, parsed successfully)
  - XML evidence: 0.0 (no XML match for folio "312")
  - Classification: 0.95 (mapped via established rule)
  - Aggregation: 1.0 (deterministic SUM)
  - OVERALL: 0.85 — Strong financial evidence, weak legal evidence
```

### Example 2: "Comisión" (Costo Comercial)

```
CIFRA: -$246,913 CLP — Comisión
PERIODO: 2026-04
LIQUIDACIÓN: 000312-2815

CHAIN:
  ┌─ RIPLEY
  │
  ├── Resumen financiero/000312-2815.xlsx
  │     └── Columna: Comisión = -$246,913
  │
  ├── marketplace_ledger_v1
  │     → detalle = "Comisión"
  │     → monto = -$246,913
  │     → tipo_movimiento = "EGRESO_COMISION"
  │
  ├── marketplace_ledger_clasificado_v1
  │     → clasificacion_operativa = "Comisiones"
  │     → financial_group = "costos_comerciales"
  │     → include_in_operational_pnl = TRUE
  │
  └── marketplace_cierre_financiero_v1
        → total_costos_comerciales = includes -$246,913

CONFIDENCE: 0.88
  - Source: 1.0  |  XML: 0.0  |  Classification: 0.95  |  Aggregation: 1.0
  - OVERALL: 0.88
  - Note: Commission always classified deterministically, no ambiguity
```

### Example 3: "Pedidos reembolsados" (Devolución)

```
CIFRA: -$100,000 CLP — Pedidos reembolsados
PERIODO: 2026-04
LIQUIDACIÓN: 000312-2815

CHAIN:
  ┌─ RIPLEY
  │
  ├── Resumen financiero/000312-2815.xlsx
  │     └── Columna: Pedidos reembolsados = -$100,000
  │
  ├── marketplace_ledger_v1
  │     → detalle = "Pedidos reembolsados"
  │     → monto = -$100,000
  │     → tipo_movimiento = "DEVOLUCION"
  │
  ├── marketplace_ledger_clasificado_v1
  │     → clasificacion_operativa = "Devolucion"
  │     → financial_group = "devoluciones"
  │     → include_in_operational_pnl = TRUE
  │
  └── marketplace_cierre_financiero_v1
        → total_devoluciones = includes -$100,000

CONFIDENCE: 0.80
  - Source: 1.0  |  XML: 0.0  |  Classification: 0.85  |  Aggregation: 1.0
  - OVERALL: 0.80
  - Note: Devoluciones without XML backing have lower classification confidence
```

### Example 4: "A pagar" (Net Payable)

```
CIFRA: $987,654 CLP — A pagar (Importe del pedido - Comisión)
PERIODO: 2026-04
LIQUIDACIÓN: 000312-2815

CHAIN:
  ┌─ RIPLEY
  │
  ├── Resumen financiero/000312-2815.xlsx
  │     ├── Fila: Importe del pedido = $1,234,567
  │     ├── Fila: Comisión = -$246,913
  │     └── Columna: A pagar = $987,654 (derived: 1,234,567 - 246,913)
  │
  ├── marketplace_ledger_v1
  │     ├── INGRESO: $1,234,567 (Importe del pedido)
  │     ├── EGRESO: -$246,913 (Comisión)
  │     └── (A pagar is NOT a ledger row — it's a COMPUTED figure)
  │
  ├── marketplace_ledger_clasificado_v1
  │     ├── Ingreso → "ingresos"
  │     └── Comisión → "costos_comerciales"
  │
  └── marketplace_cierre_financiero_v1
        → resultado_neto = $987,654 (1,234,567 - 246,913 + 0 - 0)

  CONFIDENCE: 0.88
  - Source: 1.0  |  XML: 0.0  |  Classification: 0.95/0.95  |  Aggregation: 1.0
  - OVERALL: 0.88
  - Note: "A pagar" is the net result of multiple ledger rows.
          It does NOT exist as a single record — it's reconstructed.
```

### RIPLEY Chain Gap Summary

| Concept | Evidence Level | XML Gap | Impact |
|---|---|---|---|
| Importe del pedido | Strong (XLSX + Classification) | No XML (0%) | Can explain WHAT and HOW MUCH, not WHY legally |
| Comisión | Strong | No XML | Same. Business logic is clear, legal backing missing |
| Devolución | Medium | No XML | Refunds need XML for tax reconciliation |
| A pagar | Strong (derived) | N/A | Computed, not stored. Requires dynamic reconstruction |

**Key insight for RIPLEY**: The system can explain **financial operations** (what happened, how much, where it impacts) but cannot explain **legal compliance** (why it's justified, which DTE supports it). This distinction must be clear in the UI.

---

## FASE 5 — VISUAL FLOW

### Conceptual View

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FINANCIAL FIGURE                             │
│                                                                     │
│  $927,759 CLP  │  Resultado neto  │  ML  │  2026-04                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  COMPONENTS             │   │  EXCLUDED               │
│                         │   │                         │
│  Ingresos    $1,000,000 │   │  Mediación   $18,331    │
│  Costos Op.   -$72,241  │   │  Cashback        $0     │
│                         │   │                         │
│  NETO:       $927,759   │   │                         │
└─────────────────────────┘   └─────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EXPLANATION PATH                                                    │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  File    │ →  │  Ledger  │ →  │  Class   │ →  │  Close   │      │
│  │  XLSX    │    │  Row     │    │  Group   │    │  Period  │      │
│  │  2026_04 │    │  TX-0001 │    │ ingresos │    │  2026-04 │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│                                                                     │
│  ┌──────────┐    ┌──────────┐                                       │
│  │  XML     │ →  │  DTE     │                                       │
│  │  033-001 │    │  Truth   │                                       │
│  │  3380337 │    │  CERTIF  │                                       │
│  └──────────┘    └──────────┘                                       │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CONFIDENCE                                                        │
│                                                                     │
│  ● Source File:  ████████░░ 0.80                                    │
│  ● XML Evidence: ████████░░ 0.80                                    │
│  ● Classification: ██████████ 1.00                                   │
│  ● Aggregation:  ██████████ 1.00                                    │
│  ───────────────────────────────────                                │
│  ● OVERALL:      █████████░ 0.90                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Visual Components Definition

```typescript
interface VisualFlow {
  /** The figure being explained */
  figure: {
    value: number;
    currency: string;
    marketplace: string;
    period: string;
    label: string;
  };

  /** Breakdown tree of components */
  components: VisualComponent[];

  /** Items excluded from this figure */
  excluded: VisualExclusion[];

  /** Ordered evidence path */
  path: VisualPathNode[];

  /** Confidence bar per dimension */
  confidence: VisualConfidence[];
}

interface VisualComponent {
  name: string;
  value: number;
  percentage: number;  // relative to total
  financial_group: string;
  color: string;       // semantic color (green=income, red=cost)
  drill_down: VisualPathNode[];  // click to expand
}

interface VisualExclusion {
  name: string;
  value: number;
  reason: string;      // why excluded (e.g., "Non-operational P&L")
}

interface VisualPathNode {
  type: 'file' | 'database' | 'concept' | 'close';
  label: string;
  detail: string;
  confidence: number;
  actionable: boolean;  // can user click to open/download?
  link?: string;        // file path or query
  icon: string;         // visual icon
}

interface VisualConfidence {
  dimension: string;
  score: number;        // 0.0 to 1.0
  description: string;
}
```

### Layout Rules

1. **Figure at top**: largest font, destacado
2. **Components below**: bar chart with color coding (green/red/gray)
3. **Excluded items**: visually separated with dimmed opacity and reason badge
4. **Path**: horizontal timeline left-to-right, each node clickable
5. **Confidence**: stacked horizontal bars, overall at bottom with bold border
6. **NO scroll** for the primary view — all 5 sections fit in one viewport
7. **Secondary views** open on click (drill-down: full file list, row-by-row detail)

---

## FASE 6 — CONFIDENCE MODEL

### Confidence Levels

| Level | Score | Meaning | Example |
|---|---|---|---|
| **CERTIFIED** | 1.0 | Document + ledger match perfectly | ML row with folio_xml in dte_truth_v1, estado_xml = 'CERTIFICADO' |
| **VERIFIED** | 0.90 | Document linked indirectly | PARIS bridge match (folio from Excel → XML exists in facturación) |
| **MATCHED** | 0.75 | Matched by period/amount heuristic | xml_matcher.py: amount ± 7 days matched but no direct folio link |
| **CLASSIFIED** | 0.50 | Classification exists, no document link | RIPLEY row: classified but 0% XML coverage |
| **RAW** | 0.25 | Ingested but unclassified | marketplace_ledger_v1 row with detalle not in any mapping |
| **ORPHAN** | 0.0 | Source file missing or corrupted | 7 RIPLEY facturas not loaded ($50.5M gap) |

### Confidence Calculation

```
OVERALL_CONFIDENCE = 0.30 × SOURCE_CONFIDENCE
                   + 0.25 × XML_CONFIDENCE
                   + 0.25 × CLASSIFICATION_CONFIDENCE
                   + 0.20 × AGGREGATION_CONFIDENCE

Where:
  SOURCE_CONFIDENCE        = 1.0 if source file exists and was parsed
                             0.0 if source file missing or parsing failed

  XML_CONFIDENCE           = 1.0 if folio_xml in dte_truth_v1 (CERTIFICADO)
                             0.9 if bridge match (PARIS methodology)
                             0.5 if heuristic match (amount + date window)
                             0.0 if no XML link exists

  CLASSIFICATION_CONFIDENCE = confianza_clasificacion from DB
                              (0.50-1.00 depending on mapping certainty)
                              0.25 if detalle = 'NO_CLASIFICADO'

  AGGREGATION_CONFIDENCE   = 1.0 for deterministic aggregation (SUM)
                             0.9 for computed figures (A pagar, neto derivado)
```

### Per-Marketplace Confidence Baseline

| Marketplace | Source | XML | Class | Aggregation | **Overall** |
|---|---|---|---|---|---|
| **ML** | 1.0 | 0.90 (89.4% folio_xml) | 0.95 | 1.0 | **0.96** |
| **RIPLEY** | 1.0 | 0.0 (0% CERTIFICADO) | 0.85 | 1.0 | **0.71** |
| **PARIS** | 1.0 | 0.75 (51.1% bridge) | 0.90 | 1.0 | **0.91** |
| **FALABELLA** | 1.0 | 0.50 (4 XMLs, no CERT) | 0.80 | 1.0 | **0.83** |

### Confidence Display Rules

1. **Always display overall confidence** as a percentage (0-100%)
2. **Always display dimension breakdown** (source, xml, class, aggregation)
3. **Confidence < 70%** should show a warning indicator
4. **Confidence < 50%** should show a blocking warning + explanation
5. **Each dimension can be clicked** to see why that score was assigned
6. **Missing evidence** (0% XML) must be visible, not hidden in aggregate

---

## FASE 7 — PRODUCT VALUE

### Questions the System Answers That Excel Cannot

| # | Question | Excel | This System |
|---|---|---|---|
| 1 | "This $1.5M figure — what transactions compose it?" | Manual VLOOKUP across 4 marketplaces | ONE query: `WHERE financial_group = 'ingresos' AND periodo = '2026-04'` |
| 2 | "Show me the XML that justifies this specific line item" | Manual file search through 920 XMLs | Click → `folio_xml` → `dte_truth_v1` → XML path → file preview |
| 3 | "What is the confidence of this financial close?" | Not computable | 0.96 — calculated from 4 dimensions automatically |
| 4 | "Which transactions lack legal backing?" | Manual cross-reference of 414K rows against 920 XMLs | WHERE `folio_xml IS NULL` OR `estado_xml = 'SIN_RECURSO_XML'` |
| 5 | "Trace this $50.5M gap: which marketplaces, periods, concepts?" | Manual pivot table construction | Pre-built evidence chain with gap analysis per dimension |
| 6 | "What changed between last month's close and this month's?" | Manual snapshot comparison | Versioned comparisons with per-concept delta |
| 7 | "Which classification rules need updating?" | Manual audit of 231 mappings | `marketplace_auditoria_v1` with `MOVIMIENTOS_NO_CLASIFICADOS` alerts |

### Questions the System Answers That Power Query Cannot

| # | Question | Power Query | This System |
|---|---|---|---|
| 1 | "Link a financial transaction to its legal XML document" | Requires custom M code per marketplace | Built-in: `folio_xml` → `dte_truth_v1` across ALL marketplaces |
| 2 | "Show the end-to-end evidence chain for a figure" | Manual step-by-step rebuild | 6-question Explainability Contract — automatic |
| 3 | "What is the confidence score of this number?" | Not a Power Query concept | 4-dimension weighted model, computed per row and per aggregation |
| 4 | "Which numbers are audit-proof?" | Manual verification | `estado_xml = 'CERTIFICADO'` → `confidence > 0.90` |
| 5 | "Compare evidence quality across 4 marketplaces" | Not possible without custom schema | Per-marketplace confidence dashboard |
| 6 | "Exclude non-operational items from P&L" | Requires manual filtering rules | `include_in_operational_pnl` flag — single WHERE clause |
| 7 | "What would happen if we reclassified this concept?" | Manual what-if analysis | Classification preview with impact on close (SIMULATE mode) |

### Core Value Proposition

```
FOR AUDITORS:
  → "Show me the evidence for any number in 1 click"
  → "Which numbers are audit-ready? Which need work?"
  → "Export the complete evidence chain as PDF for audit trail"

FOR ACCOUNTANTS:
  → "Reconcile marketplace reports against bank statements automatically"
  → "Monthly close in minutes instead of days"
  → "Trace any variance to its transactional root cause"

FOR MARKETPLACES:
  → "Which fees are being charged? Are they correct?"
  → "Show me my net revenue after all costs per product category"
  → "Which periods have missing XML documentation?"

FOR MANAGEMENT:
  → "What is our real P&L across all 4 marketplaces combined?"
  → "How trustworthy is each number? (0-100% confidence)"
  → "Where should we invest in data quality improvement?"
```

### Differentiation vs Power Query

| Capability | Power Query | Financial Evidence Chain |
|---|---|---|
| Data extraction | ✅ Yes (from any source) | ✅ Yes (4 marketplaces, 3 file formats) |
| Data transformation | ✅ Yes (M language) | ✅ Yes (ETL pipeline) |
| Data modeling | ⚠️ Manual (star schema) | ✅ Built-in (6-layer evidence architecture) |
| Lineage tracking | ❌ No | ✅ Full chain: file → ledger → classification → close |
| XML integration | ❌ Manual | ✅ Built-in (920 XMLs, folio_xml bridge) |
| Confidence scoring | ❌ No | ✅ 4-dimension weighted model |
| Explainability | ❌ No | ✅ 6-question standard contract |
| Audit certification | ❌ No | ✅ CERTIFICADO / SIN_RECURSO_XML per row |
| Cross-marketplace | ❌ Separate queries | ✅ Unified ledger (4 MPs, 1 schema) |
| Versioned snapshots | ❌ No | ✅ 18 snapshots (V2→V6) |

### Commercial Summary

```
THE PRODUCT: Financial Evidence Chain (this design)
THE MARKET: Marketplace operators, auditors, accountants managing
            multi-marketplace financial operations
THE PROBLEM (solved): Financial data was scattered across 4+ marketplaces,
             920 XML files, 156 XLSX files, 47 CSV files.
             No single source of truth. No audit trail. No confidence metric.
             Marketplace Financial (DuckDB + API + Dashboard) now resolves
             this — see governance/TRUTH_CONSOLIDATION_APPROVAL.md (DEC-001).
THE SOLUTION: A unified evidence chain from source document to financial close,
              with per-row confidence scoring and one-click explainability.
THE MOAT: Multi-marketplace normalization + XML legal evidence linking +
           confidence model + explainability contract.
           Cannot be replicated with Excel or Power Query alone.
```

---

## ANNEX: GLOSSARY

| Term | Definition |
|---|---|
| Evidence Chain | End-to-end path from source file to financial close |
| Evidence Node | A single point in the chain (file, ledger row, classification, close) |
| Explainability Contract | The 6-question standard response for any figure |
| Confidence Score | 0-100% weighted metric per figure (source × XML × class × aggregation) |
| folio_xml | The key linking ledger rows to XML DTE evidence |
| estado_xml | 'CERTIFICADO' (verified) / 'SIN_RECURSO_XML' (no match) |
| Financial Group | High-level category: ingresos, costos_operacionales, costos_comerciales, ajustes, devoluciones |
| include_in_operational_pnl | Boolean flag: TRUE = operational P&L, FALSE = excluded (risk/adjustment) |
| Bridge | Cross-reference methodology (e.g., PARIS: Excel "folio" → XML "folio") |
| CERTIFIED | Maximum confidence level (1.0): document + ledger match perfectly |

---

**Document designed by**: Sprint B2 — Financial Evidence Chain
**Regime**: ARQUITECTURA — READ ONLY
**Status**: Design complete — ready for implementation planning
