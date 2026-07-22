# CASH_REALITY_CORE_V1 — Abstract Cash Reality Framework

**Estado:** CERTIFICADO (versión abstracta)
**Fecha:** 2026-06-05
**Primer marketplace certificado:** Mercado Libre

---

## Definiciones Core

```
CASH REALITY = la correspondencia entre
los montos registrados en el ledger (acrual)
y los montos que efectivamente se movieron en caja (cash).
```

## Verdades Fundamentales (Universales)

| Verdad | Definición | Fuente |
|--------|------------|--------|
| **Verdad Transaccional** | Qué se vendió, a qué precio, qué costos | Ledger (acrual) |
| **Verdad Fiscal** | Documentos tributarios que soportan la operación | XML DTE / Facturas |
| **Verdad Caja** | Cuándo y cuánto dinero realmente se movió | Liberaciones / Bank statements / Payment processor reports |

## Reglas Universales

### Regla 1: Movimiento de dinero ≠ Evento económico

```
Un pago NO es una venta.
Una liberación NO es una venta.
Un cobro NO es una venta.

Son representaciones de caja de un evento económico
que ocurrió en otro momento.
```

### Regla 2: Timing difference es esperada

```
El monto liberado en un período NO equivale
a las transacciones del mismo período.

Causas:
  - Días hábiles entre venta y liquidación
  - Retenciones (impuestos, comisiones, garantías)
  - Ajustes postventa (devoluciones, reclamos)
  - Reservas contables que se reversan
```

### Regla 3: Cash proxy por concepto

```
Cada concepto en el ledger debe tener:
  - Un cash proxy identificado (fuente de caja externa)
  - Un delta certificado (ledger vs cash)
  - Una clasificación: REAL_CASH / ACCRUAL / MIRROR_ZERO
```

## Cash Roles

| Rol | Significado | Ejemplo |
|-----|-------------|---------|
| `REAL_CASH` | Representa dinero real, tiene cash proxy | Ventas, comisiones, Mediación |
| `ACCRUAL` | Devengado, puede diferir temporalmente de caja | Comisiones ML, publicidad |
| `MIRROR_ZERO` | Mirror contable, NET = $0 en caja | BPP pareado, reserve_for_dispute |
| `PASS_THROUGH` | Flujo que pasa sin impacto neto | Envío pagado por cliente |

## Metodología de Cash Reality

```
Para cada marketplace:

  1. Identificar cash source:
     - Liberaciones (ML)
     - Bank statements (general)
     - Payment processor (Stripe, Mercado Pago, etc.)
     - Settlement reports (A pagar para RIPLEY)

  2. Por cada concepto en ledger:
     - Encontrar proxy en cash source
     - Comparar montos: ledger vs cash
     - Calcular delta: |ledger - cash| / ledger
     - Clasificar delta como ESPERADO o ANÓMALO

  3. Para MECHANISMS:
     - Verificar que reserve NET ≈ $0
     - Verificar paired mechanism ≠ real cash
     - Standalone mechanism = real cash

  4. Certificar:
     - PASS si delta < 5% y explicable
     - PASS CONDITIONAL si delta > 5% pero explicable
     - FAIL si delta inexplicable
```

## Matriz de Cash Reality por Marketplace

| Marketplace | Cash Source | Delta Certified | Status |
|-------------|-------------|----------------|--------|
| **ML** | Liberaciones (2025-04) | 3.9% | **CERTIFICADO** |
| ML (BPP/Poscobro) | reserve_for_dispute | NET=$0 | **CERTIFICADO** |
| RIPLEY | A pagar (settlement) | N/A | PENDIENTE |
| PARIS | N/A | N/A | PENDIENTE |
| FALABELLA | N/A | N/A | PENDIENTE |
| SHOPIFY | N/A | N/A | PENDIENTE |

## Certificaciones Core

| Documento | Relación |
|-----------|----------|
| `governance/G6_CASH_REALITY_CERTIFICATION.md` | ML 2025-04 certified |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | BPP+Poscobro cash |
| `governance/MARKETPLACE_MONEY_FLOW_TRUTH.md` | Money flow framework |
| `knowledge/marketplaces/mercadolibre/ML_CASH_REALITY_MODEL_V1.md` | ML certified implementation |
