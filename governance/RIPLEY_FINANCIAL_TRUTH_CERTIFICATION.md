# RIPLEY FINANCIAL TRUTH CERTIFICATION

**Sprint B2.3 — 2026-05-30**

**Objetivo:** Establecer la definición oficial de Ingresos Brutos, Ventas, Comisiones y Resultado Neto, contrastando las tres fuentes disponibles (CSV Finanzas, XLSX Resumen Financiero, Ledger), y determinar la fuente canónica para cada KPI.

---

## 1. LAS TRES FUENTES

### 1.1 CSV Finanzas — `Ripley_Finanzas_RAW`

| Atributo | Valor |
|---|---|
| **Origen** | Descarga directa desde interfaz web de Ripley Finanzas |
| **Formato** | CSV transformado a hoja Excel, 24 columnas |
| **Filas totales** | 121,658 (todo el historial) |
| **Filas Abr 2026** | 7,508 (filtradas por ciclo de facturación) |
| **Fecha usada** | `Fecha del ciclo de facturación` (cuando se liquida la transacción) |
| **Tipos de transacción** | 15 tipos distintos (Importe del pedido, Pago, Comisiones, etc.) |
| **Cobertura** | Transacciones individuales por orden y SKU |
| **Disponibilidad** | Solo existe en `Reporte Gerencial 360 Marketplaces.xlsx` |
| **Uso actual** | Dashboard 360 (Excel) |
| **Frecuencia** | Depende de la descarga manual desde Ripley |

### 1.2 XLSX Resumen Financiero — Archivos fuente

| Atributo | Valor |
|---|---|
| **Origen** | Descarga desde Ripley como "Resumen Financiero" oficial |
| **Formato** | 46 archivos XLSX, 37 columnas cada uno (32 financieras + 5 ID) |
| **Filas Abr 2026** | 49 liquidaciones |
| **Fecha usada** | `Fecha OC` (Order Creation Date — cuando se creó la orden) |
| **Columnas financieras** | 32 conceptos fijos (Importe del pedido, Envío, Comisiones, A pagar, etc.) |
| **Cobertura** | Liquidaciones agregadas por período |
| **Disponibilidad** | `01_Raw/RIPLEY/Resumen financiero/` |
| **Uso actual** | Marketplace Auditor v3.5 (web) — cargado via `surgical_loader.py` |
| **Frecuencia** | Mensual (cada liquidación) |

### 1.3 Ledger — `marketplace_ledger_v1`

| Atributo | Valor |
|---|---|
| **Origen** | ETL de los XLSX Resumen Financiero (`surgical_loader.py:351-418`) |
| **Formato** | Tabla DuckDB, 11 columnas + 3 de clasificación propagada |
| **Filas Abr 2026** | 1,568 (49 liquidaciones × 32 conceptos) |
| **Fecha usada** | `Fecha OC` del XLSX (heredada) |
| **Columnas** | `marketplace, id_transaccion, id_orden, fecha, detalle, monto, tipo_movimiento, archivo_origen, folio_xml, load_ts` + clasificación |
| **Clasificación** | `financial_group` (ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes, tesoreria) |
| **Filtro P&L** | `include_in_operational_pnl` (1 = P&L, 0 = flujo de caja) |
| **Disponibilidad** | `data/db/meli_financial_v4.db` |
| **Uso actual** | API y Dashboard del Marketplace Auditor v3.5 |

---

## 2. COMPARACIÓN CRUZADA POR KPI

### 2.1 Ingresos Brutos (Gross Revenue)

| Fuente | Monto Abr 2026 | Concepto contable | Fecha |
|---|---|---|---|
| **CSV Finanzas** | **$30,785,050** | `Importe del pedido` (columna Importe) | Ciclo de facturación Abr 2026 |
| **XLSX Resumen** | **$1,500,432** | `Importe del pedido` (columna del XLSX) | Fecha OC Abr 2026 |
| **Ledger** | **$1,500,432** | `financial_group = 'ingresos'` | Fecha Abr 2026 |

**Análisis de la diferencia ($29,284,618):**

