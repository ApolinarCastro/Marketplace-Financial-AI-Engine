## Goal
- Complete forensic audit of BASELINE_V6 (8 areas) then execute authorized remediation sprints (A1 Foundation, A2 PARIS XML, A3 RIPLEY Certification, etc.)

## Constraints & Preferences
- PROHIBIDO: modificar montos, ETL financiero, loaders, clasificaciones, cierres, marketplace_ledger_v1, marketplace_ledger_clasificado_v1, ejecutar DTEIndexer, ejecutar XMLJustifier, reparar RIPLEY, crear BASELINE_V7
- BASELINE_V6 continúa siendo la única fuente oficial
- SQL=API=UI contractos inmutables (14/14 regression)
- **DB OFICIAL: `data/db/meli_financial_v4.db`** (DuckDB V1.5.1) — NO `database/marketplace.db`

## SOURCE OF TRUTH OFICIAL
- **Marketplace Financial = única fuente de verdad financiera corporativa.**
- `marketplace_ledger_v1.financial_group='ingresos'` = fuente oficial de Ventas.
- `marketplace_ledger_v1.financial_group='devoluciones'` = fuente oficial de Devoluciones.
- `marketplace_cierre_financiero_v1.resultado_neto` = fuente oficial de Disponible.
- **Reporte_Gerencial_Marketplaces = LEGACY.** No utilizar para validar KPIs financieros oficiales.
- Toda conciliación debe realizarse contra Marketplace Financial.
- Looker Studio no es fuente oficial. Ninguna visualización externa reemplaza la DB oficial.

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

- **G5.6 — Revenue Engine Decomposition (COMPLETED 2026-06-03)**
  - FASE 1-5: Complete revenue driver inventory per MP — RIPLEY (9 drivers, 17.9% take rate), ML (16 drivers, 3.7% net via 90.3% adj ratio), PARIS (12 drivers, implicit $48.7M commission), FALABELLA (8 drivers, 24.1% rate)
  - Monetization classification: RIPLEY = commission hybrid, PARIS = margin 1P, ML = adjustment-eroded, FALABELLA = commission high-rate
  - ML identified as #1 financial vulnerability — net revenue 3× more sensitive to adjustment ratio than to GMV
  - Stress test at -10/-20/-30% with dual-variable analysis for ML
  - 4 certificates PASS, $0 residual
  - Deliverables: `governance/REVENUE_ENGINE_DECOMPOSITION.md`, `governance/REVENUE_ENGINE_STRESS_TEST.md`, `governance/REVENUE_ENGINE_CERTIFICATION.md`

- **G5.7 — Marketplace Value Creation Opportunities (COMPLETED 2026-06-03)**
  - FASE 1: Full opportunity inventory — 20+ levers classified ALTO/MEDIO/BAJO per marketplace
  - FASE 2: Revenue recovery analysis — $306.6M ML adjustments decomposed, $308.7M returns quantified, $98.7M logistics base identified
  - FASE 3: Margin simulator — +1%/+3%/+5% scenarios for all 4 MPs. ML shows +179.5% potential
  - FASE 4: Negotiation Playbook — TOP 20 concepts ranked by expected return × probability. Quick wins: reconciled ($29.4M), penalidades ($14.8M), RIPLEY penalties ($3.0M)
  - FASE 5: 90/180/365-day roadmap — $56.3M in first 90 days, $147M at 365 days
  - 7 questions answered: Easiest money = reconciled adjustments. Highest impact = ML adjustments. Best negotiation = ML logistics. Best MP = ML (+193% potential). Least effort = penalidades. No-selling improvement = adj reduction.
  - **Paradox:** ML has worst economics but largest opportunity. RIPLEY best economics, smallest relative opportunity.
  - Deliverables: `governance/MARKETPLACE_VALUE_CREATION_OPPORTUNITIES.md`, `governance/MARGIN_IMPROVEMENT_SIMULATOR.md`, `governance/NEGOTIATION_PLAYBOOK.md`, `governance/VALUE_CREATION_ROADMAP.md`

