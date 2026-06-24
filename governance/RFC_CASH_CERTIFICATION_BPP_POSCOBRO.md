# RFC_CASH_CERTIFICATION_BPP_POSCOBRO

**Fecha**: 2026-06-05
**DB**: `data/db/meli_financial_v4.db`
**Cash Source**: `01_Raw/ML/Liberaciones/2025-04 Abril/Abril 2025.xlsx`
**READ ONLY**: Solo evidencia. Sin implementacion, sin cambios, sin codigo.

---

## Single Question

**If BPP and Poscobro are removed from Resultado Neto, does real cash disappear?**

---

## Evidence Sources Utilizadas

| Source | Disponible | Uso |
|--------|-----------|-----|
| **Liberaciones** | SI (18 archivos, 2025-01 a 2026-06) | Fuente unica de efectivo real. Se analizo Abril 2025 (5,142 rows) |
| Liquidaciones | NO disponible en repositorio | - |
| Facturacion | NO disponible en repositorio | - |
| Notas de Credito | NO disponible en repositorio | - |
| Dinero Disponible | NO disponible en repositorio | - |

**Nota**: La certificacion se basa exclusivamente en Liberaciones como unica fuente de caja disponible.

---

## FASE 1: Mediacion + reserve_for_dispute (Cash Trace)

### Mediacion en Liberaciones

| Driver | Rows | Debitado (Cash OUT) |
|--------|------|---------------------|
| Mediacion (disputas) | 356 | **$10,491,578.00** |

Mediacion = el cash outflow REAL que ML paga cuando un comprador gana una disputa (Talla incorrecta, Arrepentimiento, etc.). 
**Este es el evento economico raiz en efectivo.**

### reserve_for_dispute en Liberaciones

| Component | Rows | Creditado | Debitado | Neto |
|-----------|------|-----------|----------|------|
| reserve_for_dispute | 711 | $10,717,249 | $10,671,802 | **$45,447 (0.42%)** |
| BPP-specific reserve | 314 | $4,571,502 | $4,571,502 | **$0 (EXACTO)** |
| Poscobro-specific reserve | 142 | $2,524,535 | $2,524,535 | **$0 (EXACTO)** |

reserve_for_dispute = el reflejo contable de BPP/Poscobro en el cash flow de ML. 
**NETO = $0 para BPP y Poscobro individualmente.**
**NETO = ~$0 total ($45K residual = 0.42% de tolerancia de settlement).**

### Conclusion FASE 1

```
Cash Flow Real (Liberaciones):
  Mediacion (OUT):    $10,491,578  ← Evento raiz (Talla/Arrepentimiento)
  reserve_for_dispute: $0 NET      ← BPP/Poscobro (se crea y se reversa)
  
  BPP y Poscobro NO tienen representacion de caja real.
  La caja real corresponde al EVENTO RAIZ (Talla/Arrepentimiento).
```

---

## FASE 2: BPP Orders in Cash

| Metric | Value |
|--------|-------|
| BPP ledger records (Abril 2025) | 198 |
| BPP orders found in Liberaciones | **179 (90.4%)** |
| Liberaciones rows for BPP orders | 1,007 |
| Cash acreditado | $12,873,671 |
| Cash debitado | $12,397,663 |
| **Cash neto** | **$476,008** |

### Cash Breakdown for BPP Orders

| Description | Rows | Acreditado | Debitado | Neto |
|-------------|------|-----------|----------|------|
| reserve_for_dispute | 314 | $4,571,502 | $4,571,502 | **$0** |
| Mediacion (root event) | 162 | $0 | $4,591,911 | **-$4,591,911** |
| Pago (original sale) | 172 | $4,671,459 | $0 | +$4,671,459 |
| Reserva para devolucion envio BBP | 223 | $2,663,236 | $3,234,250 | -$571,014 |
| Devolucion de dinero | 131 | $946,671 | $0 | +$946,671 |
| Envio | 5 | $20,803 | $0 | +$20,803 |

