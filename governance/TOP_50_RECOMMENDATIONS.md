# P27 Top 50 Recommendations — Marketplace Financial AI Engine

Ordered by priority (P0 → P4), then by effort (quickest first within each tier).

---

## TIER 1 — CRITICAL (P0) — Do Before Any Production Use

| # | Recommendation | Effort | Impact | File(s) Affected | Detail |
|---|---------------|--------|--------|-----------------|--------|
| 1 | Replace all hardcoded `ROOT` paths with env var | 4h | HIGH | ALL engine files | Create `MELI_ROOT` env var. Config in `database.py`. |
| 2 | Fix SQL injection in `explainability_engine.py` | 15min | CRITICAL | `explainability_engine.py:209` | Replace f-string params with `?` placeholders |
| 3 | Create `pyproject.toml` with dependency declarations | 1h | HIGH | New file | Add `duckdb>=1.5.1`, `fastapi`, `uvicorn`, `pandas`, `openpyxl`, `calamine` |
| 4 | Add GitHub Actions CI workflow | 2h | HIGH | `.github/workflows/ci.yml` | Run `pytest tests/`, `ruff check .`, `mypy api/ engine/` |
| 5 | Remove orphan `database/marketplace.db` | 5min | MEDIUM | Project root | 0-byte SQLite file. Delete it. |
| 6 | Remove wide-open CORS | 15min | HIGH | `api/api.py` | Replace `["*"]` with specific origins or env config |
| 7 | Create `knowledge/` directory with actual files | 4h | HIGH | `knowledge/` | Move taxonomies from `KnowledgeBase/`. Create concept/event/cash registries. |
| 8 | Update CLAUDE.md to match reality | 2h | HIGH | `CLAUDE.md` | Remove claims about non-existent files. Correct paths. |
| 9 | Add API key middleware | 4h | HIGH | `api/api.py` | Single middleware checking `X-API-Key` header. Configurable. |
| 10 | Add .gitignore patterns for exports and pycache | 30min | MEDIUM | `.gitignore` | Add `*.json` (root), `*__pycache__/`, `backup_*/`, `_archive/` |

## TIER 2 — HIGH (P1) — Fix Within 90 Days

| # | Recommendation | Effort | Impact | Detail |
|---|---------------|--------|--------|--------|
| 11 | Remove JSON export files from repo root | 30min | MEDIUM | Move to `data/exports/` or remove. 10+ files. |
| 12 | Remove `__pycache__` from repo | 5min | LOW | Add to `.gitignore`. Delete existing. |
| 13 | Consolidate taxonomy systems | 2w | HIGH | Unify: `taxonomy_rules.yaml` (canonical), `taxonomy_mappings.yaml` (backward compat), `KnowledgeBase/` JSON (per-MP view). Auditors dict (deprecated). |
| 14 | Implement DuckDB indices | 4h | HIGH | Add indices on `marketplace`, `fecha`, `financial_group`, `detalle` |
| 15 | Extract FinancialEngine into focused services | 2w | HIGH | Split into: `LedgerService`, `CierreService`, `WaterfallService`, `DesgloseService` |
| 16 | Break DatabaseV4 singleton with connection pool | 1w | HIGH | Create connection pool or at minimum connection-per-request pattern |
| 17 | Fix DatabaseV4.reset() cascade | 2d | HIGH | Remove auto-reset on error. Propagate errors properly. |
| 18 | Add DTE order_id matcher for PARIS/FALABELLA | 2w | HIGH | Implement matching heuristic to link 68 indexed XMLs to ledger `folio_xml` |
| 19 | Process RIPLEY 407 XMLs | 2w | HIGH | Run `DTEIndexer` on RIPLEY XML directory |
| 20 | Add automated DB backup script | 1d | HIGH | `backup.py` that snapshots `meli_financial_v4.db` with timestamp |
| 21 | Remove silent `except: continue` patterns | 2d | HIGH | Replace with proper error logging and propagation |
| 22 | Add data freshness loading (Junio 2026) | 2d | HIGH | Load/process June 2026 data for all 4 MPs |
| 23 | Fix ML audit trail (0 rows) | 3d | HIGH | Implement ML audit rules in `marketplace_auditor.py` |
| 24 | Extract period calculation to shared utility | 1d | MEDIUM | Create single `resolve_period()` function used by all engines |
| 25 | Remove Chart.js CDN or add SRI hash | 1h | MEDIUM | Security: subresource integrity for CDN link |
| 26 | Add Pydantic request/response models | 1w | MEDIUM | Create `api/schemas.py` with models for all routes |
| 27 | Extract COALESCE pattern to constant | 1h | LOW | Define `OP_PNL_CLAUSE = "AND COALESCE(include_in_operational_pnl,1)=1 "` once |
| 28 | Add `conftest.py` for shared test fixtures | 2h | MEDIUM | Move common fixtures (FinancialEngine, DB connection) to single file |
| 29 | Add property-based tests with Hypothesis | 2d | MEDIUM | Test invariants: conservation, sum=SQL, negations |
| 30 | Move DuckDB to read-replica for API queries | 1w | MEDIUM | Separate write (ETL) and read (API) connections |

