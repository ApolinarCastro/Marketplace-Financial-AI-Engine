# Ajustes Sign Certification

**Date:** 2026-06-06
**Status:** PASS — sin ambigüedad

---

## 1. Fórmula Exacta del RN

`engine/v4/marketplace_auditor.py:555`:

```
neto = ing + dev + cop + ccm + aju
```

Cada término es `SUM(monto)` de conceptos agrupados por `FINANCIAL_STRUCTURE`. No hay inversión de signo — es flat sum.

Para ML 2026-01, los valores del cierre:

| Componente | Valor | Efecto |
|---|---|---|
| Ingresos (ing) | +$27,646,200 | Suma al RN |
| Costos Op (cop) | -$2,075,055 | Resta del RN |
| Costos Com (ccm) | -$7,954,836 | Resta del RN |
| Ajustes (aju) | **+$1,785,194** | **Suma al RN** |
| **RN** | **$19,401,503** | — |

Verificación: 27,646,200 + (-2,075,055) + (-7,954,836) + 1,785,194 = 19,401,503 ✅

**Sin ajustes:** 27,646,200 + (-2,075,055) + (-7,954,836) = 17,616,309
**Con ajustes:** 19,401,503 — el aju de +$1,785,194 **AUMENTA** el RN.

## 2. Signo Individual de Cada ROOT_EVENT

Todos los ROOT_EVENT tienen monto POSITIVO en el ledger:

| ROOT_EVENT | Rows | Total | Signo | Efecto RN |
|---|---|---|---|---|
| Ajuste por Talla/Garantía | 143 | +$3,575,845 | POS | Suma |
| Ajuste por Arrepentimiento | 105 | +$2,520,642 | POS | Suma |
| Ajuste por Retraso en Entrega | 12 | +$246,083 | POS | Suma |
| Ajuste por Falla en Entrega | 4 | +$81,960 | POS | Suma |
| Ajuste por Producto Dañado/Vacío | 5 | +$75,960 | POS | Suma |

## 3. Por Qué Son Positivos

ML cobra **comisiones a los sellers** por manejar cada evento post-venta. No es un costo que ML paga — es una tarifa que ML **cobra**. Por eso:

- El monto es positivo en el ledger (ML recibe)
- Suma al RN (es ingreso por comisiones de servicio)
- Es REAL_CASH (ML cobra efectivamente del seller)
- Impacta Disponible (aumenta caja de ML)

Ejemplo: cuando un comprador devuelve un producto por talla incorrecta, ML cobra al seller una comisión por la gestión de la devolución. Ese cobro aparece como "Ajuste por Talla/Garantía" con monto positivo.

## 4. Dictamen Final

**Opción A)** Los ROOT_EVENT **SUMAM al RN.**

No hay ambigüedad matemática: `neto = SUM(ingresos + devoluciones + costos + ajustes)` con montos raw del ledger. Todo peso de Ajustes con signo positivo se suma directamente al Resultado Neto. El signo "+" en la UI de Estructura Financiera es correcto.

Los ROOT_EVENT son REAL_CASH que **aumentan** la utilidad de ML, porque representan tarifas cobradas a sellers, no costos operacionales.
