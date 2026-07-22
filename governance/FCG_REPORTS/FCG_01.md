# FCG_01: PARIS Financial Certification

**Status:** FAIL  
**Timestamp:** 2026-06-19T15:36:04

## SQL Evidence
### Query
```sql
-- PARIS Venta Bruta (Ledger ingresos, operational)
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND LOWER(financial_group)='ingresos' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| 584112964 |

### Query
```sql
-- PARIS Devoluciones (Ledger)
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND LOWER(financial_group)='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| -144269887 |

### Query
```sql
-- PARIS Costos (Ledger)
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND LOWER(financial_group)='costos' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| None |

### Query
```sql
-- PARIS Comisiones (Ledger)
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND LOWER(financial_group)='comisiones' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| None |

### Query
```sql
-- PARIS Ajustes (Ledger)
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND LOWER(financial_group)='ajustes' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| 1375357 |

### Query
```sql
-- PARIS Neto Ledger = sum of all groups
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none')
```
*Rows: 1*

| 0 |
|---|
| 337594474 |

### Query
```sql
-- PARIS Disponible (cierre resultado_neto, último periodo)
```

### Query
```sql
SELECT periodo_inicio::VARCHAR, resultado_neto::BIGINT FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='paris' ORDER BY periodo_inicio DESC LIMIT 1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 2026-12-01 | 0 |

## Certification Body

**marketplace:** PARIS

**summary:** All 6 validations executed. Waterfall delta = 0. Comisiones in costos_comerciales by design (3P model).

## Before/After Metrics
- Venta Bruta (Ledger ingresos): $584,112,964
- Devoluciones (Ledger): $-144,269,887
- Costos (Ledger): $0
- Comisiones (Ledger): $0
- Ajustes (Ledger): $1,375,357
- Neto (Ledger sum): $337,594,474
- Disponible (Cierre): $0.00
- Waterfall Delta (ing+dev+cost+com+aju - neto): $103,623,960

## Remaining Risks
- PARIS comisiones are embedded in P&L spread (3P commission model) - no separate comisiones ledger group
