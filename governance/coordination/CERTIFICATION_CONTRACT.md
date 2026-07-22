# MARKETPLACE FINANCIAL OPERATING SYSTEM
# CERTIFICATION CONTRACT

Version: 1.0

Status: ACTIVE

---

# PREAMBLE

This contract defines the official, auditable, and reproducible criteria for
certifying the Marketplace Financial Operating System.

It is derived from automated inventory of the repository at commit
`79ae47dfcfab349ae64d4096d4c501f0eb88da0d`, cross-referenced against the
main working repository (`f4-clean-code` at `d15e94e`) and the last certified
F4 execution evidence.

---

## 1. CERTIFIED COMMIT

| Field | Value |
|---|---|
| HEAD | `79ae47d5129133ee13ccb868cc70dd3c4535b288` |
| Branch | `release/clean-functional-flow` |
| Origin | `git worktree add` from main repo |
| Dependencies | `requirements.txt` (httpx, sqlglot, pytest-asyncio) verified |
| Worktree | CLEAN (no tracked modifications) |
| Main repo HEAD | `d15e94e` (`f4-clean-code`) |

### Commit Chain (relevant ancestry)

```
79ae47d fix(deps): declare reproducible test runtime dependencies
7b03538 fix: restore reproducible financial reconciliation and copilot flow
d15e94e fix(ingestion): restore content-addressed registry chain
c52755a fix(loader): separate ingestion from classification audit and closing
0375ead F4: preflight-only mode harness correction
a3e0804 F4: final verdict PHASE_4_GATE_SATISFIED
3a35826 F4: evidence 96/96 PASS (execution_id F4_20260719_183358)
992e10b F4: import closure for financial_engine.py
dd62377 F4: path fixes + F4_TEMP_ROOT + JUnit + protected hashes
3019b20 F4: test suites + harness (code-only)
64f030a F4 Suites: 4 suites, 96 tests, PHASE_4_GATE_SATISFIED
67e5e0e BASELINE_V6 — Initial commit
```

---

## 2. DEPENDENCIES

### Python Runtime (from requirements.txt)

| Package | Constraint | Purpose |
|---|---|---|
| Python | >=3.12 | Runtime |
| duckdb | >=1.5,<2 | DB engine |
| fastapi | >=0.115,<1 | API server |
| uvicorn | >=0.34,<1 | ASGI server |
| pandas | >=2,<3 | Data processing |
| openpyxl | >=3.1,<4 | Excel I/O |
| python-multipart | >=0.0.18,<1 | File uploads |
| httpx | >=0.27,<1 | HTTP client (tests) |
| sqlglot | >=25,<31 | SQL parsing (tests) |
| pytest | >=8,<9 | Test runner |
| pytest-asyncio | >=0.21,<2 | Async test support |
| anyio | >=4,<5 | Async runtime |

### System

| Tool | Purpose |
|---|---|
| Git | Version control, worktree |
| PowerShell 5.1 | Shell on Windows |

---

## 3. REQUIRED DATABASES

### 3.1 Official Database (Production Truth)

| Property | Value |
|---|---|
| Path | `data/db/meli_financial_v4.db` |
| SHA256 | `c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce` |
| Size | 53,305,856 bytes |
| Engine | DuckDB V1.5.1 |
| Role | Single Financial Truth — ledger, classification, closing |

### 3.2 V8 Baseline Database (F4 Certification)

| Property | Value |
|---|---|
| Path | `data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db` |
| SHA256 | `733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00` |
| Size | 53,305,856 bytes |
| Role | Required by F4 harness as temp DB copy for certification gate tests |

### 3.3 V9 Baseline Database (Truth Recovery)

| Property | Value |
|---|---|
| Path | `data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/meli_financial_v4.db` |
| SHA256 | `c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce` |
| Size | 53,305,856 bytes |
| Role | Required by `test_truth_005_registry.py` (ingestion registry traceability) |
| Note | Identical hash to official DB — V9 IS current truth |

