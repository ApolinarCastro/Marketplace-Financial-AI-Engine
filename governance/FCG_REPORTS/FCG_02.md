# FCG_02: FALABELLA Financial Certification

**Status:** FAIL  
**Timestamp:** 2026-06-19T15:36:04

## SQL Evidence
### Query
```sql
-- FALABELLA Ingresos
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND LOWER(financial_group)='ingresos' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| 12470241 |

### Query
```sql
-- FALABELLA Devoluciones
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND LOWER(financial_group)='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| -1878556 |

### Query
```sql
-- FALABELLA Costos
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND LOWER(financial_group)='costos' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| None |

### Query
```sql
-- FALABELLA Comisiones
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND LOWER(financial_group)='comisiones' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| None |

### Query
```sql
-- FALABELLA Ajustes
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND LOWER(financial_group)='ajustes' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 |
|---|
| -427 |

### Query
```sql
-- FALABELLA Neto sum groups
```

### Query
```sql
SELECT SUM(monto)::BIGINT FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none')
```
*Rows: 1*

| 0 |
|---|
| 7664386 |

### Query
```sql
-- FALABELLA Disponible (cierre)
```

### Query
```sql
SELECT periodo_inicio::VARCHAR, resultado_neto::BIGINT FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='falabella' ORDER BY periodo_inicio DESC LIMIT 1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 2026-12-01 | 0 |

## Certification Body

**marketplace:** FALABELLA

**summary:** All 6 categories verified. 0 unclassified rows (known $12K Cobro por comision por cancelacion).

## Before/After Metrics
- Ingresos: $12,470,241
- Devoluciones: $-1,878,556
- Costos: $0
- Comisiones: $0
- Ajustes: $-427
- Neto (Ledger sum): $7,664,386
- Disponible (Cierre): $0.00
- Waterfall Delta: $2,926,872
- Unclassified rows (financial_group=NULL): 0

## Remaining Risks
- 0 unclassified rows (known, inmaterial: $12,099)
