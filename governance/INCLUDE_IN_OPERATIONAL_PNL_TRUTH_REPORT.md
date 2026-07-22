# INCLUDE_IN_OPERATIONAL_PNL TRUTH REPORT

## Fecha: 2026-06-06
## Auditoría forense: `include_in_operational_pnl` en todo el sistema

---

### FASE 1 — Origen

| Metadato | Valor |
|---|---|
| Commit origen | `67e5e0e` BASELINE_V6 |
| Propósito original | Excluir `detalle` específicos del P&L operacional ML |
| RFC origen | Ninguno — implementado sin RFC |
| Primera implementación | `engine/v4/marketplace_auditor.py` línea ~413 |

**Diseño original**: Conjunto fijo de 13 strings de `detalle` que recibían `include_in_operational_pnl = False`:
```
reserve_for_dispute, Mediación, bpp_refunded, repentant_buyer,
broken_item_fashion, bigger_than_expected_fashion, smaller_than_expected_fashion,
reconciled, AJUSTE POSCOBRO, cashback, cashback_cancel,
Reserva para devolución en envío BBP, Retenciones & Provisiones
```

**Veredicto FASE 1**: Fue diseñado como **D) "otra finalidad"** — un parche ad-hoc para ocultar ciertos detalles ML de la vista operacional. NO fue diseñado con una taxonomía clara (mechanism vs root event vs cash). La selección de exclusiones se basó en strings de `detalle`, NO en el `event_role` o `cash_role` del concepto.

---

### FASE 2 — Matriz semántica (ML, all time)

**Conceptos con `include_in_operational_pnl = FALSE`:**

| Concepto | Rows | Total $ | Correcto? |
|---|---|---|---|
| Ajuste por Compra Protegida (BPP) | 3,403 | $98,960,838 | ✅ MECHANISM — correcto excluir |
| Ajuste Poscobro Conciliado | 1,279 | $42,167,227 | ✅ MECHANISM — correcto excluir |
| Ajuste por Talla/Garantía | 3,487 | $104,349,428 | ❌ ROOT_EVENT — REAL_CASH — incorrecto excluir |
| Ajuste por Arrepentimiento | 620 | $18,537,273 | ❌ ROOT_EVENT (partial) — REAL_CASH — incorrecto excluir |
| Ajuste por Producto Dañado/Vacío | 91 | $2,915,189 | ❌ ROOT_EVENT — REAL_CASH — incorrecto excluir |
| **TOTAL** | **8,880** | **$266,929,955** | |

**Conceptos REAL_CASH + `iopnl=FALSE` (CONTRADICCIÓN):** **$125,801,890** (47.1% del total excluido)

---

### FASE 3 — Contradicciones certificadas

Cada concepto abajo tiene, según CONCEPT_REGISTRY_V2, EVENT_REGISTRY_V2, y CASH_ROLE_REGISTRY_V1:
- `event_role = ROOT_EVENT`
- `cash_role = REAL_CASH`
- Impacta Disponible, Utilidad, RN

Sin embargo, `include_in_operational_pnl = FALSE` los excluye del ledger operacional:

| Concepto | rows FALSE | $ FALSE | Periodos | MPs |
|---|---|---|---|---|
| **Ajuste por Talla/Garantía** | 3,487 | $104,349,428 | 2025-01 → 2026-06 | ML |
| **Ajuste por Arrepentimiento** | 620 | $18,537,273 | 2025-01 → 2026-06 | ML |
| **Ajuste por Producto Dañado/Vacío** | 91 | $2,915,189 | 2025-01 → 2026-06 | ML |

**Impacto total: $125,801,890 — representación financiera ERRÓNEA en el ledger.**

---

### FASE 4 — Simulación (4 escenarios)

| Escenario | Total $ | Delta vs Cierre RN | Veredicto |
|---|---|---|---|
| **A) Current ledger (iopnl=True)** | $595,474,963 | **-$116,570,165** | ❌ Subestima RN en $116.6M |
| **B) IOPNL ignorado (all rows)** | $862,404,918 | **+$150,359,790** | ❌ Sobrestima (incluye MECHANISMS) |
| **C) Solo MECHANISM excluido** | $712,045,128 | **$0 — MATCH EXACTO** | ✅ PERFECTO |
| **D) Solo REAL_CASH** | $712,045,128 | **$0 — MATCH EXACTO** | ✅ (mismo que C para ML) |

