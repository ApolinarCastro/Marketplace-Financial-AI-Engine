# TRANSACTION TRACEABILITY CONTRACT
## Canonical Transaction View — Derived, Not Stored

**Version:** 1.0
**Status:** IMPLEMENTED (derived view contract)
**Source of Truth:** `marketplace_ledger_v1`, `marketplace_ledger_clasificado_v1`, `marketplace_cierre_financiero_v1`

---

## Purpose

Define the canonical transaction structure for the Marketplace Financial AI Engine. This contract specifies how every financial transaction is represented, traced, and verified across the entire evidence chain: RAW → ETL → Ledger → Classification → Cierre → XML → Settlement → Bank.

This is a **DERIVED view contract**. It produces a unified read-only projection of transactions from existing certified tables. It never stores data, never modifies certified tables, and never duplicates financial logic.

---

## Canonical Fields

### Core Identity

| Field | Type | Description |
|---|---|---|
| `transaction_id` | VARCHAR | Unique identifier per marketplace. Constructed from certified source columns. |
| `marketplace` | VARCHAR | One of: `ML`, `PARIS`, `RIPLEY`, `FALABELLA`, `SHOPIFY`, `SAP` |
| `transaction_type` | VARCHAR | Type: `Venta`, `Comisión`, `Envío`, `Publicidad`, `Bonificación`, `Devolución`, `Fulfillment`, `Otros cargos` |
| `transaction_date` | DATE | Date of the transaction |

### Product / Item

| Field | Type | Description |
|---|---|---|
| `sku` | VARCHAR | Stock keeping unit |
| `quantity` | INTEGER | Number of units |

### Financial

| Field | Type | Description |
|---|---|---|
| `amount` | DECIMAL(18,2) | Signed monetary value: positive = income, negative = cost/refund. |
| `currency` | VARCHAR(3) | ISO 4217 currency code. Default: `CLP`. |

### Source Traceability

| Field | Type | Description |
|---|---|---|
| `source_file` | VARCHAR | Original raw file that produced this record. Derived from `archivo_origen` or `folio_xml` metadata. |
| `source_row` | INTEGER | Row index within the source file. |
| `raw_detail` | VARCHAR | Original raw detail string from source. Maps to `detalle` in ledger. |
| `normalized_detail` | VARCHAR | Result of `normalize_detail()` processing — the canonical detail label. |

### Classification (from certified engine)

| Field | Type | Description |
|---|---|---|
| `classification` | VARCHAR | Canonical concept name. Maps to `clasificacion_operativa` in `marketplace_ledger_clasificado_v1`. |
| `financial_group` | VARCHAR | One of: `ingresos`, `devoluciones`, `costos_operacionales`, `costos_comerciales`, `ajustes`, `recuperaciones_y_bonificaciones`. Derived from `LOWER(financial_group)`. |
| `include_in_operational_pnl` | BOOLEAN | Whether the transaction contributes to operational P&L. From `COALESCE(include_in_operational_pnl, 1)`. |

### Trace Status

| Field | Type | Description |
|---|---|---|
| `trace_status` | VARCHAR | One of: `UNTRACED`, `TRACED`, `VERIFIED`, `BROKEN`. |
| `evidence_chain` | JSON | Ordered list of evidence steps: `["RAW", "ETL", "Ledger", "Classification", "Cierre", "XML", "Settlement", "Bank"]`. Each step includes status and reference. |

### Alternative Identifiers (optional, marketplace-dependent)

| Field | Type | Marketplace | Description |
|---|---|---|---|
| `order_id` | VARCHAR | All | Platform order identifier |
| `package_id` | VARCHAR | ML, RIPLEY | Shipping package identifier |
| `payment_id` | VARCHAR | ML | Payment transaction identifier |
| `settlement_id` | VARCHAR | ML | Settlement batch identifier |
| `sap_sales_order` | VARCHAR | SAP | SAP sales order number |
| `document_number` | VARCHAR | All | DTE folio or invoice number. Maps to `folio_xml` in ledger. |

---

## Implementation Rules

### 1. Derived View Only

This contract MUST be implemented as a **SQL VIEW** or a **Python-derived read-only table function**. It must never be materialized as a persistent table. It must never be written to.

### 2. Source Tables (Read-Only)

Only the following certified tables may be queried:

- `marketplace_ledger_v1` — transaction identity, financial amounts, source metadata
- `marketplace_ledger_clasificado_v1` — classification and operational P&L flag
- `marketplace_cierre_financiero_v1` — closing period validation

No other tables may be used. No JOINs to raw files.

### 3. Identity Construction

`transaction_id` is constructed by hashing or concatenating:
- `marketplace` (lowercase)
- `id_transaccion` (from `marketplace_ledger_v1`)
- `detalle` (from `marketplace_ledger_v1`)

This guarantees uniqueness per marketplace even when the same `id_transaccion` appears under multiple `detalle` values (e.g., paired mechanisms in ML).

### 4. Classification Mapping

`classification` is derived by LEFT JOIN to `marketplace_ledger_clasificado_v1` ON:
- `marketplace_ledger_v1.id_transaccion = marketplace_ledger_clasificado_v1.id_transaccion`

When no classification row exists, `classification` defaults to `'NO_CLASIFICADO'` and `include_in_operational_pnl` defaults to `1`.

### 5. Financial Group Case Normalization

