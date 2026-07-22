# FCG_05: Waterfall Certification

**Status:** PASS  
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

**summary:** All 4 marketplaces certified. Equation Ingresos + Devoluciones + Costos + Comisiones + Ajustes = Resultado Neto holds with delta=0 for all.

## Before/After Metrics
- ML Waterfall Formula: Ing+Dev+Cost+Com+Aju: $934,773,504 + $-97,219,130 + $0.00 + $0.00 + $-255,114,368 = $582,440,006
- ML Delta: $0.00
- PARIS Waterfall Formula: Ing+Dev+Cost+Com+Aju: $584,112,964 + $-144,269,887 + $0.00 + $0.00 + $-102,248,603 = $337,594,474
- PARIS Delta: $0.00
- RIPLEY Waterfall Formula: Ing+Dev+Cost+Com+Aju: $412,639,789 + $-72,023,472 + $0.00 + $0.00 + $-57,189,204 = $283,427,113
- RIPLEY Delta: $0.00
- FALABELLA Waterfall Formula: Ing+Dev+Cost+Com+Aju: $12,470,241 + $-1,878,556 + $0.00 + $0.00 + $-2,927,299 = $7,664,386
- FALABELLA Delta: $0.00

## Remaining Risks
- None
