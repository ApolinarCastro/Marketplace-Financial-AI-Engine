# PARIS COMMISSION EXISTENCE CERTIFICATION
**Date:** 2026-06-11
**Certification ID:** PARIS-ECON-FASE2

---

## Question

¿Existe hoy una entidad econÃ³mica explÃ­cita de comisiÃ³n marketplace en el ledger?

---

## Answer

**NO** — No existe ningÃºn concepto de comisiÃ³n marketplace en `marketplace_ledger_v1` para PARIS.

---

## Evidence

### 1. Ledger Concepts (all 12 for PARIS)

| Concepto | Financial Group | Total | Es ComisiÃ³n? |
|---|---|---|---|
| Venta | ingresos | $483,888,712 | NO |
| DevoluciÃ³n | devoluciones | -$121,458,109 | NO |
| Cobro por despacho | costos_operacionales | -$21,625,080 | NO |
| LogÃ­stica inversa | costos_operacionales | -$3,088,120 | NO |
| Retiro stock bodega Paris | costos_operacionales | -$1,630,800 | NO |
| CompensaciÃ³n logÃ­stica | ajustes | $1,618,057 | NO |
| Ajuste Inventario Activo | ajustes | $647,108 | NO |
| Cargo | ajustes | -$646,295 | NO |
| Cobro stock antiguo | costos_operacionales | -$316,638 | NO |
| Rebate | ingresos | $273,230 | NO |
| Cobro por campaÃ±a | ajustes | -$260,504 | NO |
| Merma | ajustes | $16,991 | NO |
| **ComisiÃ³n Marketplace** | **—** | **$0** | **❌ NO EXISTE** |

No hay ninguna fila en `marketplace_ledger_v1` para PARIS cuyo `detalle` contenga "comisi", "fee", o "comision".

### 2. Source File Commission

Los archivos RAW (DS y FF) tienen una columna `comisiÃ³n` explÃ­cita:

| Fuente | SUM(comisiÃ³n) | InterpretaciÃ³n |
|---|---|---|
| DS files (18 archivos) | $709,258 | ComisiÃ³n explÃ­cita en archivos fuente |
| FF files (4 archivos) | $265,677 | ComisiÃ³n explÃ­cita en archivos fuente |
| **Total RAW** | **$974,935** | |

**Sin embargo**, la diferencia entre `monto` (bruto) y `monto a pagar` (neto) es MUCHO mayor:

| MÃ©trica | VALOR |
|---|---|
| SUM(monto) raw (gross) | $415,553,028 |
| SUM(monto a pagar) raw (net) | $338,658,414 |
| **Diferencia bruto - neto** | **$76,894,614** |
| SUM(columna comisiÃ³n) | **$974,935** |
| **Diferencia NO explicada por comisiÃ³n** | **$75,919,679** |

### 3. Interpretation

La columna `comisiÃ³n` en los archivos fuente ($974,935 total) NO representa la comisiÃ³n marketplace completa. Es solo una comisiÃ³n operacional pequeÃ±a (tÃ­picamente $15 por transacciÃ³n).

La diferencia real entre `monto` (bruto) y `monto a pagar` (neto) de **$76.9M** incluye:

| Componente | EstimaciÃ³n |
|---|---|
| ComisiÃ³n operacional explÃ­cita (columna comisiÃ³n) | $0.97M |
| Descuento Comercial | ~$5-10M |
| Otros ajustes, cargos, y margen | ~$66-71M |
| **Diferencia total (bruto - neto)** | **$76.9M** |

En el modelo 1P de PARIS (Cencosud actÃºa como retailer directo), la "comisiÃ³n marketplace" **es implÃ­cita** — representa el margen de venta al por menor. No existe como concepto separado porque PARIS no es un marketplace de terceros (como ML o RIPLEY), sino un retailer 1P.

---

## VerificaciÃ³n

```
SUM(monto) - SUM(monto a pagar) = 415,553,028 - 338,658,414 = 76,894,614
SUM(columna comisiÃ³n)           = 974,935
Diferencia no explicada          = 75,919,679
```

La comisiÃ³n explÃ­cita ($0.97M) es solo el **1.3%** de la diferencia bruto-neto ($76.9M).

---

## Veredicto FASE 2

**NO** — No existe una entidad econÃ³mica explÃ­cita de comisiÃ³n marketplace en el ledger para PARIS. La comisiÃ³n es **implÃ­cita** en el modelo 1P (margen de venta al por menor), no un cargo explÃ­cito como en los modelos MP (ML, RIPLEY).

**ComisiÃ³n histÃ³rica total en RAW (columna explÃ­cita): $974,935**
**Margen implÃ­cito total (diferencia bruto-neto): $76,894,614**
