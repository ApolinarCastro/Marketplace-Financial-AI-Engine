# P34 — Repository Hygiene

**Date:** 2026-07-09
**Scope:** Raíz del proyecto, governance/, knowledge/, ARCHIVED/

---

## 1. Root Directory (178 files, 46.92 MB)

### 1.1 CONSERVAR (22 files, ~226 KB)

Archivos esenciales que deben permanecer en raíz:

| File | Size | Reason |
|---|---|---|
| `AGENTS.md` | 73 KB | FUENTE OFICIAL del estado del proyecto |
| `CLAUDE.md` | 73 KB | AI config |
| `GEMINI.md` | 2 KB | AI config |
| `.gitignore` | 225 B | Git ignore |
| `.mcp.json` | 514 B | MCP tools |
| `config.py` | 646 B | App config |
| `requirements.txt` | 177 B | Dependencies |
| `pyproject.toml` | 596 B | Project metadata |
| `run_app.py` | 812 B | Entry point |
| `START_APP.bat` | 1.9 KB | Windows startup |
| `package.json` | 343 B | Node deps |
| `skills-lock.json` | 3 KB | Skills config |
| `project.yaml` | 184 B | Project config |
| `knowledge_index.yaml` | 3.3 KB | Knowledge index |
| `README.md` | 3.6 KB | Readme |
| `BACKLOG.md` | 645 B | Backlog |
| `setup_aesp.py` | 5.4 KB | AESP setup |
| `setup_aesp_phase2.py` | 5.9 KB | AESP setup |
| `migrate_knowledge_base.ps1` | 5.2 KB | KB migration |
| `master_marketplace_dictionary_v1.json` | 9.1 KB | **CORE** financial dictionary |
| `poscobro_dictionary.json` | 28 KB | Poscobro reference |
| `poscobro_evidence.json` | 31 KB | Poscobro evidence |

### 1.2 ARCHIVAR → governance/ (70 files, ~148 KB)

Reportes de auditoría/certificación colocados en raíz en vez de governance/:

- `FINAL_VERDICT.md` (4.5 KB) — mover a governance/
- `SYSTEM_HEALTH.md` (10.4 KB)
- `TECHNICAL_FINDINGS.md` (7.0 KB)
- `TECHNICAL_CERTIFICATION.md` (14.5 KB)
- `TECHNICAL_DEBT_MATRIX.md` (8.8 KB)
- `ARCHITECTURE_REVIEW.md` (10.6 KB)
- `EVIDENCE_MATRIX.md` (7.9 KB)
- `EXECUTIVE_ASSESSMENT.md` (7.6 KB)
- `EXECUTIVE_VERDICT.md` (5.1 KB)
- `PLATFORM_SCORECARD.md` (7.3 KB)
- `PLATFORM_MATURITY_SCORECARD.md` (9.6 KB)
- `PRODUCT_READINESS.md` (4.7 KB)
- `COMMERCIAL_READINESS.md` (4.1 KB)
- `COMPETITIVE_ANALYSIS.md` (5.7 KB)
- `TOP_50_RECOMMENDATIONS.md` (8.2 KB)
- `INFORME_P27_RESUMEN_EJECUTIVO.md` (8.1 KB)
- `P0_P3_FINDINGS.md` (9.2 KB)
- `REPOSITORY_CERTIFICATION.md` (1.8 KB)
- `REGRESSION_ROOT_CAUSE.md` (1.2 KB)
- `LEDGER_CONSISTENCY_AUDIT.md` (3.0 KB)
- `API_CONTRACT_VALIDATION.md` (2.4 KB)
- `API_REGRESSION_REPORT.md` (1.7 KB)
- `FETCH_DUPLICATION_REPORT.md` (2.3 KB)
- `XML_CERTIFICATION_TRACE.md` (1.9 KB)
- `ELECTRONIC_CERTIFICATION_RECOVERY.md` (1.1 KB)
- `FRONTEND_BASELINE.md` (800 B)
- `FRONTEND_CALL_GRAPH_AFTER.md` (3.0 KB)
- `FRONTEND_CALL_GRAPH_BEFORE.md` (4.2 KB)
- `FRONTEND_CONCURRENCY_AUDIT.md` (1.3 KB)
- `FRONTEND_DIFF_REPORT.md` (1.1 KB)
- `FRONTEND_FINAL_CERTIFICATION.md` (958 B)
- `FRONTEND_PERFORMANCE_TRACE.md` (1.1 KB)
- `FRONTEND_RECOVERY_REPORT.md` (921 B)
- `FRONTEND_REGRESSION_REPORT.md` (1.1 KB)
- `FRONTEND_REGRESSION_ROOT_CAUSE.md` (2.4 KB)
- `FRONTEND_STATE_TRACE.md` (2.7 KB)
- `DATABASE_REGISTRY.md` (1.2 KB)
- `PLATFORM_BASELINE_V4_HASHES.txt` (763 B)
- `BASELINE_MANIFEST_V1.json` (1.5 KB)
- `BASELINE_MANIFEST_V1_P22Z.json` (977 B)
- `P32R4_API_TRACE.md` (711 B)
- `P32R4_DOCUMENT_TRACE.md` (906 B)
- `P32R4_FINAL_CERTIFICATION.md` (1.1 KB)
- `P32R4_FRONTEND_TRACE.md` (738 B)
- `P32R4_XML_TRACE.md` (666 B)
- `P32R5_ENDPOINT_TRACE.md` (1.3 KB)
- `P32R5_FINAL_CERTIFICATION.md` (1.0 KB)
- `P32R5_PERIOD_PROPAGATION.md` (1.5 KB)
- `P32R5_PERIOD_VALIDATION.md` (1.4 KB)
- `P32R5_SQL_LOG.md` (1.1 KB)
- `P32R7_BACKEND_HEALTH.md` (616 B)
- `P32R7_CONTRACT_MATRIX.md` (586 B)
- `P32R7_FINAL_HEALTH_CERTIFICATION.md` (708 B)
- `P32R7_FRONTEND_HEALTH.md` (614 B)
- `P32R7_REGRESSION_MATRIX.md` (969 B)
- `P32R7_SINGLE_SOURCE_AUDIT.md` (515 B)
- `P32R7_TRACEABILITY_AUDIT.md` (815 B)
- `P32R7_TRACEABILITY_CONSUMPTION.md` (588 B)
- `P32R8_BACKEND_HEALTH.md` (410 B)
- `P32R8_CONTRACTS.md` (373 B)
- `P32R8_FINAL_VERDICT.md` (302 B)
- `P32R8_QUERY_TRACE.md` (873 B)
- `P32R8_SINGLE_SOURCE.md` (102 B)
- `P32R8_STRESS_TEST.md` (497 B)
- `P32R8_TRACEABILITY.md` (230 B)
- `FINAL_STABILITY_CERTIFICATION.md` (1.2 KB)
- `FINAL_API_STABILITY_CERTIFICATION.md` (1.1 KB)
- `FINAL_FINANCIAL_CONSISTENCY_CERTIFICATION.md` (1.3 KB)
- `FINAL_FRONTEND_PERFORMANCE_CERTIFICATION.md` (1.6 KB)
- `MASTER_KNOWLEDGE_INDEX.md` (208 B) → `knowledge/`

### 1.3 ELIMINAR (85 files, ~47.8 MB)

**Categoría A: Logs masivos (43.2 MB)**

| File | Size | Evidence |
|---|---|---|
| `marketplace_audit_sql.log` | 43.06 MB | SQL trace log de auditoría. No git-tracked, no consumido por sistema. **92% del peso de raíz.** |
| `tmp_out2.txt` | 1.76 MB | Temp output |
| `tmp_rfc_causality_out.txt` | 617 KB | Temp RFC dump |

**Categoría B: Backups de dashboard (4 archivos, 418 KB)**

| File | Size | Evidence |
|---|---|---|
| `baseline_dashboard.html` | 124 KB | Baseline, superseded by api.py |
| `dashboard_old.html` | 124 KB | Old version |
| `dashboard_before.html` | 85 KB | Pre-fix backup |
| `dashboard_before_hotfix.html` | 85 KB | Pre-hotfix backup |

