# P30 — EVIDENCE MATRIX

Toda afirmación respaldada por:
- archivo → función → endpoint → tabla → consulta → test → captura

---

## E-001: Ledger total y clasificación

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/database.py` |
| **Tabla** | `marketplace_ledger_v1` |
| **Consulta** | `SELECT COUNT(*) as cnt, COALESCE(SUM(COALESCE(monto,0)),0) as total FROM marketplace_ledger_v1` |
| **Resultado** | 402,089 rows, $3,381,794,665.45 |
| **Test** | `test_financial_engine.py::test_all_marketplaces_have_data` |

## E-002: Ledger == Clasificado (Single Financial Truth base)

| Campo | Valor |
|-------|-------|
| **Tablas** | `marketplace_ledger_v1`, `marketplace_ledger_clasificado_v1` |
| **Consulta** | `SELECT COUNT(*) as cnt, SUM(monto) as total FROM marketplace_ledger_v1` vs `marketplace_ledger_clasificado_v1` |
| **Resultado** | Delta 0 rows, $0.00 |
| **Test** | `test_taxonomy_equivalence.py::test_financial_group_monetary_equivalence` (4 MPs PASS) |

## E-003: Cierre financiero

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_cierre_financiero_v1` |
| **Consulta** | `SELECT COUNT(*) as cnt, COALESCE(SUM(COALESCE(resultado_neto,0)),0) as total FROM marketplace_cierre_financiero_v1` |
| **Resultado** | 246 rows, $1,311,453,028.12 |
| **Gap vs Ledger** | $2,070,341,637.33 |

## E-004: Conservation gap per-MP

| Campo | Valor |
|-------|-------|
| **Consulta** | `SELECT LOWER(marketplace), SUM(monto) FROM marketplace_ledger_v1 GROUP BY 1` vs `SELECT LOWER(marketplace), SUM(resultado_neto) FROM marketplace_cierre_financiero_v1 GROUP BY 1` |
| **Resultados** | ML gap $291.5M, RIPLEY gap $1.80B, PARIS gap -$18.1M, FALABELLA gap -$6.0M |

## E-005: DTE coverage

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_ledger_v1` |
| **Consulta** | `SELECT LOWER(marketplace), COUNT(*), COUNT(folio_xml) FROM marketplace_ledger_v1 GROUP BY 1` |
| **Resultados** | ML 89.4%, RIPLEY 97.3%, PARIS 81.2%, FALABELLA 0% |
| **Test** | `test_certification_gate.py::test_gate_dte_coverage` |

## E-006: DTE documents indexed

| Campo | Valor |
|-------|-------|
| **Tabla** | `dte_truth_v1` |
| **Consulta** | `SELECT COUNT(*) FROM dte_truth_v1` |
| **Resultado** | 667 documentos XML |
| **Endpoint** | `GET /api/v4/dte/count` → `{"count": 667}` |

## E-007: DTE certification

| Campo | Valor |
|-------|-------|
| **Endpoint** | `GET /api/v4/dte/certify` |
| **Resultado ML** | Cobertura 97.7%, $301.6M certificado |

## E-008: Auditoria alerts

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_auditoria_v1` |
| **Consulta** | `SELECT LOWER(marketplace), COUNT(*) FROM marketplace_auditoria_v1 GROUP BY 1` |
| **Resultados** | RIPLEY 4,619, ML 3,743, PARIS 0, FALABELLA 0 |

## E-009: Tests suite

| Campo | Valor |
|-------|-------|
| **Comando** | `python -m pytest tests/ -v --tb=short` |
| **Resultado** | 268 PASS, 2 FAIL, 8 SKIP, 278 total |
| **Detalle FAIL** | `test_paris_classification.py::test_recursive_glob_ingests_from_subdirectories` — DB locked |
| | `test_v4_surgical_pipeline.py::test_full_pipeline_ingestion_classification_and_audit` — DB locked |
| **Detalle SKIP** | 8 taxonomy tests — `knowledge/taxonomy/` no existe (archivos en `KnowledgeBase/Marketplace/Taxonomy/`) |

## E-010: API routes

| Campo | Valor |
|-------|-------|
| **Archivo** | `api/api.py` |
| **Comando** | `[route.path for route in app.routes]` |
| **Resultado** | 37 rutas registradas (ver TECHNICAL_CERTIFICATION.md §6) |
| **Test** | `test_api_smoke.py::test_all_routes_exist` — PASS |

## E-011: Regression contracts

| Campo | Valor |
|-------|-------|
| **Archivo** | `test_regression_contracts.py` |
| **Cobertura** | 8 casos: ML, RIPLEY, PARIS, FALABELLA |
| **Resultado** | 12 tests PASS, SQL=API=Panel con $0 delta |

## E-012: Waterfall conservation

