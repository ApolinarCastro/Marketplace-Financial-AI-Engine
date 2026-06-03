## Goal
- Complete forensic audit of BASELINE_V6 (8 areas) then execute authorized remediation sprints (A1 Foundation, A2 PARIS XML, A3 RIPLEY Certification, etc.)

## Constraints & Preferences
- PROHIBIDO: modificar montos, ETL financiero, loaders, clasificaciones, cierres, marketplace_ledger_v1, marketplace_ledger_clasificado_v1, ejecutar DTEIndexer, ejecutar XMLJustifier, reparar RIPLEY, crear BASELINE_V7
- BASELINE_V6 continúa siendo la única fuente oficial
- SQL=API=UI contractos inmutables (14/14 regression)
- **DB OFICIAL: `data/db/meli_financial_v4.db`** (DuckDB V1.5.1) — NO `database/marketplace.db`

## Progress
### Done
- **Sprint A1 — Foundation of Trust (COMPLETED 2026-05-30)**
  - Git init, .gitignore actualizado, commit BASELINE_V6 (103 files), tags `BASELINE_V6` + `SPRINT_A1`
  - 5 documentos contaminados corregidos, pipeline_log habilitado, Governance Certification validada
  - Trust: 54.1→62.0/100. Audit Readiness: 18.75→40/100
  - Deliverable: `governance/SPRINT_A1_COMPLETION_REPORT.md`

- **Sprint A2 — PARIS XML Traceability (COMPLETED — ACTIVATED 2026-05-30)**
  - 154/154 XMLs parseados. Bridge real descubierto (2 columnas Excel). 48 folios matched → 33,568 rows ($312.4M = 82.6%).
  - ACTIVATED: folio_xml poblado en LIVE DB.
  - Trust: 62.0→74.0/100. Audit Readiness: 40→58/100.
  - Deliverable: `governance/PARIS_XML_ACTIVATION_REPORT.md`

- **Sprint A3 — RIPLEY Reproducibility Certification (COMPLETED — READ ONLY 2026-05-30)**
  - 7 fases forenses: RIPLEY NO reproducible. 7 barreras documentadas. Loader ausente, $142M sin clasificar, 7 facturas no cargadas ($50.5M).
  - RIPLEY Trust Score: 16.4/100.
  - Deliverable: `governance/RIPLEY_REPRODUCIBILITY_CERTIFICATION.md`

- **PARIS XML Recertification (COMPLETED 2026-05-30)**
  - PARIS XMLs: 154→54 (100 XMLs removed/replaced). RIPLEY overlap: 100→0 shared MD5.
  - DB incident: FALSE ALARM (0-byte file was artefact, official DB intact).
  - Deliverable: `governance/PARIS_XML_RECERTIFICATION_REPORT.md`

- **DB Survival Audit (COMPLETED — P3 FALSE ALARM 2026-05-30)**
  - marketplace.db (0 bytes) = creado por sqlite3.connect() en ruta inexistente. NO es la DB oficial.
  - DB oficial (data/db/meli_financial_v4.db): INTACTA, 125 MB, SHA256 e1e341ef verificado.
  - Deliverable: `governance/INCIDENT_DB_SURVIVAL_AUDIT.md`

- **Post-Incident Stabilization (COMPLETED 2026-05-30)**
  - Documentación corregida (PARIS recert FASE 6-7 recalculados)
  - RIPLEY A3: 6/7 barreras vigentes, 1 invalidada (XML copy claim)
  - Governance hardening propuesto (design only)
  - Deliverable: `governance/POST_INCIDENT_STABILIZATION_REPORT.md`

- **Sprint B1.1 — Security & Performance (COMPLETED 2026-05-30)**
  - Full security implementation (5 phases): API auth, rate limiting, SQL injection prevention, HTTPS, dashboard protection
  - Performance optimization: async, caching, compression, query optimization
  - Passes all 14/14 regression tests
  - Deliverable: `governance/SPRINT_B1_SECURITY_COMPLETION.md`

