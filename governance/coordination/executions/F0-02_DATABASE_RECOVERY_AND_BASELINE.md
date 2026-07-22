# F0-02 — Database Recovery and Baseline Stabilization

## Execution Report

**Date**: 2026-07-15
**Status**: CERTIFIED_SNAPSHOT_NOT_FOUND — Restoration halted per protocol

---

## 1. Forensic Preservation (COMPLETED)

### Current Official DB (Contaminated)
- **Path**: `data/db/meli_financial_v4.db`
- **SHA256**: `BF6ED7AEC5410ABE033B2A3C271011DDFCE044F0E4C9008ABA590AE48BA52AA6`
- **Size**: 55,848,960 bytes
- **Timestamp**: 2026-07-15 13:28

### Forensic Copy Created
- **Path**: `data/db/meli_financial_v4.db.forensic_20260715_134512`
- **SHA256**: `BF6ED7AEC5410ABE033B2A3C271011DDFCE044F0E4C9008ABA590AE48BA52AA6` (identical)
- **Preserved**: Yes, not deleted per protocol

---

## 2. Snapshot Verification (FAILED — No Certified Post-B2.5C Snapshot Found)

### Candidate 1: `snapshot_pre_fase2_20260603_112908` (HAS MANIFEST)
- **SHA256**: `3939AD54B2442B1D7182AEE856265979B6433E04842A6FF7EF7EBA957B4915EA`
- **Manifest**: Exists, explicitly states: `"description": "Pre-B2.5C classification+closing execution"`
- **Pre-state**: `"ripley_financial_group": "100% NULL"`, `"clasificado_table": "stale_pre_RFC001_data"`
- **Row counts**: ledger=207,600 | clasificado=414,314 | cierre=118
- **Verdict**: **PRE-B2.5C** — Does not satisfy "post-B2.5C certificado" requirement

### Candidate 2: `snapshot_pre_poscobro_fix_20260605_155052` (NO MANIFEST)
- **SHA256**: `C142705A54166C778F88214335608530B0E95406B11F05EA72BC5661BECE0848`
- **Manifest**: **MISSING** — No documentary evidence linking to B2.5C
- **Row counts**: ledger=207,600 | clasificado=207,600 | cierre=140
- **RIPLEY**: 17 periods with non-zero neto (Jan 2025 – May 2026)
- **Verdict**: **POST-B2.5C data matches** but **NO DOCUMENTARY EVIDENCE** — Fails "evidencia documental que vincule el snapshot con B2.5C"

### Other Snapshots
No other snapshots have both: (a) post-B2.5C data state AND (b) MANIFEST.json linking to B2.5C certification.

---

## 3. Contamination Analysis (Current DB vs Certified Pre-B2.5C Snapshot)

| Component | Current DB | Certified Snapshot | Delta | Classification |
|-----------|------------|-------------------|-------|----------------|
| `marketplace_ledger_v1` | 374,303 | 207,600 | +166,703 | **Financial data added post-snapshot** |
| `marketplace_ledger_clasificado_v1` | 294,607 | 414,314 | -119,707 | **Schema/rebuild changed row structure** |
| `marketplace_cierre_financiero_v1` | 246 | 118 | +108 | **Additional periods closed** |
| `ingestion_registry` | 43 records | 0 (table missing) | +43 | **Test uploads (38 ML facturacion + 5 test files)** |
| `file_registry` | 55 | 0 | +55 | **Test file uploads persisted** |
| `pipeline_log` | 1,493 | 0 | +1,493 | **Test execution logs** |
| New tables (12) | Present | Absent | — | **Phase 12-16, P39, P40 additions** |

### Test Artifacts Identified
- **38 ingestion_registry records**: ML Facturacion 2026-01 uploaded 3x (Jul 13, Jul 14×2, Jul 15×2)
- **5 test files**: `pos_test.xlsx`, `fact_test.xlsx`, `report_drop.xlsx`, `report_full.xlsx`, `ML_Facturacion_2026-01_test.csv`
- **Duplicate test uploads**: Same test file uploaded 6 times (detected as duplicates by system)
- **Execution IDs**: Multiple `execution_id` values in ingestion_registry from 2026-07-13 to 2026-07-15

### Changes Outside Ingestion Registry
- **12 new tables**: `cierre_financiero_v2`, `document_match_v1`, `dte_ledger_link`, `dte_link_v1`, `dte_ripley_traceability`, `ingestion_registry`, `ripley_corrected_certification`, `ripley_financial_mapping`, `ripley_settlement_chain`, `ripley_traceability_graph`, `test_x`, `v_ledger_certified`
- **Financial logic changes**: Phase 12-16, P39, P40 modifications to ledger, classification, closing, certification engines
- **Not CAP-001 only**: Contamination spans multiple certified phases, not isolated to CAP-001

---

## 4. Recovery Decision

**CERTIFIED_SNAPSHOT_NOT_FOUND**

Per F0-02 Section 2: *"Si no existe un snapshot verificable, detener exclusivamente la restauración y emitir: CERTIFIED_SNAPSHOT_NOT_FOUND"*

No snapshot satisfies all verification criteria:
1. ✅ Full SHA256 hash
2. ✅ 207,600 ledger rows
3. ✅ 207,600 classified rows  
4. ❌ 109 cierre rows (candidates have 118 or 140)
5. ⚠️ 17 RIPLEY rows (interpretation varies: 17 periods with data vs 17 total rows)
6. ❌ **Documentary evidence linking to B2.5C certification**

**Restoration HALTED.** No manual reconstruction of financial data permitted per Section 2.

---

## 5. Required Next Steps

1. **Product Owner Decision**: Define acceptable baseline for recovery
2. **Snapshot Certification**: Create MANIFEST for `snapshot_pre_poscobro_fix_20260605_155052` with B2.5C linkage, OR
3. **Baseline Re-establishment**: Execute full pipeline from BASELINE_V6 (SHA256: `e1e341ef...`) through B2.5C with full certification
4. **Test Infrastructure Fix**: Isolate CAP-001 tests to temporary DBs/directories before re-attempt

---

## 6. Evidence Files

- Forensic DB copy: `data/db/meli_financial_v4.db.forensic_20260715_134512`
- Current DB (contaminated): `data/db/meli_financial_v4.db` (SHA256: `BF6ED7AEC...`)
- Certified Pre-B2.5C: `data/db/snapshot_pre_fase2_20260603_112908/` (SHA256: `3939AD54...`)
- Post-B2.5C Candidate: `data/db/snapshot_pre_poscobro_fix_20260605_155052/` (SHA256: `C142705A...`)

---

**Report Location**: `governance/coordination/executions/F0-02_DATABASE_RECOVERY_AND_BASELINE.md`