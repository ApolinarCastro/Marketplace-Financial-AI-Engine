# PARIS DOCUMENTARY TRUTH
**Date:** 2026-06-11
**Certification ID:** PARIS-ECON-FASE4

---

## XML DTE Documents

62 SII DTE XML files in `01_Raw/PARIS/Facturacion/`:

| Tipo DTE | Nombre | Cantidad | Monto Total |
|---|---|---|---|
| **33** | Factura Electrónica | 36 | $59,926,401 |
| **43** | Liquidación-Factura Electrónica | 25 | $138,154,627 |
| **61** | Nota de Crédito Electrónica | 1 | $7,818,947 |
| **TOTAL** | | **62** | **$205,899,975** |

---

## Documentary Backing by Economic Component

### ¿Qué respalda DTE 33?

**Factura Electrónica** — Respalda la Venta Bruta (MONTO).

- Emitido por: Cencosud Retail S.A. (RUT 81201000-K)
- Monto total: $59.9M
- Cobertura: 12.3% de la Venta Bruta RAW ($487.7M)
- Significado: Documento tributario que acredita la venta al consumidor final
- **No todos los documentos 33 tienen respaldo completo en ledger** — la cobertura DTE es parcial (42.6% del ledger)

### ¿Qué respalda DTE 43?

**Liquidación-Factura Electrónica** — Respalda la Liquidación Neta (MONTO_A_PAGAR).

- Emitido por: Cencosud Retail S.A. (RUT 81201000-K)
- Monto total: $138.2M
- Significado: Documento de liquidación entre Cencosud y el seller/operador logístico
- **No es una comisión** — es una liquidación de pagos netos

### ¿Qué respalda DTE 61?

**Nota de Crédito Electrónica** — Respalda ajustes/créditos.

- Monto: $7.8M
- Significado: Corrección o anulación de documentos anteriores

---

## Economic Component vs DTE Backing

| Componente Económico | Ledger | DTE Backing | % Cubierto |
|---|---|---|---|
| Venta (neto) | $483,888,712 | $205,899,975 (DTE 33+61) | 42.6% |
| Venta Bruta (gross) | NO EXISTE | $59,926,401 (DTE 33) | — |
| Comisión | NO EXISTE | $138,154,627 (DTE 43) | — |
| Devoluciones | -$121,458,109 | Parcial (vía DTE 61) | — |
| Costos Operacionales | -$26,660,638 | No respaldado por DTE | 0% |
| Ajustes | $1,375,357 | Parcial (DTE 61) | — |

---

## Interpretación del Modelo 1P

PARIS opera como **first-party retailer** (Cencosud):

1. **DTE 33** → Venta directa al consumidor (Factura Electrónica)
2. **DTE 43** → Liquidación entre entidades Cencosud (Liquidación-Factura)
3. **DTE 61** → Nota de Crédito (ajustes)

El DTE 43 NO es una comisión marketplace en el sentido MP. Es una liquidación interna entre la operación logística de Cencosud y Cencosud Retail.

Para un modelo 1P:
- **Venta** = respaldada por DTE 33 + registros internos
- **Comisión implícita** = margen entre DTE 33 y liquidación neta
- **Liquidación** = respaldada por DTE 43 + DTE 33

---

## Áreas Sin Respaldo Documental

| Componente | % Sin DTE | Riesgo |
|---|---|---|
| Costos Operacionales (Cobro por despacho, Logística inversa) | **100%** | ALTO — sin respaldo tributario directo |
| Devoluciones (neto) | **~90%** | ALTO — solo parcialmente en DTE 61 |
| Ajustes (Compensación logística, Cargos) | **~90%** | ALTO — sin respaldo documental directo |

---

## Veredicto FASE 4

| Componente | Respaldo Documental |
|---|---|
| **Venta (monto_a_pagar)** | **Parcial** (42.6% por DTE 33+43+61) |
| **Venta Bruta (monto)** | **Sin respaldo directo en ledger** |
| **Comisión Marketplace** | **No existe como concepto** |
| **Costos Operacionales** | **Sin DTE** (basado en archivos Transacciones) |
| **Devoluciones** | **Parcial** (DTE 61 para créditos) |
