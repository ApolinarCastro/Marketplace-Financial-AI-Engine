# P36 — INTEGRATION MATRIX

**Fecha:** 2026-07-09
**Fase:** P36 — External Intelligence Integration
**Tipo:** Matriz consolidada de capacidades extraídas
**Modo:** SURGICAL — Extension First, no copy

---

## MATRIZ CONSOLIDADA — CAPACIDADES A INCORPORAR

| ID | Proyecto Origen | Capacidad | Beneficio | Complejidad | Prioridad | Componente Destino | RFC Requerido |
|---|---|---|---|---|---|---|---|
| **C-01** | QWED-Finance | Deterministic verification middleware (SymPy + Z3 philosophy) | Reforzar Governance con verificación matemática simbólica en vez de heurísticas | ALTA | **ALTA** | `engine/v4/governance/` (nuevo) | **SÍ** — RFC_DETERMINISTIC_VERIFICATION |
| **C-02** | QWED-Finance | QueryGuard pattern (SQLGlot AST-based SQL analysis) | Prevenir mutations/PII access en endpoints dinámicos | MEDIA | **ALTA** | `engine/v4/security/sql_guard.py` (nuevo) | **SÍ** — RFC_SQL_GUARD |
| **C-03** | QWED-Finance | GitHub Action for CI/CD financial verification | Automatizar `test_certification_gate.py` en cada PR | BAJA | **ALTA** | `.github/workflows/financial-truth-verify.yml` (nuevo) | NO — aplica patrón existente |
| **C-04** | QWED-Finance | Verification Receipts (cryptographic, reproducible) | Cada certificación genera receipt inmutable auditable | MEDIA | **MEDIA** | `engine/v4/certification/receipts.py` (extender) | **SÍ** — RFC_VERIFICATION_RECEIPTS |
| **C-05** | QWED-Finance | Fail-closed enforcement pattern (Decimal, no heuristic) | Migrar posibles floats a Decimal en cálculos sensibles | BAJA | **MEDIA** | `engine/v4/domain/financial_engine.py` (extender con Decimal) ⚠️ LIMITADO | **SÍ** — RFC_DECIMAL_MIGRATION |
| **C-06** | AgentFactory | IDFA Pattern: 4 guardrails + 3 layers + 2 skills for audit-proof financial models | Refactor CertificationEngine con guardrails explícitos | ALTA | **ALTA** | `engine/v4/certification/certification_engine.py` (extender) | **SÍ** — RFC_IDFA_CERTIFICATION |
| **C-07** | AgentFactory | Plugin Architecture Pattern (skills/commands/hooks/evals) | Re-estructurar Skills Registry como plugins autocontenidos | MEDIA | **MEDIA** | `engine/v4/skills/` (refactor) | **SÍ** — RFC_PLUGIN_REGISTRY |
| **C-08** | AgentFactory | Eval Harness with golden-file tests | Validar outputs de engines son inmutables entre releases | MEDIA | **ALTA** | `tests/golden/` (nuevo) | NO — extender pytest existente |
| **C-09** | AgentFactory | Jurisdiction overlays (13 overlays en islamic-finance) | Applique multi-region/marketplace overlays (PARIS RIPLEY ML FALABELLA) | MEDIA | **MEDIA** | `knowledge/taxonomy/overlays/` (nuevo) | **SÍ** — RFC_MARKETPLACE_OVERLAYS |
| **C-10** | AgentFactory | Workflow recipes as zip download | Empaquetar playbooks operacionales para distribución | BAJA | **BAJA** | `knowledge/recipes/` (nuevo) | NO |
| **C-11** | OpenClaw Personas | 10-file Persona Architecture (SOUL+AGENTS+SKILL+IDENTITY+HEARTBEAT+STYLE+BOOTSTRAP+USER+TOOLS+MEMORY) | Estructurar agentes especializados para nuestro dominio | ALTA | **MEDIA** | `engine/v4/agents/personas/` (nuevo) | **SÍ** — RFC_PERSONA_ARCHITECTURE |
| **C-12** | OpenClaw Personas | Financial Forecaster persona framework (best/base/worst-case) | Baseline para G5.9 Forecast Model (Next Steps) | MEDIA | **MEDIA** | `knowledge/personas/financial_forecaster.md` (nuevo) | NO |
| **C-13** | OpenClaw Personas | Fraud Detector pattern (risk scoring, velocity spikes, geo impossibilities) | Aplicable a detectar anomalies en ledger | MEDIA | **MEDIA** | `engine/v4/intelligence/financial_anomalies.py` (extender) | NO — extensión natural |
| **C-14** | OpenClaw Personas | HEARTBEAT.md — periodic self-checks | Health programado de engines (cerrar gaps de audit) | BAJA | **MEDIA** | `engine/v4/observability/heartbeat.py` (nuevo) | NO |
| **C-15** | OpenClaw Personas | MEMORY.md pattern (curated long-term memory) | Ya cubierto por KCE retention_manager | BAJA | **BAJA** | — | NO — redundante con KCE existente |
| **C-16** | Ponytail benchmarks | Reproducible benchmark methodology (3 arms × N tasks × 10 runs × mediana) | Medir performance regression en engines | MEDIA | **MEDIA** | `benchmarks/` (nuevo) | **SÍ** — RFC_BENCHMARK_METHODOLOGY |
| **C-17** | Ponytail benchmarks | Cost + Latency + LOC + Correctness metric definitions | Cuantificar efficiency del pipeline | BAJA | **MEDIA** | `benchmarks/metrics.py` (nuevo) | NO |
| **C-18** | Ponytail benchmarks | Independent benchmark corroboration protocol | Auditores externos validen performance | BAJA | **BAJA** | `governance/BENCHMARK_PROTOCOL.md` (nuevo) | NO |
| **C-19** | Ponytail benchmarks | Honesty notes pattern (transparency about limitations) | Cultural: documentar limitaciones en cada cert | BAJA | **BAJA** | Aplicar a futuras certifications | NO — cultural |
| **C-20** | Escalafy | LLM-readable knowledge layer pattern (JSONs versionados para LLM ingestion) | Exponer knowledge a LLMs externos sin API calls | MEDIA | **BAJA** | `knowledge/llm-readable/*.json` (nuevo) | NO |
| **C-21** | CEcommerce | Gamification pattern (XP/misiones/streaks) para auditor workflow | Incentivar uso del dashboard | ALTA | **BAJA** | — | NO — scope creep |
| **C-22** | CEcommerce | Estado labels (Testeo/Escalado/Estable) | Aplicable a fases del proyecto | BAJA | **BAJA** | Cultural, no arquitectural | NO |

