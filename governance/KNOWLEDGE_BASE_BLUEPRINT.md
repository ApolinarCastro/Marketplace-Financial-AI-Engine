# KNOWLEDGE_BASE_BLUEPRINT.md — Knowledge Foundation Architecture

**Date:** 2026-06-05  
**Scope:** Unified knowledge layer for ML, PARIS, RIPLEY, FALABELLA, SHOPIFY  
**Status:** BLUEPRINT (no code, no DB, no pipeline changes)

---

## Architecture: 4 Knowledge Bases

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE KNOWLEDGE BASE                        │
│  Certifications · RFCs · Decisions · Rules · Protocols · Registry   │
└─────────────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
│  FINANCIAL KB    │  │  MARKETPLACE KB  │  │  ECOMMERCE KB       │
│  · Ledger truth  │  │  · MP taxonomy   │  │  · Event model      │
│  · P&L structure │  │  · Concept maps  │  │  · Fee structures   │
│  · KPI formulas  │  │  · Rate tables   │  │  · Loader specs     │
│  · Closing rules │  │  · XML bridges   │  │  · Channel rules    │
└─────────────────┘  └─────────────────┘  └─────────────────────┘
```

---

## 1. Financial Knowledge Base

The **certified source of truth** for all financial numbers.

### Entity: `financial_metric_v1`

| Campo | Tipo | Propósito | Ejemplo |
|-------|------|-----------|---------|
| `metric_id` | UUID | PK | `fin_001` |
| `marketplace` | TEXT | MP scope | `ML`, `RIPLEY`, `ALL` |
| `metric_name` | TEXT | Canonical name | `Ventas`, `Disponible` |
| `formula` | TEXT | Deterministic formula | `SUM(monto) WHERE financial_group='ingresos'` |
| `source_table` | TEXT | Source of truth | `marketplace_ledger_v1` |
| `source_filter` | TEXT | Row filter | `financial_group='ingresos'` |
| `kpi_group` | TEXT | Gerencial hierarchy | `ingresos`, `devoluciones`, `cobros`, `disponible` |
| `certification_ref` | TEXT | RFC that certified it | `DASHBOARD_DATABASE_CERTIFICATION.md` |
| `cash_role` | TEXT | Cash equivalence | `REAL_CASH`, `ACCRUAL`, `MIRROR` |
| `event_role` | TEXT | Event model role | `ROOT_EVENT`, `MECHANISM`, `STANDALONE` |
| `version` | INTEGER | Versioning | `1` |
| `valid_from` | DATE | Effective since | `2026-01-01` |
| `valid_to` | DATE | Deprecation | `NULL` (active) |
| `governance_status` | TEXT | Certification status | `CERTIFICADO`, `PENDIENTE` |

### Entity: `financial_structure_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `group_id` | TEXT | PK: `ingresos`, `devoluciones`, `costos_operacionales`, `costos_comerciales`, `ajustes`, `tesoreria` |
| `formula_expression` | TEXT | Deterministic SQL expression |
| `sign_convention` | TEXT | `POSITIVE`, `NEGATIVE`, `MIXED` |
| `closing_behavior` | TEXT | `SUM`, `NET_ZERO`, `EXCLUDE` |
| `certification_ref` | TEXT | RFC that certified this group |
| `immutable` | BOOLEAN | Whether structure is frozen |

### Entity: `kpi_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `kpi_id` | TEXT | PK |
| `kpi_name` | TEXT | `Ventas`, `Devoluciones`, `Cobros`, `Disponible` |
| `canonical_source` | TEXT | Which table is official |
| `formula` | TEXT | How to compute |
| `certification_level` | TEXT | `EXACTO`, `ESTIMADO`, `PENDIENTE` |
| `last_certified` | DATE | Date of last certification |

### Relaciones

```
financial_metric_v1 → financial_structure_v1 (by financial_group)
financial_metric_v1 → kpi_v1 (by kpi_group)
kpi_v1 → financial_metric_v1 (by formula components)
```