- **E1.0 — Executable Value Capture Plan (COMPLETED 2026-06-03)**
  - 5 Eccsa-controlled projects: RIPLEY penalidades ($6.7M EV), PARIS inventory ($0.9M), ML Poscobro ($0.5M)
  - Total portfolio: $8.06M expected value, $160K investment, 4,940% ROI, < 2 week payback
  - All require zero external approval — Eccsa alone can execute
  - 6-sprint backlog, 14-week implementation plan, KPI dashboard
  - 8 questions answered: Start tomorrow (all 5), least effort = P3 ($652K, process only), most money = P1 ($3.36M), lowest risk = P4 ($268K, ops fix), 90-day capture = $5.9-7.3M
  - **Verdict:** $8.06M is Eccsa's to lose. No contracts, no third parties, no negotiations. Only execution.
  - Deliverables: `governance/EXECUTABLE_PROJECT_PORTFOLIO.md`, `governance/BUSINESS_CASE_LIBRARY.md`, `governance/VALUE_CAPTURE_BACKLOG.md`, `governance/EXECUTIVE_VALUE_TRACKING.md`

- **E1.1 — Expected Value Traceability Certification (COMPLETED 2026-06-03)**
  - FASE 1-5: Every peso traced to DB or source. P1/P2 identified as double-count ($3.36M inflation corrected)
  - Portfolio corrected: $8,064,479 → **$4,709,456** (42% overstatement removed)
  - Classification: 0% HECHO puro, 71% BENCHMARK, 90% ESTIMACIÓN, 10% HIPÓTESIS
  - 11 assumptions registered with worst/best case analysis
  - P5 excluded from dashboard (speculative — "under investigation")
  - Range: $2.0M worst case / $4.7M expected / $9.2M best case
  - Deliverables: `governance/EXPECTED_VALUE_TRACEABILITY_CERTIFICATION.md`, `governance/PROJECT_CONFIDENCE_MATRIX.md`, `governance/EXECUTIVE_ASSUMPTION_REGISTER.md`

- **G5.7A — Opportunity Feasibility Certification (COMPLETED 2026-06-03)**
  - FASE 1: Unified catalog of 27 opportunities from G5.7 ($243.7M gross potential)
  - FASE 2: Feasibility per opportunity — 4 INTERNO ($8.3M), 12 EXTERNO ($117.4M), 11 MIXTO ($118.0M)
  - FASE 3: Conservative probability assignment — MUY ALTA (95%) to MUY BAJA (5%)
  - FASE 4: Expected value = Gross × Probability — $243.7M → **$46.4M** expected
  - FASE 5: Executive matrix — Quick Wins ($17.1M), Mid Term ($17.4M), Strategic ($12.2M)
  - 9 questions answered: Realistic value = $46.4M. Eccsa-controlled = $11.6M. Third-party = $34.8M. 90-day capture = $14.2M. #1 = reconciled ($8.2M EV). First action = penalidades.
  - **Key insight:** $243.7M mathematically possible → $46.4M realistically executable → $23.2M conservative floor
  - Deliverables: `governance/OPPORTUNITY_FEASIBILITY_CERTIFICATION.md`, `governance/EXECUTABLE_VALUE_MATRIX.md`, `governance/REALISTIC_VALUE_CREATION_ROADMAP.md`

- **UX1.0 — Executive Dashboard (COMPLETED 2026-06-04)**
  - New standalone page at `/exec` with 4 components: Executive Summary (4 KPI cards — certified data), Marketplace Scorecard (4 per-MP cards with gross/net/margin/alerts), Financial Waterfall (Chart.js stacked bar, filterable per MP or consolidated), Drill-down to Auditor (paginated, filterable audit alerts with click-through to `/app`).
  - 5 new read-only API endpoints consuming only certified data: `/api/v4/exec/summary`, `/exec/waterfall`, `/exec/audit-drilldown`, `/exec/audit-types`, and `/exec` template route.
  - Navigation bar added to both dashboards (Auditor ↔ Executive).
  - Zero existing tables modified. Zero financial logic duplicated. Passes 14/14 regression.
  - Deliverables: `templates/executive_dashboard.html`, `api/api.py` (new endpoints)

