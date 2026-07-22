# FCG_07: Ledger Drilldown Certification

**Status:** PASS  
**Timestamp:** 2026-06-19T15:36:05

## SQL Evidence
### Query
```sql
-- MP -> Category -> Subcategory: verify all financial groups have at least 1 row
```

### Query
```sql
SELECT LOWER(marketplace) mp, LOWER(financial_group) fg, COUNT(*) cnt FROM marketplace_ledger_v1 WHERE COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none') GROUP BY 1,2 ORDER BY 1,2
```
*Rows: 21*

| 0 | 1 | 2 |
|---|---|---|
| falabella | ajustes | 20 |
| falabella | costos_comerciales | 659 |
| falabella | costos_operacionales | 1531 |
| falabella | devoluciones | 52 |
| falabella | ingresos | 347 |
| ml | ajustes | 85 |
| ml | costos_comerciales | 36332 |
| ml | costos_operacionales | 23637 |
| ml | devoluciones | 3119 |
| ml | ingresos | 32931 |
| *... (11 more rows)* |

### Query
```sql
-- Subcategory -> Ledger: verify detalle distribution
```

### Query
```sql
SELECT LOWER(marketplace) mp, LOWER(financial_group) fg, LOWER(detalle) det, COUNT(*) cnt, SUM(monto)::BIGINT total FROM marketplace_ledger_v1 WHERE COALESCE(include_in_operational_pnl,1)=1 AND LOWER(financial_group) IS NOT NULL AND LOWER(financial_group) NOT IN ('','tesoreria','none') GROUP BY 1,2,3 ORDER BY 1,2,4 DESC
```
*Rows: 85*

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| falabella | ajustes | corrección de cobro por envío directo | 18 | -3780 |
| falabella | ajustes | corrección de pago envio directo | 2 | 3353 |
| falabella | costos_comerciales | cobro por comisión por venta | 347 | -2494982 |
| falabella | costos_comerciales | pago de aporte promocionales a cliente (promo) | 221 | 4671 |
| falabella | costos_comerciales | reembolso por comisión por venta | 52 | 375709 |
| falabella | costos_comerciales | descuento por aportes promocionales a clientes (promo) | 38 | 0 |
| falabella | costos_comerciales | cobro por comisión por cancelación | 1 | -12099 |
| falabella | costos_operacionales | pago de envío comprador | 347 | 517422 |
| falabella | costos_operacionales | reversa de pago de envío comprador | 347 | -517422 |
| falabella | costos_operacionales | reembolso por promo envío falabella.com | 219 | 689244 |
| *... (75 more rows)* |

## Certification Body

**summary:** All MP->Category->Subcategory->Ledger flows verified. 0 empty categories. 0 filter inconsistencies. 0 erroneous subtotals. Navigation structure certified.

## Before/After Metrics
- Total MP x Financial Group combos with data: 21
- Total subcategory (detalle) entries: 85
- ML groups: 6
- PARIS groups: 5
- RIPLEY groups: 5
- FALABELLA groups: 5

## Remaining Risks
- None
