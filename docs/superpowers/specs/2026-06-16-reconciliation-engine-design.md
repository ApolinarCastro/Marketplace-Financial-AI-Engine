# Reconciliation Engine V1 — Design Spec

## Status: APROBADO

## Purpose

Single universal reconciliation authority for Marketplace Financial AI Engine.
Eliminates scattered validations, duplicate calculations, inconsistent states, and
marketplace-specific rules.

## Architecture

```
engine/v4/reconciliation/
├── reconciliation_engine.py      # Main engine (5 levels + universal contract)
├── reconciliation_contracts.py   # Pydantic models for all outputs
└── reconciliation_rules.yaml     # Configurable rules (deltas, coverage thresholds)
```

## Constraints (hard gates)

1. **SINGLE FINANCIAL TRUTH** — consume exclusively `marketplace_ledger_clasificado_v1`.
   No legacy tables, temp views, or parallel sources.
2. **NO RE-PARSING XML** — documentary reconciliation uses only `document_match_v1` + `dte_truth_v1`.
3. **ÚNICA AUTORIDAD** — all statuses (CERTIFICADO|PARCIAL|PENDIENTE|ERROR|FINANCIAL_INTEGRITY_BROKEN)
   come exclusively from this engine. No endpoint or frontend calculates states.
4. **EVIDENCIA OBLIGATORIA** — every alert includes marketplace, period, rule violated,
   impact amount, row count, SQL query, associated evidence. No evidence = no alert.
5. **COBERTURA TAXONÓMICA** — if any records lack `financial_group`, status = PARCIAL. Never CERTIFICADO.
6. **VALIDACIÓN UNIVERSAL** — same code for ML/PARIS/RIPLEY/FALABELLA. Zero MP-specific branches.
7. **OBSERVABILIDAD** — native metrics: `reconciliation_delta`, `taxonomy_coverage`,
   `document_coverage`, `orphan_records`, `certification_status`.
8. **PROHIBICIONES** — no UI, no dashboards, no taxonomy YAML, no financial_engine.py modifications.
9. **Zero new tables** — engine is read-only (query only).

## Universal Contract

```python
def validate_marketplace_consistency(
    marketplace: str,
    periodo: str | None = None,
) -> ReconciliationResult
```

### ReconciliationResult

| Field | Type | Description |
|-------|------|-------------|
| marketplace | str | MP code |
| period | str | Period label |
| certification_status | Literal[CERTIFICADO, PARCIAL, PENDIENTE, ERROR, FINANCIAL_INTEGRITY_BROKEN] | Final verdict |
| delta | float | Total delta across all levels |
| operational_total | float | Operational P&L |
| settlement_total | float | Settlement total |
| treasury_total | float | Treasury total |
| taxonomy_coverage | float | % of records with financial_group |
| document_coverage | float | % of records with document match |
| orphan_records | int | Records without document match |
| alerts | list[ReconciliationAlert] | Violations with evidence |
| levels | dict[str, LevelResult] | Per-level results |

### ReconciliationAlert

| Field | Type |
|-------|------|
| marketplace | str |
| period | str |
| level | str |
| rule | str |
| impact_amount | float |
| record_count | int |
| sql_query | str |
| evidence | str |

### LevelResult

| Field | Type |
|-------|------|
| level | str |
| status | str |
| delta | float |
| source_total | float |
| target_total | float |
| alerts | list[ReconciliationAlert] |

## 5 Levels

| Level | Name | Source A | Source B | Validation |
|-------|------|----------|----------|------------|
| 1 | INTERNA | `clasificado_v1` SUM by `financial_group` | `cierre_financiero_v1` totals | SUM(clasificado) by group = cierre totals per group |
| 2 | OPERACIONAL | `clasificado_v1` WHERE `include_in_operational_pnl=1` | `cierre_financiero_v1.resultado_neto` | Operational P&L = cierre resultado_neto |
| 3 | TESORERÍA | `clasificado_v1` WHERE `financial_group='tesoreria'` | Resultado neto - Operational P&L | Settlement = Treasury |
| 4 | DOCUMENTAL | `clasificado_v1.folio_xml` | `document_match_v1` + `dte_truth_v1` | Coverage %, orphans, unmatched |
| 5 | UNIVERSAL | Same contract × 4 MPs | — | All MPs pass same validation |

## Rules YAML Structure

```yaml
rules:
  allowed_delta: 0
  critical_delta: 1
  minimum_coverage:
    taxonomy: 100
    document: 95
  status_thresholds:
    - name: CERTIFICADO
      max_delta: 0
      min_taxonomy_coverage: 100
    - name: PARCIAL
      max_delta: 10
      min_taxonomy_coverage: 50
  observability:
    enabled: true
```

## Status Determination

| Condition | Status |
|-----------|--------|
| delta = 0 AND taxonomy_coverage = 100% | CERTIFICADO |
| delta <= critical_delta AND taxonomy_coverage >= 50% | PARCIAL |
| taxonomy_coverage < 50% | PENDIENTE |
| delta > critical_delta AND delta <= 1000 | ERROR |
| delta > 1000 | FINANCIAL_INTEGRITY_BROKEN |

## Testing (40+ tests)

- delta = 0 (happy path)
- delta > 0 (alert path)
- Marketplace vacío (no data)
- Taxonomía incompleta (missing financial_group)
- Cobertura documental insuficiente (< 95%)
- Marketplace certificado (full coverage)
- All 4 MPs tested
- Edge: NaN, None, empty results

## Dependencies

- `engine.v4.database.DatabaseV4` — DB singleton
- `engine.v4.domain.financial_engine.FinancialEngine` — period resolution, cierre queries
- `taxonomy.taxonomy_loader` — concept → financial_group resolution
- `pydantic` — output contracts

## Deliverables

- `docs/superpowers/specs/2026-06-16-reconciliation-engine-design.md` (this file)
- `engine/v4/reconciliation/reconciliation_contracts.py`
- `engine/v4/reconciliation/reconciliation_rules.yaml`
- `engine/v4/reconciliation/reconciliation_engine.py`
- `tests/test_reconciliation_engine.py`
- `RECONCILIATION_ENGINE_CERTIFICATION.md`
- `RECONCILIATION_ENGINE_EVIDENCE_REPORT.md`
