# P32R10 — SQL TRACE

## Consultas Eliminadas

### Pre-Fix: `get_executive_breakdown()` — 10 consultas

```sql
-- Q1: Neto total (ALL)
SELECT COALESCE(SUM(monto), 0) as neto FROM marketplace_ledger_v1 WHERE {where}

-- Q2: Per-group breakdown (ALL) 
SELECT COALESCE(SUM(CASE ...)) as gross_sales, ... FROM marketplace_ledger_v1 WHERE {where}

-- [LOOP x4 MPs]
-- Q3-Q10: 2 queries per MP (neto + per-group)
```

### Post-Fix: `get_executive_breakdown()` — 1 consulta

```sql
-- Q1: GROUP BY (ALL MPs + breakdown in 1 query)
SELECT LOWER(marketplace) as mp, 
  COALESCE(SUM(monto), 0) as neto,
  COALESCE(SUM(CASE WHEN financial_group='ingresos' ...), 0) as gross, ...
FROM marketplace_ledger_v1 WHERE {where}
GROUP BY LOWER(marketplace)
```

### Pre-Fix: `get_risk_summary()` — 4 SQL + file I/O

```sql
-- + glob + pd.read_excel + pd.read_csv for RIPLEY/FALABELLA files
SELECT ... FROM marketplace_ledger_v1 LEFT JOIN document_match_v1 ... -- FULL SCAN
```

### Post-Fix: `get_risk_summary()` — 2 consultas SQL (sin file I/O)

```sql
-- Q1: Risk counts
SELECT 
  COALESCE(SUM(CASE WHEN (folio_xml IS NULL ...) AND financial_group IN ('costos_comerciales','costos_operacionales','ajustes') THEN 1 ELSE 0 END), 0) as xml_missing,
  ...
FROM marketplace_ledger_v1 WHERE {where}

-- Q2: Top XML_MISSING groups  
SELECT financial_group, COUNT(*) as cnt
FROM marketplace_ledger_v1 WHERE (folio_xml IS NULL ...) 
  AND financial_group IN ('costos_comerciales','costos_operacionales','ajustes')
GROUP BY financial_group ORDER BY cnt DESC LIMIT 2
```

### Pre-Fix: `exec/summary` — 2x `get_all_certifications()`

```python
# Llamada 1: get_coverage_summary() -> get_all_certifications()  [4 queries]
# Llamada 2: get_risk_summary() -> get_all_certifications()      [4 queries DUPLICADAS]
```

### Post-Fix: `exec/summary` — 0 `get_all_certifications()`

```python
# No se llama get_all_certifications(). Se pasa certifications={}
```

## Resumen

| Métrica | Pre-Fix | Post-Fix | Mejora |
|---------|---------|----------|--------|
| Consultas SQL en exec/summary | ~18 | ~4 | 78% |
| Archivos leídos desde disco | ~50+ (Excel/CSV) | 0 | 100% |
| Lecturas JSON taxonomía | 5+ | 1 (cached) | 80% |
| Duplicación de certificaciones | 2× | 0× | 100% |