- **UX1.1 — Executive Dashboard Convergence (COMPLETED 2026-06-04)**
  - Reverse-engineered `Reporte Gerencial 360 Marketplaces.xlsx` (13 concept types, 4 hierarchies: Ventas/Devoluciones/Cobros/Disponible, 251,651 rows across 4 MPs).
  - Gap analysis: 6 features Ya Existen, 5 Falta, 3 Mejorable — documented in `governance/GERENCIAL_GAP_ANALYSIS.md`.
  - Converged UX1.0 frontend exclusively (SOLO FRONTEND — no API/DB changes):
    - New gerencial hierarchy: **Ventas → Devoluciones → Cobros → Disponible** (replaces "Net Revenue" / "Costos Operacionales" taxonomy)
    - **4 KPI cards** with border color coding + explicabilidad tooltips per KPI (Qué es, Cómo se calcula, Qué incluye, Qué no incluye)
    - **Per-marketplace scorecard** renamed to "Distribución por Marketplace" with gerencial metrics (Ventas, Disponible, Margen Neto)
    - **Simplified waterfall**: CSS bar visualization (Ventas ↓ Devoluciones ↓ Cobros ↓ Disponible), replacing Chart.js waterfall
    - **Cobros breakdown matrix**: Per-concept × per-MP grid (Comisiones, Logística, Publicidad, Servicios, Fulfillment, Bonificaciones, Otros) — sourced from `/api/v4/cierre/desglose`
    - **Explicabilidad modal**: Each KPI links to explanations using only concepts from Economic Dictionary, Financial Truth, Money Flow Truth
    - All existing UX1.0 APIs preserved unchanged. Navigation updated: "Executive" → "Gerencial". 14/14 regression PASS.
  - Deliverables: `templates/executive_dashboard.html` (converged), `governance/GERENCIAL_GAP_ANALYSIS.md`

- **G6 — Cash Reality Certification: ML 2025-04 (COMPLETED 2026-06-05)**
  - Liberaciones file analyzed (5,142 rows, $259.8M gross, $69.9M net)
  - DB resultado_neto ($67.2M) vs Liberaciones neto ($69.9M): 3.9% delta
  - 197 paired orders (Talla+BPP, Arre+Posc): 97.5% traced to Liberaciones
  - Net cash impact of double-counted orders: -$40,599 ≈ $0
  - 4 verdicts issued: (a) MF=real cash (YES, 3.9% delta), (b) double economic impact (NO), (c) double documentary representation (YES — adjustments only), (d) confidence = ALTA
  - Deliverable: `governance/G6_CASH_REALITY_CERTIFICATION.md`

- **RFC_CASH_CERTIFICATION_BPP_POSCOBRO (COMPLETED 2026-06-05)**
  - Final certification: PASS CONDITIONAL — $134.4M (93.8%) paired mechanisms removal justified (zero cash in reserve_for_dispute), $8.8M (6.2%) standalone mechanisms must remain in P&L
  - Cash evidence: reserve_for_dispute NET=$0 EXACTO (BPP: $4.57M=, Poscobro: $2.52M=); Mediacion=$10.5M cash outflow = root events only
  - BPP orders in cash: 179/198 (90.4%), Poscobro: 92/148 (62.2%), Paired: 192/197 (97.5%)
  - All-time: $143.2M total mechanisms → $134.4M paired (removable) + $8.8M standalone (preserve)
  - Deliverable: `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md`

