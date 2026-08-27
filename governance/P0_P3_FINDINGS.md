# P30 — P0/P1/P2/P3 FINDINGS

Clasificación basada exclusivamente en evidencia ejecutable.

---

## P0 — Impide Operar

### F-001: Ledger → Cierre no converge

| Campo | Valor |
|-------|-------|
| **Archivo** | `marketplace_cierre_financiero_v1` / `marketplace_ledger_v1` |
| **Evidencia** | Ledger $3.38B vs Cierre $1.31B = gap $2.07B |
| **E-REF** | E-003, E-004 |
| **Impacto** | Single Financial Truth NO se cumple. No se puede confiar en resultado_neto como source of truth. |
| **Detalle** | RIPLEY contribuye $1.8B del gap. ML contribuye $291.5M. |

### F-002: RIPLEY gap masivo ledger vs cierre

| Campo | Valor |
|-------|-------|
| **Archivo** | `marketplace_ledger_v1` / `marketplace_cierre_financiero_v1` |
| **Evidencia** | RIPLEY ledger $2.14B, cierre $337M = gap $1.80B |
| **E-REF** | E-004 |
| **Impacto** | 54.7% de las transacciones del sistema no convergen con el cierre. RIPLEY no puede reportarse financieramente. |
| **Causa** | op_pnl=0 (no operacional) explica $2.18B de RIPLEY — 95.6% del valor es tesorería, no P&L |

### F-003: Sin dependencias Python declaradas

| Campo | Valor |
|-------|-------|
| **Archivo** | `package.json`, `pyproject.toml` |
| **Evidencia** | `dependencies: {}`, `devDependencies: {}`. No hay `pyproject.toml` con deps. |
| **E-REF** | E-025 |
| **Impacto** | No se puede reconstruir el entorno. `import duckdb`, `import fastapi` funcionan solo si están instalados manualmente. |

### F-004: Rutas absolutas hardcoded

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/database.py:12`, `surgical_loader.py:12`, `dte_indexer.py:13-19` |
| **Evidencia** | `Path(r"C:\Users\ASUS Zenbook\...")` |
| **E-REF** | E-020 |
| **Impacto** | El sistema funciona SOLO en la máquina del desarrollador. Cero portabilidad. |

---

## P1 — Riesgo Alto

### F-005: Sin índices en DuckDB

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/database.py` |
| **Evidencia** | No hay `CREATE INDEX` en ninguna parte |
| **Impacto** | Full table scans en cada query. `SELECT COUNT(folio_xml) FROM marketplace_ledger_v1` escanea 402K rows. |
| **Rendimiento actual** | DuckDB columnar maneja 402K rows sin problema, pero no escala a millones. |

### F-006: SQL injection en ExplainabilityEngine

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/explainability/explainability_engine.py:209` |
| **Evidencia** | `sql += f" WHERE l.financial_group='{g}' AND l.marketplace='{mp}'"` |
| **E-REF** | E-022 |
| **Impacto** | `marketplace` y `financial_group` vienen del endpoint. Si un atacante controla estos valores, puede inyectar SQL. |

### F-007: Singleton DatabaseV4 con reset cascada

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/database.py:41-58` |
| **Evidencia** | `DatabaseV4._instance = None` en error → todas las conexiones existentes mueren |
| **E-REF** | E-021 |
| **Impacto** | Un error SQL en un request puede matar la conexión para todos los demás requests concurrentes. |

### F-008: Sin DTE coverage para FALABELLA

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_ledger_v1` WHERE LOWER(marketplace)='falabella' |
| **Evidencia** | 0/678 rows con folio_xml no NULL |
| **E-REF** | E-005 |
| **Impacto** | FALABELLA no tiene respaldo documental. Cualquier auditoría rechazaría estos datos. |

### F-009: Sin auditoría para PARIS y FALABELLA

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_auditoria_v1` |
| **Evidencia** | 0 alerts para PARIS, 0 alerts para FALABELLA |
| **E-REF** | E-008 |
| **Impacto** | No hay detección de anomalías para 2 de 4 MPs. PARIS tiene $337.6M sin supervisión de auditoría. |

### F-010: CORS abierto

| Campo | Valor |
|-------|-------|
| **Archivo** | `api/api.py` |
| **Evidencia** | `allow_origins=["*"]` |
| **Impacto** | Cualquier sitio web puede hacer requests a la API. En entorno de producción, es riesgo de seguridad. |

### F-011: DTE documents indexados pero no vinculados

| Campo | Valor |
|-------|-------|
| **Tablas** | `dte_truth_v1` (667 docs) vs `folio_xml` en ledger (219 distinct) |
| **Evidencia** | 667 - 219 = 448 documentos DTE sin vincular a transacciones |
| **E-REF** | E-006 |
| **Impacto** | 67% de los XML procesados no tienen contraparte en ledger. La cobertura DTE real es menor que la reportada. |

### F-012: Taxonomy path mismatch

