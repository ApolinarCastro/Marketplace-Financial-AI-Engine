# REPORTE GERENCIAL UX1.2 - REDISEÑO FINANCIERO

**Contexto:** Alineación de la interfaz de usuario con la política de Single Financial Truth (DEC-019) y el modelo P&L del Seller. El objetivo es desvincular métricas operativas de las métricas puramente financieras, garantizando un Resultado Neto preciso y comprensible.

---

## 1. REEMPLAZO DE KPI PRINCIPALES (HEADER CARDS)

Se eliminan las tarjetas superiores que mezclaban devengado (Ventas) con flujo de caja (Cobros / Disponible).

### ❌ Estructura Actual (UX1.1)
Las tarjetas superiores mostraban un mix de conceptos:
1. `VENTAS` (Devengado)
2. `DEVOLUCIONES` (Devengado Negativo)
3. `COBROS` (Caja / Pasarela)
4. `DISPONIBLE` (Caja)

*Problema:* El usuario intentaba sumar/restar mentalmente Ventas - Devoluciones y no cuadraba con Cobros o Disponible por las diferencias temporales y los Costos Operativos ocultos.

### ✅ Estructura Nueva (UX1.2) - Vista P&L Financiero
1. `VENTAS BRUTAS`
2. `DEVOLUCIONES`
3. `COSTOS MARKETPLACE`
4. `RESULTADO NETO`

*Ventaja:* Representa la ecuación matemática real del P&L. Es directo y 100% auditable desde el Ledger sin sesgos temporales de caja.

---

## 2. NUEVA VISTA DUAL: FINANZAS VS CAJA

Para resolver la necesidad del Seller de entender su liquidez, se incorpora un _toggle_ (Switch) en la parte superior derecha del Dashboard: **[ P&L Financiero | Flujo de Caja ]**

### Vista: FLUJO DE CAJA (Caja / Liquidez)
Al activar esta vista, las tarjetas principales mutan para reflejar el estado del extracto bancario o billetera virtual (Mercado Pago):
1. `DISPONIBLE` (Fondo actual líquido en cuenta).
2. `LIBERACIONES` (Fondos que pasaron el periodo de cuarentena/reserva).
3. `RETENCIONES` (Fondos bloqueados por disputas temporales o políticas de la plataforma).
4. `TRANSFERENCIAS` (Dinero efectivamente depositado en la cuenta bancaria del Seller).

---

## 3. MOCKUP ANTES / DESPUÉS

### 🔴 ANTES (Versión 1.1)
```text
======================================================================
[ DASHBOARD GERENCIAL V1.1 ]
======================================================================
[ VENTAS: $100k ] [ DEVOLUCIONES: $10k ] [ COBROS: $80k ] [ DISPONIBLE: $35k ]

>> WATERFALL DE RENTABILIDAD
  Ventas        |████████████████████
  Devoluciones  |██
  Logística     |███
  Comisiones    |████
  Aj. y Reten.  |████   <-- (Confuso: incluye publicidad, retenciones, garantías)
  ---------------------------------
  R. Neto       |███████
======================================================================
```

### 🟢 DESPUÉS (Versión 1.2)
```text
======================================================================
[ DASHBOARD GERENCIAL V1.2 ]                  Vista: (◉ P&L | ○ Caja )
======================================================================
[ VENTAS BRUTAS: $100k ] [ DEVOLUCIONES: $10k ] [ COSTOS MKT: $15k ] [ RESULTADO NETO: $70k ]

>> WATERFALL FINANCIERO V2
  Ventas Brutas |████████████████████
  Devoluciones  |██
  Ingresos Netos|██████████████████
  Costos Market.|████
  Gastos Comerc.|█
  Recuperaciones|
  ---------------------------------
  Resultado Neto|█████████████

======================================================================
>> MÓDULO INTELIGENCIA OPERACIONAL (No impacta P&L)
   ⚠️ Talla/Garantía: 150 órdenes ($5,000) - 45% del total de quejas 📈
   ⚠️ Falla Entrega:   40 órdenes ($2,000) - 12% del total de quejas 📉
   🛡️ Chargebacks:      5 órdenes ($500)   - Riesgo bajo
======================================================================
```

---

## 4. IMPACTO TÉCNICO
1. **API:** El endpoint del dashboard requiere un flag `?view=pnl` o `?view=cash`.
2. **Ledger:** Intacto. Solo se utilizan sumatorias diferentes filtrando por `clasificacion_v2`.
3. **Validación Visual:** El delta financiero para un mes cerrado debe ser `$0`. El `RESULTADO NETO` que antes se mostraba al final del gráfico ahora estará en el Header, coincidiendo al centavo.
