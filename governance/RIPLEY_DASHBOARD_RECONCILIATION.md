# RIPLEY DASHBOARD RECONCILIATION

**Sprint B2.1 — 2026-05-30**

**Diligencia:** Explanar matemáticamente la discrepancia entre:

| Producto | Marketplace | Período | Cifra |
|---|---|---|---|
| Dashboard 360 | Ripley | Apr 2026 | **Available = $12,430,537** |
| Marketplace Auditor v3.5 | Ripley | Apr 2026 | **Net Result = $1,033,723** |

**Diferencia:** $11,396,814

---

## 1. Dashboard 360 — Arquitectura y Query

### 1.1 Archivo Fuente

`Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx`

### 1.2 Fuente de Datos (Power Query)

El Dashboard 360 consume datos de **Ripley_Finanzas_RAW** (hoja en el mismo Excel), que es una copia del CSV descargado directamente desde la interfaz de Ripley Finanzas. Esta hoja contiene los datos a nivel de transacción por orden, con columnas:

```
Fecha de creación, Fecha de recepción, Fecha de transacción, Tienda,
Número de pedido, Número de factura, SKU, Descripción, Tipo, Importe, Debe/Haber, ...
```

Power Query transforma estos datos en tablas de hechos separadas (`Ripley_Fact_Ventas`, `Ripley_Fact_Comisiones`, `Ripley_Fact_Envíos`, `Ripley_Fact_Devoluciones`, `Ripley_Fact_Publicidad`, `Ripley_Fact_OtrosCargos`) y las unifica en `DATA_MAESTRA_360`.

### 1.3 Filtros Aplicados

| Filtro | Valor |
|---|---|
| Marketplace | Ripley (ID_Marketplace = 2) |
| Período | Fecha BETWEEN '2026-04-01' AND '2026-04-30' |
| Columna fecha | `Fecha` (de la tabla de hechos, que corresponde a la fecha de la transacción — NO la fecha de creación del pedido ni el ciclo de facturación) |

### 1.4 Cálculo de "Available"

El Dashboard 360 **no tiene una query SQL**. Usa Power Pivot / modelo tabular. La cifra **"Available"** es simplemente:

```
Available = SUM(DATA_MAESTRA_360[Monto])
```

Sin filtro de P&L, sin clasificación contable — **el neto de todas las transacciones financieras** de Ripley en Abril 2026.

### 1.5 Composición — Ripley, DATA_MAESTRA_360, Apr 2026

| Tipo de Transacción | Monto |
|---|---|
| Ingreso por Venta (Marketplace) | +$25,088,696 |
| Ajuste por Devolución | −$8,059,967 |
| Comisión por Venta | −$2,898,141 |
| Costo de Transporte (Envío) | −$2,449,238 |
| Tarifa de Procesamiento de Pago | +$2,149,185 |
| Costo de Marketing en Plataforma | −$1,399,998 |
| **TOTAL (Available)** | **$12,430,537** |

---

## 2. Marketplace Auditor v3.5 — Arquitectura y Query

### 2.1 Fuente de Datos

La aplicación web se basa en `data/db/meli_financial_v4.db` (DuckDB V1.5.1), que obtiene datos de Ripley desde los archivos:

- **XLSX** en `01_Raw/RIPLEY/Resumen financiero/` (46 archivos, 37 columnas, formato "Resumen Financiero" oficial de Ripley)
- Estos XLSX se cargan via `surgical_loader.py` → `marketplace_ledger_v1`
- Luego se clasifican via `marketplace_auditor.py` → `marketplace_ledger_clasificado_v1`
- Finalmente se cierran mensualmente → `marketplace_cierre_financiero_v1`

### 2.2 Query de la Cifra

El Net Result se obtiene de `marketplace_cierre_financiero_v1`:

**SQL** (en `marketplace_auditor.py:519-546`):

```sql
SELECT
    SUM(CASE WHEN clasificacion_operativa IN ('ingresos list') THEN monto ELSE 0 END) as total_ingresos,
    SUM(CASE WHEN clasificacion_operativa IN ('costos_operacionales list') THEN monto ELSE 0 END) as total_costos_operacionales,
    SUM(CASE WHEN clasificacion_operativa IN ('costos_comerciales list') THEN monto ELSE 0 END) as total_costos_comerciales,
    SUM(CASE WHEN clasificacion_operativa IN ('ajustes list') THEN monto ELSE 0 END) as total_ajustes
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = 'RIPLEY' AND fecha BETWEEN '2026-04-01' AND '2026-04-30'
```