| Campo | Valor |
|-------|-------|
| **Test** | `test_certification_gate.py::test_gate_waterfall_conservation` |
| **Resultado** | ML: PASS, PARIS: PASS, RIPLEY: PASS, FALABELLA: PASS |
| **Fórmula** | `ing + dev + cob + rec = disp` con delta < $1 |

## E-013: Exec summary vs Waterfall

| Campo | Valor |
|-------|-------|
| **Test** | `test_certification_gate.py::test_gate_exec_summary_vs_waterfall` |
| **Resultado** | 4/4 MPs PASS |
| **Fórmula** | `exec.net_profit == waterfall.disponible` con delta < $1,000 |

## E-014: Financial structure endpoint

| Campo | Valor |
|-------|-------|
| **Endpoint** | `GET /api/v4/financial-structure?marketplace=RIPLEY&signal_mode=SIGNAL` |
| **Resultado** | 5 categorías: Ingresos $93.9M, Devoluciones -$15.6M, Costos Op -$2.2M, Costos Com -$8.0M, Ajustes -$7.2K |
| **Otros MPs** | ML: 6 cats, PARIS: 6 cats, FALABELLA: 5 cats |

## E-015: RIPLEY P&L operacional vs total

| Campo | Valor |
|-------|-------|
| **Consulta** | `SELECT COALESCE(include_in_operational_pnl, -1) as op, SUM(monto) FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' GROUP BY 1` |
| **Resultado** | op_pnl=1: $X (señal), op_pnl=0: $2.18B (ruido/tesorería) |
| **Ratio** | ~4.4% del valor RIPLEY es operacional (señal P&L) |

## E-016: Financial groups

| Campo | Valor |
|-------|-------|
| **Consulta** | `SELECT DISTINCT LOWER(financial_group) FROM marketplace_ledger_v1 WHERE financial_group IS NOT NULL` |
| **Resultado** | 7 grupos: ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes, recuperaciones_y_bonificaciones, tesoreria |

## E-017: Per-MP rows and value

| Campo | ML | RIPLEY | PARIS | FALABELLA |
|-------|-----|--------|-------|-----------|
| **Rows** | 107,482 | 219,901 | 74,028 | 678 |
| **Valor** | $901.7M | $2,139.9M | $337.6M | $2.6M |
| **% del total** | 26.7% | 54.7% | 18.4% | 0.2% |

## E-018: Date range

| Campo | Valor |
|-------|-------|
| **Consulta** | `SELECT MIN(fecha), MAX(fecha) FROM marketplace_ledger_v1` |
| **Resultado** | 2025-01-01 to 2026-12-06 |

## E-019: Cierre periods with data

| MP | Primer período | Último período | Cantidad |
|----|---------------|----------------|----------|
| ML | 2025-01 | 2026-06 | 19 |
| RIPLEY | 2025-01 | 2026-06 | 19 |
| PARIS | 2025-01 | 2026-06 | 19 |
| FALABELLA | 2026-03 | 2026-06 | 4 |

## E-020: Hardcoded paths

| Archivo | Línea | Ruta |
|---------|-------|------|
| `engine/v4/database.py` | 12 | `C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db` |
| `engine/v4/surgical_loader.py` | 12-15 | `ROOT = Path(r"C:\Users\ASUS Zenbook\...")` |
| `engine/v4/dte_indexer.py` | 13-19 | `self.raw_dir = Path(r"C:\Users\ASUS Zenbook\...\01_Raw\...")` |

## E-021: Singleton database connection

| Archivo | Líneas | Patrón |
|---------|--------|--------|
| `engine/v4/database.py` | 41-58 | `DatabaseV4._instance = None` + `DatabaseV4.reset()` |
| `test_regression_contracts.py` | 53-54 | `except Exception: DatabaseV4.reset()` |

## E-022: SQL injection

| Archivo | Línea | Código |
|---------|-------|--------|
| `engine/v4/explainability/explainability_engine.py` | 209 | `sql += f" WHERE l.financial_group='{g}' AND l.marketplace='{mp}'"` |

## E-023: Taxonomy path mismatch

| CLAUDE.md dice | Realidad | Impacto |
|----------------|----------|---------|
| `knowledge/taxonomy/ripley_v1.json` | `KnowledgeBase/Marketplace/Taxonomy/ripley_v1.json` | 8 tests SKIP |
| `knowledge/core/CONCEPT_REGISTRY_V2.md` | No existe | — |
| `knowledge/core/EVENT_REGISTRY_V2.md` | No existe | — |

## E-024: CORS

| Archivo | Línea | Código |
|---------|-------|--------|
| `api/api.py` | `allow_origins=["*"]` | Permite cualquier origen |

## E-025: Dependencias

| Archivo | Contenido |
|---------|-----------|
| `package.json` | `dependencies: {}`, `devDependencies: {}` |
| `pyproject.toml` | Sin dependencias Python |

## E-026: CI/CD

| Ruta | Estado |
|------|--------|
| `.github/workflows/` | Vacío — no existe pipeline CI/CD |
