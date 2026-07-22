# DEC-027: Reconciliation Engine Authority

**Status**: CERTIFIED  
**Date**: 2026-06-16  
**Author**: System (Phase 11)

## Decision

`engine/v4/reconciliation/reconciliation_engine.py` is the **single universal reconciliation authority**. All cross-source financial verification must use this engine.

## Rationale

- 5 reconciliation levels: INTERNA, OPERACIONAL, TESORERÍA, DOCUMENTAL, UNIVERSAL
- Every alert includes SQL evidence, row count, and financial impact
- NaN-safe, Pydantic-validated, deterministic
- 66 tests PASS across all levels

## Frozen Interface

```python
class ReconciliationEngine:
    def validate_marketplace_consistency(marketplace, periodo) -> ReconciliationResult
    def reconcile_level1_internal(marketplace, periodo) -> LevelResult
    def reconcile_level2_operational(marketplace, periodo) -> LevelResult
    def reconcile_level3_treasury(marketplace, periodo) -> LevelResult
    def reconcile_level4_documentary(marketplace, periodo) -> LevelResult
```

## Contract

```python
class ReconciliationResult(BaseModel):
    marketplace: str
    period: str
    certification_status: CertificationStatus
    delta: float
    operational_total: float
    settlement_total: float
    treasury_total: float
    taxonomy_coverage: float
    document_coverage: float
    orphan_records: int
    total_records: int
```

## Rollback

Comment out `ReconciliationEngine` calls in api.py and use previous inline reconciliation (not recommended — loss of evidence traceability).
