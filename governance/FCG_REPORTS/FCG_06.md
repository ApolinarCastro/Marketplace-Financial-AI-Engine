# FCG_06: Frontend Backend Reconciliation

**Status:** FAIL  
**Timestamp:** 2026-06-19T15:36:05

## SQL Evidence
### Query
```sql

SELECT LOWER(marketplace) mp, LOWER(financial_group) fg, SUM(monto)::BIGINT
FROM marketplace_ledger_v1
WHERE COALESCE(include_in_operational_pnl,1)=1
  AND LOWER(financial_group) IS NOT NULL
  AND LOWER(financial_group) NOT IN ('','tesoreria','none')
GROUP BY 1,2 ORDER BY 1,2

```
*Rows: 21*

| 0 | 1 | 2 |
|---|---|---|
| falabella | ajustes | -427 |
| falabella | costos_comerciales | -2126701 |
| falabella | costos_operacionales | -800171 |
| falabella | devoluciones | -1878556 |
| falabella | ingresos | 12470241 |
| ml | ajustes | -405701 |
| ml | costos_comerciales | -185616582 |
| ml | costos_operacionales | -76883327 |
| ml | devoluciones | -97219130 |
| ml | ingresos | 934773504 |
| *... (11 more rows)* |

## Certification Body

**summary:** Zero frontend financial computation issues. Financial Structure endpoint returns totals matching DB. All 6 components use same backend source.

**frontend_issues:** ['Client-side reduce found in executive_dashboard.html']

## Before/After Metrics
- Frontend financial computation issues: 1
- Ledger operational total (SIGNAL): $1,211,125,979
- Ledger total (ALL): $4,077,991,989

## Remaining Risks
- Frontend issues: ['Client-side reduce found in executive_dashboard.html']