---

## 4. MANDATORY HASHES

### 4.1 Databases

| Artifact | SHA256 |
|---|---|
| Official DB | `c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce` |
| V8 Baseline DB | `733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00` |
| V9 Baseline DB | `c76c3fee51c31949571f829da6043f1682023dc39f5b093f7af794654dbf6fce` |

### 4.2 Taxonomy Files (KnowledgeBase)

| Artifact | SHA256 |
|---|---|
| `KnowledgeBase/Marketplace/Taxonomy/ml_v1.json` | `ba9087b87a54ebc74898d319701741e3876600217080410ea9cf8dcc5a7898ac` |
| `KnowledgeBase/Marketplace/Taxonomy/paris_v1.json` | `21b7117646badf3324321ff30acbbe405d18cdd748c3e82b643476cbe1c81458` |
| `KnowledgeBase/Marketplace/Taxonomy/ripley_v1.json` | `220f8f314d1377a1e16dde6181de39a1f51c3b7c6a0c0690c2732f653be93cdc` |
| `KnowledgeBase/Marketplace/Taxonomy/falabella_v1.json` | `30942ba71f8f30c00a31edf953376304bdf721142b30452cd854b21cdfe5c80f` |

### 4.3 Taxonomy Engine (YAML)

| Artifact | SHA256 |
|---|---|
| `taxonomy/taxonomy_rules.yaml` | `ba856b6a05c61d5d2c976f0b3d2e239c61c2251ccdd61d2e3a54438d3ff452b6` |
| `taxonomy/taxonomy_mappings.yaml` | `f3e0090370c2048e67d9cd85282c631eb3b63d51e8ffc978dc71f21d36cba233` |
| `taxonomy/taxonomy_loader.py` | `f12d67a4f30078f56d431253e9f11c8d8a6f1cc158af8aaceaefa39ba2964b19` |

### 4.4 Templates

| Artifact | SHA256 |
|---|---|
| `templates/executive_dashboard.html` | `818d66cd6a79edf621b0028587e6d2199badacbb2496728cc08093f8b33da388` |
| `templates/copilot.html` | `cc6f956af7a4fa1295507992e1d9c4944b1c6a6cb2ce43c803548fea623a0f89` |
| `templates/upload_center.html` | `8abd13f04a5ca117c86e487971440868671693d177fe3cf2c01c0e7b664cbc2f` |
| `templates/documentary_dashboard.html` | `be713aa11edbf97b82a6633106d27c17354461a8a06f59ea7535565d0f2d5c92` |

### 4.5 Test Infrastructure

| Artifact | SHA256 |
|---|---|
| `tests/conftest.py` | `508f57c442e8078e1979d3f60ffb5c768d4d49c5e32239109a2f7e44db4522f0` |
| `tools/run_f4_suites.py` | `172a4462f5498f101aed6110f2705c5b1c8fca0cadf8bcd3e819ff1d46f86c31` |

### 4.6 Test Fixtures (F3 traceability)

| Artifact | SHA256 |
|---|---|
| `tests/fixtures/f3_03/f3_03_fixture.xlsx` | `9be8effcba44cce1810e775651f872b2b4891fb61850d0cf5a7aa6859fed7d9a` |

---

## 5. REQUIRED ARTIFACTS

### 5.1 Runtime (required for system operation)