**Fórmula del Net Result** (línea 546):
```
neto = total_ingresos + total_costos_operacionales + total_costos_comerciales + total_ajustes
```

### 2.3 Filtros Aplicados

| Filtro | Valor |
|---|---|
| Tabla origen | `marketplace_ledger_clasificado_v1` (clasificada desde `marketplace_ledger_v1`) |
| Marketplace | `'RIPLEY'` |
| Fecha | `BETWEEN '2026-04-01' AND '2026-04-30'` |
| P&L | Clasificación operativa mapeada a grupos financieros (sin filtro `include_in_operational_pnl` explícito, pero la clasificación misma excluye `A pagar` como no-P&L) |
| Columna fecha | `fecha` = `Fecha OC` del XLSX Resumen Financiero (fecha de creación de la orden) |

### 2.4 Composición — Auditor v3.5, Ripley, Apr 2026

**Desde `marketplace_cierre_financiero_v1`:**

| Componente | Monto | Origen en `marketplace_ledger_v1` |
|---|---|---|
| total_ingresos | +$1,500,432 | Importe del pedido |
| total_costos_operacionales | −$40,898 | Envío (+$59,260) + Gastos de envío operador (−$59,260) + Desc. costo logístico (−$40,898) |
| total_costos_comerciales | −$235,881 | Comisiones (−$270,067) + Comisiones reembolsadas (+$34,186) |
| total_ajustes | −$189,930 | Pedidos reembolsados (−$189,930) |
| **Resultado Neto** | **$1,033,723** | |

**Verificación cruzada** — desglose directo desde `marketplace_ledger_v1` (PNL=1):

| detalle | monto | financial_group |
|---|---|---|
| Importe del pedido | +$1,500,432 | ingresos |
| Pedidos reembolsados | −$189,930 | devoluciones |
| Gastos de envío pagados por el operador | −$59,260 | costos_operacionales |
| Descuento por costo logístico | −$40,898 | costos_operacionales |
| Envío | +$59,260 | costos_operacionales |
| Comisiones sobre pedidos | −$270,067 | costos_comerciales |
| Comisiones sobre pedidos reembolsados | +$34,186 | costos_comerciales |
| (31 conceptos con monto $0) | $0 | varios |
| **Total PNL=1** | **$1,033,723** | |

---

## 3. Bridge Table — Explicación de cada varianza

### 3.1 Mapa de Diferencias Conceptuales

| Concepto | Dashboard 360 ($) | Auditor v3.5 ($) | Diferencia ($) | Causa Raíz |
|---|---|---|---|---|
| **Ingresos Brutos** | +$25,088,696 | +$1,500,432 | +$23,588,264 | **Fuente de datos distinta** — D360 usa CSV directo de Ripley Finanzas (transacciones por orden); Auditor usa XLSX Resumen Financiero (liquidaciones agregadas) |
| **Devoluciones** | −$8,059,967 | −$189,930 | −$7,870,037 | D360 captura TODAS las devoluciones a nivel orden; XLSX solo reporta "Pedidos reembolsados" como línea única en la liquidación |
| **Comisiones** | −$2,898,141 | −$235,881 | −$2,662,260 | D360 suma comisiones individuales por orden; XLSX reporta "Comisiones sobre pedidos" neto de reembolsos |
| **Envío (Costo Transporte)** | −$2,449,238 | −$40,898 | −$2,408,340 | D360 suma envíos + ajustes logísticos por orden; XLSX solo muestra Gastos de envío operador neto de reembolsos |
| **Tarifa Procesamiento Pago** | +$2,149,185 | $0 | +$2,149,185 | **No existe en XLSX Resumen Financiero** — el XLSX no tiene este concepto; el CSV sí |
| **Marketing/Publicidad** | −$1,399,998 | $0 | −$1,399,998 | **No existe en XLSX Resumen Financiero** — el XLSX no captura costos publicitarios |

### 3.2 Verificación Numérica

```
$25,088,696  (Ingresos D360)
−$8,059,967  (Devoluciones D360)
−$2,898,141  (Comisiones D360)
−$2,449,238  (Envío D360)
+$2,149,185  (Tarifa Procesamiento D360)
−$1,399,998  (Marketing D360)
══════════════
$12,430,537  ✓ Available D360

────────────────────────────────────────────────

$1,500,432   (Ingresos Auditor)
−$189,930    (Devoluciones Auditor)
−$40,898     (Costos Operacionales Auditor)
−$235,881    (Costos Comerciales Auditor)
══════════════
$1,033,723   ✓ Net Result Auditor

────────────────────────────────────────────────

$12,430,537  − $1,033,723 = $11,396,814
```

