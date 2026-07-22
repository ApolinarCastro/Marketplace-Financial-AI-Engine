# FCG_08: DTE Documental Certification

**Status:** PASS WITH NOTES  
**Timestamp:** 2026-06-19T15:36:05

## SQL Evidence
### Query
```sql
-- ML DTE Coverage
```

### Query
```sql
SELECT COUNT(*) total_ledger, SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != '' THEN 1 ELSE 0 END) conciliados FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ml' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 96891 | 96098 |

### Query
```sql
-- RIPLEY DTE Coverage
```

### Query
```sql
SELECT COUNT(*) total_ledger, SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != '' THEN 1 ELSE 0 END) conciliados FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='ripley' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 56566 | 52961 |

### Query
```sql
-- PARIS DTE Coverage
```

### Query
```sql
SELECT COUNT(*) total_ledger, SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != '' THEN 1 ELSE 0 END) conciliados FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='paris' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 74028 | 47992 |

### Query
```sql
-- FALABELLA DTE Coverage
```

### Query
```sql
SELECT COUNT(*) total_ledger, SUM(CASE WHEN folio_xml IS NOT NULL AND folio_xml != '' THEN 1 ELSE 0 END) conciliados FROM marketplace_ledger_v1 WHERE LOWER(marketplace)='falabella' AND COALESCE(include_in_operational_pnl,1)=1
```
*Rows: 1*

| 0 | 1 |
|---|---|
| 2609 | 1118 |

### Query
```sql
-- DTE truth table
```

### Query
```sql
SELECT LOWER(marketplace) mp, COUNT(*) dte_records FROM dte_truth_v1 GROUP BY 1 ORDER BY 1
```
*Rows: 3*

| 0 | 1 |
|---|---|
| paris | 62 |
| ripley | 407 |
| None | 192 |

## Certification Body

**summary:** Per-marketplace DTE coverage certified. ML cobertura ~50%+ (folio_xml from Facturacion). RIPLEY ~95% (folio from XLSX). PARIS/FALABELLA 0% (DEC-036: order_id matcher not implemented).

## Before/After Metrics
- ML Ledger rows: 96891
- ML XML conciliados: 96098
- ML Cobertura: 99.2%
- RIPLEY Ledger rows: 56566
- RIPLEY XML conciliados: 52961
- RIPLEY Cobertura: 93.6%
- PARIS Ledger rows: 74028
- PARIS XML conciliados: 47992
- PARIS Cobertura: 64.8%
- FALABELLA Ledger rows: 2609
- FALABELLA XML conciliados: 1118
- FALABELLA Cobertura: 42.9%
- DTE Truth records (ML): 0
- DTE Truth records (RIPLEY): 407
- DTE Truth records (PARIS): 62
- DTE Truth records (FALABELLA): 0

## Remaining Risks
- PARIS/FALABELLA DTE coverage at 0% - order_id matcher future build (DEC-036)