---

## MATRIZ CONSOLIDADA — CAPACIDADES A DESCARTAR

| ID | Proyecto Origen | Capacidad | Razón de Descarte |
|---|---|---|---|
| **D-01** | Escalafy | Contenido comercial (overview/features/pricing/competitors) | Marketing de terceros, no nuestro producto |
| **D-02** | Escalafy | Dependencia Tiendanube/Shopify | Out of scope (dominio es ML/PARIS/RIPLEY/FALABELLA) |
| **D-03** | CEcommerce | Next.js/React/TailwindCSS stack | Stack incompatible (FastAPI + HTML nativo) |
| **D-04** | CEcommerce | LocalStorage persistence | DuckDB es fuente oficial |
| **D-05** | CEcommerce | COD ROAS/CPA formulas | No auditadas, violarían Single Financial Truth |
| **D-06** | CEcommerce | Sistema de misiones completo | Scope creep |
| **D-07** | OpenClaw | Personas marketing/creative/gaming | Out of scope |
| **D-08** | OpenClaw | OpenClaw platform runtime | Platform-specific |
| **D-09** | OpenClaw | Personas con dependencias externas (Notion/Jira/Slack) | No integramos terceros |
| **D-10** | OpenClaw | Códigos de cálculo financiero de personas | No auditados, violarían SFT |
| **D-11** | AgentFactory | Claude Code / Cowork / OpenClaw runtime | Nuestro runtime es custom |
| **D-12** | AgentFactory | islamic-finance skills específicas | Diferente dominio |
| **D-13** | AgentFactory | banking regulatory (IFRS 9, Basel III) | Diferente dominio |
| **D-14** | AgentFactory | Hooks que inyectan system prompts | Violaría Evidence First |
| **D-15** | AgentFactory | `.claude-plugin/manifest.json` format | Claude-specific |
| **D-16** | QWED-Finance | SymPy, mpmath, Z3, SQLGlot como dependencias directas | Añaden peso, evaluar antes |
| **D-17** | QWED-Finance | Banking guards (compliance/derivatives/ISO 20022/bond/FX/risk) | Fuera de scope |
| **D-18** | QWED-Finance | `qwed-finance` package | No tercer party dependency |
| **D-19** | QWED-Finance | Cálculos financieros propios de QWED | Nuestros ya certificados |
| **D-20** | QWED-Finance | "Verified by QWED" badge | No relación con ellos |
| **D-21** | Ponytail | Ponytail skill itself | No nuestro dominio |
| **D-22** | Ponytail | promptfoo dependency | Stack Python |
| **D-23** | Ponytail | Node.js ≥ 22.22 constraint | Stack Python |
| **D-24** | Ponytail | Código específico (behavior.js, loc.js, correctness.js) | Implementación específica |
| **D-25** | Ponytail | Claude Code session benchmark | No usamos Claude Code en prod |

