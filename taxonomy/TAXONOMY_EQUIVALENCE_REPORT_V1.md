# TAXONOMY EQUIVALENCE REPORT V1

**Date:** 2026-06-16
**Status:** ✅ PASS — 100% equivalence

## Executive Summary

La taxonomía financiera ha sido extraída del código Python embebido (`marketplace_auditor.py`) hacia una capa declarativa YAML. Ambas clasificaciones (legacy Python vs YAML) producen resultados idénticos para los 4 marketplaces.

## Estructural Equivalence

| Metric | Value |
|--------|-------|
| Financial Groups | 8 (ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes, recuperaciones_y_bonificaciones, tesoreria, impuestos) |
| Total Concepts in Groups | 163 |
| Raw Detail Mappings | 215 |
| Normalized Map Entries | 199 |
| Structural Mismatches | 0 ✅ |
| Normalized Map Mismatches | 0 ✅ |
| Concept → Group Mismatches | 0 ✅ |

### Edge Cases (Expected)
4 concepts are dynamically resolved in runtime (not in FINANCIAL_STRUCTURE):
- `Pago` → handled by payout_rule, gets `None` financial_group
- `Devolución de dinero\nEnvío` (and 2 encoding variants) → compound concept

These are identical between legacy Python and YAML classification.

## Runtime Equivalence

### Per-Marketplace Classification

| Marketplace | Rows | Clasificacion | Financial Group | Op PnL | Delta $ |
|-------------|------|--------------|-----------------|--------|---------|
| ML | 101,603 | 0 mismatches | 0 mismatches | 0 mismatches | $0 |
| PARIS | 42,487 | 0 mismatches | 0 mismatches | 0 mismatches | $0 |
| RIPLEY | 62,502 | 0 mismatches | 0 mismatches | 0 mismatches | $0 |
| FALABELLA | 1,008 | 0 mismatches | 0 mismatches | 0 mismatches | $0 |

### Financial Group Monetary Equivalence (per MP, per group)

All financial groups across all 4 marketplaces show $0 delta between legacy and YAML classification.

### Operational PnL Equivalence

Operational PnL (include_in_operational_pnl=True) shows $0 delta across all marketplaces.

## Coverage

| Component | Legacy Python | YAML | Match |
|-----------|-------------|------|-------|
| FINANCIAL_STRUCTURE | 8 groups, 163 concepts | 8 groups, 163 concepts | 100% |
| RAW_TO_CLASSIFICATION_MAP | 215 mappings | 215 mappings | 100% |
| NORMALIZED_CLASSIFICATION_MAP | 199 entries | 199 entries | 100% |
| CLASIFICACION_TO_FINANCIAL_GROUP | 159 entries | 159 entries | 100% |
| normalize_detail | Unicode NFD + lowercase + alphanumeric | Same implementation | 100% |
| payout_rule | regex match | Same regex | 100% |
| history_rule | date-based | Same date logic | 100% |
| ml_mandatory_exclusions | 14 items | Same 14 items | 100% |
| general_exclusions | 8 items | Same 8 items | 100% |

## Resultado Final

```
Coincidencias = 100%
Diferencias = 0
Delta monetario = $0
```

**Veredicto: APROBADO ✅** — Taxonomía YAML lista para FASE REFACTOR.
