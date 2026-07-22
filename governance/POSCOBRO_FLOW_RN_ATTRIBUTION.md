# POSCOBRO FLOW → RN ATTRIBUTION

**Fecha:** 2026-06-07
**Prioridad:** CRÍTICA
**Objetivo:** Determinar exactamente qué parte de PosCobro impacta el RN por FLOW, resolviendo la contradicción entre DELETE vs MIXED.

---

## RESUMEN EJECUTIVO

**Veredicto: POSCOBRO_SAFE_TO_DELETE = NO** (solo parcialmente)

| FLOW | RN Impact | Paired (Eliminable) | Exclusive (No Eliminar) | Eliminable |
|---|---|---|---|---|
| claim | $169,843,875 | $86,622,511 (51%) | $83,221,364 (49%) | PARCIAL |
| refund | $4,659,383 | $4,071,553 (87%) | $587,830 (13%) | PARCIAL |
| chargeback | $100,970 | $21,990 (22%) | $78,980 (78%) | PARCIAL |
| unmatched | $10,096,682 | — | — | NO |
| **TOTAL** | **$184,700,910** | **$90,716,054 (49%)** | **$83,888,174 (45%)** | — |

**Contradicción resuelta:**
- DEC-009 (DELETE) tenía razón en que **~49% es duplicativo** — paired con devoluciones, $0 cash.
- AJUSTES_RETENCIONES_FINANCIAL_DESTINY (MIXED) tenía razón en que **~45% es exclusivo** — datos financieros genuinos sin representación en devoluciones.

---

## FASE 1 — DESGLOSE FLOW

### 1A. Raw Files (11,914 rows, $338M)

Recuperamos el `flow` column desde los 5 XLSX raw en `01_Raw/ML/Poscobro/`:

| FLOW | Raw Rows | % Rows | Raw Operation Amount | % Amount |
|---|---|---|---|---|
| claim | 6,158 | 51.7% | $183,063,202 | 54.1% |
| refund | 5,749 | 48.2% | $154,945,449 | 45.8% |
| chargeback | 7 | 0.06% | $212,930 | 0.06% |
| **TOTAL** | **11,914** | **100%** | **$338,221,581** | **100%** |

**Nota:** No existe `cashback` como flow en ningún archivo raw.

### 1B. Ledger PosCobro (6,655 rows, $184.7M)

Los rows que efectivamente entran al ledger (con `financial_group='ajustes'`) son menos que raw por: (1) dedup por `(operation_id, detalle, monto, fecha)`, (2) filtro `_filter_old_years()` (pre-2025), (3) solo eventos que resultaron en ajuste real.

| Métrica | Valor |
|---|---|
| Total ledger rows (POS_% + op_pnl=1) | 6,655 |
| Total ledger monto | $184,700,910 |
| Archivos origen | 5 XLSX (ene 2025 — jun 2026) |
| 100% clasificado como | `financial_group='ajustes'` |

---

## FASE 2 — ATRIBUCIÓN RN POR FLOW

### Matching: Raw Flow → Ledger Rows

Método exacto: (1) agregar raw por `operation_id` (6,514 únicos), (2) matchear 1:1 contra `id_transaccion` del ledger que contiene `POS_{operation_id}_{file}_{idx}`.

**Match rate:** 6,315/6,514 (96.9%) — 199 operation_ids unmatched ($4.6M, mayormente refund sin claim previo).

### FLOW → RN Attribution

| FLOW | Ledger Rows | RN Impact | % of Total |
|---|---|---|---|
| claim | 5,615 | $169,843,875 | 92.0% |
| refund | 697 | $4,659,383 | 2.5% |
| chargeback | 3 | $100,970 | 0.05% |
| unmatched (raw) | 340 | $10,096,682 | 5.5% |
| **TOTAL** | **6,655** | **$184,700,910** | **100%** |

### ¿Por qué claim domina (92%) vs refund raw (45.8%)?

Porque en el archivo raw, una misma `operation_id` tiene MÚLTIPLES estados:
1. `flow='claim'` (cuando el reclamo se abre)
2. `flow='refund'` (cuando se resuelve)