---

## MATRIZ DE PRIORIZACIÓN POR COMPONENTE DESTINO

### `engine/v4/governance/` (nuevo — 1 capacidad ALTA)
- **C-01** Deterministic verification middleware — RFC_DETERMINISTIC_VERIFICATION

### `engine/v4/security/` (nuevo — 1 capacidad ALTA)
- **C-02** QueryGuard pattern — RFC_SQL_GUARD

### `.github/workflows/` (nuevo — 1 capacidad ALTA)
- **C-03** GitHub Action for financial-truth-verify

### `engine/v4/certification/` (extender — 2 capacidades)
- **C-04** Verification Receipts (MEDIA) — RFC_VERIFICATION_RECEIPTS
- **C-06** IDFA Pattern (ALTA) — RFC_IDFA_CERTIFICATION

### `engine/v4/domain/financial_engine.py` (extender con cuidado — 1 capacidad MEDIA)
- **C-05** Decimal migration ⚠️ LIMITADO — RFC_DECIMAL_MIGRATION (solo lectura-safe, no RN)

### `engine/v4/skills/` (refactor — 1 capacidad MEDIA)
- **C-07** Plugin Architecture Pattern — RFC_PLUGIN_REGISTRY

### `tests/golden/` (nuevo — 1 capacidad ALTA)
- **C-08** Eval Harness with golden-file tests

### `knowledge/taxonomy/overlays/` (nuevo — 1 capacidad MEDIA)
- **C-09** Jurisdiction overlays per marketplace — RFC_MARKETPLACE_OVERLAYS

### `knowledge/recipes/` (nuevo — 1 capacidad BAJA)
- **C-10** Workflow recipes as zip download

### `engine/v4/agents/personas/` (nuevo — 1 capacidad MEDIA)
- **C-11** 10-file Persona Architecture — RFC_PERSONA_ARCHITECTURE

### `knowledge/personas/` (nuevo — 1 capacidad MEDIA)
- **C-12** Financial Forecaster persona framework

### `engine/v4/intelligence/financial_anomalies.py` (extender — 1 capacidad MEDIA)
- **C-13** Fraud Detector pattern

### `engine/v4/observability/heatmap.py` (nuevo — 1 capacidad MEDIA)
- **C-14** HEARTBEAT.md periodic self-checks

### `benchmarks/` (nuevo — 1 capacidad MEDIA)
- **C-16** Reproducible benchmark methodology — RFC_BENCHMARK_METHODOLOGY

### `benchmarks/metrics.py` (nuevo — 1 capacidad MEDIA)
- **C-17** Metric definitions (LOC/cost/latency/correctness)