### Versionado

- Schema version tracked in `_version` field
- Changes require RFC + certification
- Historical versions preserved (no in-place mutation)
- All versions reference their certification RFC

### Gobernanza

- READ ONLY from application code
- Modified only via governance RFC process
- Changes require 14/14 regression pass
- All metrics require cash cross-check (Liberaciones or equivalent)

---

## 2. Marketplace Knowledge Base

The **source of truth for marketplace-specific taxonomy** — concept maps, rate tables, fee structures, XML bridges.

### Entity: `marketplace_concept_v1`

| Campo | Tipo | Propósito | Ejemplo |
|-------|------|-----------|---------|
| `concept_id` | UUID | PK | |
| `marketplace` | TEXT | MP scope | `ML`, `SHOPIFY` |
| `source_file` | TEXT | Original source | `2026_04.xlsx` |
| `raw_detail` | TEXT | Raw string from source | `"Cargo por venta (Comisión)"` |
| `canonical_name` | TEXT | Normalized classification | `Cargo por venta (Comisión)` |
| `financial_group` | TEXT | P&L group | `costos_comerciales` |
| `event_role` | TEXT | Event model | `ROOT_EVENT` |
| `cash_role` | TEXT | Cash evidence | `REAL_CASH` |
| `sign_convention` | TEXT | `+` (income), `-` (cost) | `-` |
| `tax_support` | TEXT | XML certification status | `CERTIFICADO`, `SIN_RECURSO` |
| `load_frequency` | TEXT | How often loaded | `MONTHLY`, `DAILY` |
| `loader_class` | TEXT | Which loader handles it | `load_facturacion` |
| `mapping_version` | INTEGER | Version of classification map | `1` |
| `certification_ref` | TEXT | Certification document | |

### Entity: `marketplace_rate_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `rate_id` | UUID | PK |
| `marketplace` | TEXT | MP |
| `concept` | TEXT | What is being charged |
| `rate_type` | TEXT | `PERCENTAGE`, `FIXED`, `TIERED` |
| `rate_value` | FLOAT | Numeric rate |
| `take_rate_group` | TEXT | Which component of take rate |
| `effective_from` | DATE | Rate effective start |
| `effective_to` | DATE | Rate effective end |
| `negotiable` | BOOLEAN | Whether rate is negotiable |
| `certification_ref` | TEXT | Evidence for this rate |

### Entity: `xml_bridge_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `bridge_id` | UUID | PK |
| `marketplace` | TEXT | MP |
| `folio_pattern` | TEXT | How folio is extracted from XML |
| `ledger_match_field` | TEXT | Which ledger column matches |
| `match_method` | TEXT | `EXACT`, `LIKE`, `COMPOSITE` |
| `coverage_pct` | FLOAT | % of ledger rows matched |
| `certification_ref` | TEXT | Certification status |

### Entity: `marketplace_loader_spec_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `loader_id` | UUID | PK |
| `marketplace` | TEXT | MP |
| `source_format` | TEXT | `XLSX`, `CSV`, `XML`, `API` |
| `file_pattern` | TEXT | Glob pattern for source files |
| `expected_columns` | TEXT | Column schema expected |
| `sign_rules` | TEXT | How sign convention is applied |
| `date_column` | TEXT | Which column is the date |
| `date_format` | TEXT | `dayfirst`, `monthfirst`, etc. |
| `id_generation` | TEXT | How id_transaccion is built |
| `folio_extraction` | TEXT | How folio_xml is populated |

### Relaciones

```
marketplace_concept_v1 → marketplace_rate_v1 (by marketplace + concept)
marketplace_concept_v1 → xml_bridge_v1 (by marketplace)
marketplace_concept_v1 → marketplace_loader_spec_v1 (by marketplace)
marketplace_concept_v1 → financial_kb → financial_metric_v1 (by canonical_name)
```

### Versionado

