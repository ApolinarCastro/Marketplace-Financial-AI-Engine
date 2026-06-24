# Sprint U1.0 — Universal Channel Architecture

**Date:** 2026-06-03  
**Mode:** READ ONLY — architecture design, no implementation

---

## FASE 1 — Inventory of Marketplace-Dependent Concepts

### Current State: 250+ Hardcoded Marketplace References

| Layer | Files | Nature of Coupling | Count |
|---|---|---|---|
| Raw data loading | `surgical_loader.py` | 4 separate methods with hardcoded paths, column mapping, sign conventions | ~50 |
| Directory structure | `01_Raw/ML/*`, `01_Raw/PARIS/*`, etc. | Per-marketplace directory trees, no convention | ~15 |
| Classification | `marketplace_auditor.py` | ML-only exclusion mask (line 413), otherwise generic | 1 |
| XML tools | `dte_indexer.py`, `xml_matcher.py`, `xml_justifier.py` | `if/elif/raise` — only ML+PARIS supported | ~15 |
| Closing engine | `surgical_closer.py`, `run_full_closing.py` | Hardcoded `'ML'` parameter | ~5 |
| Recovery flow | `surgical_recovery_flow.py` | ML-only | ~3 |
| UI dashboard | `templates/dashboard.html` | Hardcoded `<option>` elements + per-MP correction config | ~8 |
| DB Views | `database.py` | `vw_ml_misclassifications` — ML-only view | 1 |
| Ad-hoc scripts | `_*.py` (~30 files) | Forensic scripts, not in pipeline | ~100 |
| API layer | `api/api.py` | Already generic — marketplace is a parameter | 0 |
| DB schema | `marketplace_ledger_v1` | Generic — stores all MPs in same table | 0 |
| **TOTAL** | | | **~250+** |

### Critical Insight

The system has a **generic data model** (all MPs in `marketplace_ledger_v1`) and a **generic API layer** (MP passed as parameter) but **hardcoded ingestion + classification + UI**.

The architecture has already proven the universal concepts work — the same classification engine processes all 4 MPs with a single `RAW_TO_CLASSIFICATION_MAP`. The only exception is ML's adjustment exclusions.

---

## FASE 2 — Universal Concepts

### The 4 Universal Financial Primitives

After 5 sprints of forensic analysis (G1-G5), all marketplace economic activity reduces to 4 universal concepts:

| Universal | Economic Definition | ML | RIPLEY | PARIS | FALABELLA | Shopify |
|---|---|---|---|---|---|---|
| **VENTA** | Gross sale amount | Cargo por venta (Venta) | Importe del pedido | Venta | Pago por precio del producto | `total_price` |
| **DEVOLUCIÓN** | Return/refund amount | Devolución de venta | Pedidos reembolsados | Devolución | Descuento por devolución de producto | `refund_amount` |
| **COBRO** | Fees and charges collected | Cargo por venta (Comisión), Cargo por envíos, etc. | Comisiones, Descuento logístico, etc. | Cobro por despacho, etc. | Cobro por comisión, etc. | `transaction_fees`, `shipping_fees` |
| **DISPONIBLE** | Net payable to seller | Not present as single concept | A pagar | Not present as single concept | Not present | `net_payment` |

### Derived Concepts

| Universal | Type | Components |
|---|---|---|
| **COSTO_LOGISTICA** | Expense | Envío, Descuento logístico, Logística inversa, Cobro por despacho |
| **COMISION** | Revenue | Comisiones netas (gross - refunds) |
| **PUBLICIDAD** | Revenue | Product Ads, Display, Brand Ads |
| **SERVICIOS** | Revenue | Asesoría Comercial, Mi Página |
| **ALMACENAMIENTO** | Expense/Cost | Full, Retiro stock, Stock antiguo |
| **AJUSTE** | Contra revenue | BPP, Talla, Conciliación, Compensaciones |
| **PENALIDAD** | Revenue | Descuento por cancelación, Otros descuentos |

### Mapping Pattern