Ambos copias del mismo evento. El loader procesa archivos en orden cronológico y deduplica por `(operation_id, detalle, monto, fecha)`. El **claim** queda, el **refund** se descarta como duplicado.

**Conclusión:** El flow del raw NO determina el flow en el ledger. Lo que determina la permanencia es el orden de procesamiento.

### Paired vs Exclusive por FLOW

| FLOW | Total | Paired (con dev) | Exclusive (sin dev) | % Paired |
|---|---|---|---|---|
| claim | $169,843,875 | $86,622,511 | $83,221,364 | 51.0% |
| refund | $4,659,383 | $4,071,553 | $587,830 | 87.4% |
| chargeback | $100,970 | $21,990 | $78,980 | 21.8% |
| unmatched | $10,096,682 | — | — | — |
| **TOTAL** | **$184,700,910** | **$90,716,054** | **$83,888,174** | **~49%** |

---

## FASE 3 — ATRIBUCIÓN CONCEPTO × FLOW

| Concepto | FLOW | Total | Paired | Exclusive | % Paired |
|---|---|---|---|---|---|
| bigger_than_expected_fashion | ALL | $55,919,549 | $27,708,313 | $28,211,236 | 49.6% |
| smaller_than_expected_fashion | ALL | $43,091,674 | $19,884,487 | $23,207,187 | 46.1% |
| repentant_buyer | ALL | $18,135,631 | $7,418,787 | $10,716,844 | 40.9% |
| dont_want_it_another_cause_fashion | ALL | $14,911,545 | $6,407,131 | $8,504,414 | 43.0% |
| undelivered_repentant_buyer | ALL | $10,450,267 | $9,518,055 | $932,212 | **91.1%** |
| different_color_or_size_fashion | ALL | $5,387,142 | $2,391,630 | $2,995,512 | 44.4% |
| undelivered_other | ALL | $3,990,515 | $3,581,465 | $409,050 | **89.7%** |
| item_not_useful_fashion_different_change | ALL | $3,215,655 | $1,843,504 | $1,372,151 | 57.3% |
| broken_item_fashion | ALL | $2,788,219 | $1,299,229 | $1,488,990 | 46.6% |
| Ajuste Poscobro | ALL | $2,724,418 | $2,341,348 | $383,070 | **85.9%** |
| not_match_size_guide_fashion | ALL | $2,692,880 | $1,315,808 | $1,377,072 | 48.9% |
| compensated | ALL | $2,229,195 | $1,681,924 | $547,271 | 75.5% |
| estimated_delivery_out_of_time | ALL | $1,922,567 | $1,736,436 | $186,131 | **90.3%** |
| different_than_published | ALL | $1,431,560 | $584,820 | $846,740 | 40.9% |
| otros (15+ concepts) | ALL | $16,010,394 | $7,423,840 | $8,586,554 | 46.4% |

**Patrón:** Conceptos de "Talla/Garantía" (bigger_than_expected, smaller_than_expected) tienen ~50/50 paired/exclusive. Conceptos de "Logística/Entrega" (undelivered_repentant_buyer, estimated_delivery_out_of_time) tienen >89% paired (casi siempre hay devolución asociada).

---

## FASE 4 — CASHBACK + ESPECIALES

| Término | En Raw | En Ledger | Impacto RN |
|---|---|---|---|
| `cashback` | NO existe como flow | 0 rows | $0 |
| `reserve_for_dispute` | NO existe como flow | 0 rows | $0 |
| `bpp_refunded` | NO existe como flow | 0 rows | $0 |
| `reconciled` | NO existe como flow | 13 rows, $497,870 | $497,870 |
| `bpp` | NO existe como flow | 0 rows | $0 |

**Cashback no es un flow independiente en PosCobro.** Los 13 rows `reconciled` ($497K) son inmateriales (<0.3% del total PosCobro).

### CASH VALIDATION — Paired PosCobro

| Métrica | Valor |
|---|---|
| Paired orders (ajustes + devoluciones misma orden) | 2,821 |
| Paired ajustes total | **$94,357,912** |
| Cash real (Liberaciones) | **$0.00** |
| Cash ratio | **0.0%** |

