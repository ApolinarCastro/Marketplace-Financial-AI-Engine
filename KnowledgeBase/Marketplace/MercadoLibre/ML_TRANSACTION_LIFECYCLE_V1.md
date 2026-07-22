# ML_TRANSACTION_LIFECYCLE_V1 — Certified Transaction Lifecycle

**CERTIFICADO 003**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** RFC_POSCOBRO_CAUSALITY_FINAL, RFC_EVENT_MODEL_CERTIFICATION

---

## Ciclo de Vida Completo

```
VENTA
  │
  ▼
CARGO (Cargo por venta)
  │
  ▼
PAGO (Pago recibido, reserve_for_dispute)
  │
  ├────────────────────────────────────┐
  │                                    │
  ▼                                    ▼
LIBERACIÓN (sin reclamo)          AJUSTE / POSCOBRO (con reclamo)
  │                                    │
  ▼                                    ▼
CAJA REAL                         MEDIACIÓN / RECLAMO
                                       │
                                       ▼
                                  NOTA CRÉDITO (si aplica)
                                       │
                                       ▼
                                  LIBERACIÓN (neto)
                                       │
                                       ▼
                                  CAJA REAL
```

## ROOT_EVENT

| Concepto | Rol | Justificación |
|----------|-----|---------------|
| **VENTA** | ROOT_EVENT | Es el evento económico original. Todo lo demás es consecuencia. |
| Cargo por venta (Venta) | ROOT_EVENT | Representación directa de la venta. |
| Cargo por venta (Comisión) | ROOT_EVENT | Costo directo asociado a la venta. |

## MECHANISMS

| Concepto | Rol | Justificación |
|----------|-----|---------------|
| Pago | MECHANISM | Ejecución operacional del cobro. No es un evento económico nuevo. |
| Liberación | MECHANISM | Movimiento de caja. No es revenue. |
| reserve_for_dispute | MECHANISM | Reserva contable. NET=$0. |
| Poscobro | MECHANISM | Pipeline postventa. NO es devolución. NO es caja. |
| BPP | MECHANISM | Ejecución de garantía. NET=$0 cuando pareado. |

## Regla de Resultado Neto

```
ROOT_EVENT → participa en Resultado Neto
MECHANISM → excluido cuando está pareado con ROOT_EVENT
MECHANISM → preservado cuando es STANDALONE
```

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/RFC_EVENT_MODEL_CERTIFICATION.md` | Event model (PASS) |
| `governance/RFC_POSCOBRO_CAUSALITY_FINAL.md` | Ciclo de vida poscobro |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | Cash reality de mechanisms |
| `governance/G6_1_RESULTADO_NETO_EVENTS_VS_RECORDS.md` | Eventos vs registros (FAIL) |

## Aplicación a otros marketplaces

La estructura ROOT_EVENT → MECHANISM se aplica a cualquier marketplace que tenga:
- Un pipeline postventa (reclamos, ajustes)
- Un sistema de garantías (BPP equivalente)
- Reservas contables que se reversan

Marketplaces SIN pipeline postventa (RIPLEY, PARIS, FALABELLA, SHOPIFY) tienen:
- Todos los conceptos = ROOT_EVENT
- Sin MECHANISM concepts