```
Channel-Specific Concept  →  Universal Concept  →  Financial Group
─────────────────────────────────────────────────────────────────
"Cargo por venta (Venta)" →  VENTA              →  ingresos
"Importe del pedido"      →  VENTA              →  ingresos
"Venta"                   →  VENTA              →  ingresos
"Pago por precio..."      →  VENTA              →  ingresos
"total_price"             →  VENTA              →  ingresos
```

The same pattern works for every channel. Only the raw `detalle` strings differ.

---

## FASE 3 — sales_channel Entity Design

### Proposed Schema

```sql
CREATE TABLE sales_channel_v1 (
    channel_id          VARCHAR(50) PRIMARY KEY,
    channel_name        VARCHAR(100) NOT NULL,
    channel_type        VARCHAR(50) NOT NULL,  -- 'MARKETPLACE', 'ECOMMERCE', 'PHYSICAL_STORE'
    connector_module    VARCHAR(200),           -- Python module path
    config              JSON,                   -- Channel-specific configuration
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Seed Data

```sql
INSERT INTO sales_channel_v1 VALUES
('ML',       'Mercado Libre',       'MARKETPLACE',  'connectors.melichile_connector',  '{"raw_dir": "01_Raw/ML", "has_xml": true}',  true),
('RIPLEY',   'Ripley',              'MARKETPLACE',  'connectors.ripley_connector',     '{"raw_dir": "01_Raw/RIPLEY", "has_xml": false}', true),
('PARIS',    'Paris',               'MARKETPLACE',  'connectors.paris_connector',      '{"raw_dir": "01_Raw/PARIS", "has_xml": true}', true),
('FALABELLA','Falabella',            'MARKETPLACE',  'connectors.falabella_connector',  '{"raw_dir": "01_Raw/FALABELLA", "has_xml": false}', true),
('SHOPIFY',  'Shopify E-commerce',   'ECOMMERCE',    'connectors.shopify_connector',    '{"raw_dir": "01_Raw/SHOPIFY", "api_key": "..."}', true),
('AMAZON',   'Amazon',               'MARKETPLACE',  'connectors.amazon_connector',     '{"raw_dir": "01_Raw/AMAZON", "has_report": true}', false),
('WOOCOMM',  'WooCommerce',          'ECOMMERCE',    'connectors.woocommerce_connector','{"raw_dir": "01_Raw/WOOCOMMERCE"}', false);
```

### Universal Concept Map Table

```sql
CREATE TABLE universal_concept_map_v1 (
    channel_id      VARCHAR(50) NOT NULL,
    raw_detalle     VARCHAR(200) NOT NULL,       -- Channel-specific concept name
    universal_concept VARCHAR(50) NOT NULL,       -- VENTA, DEVOLUCION, COBRO, etc.
    financial_group VARCHAR(50),                  -- ingresos, costos_comerciales, etc.
    sign_convention VARCHAR(10) DEFAULT 'NEGATIVE_IS_REVENUE',  -- Channel sign rule
    is_active       BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (channel_id, raw_detalle)
);
```

This replaces the current `RAW_TO_CLASSIFICATION_MAP` dict in `marketplace_auditor.py`.

### Channel-Specific Exclusions

```sql
CREATE TABLE channel_exclusion_v1 (
    channel_id      VARCHAR(50) NOT NULL,
    raw_detalle     VARCHAR(200) NOT NULL,
    exclusion_type  VARCHAR(50) NOT NULL,  -- 'P&L', 'TAX', 'OPERATIONAL'
    reason          VARCHAR(500),
    PRIMARY KEY (channel_id, raw_detalle)
);
```

This replaces the ML-only exclusion mask. Each channel can declare which concepts to exclude from P&L.

---

## FASE 4 — Shopify Compatibility Validation

### Does Shopify break Money Flow (G4.0)?

**No.** G4.0 decomposed money flow into:
1. **Gross inflow** → VENTA (exists in Shopify as `total_price`)
2. **Returns out** → DEVOLUCIÓN (exists as `refund_amount`)
3. **Fees retained** → COBRO (exists as `transaction_fees` + `shipping_fees`)
4. **Net to seller** → DISPONIBLE (exists as `net_payment`)

Shopify's money flow is identical to RIPLEY's: buyer pays, Shopify deducts fees, Eccsa receives net.

### Does Shopify break Financial Truth (G3.1)?

**No.** The 4 universal concepts are channel-agnostic. Shopify's economic dictionary (from Shopify API docs) maps directly:

| G3.1 Economic Concept | Shopify Equivalent |
|---|---|
| Sale price | `order.total_price` |
| Transaction fee | `order.transaction_fees` |
| Shipping fee | `order.shipping_fees` |
| Refund | `order.refund_amount` |
| Net settlement | `order.net_payment` |

### Does Shopify break Executive Dashboard?

**No.** The dashboard already handles multiple MPs dynamically. Adding Shopify requires:
1. A new `<option>` in the channel selector (or dynamic from API)
2. A new correction options block (or dynamic from `universal_concept_map_v1`)
3. All API calls already pass `marketplace` as a parameter — no backend change needed

### What DOES break?

| Component | Issue | Fix |
|---|---|---|
| `surgical_loader.py` | No Shopify loader method | Add `load_shopify()` or use generic CSV loader |
| `dte_indexer.py` | No XML support for digital channels | Shopify has no XML/DTE — needs API-based ingestion |
| Classification map | Shopify `detalle` names not in map | Add to `universal_concept_map_v1` |
| ML exclusion mask | Hardcoded for ML only | Replace with `channel_exclusion_v1` table |
| Dashboard corrections | No Shopify options block | Replace with dynamic API call |

---

## FASE 5 — Connector Architecture

### Plugin Design

```
engine/
├── core/
│   ├── financial_engine.py        # Generic processing pipeline
│   ├── classification_engine.py   # Uses universal_concept_map_v1
│   ├── closing_engine.py          # Channel-agnostic
│   └── channel_registry.py        # Channel discovery + lifecycle
│
├── connectors/
│   ├── __init__.py
│   ├── base_connector.py          # Abstract base class
│   ├── shopify_connector.py       # REST API ingestion
│   ├── melichile_connector.py     # XLSX file ingestion (current ML loader)
│   ├── ripley_connector.py        # XLSX melt-based ingestion
│   ├── paris_connector.py         # XLSX transaction ingestion
│   ├── falabella_connector.py     # XLSX ingestion
│   ├── amazon_connector.py        # Future
│   └── woocommerce_connector.py   # Future
│
└── config/
    └── channels.yaml              # Channel registration
