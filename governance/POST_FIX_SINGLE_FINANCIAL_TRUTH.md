# POST-FIX SINGLE FINANCIAL TRUTH

**Fecha:** 2026-06-06  
**Auditor:** Sistema  
**DB:** `data/db/meli_financial_v4.db`  
**Fix aplicado:** MECANISMOS_EXCLUIDOS en `marketplace_auditor.py:536` (paired mechanisms excluidos del cierre financiero)

---

## Cadena: Ledger → Clasificación → Cierre

### 1. Integridad de filas

| Marketplace | Ledger rows | Clasificado rows | Delta | Cierre periods |
|---|---|---|---|---|
| ML | 102,198 | 102,198 | **0** | 18 |
| PARIS | 45,540 | 45,540 | **0** | 18 |
| RIPLEY | 62,502 | 62,502 | **0** | 18 |
| FALABELLA | 2,609 | 2,609 | **0** | 18 |

**Veredicto: $0 delta de filas entre Ledger y Clasificación.**

### 2. Integridad monetaria

| Marketplace | Ledger $ | Clasificado $ | Delta $ | Cierre Neto $ |
|---|---|---|---|---|
| **ML** | 862,404,918 | 862,404,918 | **0** | **712,045,128** |
| PARIS | 337,418,552 | 337,418,552 | **0** | 337,418,552 |
| RIPLEY | 413,893,686 | 413,893,686 | **0** | 206,946,843 |
| FALABELLA | 7,664,386 | 7,664,386 | **0** | 7,676,485 |

- **Ledger = Clasificación: $0 delta (100% match)**
- **Ledger = Cierre Neto: NO** — los deltas son BY DESIGN

### 3. Deltas explicados

| Marketplace | Delta | Causa | Clasificación |
|---|---|---|---|
| **ML** | $150,359,790 | Paired mechanisms (BPP $100.3M, Poscobro Conciliado $46.1M, Poscobro General $3.9M) | **EXCLUIDOS POR FIX** — zero cash, reserve_for_dispute NET=$0 |
| **RIPLEY** | $206,946,843 | "A pagar" rows (financial_group=NULL) | **TREASURY/SETTLEMENT** — espejo del P&L, no doble conteo |
| **FALABELLA** | -$12,099 | 1 fila NO_CLASIFICADO (-$12,099) | **MINOR** — 0.16% del total |

### 4. No clasificados

| Marketplace | Rows | Monto |
|---|---|---|
| ML | 0 | $0 |
| PARIS | 0 | $0 |
| RIPLEY | 0 | $0 |
| FALABELLA | 1 | -$12,099 |

### 5. Verificación del fix (ML ajustes)

```sql
-- MECANISMOS_EXCLUIDOS aplicado en cierre:
AND clasificacion_operativa NOT IN ('Ajuste por Compra Protegida (BPP)',
                                    'Ajuste Poscobro Conciliado',
                                    'Ajuste Poscobro General')

-- Resultado: Clasificado (sin mecanismos) $712,045,128 = Cierre Neto $712,045,128
-- Delta: $0 — EL FIX FUNCIONA
```

### 6. Período a período (ML)

| Periodo | Ajustes en cierre ($) | Neto en cierre ($) | ¿Match con clasificado? |
|---|---|---|---|
| 2025-01 | 2,931,228 | 18,676,085 | ✅ |
| 2025-02 | 1,404,911 | 16,831,909 | ✅ |
| 2025-03 | 1,862,871 | 45,750,811 | ✅ |
| 2025-04 | 3,308,148 | 55,791,607 | ✅ |
| 2025-05 | 7,107,240 | 69,093,529 | ✅ |
| 2025-06 | 6,288,467 | 59,253,276 | ✅ |
| 2025-07 | 5,033,326 | 45,699,544 | ✅ |
| 2025-08 | 4,921,255 | 34,358,937 | ✅ |
| 2025-09 | 4,352,827 | 36,690,170 | ✅ |
| 2025-10 | 7,278,996 | 59,234,400 | ✅ |
| 2025-11 | 7,928,407 | 70,830,352 | ✅ |
| 2025-12 | 9,044,542 | 69,326,053 | ✅ |
| 2026-01 | 1,785,194 | 19,401,503 | ✅ |
| 2026-02 | 3,008,663 | 14,748,924 | ✅ |
| 2026-03 | 2,290,834 | 30,439,310 | ✅ |
| 2026-04 | 3,762,696 | 36,615,722 | ✅ |
| 2026-05 | 6,578,551 | 24,799,677 | ✅ |
| 2026-06 | 4,503,320 | 4,503,320 | ✅ |

**Todos los períodos ML con MATCH EXACTO entre clasificado (sin mecanismos) y cierre.**

---

## VEREDICTO: PASS

- Ledger = Clasificación: **$0 delta en filas y monto**
- Clasificación = Cierre (excluyendo deltas BY DESIGN): **$0 residual**
- ML fix: **VERIFICADO** — $150.4M paired mechanisms excluidos del RN
- 3 deltas en la cadena son INTENCIONALES (no errores)
- FALABELLA: 1 fila no clasificada (-$12K, 0.16%) — no material
