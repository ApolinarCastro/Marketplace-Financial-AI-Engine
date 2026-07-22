# P33 — SYSTEM HEALTH

## 1. Database

**Engine:** DuckDB V1.5.1  
**File:** `data/db/meli_financial_v4.db`  
**Size:** ~125 MB  
**Tables:** 35 (plus 4 views)

### Tables with data

| Table | Rows | Purpose |
|-------|------|---------|
| `marketplace_ledger_v1` | 402,105 | **Primary ledger** — all 4 MPs |
| `marketplace_ledger_clasificado_v1` | 402,089 | Classified ledger (16 orphan rows excluded) |
| `marketplace_cierre_financiero_v1` | 246 | Official financial closing (50 periods, 2023–2026) |
| `ripley_settlement_chain` | 219,901 | RIPLEY settlement traceability |
| `ripley_traceability_graph` | 219,901 | RIPLEY traceability graph |
| `financial_operational_view_v1` | 228,163 | Materialized view (op_pnl=True rows) |
| `risk_postsale_view_v1` | 173,926 | View (op_pnl=False rows) |
| `v_ledger_certified` | 402,105 | Certified ledger view with DTE links |
| `dte_ledger_link` | 370,171 | DTE-to-Ledger link table |
| `dte_link_v1` | 339,112 | DTE link registry |
| `dte_truth_v1` | 667 | Indexed DTE XMLs |
| `ventas_marketplace` | 57,109 | Sales detail |
| `cierre_financiero_v2` | 96 | Duplicate closing table (24 periods, signal_mode) |
| `document_match_v1` | 9,431 | Document matching |
| `marketplace_auditoria_v1` | 8,362 | Audit alerts |
| `vw_ml_misclassifications` | 3,113 | View: ML misclassifications |
| `pipeline_log` | 1,493 | ETL pipeline events |
| `file_registry` | 216 | File tracking |
| `ripley_financial_mapping` | 34 | RIPLEY mapping rules |
| `marketplace_correcciones_v1` | 20 | Manual corrections |
| `vw_dashboard_kpis` | 1 | Dashboard KPI cache |
| `ripley_corrected_certification` | 1 | RIPLEY certification record |
| `dte_ripley_traceability` | 1 | RIPLEY DTE traceability record |

### Tables with zero rows (21)

`TABLA_MAPEO`, `ai_suggestions_log`, `bank_statement`, `cargos_no_clasificados`, `exceptions`, `financial_reconciliation`, `inconsistencias_financieras`, `liberaciones`, `order_reconciliation`, `retiros`, `test_x`, `transaction_ledger`

### Ledger distribution

| Marketplace | Rows | Total $ |
|------------|------|---------|
| RIPLEY | 219,901 | $2,139,918,844 |
| ML | 107,490 | $901,722,441 |
| PARIS | 74,036 | $337,734,474 |
| FALABELLA | 678 | $2,568,906 |

### Financial groups

| Group | Rows | Total $ |
|-------|------|---------|
| ingresos | 132,061 | $3,505,943,335 |
| costos_comerciales | 97,153 | -$382,908,140 |
| costos_operacionales | 79,533 | -$129,163,692 |
| tesoreria | 32,402 | $674,761,315 |
| ajustes | 28,958 | -$203,249,547 |
| devoluciones | 16,119 | -$430,787,414 |
| recuperaciones_y_bonificaciones | 1,303 | $42,903,836 |
| NULL (unclassified) | 14,606 | $0+ |

### Status

**VERDE.** Core financial data is intact, consistent, and certified across 50 periods (2023–2026).

---

## 2. ETL Pipeline

### Active pipeline

`SurgicalLoader` (`engine/v4/surgical_loader.py`, 845 lines) — the only active loader. Handles all 4 MPs:

- **ML**: Facturacion (18 XLSX), Poscobro (3 XLSX), Liberaciones (18 monthly dirs)
- **PARIS**: Transacciones (Dropshipping + Fulfillment XLSX)
- **RIPLEY**: XLSX files (46 files: abonos_descuentos, ciclos)
- **FALABELLA**: Facturacion + Ordenes (4+4 XLSX)

### Dead/inactive loaders