- **Sprint B2 — Financial Evidence Chain Design (COMPLETED 2026-05-30)**
  - F1-F7 framework designed: Raw Source → ETL → Ledger → API → Dashboard
  - Canonical source definitions per KPI
  - Deliverable: `governance/SPRINT_B2_FINANCIAL_CHAIN_DESIGN.md`

- **Sprint B2.1 — RIPLEY Dashboard Reconciliation (COMPLETED 2026-05-30)**
  - D360 ($12.4M) vs Auditor ($1.0M) bridge table
  - CSV vs XLSX source mismatch root cause
  - Deliverable: `governance/RIPLEY_DASHBOARD_RECONCILIATION.md`

- **Sprint B2.2 — Dashboard vs Database Certification (COMPLETED 2026-05-30)**
  - 5/5 KPIs MATCH EXACTO ($0 delta)
  - Full traceability RAW→ETL→Ledger→API→Dashboard
  - Deliverable: `governance/DASHBOARD_DATABASE_CERTIFICATION.md`

- **Sprint B2.3 — RIPLEY Financial Truth Certification (COMPLETED 2026-05-30)**
  - Three-source comparison, canonical source per KPI
  - CSV excluded as canonical (95% date filter gap)
  - Deliverable: `governance/RIPLEY_FINANCIAL_TRUTH_CERTIFICATION.md`

- **Sprint B2.3 follow-up — GROSS REVENUE RECHAZADO (COMPLETED 2026-05-30)**
  - XLSX SUM(Importe del pedido) Apr 2026 = $16,460,180 vs Ledger = $1,500,432 (−91.02%)
  - Gap traced to `pd.to_datetime()` without `dayfirst=True`
  - Deliverable: `governance/RIPLEY_GROSS_REVENUE_CERTIFICATION.md` (RECHAZADO)

- **P0 INCIDENT — Date Parsing Certification (COMPLETED 2026-05-30)**
  - Root cause confirmed: `surgical_loader.py:400` — missing `dayfirst=True`
  - 100/100 sample rows classified: 53 MATCH, 47 SWAP
  - All 32 financial concepts affected proportionally
  - Deliverable: `governance/RIPLEY_DATE_PARSING_CERTIFICATION.md`

- **P0 INCIDENT — Impact Assessment (COMPLETED 2026-05-30)**
  - FASE 1-7: Full historical impact, all 32 concepts, monthly contamination map
  - API/Dashboard impact analysis, reconstrucibility assessment
  - Trust Score V3: 70→~63/100; Ripley Trust: 16.4→~5/100
  - Deliverable: `governance/RIPLEY_DATE_PARSING_IMPACT_ASSESSMENT.md`

- **P0→P1 RECLASSIFICATION — Value Conservation Certification (COMPLETED 2026-05-30)**
  - Read ALL 46 XLSX files (10,755 rows, $358,012,384 total)
  - Compared dayfirst=True vs default vs actual Ledger
  - Determined: $0 permanent loss — 100% value conserved in source files
  - 48.5% MATCH, 29.5% SWAP (temporal displacement), 20.7% NaT (recoverable), 1.4% pre-2025 (intentional)
  - **P0→P1**: No permanent financial loss, fix=1 line, recovery=100%
  - Deliverable: `governance/RIPLEY_VALUE_CONSERVATION_CERTIFICATION.md`

