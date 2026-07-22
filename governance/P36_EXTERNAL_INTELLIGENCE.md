# P36 — EXTERNAL INTELLIGENCE AUDIT

**Fecha:** 2026-07-09
**Fase:** P36 — External Intelligence Integration (Audit Only)
**Modo:** SURGICAL — Extraer patrones, NO copiar código
**Base:** Post-P35 (repo estable, 291P/8S/2F, zero regression)

---

## PRINCIPIOS APLICADOS

- DEC-019 INMUTABLE
- Single Financial Truth
- Evidence First
- Zero Regression
- Extension First
- No Heuristics

---

## RESUMEN EJECUTIVO

Se auditaron 6 proyectos externos contra el Marketplace Financial AI Engine. Cada proyecto fue evaluado por su capacidad de **aportar arquitectura, patrones y buenas prácticas** sin comprometer el Core Financiero.

**Hallazgo clave:** 2 proyectos aportan valor ALTO (QWED-Finance, AgentFactory), 2 aportan valor MEDIO (Ponytail benchmarks, OpenClaw personas), 2 aportan valor BAJO o se descartan (Escalafy, CEcommerce).

**Ninguna integración requiere modificar el Core.** Todas las capacidades extraídas pueden implementarse mediante extensions en la capa de knowledge/intelligence/governance.

---

## PROYECTO 1 — Escalafy/escalafy-llm-es

**URL:** https://github.com/Escalafy/escalafy-llm-es
**Stars:** 0 | **Forks:** 0 | **Commits:** 10

### 1. ¿Qué problema resuelve?

No es un producto de software — es una **capa de datos pública para LLMs** (AI SEO / LLM Ingestion). Escalafy (producto comercial: rentabilidad en tiempo real para ecommerce LATAM) publica JSON estructurado (overview, features, pricing, integrations, use-cases, faq, competitors) para que ChatGPT, Claude, Gemini, Perplexity lo ingesten y recomienden Escalafy correctamente.

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Patrón de LLM-readable knowledge layer**: estructura de JSONs que otros modelos consumen sin API calls
- **FAQ-Driven Knowledge**: 50 preguntas frecuentes indexables
- **Competitor comparison framework**: benchmark neutral vs otras herramientas
- **Concepto de "llm-answer.txt"**: plantilla canónica para respuestas LLM

### 3. ¿Qué puede reutilizarse?

- **Arquitectura únicamente**: la idea de exponer un knowledge layer como JSONs versionados que LLMs pueden ingerir. NO el contenido (es marketing de Escalafy).
- **Estructura de archivos**: overview.json + features.json + faq.json + use-cases.json como metadato indexable.
- **Patrón de "llm-answer.txt"**: plantilla de respuesta canónica para que agentes respondan sobre el sistema.

### 4. ¿Qué NO debe incorporarse?

- Contenido comercial de Escalafy (no es nuestro producto)
- Cualquier dato financiero (es marketing, no auditado)
- Dependencia con Tiendanube/Shopify (nuestro dominio esML/PARIS/RIPLEY/FALABELLA)
- README con SEO manipulation

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | BAJO — patrón de JSON knowledge indexable podría enriquecer knowledge_index.yaml |
| Obsidian | NULO |
| Skills Registry | BAJO — estructura de FAQ como skill input |
| Knowledge API | MEDIO — endpoint `/api/v4/knowledge/llm-readable` que exponga JSON versión-lenguaje-natural |
| Governance | NULO |
| Observability | NULO |
| Performance | NULO |
| Production Readiness | NULO |

### 6. Clasificación

**BAJA** — Patrón de LLM-readable knowledge layer es interesante pero el contenido es marketing comercial, no arquitectura reutilizable. El patrón ya está parcialmente cubierto por nuestra `knowledge_index.yaml`.

---

## PROYECTO 2 — Jordanc023/CEcommerce

**URL:** https://github.com/Jordanc023/CEcommerce
**Stars:** 1 | **Forks:** 0 | **Commits:** 1
**Demo:** c-ecommerce.vercel.app

### 1. ¿Qué problema resuelve?