**El paired PosCobro es 100% ruido contable.** $94.4M en ajustes apareados con devoluciones en la misma orden genera $0 cash real. Confirmación directa del análisis SALE_TO_BANK_TRUTH y RFC_CASH_CERTIFICATION.

---

## FASE 5 — DECISIÓN FINAL

### Tabla de Decisión

| FLOW | RN Impact | ¿Eliminable? | Condición |
|---|---|---|---|
| **claim paired** | $86,622,511 | **SI** ✅ | $0 cash, duplicativo con devoluciones |
| **claim exclusive** | $83,221,364 | **NO** ❌ | Datos financieros genuinos sin devolución asociada |
| **refund paired** | $4,071,553 | **SI** ✅ | $0 cash, duplicativo |
| **refund exclusive** | $587,830 | **NO** ❌ | Genuino sin devolución |
| **chargeback** | $100,970 | — | Inmaterial (0.05%) |
| **unmatched** | $10,096,682 | **NO** ❌ | Sin fuente confirmada |
| **TOTAL ELIMINABLE** | **$90,716,054 (49%)** | SI | Con corrección de RN |
| **TOTAL NO ELIMINABLE** | **$83,888,174 (45%)** | NO | Datos financieros exclusivos |

### Contradicción Resuelta

| Certificación | Anterior | Nueva | Resolución |
|---|---|---|---|
| POSCOBRO_DELETION (DEC-009) | DELETE (99.77% redundante) | **DELETE PARCIAL (~49%)** | DEC-009 sobrestimó la redundancia. Solo el paired es eliminable |
| AJUSTES_RETENCIONES_FINANCIAL_DESTINY | MIXED (50/50) | **MIXED** confirmado | 49% paired (corrección RN), 51% exclusivo (datos genuinos) |
| POSCOBRO_FLOW_FINANCIAL_TRUTH | 100% Ajustes (correcto) | **MANTENIDO** | Flow no cambia la clasificación financiera |

### Flujo Recomendado

```
PosCobro (6,655 rows, $184.7M)
├── Paired (3,663 rows, $90.7M) → ELIMINABLE
│   ├── claim: $86.6M
│   └── refund: $4.1M
│   └── chargeback: $22K
│
└── Exclusive (2,641 rows, $83.9M) → PRESERVAR en ledger
    ├── claim: $83.2M
    ├── refund: $0.6M
    └── chargeback: $79K

    └── Unmatched (~340 rows, $10.1M) → INVESTIGAR
        (raw operation_ids sin match en ledger)
```

### Impacto RN por Escenario

| Escenario | RN Impacto | RN Post |
|---|---|---|
| **ML RN actual** | — | **$712,045,126** |
| **S1: Eliminar Solo Paired** | -$90,716,054 | $621,329,072 |
| **S2: Eliminar Solo Exclusive** | -$83,888,174 | $628,156,952 |
| **S3: Eliminar Todo PosCobro** | -$184,700,910 | $527,344,216 |
| **S4: Eliminar Paired + Dejar Exclusive** | **-$90,716,054** | **$621,329,072** (RECOMENDADO) |

---

## VEREDICTO FINAL

### POSCOBRO_SAFE_TO_DELETE = NO

**No es seguro eliminar el 100% de PosCobro.** El 49% paired ($90.7M) sí puede eliminarse (corrige sobrestimación de RN sin impacto cash). El 45% exclusive ($83.9M) NO puede eliminarse sin perder datos financieros genuinos.

**Acción recomendada:**
1. ✅ **Eliminar paired PosCobro** — $90.7M, $0 cash, corrige RN
2. ❌ **Preservar exclusive PosCobro** — $83.9M, datos financieros genuinos
3. ❌ **Investigar unmatched** antes de cualquier acción adicional

**Condiciones originales de DEC-009 re-evaluadas:**

| Condición | Estado |
|---|---|
| Preservar raw files | ✅ Válida |
| Snapshots pre-deletion | ✅ Válida |
| Mantener granularidad operacional | ✅ Válida |
| Re-clasificar ML | ⚠️ No necesaria si solo se elimina paired |
| **DEC-009 corrección:** | DELETE → DELETE PARCIAL (49%) |