- **FASE 4 — V2 Core Registries (COMPLETED 2026-06-05)**
  - CONCEPT_REGISTRY_V2.md: 96 concepts across 5 MPs mapped with canonical name, financial group, event_role, cash_role, pnl_role, audit_role, coverage, cert refs
  - EVENT_REGISTRY_V2.md: Cross-MP event role assignments, 7 causality rules, 3 MECHANISMS (ML) + all others ROOT_EVENTS
  - CASH_ROLE_REGISTRY_V1.md: 18 REAL_CASH (ML), 19 ACCRUAL (ML), 54 UNASSIGNED (non-ML). Default: ACCRUAL.
  - Deliverables: `knowledge/core/CONCEPT_REGISTRY_V2.md`, `knowledge/core/EVENT_REGISTRY_V2.md`, `knowledge/core/CASH_ROLE_REGISTRY_V1.md`

- **Go-Live Audit — FASE A-C Analysis (COMPLETED 2026-06-06)**
  - FASE A: Data freshness — all 4 MPs queried. Junio 2026 NOT incorporated. PARIS/FALABELLA end Apr 2026.
  - FASE B: Ajustes & Retenciones — 10,874 ML rows ($306.6M). ROOT_EVENTS=5,573 ($163.4M). MECHANISMS=5,301 ($143.2M). BPP=$89.3M paired, Poscobro Conciliado=$41.6M, Poscobro General=$3.4M.
  - FASE C: 15-month RN impact — RN_ACTUAL=$783M → RN_SIN_PAIRED=$747M. **$35.8M (4.59%) overstatement.**
  - 3 deliverable files: DATA_FRESHNESS_CERTIFICATION.md (FAIL), AJUSTES_RETENCIONES_IMPACT.md (FAIL), GO_LIVE_AUDIT.md (FAIL)
  - Temp analysis files removed: 4 `tmp_go_live_*.py` cleaned
  - Deliverables: `governance/DATA_FRESHNESS_CERTIFICATION.md`, `governance/AJUSTES_RETENCIONES_IMPACT.md`, `governance/GO_LIVE_AUDIT.md`

### In Progress
- **FASE D — Impact Assessment**: 7/7 questions answered. RN inflated by $36M (4.59%). 3 concepts cause it. Material=YES. Audit risk=HIGHEST. Production risk=YES.
- **FASE E — Go-Live Verdicts**: 5 certifications (3 FAIL, 2 PASS). **FINAL: FAIL ❌** — 3 structural issues block go-live.

### Blocked
- (none)

## Key Decisions
- **Financial Truth Consolidation (DEC-001)**: Marketplace Financial reemplaza Reporte_Gerencial_Marketplaces como fuente oficial corporativa. Reporte_Gerencial = LEGACY.
- **DB OFICIAL: `data/db/meli_financial_v4.db`** (DuckDB, 125 MB, SHA256 e1e341ef). NO usar `database/marketplace.db`.
- **PARIS XML set reemplazado**: 154→54 XMLs. Bridge methodology sigue válida. Cobertura cuantitativa reducida.
- **RIPLEY 0 MD5 shared**: Sprint A3 FASE E (100% copies claim) INVALIDATED. Resto de A3 vigente.
- **P0→P3**: Incidente de DB fue falsa alarma. Root cause: sqlite3.connect() crea archivos vacíos.
- **P0→P1**: Date parsing bug. Permanent loss = $0. All value conserved in 46 source XLSX files.
  - 48.5% MATCH, 29.5% SWAP (temporal displacement), 20.7% NaT (recoverable), 1.4% pre-2025 intentional
  - 10,755 rows verified from source files, $358,012,384 total intact