**Categoría C: One-off fix scripts (9 archivos, 58 KB)**

| File | Evidence |
|---|---|
| `fix_dashboard.py` (11.5 KB) | One-off |
| `fix_drawer.py` (6.5 KB) | One-off |
| `fix_drawer_2.py` (10.0 KB) | One-off |
| `fix_status_3.py` (4.4 KB) | One-off |
| `fix_head.py` (1.2 KB) | One-off |
| `fix_auditoria.py` (1.0 KB) | One-off |
| `fix_workflow.py` (1.3 KB) | One-off |
| `update_dash.py` (23 KB) | One-off |
| `baseline_api.py` (25 KB) | Superseded by api/api.py |

**Categoría D: Temp/output scripts (15 archivos, 57 KB)**

| File | Evidence |
|---|---|
| `tmp_h3_sft.py` (4.6 KB) | Scratch |
| `tmp_p32r7_deep_stress.py` (6.6 KB) | Scratch |
| `tmp_g6_full.txt` (10 KB) | Temp output |
| `tmp_g6_f2_out.txt` (10 KB) | Temp output |
| `tmp_g6_f3_out.txt` (8.5 KB) | Temp output |
| `tmp_g6_out.txt` (8.5 KB) | Temp output |
| `tmp_out1.txt` (6.1 KB) | Temp output |
| `tmp_rfc_structure_out.txt` (26 KB) | Temp output |

**Categoría E: Scratch tests (14 archivos, 7 KB)**

| File | Evidence |
|---|---|
| `test.py`, `test2.py` through `test6.py` (149-241 B) | Scratch |
| `test_apis.py`, `test_app.py`, `test_endpoints.py` etc. | Scratch |

**Categoría F: Audit one-off scripts (4 archivos, 23 KB)**

| File | Evidence |
|---|---|
| `generate_audit_p32r7.py` (6.5 KB) | One-off |
| `run_p32r8_audit.py` (5.4 KB) | One-off |
| `generate_p32r8_audit_direct.py` (4.4 KB) | One-off |
| `validate_endpoints.py` (1.1 KB) | One-off |

**Categoría G: JSON artifacts (13 archivos, 143 KB)**

| File | Evidence |
|---|---|
| `api_edits.jsonl` (96 KB) | AI edit log |
| `api_edits_all.jsonl` (79 KB) | AI edit log |
| `api_edits_exclude.jsonl` (268 KB) | AI edit log |
| `recovered_data.json` (46 KB) | Data dump, already consumed |
| `_classification_results.json` (3.7 KB) | Temp intermediate |
| `_dry_run_results.json` (3.7 KB) | Temp intermediate |
| `_fase2_results.json` (3.2 KB) | Temp intermediate |
| `_fase3_results.json` (803 B) | Temp intermediate |
| `data_state_duckdb.json` (1.8 KB) | DB state dump |
| `stress_results.json` (780 B) | Temp |
| `summary_result.json` (4.1 KB) | Temp |
| `metrics_before/after.json` (173 B each) | Metrics snapshots |

**Categoría H: Text diff/output (9 archivos, 324 KB)**

| File | Evidence |
|---|---|
| `dashboard_history.txt` (127 KB) | Git log dump |
| `dashboard_log.txt` (127 KB) | Log dump |
| `git_log_dashboard.txt` (127 KB) | Git log dump |
| `dashboard_diff*.txt` (57-126 KB) | Git diff artifacts |
| `executive_content.txt` (76 KB) | Content dump |
| `sql_evidence_output.txt` (7.5 KB) | SQL output |
| `_audit_full_output.txt` (11.6 KB) | Audit output |
| `syntax_before.*` (0-479 B) | Empty/patch files |

**Categoría I: Misc debris (8 archivos, 784 KB)**

