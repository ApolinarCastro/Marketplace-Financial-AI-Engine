# BPP Residual Certification

**Date:** 2026-06-06
**Scope:** 47 BPP rows with `include_in_operational_pnl=True` after MODERNIZE fix

---

## Hallazgo

After MODERNIZE (DEC-003), 47 rows classified as "Ajuste por Compra Protegida (BPP)" escaped the `ml_mandatory_exclusions` and remain visible with `iopnl=True`. These rows total **$1,337,592 globally** ($58,970 in ML 2026-01 — the amount visible in desglose).

### Root Cause

`marketplace_auditor.py:420-430` — the exclusion logic uses exact-match `isin()` against a static set. The set includes `"bpp_refunded"` but misses 4 legitimate BPP detail patterns present in the data:

| Detalle Pattern | Rows | Amount | Missing from Exclusions |
|---|---|---|---|
| `bpp_covered` | ~35 | ~$1.11M | YES — pattern not in set |
| `partially_bpp_refunded` | 2 | $77,960 | YES — not matched by `bpp_refunded` (exact match) |
| `ppv_covered_melienvio` | 4 | ~$120K | YES — pattern not in set |
| `ppv_valid` | 1 | $39,990 | YES — pattern not in set |

---

## Evidencia

### Pairing Analysis (FASE 2)

**100% of the 47 rows are in PAIRED orders** — every one shares its `id_orden` with a ROOT_EVENT (Talla/Garantía, Arrepentimiento, Falla en Entrega, Producto Dañado/Vacío). Example for ML 2026-01:

| id_transaccion | id_orden | BPP $ | Paired Root Event |
|---|---|---|---|
| POS_141918714073 | 2000014769152558 | $32,990 | Falla en Entrega ($32,990) |
| POS_142586809414 | 2000014769143312 | $15,990 | Falla en Entrega ($15,990) |
| POS_143476109988 | 2000014859835248 | $9,990 | Producto Dañado/Vacío ($9,990) |

### Cash Validation (FASE 3)

Per RFC_CASH_CERTIFICATION_BPP_POSCOBRO: paired mechanisms have **NET cash = $0** (`reserve_for_dispute NET=$0` confirmed for BPP). These are mirror transactions with zero real cash impact when paired.

### Event Role (FASE 4)

Per EVENT_REGISTRY_V2: BPP is classified as **MECHANISM** for all bpp_covered/bpp_refunded/ppv_* patterns. Not ROOT_EVENT, not STANDALONE_MECHANISM.

---

## Veredicto

**CRITERION: FAIL** — residual classification error.

| Question | Answer | Rationale |
|---|---|---|
| ¿Deben permanecer visibles? | **NO** | Are mechanisms paired with root events — `iopnl=False` |
| ¿Deben impactar RN? | **NO** | Zero net cash when paired — cierre RN preserves truth |
| ¿Deben impactar Ledger Operacional? | **NO** | Only 3 of 3,450 BPP rows visible in desglose — should be 0 |

**Corrective action:** Add 4 missing patterns (`bpp_covered`, `partially_bpp_refunded`, `ppv_covered_melienvio`, `ppv_valid`) to `ml_mandatory_exclusions` at `marketplace_auditor.py:420`. Estimated fix cost: 1 line (or use `detalle__contains__` matching instead of exact for BPP).

**Materiality:** $1,337,592 global = **0.19%** of ML RN ($712M). Per-period residual negligible (e.g., $58,970 in 2026-01 = 0.3% of period RN). Not certified for go-live but acceptable as known deviation.