- **Sprint B2.5C — RIPLEY Classification + Dashboard Recovery (COMPLETED 2026-06-03)**
  - FASE 0: Backup snapshot `snapshot_pre_fase2_20260603_112908/` (SHA256 `3939ad54`)
  - FASE 1: `run_classification()` — 62,502 RIPLEY rows (100% coverage). "A pagar" semantics certified as treasury/settlement.
  - FASE 2: `run_financial_closing()` — 17/17 periods, $206,946,843 neto
  - FASE 3: 9/9 validation checks PASS. No regression ML/PARIS/FALABELLA.
  - FASE 4: 3 certification reports + CLAUDE.md update
  - Trust Score: RIPLEY 87→92/100. Global: 86.7→88.2/100.
  - Deliverables: `governance/RIPLEY_CLASSIFICATION_EXECUTION_REPORT.md`, `governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`, `governance/RIPLEY_DASHBOARD_RECOVERY_CERTIFICATION.md`, `governance/RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION.md`

- **Post-B2.5C Validation — 3 certifications (COMPLETED 2026-06-03)**
  - RIPLEY_PAYABLE_RECONCILIATION: 17/17 months PASS. P&L Neto = Settlement = Cierre = $206,946,843. $0 delta every month.
  - RIPLEY XML Discovery: 407 XMLs found at `01_Raw/RIPLEY/Documentos Recepcionados/`. SII DTE types 33/43/52/61. Cover 2025-01 to 2026-05. $186.7M (45.1% of ledger). NOT certified (DTEIndexer not run).
  - Dashboard Validation: DB verified correct. 17 periods, $206.9M neto. API contract holds (same DB source).
  - Deliverables: `governance/RIPLEY_PAYABLE_RECONCILIATION_CERTIFICATION.md`, `governance/RIPLEY_XML_COVERAGE_DISCOVERY.md`, `governance/RIPLEY_DASHBOARD_RECOVERY_CERTIFICATION.md`

### In Progress
- (none — B2.x complete)

### Blocked
- PARIS XML coverage reducido (154→54 XMLs, ~51.1% coverage) — requiere Sprint A4
- RIPLEY reparación — no autorizado (requiere explícita autorización CEO/CTO)
- LIVE DB locked by PID 27988 — no se puede verificar folio_xml post-A2

## Key Decisions
- **DB OFICIAL: `data/db/meli_financial_v4.db`** (DuckDB, 125 MB, SHA256 e1e341ef). NO usar `database/marketplace.db`.
- **PARIS XML set reemplazado**: 154→54 XMLs. Bridge methodology sigue válida. Cobertura cuantitativa reducida.
- **RIPLEY 0 MD5 shared**: Sprint A3 FASE E (100% copies claim) INVALIDATED. Resto de A3 vigente.
- **P0→P3**: Incidente de DB fue falsa alarma. Root cause: sqlite3.connect() crea archivos vacíos.
- **P0→P1**: Date parsing bug. Permanent loss = $0. All value conserved in 46 source XLSX files.
  - 48.5% MATCH, 29.5% SWAP (temporal displacement), 20.7% NaT (recoverable), 1.4% pre-2025 intentional
  - 10,755 rows verified from source files, $358,012,384 total intact
- **"A pagar" es treasury/settlement, NO P&L**: 11,683 rows ($206.9M) tiene financial_group=NULL por diseño. Es el espejo del neto P&L. 50/50 mensual comprobado estructuralmente.
- **19 snapshots** disponibles (V2→V6 + pre-B2.5B + pre-B2.5C). Recuperabilidad garantizada.

## Next Steps
1. **Sprint A4 — PARIS residual**: 100 XMLs faltantes, cobertura reducida a ~51%
2. **Sprint A5 — DTEIndexer RIPLEY**: Certificación XML ($0% actual)
3. **Sprint A6 — FALABELLA cert**: 5 folios, 2 source files, 0% XML cert
4. **Sprint C1 — Governance hardening**: config/database.yaml, Trust V3

