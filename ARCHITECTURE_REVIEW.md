# P27 Architecture Review — Marketplace Financial AI Engine

## 1. System Architecture Overview

### Current Architecture
```
┌──────────────────────────────────────────────────────────┐
│                   FastAPI (api.py)                       │
│  ~37 routes, thin orchestration, wide-open CORS          │
└──────────┬──────────────────────────────────┬────────────┘
           │                                  │
┌──────────▼──────────┐       ┌──────────────▼──────────┐
│   Templates/        │       │   Engine Layer           │
│   dashboard.html    │       │   financial_engine.py     │
│   executive_dashboard│      │   reconciliation_engine.py│
│                     │       │   certification_engine.py │
│   Vanilla JS        │       │   lineage_engine.py       │
│   Chart.js          │       │   closing_engine.py       │
│   Tailwind CDN      │       │   explainability_engine.py│
│                     │       │   marketple_auditor.py    │
└─────────────────────┘       │   surgical_loader.py      │
                              │   dte_indexer.py          │
                              │   scorecard_engine.py     │
                              │   quality_engine.py       │
                              └──────────────┬────────────┘
                                             │
                              ┌──────────────▼────────────┐
                              │   DuckDB V1.5.1           │
                              │   meli_financial_v4.db    │
                              │   3 core tables + config  │
                              └───────────────────────────┘
```

### Architecture Classification: LAYERED MONOLITH WITH ASPIRATIONAL MODULARITY

The architecture claims a "12 engine" modular design. In practice:
- Engines are **tightly coupled** — `FinancialEngine` is imported by 7 of 12 engines, creating a hub-and-spoke dependency graph
- **DuckDB** is the single point of failure — all engines share one database connection via `DatabaseV4.get()` singleton
- No **service boundaries** — engines import each other freely (circular import risk evidenced by `MarketplaceAuditorEngine` instantiation inside `ClosingEngine`)
- No **dependency injection** beyond optional `db: DatabaseV4 | None = None` — most engines create their own dependencies via `FinancialEngine()`

## 2. Layer Review

### 2.1 API Layer (api.py)

| Aspect | Assessment |
|--------|-----------|
| Route design | REST-like but inconsistent (`/api/v4/ledger` returns different shapes than `/api/v4/cierre/desglose`) |
| Input validation | Minimal — FastAPI Pydantic models not used; raw params passed to engine |
| Error handling | Inconsistent — some routes return `{"error": msg}`, others return `[]` |
| CORS | `allow_origins=["*"]` — production-critical vulnerability |
| Auth | None — `ENGINE_API_KEY` checked in one place, not enforced middleware |
| Versioning | `/api/v4/` prefix suggests versioning; no v3 routes removed |
| Rate limiting | None |

**Critical finding**: `api.py` imports `financial_engine.FinancialEngine` directly from route functions. No serialization layer, no response models, no OpenAPI schema.

### 2.2 Engine Layer

| Engine | Maturity | Issues |
|--------|----------|--------|
| FinancialEngine | HIGH (core) | Dual-mode taxonomy (YAML + legacy fallback). Complex. Used everywhere. |
| ReconciliationEngine | HIGH | 5-level validation is well-designed. Genuinely useful. |
| CertificationEngine | MEDIUM | Depends on ReconciliationEngine + FinancialEngine. Output is conceptual, not actionable. |
| LineageEngine | MEDIUM | Good concept. Returns raw DB rows. No graph traversal. |
| ExplainabilityEngine | LOW | SQL injection in drill_sql(). Hardcoded KPI_CATALOG dict. |
| ClosingEngine | LOW | Wraps other engines. dry_run only. No real closing logic. |
| ScorecardEngine | MEDIUM | Solid per-MP KPIs. Redundant with FinancialEngine. |
| QualityEngine | MEDIUM | 7 checks. Coverage score is useful. |
| MarketplaceAuditor | LEGACY | 900-line file with hardcoded mapping dict. Needs refactoring. |
| SurgicalLoader | LEGACY | 829 lines, hardcoded paths, auto-header detection is fragile. |
| DTEIndexer | MEDIUM | XML parsing is solid. 0/68 linked to ledger. |
| ExecutiveIntelligence | LOW | SQL-based. 0/4 endpoints consumed by frontend. |

**Critical finding**: The engine layer suffers from **layering violation**. `ClosingEngine` instantiates `MarketplaceAuditorEngine` inside a `try/except` block. `ExplainabilityEngine` bypasses parameterized queries. `FinancialEngine` is a god object.

### 2.3 Data Layer

**Schema**: 3 core tables + auxiliary tables
- `marketplace_ledger_v1` — Main transaction table (207K rows, $1.6B)
- `marketplace_ledger_clasificado_v1` — Classified mirror (same rows)
- `marketplace_cierre_financiero_v1` — Period closing summary (109 rows)
- `dte_truth_v1` — XML document index
- Other: `marketplace_auditoria_v1`, `marketplace_metadata_v1`, `file_registry`