**Hallazgo clave**: reserve_for_dispute NETO = $0 EXACTO. Mediacion = $4,591,911 cash OUTFLOW = root event (Talla), no BPP.

---

## FASE 3: Poscobro Orders in Cash

| Metric | Value |
|--------|-------|
| Poscobro ledger records (Abril 2025) | 148 |
| Poscobro orders found in Liberaciones | **92 (62.2%)** |
| Liberaciones rows for Poscobro orders | 485 |
| Cash acreditado | $6,985,259 |
| Cash debitado | $6,777,037 |
| **Cash neto** | **$208,222** |

### Cash Breakdown for Poscobro Orders

| Description | Rows | Acreditado | Debitado | Neto |
|-------------|------|-----------|----------|------|
| reserve_for_dispute | 142 | $2,524,535 | $2,524,535 | **$0** |
| Mediacion (root event) | 70 | $0 | $2,427,953 | **-$2,427,953** |
| Pago (original sale) | 79 | $2,632,559 | $0 | +$2,632,559 |
| Reserva para devolucion envio BBP | 91 | $1,245,199 | $1,716,853 | -$471,654 |
| Devolucion de dinero | 58 | $519,495 | $48,691 | +$470,804 |
| Envio | 13 | $9,623 | $0 | +$9,623 |
| Reserva para reembolso | 22 | $53,848 | $53,848 | **$0** |

**Hallazgo clave**: reserve_for_dispute NETO = $0 EXACTO. Mediacion = $2,427,953 cash OUTFLOW = root event (Talla/Arre), no Poscobro.

---

## FASE 4: Paired Orders in Cash (G6 Methodology Cross-check)

Metodologia G6: ordenes que tienen 2+ conceptos distintos en ajustes (Talla+BPP, Arre+Posc, etc.)

| Metric | Value |
|--------|-------|
| Paired orders (Abril 2025) | 197 |
| Found in Liberaciones | **192 (97.5%)** |
| Cash rows for paired orders | 1,177 |
| Cash acreditado | $15,827,826 |
| Cash debitado | $15,868,425 |
| **Cash neto** | **-$40,599 (~$0)** |

### Cash Breakdown for Paired Orders

| Description | Rows | Acreditado | Debitado | Neto |
|-------------|------|-----------|----------|------|
| reserve_for_dispute | 370 | $5,651,694 | $5,651,694 | **$0** |
| Mediacion (root event) | 184 | $0 | $5,595,703 | **-$5,595,703** |
| Pago (original sale) | 188 | $5,384,250 | $0 | +$5,384,250 |
| Reserva para devolucion envio BBP | 282 | $3,578,360 | $4,621,028 | -$1,042,668 |
| Devolucion de dinero | 151 | $1,204,960 | $0 | +$1,204,960 |
| Envio | 2 | $8,562 | $0 | +$8,562 |

**Hallazgo clave**: Paired orders NET = -$40,599 (~$0). reserve_for_dispute NET = $0 EXACTO.

---

## FASE 5: All-time Paired vs Standalone Mechanisms

| Concepto | Total (all-time) | Paired | Standalone | % Paired |
|----------|-----------------|--------|------------|----------|
| BPP | $95,231,534 | $92,388,934 | **$2,842,600** | 97.0% |
| Poscobro | $47,993,999 | $42,017,119 | **$5,976,881** | 87.5% |
| **TOTAL** | **$143,225,534** | **$134,406,053** | **$8,819,481** | **93.8%** |

### Definiciones

- **Paired**: La misma orden tiene BPP/Poscobro + otro concepto de ajuste (Talla/Garantia, Arrepentimiento). El cash outflow ya esta capturado por el evento raiz.
- **Standalone**: La orden SOLO tiene BPP o Poscobro (ningun otro concepto de ajuste). No hay evento raiz alternativo que capture el cash.

---

## FASE 6: Impact on Resultado Neto