- Concept maps are versioned (mapping_version)
- Rate changes tracked via effective dates
- Loader specs versioned when schema changes
- XML bridge coverage recertified per batch

### Gobernanza

- New concepts require certification (classification match, financial group assignment)
- Rate changes require negotiation document + certification
- Loader spec changes require 14/14 regression
- XML bridges recertified when new XML batch arrives

---

## 3. Ecommerce Knowledge Base

The **canonical event model** — universal across all channels (marketplaces + direct ecommerce).

### Entity: `event_model_v1`

| Campo | Tipo | Propósito | Ejemplo |
|-------|------|-----------|---------|
| `event_id` | UUID | PK | |
| `marketplace` | TEXT | MP or ecommerce | `ML`, `SHOPIFY` |
| `id_orden` | TEXT | Order identifier | `#10018` |
| `id_transaccion` | TEXT | Transaction | `ADJ_{order_id}_{idx}` |
| `concept` | TEXT | Canonical concept | `Ajuste por Talla/Garantía` |
| `event_role` | TEXT | ROOT_EVENT / MECHANISM / STANDALONE | `ROOT_EVENT` |
| `pair_id` | TEXT | Paired transaction if MECHANISM | `ADJ_{order}_{idx}` |
| `amount` | FLOAT | Monetary amount | `-15,000` |
| `cash_role` | TEXT | `REAL_CASH`, `ACCRUAL`, `MIRROR_ZERO` |
| `pnl_role` | TEXT | `INCLUDE`, `EXCLUDE` (when paired) |
| `audit_role` | TEXT | `PRESERVE` (always in ledger) |
| `model_version` | INTEGER | Event model schema version |
| `certification_ref` | TEXT | Certification that validated this |

### Entity: `event_rule_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `rule_id` | UUID | PK |
| `rule_name` | TEXT | `ROOT_EVENT_PARTICIPATES`, `MECHANISM_EXCLUDED_WHEN_PAIRED` |
| `condition` | TEXT | When rule applies |
| `action` | TEXT | What happens to P&L |
| `exception` | TEXT | Standalone mechanism preserved |
| `certification_ref` | TEXT | RFC_EVENT_MODEL_CERTIFICATION |
| `marketplace` | TEXT | Which MPs this applies to |

### Entity: `concept_typology_v1`

| Campo | Tipo | Propósito | Ejemplo |
|-------|------|-----------|---------|
| `typology_id` | UUID | PK | |
| `marketplace` | TEXT | MP | `ML`, `SHOPIFY` |
| `concept` | TEXT | Concept name | `Ajuste por Talla/Garantía` |
| `event_role` | TEXT | ROOT_EVENT / MECHANISM | `ROOT_EVENT` |
| `standalone_pct` | FLOAT | Certified standalone ratio | `15.2%` |
| `pair_partners` | TEXT | Known causal pairs | `Ajuste por Compra Protegida (BPP)` |
| `cash_proxy` | TEXT | Cash evidence source | `Mediación` |
| `certification_ref` | TEXT | Certification | |

### Relaciones

```
event_model_v1 → event_rule_v1 (by rule_id)
event_model_v1 → concept_typology_v1 (by marketplace + concept)
event_model_v1 → marketplace_kb → marketplace_concept_v1 (by concept)
concept_typology_v1 → marketplace_kb → marketplace_concept_v1
```

### Versionado

- Event model versioned per certification cycle
- Typology may expand as new concepts discovered
- Rules frozen until recertification

### Gobernanza

- Event roles assigned per concept based on forensic evidence
- Changes require RFC + cash cross-check
- Standalone exception is non-negotiable (must preserve real cash)
- New marketplace onboarding requires typology assignment for ALL its concepts

---

## 4. Governance Knowledge Base

The **registry of authority** — what is certified, by whom, and what it means.

### Entity: `certification_v1`