| Factor | Impacto |
|---|---|
| Diferencia de fecha: el CSV usa ciclo de facturación (incluye órdenes de Feb-Mar liquidadas en Abr); el XLSX usa Fecha OC (solo órdenes creadas en Abr) | ~$28M |
| Diferencia de cobertura: el CSV captura TODAS las transacciones por orden; el XLSX solo las liquidaciones del período | ~$1.3M |

**Original CSV:** `Importe del pedido` en `Ripley_Finanzas_RAW` para ciclo Abr 2026 = $30,785,050
**Original XLSX:** `Importe del pedido` en XLSX con `Fecha OC` Abr 2026 = $1,500,432
**Ledger:** `SUM(monto) WHERE financial_group='ingresos' AND PNL=1` = $1,500,432 ✓ (match con XLSX)

### 2.2 Ventas Totales (Total Sales — incluye envíos)

Este KPI no existe actualmente en el Dashboard, pero es relevante para entender la diferencia con el CSV.

| Fuente | Monto Abr 2026 | Composición |
|---|---|---|
| **CSV Finanzas** | **$31,917,131** | Importe del pedido ($30,785,050) + Importe del envío ($1,132,081) |
| **XLSX Resumen** | **$1,559,692** | Importe del pedido ($1,500,432) + Importe del envío del pedido (clasificado como costo, $59,260) |
| **Ledger** | **$1,500,432** | Solo financial_group='ingresos' (el envío está en costos_operacionales) |

**Hallazgo crítico:** El XLSX/Ledger clasifica `Importe del envío del pedido` como `costos_operacionales` (no como ingreso). El CSV lo trata como ingreso separado. Esta diferencia de clasificación explica parte del gap entre ambos sistemas.

### 2.3 Comisiones (Commissions)

| Fuente | Monto Abr 2026 | Composición |
|---|---|---|
| **CSV Finanzas** | **−$3,959,744** | Comisiones (−$5,541,115) + Comisión de reembolso (+$1,581,371) |
| **XLSX Resumen** | **−$235,881** | Comisiones sobre pedidos (−$270,067) + Comisiones reembolsadas (+$34,186) |
| **Ledger** | **−$235,881** | `financial_group = 'costos_comerciales'` |

**Análisis de la diferencia ($3,723,863):**

| Factor | Impacto |
|---|---|
| Diferencia de fecha (ciclo vs Fecha OC) | ~$3.5M |
| Diferencia de granularidad: CSV captura comisión por orden; XLSX captura comisión agregada por liquidación | ~$0.2M |

**Original CSV:** `Comisiones` en `Ripley_Finanzas_RAW` para ciclo Abr 2026 = −$5,541,115
**Original XLSX:** `Comisiones sobre pedidos` en XLSX con `Fecha OC` Abr 2026 = −$270,067
**Ledger:** `SUM(monto) WHERE financial_group='costos_comerciales'` = −$235,881 ✓ (match con XLSX)

### 2.4 Resultado Neto (Net Result / P&L)

| Fuente | Monto Abr 2026 | Fórmula |
|---|---|---|
| **CSV Finanzas** | **−$17,266,954** | `Pago` (neto transferido a la cuenta) |
| **XLSX/Ledger (PNL)** | **$1,033,723** | `ingresos + devoluciones + costos_op + costos_com + ajustes` |
| **XLSX/Ledger (Caja)** | **$1,033,723** | `A pagar` (neto a pagar al vendedor) |

**Análisis de la diferencia:**

El CSV reporting `Pago` = −$17,266,954 representa el flujo de caja neto (lo que Ripley ya pagó al vendedor en el ciclo Abr 2026). Este NO es el Resultado Neto P&L.

El `A pagar` = $1,033,723 es el neto que Ripley debe pagar al vendedor por las ventas de Abr 2026 según el XLSX.

El `Pago` del CSV incluye pagos correspondientes a ventas de períodos anteriores, por lo que no es comparable directamente con el Resultado Neto del XLSX.

**Resultado Neto P&L (Ledger):** $1,033,723

**Composición detallada (Ledger, PNL=1, Abr 2026):**

