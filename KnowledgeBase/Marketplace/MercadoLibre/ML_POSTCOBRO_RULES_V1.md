# ML_POSTCOBRO_RULES_V1 — Certified Poscobro Rules

**CERTIFICADO 007**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** RFC_POSCOBRO_CAUSALITY_FINAL, ML_POSCOBRO_FORENSICS, RFC_EVENT_MODEL_CERTIFICATION

---

## Definiciones Fundamentales

```
Poscobro NO es devolución.
Poscobro NO es caja.
Poscobro NO es liberación.
Poscobro NO es nota de crédito.
```

## ¿Qué es Poscobro?

```
Poscobro = pipeline postventa.

Es el proceso de gestión de reclamos,
devoluciones, mediaciones, reembolsos
y compensaciones que ocurren DESPUÉS
de que una venta ha sido completada.
```

## ¿Qué contiene Poscobro?

| Componente | Descripción | Rol |
|------------|-------------|-----|
| Reclamos | Cliente reporta un problema | ROOT_EVENT |
| Devoluciones | Producto devuelto | ROOT_EVENT |
| Mediaciones | MercadoLibre interviene | ROOT_EVENT (cash) |
| Reembolsos | Dinero devuelto al cliente | MECHANISM |
| Compensaciones | Ajuste a favor del vendedor | MECHANISM |

## Reglas de Análisis

| Regla | Descripción |
|-------|-------------|
| P1 | Poscobro debe analizarse siempre junto con Facturación ML + Liberaciones + Todas las Transacciones. |
| P2 | Nunca analizar Poscobro aisladamente — no tiene sentido sin contexto transaccional. |
| P3 | Poscobro CONCILIADO = mechanism pareado con ROOT_EVENT → NET cash = $0. |
| P4 | Poscobro GENERAL = puede ser ROOT_EVENT o MECHANISM según contexto. |
| P5 | BPP = execution mechanism de garantía → NET cash = $0 cuando pareado. |
| P6 | BPP standalone ($2.8M) = real cash → preservar en Resultado Neto. |
| P7 | Mediación = real cash outflow → ROOT_EVENT. |
| P8 | reserve_for_dispute = accounting mirror → NET $0. |

## Estructura de Conceptos Poscobro (14 concepts)

```
AJUSTES POSCOBRO
├── ROOT_EVENTS (preserve in P&L)
│   ├── Talla/Garantía
│   ├── Arrepentimiento
│   ├── Producto Dañado/Vacío
│   ├── Diferencia Publicación
│   ├── Item Faltante
│   ├── Falta de Stock
│   ├── Retraso en Entrega
│   ├── Cambio de Dirección
│   ├── Falla en Entrega
│   └── Disputa no Respondida
│
├── EXECUTION MECHANISMS (exclude when paired)
│   ├── BPP (Compra Protegida)
│   ├── Poscobro Conciliado
│   └── Poscobro General
│
└── OTHER
    └── Abono manual
```

## Cash Impact (ALL-TIME)

| Categoría | Amount | % | Cash |
|-----------|--------|---|------|
| Paired mechanisms | $134,402,513 | 93.8% | $0 |
| Standalone mechanisms | $8,819,481 | 6.2% | REAL |
| **Total Poscobro** | **$143,225,534** | **100%** | **$8.8M real** |

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/RFC_POSCOBRO_CAUSALITY_FINAL.md` | Ciclo de vida poscobro certificado |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | Cash certification (PASS CONDITIONAL) |
| `governance/RFC_EVENT_MODEL_CERTIFICATION.md` | Event model (PASS) |
| `governance/ML_POSCOBRO_FORENSICS.md` | Poscobro forensics (634 rows) |

## Aplicación a otros marketplaces

Poscobro es específico de Mercado Libre. Ningún otro marketplace tiene un pipeline postventa equivalente en tamaño o complejidad. Sin embargo, el marco conceptual (ROOT_EVENT vs MECHANISM, triangulación 3-vías) es universal.