| File | Purpose | Status |
|------|---------|--------|
| `engine/data_loader_v3.py` | Legacy V3 SQLite loader | Dead — references `Marketplace_Conciliacion/conciliador.db` |
| `engine/data_loader_v4.py` | Legacy V4 SQLite loader | Dead — same old project path |
| `engine/data_loader_enhanced.py` | Legacy Enhanced loader | Dead — same old project path |
| `engine/v4/etl/ripley_loader.py` | RipleyETL class (106 lines) | Dead — **never called** from SurgicalLoader |
| `Scripts/pipeline_cli.py` | CLI orchestrator | **Broken** — imports `AntigravityEngineV4` that doesn't exist |

### Raw data coverage

```
01_Raw/ML/      → Facturacion (18), Poscobro (3), Liberaciones (18 dirs)
01_Raw/PARIS/   → XMLs (62), Transacciones (Dropshipping + Fulfillment)
01_Raw/RIPLEY/  → Ciclos (CSV), Cumplimiento (36+ XLSX), Facturacion (350+ XML), Historial (CSV), Realización (36+ CSV)
01_Raw/FALABELLA/ → XMLs (8), Facturación (4 XLSX), Órdenes (4 XLSX)
01_Raw/SHOPIFY/ → Facturacion (90+ XML), Mercado Pago (18 XLSX), Pedidos, Transbank, Ventas
```

SHOPIFY data exists but has **no loader** — no ETL ingests it.

### Status

**AMARILLO.** SurgicalLoader works for 4/5 MPs. No pipeline exists for SHOPIFY. RipleyETL class is dead code. Pipeline CLI is broken. Legacy loaders (3 files) are clutter.

---

## 3. API

### Endpoints: 33 (28 GET, 5 POST)

### Working endpoints

Most endpoints are functional. Core financial routes (`/api/v4/ledger`, `/exec/summary`, `/financial-structure`, `/periodos`, `/exec/waterfall-v3`) return correct data with ~24ms response time.

### Broken endpoint

| Endpoint | Error | Cause |
|----------|-------|-------|
| `POST /api/v4/dte/certify` | **Both code paths broken** | ALL path: missing required `periodo` param. Per-MP path: calls non-existent method `get_certification()` |

### Dead imports

In `run_full_audit()` (api.py lines 661–663):
- `load_marketplace_ledger_standalone` — imported but never called
- `SurgicalLoader` — imported but never called
- `XMLJustifier` — imported but never called

### Parameter ignored

`GET /api/v4/executive/insights` — accepts `marketplace` param but **never uses it** in the SQL query (always queries all data).

### Wasted call

`GET /api/v4/documentary/coverage` — calls `get_all_certifications()` then immediately discards the result.

### Dead code

`_DTE_LIMITATIONS` dict (lines 349–354) — defined but never referenced by any endpoint.

### V3 artifact

Waterfall endpoint is named `/api/v4/exec/waterfall-v3` — carries a version suffix that has no meaning.

### Status

**AMARILLO.** Core financial API is healthy and fast. One completely broken endpoint. Minor dead code and unused parameters.

---

## 4. Frontend

### Templates served: 3 (across 5 routes)

| Route | Template | Lines |
|-------|----------|-------|
| `/`, `/app` | `templates/dashboard.html` | 1,397 |
| `/exec`, `/executive-dashboard` | `templates/executive_dashboard.html` | 882 |
| `/documentary-dashboard` | `templates/documentary_dashboard.html` | 1,484 |

### Technology

- Vanilla JavaScript (no framework, no SPA)
- Tailwind CSS via CDN
- Font Awesome via CDN
- Google Fonts via CDN
- No static directory, no build step
- No Jinja2 server-side rendering

### Duplication

`window.ApiClient` code is copy-pasted identically into **4 locations**:
1. dashboard.html (lines 16–119)
2. executive_dashboard.html (lines 40–148)
3. documentary_dashboard.html (lines 40–148)
4. `frontend/shared/api_client.js` (standalone, **never loaded**)

### Dead template files

| File | Lines | Status |
|------|-------|--------|
| `templates/dashboard.html.bak` | 1,408 | Backup only, never served |
| `templates/dashboard_utf8.html` | 1 line (93KB) | **Binary-corrupted** (mojibake), never served |
| `templates/executive_dashboard.html.p16g_04e_backup_*.html` | 804 | Backup only, never served |