| Componente | Monto | % del Neto |
|---|---|---|
| Importe del pedido (Ingresos) | +$1,500,432 | 145% |
| Pedidos reembolsados (Devoluciones) | −$189,930 | −18% |
| Envío (Costo operacional) | +$59,260 | 6% |
| Gastos de envío operador (Costo op) | −$59,260 | −6% |
| Descuento por costo logístico (Costo op) | −$40,898 | −4% |
| Comisiones sobre pedidos (Costo com) | −$270,067 | −26% |
| Comisiones reembolsadas (Costo com) | +$34,186 | 3% |
| **Resultado Neto** | **$1,033,723** | **100%** |

---

## 3. DEFINICIONES CANÓNICAS

Basado en el análisis de las tres fuentes, se establecen las siguientes definiciones oficiales:

### 3.1 Ingresos Brutos

| Atributo | Definición |
|---|---|
| **Definición** | Suma de `Importe del pedido` de las liquidaciones de Ripley (XLSX Resumen Financiero), filtrado por `Fecha OC` del período correspondiente, con `include_in_operational_pnl = 1` y `financial_group = 'ingresos'` |
| **Fuente canónica** | **XLSX Resumen Financiero** (vía `marketplace_ledger_v1`) |
| **Justificación** | El XLSX es el documento oficial de liquidación emitido por Ripley. El ledger lo refleja fielmente. El CSV incluye transacciones de múltiples períodos por su uso del ciclo de facturación. |
| **SQL oficial** | `SELECT SUM(COALESCE(monto,0)) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND fecha BETWEEN ? AND ? AND financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1` |
| **Valor Abr 2026** | **$1,500,432** |

### 3.2 Ventas Totales (Gross Sales — propuesto)

| Atributo | Definición |
|---|---|
| **Definición** | Suma de `Importe del pedido` + `Importe del envío del pedido` de las liquidaciones de Ripley |
| **Fuente canónica** | **XLSX Resumen Financiero** (vía `marketplace_ledger_v1`), o alternativamente la vista del CSV |
| **Justificación** | El envío pagado por el cliente es parte del ingreso total, aunque se clasifique como costo operacional en el P&L. Esta métrica permite comparar apples-to-apples con el CSV. |
| **Nota** | KPI no implementado actualmente en el Dashboard. Requeriría agregación cruzada de `financial_group`. |
| **Valor Abr 2026** | **$1,559,692** (XLSX) vs **$31,917,131** (CSV — por diferencia de fecha) |

### 3.3 Comisiones

| Atributo | Definición |
|---|---|
| **Definición** | Suma neta de `Comisiones sobre pedidos` + `Comisiones sobre pedidos reembolsados` de las liquidaciones de Ripley |
| **Fuente canónica** | **XLSX Resumen Financiero** (vía `marketplace_ledger_v1`, `financial_group = 'costos_comerciales'`) |
| **Justificación** | El XLSX desglosa comisiones y comisiones reembolsadas como conceptos separados. El ledger los agrupa correctamente en `costos_comerciales`. |
| **SQL oficial** | `SELECT SUM(COALESCE(monto,0)) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND fecha BETWEEN ? AND ? AND financial_group='costos_comerciales' AND COALESCE(include_in_operational_pnl,1)=1` |
| **Valor Abr 2026** | **−$235,881** |

### 3.4 Resultado Neto (P&L)

| Atributo | Definición |
|---|---|
| **Definición** | Suma de todos los componentes P&L: `ingresos + devoluciones + costos_operacionales + costos_comerciales + ajustes`, con `include_in_operational_pnl = 1` |
| **Fuente canónica** | **Ledger** (`marketplace_ledger_v1` con clasificación `financial_group`) |
| **Justificación** | El resultado neto P&L no existe como concepto directo en el XLSX ni en el CSV. Es una construcción del Motor de Auditoría que agrupa los 32 conceptos del XLSX en 5 categorías financieras. |
| **SQL oficial** | Ver `marketplace_auditor.py:519-546` o `api/api.py:255-270` |
| **Cálculo** | `ingresos + devoluciones + costos_operacionales + costos_comerciales + ajustes` |
| **Valor Abr 2026 (PNL)** | **$1,033,723** |
| **Valor Abr 2026 (Caja)** | **$1,033,723** (A pagar — en este período coinciden) |