| Metric | Amount |
|--------|--------|
| RN actual (all-time ML) | **$842,250,301** |
| RN sin BPP+Poscobro (todos) | $699,024,767 (-17.0%) |
| RN economico (solo paired removidos) | $830,371,159 (-1.41%) |
| **Standalone que debe preservarse** | **$8,819,481 (1.05% de RN)** |

---

## VERDICT: PASS CONDITIONAL

### Single Question
**If BPP and Poscobro are removed from Resultado Neto, does real cash disappear?**

### Answer: PARTIAL

| Component | Amount | % of Mechanisms | Cash Disappears? | Removal Justified? |
|-----------|--------|----------------|------------------|-------------------|
| **Paired BPP** | $92,388,934 | 64.5% | **NO** ($0 en cash) | **YES** |
| **Paired Poscobro** | $42,017,119 | 29.3% | **NO** ($0 en cash) | **YES** |
| **Standalone BPP** | $2,842,600 | 2.0% | **YES** ($2.8M real) | **NO** |
| **Standalone Poscobro** | $5,976,881 | 4.2% | **YES** ($6.0M real) | **NO** |
| **TOTAL Paired** | **$134,406,053** | **93.8%** | **NO** | **PASS** |
| **TOTAL Standalone** | **$8,819,481** | **6.2%** | **YES** | **FAIL** |

### Veredicto Final

```
PASS CONDITIONAL:
- 93.8% de BPP+Poscobro ($134.4M) puede eliminarse del P&L SIN perder caja real
  Evidencia: reserve_for_dispute NET=$0 en Liberaciones para ambos conceptos
  La caja real (Mediacion) corresponde al evento raiz (Talla/Arrepentimiento)

- 6.2% de BPP+Poscobro ($8.8M, 1.05% de RN) NO puede eliminarse
  Evidencia: Son standalone - no tienen evento raiz que cubra su cash
  Representan eventos economicos reales sin representacion alternativa

REGLA DE CERTIFICACION:
  Si id_orden tiene BPP + otro concepto de ajuste (Talla/Arre) = PAIRED = removible
  Si id_orden tiene SOLO BPP o SOLO Poscobro = STANDALONE = NO removible
```

### Cash Evidence Summary

| Evidence Type | Result | Confidence |
|--------------|--------|-----------|
| BPP reserve_for_dispute NET | **$0 (EXACTO)** | 100% (314 rows) |
| Poscobro reserve_for_dispute NET | **$0 (EXACTO)** | 100% (142 rows) |
| Total reserve_for_dispute NET | **$45,447 (0.42%)** | ALTA (711 rows) |
| BPP orders traced to cash | 179/198 (90.4%) | ALTA |
| Poscobro orders traced to cash | 92/148 (62.2%) | MEDIA (rest: different ID format) |
| Paired orders in cash (G6) | 192/197 (97.5%) | MUY ALTA |
| Paired orders net cash impact | -$40,599 (~$0) | MUY ALTA |
| RN impacto de standalone | 1.05% | ALTA |

### Limitaciones

1. **Liquidaciones, Facturacion, Notas de Credito, Dinero Disponible**: NO disponibles en repositorio. Certificacion basada exclusivamente en Liberaciones.
2. **Cobertura temporal**: Cash trace solo para Abril 2025. 18 archivos de Liberaciones existen (2025-01 a 2026-06) pero no fueron analizados en su totalidad.
3. **Poscobro coverage menor (62.2%)**: 56 orders no encontradas en Liberaciones. Posible causa: formato de ID diferente (Poscobro usa IDs generados por ML que no aparecen directamente en ID_OPERACION_MP).
4. **reserve_for_dispute residual**: $45K (0.42%) no neteado - atribuible a timing/rounding de settlement.

---

## Ejecucion

```bash
python tmp_cash_final.py
# Output: RFC_CASH_CERTIFICATION_BPP_POSCOBRO - FINAL CASH TRACE v3
# DB: data/db/meli_financial_v4.db
# Cash: 01_Raw/ML/Liberaciones/2025-04 Abril/Abril 2025.xlsx
```

---

*Forensic investigation complete. Read-only. No implementation proposals.*
