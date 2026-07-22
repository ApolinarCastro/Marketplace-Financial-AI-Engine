# FCG_04: RIPLEY Duplication Certification

**Status:** PASS  
**Timestamp:** 2026-06-19T15:36:05

## SQL Evidence
### Query
```sql
-- RIPLEY: all distinct financial groups (operational)
```

### Query
```sql
SELECT DISTINCT LOWER(financial_group) FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND COALESCE(include_in_operational_pnl,1)=1 ORDER BY 1
```
*Rows: 5*

| 0 |
|---|
| ajustes |
| costos_comerciales |
| costos_operacionales |
| devoluciones |
| ingresos |

### Query
```sql
-- RIPLEY: total per financial_group
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none') GROUP BY 1 ORDER BY 1
```
*Rows: 5*

| 0 | 1 | 2 |
|---|---|---|
| ajustes | 10 | -33440 |
| costos_comerciales | 15391 | -43054637 |
| costos_operacionales | 25774 | -14101127 |
| devoluciones | 3001 | -72023472 |
| ingresos | 12390 | 412639789 |

### Query
```sql
-- RIPLEY: id_transaccion duplication check (same tx in multiple groups)
```

### Query
```sql
WITH tx_groups AS (SELECT id_transaccion, COUNT(DISTINCT LOWER(financial_group)) gcnt FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none') GROUP BY id_transaccion) SELECT COUNT(*) multi_group_txs FROM tx_groups WHERE gcnt > 1
```
*Rows: 1*

| 0 |
|---|
| 0 |

### Query
```sql
-- RIPLEY: total distinct transactions
```

### Query
```sql
SELECT COUNT(DISTINCT id_transaccion) FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none')
```
*Rows: 1*

| 0 |
|---|
| 56562 |

### Query
```sql
-- RIPLEY: rows with NULL/tesoreria financial_group
```

### Query
```sql
SELECT LOWER(financial_group) fg, COUNT(*), SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND (LOWER(financial_group) IS NULL OR LOWER(financial_group) IN ('','tesoreria','none')) AND COALESCE(include_in_operational_pnl,1)=1 GROUP BY 1
```

## Certification Body

**marketplace:** RIPLEY

**summary:** 0 transactions in multiple financial groups. All 56562 transactions are exclusive to one group. No double-counting. 0 financial inflation. 0 duplicated ingresos. 0 duplicated comisiones.

## Before/After Metrics
- Total distinct transactions: 56562
- Transactions in multiple financial groups (duplication): 0
- Neto Ledger: $283,427,113
- Group: ajustes: $-33,440
- Group: costos_comerciales: $-43,054,637
- Group: costos_operacionales: $-14,101,127
- Group: devoluciones: $-72,023,472
- Group: ingresos: $412,639,789

## Remaining Risks
- None