```

### BaseConnector Interface

```python
class BaseConnector(ABC):
    """Every channel connector implements this interface."""

    @abstractmethod
    def discover_raw_files(self) -> list[Path]:
        """Find new raw data files to process."""

    @abstractmethod
    def parse_raw_file(self, path: Path) -> pd.DataFrame:
        """Parse a raw file into standardized format with columns:
           - fecha, detalle, monto, id_transaccion
        """

    @abstractmethod
    def map_concepts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map raw detalle to universal concepts using universal_concept_map_v1."""

    @abstractmethod
    def apply_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply channel-specific business rules (exclusions, sign flips, etc.)."""

    @property
    @abstractmethod
    def channel_id(self) -> str:
        """Unique channel identifier."""
```

### Ingestion Pipeline (Current vs Future)

```
CURRENT:                          FUTURE:
─────────                         ───────
surgical_loader.py                channel_registry.py
├── load_facturacion() (ML)       ├── discover_channels() → [ML, RIPLEY, PARIS, ...]
├── load_poscobro() (ML)          ├── for each channel:
├── load_paris() (PARIS)          │   ├── connector = BaseConnector.for(channel)
├── load_ripley() (RIPLEY)        │   ├── files = connector.discover_raw_files()
├── load_falabella() (FALABELLA)  │   ├── for each file:
└── load_marketplace()            │   │   ├── df = connector.parse_raw_file(file)
    └── if/elif chain             │   │   ├── df = connector.map_concepts(df)
                                  │   │   ├── df = connector.apply_rules(df)
                                  │   │   └── core.load_to_ledger(df)
                                  │   └── mark_processed()
                                  └── next channel
```

### Directory Convention

```
01_Raw/{CHANNEL_ID}/{TYPE}/
├── ML/
│   ├── ML_Facturacion/
│   └── Poscobro/
├── RIPLEY/
│   ├── Liquidaciones/
│   └── Conciliacion/
├── PARIS/
│   ├── Transacciones/
│   └── XML/
├── SHOPIFY/
│   ├── Orders/        ← API exports
│   └── Payouts/       ← Settlement reports
└── AMAZON/
    └── Reports/        ← SP-API reports