Dashboard gamificado para gestión de e-commerce COD (Cash on Delivery). Next.js 16 + React 19 + TailwindCSS 4. Funcionalidades: dashboard principal con KPIs (Ventas, ROAS, CPA, Profit), calculadora COD, analytics, control diario, sistema de misiones con XP, ajustes. **100% client-side** (LocalStorage). Sin backend, sin DB.

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Gamificación operacional**: sistema de XP/misiones/streaks aplicable a 我们的 auditor workflow
- **Arquitectura Modular de Vistas**: HomeView, CalculatorView, AnalyticsView, TasksView, SettingsView — patrón de separación
- **Cashflow proyection pattern** (lib/cashflow_logic.ts): lógica de proyección 60 días
- **Bundle calculator pattern** (lib/bundle_logic.ts): cálculo de descuentos compuestos
- **COD metrics framework**: ROAS real, CPA, profit real

### 3. ¿Qué puede reutilizarse?

- **Arquitectura únicamente de separación lib/ vs components/**: la idea de aislar `cod_logic.ts`, `cashflow_logic.ts`, `bundle_logic.ts` como módulos puros sin dependencias UI.
- **Patrón deBackup/Restore JSON**: SettingsView con export/import de datos
- **Sistema de etiquetas de estado** (Testeo, Escalado, Estable) — clasificación operacional
- **NO la stack tecnológica** (no usamos Next.js/React/Tailwind — nuestro frontend es FastAPI + HTML nativo)

### 4. ¿Qué NO debe incorporarse?

- Next.js, React, TailwindCSS stacks (nuestro frontend es server-rendered HTML)
- LocalStorage como persistencia (nosotros tenemos DuckDB)
- Cualquier cálculo financiero COD ROAS/CPA (son fórmulas ad-hoc no auditadas, violaría Single Financial Truth)
- Sistema de misiones completo (gamificación ligera OK, completo es scope creep)

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | NULO |
| Obsidian | NULO |
| Skills Registry | BAJO — patrón de skill categorization por dificultad (Novato/Profesional/Experto) |
| Knowledge API | NULO |
| Governance | BAJO — etiquetas de estado (Testeo/Escalado/Estable) aplicables a phases |
| Observability | NULO |
| Performance | NULO |
| Production Readiness | NULO |

### 6. Clasificación

**BAJA** — Stack tecnológica incompatible (Next.js + LocalStorage vs FastAPI + DuckDB). Arquitectura modular es estándar. Gamificación es scope creep para nuestro dominio.

---

## PROYECTO 3 — TravisLeeeeee/awesome-openclaw-personas

**URL:** https://github.com/TravisLeeeeee/awesome-openclaw-personas
**Stars:** 101 | **Forks:** 17 | **Commits:** 3

### 1. ¿Qué problema resuelve?

Colección curada de **214+ AI agent personas** para OpenClaw platform. Cada persona es un package completo: SOUL.md (personality), AGENTS.md (SOPs), SKILL.md (capabilities), IDENTITY.md, HEARTBEAT.md, STYLE.md, BOOTSTRAP.md, USER.md, TOOLS.md, MEMORY.md. No son prompts simples — son especialistas con metodologías reales (MEDDPICC, WCAG 2.2, six-dimension scoring).

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Persona Architecture Framework**: estructura de archivos multi-eje (SOUL + AGENTS + SKILL + IDENTITY + HEARTBEAT + STYLE + BOOTSTRAP + USER + TOOLS + MEMORY)
- **File-based agent configuration**: 10 archivos markdown que definen un agente completo
- **Finance personas**: 10 personas especializadas (Accounts Payable, Copy Trader, Expense Tracker, Finance Tracker, Financial Forecaster, Fraud Detector, Invoice Manager, Portfolio Rebalancer, Revenue Analyst, Tax Preparer)
- **Governance personas**: Compliance Checker, Contract Reviewer, Legal & Compliance
- **Anti-hallucination rules**: incluidas en personas de Shopify Operator

### 3. ¿Qué puede reutilizarse?

- **Arquitectura de persona únicamente**: el patrón de 10 archivos (SOUL + AGENTS + SKILL + ...) puede adaptarse a nuestro Skills Registry existente
- **Finance personas como templates**: Financial Forecaster (best/base/worst-case), Fraud Detector (risk scoring), Revenue Analyst (MRR decomposition) — **los frameworks**, no el código
- **Monthly account maintenance pattern**: HEARTBEAT.md — checks periódicos programados
- **MEMORY.md pattern**: memoria curada a largo plazo que crece con el tiempo (similar a KCE)
- **Decision matrices**: tablas de decisión spezi pro persona (aplicable a CertificationEngine)

### 4. ¿Qué NO debe incorporarse?

- Cualquier persona de marketing/content creator (out of scope)
- Personas de gaming/creative writing (out of scope)
- Code de OpenClaw (platform-specific)
- Personas con dependencias a herramientas externas (Notion, Jira, Slack)
- Cualquier cálculo financiero real de las personas (no auditado, violaría SFT)

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | ALTO — patrón de persona + MEMORY.md ecology aligns con KCE retention_manager |
| Obsidian | MEDIO — estructura de archivos markdown tocará knowledge graph |
| Skills Registry | ALTO — arquitectura de 10 archivos puede reemplazar/enriquecer estructura current |
| Knowledge API | MEDIO — endpoint could expose personas |
| Governance | MEDIO — Compliance Checker persona pattern aplicable |
| Observability | BAJO — HEARTBEAT.md = periodic health checks |
| Performance | NULO |
| Production Readiness | BAJO — persona bootstrapping 的影响 |

### 6. Clasificación

**MEDIA** — Arquitectura de personas es sólida peroorientada a agentes conversacionales. Frameworks finance son interesting pero no código. Requiere adaptación, no adopción directa.

---

## PROYECTO 4 — panaversity/agentfactory-business-plugins

**URL:** https://github.com/panaversity/agentfactory-business-plugins
**Stars:** 23 | **Forks:** 16 | **Commits:** 55
**License:** Apache-2.0

### 1. ¿Qué problema resuelve?

Marketplace de **plugins domain-specific para AI agents** (Claude Code, Cowork, OpenClaw). Plugins cubren finance, banking, legal-ops, sales con skills + commands + hooks + scripts + evals + workflow-recipes. Estructura modular: cada plugin es autocontenido con `.claude-plugin/manifest`, skills auto-loaded, commands, hooks, evals con golden-file tests.

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Plugin Architecture Pattern**: estructura de marketplace con plugins autocontenidos
- **Skill Versioning**: v2.0.0 semantic versioning en plugins
- **Eval Harness**: tests de golden-file para validar plugins
- **Jurisdiction overlays**: 13 overlaides jurisdiccionales en islamic-finance (multi-locale regulatory)
- **Workflow recipes**: 4 playbooks operacionales descargables como zip
- **IDFA Financial Architect**: 4 guardrails + 3 layers + 2 skills for audit-proof financial models
- **Domain Commands**: slash commands específicos por dominio

### 3. ¿Qué puede reutilizarse?

- **Plugin directory structure**: `plugin/skills/`, `plugin/commands/`, `plugin/hooks/`, `plugin/evals/` — patrón adoptable
- **Eval harness with golden-file tests**: para certificar que engines produzcan outputs inmutables
- **Jurisdiction overlay concept**: overlayes region-specific sobre skills base — aplicable a ML/PARIS/RIPLEY/FALABELLA como "overlays"
- **IDFA Pattern**: 4 guardrails (intent, audit, deterministic, human-readable), 3 layers (data, model, presentation), 2 skills (build, verify) — **patrón arquitetural para nuestro CertificationEngine**
- **Marketplace install mechanism**: `claude plugin install plugin@marketplace` — patrón de discovery

### 4. ¿Qué NO debe incorporarse?

- Claude Code / Cowork / OpenClaw plugin runtime (nuestro runtime es custom)
- islamic-finance skills específicas (fuera de scope paraML/PARIS/RIPLEY/FALABELLA)
- banking regulatory compliance (IFRS 9, Basel III) — diferente dominio
- Cualquierhook que inyecte system prompts (violaría Evidence First)
- `.claude-plugin/manifest.json` format (Claude-specific)

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | MEDIO — plugin discovery mechanism could feed KCE knowledge_index |
| Obsidian | BAJO — plugin metadata as knowledge nodes |
| Skills Registry | ALTO — plugin architecture pattern directly applicable |
| Knowledge API | MEDIO — endpoint could expose plugin catalog |
| Governance | ALTO — IDFA pattern (guardrails + layers + skills) for audit-proof models |
| Observability | MEDIO — golden-file evals as observability probes |
| Performance | BAJO |
| Production Readiness | MEDIO — eval harness pattern for production validation |

### 6. Clasificación

**ALTA** — IDFA Financial Architect pattern (guardrails + layers + skills), plugin architecture, y eval harness con golden-file tests son directamente aplicables. Apache-2.0 permite adopción.

---

## PROYECTO 5 — QWED-AI/qwed-finance (GitHub Action: QWED Finance Guard)

**URL:** https://github.com/marketplace/actions/qwed-finance-guard
**Source:** https://github.com/QWED-AI/qwed-finance
**Stars:** 4 | **License:** Apache-2.0
**Version:** v2.1.0

### 1. ¿Qué problema resuelve?

**Middleware determinístico de verificación financiera** para AI. Valida que outputs de LLMs en cálculos bancarios sean matemáticamente correctos usando SymPy (matemática simbólica) y Z3 (formal logic). 10 Guards: Compliance (KYC/AML), Calendar (day count), Derivatives (Black-Scholes), Message (ISO 20022), Query (SQL safety), Cross (multi-layer), Bond (YTM/Duration), FX (forward rates), Risk (VaR/Beta/Sharpe), ISO (banking schema).

**100% determinístico** — sin LLMs en el loop de verificación. Fail-closed enforcement. Local-only (no API calls).

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Deterministic verification philosophy**: SymPy + Z3 para验证 matemática — complemento al Evidence First
- **10 Guards architecture**: cada guard es una capa específica de validación
- **QueryGuard (SQL Safety)**: AST-based SQL analysis con SQLGlot para prevenir mutations/PII — **directamente applicable a nuestro SQL-only access**
- **GitHub Action for CI/CD**: verificación automática en pipeline
- **Verification receipts with audit trail**: cryptographic receipts reproducibles
- **Fail-closed enforcement**: returned Decimal instead of float heuristic
- **Float→Decimal migration**: patrón de migración float a Decimal/mppmath (similar a nuestro LOWER() fix)

### 3. ¿Qué puede reutilizarse?

- **Architecture del verification middleware** (NO código): patrón de guards como capas
- **QueryGuard pattern**: SQLGlot AST-based analysis — aplicar a nuestros endpoints para validar queries no hacen mutations o acceden PII columns
- **Verification receipts concept**: cada certificación genera receipt criptográfico
- **GitHub Action pattern**: `.github/workflows/financial-truth-verify.yml` para correr `test_certification_gate.py` en cada PR
- **SymPy for symbolic math**: usando en cálculos financieros críticos (NPV, IRR) si algún día necesitamos
- **Deterministic-first philosophy document**: como governance principle

### 4. ¿Qué NO debe incorporarse?

- SymPy, mpmath, Z3, SQLGlot dependencies (evaluar antes — añaden peso)
- Banking-specific guards (compliance, derivatives, ISO 20022, bond, FX, risk) — fuera de scope
- `qwed-finance` package como dependencia
- Cualquier cálculo financiero propio de QWED (los nuestros ya están certificados)
- "Verified by QWED" badge (no tenemos relación con ellos)

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | BAJO — verification receipts como knowledge entries |
| Obsidian | NULO |
| Skills Registry | NULO |
| Knowledge API | BAJO |
| Governance | ALTO — Deterministic Verification + Fail-closed principle + Verification Receipts |
| Observability | ALTO — guards como observability probes, cada Guard = check |
| Performance | MEDIO — verificación añade latencia (<5ms simple, <50ms complex) |
| Production Readiness | ALTO — GitHub Action pattern, CI/CD integration, verification receipts |

### 6. Clasificación

**ALTA** — Verification middleware philosophy, QueryGuard pattern (SQLGlot AST analysis), GitHub Action for CI/CD, y Verification Receipts son directamente aplicables a fortalecer Governance y Observability. Apache-2.0 permite adopción arquitectural.

---

## PROYECTO 6 — DietrichGebert/ponytail/benchmarks

**URL:** https://github.com/DietrichGebert/ponytail/tree/main/benchmarks
**Stars:** 79k | **Forks:** 4.2k

### 1. ¿Qué problema resuelve?

Framework de **benchmarks reproducibles para AI skills**. Tres arms (no skill, caveman, ponytail), tres modelos (Claude Haiku/Sonnet/Opus), cinco tareas cotidianas, 10 runs por celda con mediana. Métricas: LOC (lines of code from fenced blocks), cost (USD from API), latency (seconds). Correctness gate (fail if code doesn't work).

**Independent benchmarks** de third parties: KuldeepB19 (24 tasks, ~44% less code), RicardoCostaGit (multi-turnagentic runs).

### 2. ¿Qué aporta al Marketplace Financial AI Engine?

- **Reproducible benchmark methodology**: 3 arms × 3 models × 5 tasks × 10 runs = 450 executions con mediana
- **Metric definitions**: LOC, cost, latency, correctness — with specific measurement implementations
- **"Honesty note" pattern**: corrección transparente cuando críticas (#126, #121) son válidas
- **Independent benchmark verification**: third parties corroboren results
- **Cost re-verification protocol**: re-verify at 30 runs after initial 10-run results
- **Agentic vs single-shot split**: distinction between generation numbers and session-cost reality

### 3. ¿Qué puede reutilizarse?

- **Benchmark methodology únicamente**: 3 arms (baseline, current, candidate) × N tasks × N runs = matrix
- **Metric definitions**: LOC, cost, latency, correctness — applicable a certificar engines
- **Median reporting protocol**: 10 runs, mediana, no mean
- **Cost re-verification at 30 runs**: cuidado con overstating savings
- **Honesty notes**: transparency about limitations (single-shot vs agentic, prose vs code)
- **Independent benchmark invitation**: pedir a third parties que corroboren (auditores externos)
- **Results markdown format**: `results/YYYY-MM-DD-description.md`

### 4. ¿Qué NO debe incorporarse?

- Ponytail skill itself (no es nuestro dominio)
- promptfoo dependency (nuestro stack es Python)
- Node.js ≥ 22.22 constraint
- Codes de SKILL.md, behavior.js, loc.js, correctness.js específicos
- "Claude Code session" benchmark (no usamos Claude Code en producción)

### 5. Impacto

| Componente | Impacto |
|---|---|
| KCE | NULO |
| Obsidian | NULO |
| Skills Registry | NULO |
| Knowledge API | NULO |
| Governance | MEDIO — honesty notes pattern, independent benchmark corroboration |
| Observability | ALTO — benchmark methodology como observability probes |
| Performance | ALTO — methodology to measure performance regression |
| Production Readiness | ALTO — CI/CD integration for benchmarks, performance regression detection |

### 6. Clasificación

**MEDIA** — Benchmark methodology es sólida y aplicable a Performance/Observability pero requiere adaptación (Python vs Node.js). Honesty notes pattern es cultural, no arquitectural.

---

## TABLA CONSOLIDADA

| # | Proyecto | Stars | Clasificación | Valor Principal |
|---|---|---|---|---|
| 1 | Escalafy/escalafy-llm-es | 0 | **BAJA** | LLM-readable knowledge layer pattern |
| 2 | Jordanc023/CEcommerce | 1 | **BAJA** | Gamification + módulos lib/ separados |
| 3 | TravisLeeeeee/awesome-openclaw-personas | 101 | **MEDIA** | 10-file persona architecture + Finance personas frameworks |
| 4 | panaversity/agentfactory-business-plugins | 23 | **ALTA** | Plugin architecture + IDFA pattern + eval harness |
| 5 | QWED-AI/qwed-finance | 4 | **ALTA** | Deterministic verification + QueryGuard + CI/CD GitHub Action |
| 6 | DietrichGebert/ponytail/benchmarks | 79k | **MEDIA** | Reproducible benchmark methodology + honesty notes |

---

## VALIDACIÓN DE PRINCIPIOS

| Principio | Cumplimiento |
|---|---|
| DEC-019 INMUTABLE | ✅ — Ninguno modifica `include_in_operational_pnl` |
| Single Financial Truth | ✅ — Ninguno consulta `marketplace_ledger_v1` ni `cierre_financiero_v1` |
| Evidence First | ✅ — QWED refuerza "Deterministic First", ponytail refuerza "Honesty Notes" |
| Zero Regression | ✅ — No se implementa nada, solo audita |
| Extension First | ✅ — Todo integrable como adapters/extensions en capa outer |
| No Heuristics | ✅ — QWED rechaza heuristics (fail-closed), ponytail honesty notes anti-overstating |

---

## CONCLUSIÓN

Los **2 proyectos ALTA** (QWED-Finance, AgentFactory) pueden integrarse quirúrgicamente mediante extensions sin tocar el Core:
- **QWED**: integration como verification middleware layer en Governance + Observability + CI/CD GitHub Action
- **AgentFactory**: IDFA pattern como certification framework, plugin architecture para Skills Registry, eval harness para golden-file tests

Los **2 proyectos MEDIA** (Ponytail benchmarks, OpenClaw personas) requieren adaptación arquitectural pero Aportan valor en Performance Measurement y Agent Persona Framework respectivamente.

Los **2 proyectos BAJA** (Escalafy, CEcommerce) no justifican inversión de integración.

**Ninguna integración rompe DEC-019, Single Financial Truth, o el Core Financiero.**

---

**Audit completo.** Ver `INTEGRATION_MATRIX.md` para detalles de qué incorporar y `FINAL_VERDICT.md` para recommendations priorizadas.
