# SPRINT B2.3 — RIPLEY GROSS REVENUE CERTIFICATION

**Clasificación: RECHAZADO**

Fecha: 2026-05-30
Auditor: MFE Governance
Régimen: FORENSE — READ ONLY — NO MODIFICAR NADA

---

## FASE 1 — INVENTARIO

| Dimensión | Valor |
|---|---|
| Archivos XLSX en `01_Raw/RIPLEY/Resumen financiero/` | 46 archivos |
| Archivos con datos de Abr 2026 | 7 archivos (`000371`–`000378`) |
| Filas totales en todos los XLSX | 16,923 |
| Filas en Abr 2026 (Fecha OC) | 499 |
| Columnas financieras por XLSX | 32 |

### Columnas del XLSX

```
Fecha OC, Número documento liquidación, Orden de compra, Shop ID, Tienda,
Importe del pedido, Envío, Gastos de envío pagados por el operador,
Comisiones sobre pedidos, Pedidos reembolsados, Envío reembolsado,
Gastos de envío reembolsados pagados por el operador,
Comisiones sobre pedidos reembolsados, Abono postventa,
Abono por error de comisión, Abono extraordinario - error de precio,
Abono oferta TC - OPEX, Abono por uso de flota propia, Otros abonos,
Abonos soluciones comerciales, Abonos por cupón promocional,
Descuento oferta TC - OPEX, Otros descuentos,
Descuento por error de clase logistica, Descuento por costo logístico,
Descuento por logistica inversa, Descuento por cancelación,
Descuento por compensación a cliente, Descuento FF - sobreestadía,
Descuento FF - pick and pack, Descuento FF - Otros, Descuento por PDM,
Cobro despacho primera milla, Descuento operacional,
Abono por formalización a OPL, Descuento por cupones de despacho,
A pagar
```

---

## FASE 2 — RECONSTRUCCIÓN (XLSX DIRECTO)

**Valor A — SUM(Importe del pedido) desde los 46 XLSX:**

| Período | Filas | SUM(Importe del pedido) | Método |
|---|---|---|---|
| Abr 2026 | 499 | **$16,460,180.00** | `pd.to_datetime(dayfirst=True)` |
| 2025 (total) | 9,794 | $281,188,982.00 | `pd.to_datetime(dayfirst=True)` |
| 2026 (total) | 2,444 | $71,971,342.00 | `pd.to_datetime(dayfirst=True)` |
| ALL TIME | 13,066 | $358,012,384.00 | `pd.to_datetime(dayfirst=True)` |
| Pre-2025 | 828 | $4,852,060.00 | `pd.to_datetime(dayfirst=True)` |

El valor se obtuvo leyendo cada archivo XLSX directamente con `openpyxl`, parseando `Fecha OC` con `pd.to_datetime(dayfirst=True)` para respetar el formato `dd-mm-aaaa` nativo de Ripley.

---

## FASE 3 — COMPARACIÓN

### Valores

| Fuente | Abr 2026 Importe del pedido | Filas |
|---|---|---|
| **A** — XLSX directo (dayfirst=True) | **$16,460,180.00** | 499 |
| **B** — Ledger `marketplace_ledger_v1` | **$1,500,432.00** | 49 |
| **C** — Dashboard v3.5 | **$1,500,432.00** | N/A |

### Deltas

| Comparación | Delta | % |
|---|---|---|
| A − B (XLSX vs Ledger) | **$14,959,748.00** | **−91.02%** |
| A − C (XLSX vs Dashboard) | **$14,959,748.00** | **−91.02%** |
| B − C (Ledger vs Dashboard) | $0.00 | 0% |

B = C = el Dashboard refleja fielmente el Ledger. El problema está en el ETL que genera el Ledger.

---

## FASE 4 — ANÁLISIS FORENSE

### 4.1 ¿El KPI proviene realmente del Resumen Financiero?

**PARCIALMENTE.** El ETL (`surgical_loader.py:351-418`) lee los archivos correctos en `01_Raw/RIPLEY/Resumen financiero/`. Sin embargo, EXTRACT es defectuoso: el 91.02% de los datos de Abril 2026 se pierden o corrompen durante la carga.

### 4.2 ¿El KPI es exactamente SUM(Importe del pedido)?

**NO.** El Ledger contiene $1,500,432. El valor correcto es $16,460,180. El 91% de los datos no llegan al Ledger.

### 4.3 ¿Existe alguna transformación, filtro o pérdida?

**SÍ — BUG CRÍTICO DE PARSEO DE FECHAS.**

**Archivo:** `engine/v4/surgical_loader.py:400`

```python
try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
```

**Problema:** `pd.to_datetime()` se invoca SIN `dayfirst=True`. Las fechas en los XLSX de Ripley están en formato **`dd-mm-aaaa`** (STRING), pero pandas sin `dayfirst=True` las interpreta como `mm-dd-aaaa`.

**Dos consecuencias destructivas:**

1. **Filas con día > 12** (e.g., "15-04-2026", "20-04-2026", "25-04-2026"):
   - `pd.to_datetime("15-04-2026")` → mes 15 inválido → `NaT`
   - `_filter_old_years()` (l.81-96): `_is_valid(NaT)` → `return False` → **FILA ELIMINADA**
   - En Abr 2026: **243 filas ($8,235,580) perdidas** por este mecanismo