| # | Artifact | Type | Location |
|---|---|---|---|
| R1 | Official DB | database | `data/db/meli_financial_v4.db` |
| R2 | Dashboard template | template | `templates/dashboard.html` |
| R3 | Executive template | template | `templates/executive_dashboard.html` |
| R4 | Copilot template | template | `templates/copilot.html` |
| R5 | Upload Center template | template | `templates/upload_center.html` |
| R6 | Documentary Dashboard | template | `templates/documentary_dashboard.html` |
| R7 | ML taxonomy | taxonomy | `KnowledgeBase/Marketplace/Taxonomy/ml_v1.json` |
| R8 | PARIS taxonomy | taxonomy | `KnowledgeBase/Marketplace/Taxonomy/paris_v1.json` |
| R9 | RIPLEY taxonomy | taxonomy | `KnowledgeBase/Marketplace/Taxonomy/ripley_v1.json` |
| R10 | FALABELLA taxonomy | taxonomy | `KnowledgeBase/Marketplace/Taxonomy/falabella_v1.json` |
| R11 | Taxonomy rules | config | `taxonomy/taxonomy_rules.yaml` |
| R12 | Taxonomy mappings | config | `taxonomy/taxonomy_mappings.yaml` |
| R13 | Taxonomy loader | code | `taxonomy/taxonomy_loader.py` |

**13 runtime artifacts required.**

### 5.2 Test (required for certification execution)

| # | Artifact | Type | Location |
|---|---|---|---|
| T1 | V8 Baseline DB | database | `data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db` |
| T2 | V9 Baseline DB | database | `data/db/BASELINE_ESTABLE_V9_TRUTH_RECOVERED/meli_financial_v4.db` |
| T3 | Test conftest | config | `tests/conftest.py` |
| T4 | F4 test harness | script | `tools/run_f4_suites.py` |
| T5 | F3 traceability fixture | fixture | `tests/fixtures/f3_03/f3_03_fixture.xlsx` |

**5 test artifacts required.**

### 5.3 Optional (no certification impact)

| # | Artifact | Reason |
|---|---|---|
| O1 | All `data/db/snapshot_*` directories | Historical backups |
| O2 | All `data/db/tmp_*` directories | Debug copies (identical to official DB) |
| O3 | `evidence/` directory | Output of certification runs (not input) |
| O4 | `governance/` directory | Documentation, not runtime |
| O5 | `00_Config/` directory | Configuration reference |
| O6 | `AESP/` directory | Agent registry |
| O7 | `docs/` directory | Documentation |

---

## 6. OFFICIAL CERTIFICATION SUITE

### 6.1 Definition

The official certification suite is **F4: 96 tests across 4 files**.

### 6.2 Evidence

- **F4_VERDICT.md**: `evidence/F4_VERDICT.md` — declares PHASE_4_GATE_SATISFIED
- **Last certified run**: Commit `3a35826`, execution_id `F4_20260719_183358`
- **Harness**: `tools/run_f4_suites.py` v1.0.0-r6
- **Result**: 96/96 PASS, 0 FAIL, 0 ERROR, 0 SKIP
- **DB integrity**: Official/V7/V8 intact (pre-run = post-run SHA256)
- **Mutation**: FALSE

### 6.3 Suite Composition

| # | File | Tests | Coverage | Duration (certified) |
|---|---|---|---|---|
| S1 | `tests/test_certification_gate.py` | 29 | Financial Truth, Waterfall, DTE, Taxonomy, Ledger | 1.19s |
| S2 | `tests/test_semantic_consistency.py` | 27 | Semantic layer, cross-MP consistency | 1.38s |
| S3 | `tests/test_f4_traceability.py` | 22 | RAW-to-Cierre traceability (22 transactions) | 239.12s |
| S4 | `tests/test_taxonomy_equivalence.py` | 18 | YAML vs legacy classification equivalence | 13.47s |
| **Total** | **4** | **96** | **Financial Truth Chain** | **255.33s** |

### 6.4 Why F4 is the Official Suite

1. **Only certified suite** — No other suite has reproducible evidence of full PASS.
2. **Complete chain coverage** — Financial Truth, Semantic Consistency, Traceability, Taxonomy Equivalence.
3. **Dedicated harness** — `tools/run_f4_suites.py` with preflight checks, mutation detection, DB integrity.
4. **Reproducible evidence** — 9 execution runs documented in `evidence/f4_suites/`.
5. **Historical precedent** — Commits `64f030a`, `3019b20`, `a3e0804`, `3a35826` all reference F4.

### 6.5 Relationship to Full Suite