| Campo | Valor |
|-------|-------|
| **Archivo** | `tests/test_certification_gate.py` espera `knowledge/taxonomy/` |
| **Evidencia** | 8 tests SKIP porque los archivos están en `KnowledgeBase/Marketplace/Taxonomy/` |
| **E-REF** | E-023 |
| **Impacto** | Certification gate NO puede validar taxonomía. `test_gate_taxonomy_has_no_orphans` y `test_gate_taxonomy_groups_cover_financial_groups` están SKIP. |

---

## P2 — Mejora Importante

### F-013: God object FinancialEngine

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/domain/financial_engine.py` |
| **Evidencia** | 10+ métodos públicos: `resolve_period_range`, `clean_records`, `map_detalle_to_concept`, `list_periods`, `query_cierre`, `query_desglose`, `query_ledger`, `query_cobros_breakdown`, `query_exec_summary`, `query_waterfall`, `query_audit`, `query_operational_intelligence`, `query_financial_structure` |
| **Impacto** | Difícil de testear, mantener, extender. Cualquier cambio en FinancialEngine afecta 7+ engines. |

### F-014: cierre > ledger para PARIS y FALABELLA

| Campo | Valor |
|-------|-------|
| **Evidencia** | PARIS: cierre $355.7M > ledger $337.6M. FALABELLA: cierre $8.6M > ledger $2.6M |
| **E-REF** | E-004 |
| **Impacto** | El cierre tiene más valor que el ledger — inconsistencia matemática. Puede ser por rows cargadas directamente al cierre sin pasar por ledger. |

### F-015: Sin CI/CD

| Campo | Valor |
|-------|-------|
| **Ruta** | `.github/workflows/` |
| **Evidencia** | Directorio vacío — no hay pipeline |
| **Impacto** | Tests solo se ejecutan manualmente. No hay verificación automática de regresión. |

### F-016: DuckDB como DB transaccional

| Campo | Valor |
|-------|-------|
| **Archivo** | `engine/v4/database.py` |
| **Evidencia** | DuckDB es columnar (analítico). Se usa para OLTP (writes single-row from loader). |
| **Impacto** | Sin transacciones, sin row-level locking, sin concurrent write support. `insert_df` con dedup no es ACID. |

### F-017: 173,926 rows no operacionales ($2.18B)

| Campo | Valor |
|-------|-------|
| **Tabla** | `marketplace_ledger_v1` |
| **Evidencia** | `SELECT COALESCE(include_in_operational_pnl, -1), COUNT(*), SUM(monto) GROUP BY 1` |
| **E-REF** | E-015 |
| **Impacto** | 43% de las transacciones ($64% del valor) son no operacionales. El P&L real es solo $1.21B de $3.38B. |

### F-018: Sin autenticación en API

| Campo | Valor |
|-------|-------|
| **Archivo** | `api/api.py` |
| **Evidencia** | No hay middleware que valide API keys |
| **Impacto** | Cualquier persona con acceso a la red puede consultar datos financieros. |

### F-019: No hay conftest.py

| Campo | Valor |
|-------|-------|
| **Archivo** | `tests/conftest.py` no existe |
| **Evidencia** | Fixtures como `fe` (FinancialEngine) creados en cada test file |
| **Impacto** | Setup duplicado, difícil de mantener. Tests dependen de DB real. |

---

## P3 — Refactor Futuro

### F-020: Sin Pydantic models

| Archivo | `api/api.py` — parámetros pasados como raw strings |
|---------|-----------------------------------------------------|
| **Impacto** | Sin validación automática de tipos. Errores detectados en runtime. |

### F-021: Cierre all retorna 1 row con $0

| Evidencia | `GET /api/v4/cierre` → `[{"marketplace": "ALL", "resultado_neto": 0}]` |
|-----------|------------------------------------------------------------------------|
| **Impacto** | Endpoint de cierre consolidado no funcional. Siempre retorna $0. |

### F-022: Sin manejo de errores estandarizado en API

| Evidencia | Algunos endpoints retornan `{"error": "..."}`, otros retornan `[]`, otros lanzan excepción |
|-----------|-------------------------------------------------------------------------------------------|
| **Impacto** | Cliente API no puede asumir formato de error consistente. |

### F-023: Nombres de ruta inconsistentes

| Evidencia | `/api/v4/exec/waterfall-v3` (no `/api/v4/exec/waterfall`). `/api/v4/cierre` (no `/cierre/all`) |
|-----------|------------------------------------------------------------------------------------------------|
| **Impacto** | `-v3` en nombre de ruta es code smell. Confunde a consumidores de API. |

### F-024: Tests dependen de DB real

| Evidencia | No hay MockDatabase. `test_regression_contracts.py` usa `DatabaseV4.get()` |
|-----------|---------------------------------------------------------------------------|
| **Impacto** | Tests no pueden correr sin la DB. 2 tests FAIL cuando DB está locked. |

---

## Resumen

| Severidad | Cantidad | Descripción |
|-----------|----------|-------------|
| **P0** | 4 | Bloquean operación del sistema |
| **P1** | 8 | Riesgo alto para producción |
| **P2** | 7 | Mejora importante necesaria |
| **P3** | 4 | Refactor futuro |
| **Total** | **23** | |