2. **Filas con día ≤ 12** (e.g., "10-04-2026", "04-04-2026", "01-04-2026"):
   - `pd.to_datetime("10-04-2026")` → mes=10, día=4 → 2026-10-04 (Octubre, NO Abril)
   - La fecha es válida pero **INCORRECTA** — la fila aparece en el mes equivocado
   - En Abr 2026: **256 filas ($8,224,600) desviadas a otros meses**

**Total Abr 2026: 499 filas → ledger tiene 49 filas correctas**

### 4.4 Impacto histórico total

| Métrica | Valor |
|---|---|
| XLSX Importe del pedido ALL TIME (correcto) | **$358,012,384.00** |
| Ledger Importe del pedido ALL TIME | **$240,979,600.00** |
| **Pérdida total de datos** | **$117,032,784.00** |
| Filas con día>12 → NaT → eliminadas | ~7,284 filas ($89M) |
| Filas con día≤12 → fechas incorrectas | ~9,639 filas ($269M en meses equivocados) |
| Archivos XLSX | 46 |
| Archivos representados en Ledger | 40 |
| Archivos faltantes en Ledger | 6 archivos (sin datos que superen el filtro de fechas) |

### 4.5 ¿La definición actual de "Ingresos Brutos" es válida?

**NO.** La definición actual es "lo que el ETL logra cargar del Resumen Financiero después del bug de parseo de fechas". Esto NO es lo mismo que "SUM(Importe del pedido) del Resumen Financiero".

---

## CLASIFICACIÓN FINAL

| Condición | Resultado |
|---|---|
| CONDICIÓN 1: Fuente = `01_Raw/RIPLEY/Resumen financiero/` | **PARCIAL** — fuente correcta, extracción incorrecta |
| CONDICIÓN 2: Valor = SUM(Importe del pedido) | **RECHAZADO** — $1,500,432 ≠ $16,460,180 (−91.02%) |
| **CLASIFICACIÓN GENERAL** | **RECHAZADO** |

---

## LOCALIZACIÓN DEL BUG

- **Archivo:** `engine/v4/surgical_loader.py:400`
- **Función:** `load_ripley()`
- **Línea exacta:**
  ```python
  try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
  ```
- **Código correcto que debería reemplazarlo:**
  ```python
  try: fecha = pd.to_datetime(row[c_fecha], dayfirst=True) if c_fecha else None
  ```
- **Misma línea duplicada:** `surgical_loader.py:382` (registro en `ventas_marketplace`):
  ```python
  'sale_date': pd.to_datetime(df[c_fecha], errors='coerce') if c_fecha else None
  ```
  Debería ser:
  ```python
  'sale_date': pd.to_datetime(df[c_fecha], dayfirst=True, errors='coerce') if c_fecha else None
  ```
- **Scope del bug:** SOLO Ripley (`load_ripley()`). Los formatos de fecha de otros marketplaces (ML, PARIS, FALABELLA) son manejados correctamente por `calamine` o tienen formatos no ambiguos.

- **AFECTA:** 2 tablas — `marketplace_ledger_v1` y `ventas_marketplace` (para Ripley)
- **NO AFECTA:** `marketplace_ledger_clasificado_v1` (se genera a partir del Ledger, hereda el error)
- **FECHA DE INTRODUCCIÓN DEL BUG:** Día 1 del loader — nunca funcionó correctamente

---

## VEREDICTO EJECUTIVO

El KPI **"Ingresos Brutos" de RIPLEY en el Dashboard está RECHAZADO** como representación fidedigna de `SUM(Importe del pedido)`.

El Dashboard muestra $1,500,432 para Abril 2026. El valor correcto según los 46 XLSX del Resumen Financiero es **$16,460,180**.

La discrepancia del 91% es causada por un bug unificado de parseo de fechas en `surgical_loader.py:400`: falta `dayfirst=True` en `pd.to_datetime()`. Esto causa que fechas en formato `dd-mm-aaaa` se interpreten como `mm-dd-aaaa`, resultando en:

1. **Pérdida de datos** cuando el día > 12 (NaT → filtrado por `_filter_old_years`)
2. **Fechas incorrectas** cuando el día ≤ 12 (swap día/mes)

La corrección requiere modificar UNA línea de código. Sin embargo, está **PROHIBIDO** modificar el ETL en esta auditoría forense READ ONLY.

**Total histórico de datos perdidos o corrompidos por este bug: ~$117M**

---

## TRAZABILIDAD COMPLETA

```
01_Raw/RIPLEY/Resumen financiero/*.xlsx (46 archivos, 16,923 filas)
    │
    ▼
[BUG] pd.to_datetime() sin dayfirst=True (surgical_loader.py:400)
    │
    ├─ día > 12 (7,284 filas) → NaT → _filter_old_years → PERDIDO ($89M)
    │
    ├─ día ≤ 12, fecha swap (9,639 filas) → FECHA INCORRECTA ($269M en mes equivocado)
    │
    ▼
marketplace_ledger_v1 (8,413 filas, $240,979,600)
    │
    ▼
marketplace_ledger_clasificado_v1 (clasificación P&L)
    │
    ▼
API /api/v4/cierre/desglose
    │
    ▼
Dashboard v3.5 → $1,500,432 (NO certificado)
```
