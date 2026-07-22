# P16F_02 — ML Adjustments Certification (ROOT CAUSE)

## Problem Statement
Ajustes & Retenciones muestra conceptos que provienen de `recuperaciones_y_bonificaciones`. Se requiere auditar `compensated`, `missing_invoice`, `Ajuste Poscobro`.

## Audit Results

### Concept-by-Concept Classification Audit

| detalle | canonical concept | financial_group (DB) | expected | match? |
|---------|------------------|---------------------|----------|--------|
| `compensated` | Recuperación por Pérdida de Inventario | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `missing_invoice` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `Ajuste Poscobro` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `reconciled` | Recuperación por Pérdida de Inventario | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `not_reconciled` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `refund_account_money` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `by_admin` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `INVALID_AUTHORIZATION` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `CREDIT_NOT_PROCESSED` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |
| `refunded` | Bonificación Logística Flex | `recuperaciones_y_bonificaciones` | `recuperaciones_y_bonificaciones` | ✅ |

### Full ML Financial Group Distribution

| financial_group | rows | total $ |
|----------------|-----:|--------:|
| ingresos | 32,931 | $934,773,504 |
| tesoreria | 79,973 | $691,101,844 |
| devoluciones | 12,425 | $179,783,187 |
| recuperaciones_y_bonificaciones | 2,072 | $50,061,360 |
| costos_operacionales | 23,637 | -$76,883,327 |
| costos_comerciales | 36,332 | -$185,616,582 |
| **ajustes** | **85** | **-$405,701** |

### ML Ajustes Detail (only concept = `Abono manual`)
| clasificacion_operativa | rows | total |
|------------------------|-----:|------:|
| Abono manual | 85 | -$405,701 |

There is **zero contamination** in ML `ajustes`. Only `Abono manual` (85 rows, -$405K) appears — all correctly classified as adjustments.

## Certification Status: PASS ✅

### Verdict
All 10 audited concepts are **correctly classified** in the DB:
- `compensated` → `recuperaciones_y_bonificaciones` ✅
- `missing_invoice` → `recuperaciones_y_bonificaciones` ✅
- `Ajuste Poscobro` → `recuperaciones_y_bonificaciones` ✅
- ML `ajustes` contains ONLY `Abono manual` — no contamination from return reasons or recovery concepts

### Evidence
- Full `recuperaciones_y_bonificaciones` breakdown documented (2 canonical concepts, 10 source detalle)
- ML `ajustes` verified via direct DB query — only 1 concept present
- Classification verified against both `marketplace_ledger_v1` (raw) and `marketplace_ledger_clasificado_v1` (classified)
- `taxonomy_rules.yaml` and `taxonomy_mappings.yaml` both consistent with DB classification

### Files Modified
None required — all classifications are correct.

### Remaining Risks
- `Abono manual` in ML `ajustes` (-$405K, 85 rows) — low value, appears to be genuine exceptional adjustments
- Root source of `Abono manual` not traced (out of scope for this certification)