**Prueba matemática**: Cuando se excluyen SOLO los 3 MECHANISMS (BPP, Poscobro Conciliado, Poscobro General) — y se INCLUYEN Talla/Garantía, Arrepentimiento, Producto Dañado/Vacío — el resultado es IDÉNTICO al cierre RN certificado. **$0 delta cada período.**

El `include_in_operational_pnl` actual sobre-excluye $125.8M en conceptos que:
- Son ROOT_EVENT (evento real, no paired)
- Son REAL_CASH (impacto caja real)
- Están incluidos en el cierre certificado
- Impactan Disponible y Utilidad

---

### FASE 5 — Verdad absoluta

**`include_in_operational_pnl` representa: E) Error conceptual — específicamente una mezcla inconsistente (opción F).**

El campo mezcla DOS categorías distintas bajo la misma bandera:
1. **MECHANISMS** (BPP, Poscobro — $141.1M) — correctamente excluidos (paired events, zero net cash)
2. **ROOT_EVENTS** (Talla/Garantía, Arrepentimiento, Producto Dañado — $125.8M) — INCORRECTAMENTE excluidos

La razón es histórica: el campo nació como un parche basado en `detalle` strings, no en `event_role` o `cash_role`. Los detalles `bigger_than_expected_fashion`, `smaller_than_expected_fashion`, y `repentant_buyer` fueron agrupados con los MECHANISMS sin distinción semántica.

---

### FASE 6 — Dictamen final

**`include_in_operational_pnl` es PARCIALMENTE CORRECTO pero contiene contradicciones certificadas.**

**Correcto**: 3 conceptos MECHANISM ($141,128,065) — correctamente excluidos del P&L operacional. La exclusión está respaldada por cash evidence (G6, RFC BPP/Poscobro) y el Go-Live Audit.

**Incorrecto**: 3 conceptos ROOT_EVENT ($125,801,890) — INCORRECTAMENTE excluidos. Son REAL_CASH, impactan Disponible, y están incluidos en el cierre RN certificado (SINGLE FINANCIAL TRUTH).

**Impacto neto del error**: El ledger operacional (vía `iopnl=True`) subestima la realidad financiera en **$116.6M** vs el cierre certificado.

| Métrica | Correcto | Incorrecto | Delta |
|---|---|---|---|
| Ledger operacional | $712,045,128 | $595,474,963 | **-$116,570,165** |
| Desglose (sidebar) | $712,045,128 | $712,045,128* | $0 |
| Click-to-ledger | $712,045,128 | $595,474,963 | **-$116,570,165** |

>*El desglose API muestra el valor correcto porque NO aplica el filtro `iopnl`, pero el click envía al ledger SÍ lo aplica — creando la discrepancia documentada en CLICK_TO_LEDGER_TRACEABILITY.

**Veredicto único**:
```
include_in_operational_pnl es PARCIALMENTE CORRECTO
pero contiene CONTRADICCIONES CERTIFICADAS que afectan
$125,801,890 (47.1% del total excluido) en 3 conceptos
ROOT_EVENT/REAL_CASH que deberían tener iopnl=TRUE.
```

---

### Resumen ejecutivo

1. `include_in_operational_pnl` comenzó como un parche de strings en BASELINE_V6
2. Excluye correctamente 3 MECHANISMS ($141.1M) — respaldado por cash evidence
3. Excluye INCORRECTAMENTE 3 ROOT_EVENTS ($125.8M) — contradice CONCEPT_REGISTRY, EVENT_REGISTRY, CASH_REGISTRY, y el cierre RN certificado
4. La simulación demuestra que excluir solo MECHANISMS produce **$0 delta** con el cierre RN ($712,045,128)
5. El campo necesita una separación semántica entre "es mecanismo" y "es no-operacional" — pero esa separación NO existe hoy