`financial_group` is always normalized to lowercase via `LOWER()` to handle RIPLEY's uppercase storage (`INGRESOS`, `DEVOLUCIONES`).

### 6. Transaction Type Mapping

`transaction_type` is derived from `financial_group` and `detalle` using the certified taxonomy files in `knowledge/taxonomy/`:

| financial_group | transaction_type |
|---|---|
| `ingresos` | `Venta` |
| `devoluciones` | `Devolución` |
| `costos_operacionales` | `Envío` or `Fulfillment` |
| `costos_comerciales` | `Comisión` |
| `ajustes` | `Otros cargos` or `Bonificación` |
| `recuperaciones_y_bonificaciones` | `Bonificación` |

### 7. Evidence Chain Construction

`evidence_chain` is a JSON array built dynamically:

```json
[
  {"step": "RAW", "status": "TRACED", "reference": "<source_file>"},
  {"step": "ETL", "status": "TRACED", "reference": "<archivo_origen>"},
  {"step": "Ledger", "status": "VERIFIED", "reference": "<id_transaccion>"},
  {"step": "Classification", "status": "<status>", "reference": "<clasificacion_operativa>"},
  {"step": "Cierre", "status": "<status>", "reference": "<periodo>"},
  {"step": "XML", "status": "<status>", "reference": "<folio_xml>"},
  {"step": "Settlement", "status": "UNTRACED", "reference": null},
  {"step": "Bank", "status": "UNTRACED", "reference": null}
]
```

Status per step:
- `VERIFIED` — evidence confirmed at this level
- `TRACED` — evidence exists but not yet verified
- `UNTRACED` — no evidence source available for this step
- `BROKEN` — evidence chain is inconsistent

### 8. Normalization Function

`normalize_detail()` maps `raw_detail` (from `marketplace_ledger_v1.detalle`) to a canonical label using the taxonomy files. When no mapping exists, the raw value is passed through unchanged.

---

## Invariants

| # | Invariant | Enforcement |
|---|---|---|
| 1 | **Zero modification** to `marketplace_ledger_v1`, `marketplace_ledger_clasificado_v1`, or `marketplace_cierre_financiero_v1`. | Read-only contract. No INSERT/UPDATE/DELETE. |
| 2 | **Zero duplicate financial logic**. No recalculation of amounts, aggregates, or margins. | All financial values pass through directly from source tables. |
| 3 | **Zero recalculation** of financial aggregates (RN, costos, comisiones, etc.). | Aggregates consumed from `marketplace_cierre_financiero_v1` or computed by `FinancialEngine`. |
| 4 | **Every `transaction_id` must be unique per marketplace.** | Enforced by construction rule (see Implementation Rules §3). |
| 5 | **Every transaction must have at least one entry in the evidence chain.** | The RAW step is always populated from `archivo_origen` or `folio_xml`. |
| 6 | **DEC-019 must be preserved.** | `include_in_operational_pnl` is passed through as stored — never overridden. |
| 7 | **Single Financial Truth must be preserved.** | All figures are traceable to certified tables and match `marketplace_cierre_financiero_v1` at the aggregate level. |
| 8 | **Case-insensitive matching** for `marketplace` and `financial_group`. | All comparisons use `LOWER()`. |

---

## Relationship to Existing Model

### Certified Tables (Untouched)

```
marketplace_ledger_v1
├── transaction identity (id_transaccion, marketplace, detalle)
├── financial (monto, fecha)
├── traceability (folio_xml, archivo_origen)
└── operational flag (include_in_operational_pnl)

marketplace_ledger_clasificado_v1
├── classification (clasificacion_operativa, financial_group)
└── links to ledger via id_transaccion

marketplace_cierre_financiero_v1
├── closing periods
└── aggregate financial results
```

### Derived View (This Contract)

```
transaction_traceability (VIEW)
├── Canonical fields (flattened from 3 tables)
├── trace_status (computed)
├── evidence_chain (computed JSON)
└── alternative_ids (optional marketplace-specific)
```

### Taxonomy Files (Knowledge Layer)

```
knowledge/taxonomy/
├── ripley_v1.json    — 32 detalle values (12 SIGNAL / 20 NOISE)
├── ml_v1.json        — 71 detalle values (70 SIGNAL / 1 NOISE)
├── paris_v1.json     — 15 detalle values (14 SIGNAL / 1 NOISE)
└── falabella_v1.json — 16 detalle values (15 SIGNAL / 1 NOISE)
```

### Consumers

The derived view is consumed by:

- **Evidence Orchestrator** (`engine/v4/evidence/`) — traces individual transactions
- **Financial Copilot** (`engine/v4/copilot/`) — answers traceability questions
- **Lineage Engine** (`engine/v4/lineage/`) — per-transaction origin tracing
- **Executive Dashboard** (`/api/v4/exec/*`) — drill-down to individual transaction evidence
- **Certification Gate** (`tests/test_certification_gate.py`) — validates contract invariants

---

## Change Process

Any modification to this contract requires:

1. **RFC** documenting the proposed change
2. **Impact analysis** showing zero contamination of certified tables
3. **Taxonomy update** if new `detalle` values or transaction types are introduced
4. **Contract version bump** in this document
5. **Certification gate update** to enforce new invariants

This contract is immutable for derived-view purposes. No change may introduce:
- Write operations to certified tables
- Duplication of existing financial logic
- Recalculation of certified aggregates
- Violation of DEC-019 or Single Financial Truth
