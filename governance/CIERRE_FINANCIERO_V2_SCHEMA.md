# CIERRE_FINANCIERO_V2_SCHEMA

## Read-Only SCOUT — Phase Governance 01 / S2 Survey  
**Date:** 2026-06-22  
**Status:** DRAFT — Not implemented

---

## 1. Design Principles

1. **Backward compatible** — v2 must coexist with v1 during migration (no breaking changes)
2. **SIGNAL-native** — The canonical close is SIGNAL-filtered; ALL mode is a secondary output
3. **Single Financial Truth** — Every row must be traceable to `marketplace_ledger_v1` via SQL
4. **Immutable** — Once written, v2 rows must never be mutated (append-only)
5. **DEC-019 compatible** — v2 must respect `include_in_operational_pnl` filter

---

## 2. Proposed Table Schema

```sql
CREATE TABLE IF NOT EXISTS marketplace_cierre_financiero_v2 (
    -- Identity
    marketplace         VARCHAR NOT NULL,
    periodo_inicio      DATE NOT NULL,
    periodo_fin         DATE NOT NULL,
    
    -- Mode: SIGNAL (canonical) or ALL (legacy-compatible)
    signal_mode         VARCHAR NOT NULL DEFAULT 'SIGNAL',
    
    -- SIGNAL-filtered aggregates (canonical P&L)
    signal_ingresos             DOUBLE DEFAULT 0,
    signal_devoluciones         DOUBLE DEFAULT 0,
    signal_costos_operacionales DOUBLE DEFAULT 0,
    signal_costos_comerciales   DOUBLE DEFAULT 0,
    signal_ajustes              DOUBLE DEFAULT 0,
    signal_resultado_neto       DOUBLE DEFAULT 0,
    
    -- ALL-mode aggregates (legacy-compatible, same as v1 formula)
    full_ingresos             DOUBLE DEFAULT 0,
    full_devoluciones         DOUBLE DEFAULT 0,
    full_costos_operacionales DOUBLE DEFAULT 0,
    full_costos_comerciales   DOUBLE DEFAULT 0,
    full_ajustes              DOUBLE DEFAULT 0,
    full_resultado_neto       DOUBLE DEFAULT 0,
    
    -- Metadata
    row_count       INTEGER DEFAULT 0,
    signal_row_count INTEGER DEFAULT 0,
    dte_linked_rows INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Uniqueness: one row per MP + period + mode
    UNIQUE(marketplace, periodo_inicio, signal_mode)
);
```

---

## 3. Column Rationale

| Column | Source | Purpose |
|--------|--------|---------|
| `signal_ingresos` | `SUM(monto) WHERE financial_group='ingresos' AND detalle IN (SIGNAL_list) AND op_pnl=1` | Canonical gross revenue |
| `signal_devoluciones` | `SUM(monto) WHERE financial_group='devoluciones' AND detalle IN (SIGNAL_list) AND op_pnl=1` | Canonical returns |
| `signal_costos_operacionales` | `SUM(monto) WHERE financial_group IN ('costos_operacionales','costos_logisticos') AND detalle IN (SIGNAL_list) AND op_pnl=1` | Canonical logistics costs |
| `signal_costos_comerciales` | `SUM(monto) WHERE financial_group IN ('costos_comerciales','comisiones') AND detalle IN (SIGNAL_list) AND op_pnl=1` | Canonical commissions |
| `signal_ajustes` | `SUM(monto) WHERE financial_group IN ('ajustes','recuperaciones_y_bonificaciones') AND detalle IN (SIGNAL_list) AND op_pnl=1` | Canonical adjustments |
| `signal_resultado_neto` | `signal_ingresos + signal_devoluciones + signal_costos_operacionales + signal_costos_comerciales + signal_ajustes` | Verified conservation |
| `full_*` | Same as current v1 formula | Legacy compatibility |
| `row_count` | Total operational rows for period | Coverage metric |
| `signal_row_count` | SIGNAL rows only | Signal density metric |
| `dte_linked_rows` | Rows with non-null `folio_xml` | DTE coverage |

---

## 4. Differences from Experimental `cierre_financiero_v2`

| Aspect | Experimental v2 | Proposed v2 |
|--------|----------------|-------------|
| Name | `cierre_financiero_v2` | `marketplace_cierre_financiero_v2` |
| Source table | `marketplace_ledger_v1` | `marketplace_ledger_v1` (same) |
| SIGNAL filtering | `detalle IN (signal_list)` | Same |
| op_pnl filter | `COALESCE(include_in_operational_pnl,1)=1` | Same |
| Per-row mode | Single `signal_mode='SIGNAL'` | Two rows per period (SIGNAL + ALL) |
| `total_tesoreria` | Present (misnamed) | Removed (not P&L) |
| `resultado_neto_full` | Separate column | Two rows approach |
| `row_count` | Present | Present + `signal_row_count` |
| `dte_linked_rows` | Present | Present |
| DEC-019 filter | Not applied | Applied via `op_pnl=1` (already handled) |

---

## 5. Query Examples

### Read canonical neto (SIGNAL)
```sql
SELECT signal_resultado_neto 
FROM marketplace_cierre_financiero_v2 
WHERE marketplace='ML' AND periodo_inicio='2026-01-01' AND signal_mode='SIGNAL'
```

### Read legacy-compatible neto (ALL)
```sql
SELECT full_resultado_neto
FROM marketplace_cierre_financiero_v2
WHERE marketplace='ML' AND periodo_inicio='2026-01-01' AND signal_mode='ALL'
```

### Latest period (replaces MAX(periodo_inicio) pattern)
```sql
SELECT MAX(periodo_inicio) 
FROM marketplace_cierre_financiero_v2 
WHERE signal_mode='SIGNAL'
```

---

## 6. Expected Data Changes

Based on experimental v2 results (extrapolated to proposed schema):

| MP | Current v1 (ALL) | v2 SIGNAL | v2 ALL | Delta SIGNAL |
|---|-----------------|-----------|--------|-------------|
| RIPLEY | ~$482M | ~$519M | ~$1,673M | **+$37M** (vs non-zero periods) |
| PARIS | ~$387M | ~$337M | ~$337M | **-$50M** |
| ML | ~$582M | ~$583M | ~$583M | **+$1M** |
| FALABELLA | ~$15M | ~$8M | ~$8M | **-$7M** |

**Note:** These deltas will SUBSTANTIALLY change certification contracts. All existing certifications must be re-run.