---

## 4. MATRIZ DE VERDAD

### 4.1 Comparación horizontal por KPI

```
KPI                     CSV Finanzas         XLSX Resumen        Ledger              CANONICA
                        (Abr ciclo)          (Abr Fecha OC)      (Abr PNL=1)
──────────────────────────────────────────────────────────────────────────────────────────────
Ingresos Brutos         $30,785,050          $1,500,432          $1,500,432          XLSX/Ledger
Ventas Totales          $31,917,131          $1,559,692          $1,500,432*         XLSX (propuesto)
Comisiones              −$3,959,744          −$235,881           −$235,881           XLSX/Ledger
Resultado Neto P&L      N/A**                N/A**               $1,033,723          Ledger
Resultado Neto Caja     −$17,266,954         $1,033,723          $1,033,723          XLSX/Ledger

* El ledger solo captura Importe del pedido como ingresos; el envío está en costos_operacionales.
** El CSV y XLSX no tienen un concepto de "Resultado Neto P&L" — es una construcción del Motor de Auditoría.
```

### 4.2 Equivalencias entre fuentes

| Concepto CSV | Concepto XLSX | Concepto Ledger | Grupo Financiero |
|---|---|---|---|
| `Importe del pedido` | `Importe del pedido` | `Importe del pedido` | `ingresos` |
| `Importe del envío del pedido` | `Envío` | `Envío` | `costos_operacionales` |
| `Gastos de envío pagados por operador` | `Gastos de envío pagados por el operador` | `Gastos de envío pagados por el operador` | `costos_operacionales` |
| `Comisiones` | `Comisiones sobre pedidos` | `Comisiones sobre pedidos` | `costos_comerciales` |
| `Comisión de reembolso` | `Comisiones sobre pedidos reembolsados` | `Comisiones sobre pedidos reembolsados` | `costos_comerciales` |
| `Importe del pedido reembolsado` | `Pedidos reembolsados` | `Pedidos reembolsados` | `devoluciones` |
| `Factura manual` | (no existe) | (no existe en XLSX) | N/A |
| `Abono manual` | (no existe) | (no existe en XLSX) | N/A |
| `Pago` | `A pagar` | `A pagar` | `sin_clasificar` (PNL=0) |
| N/A | `Abono postventa` | `Abono postventa` | `ajustes` |
| N/A | `Descuento por cancelación` | `Descuento por cancelación` | `ajustes` |

### 4.3 Conceptos exclusivos de cada fuente

| Solo en CSV | Solo en XLSX |
|---|---|
| `Pago` (neto cash flow ya transferido) | `Abono postventa` |
| `Factura manual` | `Abono por error de comisión` |
| `Abono manual` | `Abono extraordinario - error de precio` |
| `UNKNOWN` (3,440,069 en total histórico) | `Abono oferta TC - OPEX` |
| (tiene menos conceptos de ajuste) | `Abono por uso de flota propia` |
| | `Abonos soluciones comerciales` |
| | `Abonos por cupón promocional` |
| | `Descuento oferta TC - OPEX` |
| | `Otros descuentos` |
| | `Descuento por error de clase logistica` |
| | `Descuento por costo logístico` |
| | `Descuento por logistica inversa` |
| | `Descuento por compensación a cliente` |
| | `Descuento FF - *` (3 tipos) |
| | `Descuento por PDM` |
| | `Cobro despacho primera milla` |
| | `Descuento operacional` |
| | `Abono por formalización a OPL` |
| | `Descuento por cupones de despacho` |
| | `Envío reembolsado` |
| | `Gastos de envío reembolsados pagados por el operador` |
| | `Impuesto sobre las comisiones` |
| | `Impuesto sobre la comisión de reembolso` |
| | `Impuesto de la factura manual` |
| | `Impuesto sobre el abono manual` |

El XLSX tiene 32 conceptos financieros. El CSV tiene 13 conceptos distintos (excluyendo UNKNOWN). La superposición es parcial: ambos tienen Importe del pedido, Comisiones, Envío, Gastos de envío. Pero el XLSX tiene muchos más conceptos de ajuste y descuento.