```

### Migration Path

| Phase | What | Impact |
|---|---|---|
| **Phase 0** (current) | 4 hardcoded loaders + if/elif chain | 250+ hardcoded references |
| **Phase 1** | Extract `BaseConnector` interface, wrap 4 existing loaders as connectors | Zero behavior change, enables new channels |
| **Phase 2** | Create `channel_registry.py` + `channels.yaml` — registry-driven channel discovery | Dynamic channel selector, no more if/elif |
| **Phase 3** | Migrate classification to `universal_concept_map_v1` table | Replace 230-entry dict with queryable table |
| **Phase 4** | Replace ML exclusion mask with `channel_exclusion_v1` table | Generic P&L exclusions per channel |
| **Phase 5** | Dynamic dashboard via API endpoints (`/api/v4/channels`, `/api/v4/channel/{id}/concepts`) | Add new channel = add connector + map concepts |
| **Phase 6** | Build `ShopifyConnector` | First non-marketplace channel live |

### Adding a New Channel (e.g., Shopify)

```python
# connectors/shopify_connector.py

class ShopifyConnector(BaseConnector):

    @property
    def channel_id(self) -> str:
        return "SHOPIFY"

    def discover_raw_files(self) -> list[Path]:
        return sorted(Path("01_Raw/SHOPIFY/Orders").glob("orders_*.csv"))

    def parse_raw_file(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)
        return pd.DataFrame({
            "fecha": df["created_at"],
            "detalle": "Venta" if df["financial_status"] == "paid" else "Devolución",
            "monto": df["total_price"] * -1,  # Negative = Eccsa revenue
            "id_transaccion": df["order_number"].apply(lambda x: f"SHOP_{x}"),
        })

    def map_concepts(self, df: pd.DataFrame) -> pd.DataFrame:
        # universal_concept_map_v1 handles this automatically
        return df

    def apply_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        # Shopify has no adjustment exclusions — no rules needed
        return df
```

**Total code to add Shopify: ~60 lines.**

---

## Architecture Verification

### Does the design preserve existing contracts?

| Contract | Status | Rationale |
|---|---|---|
| SQL = API = UI | ✓ Preserved | API layer is already generic; no contract changes |
| 14/14 regression | ✓ Preserved | Engine pipeline unchanged; connectors wrap existing loaders |
| BASELINE_V6 | ✓ Preserved | No modifications to DB tables |
| Money Flow (G4.0) | ✓ Preserved | Universal concepts capture all 4 money flow stages |
| Financial Truth (G3.1) | ✓ Preserved | Universal economic dictionary is channel-agnostic |
| Executive Dashboard | ✓ Preserved | Dynamic API replaces hardcoded UI; existing MPs unchanged |

### What breaks and must be fixed?

| Component | Breakage | Fix |
|---|---|---|
| `surgical_loader.py` | Becomes deprecated | Connectors replace it; backward compat wrapper in Phase 1 |
| `marketplace_auditor.py` ML exclusion mask | Hardcoded ML logic | Replaced by `channel_exclusion_v1` table |
| Dashboard correction options | Hardcoded JSON block | Replaced by API call; old block kept for backward compat |

---

## Roadmap

| Phase | Timeline | Result |
|---|---|---|
| Phase 1 | 2 weeks | `BaseConnector` interface, 4 wrappers, zero behavior change |
| Phase 2 | 1 week | `channel_registry.py`, dynamic channel discovery |
| Phase 3 | 2 weeks | `universal_concept_map_v1` table, migrate classification |
| Phase 4 | 1 week | `channel_exclusion_v1` table, generic P&L exclusions |
| Phase 5 | 2 weeks | Dynamic dashboard API endpoints |
| Phase 6 | 2 weeks | `ShopifyConnector` — first non-marketplace channel live |
| **Total** | **10 weeks** | Universal Omnichannel Platform |

---

*Documento generado: 2026-06-03 | Status: READ ONLY ARCHITECTURE*