| File | Evidence |
|---|---|
| `REPOSITORY_REGISTRY.json` (419 KB) | Generated dump |
| `browser_dom_snapshot.html` (156 KB) | Test artifact |
| `temp_verify.js` (36 KB) | Temp JS |
| `dashboard_before.js` (4 KB) | Pre-fix backup |
| `_integrate_dictionary.mjs` (13 KB) | Temp script |
| `test_db2.duckdb` (12 KB) | Scratch DB |
| `KnowledgeBase_baseline_v4.zip` (24 KB) | Zipped baseline |
| `evidence_ux12_*.png` (4 files, 848 KB) | Screenshots → governance/evidence/ |

---

## 2. governance/ Hygiene

### 2.1 OBSOLETO (14 files) — recomienda: archivar o eliminar

14 archivos que contienen conclusiones invalidadas. Conservar solo si se necesita el registro de qué se invalida.

**Paris Duplicate chain (6 files):** Contienen la conclusión errónea de $21.2M/1,573 grupos duplicados (DEC-020: SOBRESTIMÓ 93%). La corrección V2 está en `PARIS_FORENSIC_TRUTH_CERTIFICATION.md` (vigente).

**Paris Economic Model V1 (2 files):** `PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md` y `PARIS_ECONOMIC_MODEL_COMPARISON.md`. INVALIDATED por V2. La corrección está en `PARIS_BUSINESS_MODEL_V2_CERTIFICATION.md`.

**RIPLEY_GROSS_REVENUE_CERTIFICATION.md:** Título dice RECHAZADO. Contiene la conclusión que encontró el gap de date-parsing.

**EVENT_REGISTRY_V1.md:** Superseded by knowledge/core/EVENT_REGISTRY_V2.md.

**MARKETPLACE_CHARGE_RECONCILIATION_CERTIFICATION.md:** V1 superseded by V2.

**PARIS_BUSINESS_MODEL_FINAL_CERTIFICATION.md:** INVALIDATED by V2.

### 2.2 DUPLICADO (6 files)

`SKILLS_REGISTRY.json` + `SKILLS_REGISTRY.md`: mismo contenido en formatos diferentes. Ambos superseded por `SKILLS_REGISTRY_V1.md`.

`phase12b_raw.json` + `phase12b_raw_results.json`: Hallazgos absorbidos en reportes PHASE_12B_*.

### 2.3 HISTÓRICO (50 files)

Archivos de eventos únicos ya completados o diseños no implementados.

Recomendación: mover a `governance/archive/` para mantener limpio el directorio principal, o dejar en su lugar pero etiquetados (ya están correctamente agrupados en subdirectorios).

---

## 3. knowledge/ Hygiene

### 3.1 ELIMINAR — 25 stub files

Los 20 archivos "Legacy [category] artifact." con menos de 100 bytes contienen **cero contenido informativo**. Son artefactos de una estructura de archivos anterior.

Los 5 tiny KO status files (47-95 bytes) contienen frases como "Data availability analizada: 0 XML disponibles" — valor analítico nulo.

### 3.2 ARCHIVAR — 14 empty templates

8 engine templates + 4 marketplace templates + 2 empty index files. Estructura sin contenido.

---

## 4. Summary

| Location | CONSERVAR | ARCHIVAR | ELIMINAR | Total |
|---|---|---|---|---|
| Root | 22 | 70 | 85 | 178 |
| governance/ | 286 | 50+14+6 | 0* | 356 |
| knowledge/ | 88 | 14 | 25 | 127 |
| **Total** | **396** | **154** | **110** | **661** |

*governance/ OBSOLETO/DUPLICADO = 20 files que no se recomienda eliminar (contienen registro histórico de qué se invalidó)

### Space Recovery

| Category | Est. space |
|---|---|
| `marketplace_audit_sql.log` | 43.06 MB |
| Other temp/scratch/output | ~4.7 MB |
| **Total recoverable** | **~47.8 MB** |

### Files Recoverable

| Category | Count | Type |
|---|---|---|
| Root temp/scratch | 85 | Logs, backups, scripts, JSON artifacts |
| knowledge/ stubs | 25 | "Legacy artifact" files |
| knowledge/ templates | 14 | Empty engine/marketplace templates |
| **Total** | **124** | 18.8% of all files |

All evidence is based on file content, size, and cross-referencing with the project's own documentation (AGENTS.md, knowledge_index.yaml, engine code).