| Campo | Tipo | Propósito | Ejemplo |
|-------|------|-----------|---------|
| `cert_id` | UUID | PK | |
| `document` | TEXT | File path | `governance/RFC_EVENT_MODEL_CERTIFICATION.md` |
| `title` | TEXT | Full title | RFC Event Model Certification |
| `status` | TEXT | CERTIFICADO / RECHAZADO / OBSOLETO / PENDIENTE | `CERTIFICADO` |
| `category` | TEXT | Certification type | `EVENT_MODEL`, `CASH`, `TAXONOMY` |
| `marketplace_scope` | TEXT | Which MPs | `ML` |
| `verdict` | TEXT | PASS / FAIL / PASS CONDITIONAL | `PASS` |
| `financial_impact` | FLOAT | $ impact if applied | `-5,313,560.93` |
| `cash_impact` | FLOAT | $ cash impact | `0` |
| `date_certified` | DATE | When certified | `2026-06-05` |
| `supersedes` | TEXT | Previous cert replaced | |
| `superseded_by` | TEXT | Newer cert that replaces this | |
| `depends_on` | TEXT | Prerequisite certifications | `RFC_CASH_CERTIFICATION_BPP_POSCOBRO` |

### Entity: `decision_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `decision_id` | TEXT | PK: DEC-XXX |
| `title` | TEXT | Decision title |
| `date` | DATE | When decided |
| `status` | TEXT | `APPROVED`, `REJECTED`, `PENDING` |
| `context` | TEXT | What problem it solves |
| `decision` | TEXT | What was decided |
| `consequences` | TEXT | Impacts of this decision |

### Entity: `change_register_v1`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `change_id` | UUID | PK |
| `date` | DATE | When change occurred |
| `description` | TEXT | What changed |
| `reason` | TEXT | Why it changed |
| `authorization` | TEXT | Who authorized |
| `certification_ref` | TEXT | Certification validating the change |
| `rollback_plan` | TEXT | How to undo |
| `impact` | TEXT | Financial/system impact |

### Relaciones

```
certification_v1 → certification_v1 (supersedes/superseded_by self-ref)
certification_v1 → decision_v1 (by decision that enabled it)
change_register_v1 → certification_v1 (by cert that validated it)
```

### Versionado

- Immutable append-only log
- Certifications superseded, never deleted
- Decisions archived when superseded

### Gobernanza

- Certifications require forensic evidence
- Decisions require CEO or authorized approver
- Changes require certification before execution
- Governance KB is the single source of truth for "what is certified"

---

## Cross-KB Relationships

```
Financial KB                    Marketplace KB                Ecommerce KB
─────────────                   ──────────────                ────────────
financial_metric_v1             marketplace_concept_v1        event_model_v1
  │                                  │                          │
  │  canonical_name ──────────►  canonical_name                │
  │  (concept joined)              │  event_role ──────────►  event_role
  │                                │  financial_group ────►  (derived)
  │                                │                          │
  ▼                                ▼                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      GOVERNANCE KNOWLEDGE BASE                       │
│                                                                      │
│  certification_v1 certifies entities in all 3 KBs                    │
│  decision_v1 records the decisions that created/approved them        │
│  change_register_v1 tracks all modifications                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Shopify Onboarding Path

| KB | What Shopify needs | Status |
|----|--------------------|--------|
| Financial | KPI definitions apply universally | Ready (KPI_DEFINITIONS_V1) |
| Financial | P&L structure (ingresos → disponible) | Ready (FINANCIAL_STRUCTURE) |
| Marketplace | Concept map CSV details → canonical | PENDIENTE (need mapping) |
| Marketplace | Loader spec (format, columns, sign rules) | PENDIENTE (need Shopify file spec) |
| Marketplace | Rate tables (commissions, fees) | PENDIENTE (from XMLs) |
| Ecommerce | Event model per concept | PENDIENTE (need typology assignment) |
| Ecommerce | Cash cross-check per concept | PENDIENTE (need cash source) |
| Governance | Certification of Shopify onboarding | PENDIENTE |