| Suite | Tests | Certified | Notes |
|---|---|---|---|
| Full suite | 250 (203P/8F/39E) | NOT CERTIFIED | Includes F4 + 13 additional test files |
| F4 (certified) | 96 | YES (96/96 PASS) | Subset of full suite |
| Other tests | 154 | NOT CERTIFIED | ingestion, copilot, upload, regression, etc. |

---

## 7. MINIMUM REQUIRED RESULT

### 7.1 For Certification (F4 Suite)

```
96 PASS
0 FAIL
0 ERROR
0 SKIP
```

All 96 tests must pass with zero failures and zero errors.

### 7.2 For Full Suite Gate

```
0 FAIL
0 ERROR
```

(Pass count may vary as tests are added/removed. Failures and errors are
absolute blockers.)

---

## 8. CONDITIONS FOR PUSH

A push to `release/clean-functional-flow` or `master` requires:

1. **F4 Suite**: 96/96 PASS from clean worktree with V8 baseline copy.
2. **Zero new regressions**: All previously passing tests in full suite
   must continue passing.
3. **DB integrity**: Official DB SHA256 unchanged from certified value
   (`c76c3fee...`).
4. **No source-code changes** to: `engine/v4/domain/financial_engine.py`,
   `engine/v4/surgical_loader.py`, classification logic, closing logic.
5. **Evidence captured**: JUnit XML + execution JSON in `evidence/`.
6. **Worktree clean**: `git status` shows no modified tracked files.
7. **Dependencies verifiable**: `requirements.txt` produces reproducible
   venv.

---

## 9. CONDITIONS FOR PRODUCTION

In addition to all Push conditions:

1. **Full suite**: 0 FAIL, 0 ERROR across all 250 tests.
2. **Real regressions resolved**: RC3 (UPLOAD_DIR), RC6 (ML Cargo Venta),
   RC7 (PARIS taxonomy), RC8 (PARIS $15K delta) — must be fixed and
   certified.
3. **Environment artifacts resolved**: All worktree-sensitive tests must
   pass on production infrastructure (not relying on git worktree).
4. **Three clean consecutive runs**: F4 suite executed 3 times from clean
   checkout with identical results.
5. **DTE coverage**: Not required for production but must be measured.
6. **Apolinar Castro approval**: Product Owner sign-off.

---

## 10. MANDATORY EVIDENCE

### 10.1 Per Execution

Each certification execution MUST produce:

| Evidence | Format | Location |
|---|---|---|
| JUnit XML | `.xml` | `evidence/f4_suites/F4_{execution_id}.xml` |
| Execution JSON | `.json` | `evidence/f4_suites/F4_{execution_id}.json` |
| Harness stdout log | `.log` | `evidence/f4_suites/F4_{execution_id}.log` |
| Per-suite JUnit | `.xml` | `evidence/f4_suites/F4_{execution_id}_suite*.xml` |

### 10.2 Per Execution (mandatory fields in JSON)

| Field | Description |
|---|---|
| `execution_id` | Unique ID (timestamp-based) |
| `timestamp` | ISO 8601 timestamp |
| `harness_version` | Harness version (semver) |
| `commit` | Git commit SHA at execution time |
| `repository` | Repository URL or local path |
| `branch` | Git branch name |
| `returncode` | pytest exit code (0 = success) |
| `summary_line` | Full pytest summary line |
| `verdict` | PASS / REQUIRES_REMEDIATION / REJECTED |
| `verdict_reason` | Human-readable justification |
| `outcomes` | Per-test result (pass/fail/error/skip) |
| `pre_run_hashes` | SHA256 of all DBs before run |
| `post_run_hashes` | SHA256 of all DBs after run |
| `mutation_detected` | Boolean: any DB changed during run |
| `temp_v8_cleaned` | Boolean: temp V8 copy was removed |

### 10.3 Evidence Chain

