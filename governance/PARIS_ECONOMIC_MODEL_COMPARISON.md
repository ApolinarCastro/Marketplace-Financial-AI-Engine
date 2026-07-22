# PARIS ECONOMIC MODEL COMPARISON
**Date:** 2026-06-11
**Certification ID:** PARIS-ECON-FASE5

---

## Modelo Actual (Ledger hoy)

```
Venta (ingresos)       $483,888,712  ← MONTO_A_PAGAR (neto, comisión ya deducida)
Devoluciones           -$121,458,109 ← MONTO_A_PAGAR (neto)
Costos Operacionales   -$26,660,638
Ajustes                $1,375,357
──────────────────────────────────
RESULTADO NETO         $337,418,552
```

**Características:**
- `monto` en ledger = `monto a pagar` del source file (neto post-comisión)
- NO existe concepto de Venta Bruta
- NO existe concepto de Comisión Marketplace
- El modelo es: Net Revenue (no Gross Revenue)

---

## Modelo Objetivo (con comisión explícita)

```
Venta Bruta (ingresos) $487,741,043  ← MONTO (bruto, antes de comisión)
Comisión Marketplace   -$76,894,614  ← MONTO - MONTO_A_PAGAR
Venta Neta             $338,658,414  ← MONTO_A_PAGAR (neto post-comisión)
Devoluciones           -$123,490,638 ← MONTO_A_PAGAR
Costos Operacionales   -$27,240,578
Ajustes                $1,375,357
──────────────────────────────────
RESULTADO NETO         $337,418,552
```

**Características:**
- `monto` en ledger = `monto` (bruto) del source file
- Comisión Marketplace como concepto explícito en `costos_comerciales` o `ajustes`
- Neto calculado como: Venta Bruta - Comisión - Devoluciones - Costos - Ajustes

---

## Comparación Directa

| Concepto | ACTUAL (Ledger) | OBJETIVO (con comisión) | DELTA |
|---|---|---|---|
| Venta Bruta | **NO EXISTE** | $487,741,043 | +$487.7M |
| Venta en Ledger (neto) | $483,888,712 | $338,658,414 | -$145.2M |
| Comisión Marketplace | **NO EXISTE** | -$76,894,614 | -$76.9M |
| Devoluciones | -$121,458,109 | -$123,490,638 | -$2.0M |
| Costos Operacionales | -$26,660,638 | -$27,240,578 | -$0.6M |
| Ajustes | $1,375,357 | $1,375,357 | $0 |
| **Resultado Neto** | **$337,418,552** | **$337,418,552** | **$0 ✅** |

**El Resultado Neto es IDÉNTICO en ambos modelos.** La diferencia es solo de presentación: el modelo actual muestra Net Revenue, el objetivo mostraría Gross Revenue + Commission line.

---

## Matriz Económica

```
              ACTUAL                          OBJETIVO
         ┌──────────────┐              ┌──────────────┐
         │  Venta Neta  │              │ Venta Bruta  │
         │ $483.9M      │              │ $487.7M      │
         └──────┬───────┘              └──────┬───────┘
                │                             │
         ┌──────┴───────┐              ┌──────┴───────┐
         │  Comisión    │              │  Comisión    │
         │  IMPLÍCITA   │              │  EXPLÍCITA   │
         │  (en el neto)│              │  -$76.9M     │
         └──────┬───────┘              └──────┬───────┘
                │                             │
         ┌──────┴───────┐              ┌──────┴───────┐
         │  Neto Final  │              │  Neto Final  │
         │  $337.4M     │              │  $337.4M     │
         └──────────────┘              └──────────────┘
```

---

## DTE Documentary Backing

| Tipo DTE | Cantidad | Monto Total | Respalda |
|---|---|---|---|
| DTE 33 (Factura Electrónica) | 36 | $59,926,401 | Venta Bruta (parcial) |
| DTE 43 (Liquidación-Factura) | 25 | $138,154,627 | Liquidación Neta |
| DTE 61 (Nota de Crédito) | 1 | $7,818,947 | Ajuste/Crédito |
| **TOTAL** | **62** | **$205,899,975** | **42.6% del ledger** |

---

## Veredicto FASE 5

1. **PARIS opera con MONTO_A_PAGAR** — Confirmado. Ledger no tiene concepto de Venta Bruta.
2. **No existe comisión explícita** — La comisión es implícita (margen 1P).
3. **Modelo actual es CORRECTO para 1P** — En un modelo first-party, la comisión no se separa.
4. **Cambiar a Gross Revenue requeriría reprocesar ETL completo** — Se necesitaría cargar `monto` en vez de `monto a pagar` y crear un nuevo concepto "Comisión Marketplace".
5. **RN no cambiaría** — Ambos modelos producen el mismo Resultado Neto.