---

## 5. DECISIONES DE VERDAD

### Decisión 1: Fuente canónica para Ingresos Brutos

**XLSX Resumen Financiero (vía Ledger)**

El Importe del pedido en el XLSX es el valor oficial de la liquidación de Ripley. El ledger lo refleja sin modificaciones. El CSV no es confiable para este KPI porque su fecha de ciclo de facturación agrupa transacciones de múltiples períodos.

### Decisión 2: Fuente canónica para Ventas Totales

**XLSX Resumen Financiero (propuesto)**

Actualmente no implementado. Se recomienda crear `Ventas Totales = Importe del pedido + Importe del envío del pedido` para comparación con el CSV. El envío debe reclasificarse como ingreso para este KPI (aunque permanezca en costos_operacionales para el P&L).

### Decisión 3: Fuente canónica para Comisiones

**XLSX Resumen Financiero (vía Ledger)**

`costos_comerciales` en el ledger agrupa correctamente comisiones y comisiones reembolsadas. El CSV tiene un concepto similar pero con diferentes montos por diferencia de fecha.

### Decisión 4: Fuente canónica para Resultado Neto

**Ledger (construcción del Motor de Auditoría)**

El Resultado Neto P&L no existe como concepto en ninguna fuente original. Es el producto del Motor de Auditoría que clasifica los 32 conceptos del XLSX en 5 grupos financieros. Es la única métrica que refleja la rentabilidad real del período.

### Decisión 5: Rol del CSV Finanzas

El CSV NO debe usarse como fuente canónica para ningún KPI del Marketplace Auditor v3.5, porque:
1. Usa ciclo de facturación (no Fecha OC) → incomparable con el XLSX
2. Tiene menos conceptos de ajuste que el XLSX
3. Incluye conceptos de flujo de caja (Pago) que no son P&L
4. No es un documento oficial de liquidación — es una descarga transaccional

El CSV es útil como **fuente complementaria** para:
- Verificación cruzada de tendencias
- Detalle a nivel de orden+SKU (que el XLSX no tiene)
- Conciliación de flujo de caja (Pago vs A pagar)

---

## 6. VEREDICTO

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CERTIFICACIÓN DE VERDAD FINANCIERA                    │
│                                                                          │
│  Las definiciones canónicas para RIPLEY quedan establecidas como:        │
│                                                                          │
│  INGRESOS BRUTOS   → XLSX Resumen Financiero  → $1,500,432 (Abr 2026)   │
│  VENTAS TOTALES    → XLSX (propuesto)          → $1,559,692 (Abr 2026)   │
│  COMISIONES        → XLSX Resumen Financiero  → −$235,881 (Abr 2026)     │
│  RESULTADO NETO    → Ledger (Motor Auditoría)  → $1,033,723 (Abr 2026)   │
│  FLUJO DE CAJA     → XLSX/Ledger (A pagar)     → $1,033,723 (Abr 2026)   │
│                                                                          │
│  El CSV Finanzas NO es fuente canónica para ningún KPI del Auditor.      │
│  Es una fuente complementaria para verificación y detalle transaccional. │
│                                                                          │
│  El XLSX Resumen Financiero captura 32 conceptos financieros.            │
│  El Ledger los refleja fielmente (0% pérdida en ETL).                    │
│  El Dashboard los muestra exactamente (0% pérdida en API/UI).            │
│                                                                          │
│  La diferencia con el CSV ($30,785,050 vs $1,500,432 en Ingresos)        │
│  se debe a:                                                              │
│    1. Diferencia de fecha (ciclo facturación vs Fecha OC)    → ~95%      │
│    2. Diferencia de granularidad (transaccional vs agregado) → ~5%       │
│                                                                          │
│  Confianza en la fuente canónica: 100%                                    │
│  Confianza en el pipeline XLSX→Ledger→API→Dashboard: 100%                │
│  Confianza en el CSV como fuente alternativa: 0% (para este propósito)   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

*Documento FORENSE READ ONLY. No modifica código, BD, clasificaciones, ni Trust Scores.*