### `knowledge/l1m-readable/` (nuevo — 1 capacidad BAJA)
- **C-20** LLM-readable knowledge layer pattern

---

## RFCs REQUERIDOS (8)

| RFC | Origen | Estado |
|---|---|---|
| RFC_DETERMINISTIC_VERIFICATION | C-01 (QWED) | Pendiente |
| RFC_SQL_GUARD | C-02 (QWED) | Pendiente |
| RFC_VERIFICATION_RECEIPTS | C-04 (QWED) | Pendiente |
| RFC_DECIMAL_MIGRATION | C-05 (QWED) | Pendiente ⚠️ |
| RFC_IDFA_CERTIFICATION | C-06 (AgentFactory) | Pendiente |
| RFC_PLUGIN_REGISTRY | C-07 (AgentFactory) | Pendiente |
| RFC_MARKETPLACE_OVERLAYS | C-09 (AgentFactory) | Pendiente |
| RFC_PERSONA_ARCHITECTURE | C-11 (OpenClaw) | Pendiente |
| RFC_BENCHMARK_METHODOLOGY | C-16 (Ponytail) | Pendiente |

---

## TIERING DE IMPLEMENTACIÓN

### TIER 1 — ALTA PRIORIDAD (implementar primero)
- **C-01** Deterministic verification middleware (QWED)
- **C-02** QueryGuard SQL safety (QWED)
- **C-03** GitHub Action for CI/CD (QWED)
- **C-06** IDFA Pattern certification (AgentFactory)
- **C-08** Eval Harness with golden-file tests (AgentFactory)

### TIER 2 — MEDIA PRIORIDAD (después)
- **C-04** Verification Receipts (QWED)
- **C-05** Decimal migration ⚠️ LIMITADO (QWED)
- **C-07** Plugin Architecture (AgentFactory)
- **C-09** Jurisdiction overlays (AgentFactory)
- **C-11** 10-file Persona Architecture (OpenClaw)
- **C-12** Financial Forecaster framework (OpenClaw)
- **C-13** Fraud Detector pattern (OpenClaw)
- **C-14** HEARTBEAT.md pattern (OpenClaw)
- **C-16** Benchmark methodology (Ponytail)
- **C-17** Metric definitions (Ponytail)

### TIER 3 — BAJA PRIORIDAD (opcional, futuro)
- **C-10** Workflow recipes as zip (AgentFactory)
- **C-15** MEMORY.md pattern (OpenClaw — redundante con KCE)
- **C-18** Independent benchmark protocol (Ponytail)
- **C-19** Honesty notes pattern (Ponytail — cultural)
- **C-20** LLM-readable knowledge layer (Escalafy)
- **C-22** Estado labels (CEcommerce — cultural)

### DESCARTAR
- D-01 through D-25 (ver tabla anterior)

---

## VALIDACIÓN DE NO-REGRESIÓN

| Verificación | Cumplimiento |
|---|---|
| No se modifica `marketplace_ledger_v1` | ✅ — Ninguna capacidad toca el ledger |
| No se modifica `cierre_financiero_v1` | ✅ — Ninguna capacidad toca cierres |
| No se modifica `include_in_operational_pnl` | ✅ — DEC-019 preservado |
| No se introducen heurísticas en RN | ✅ — Deterministic First refuerza lo contrario |
| No se reemplaza FinancialEngine | ✅ — Decimal migration C-05 es ⚠️ LIMITADO (solo lectura-safe) |
| No se introducen dependencias críticas sin justificación | ✅ — SymPy/Z3/SQLGlot requieren RFC |
| No se copia código | ✅ — Solo arquitectura y patrones |
| No se generan nuevas funcionalidades de finanzas | ✅ — Todas en capa outer |
| Single Financial Truth preservada | ✅ — Ningún proyecto reemplaza la DB oficial |
| Evidence First reforzado | ✅ — QWED + Ponytail honesty notes refuerzan |

---

**Matriz completa.** Ver `FINAL_VERDICT.md` para 10 questions finales.
