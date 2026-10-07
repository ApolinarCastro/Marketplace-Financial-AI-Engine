# PFO FA-007 — RESTART REPRODUCIBILITY EVIDENCE

## Task Info

```
TASK_ID: PFO-FA007-RESTART-REPRODUCIBILITY-001
DATE: 2026-10-07
HEAD: 6d3ed64aea7a152c232da3cb1f0dca0fbed3f019
BRANCH: main
```

## Formal Definition

```
FA-007: A clean restarted/recreated execution reproduces the certified E2E_V2
result without dependence on prior runtime/database state.
```

## Restart Boundary (proven, not assumed)

```
RUN_1 TEMP_DB: data/db/tmp_pfo_fa007_restart/ (fresh init, removed after)
RUN_2 TEMP_DB: data/db/tmp_pfo_fa007_restart_r2/ (fresh init, removed after)
DatabaseV4 singleton: RESET + rebound per run, reset in finally blocks
RUN_1 execution_id: bd776dd6-… (distinct)
RUN_2 execution_id: 5d2d3b9f-… (distinct, execution_ids_differ TRUE)
No shared connections, no reused TEMP_DB, no pre-populated tables.
Prior FA-005 comparison JSON carries no execution_id field; boundary proven
by fresh paths + distinct RUN_1/RUN_2 ids.
```

## RUN_1 Results

```
fresh_clean TRUE (all zero-checks 0, tables exist incl. execution_id + document_match)
ingestion COMPLETED, 9 new, 0 errors
raw ledger 9 rows, parity TRUE (0 missing/0 unexpected/0 mismatches)
classified 9 (8 op + 1 treasury Retiro de dinero/tesoreria/FALSE/-20800.0)
closing neto 20800.0 / mirror 0.0 / 9 CONCILIATED / 0 orphans / coverage 100.0
L1-L4 all PASS delta 0.0 / aggregate CERTIFICADO (delta 0, tax 100, doc 100)
business_sha256: dc9e149c2b955919…
```

## RUN_2 Results

Identical in every business field (see comparison JSON). business_sha256
identical: dc9e149c2b955919… Distinct execution_id.

## Comparisons

```
RUN_1 vs GOLDEN: EQUAL (0 mismatches; net 20800; treasury -20800; coverage 100; CERTIFICADO)
RUN_2 vs GOLDEN: EQUAL (same)
RUN_1 vs RUN_2: EQUAL (business_sha256 identical; execution_ids differ)
RUN_1 vs PRIOR CERTIFIED (11_ FA-005 R1): EQUAL (9 rows, nets, mirror, coverage, levels, aggregate)
RUN_2 vs PRIOR CERTIFIED: EQUAL (same)
TOTAL_FIELD_MISMATCHES: 0
```

Note on raw totals: raw ledger SUM = 0.0 is CORRECT (20800 operational +
−20800 treasury). Operational net 20800.0 verified separately via closing.

## Non-Contamination / Cleanup

```
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
TEMP_ARTIFACTS_LEFT: 0 (both TEMP DBs + executor script removed; verified)
```

## Boundaries (unchanged)

```
DOCUMENTAL_XML_TRACEABILITY: PASS / XML_DTE_E2E: PASS
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED
```

## Verdict

```
FA-001..FA-007: ALL PASS
FIRST_BLOCKER: NONE
PROJECT_FINISH_ONE_CORE_DOD: PASS (FA-007 is the last formal FA criterion;
  repo search finds no FA-008/FA-009/FA-010 or competing DoD declaration)
FIRST END-TO-END CERTIFIED PASS: ACHIEVED, with limitation
  ELECTRONIC_SIGNATURE_CERTIFICATION = NOT_IMPLEMENTED
```

## Next Exact Action

None within PROJECT FINISH ONE core DoD. Independent tracks remain:
electronic-signature hardening/crypto-deps, production rollout readiness.
No auto-start.
