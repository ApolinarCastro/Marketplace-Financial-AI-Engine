# P27 Technical Debt Matrix — Marketplace Financial AI Engine

## Methodology

Each debt item is scored:
- **Severity**: P0 (critical) to P4 (cosmetic)
- **Effort**: S (hours), M (days), L (weeks), XL (months)
- **Impact**: Financial correctness, Security, Maintainability, Performance, Portability

---

## CRITICAL (P0) — Must Fix Before Any Production Deployment

| # | Debt Item | Location | Effort | Impact | Description |
|---|-----------|----------|--------|--------|-------------|
| 1 | Hardcoded absolute paths | ALL engine files | M | Portability, Security | `C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\` appears in every file. Cannot deploy to any other machine. |
| 2 | SQL injection vulnerability | `explainability_engine.py:209` | S | Security, Financial | `f"...'{g}'..."` interpolates user string directly into SQL. Single example found; pattern may exist elsewhere. |
| 3 | Knowledge directory empty | `knowledge/` directory | M | Maintainability, Trust | CLAUDE.md references 4 core knowledge files that don't exist. Taxonomies in `KnowledgeBase/` instead. |
| 4 | CI/CD pipeline missing | `.github/workflows/` | S | Maintainability | No automated testing, linting, or deployment. |
| 5 | No dependency management | Project root | S | Portability | No `pyproject.toml`, `requirements.txt`, or `Pipfile`. |
| 6 | Wide-open CORS | `api/api.py` | S | Security | `allow_origins=["*"]` exposes API to any website. |
| 7 | Dual database files | `database/marketplace.db` (0 bytes) | S | Maintainability | Orphan SQLite file alongside DuckDB. Confusion risk. |
| 8 | No authentication middleware | `api/api.py` | M | Security | API key check is per-endpoint, not middleware. Missing on most routes. |
| 9 | Zero database indices | DuckDB schema | M | Performance | No indices on `marketplace`, `fecha`, `financial_group` — full table scans on every query. |
| 10 | No database migrations | All schemas | M | Maintainability | Schema changes require manual DuckDB operations. No version tracking. |

---

## HIGH (P1) — Must Fix Within 90 Days

| # | Debt Item | Location | Effort | Impact | Description |
|---|-----------|----------|--------|--------|-------------|
| 11 | God object FinancialEngine | `financial_engine.py` | L | Maintainability | 10+ responsibilities in one class. Imported by 7 engines. |
| 12 | Singleton DatabaseV4 | `database.py` | M | Reliability | Single connection reset errors cascade across all requests. |
| 13 | Dual taxonomy system overlap | `taxonomy/` + `KnowledgeBase/` + `marketplace_auditor.py` | L | Maintainability | 4 overlapping classification systems. Desynchronized. |
| 14 | JSON export files at root | 10+ `.json` files | S | Security, Cleanliness | Financial data, evidence JSON, and results files committed to repo root. |
| 15 | `__pycache__` committed | `taxonomy/__pycache__/` | S | Cleanliness | `.pyc` files in version control. |
| 16 | DTE coverage gap RIPLEY | `01_Raw/RIPLEY/XML/` (407 files) | L | Financial | 407 XMLs discovered but not processed or certified. |
| 17 | DTE coverage gap PARIS | `engine/v4/dte_indexer.py` | M | Financial | 68 XMLs indexed, 0 linked to ledger. |
| 18 | DTE coverage gap FALABELLA | `engine/v4/dte_indexer.py` | M | Financial | 0% DTE coverage. No XML linking. |
| 19 | No backup automation | Entire project | M | Reliability | Manual snapshot-based backups. No automated schedule. |
| 20 | Silent try/except patterns | Multiple engine files | M | Reliability | `except: continue`, `except Exception: pass` hide errors. |
| 21 | Data freshness gap | ETL pipeline | L | Financial | Junio 2026: 0 rows for all MPs. PARIS/FALABELLA 2 months behind. |
| 22 | ML audit trail = 0 rows | `marketplace_auditoria_v1` | L | Governance | Largest MP ($842M) has zero audit coverage. |
| 23 | No monitoring/observability | Entire project | L | Reliability | No metrics, no health checks, no structured logging. |
| 24 | Period calculation logic duplication | 6+ files | M | Maintainability | Same YYYY-MM → range logic copy-pasted across files. |
| 25 | Chart.js CDN dependency | `executive_dashboard.html` | S | Performance | Heavy library loaded from CDN for single chart. |
| 26 | No request validation models | `api/api.py` | M | Security | All params passed as raw strings. No Pydantic models. |
| 27 | `COALESCE` pattern duplication | 11+ SQL queries | M | Maintainability | `COALESCE(include_in_operational_pnl,1)=1` repeated across engines. |
| 28 | DuckDB as transactional database | Entire project | L | Architecture | DuckDB is analytical (columnar). Used for OLTP patterns. |
| 29 | No `conftest.py` | `tests/` | S | Testing | Test fixtures duplicated across test files. |
| 30 | No edge case tests | Given tests | M | Testing | No property-based tests, no negative tests, no boundary tests. |

---

## MEDIUM (P2) — Fix Within 6 Months

| # | Debt Item | Location | Effort | Impact | Description |
|---|-----------|----------|--------|--------|-------------|
| 31 | `ALLOWED_CLOSE_PHASES` excludes classification | `closing_engine.py` | S | Functionality | Closing engine cannot run full close. Classification would undo DEC-019. |
| 32 | Template duplication | 2 HTML templates | M | Maintainability | `dashboard.html` and `executive_dashboard.html` share significant code. |
| 33 | No loading states | Both templates | S | UX | API calls made without user feedback. |
| 34 | No error boundaries | Both templates | S | UX | Silent JS failures. |
| 35 | Tailwind CDN (no purge) | Both templates | S | Performance | Full Tailwind CSS loaded. No unused style removal. |
| 36 | No mobile breakpoints | Both templates | M | UX | Not tested on mobile. |
| 37 | Hardcoded MP list | Frontend + backend | M | Maintainability | MPs hardcoded in JS arrays and Python lists. |
| 38 | FastAPI `TestClient` in tests | `test_regression_contracts.py` | S | Testing | Hitting live DB, not a test fixture. |
| 39 | `DatabaseV4.reset()` called in tests | `test_regression_contracts.py:53` | S | Reliability | Recovery strategy is "destroy and recreate." |
| 40 | No API version sunset | `api/api.py` | S | Maintainability | v3 routes should be removed if v4 is current. |
| 41 | ExecutiveIntelligence not consumed | Frontend | M | Functionality | 0/4 intelligence endpoints used. Feature documented but not implemented. |
| 42 | `MAP_STRING` encoding errors | `taxonomy_mappings.yaml` | S | Data quality | Unicode normalization entries for encoding variants. |
| 43 | No `isort`/`autoflake` config | Project root | S | Code quality | Import ordering and unused imports not managed. |
| 44 | `_archive/` directory committed | `_archive/` | S | Cleanliness | Temp scripts committed to repository. |

---

## LOW (P3) — Nice to Have

| # | Debt Item | Location | Effort | Impact | Description |
|---|-----------|----------|--------|--------|-------------|
| 45 | `.mcp.json` committed | Project root | S | Configuration | MCP configuration in repo. Should be in `.gitignore`. |
| 46 | `mypy` — missing import ignores | `package.json` | S | Code quality | `--ignore-missing-imports` masks type issues. |
| 47 | No OpenAPI/Swagger docs | `api/api.py` | S | Documentation | FastAPI auto-generates OpenAPI; not configured. |
| 48 | Console log statements in JS | Templates | S | Cleanliness | `console.log` debugging statements. |
| 49 | `backup_20260608_120239/` in repo | Project root | S | Cleanliness | Full backup directory committed. |
| 50 | `.gitignore` completeness | `.gitignore` | S | Security | Missing patterns for JSON exports, pycache, backups. |

---

## Debt By Category

```
Category          Count   Total Effort
──────────────────────────────────────
Security          5       P0-P1     ~2 weeks
Portability       3       P0-P1     ~1 week
Maintainability   18      P0-P2     ~3 months
Financial         5       P0-P1     ~2 weeks
Performance       3       P0-P2     ~1 week
Reliability       4       P1-P2     ~2 weeks
UX                3       P2        ~1 week
Testing           2       P2        ~1 week
Cleanliness       5       P1-P3     ~2 days
Documentation     2       P2        ~1 week
──────────────────────────────────────
Total:            50      P0-P3     ~5 months
```

## Remediation Priority

### Sprint 1 (Week 1-2) — Security & Portability
Fix items #1-10 (P0) + #14-15 (cleanliness)

### Sprint 2 (Week 3-4) — Reliability
Fix items #11-13, #20, #23, #39

### Sprint 3 (Week 5-6) — Financial Completeness
Fix items #16-18, #21-22

### Sprint 4 (Week 7-8) — Architecture
Fix items #19, #24-30

### Sprint 5 (Week 9-10) — UX & Testing
Fix items #31-38

### Sprint 6 (Week 11-12) — Polish
Fix remaining items #39-50
