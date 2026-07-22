# Reconciliation Engine V1 — Evidence Report

## Period: 2026-01 (Enero 2026)
## Engine Version: 1.0.0

---

## 1. Executive Summary

| MP | Status | Delta | Taxonomy | Document | Records | Alerts |
|----|--------|-------|----------|----------|---------|--------|
| ML | FINANCIAL_INTEGRITY_BROKEN | $45,356,985 | 100.0% | 0.0% | 8,191 | 7 |
| PARIS | FINANCIAL_INTEGRITY_BROKEN | $8,460,850 | 100.0% | 0.0% | 1,983 | 5 |
| RIPLEY | FINANCIAL_INTEGRITY_BROKEN | $117,232,828 | 100.0% | 0.0% | 8,672 | 13 |
| FALABELLA | PENDIENTE | $0 | 100.0% | 0.0% | 0 | 1 |

## 2. Per-Marketplace Detail

### ML — Ene 2026

| Level | Status | Delta | Source | Target |
|-------|--------|-------|--------|--------|
| INTERNA | ALERTA | $4,971,696 | $41,587,389 | $36,615,693 |
| OPERACIONAL | ALERTA | $10,168,790 | $12,730,978 | $22,899,768 |
| TESORERÍA | ALERTA | $30,216,500 | $17,485,522 | -$12,730,978 |
| DOCUMENTAL | ALERTA | 100.0% | 0 | 8,191 |

**7 alerts** — All levels report deltas, consistent with the known structural
discrepancy between cierre formula and flat ledger sum. Document coverage is 0%
because document_match_v1 lacks records for this period.

### PARIS — Ene 2026

| Level | Status | Delta | Source | Target |
|-------|--------|-------|--------|--------|
| INTERNA | ALERTA | $2,996,517 | $5,464,333 | $8,460,850 |
| OPERACIONAL | PASS | $0 | $5,464,333 | $5,464,333 |
| TESORERÍA | ALERTA | $5,464,333 | $0 | -$5,464,333 |
| DOCUMENTAL | ALERTA | 100.0% | 0 | 1,983 |

**5 alerts** — Operational P&L matches resultado_neto perfectly (PASS).
Internal delta and treasury delta are structural. Document coverage 0% same as ML.

### RIPLEY — Ene 2026

| Level | Status | Delta | Source | Target |
|-------|--------|-------|--------|--------|
| INTERNA | ALERTA | $9,930,630 | $56,656,130 | $66,586,760 |
| OPERACIONAL | ALERTA | $50,646,068 | $56,656,130 | $107,302,198 |
| TESORERÍA | ALERTA | $56,656,130 | $0 | -$56,656,130 |
| DOCUMENTAL | ALERTA | 100.0% | 0 | 8,672 |

**13 alerts** — RIPLEY has the largest deltas. Multiple internal groups mismatch.
Operational P&L ≠ resultado_neto. Treasury = $0 (no tesoreria records for this
period). Document coverage 0%.

### FALABELLA — Ene 2026

| Level | Status | Delta | Source | Target |
|-------|--------|-------|--------|--------|
| INTERNA | PASS | $0 | $0 | $0 |
| OPERACIONAL | PASS | $0 | $0 | $0 |
| TESORERÍA | PASS | $0 | $0 | $0 |
| DOCUMENTAL | ALERTA | 100.0% | 0 | 0 |

**1 alert** — No data for 2026-01 (last available data is Apr 2026).
All levels correctly report zero. PENDIENTE status is correct.

## 3. Alert Sample (ML)

| Rule | Impact | Records | Evidence |
|------|--------|---------|----------|
| UNEXPECTED_GROUP:devoluciones | $0.00 | 1 | Group not in cierre |
| UNEXPECTED_GROUP:impuestos | $18,156 | 1 | Group not in cierre |
| GROUP_MISMATCH:ingresos | $343,791 | - | clasificado vs cierre delta |
| GROUP_MISMATCH:costos_operacionales | $1,379,699 | - | clasificado vs cierre delta |
| GROUP_MISMATCH:ajustes | $4,088,136 | - | clasificado vs cierre delta |
| OP_PNL_VS_RESULTADO_NETO | $10,168,790 | 8191 | operational vs resultado_neto |
| PNL_TREASURY_MISMATCH | $30,216,500 | 596 | op+tr ≠ 0 |
| INSUFFICIENT_DOCUMENT_COVERAGE | 8191 | 8191 | 0.0% coverage |

## 4. Metrics Validation

### taxonomy_coverage

| MP | Coverage | Status |
|----|----------|--------|
| ML | 100.0% | ✅ |
| PARIS | 100.0% | ✅ |
| RIPLEY | 100.0% | ✅ |
| FALABELLA | 100.0% | ✅ |

All marketplaces have 100% taxonomy coverage — every record has a `financial_group`.

### document_coverage

| MP | Coverage | Status |
|----|----------|--------|
| ML | 0.0% | ⚠️ |
| PARIS | 0.0% | ⚠️ |
| RIPLEY | 0.0% | ⚠️ |
| FALABELLA | 0.0% | ⚠️ |

0% coverage across all MPs — `document_match_v1` table lacks records for 2026-01.
This is a data ingestion gap, not an engine bug.

### orphan_records

| MP | Orphans | Detail |
|----|---------|--------|
| ML | 8,191 | All records unmatched in document_match_v1 |
| PARIS | 1,983 | All records unmatched |
| RIPLEY | 8,672 | All records unmatched |
| FALABELLA | 0 | No records to compare |

## 5. Data Freshness Note

This evidence report uses 2026-01 as the test period. All 4 MPs have data for this
period except FALABELLA (last data Apr 2026). The engine handles this gracefully
with PENDIENTE status and zero deltas.

## 6. SQL Evidence Queries

All alerts include the full SQL query that generated the alert. Key queries:

**Level 1 — Internal reconciliation:**
```sql
SELECT COALESCE(financial_group, 'sin_clasificar') as financial_group,
       SUM(COALESCE(monto, 0)) as total
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = ? AND fecha >= ? {date_end}
GROUP BY financial_group ORDER BY financial_group
```

**Level 2 — Operational P&L:**
```sql
SELECT SUM(COALESCE(monto, 0)) as total
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = ? AND fecha >= ? {date_end}
  AND COALESCE(include_in_operational_pnl, 1) = 1
```

**Level 3 — Treasury:**
```sql
SELECT SUM(COALESCE(monto, 0)) as total
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = ? AND fecha >= ? {date_end}
  AND financial_group IN ('tesoreria')
```

**Level 4 — Documentary coverage:**
```sql
SELECT COUNT(DISTINCT c.id_transaccion) as matched
FROM marketplace_ledger_clasificado_v1 c
INNER JOIN document_match_v1 d
    ON c.marketplace = d.marketplace
    AND c.id_transaccion = d.ledger_id
WHERE c.marketplace = ? AND c.fecha >= ? {date_end}
  AND d.match_status = 'CONCILIATED'
```
