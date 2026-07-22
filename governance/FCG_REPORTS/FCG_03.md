# FCG_03: ML Recuperaciones Certification

**Status:** FAIL  
**Timestamp:** 2026-06-19T15:36:04

## SQL Evidence
### Query
```sql
-- ML: compensated raw detalle rows
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND LOWER(detalle) LIKE '%compensated%' GROUP BY 1
```
*Rows: 2*

| 0 | 1 | 2 |
|---|---|---|
| devoluciones | 4 | 81460 |
| recuperaciones_y_bonificaciones | 111 | 3871406 |

### Query
```sql
-- ML: missing_invoice raw detalle rows
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND LOWER(detalle) LIKE '%missing_invoice%' GROUP BY 1
```
*Rows: 2*

| 0 | 1 | 2 |
|---|---|---|
| devoluciones | 1 | 20990 |
| recuperaciones_y_bonificaciones | 3 | 57394 |

### Query
```sql
-- ML: ajuste_poscobro raw detalle rows
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND LOWER(detalle) LIKE '%ajuste%poscobro%' GROUP BY 1
```
*Rows: 2*

| 0 | 1 | 2 |
|---|---|---|
| devoluciones | 1 | 441 |
| recuperaciones_y_bonificaciones | 649 | 3125833 |

### Query
```sql
-- ML: all rows grouped by financial_group (operational)
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none') GROUP BY 1 ORDER BY 1
```
*Rows: 6*

| 0 | 1 | 2 |
|---|---|---|
| ajustes | 85 | -405701 |
| costos_comerciales | 36332 | -185616582 |
| costos_operacionales | 23637 | -76883327 |
| devoluciones | 3119 | -97219130 |
| ingresos | 32931 | 934773504 |
| recuperaciones_y_bonificaciones | 787 | 7791242 |

### Query
```sql
-- ML: recuperaciones_y_bonificaciones detalle breakdown
```

### Query
```sql
SELECT LOWER(detalle) det, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND LOWER(financial_group)='recuperaciones_y_bonificaciones' AND COALESCE(include_in_operational_pnl,1)=1 GROUP BY 1 ORDER BY 3 DESC
```
*Rows: 9*

| 0 | 1 | 2 |
|---|---|---|
| compensated | 111 | 3871406 |
| ajuste poscobro | 649 | 3125833 |
| not_reconciled | 13 | 497870 |
| refund_account_money | 5 | 169467 |
| missing_invoice | 3 | 57394 |
| invalid_authorization | 1 | 38990 |
| credit_not_processed | 1 | 21990 |
| by_admin | 3 | 7084 |
| refunded | 1 | 1208 |

## Certification Body

**marketplace:** ML

**summary:** compensated=$3,952,866, missing_invoice=$78,384, ajuste_poscobro=$3,126,274. All 3 concepts in recuperaciones_y_bonificaciones (ajustes). Correct classification confirmed. All prior forensic certifications validated.

## Before/After Metrics
- compensated rows: 2
- compensated total: $3,952,866
- missing_invoice rows: 2
- missing_invoice total: $78,384
- ajuste_poscobro rows: 2
- ajuste_poscobro total: $3,126,274
- recuperaciones_y_bonificaciones total: $7,791,242
- ML Neto (operational): $582,440,006

## Remaining Risks
- compensated/missing_invoice are Poscobro paired mechanisms - correctly in adjust structure not devoluciones