```
RUN → evidence/f4_suites/{execution_id}.json
    → evidence/f4_suites/{execution_id}.xml
    → governance/coordination/execution_board.json (summary)
    → AGENTS.md (status update)
```

---

## 11. VERIFICATION TOOL

This contract is enforced by `tools/verify_runtime_contract.py`, which
automatically validates:

- All 13 runtime artifacts exist (SHA256 verified)
- All 5 test artifacts exist (SHA256 verified)
- Official DB integrity
- Templates present
- Taxonomy files present
- F4 suite available (4 test files exist)
- F4 harness available

Run: `python tools/verify_runtime_contract.py`

---

## 12. CONTRACT GOVERNANCE

| Role | Responsibility |
|---|---|
| **Owner** | Apolinar Castro — approves contract changes |
| **Technical Authority** | Codex — ensures contract fidelity |
| **Executor** | OpenCode — executes against contract |
| **Auditor** | `tools/verify_runtime_contract.py` — automated validation |

### Modification Process

1. RFC documenting the proposed change.
2. Impact analysis on all 10 contract clauses.
3. Owner approval.
4. Contract version bump.
5. Verifier update.
6. Evidence of re-certification.

---

## APPENDIX A: File Inventory

### A.1 All Test Files

| File | Tests | In F4? | Notes |
|---|---|---|---|
| `tests/test_certification_gate.py` | 29 | YES | Core certification gate |
| `tests/test_semantic_consistency.py` | 27 | YES | Cross-MP semantic checks |
| `tests/test_f4_traceability.py` | 22 | YES | RAW-to-Cierre trace |
| `tests/test_taxonomy_equivalence.py` | 18 | YES | YAML vs legacy equivalence |
| `tests/test_ingestion_handlers.py` | 53 | NO | 6 ingestion handler stages |
| `tests/test_copilot_ask.py` | 21 | NO | 11 Copilot question types |
| `tests/test_regression_contracts.py` | 14 | NO | Regression + contract checks |
| `tests/test_upload_center_e2e.py` | 10 | NO | Upload Center E2E |
| `tests/test_orchestrator_wiring.py` | 8 | NO | Orchestrator integration |
| `tests/test_new_mappings.py` | 6 | NO | Classification mappings |
| `tests/test_api_smoke.py` | 2 | NO | API route smoke test |
| `tests/test_falabella_promos.py` | 2 | NO | FALABELLA promos |
| `tests/test_integral_startup.py` | 2 | NO | Startup wiring |
| `tests/test_paris_classification.py` | 2 | NO | PARIS classification |
| `tests/test_ml_audit.py` | 1 | NO | ML audit |
| `tests/test_operational_pnl.py` | 3 | NO | Operational P&L |
| `tests/test_truth_005_registry.py` | 3 | NO | Registry traceability |
| `tests/test_v4_surgical_pipeline.py` | 1 | NO | Full pipeline integration |
| **Total** | **~250** | **96** | |

### A.2 All Templates

| File | In F4? | Required |
|---|---|---|
| `templates/dashboard.html` | NO | RUNTIME |
| `templates/executive_dashboard.html` | NO | RUNTIME |
| `templates/copilot.html` | NO | RUNTIME |
| `templates/upload_center.html` | NO | RUNTIME |
| `templates/documentary_dashboard.html` | NO | RUNTIME |

### A.3 All Database Baselines

| Baseline | SHA256 | Relationship |
|---|---|---|
| V2 (snapshot) | `df2ec8c3` | Historical |
| V3 (snapshot) | `50ff295e` | Historical |
| V4 (snapshot) | `28a96772` | Historical |
| V5 (snapshot) | `603cbb36` | Historical |
| V6 (snapshot) | `e1e341ef` | BASELINE_V6 — Original certified baseline |
| V7 (estable) | `bcb19aba` | Intermediate |
| V8 (candidate) | `733c759f` | F4 certification baseline |
| V9 (truth recovered) | `c76c3fee` | = Current official DB |

---

*End of CERTIFICATION CONTRACT v1.0*