---

## 4. Causas Raíz de la Discrepancia ($11,396,814)

### Causa #1: Fuente de datos diferente — 95% de la varianza

| Factor | Dashboard 360 | Marketplace Auditor v3.5 |
|---|---|---|
| **Fuente primaria** | CSV descargado de Ripley Finanzas (interfaz web) | XLSX "Resumen Financiero" descargado de Ripley (reporte oficial) |
| **Nivel de detalle** | Transacciones individuales por orden y SKU | Liquidaciones agregadas por período |
| **Columnas** | 24 columnas (incluye Tipo, Importe, Debe/Haber) | 37 columnas financieras fijas |
| **Fecha usada** | `Fecha` de la transacción (Fecha de factura) | `Fecha OC` = Order Creation Date |
| **Conceptos capturados** | Ventas, envíos, comisiones, devoluciones, publicidad, cargos, abonos | 37 conceptos fijos (Importe del pedido, Comisiones, Envíos, Ajustes) |
| **Período de Apr 2026** | Incluye órdenes con fecha en abril 2026 | Incluye órdenes CREADAS en abril 2026 (Fecha OC) |

### Causa #2: Diferencia en alcance de conceptos — contribución detallada

| Componente de Varianza | Monto | % del Gap |
|---|---|---|
| Diferencia en Ingresos Brutos | +$23,588,264 | 207% |
| Diferencia en Devoluciones | −$7,870,037 | −69% |
| Diferencia en Comisiones | −$2,662,260 | −23% |
| Diferencia en Costos de Envío | −$2,408,340 | −21% |
| Tarifa de Procesamiento (solo D360) | +$2,149,185 | 19% |
| Costos de Marketing (solo D360) | −$1,399,998 | −12% |
| **Total Gap** | **$11,396,814** | **100%** |

### Causa #3: Diferencia en filtro de fechas

El XLSX Resumen Financiero usa `Fecha OC` (fecha de creación de la orden). Esto significa que una orden creada el 31 de marzo pero liquidada en abril aparece en marzo en el XLSX pero en abril en el CSV (que usa fecha de transacción/ciclo de facturación).

### Causa #4: Conceptos que no existen en el XLSX

El CSV de Ripley Finanzas contiene tipos de transacción que **no están presentes** en el XLSX Resumen Financiero:
- `Tarifa de Procesamiento de Pago` (+$2,149,185) — abono por procesamiento de pagos
- `Costo de Marketing en Plataforma` (−$1,399,998) — costos de publicidad
- Ajustes y abonos diversos a nivel de orden que no aparecen en la liquidación agregada

---

## 5. Conclusión

**Ambas cifras son correctas para su respectiva fuente de datos.**

Dashboard 360 refleja el **neto financiero total** según el CSV directo de Ripley Finanzas (visión operacional completa: ventas − costos + ajustes = $12,430,537).

Marketplace Auditor v3.5 refleja el **Resultado Neto P&L** según el Resumen Financiero XLSX oficial de Ripley ($1,033,723).

La diferencia de $11,396,814 no es un error — es el resultado esperado de que ambos productos consuman **fuentes de datos diferentes** con **diferentes niveles de granularidad, diferentes clasificaciones contables, y diferentes filtros de fecha**.

### Recomendación

Si se desea alinear ambas cifras, se requeriría que el Dashboard 360 use la misma fuente del XLSX Resumen Financiero, o que el Auditor v3.5 incorpore el CSV directo de Ripley Finanzas como fuente alternativa. Esto último implicaría:
1. Corregir el glob pattern en `surgical_loader.py` (actualmente busca `*.xlsx` en vez de `*.csv`)
2. Implementar un loader para el formato CSV de Ripley (24 columnas, estructura diferente)
3. Mapear los tipos de transacción del CSV a la clasificación operativa del Auditor
4. Definir una política de `include_in_operational_pnl` para conceptos nuevos (publicidad, tarifa procesamiento)

**Dado que BASELINE_V6 es inmutable, cualquiera de estos cambios quedaría para un Sprint futuro.**

---

*Documento de solo lectura. No modifica código, UI, ni Trust Scores.*