### Status

**AMARILLO.** All 3 dashboards render correctly. No JS framework bloat. However, no build system, CDN-reliant for all assets, code duplication across templates (ApiClient x4), and 3 dead template files.

---

## 5. Engines

### Active engines (12 directories)

| Engine | Files | Status |
|--------|-------|--------|
| `domain/financial_engine.py` | 1 (1028 lines) | **Healthy.** Core financial logic. |
| `domain/ledger_engine.py` | 1 | Healthy |
| `reconciliation/reconciliation_engine.py` | 3 | Healthy (64 tests) |
| `certification/certification_engine.py` | 5 | Healthy |
| `certification/document_gap_engine.py` | 1 | Healthy (post-P32R10 fix) |
| `data_quality/quality_engine.py` | 2 | Healthy |
| `scorecard/scorecard_engine.py` | 2 | Healthy |
| `closing/closing_engine.py` | 2 | Healthy (dry-run mode) |
| `explainability/explainability_engine.py` | 2 | Healthy |
| `lineage/lineage_engine.py` | 2 | Healthy |
| `intelligence/` | 5 | Healthy |
| `observability/` | 4 | Healthy |
| `production/production_checklist.py` | 2 | Structural only |

### Large unused subsystems

| Subsystem | Files | Status |
|-----------|-------|--------|
| `certification/ecc/` | 23 files | **ECC certification system** — exists but is it consumed? Evidence unclear. |
| `certification/electronic_certification/` | 9 files | Electronic certification (CAF, SII, XSD validators) |
| `certification/knowledge/` | 7 files | Obsidian vault exporter, markdown builder, graph builder |
| `engine/v4/contracts/` | 7 files | Contract definitions for 5 layers + audit + exec |

### Status

**VERDE.** Core financial engines are healthy with comprehensive test coverage. Large peripheral subsystems exist but don't affect core functionality.

---

## 6. Tests

### Total tests: ~246 functions across 28 files

| Quality | Count | Files |
|---------|-------|-------|
| **Very High** | ~125 | reconciliation, taxonomy, operational_pnl, financial_engine, regression_contracts, v4_pipeline, ripley_loader, phase_16_mandatory |
| **High** | ~100 | certification, intelligence, data_quality, explainability, executive_intelligence, lineage, observability, closing, scorecard, knowledge, falabella_promos, ml_audit, new_mappings |
| **Moderate** | ~20 | api_smoke, production |

### Broken tests

| Test | File | Problem |
|------|------|---------|
| `test_recursive_glob_ingests_from_subdirectories` | `test_paris_classification.py` | Comment says "should load 0 rows" but asserts **2 rows** — will fail |
| `test_api_file_no_contains_startswith` | `test_regression_contracts.py` | Loop body is `continue` — **never asserts** forbidden patterns. Always passes silently. |

### Test dependency

~200+ tests connect to live `data/db/meli_financial_v4.db`. If DB is unavailable or schema changes, the majority of tests will fail.

### Status

**AMARILLO.** 246 tests, comprehensive coverage, 2 broken tests that disguise real issues. Live DB dependency is a risk.

---

## 7. Architecture Summary

### Overall structure

```
113 engine/ Python files     (~20 active, ~93 support/peripheral)
  2 api/ files
  3 template files served    (+3 dead)
  1 frontend/ file           (never loaded)
 28 test files
 35 DB tables                (21 empty)
357 governance/ files        (historical documentation)
129 KnowledgeBase/ files     (historical documentation)
```

### What the system actually does

```
Raw XLSX/CSV/XML → SurgicalLoader → marketplace_ledger_v1 → 
  MarketplaceAuditorEngine (classify + close + audit) → 
  API (33 endpoints) → Dashboard (3 templates)
```

### Status

**VERDE.** Architecture is clear: ETL → Ledger → Close → API → Dashboard. Core path is well-defined and working. However, the system has accumulated significant dead weight: 21 empty tables, 3 legacy loaders, 357 governance files, 129 knowledge files, 2 large unused engine subsystems, 3 dead template files.