**Issues**:
- No primary keys or foreign key constraints
- No indices on frequently queried columns (`marketplace`, `fecha`, `financial_group`)
- `id_transaccion` exists but no uniqueness constraint
- `folio_xml` in ledger but no FK to `dte_truth_v1`
- Schema is not versioned — `_v1` suffix suggests future versions but no migration strategy
- NULL handling is inconsistent — `COALESCE(include_in_operational_pnl,1)=1` repeated across 11 SQL queries
- DuckDB is column-oriented but queried with row-oriented patterns (SELECT *, repeated SUM aggregations)

### 2.4 Frontend Layer

Two templates:
- `dashboard.html` — Auditor dashboard (original)
- `executive_dashboard.html` — Executive/Gerencial dashboard (Phase UX1.0/1.1)

**Issues**:
- Duplicate data fetching (both call `/api/v4/financial-structure` and `/api/v4/exec/summary`)
- Vanilla JS only — no framework, no component isolation
- Chart.js in executive template — heavy dependency for a single chart
- Tailwind CDN dependency — no build step, no purge, bloated CSS
- Navigation between dashboards is client-side only
- No loading states, no error boundaries, no retry logic

## 3. Architecture Anti-Patterns

### God Object Pattern
`FinancialEngine` is imported by 7 engines. It handles period resolution, ledger queries, cierre queries, desglose, cobros breakdown, exec summary, waterfall, audit, intelligence, and financial-structure. This is 10+ responsibilities in one class.

### Singleton Pattern Abuse
`DatabaseV4.get()` is a singleton with `DatabaseV4._instance = None` reset mechanism. When one query fails, the entire database connection is reset (`DatabaseV4.reset()`). This means a single SQL error can disrupt all concurrent API requests. This is visible in `test_regression_contracts.py:53-54`:
```python
except Exception:
    DatabaseV4.reset()
    _db = DatabaseV4.get()
```

### Duplicate Classification Systems
| System | Location | Used By |
|--------|----------|---------|
| `RAW_TO_CLASSIFICATION_MAP` | `marketplace_auditor.py` | Auditor engine |
| `taxonomy_rules.yaml` | `taxonomy/` | YAML-driven (claimed) |
| `taxonomy_mappings.yaml` | `taxonomy/` | 670-line mapping (includes encoding errors) |
| `ml_v1.json` | `KnowledgeBase/Marketplace/Taxonomy/` | Per-MP taxonomy |
| Hardcoded `catMap` (removed) | Previously in frontend | Eliminated in Phase UX1.2 |
| Legacy `LEGACY_CONCEPT_MAP` | `financial_engine.py` | Fallback mode |

Four active classification systems co-exist. They overlap but are not synchronized.

### Connection Reset Cascade
When DuckDB query fails:
1. `DatabaseV4.reset()` destroys singleton
2. Next call to `DatabaseV4.get()` creates new connection
3. All in-flight queries on the old connection fail
4. No transaction rollback or error propagation

## 4. Technology Choices

| Choice | Assessment | Recommendation |
|--------|-----------|----------------|
| DuckDB V1.5.1 | Excellent for analytical workloads. Not a transactional database. | Keep as read-only analytics layer. Move ingestion to SQLite/Postgres. |
| FastAPI | Excellent framework. Not leveraging Pydantic models. | Add request/response models. |
| Tailwind CDN | OK for prototyping. No build step. | Move to PostCSS build pipeline. |
| Chart.js | Good for dashboards. Single use case. | Consider lightweight alternative or keep. |
| Vanilla JS | Zero dependencies. No framework lock-in. | Consider HTMX or Alpine.js for interactivity. |
| Ruff | Excellent linter. Under `devDependencies: {}`. | Add to CI/CD pipeline. |

## 5. Security Architecture

| Vulnerability | Severity | Location |
|--------------|----------|----------|
| SQL injection | CRITICAL | `explainability_engine.py:209` (`f"...'{g}'..."`) |
| Wide-open CORS | HIGH | `api/api.py:allow_origins=["*"]` |
| No API authentication | HIGH | No middleware enforcing API key |
| Hardcoded absolute paths | MEDIUM | Every engine file |
| `.pyc` files committed | LOW | `taxonomy/__pycache__/` in repo |
| Secrets exposure | MEDIUM | 10+ JSON export files at root with financial data |

## 6. Deployment Architecture

**Current**: None. Runs locally on developer machine.
**Required for production**: CI/CD, Docker, secrets management, database backup, monitoring.

No deployment configuration exists — no `Dockerfile`, no `docker-compose.yml`, no `nginx.conf`, no deployment scripts.

## 7. Architecture Verdict

> The architecture has good conceptual bones (Single Financial Truth, certification gate, reconciliation engine, signal/noise taxonomy) but the implementation is **2-3 layers deep** in documentation debt. What exists in code is functional but fragile. The gap between the documented Phase 12-16 architecture and the actual code is the single biggest risk.

**Score**: 3.5/10 — Aspirational modularity with monolithic reality.

**Next**: Single-developer project needs 2-3 months of infrastructure work before it can be considered production-grade, regardless of the correctness of its financial logic.