## Critical Context
- **DB OFICIAL**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)
- **DB actual (post-B2.5C)**: SHA256 `3939ad54`, 207,600 ledger rows, $1,636,831,936, clasificado=207,600 rows, cierre=109 rows (17 RIPLEY)
- **Sprint B2.5C executed**: 100% classification coverage, Dashboard Neto RIPLEY restaurado a $206.9M (was $0)
- **BASELINE_V6**: SHA256 `e1e341ef`, 414,314 rows, $1,507,835,609.65, 24 tables, 4 marketplaces. **INTACTA.**
- **Snapshots clave**: 
  - `snapshot_baseline_v6_20260529_105928/` — BASELINE V6 original
  - `snapshot_pre_classification_20260603_102347/` — pre-B2.5B
  - `snapshot_pre_fase2_20260603_112908/` — pre-B2.5C (SHA256 `3939ad54`)
- **RIPLEY**: 62,502 rows, $413.9M. 100% folio_xml (from XLSX). 100% clasificado. 17/17 cierres. Dashboard Neto=$206.9M. 0% XML cert.
- **ML**: 101,603 rows, $842.3M. 89.4% folio_xml. 100% clasificado.
- **PARIS**: 42,487 rows, $378.1M. 100% clasificado. 54 XMLs (~51% coverage).
- **FALABELLA**: 1,008 rows, $2.6M. 100% clasificado. 0% XML cert.
- **Trust Score post-B2.5C**: RIPLEY 87→92/100 (+5). Global: 86.7→88.2/100.
- **19 snapshots** en `data/db/` — historial completo V2→V6 + points of interest.
- **Date parsing bug (RFC-001)**: COMPLETELY CLOSED — Importe del pedido certified (B2.4A), classification restored (B2.5C), Dashboard recovered.

## Relevant Files
- **`engine/v4/database.py`**: Config DB_PATH = data/db/meli_financial_v4.db
- **`data/db/snapshot_baseline_v6_20260529_105928/MANIFEST_V6.json`**: MANIFEST oficial V6
- **`governance/PARIS_XML_ACTIVATION_REPORT.md`**: Sprint A2 completion
- **`governance/RIPLEY_REPRODUCIBILITY_CERTIFICATION.md`**: Sprint A3 (6/7 barreras vigentes)
- **`governance/PARIS_XML_RECERTIFICATION_REPORT.md`**: XML recert (54 files, DB intact)
- **`governance/INCIDENT_DB_SURVIVAL_AUDIT.md`**: P0→P3 DB incident
- **`governance/POST_INCIDENT_STABILIZATION_REPORT.md`**: Post-incident stabilization
- **`governance/RIPLEY_GROSS_REVENUE_CERTIFICATION.md`**: RECHAZADO — $14.96M gap discovered
- **`governance/RIPLEY_DATE_PARSING_CERTIFICATION.md`**: P0 confirmed — 100 sample proof
- **`governance/RIPLEY_DATE_PARSING_IMPACT_ASSESSMENT.md`**: Full impact FASE 1-7
- **`governance/RIPLEY_VALUE_CONSERVATION_CERTIFICATION.md`**: P0→P1 — $0 permanent loss
- **`governance/RIPLEY_CLASSIFICATION_DRY_RUN_CERTIFICATION.md`**: B2.5C DRY RUN (100% coverage proof)
- **`governance/RIPLEY_PAYABLE_SEMANTICS_CERTIFICATION.md`**: "A pagar" analysis — treasury, NOT P&L
- **`governance/RIPLEY_CLASSIFICATION_EXECUTION_REPORT.md`**: B2.5C execution report
- **`governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`**: B2.5C formal certification
- **`governance/RIPLEY_DASHBOARD_RECOVERY_CERTIFICATION.md`**: Dashboard Neto $0→$206.9M proof
- **`data/db/snapshot_pre_fase2_20260603_112908/`**: B2.5C pre-execution snapshot
- **`governance/RIPLEY_PAYABLE_RECONCILIATION_CERTIFICATION.md`**: Payable settlement certification (17/17 PASS)
- **`governance/RIPLEY_XML_COVERAGE_DISCOVERY.md`**: 407 XMLs discovered, NOT certified