- **"A pagar" es treasury/settlement, NO P&L**: 11,683 rows ($206.9M) tiene financial_group=NULL por diseño. Es el espejo del neto P&L. 50/50 mensual comprobado estructuralmente.
- **ML adjustment problem identified as #1 margin risk**: 90.3% of gross charges ($339.4M) returned as credits ($306.6M). Net take rate 3.7% vs gross 38.8%. ML net revenue 3× more sensitive to adjustment ratio than to GMV.
- **RIPLEY es el revenue engine más estable**: 17.9% take rate, proporcional, $63.3M net. Sin ajustes ni dependencias externas.
- **PARIS commission ($48.7M) es implícita**: embedded in P&L spread, no visible in ledger. Revenue engine = product margin, NOT marketplace fees.
- **3 monetization models identificados**: commission-driven (RIPLEY/FALABELLA), margin-driven (PARIS), adjustment-eroded + ads (ML).
- **19 snapshots** disponibles (V2→V6 + pre-B2.5B + pre-B2.5C). Recuperabilidad garantizada.

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
- **G5.6 Revenue Engine**: RIPLEY = 9 drivers, 17.9% take rate, proportional. ML = 16 drivers, 3.7% net (90.3% eroded). PARIS = 12 drivers, implicit $48.7M commission. FALABELLA = 8 drivers, 24.1% high rate.
- **19 snapshots** en `data/db/` — historial completo V2→V6 + points of interest.
- **Date parsing bug (RFC-001)**: COMPLETELY CLOSED — Importe del pedido certified (B2.4A), classification restored (B2.5C), Dashboard recovered.
- **G6 Cash Reality (ML 2025-04)**: 197 paired orders with double representation in adjustments. 97.5% traced to Liberaciones file. Net cash impact of double-counted orders: ~$0. Cash reality confirms ONE event, not two.
- **RFC Cash BPP/Poscobro**: PASS CONDITIONAL — $134.4M (93.8%) paired mechanisms removable (zero cash), $8.8M (6.2%) standalone must remain in P&L. reserve_for_dispute NET=$0 confirmed for both BPP ($4.57M=) and Poscobro ($2.52M=).
- **Go-Live Audit: FAIL ❌** — 3 structural issues block go-live: (1) RN inflation $35.8M (4.59%) from paired mechanisms, (2) Junio 2026 not incorporated for any MP, PARIS/FALABELLA end Apr 2026, (3) ML has 0 audit rows.
- **RN inflation**: $35.8M (4.59%) over 15 months. 3 concepts cause it: BPP (66.5%), Poscobro Conciliado (31.0%), Poscobro General (2.5%). All 3 are paired mechanisms in ML only.
- **Data freshness gap**: Junio 2026 = 0 rows revenue for all MPs. PARIS/FALABELLA 2 months behind (last data = Apr 2026). file_registry table EMPTY.
- **ML audit trail: 0 rows** — largest marketplace ($842M, 60% of total value) has no coverage in marketplace_auditoria_v1.
- **FASE 4 deliverables**: CONCEPT_REGISTRY_V2 (96 concepts), EVENT_REGISTRY_V2 (7 causality rules), CASH_ROLE_REGISTRY_V1 (54 UNASSIGNED non-ML).
- **FASE 4 cash default rule**: Non-ML concepts default to ACCRUAL until cash source identified. 54/96 concepts (56%) UNASSIGNED.
- **Most recent snapshot**: `snapshot_pre_poscobro_fix_20260605_155052/` (used for Go-Live Audit analysis, DB locked by PID 17680).

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
- **`governance/REVENUE_ENGINE_DECOMPOSITION.md`**: G5.6 — Monetization model per MP (commission/margin/ads)
- **`governance/REVENUE_ENGINE_STRESS_TEST.md`**: G5.6 — -10/-20/-30% scenarios, ML adj ratio risk (3×)
- **`governance/REVENUE_ENGINE_CERTIFICATION.md`**: G5.6 — 4 certificates PASS, residual $0
- **`governance/MARKETPLACE_VALUE_CREATION_OPPORTUNITIES.md`**: G5.7 — FASE 1-2 inventory + revenue recovery
- **`governance/MARGIN_IMPROVEMENT_SIMULATOR.md`**: G5.7 — FASE 3: +1%/+3%/+5% scenarios
- **`governance/NEGOTIATION_PLAYBOOK.md`**: G5.7 — FASE 4: TOP 20 negotiable concepts
- **`governance/VALUE_CREATION_ROADMAP.md`**: G5.7 — FASE 5: 90/180/365-day roadmap
- **`governance/OPPORTUNITY_FEASIBILITY_CERTIFICATION.md`**: G5.7A — FASE 1-4: catalog + feasibility + probability + expected value
- **`governance/EXECUTABLE_VALUE_MATRIX.md`**: G5.7A — FASE 5: executive matrix with execution path
- **`governance/REALISTIC_VALUE_CREATION_ROADMAP.md`**: G5.7A — Realistic roadmap replacing optimistic one
- **`governance/EXECUTABLE_PROJECT_PORTFOLIO.md`**: E1.0 — 5 Eccsa-controlled projects, $8.1M EV
- **`governance/BUSINESS_CASE_LIBRARY.md`**: E1.0 — 5 business cases with ROI, payback, risks
- **`governance/VALUE_CAPTURE_BACKLOG.md`**: E1.0 — 6 sprints, 14-week implementation plan
- **`governance/EXECUTIVE_VALUE_TRACKING.md`**: E1.0 — KPI dashboard + 8 questions answered
- **`governance/EXPECTED_VALUE_TRACEABILITY_CERTIFICATION.md`**: E1.1 — Traceability cert + P1/P2 double-count correction ($3.36M)
- **`governance/PROJECT_CONFIDENCE_MATRIX.md`**: E1.1 — Confidence per project, dashboard exclusion for P5
- **`governance/EXECUTIVE_ASSUMPTION_REGISTER.md`**: E1.1 — 11 assumptions listed, worst/best case scenarios
- **`templates/executive_dashboard.html`**: UX1.0/UX1.1 — Executive Dashboard / Reporte Gerencial converged (4 gerencial KPI cards, CSS waterfall, Cobros breakdown, audit drill-down)
- **`api/api.py`**: UX1.0 — 5 new endpoints: `/exec`, `/api/v4/exec/summary`, `/api/v4/exec/waterfall`, `/api/v4/exec/audit-drilldown`, `/api/v4/exec/audit-types`
- **`governance/GERENCIAL_GAP_ANALYSIS.md`**: UX1.1 — Gap analysis: Reporte Gerencial vs UX1.0, convergence design (FASE 1-7)
- **`governance/G6_CASH_REALITY_CERTIFICATION.md`**: G6 — Cash Reality Certification ML 2025-04
- **`governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md`**: RFC — BPP+Poscobro Cash Certification (PASS CONDITIONAL, 93.8% paired removable)
- **`governance/DATA_FRESHNESS_CERTIFICATION.md`**: Go-Live Audit FASE A — Data freshness (Junio 2026: FAIL, 0/4 MPs)
- **`governance/AJUSTES_RETENCIONES_IMPACT.md`**: Go-Live Audit FASE B+C — Ajustes & Retenciones ($35.8M RN overstatement)
- **`governance/GO_LIVE_AUDIT.md`**: Go-Live Audit FASE D+E — Impact assessment (7 questions) + 5 verdicts (FINAL: FAIL)
- **`knowledge/core/CONCEPT_REGISTRY_V2.md`**: FASE 4 — 96 concepts across 5 MPs, canonical mapping
- **`knowledge/core/EVENT_REGISTRY_V2.md`**: FASE 4 — Universal event roles, 7 causality rules
- **`knowledge/core/CASH_ROLE_REGISTRY_V1.md`**: FASE 4 — Cash equivalence, 54 UNASSIGNED (non-ML)

## Next Steps
1. **Address Go-Live Audit FAIL**: 3 structural issues block go-live — RN inflation (paired mechanisms), data freshness (Junio 2026), ML audit trail (0 rows)
2. **G5.8 — Revenue Concentration Risk**: Analyze dependency on top sellers/categories/concepts. Quantify diversification risk per MP.
3. **G5.9 — Forecast Model**: Build baseline revenue projection for 2026-2027 using take rate stability, stress scenarios, and adjustment trends.