## TIER 3 — MEDIUM (P2) — Fix Within 6 Months

| # | Recommendation | Effort | Impact | Detail |
|---|---------------|--------|--------|--------|
| 31 | Enable full close in ClosingEngine | 2w | MEDIUM | Rework classification to not undo DEC-019. Enable non-dry-run mode. |
| 32 | Merge duplicate template code | 1w | MEDIUM | Extract shared components into `templates/shared/` |
| 33 | Add loading states to both dashboards | 2d | MEDIUM | Spinner/skeleton during API calls |
| 34 | Add error boundaries to both dashboards | 2d | MEDIUM | Catch JS errors, show user-friendly messages |
| 35 | Add Tailwind build pipeline with purge | 2d | MEDIUM | Move from CDN to PostCSS build. Reduce CSS from 3MB to ~30KB. |
| 36 | Add mobile-responsive breakpoints | 1w | MEDIUM | Test and fix on 375px, 768px, 1024px breakpoints |
| 37 | Dynamize MP list (no hardcoding) | 2d | MEDIUM | Query DB for distinct marketplaces instead of hardcoding |
| 38 | Add FastAPI dependency injection for test DB | 2d | MEDIUM | Enable test fixtures to use separate DuckDB file |
| 39 | Wire ExecutiveIntelligence to frontend | 3d | MEDIUM | Implement `intelligence-cards` in executive dashboard |
| 40 | Fix encoding errors in YAML taxonomy | 1d | LOW | Clean Unicode normalization entries. They're band-aids. |
| 41 | Add `isort` and `autoflake` to CI | 1h | LOW | Automated import sorting and unused-import removal |
| 42 | Remove `_archive/` from repo | 30min | LOW | Move to `.gitignore`. Archive scripts are temp files. |
| 43 | Add version header to API responses | 1h | LOW | `X-API-Version: 4` in every response |
| 44 | Add request ID tracing | 2d | MEDIUM | `X-Request-ID` header for debugging |
| 45 | Add logging levels configuration | 1d | LOW | Environment-based log level (`DEBUG`, `INFO`, `WARNING`) |

## TIER 4 — LOW (P3-P4) — Future

| # | Recommendation | Effort | Impact | Detail |
|---|---------------|--------|--------|--------|
| 46 | Remove `.mcp.json` from repo | 5min | LOW | Add to `.gitignore`. MCP config is developer-specific. |
| 47 | Configure OpenAPI/Swagger UI | 2d | MEDIUM | FastAPI auto-generates. Enable `/docs` with proper metadata. |
| 48 | Remove console.log from JS | 30min | LOW | Clean up debugging statements |
| 49 | Remove `backup_20260608_120239/` from repo | 15min | LOW | Backup directory should not be in version control |
| 50 | Create CONTRIBUTING.md with setup guide | 1d | MEDIUM | Document setup steps once portability is fixed |

---

## Recommendation Distribution

```
P0 (Critical): 10 items — ~2 weeks to fix
P1 (High):     20 items — ~8 weeks to fix
P2 (Medium):   15 items — ~8 weeks to fix
P3-P4 (Low):   5 items  — ~1 week to fix
─────────────────────────────────────
Total:         50 items — ~20 weeks (5 months) to full remediation
```

## Key Dependencies

- **Items #1-10** must be completed before any production deployment
- **Items #11-17** must be completed before onboarding any other developer
- **Items #18-23** must be completed before the product can claim multi-MP financial coverage
- **Items #24-30** must be completed before external beta testing
- **Items #31-45** are quality-of-life improvements for production
- **Items #46-50** are cleanup tasks

## Quick Wins (Week 1)

Items that can be completed in one focused week:

| Day | Items | Description |
|-----|-------|-------------|
| Mon | #2, #5, #6, #8 | SQL injection fix, remove orphan DB, CORS fix, CLAUDE.md update |
| Tue | #1, #3 | Env var config, pyproject.toml |
| Wed | #4, #9 | CI workflow, API key middleware |
| Thu | #10, #11, #12 | .gitignore, remove exports, remove pycache |
| Fri | #7 | Create knowledge/ directory with taxonomy files |

After Week 1: ~60% of critical security/portability issues resolved.
