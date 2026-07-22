# PARIS Field Mapping V2 — MONTO_A_PAGAR Usage

**Fecha:** 2026-06-11
**FASE 2 de 7 — RFC PARIS Implementation**

---

## 1. Source de Verdad

Los archivos XLSX en `01_Raw/PARIS/Transacciones/` contienen las siguientes columnas relevantes:

| Columna XLSX | Contenido | Ejemplo | 
|-------------|-----------|---------|
| `id` | ID único de transacción | `14693770` |
| `tipo` / `descripción` | Tipo de transacción | `Venta`, `Devolución`, `Cobro por despacho` |
| `número orden` / `nro orden` | ID de orden | `307752156` |
| `monto a pagar` | **Neto liquidado** (MONTO_A_PAGAR) | `13,592` |
| `monto` | **Valor bruto** (MONTO) | `15,990` |
| `comisión` | Comisión explícita ($15 fijo) | `0` o `2,398` |
| `fecha` | Fecha de transacción | `2026-06-01` |
| `número factura` / `factura` | Folio XML/Documento | `123456` |

## 2. Estado Actual

### 2.1 Cómo se Almacena en DB

| Tabla | Campo | Valor Actual | Origen |
|-------|-------|-------------|--------|
| `marketplace_ledger_v1` | `monto` | **MONTO_A_PAGAR** (neto) | Loader L303: `['monto a pagar', 'monto']` |
| `marketplace_ledger_clasificado_v1` | `monto` | **MONTO_A_PAGAR** (neto) | Copiado desde `marketplace_ledger_v1` |
| `marketplace_cierre_financiero_v1` | `total_ingresos` | **SUM(MONTO_A_PAGAR)** para Ventas | Clasificación → closing |

### 2.2 Dónde se Usa `monto` (= MONTO_A_PAGAR) para PARIS

| Componente | Archivo | Línea | Uso |
|-----------|---------|-------|-----|
| Loader | `surgical_loader.py` | 303, 331 | `c_monto = get_col_name(df, ['monto a pagar', 'monto'])` — selecciona MONTO_A_PAGAR |
| Loader | `surgical_loader.py` | 338 | `monto: monto` — escribe como `monto` en ledger |
| Clasificación | `marketplace_auditor.py` | 355 | `SELECT monto FROM marketplace_ledger_v1` — lee monto para clasificar |
| Clasificación | `marketplace_auditor.py` | 469 | INSERT en clasificado_v1 con mismo monto |
| Closing | `marketplace_auditor.py` | 554-561 | `SUM(CASE WHEN ... THEN monto ELSE 0 END)` — suma por grupo financiero |
| Cierre fórmula | `marketplace_auditor.py` | 572 | `resultado_neto = ing + dev + cop + ccm + aju` |
| API `/api/v4/ledger` | `api.py` | 145-219 | `SELECT * FROM marketplace_ledger_v1` — monto devuelto sin transformación |
| API `/api/v4/cierre` | `api.py` | 221-238 | `SELECT total_ingresos, resultado_neto FROM cierre_financiero_v1` |
| API `/api/v4/cierre/desglose` | `api.py` | 240-294 | `SELECT financial_group, SUM(monto)` — suma de monto por grupo |
| API `/api/v4/exec/summary` | `api.py` | 496-572 | `total_ingresos` de cierre + SUM(monto) para devoluciones |
| API `/api/v4/exec/waterfall` | `api.py` | 575-633 | CASE WHEN por financial_group con SUM(monto) |
| API `/api/v4/exec/cobros-breakdown` | `api.py` | 636-703 | SUM(monto) para costos operacionales y ajustes |
| API `/api/v4/exec/ux12_summary` | `api.py` | 832-945 | CASE WHEN agrupación por grupo con SUM(monto) |
| Frontend dashboard | `dashboard.html` | ~900 | `window._cierreCertified` values de API |
| Frontend executive | `executive_dashboard.html` | ~340-348 | `ux12Data.financial_pnl.gross_sales` de API |

## 3. Mapeo Objetivo

| Variable | Alias DB | Origen | Destino |
|----------|---------|--------|---------|
| Venta Bruta | `monto_bruto` | XLSX `monto` (MONTO) | Nuevo campo en ledger |
| Comisión Marketplace | `comision_marketplace` | Calculado: `MONTO - MONTO_A_PAGAR` | Nuevo campo en ledger |
| Neto Liquidado | `monto` (existente) | XLSX `monto a pagar` (MONTO_A_PAGAR) | `monto` — sin cambios |
| Venta Bruta (agregada) | `venta_bruta` | Calculado: SUM(`monto_bruto`) para ingresos PARIS | API endpoint |
| Comisión (agregada) | `comision_marketplace_total` | Calculado: SUM(`comision_marketplace`) para PARIS | API endpoint |

## 4. Impacto por Tabla

### 4.1 `marketplace_ledger_v1`

| Campo | Cambio |
|-------|--------|
| `monto` | Sin cambios (sigue siendo MONTO_A_PAGAR) |
| `monto_bruto` | **NUEVO** — MONTO (gross) de fuente XLSX |
| `comision_marketplace` | **NUEVO** — MONTO - MONTO_A_PAGAR |

### 4.2 `marketplace_ledger_clasificado_v1`

| Campo | Cambio |
|-------|--------|
| `monto` | Sin cambios |
| `monto_bruto` | **NUEVO** — propagado desde ledger_v1 |
| `comision_marketplace` | **NUEVO** — propagado desde ledger_v1 |

### 4.3 `marketplace_cierre_financiero_v1`

| Campo | Cambio |
|-------|--------|
| `total_ingresos` | Sin cambios (sigue sumando MONTO_A_PAGAR) |
| `total_comisiones_marketplace` | **NUEVO** — SUM(comision_marketplace) para PARIS |
| `resultado_neto` | Sin cambios |
| `venta_bruta` | **NUEVO** — SUM(monto_bruto) para ingresos PARIS |

## 5. Mapeo Detalle → Grupo Financiero (Nuevo Concepto)

```python
# NUEVO concepto en RAW_TO_CLASSIFICATION_MAP
"Comisión Marketplace": "Comisión Marketplace",

# NUEVO grupo en FINANCIAL_STRUCTURE
"comisiones_marketplace": [
    "Comisión Marketplace",
],
```

## 6. Backend API Endpoints — Nuevos Campos

### 6.1 `/api/v4/exec/summary` — Nuevo response

```json
{
  "venta_bruta": { "PARIS": 598000000, "ML": ..., "RIPLEY": ..., "FALABELLA": ... },
  "comision_marketplace": { "PARIS": 113800000 },
  "neto_liquidado": { "PARIS": 484200000 },
  "resultado_neto": { "PARIS": 337400000 }  // SIN CAMBIO
}
```

### 6.2 `/api/v4/exec/waterfall` — Nuevo response

```json
{
  "PARIS": {
    "ingresos": 484200000,       // sin cambio (MONTO_A_PAGAR)
    "venta_bruta": 598000000,   // NUEVO (MONTO)
    "comision_marketplace": 113800000,  // NUEVO
    "devoluciones": -121458109,
    "resultado_neto": 337400000  // SIN CAMBIO
  }
}
```

## 7. Frontend — Consumo de Datos

```javascript
// Antes (dashboard.html):
const ventas = window._cierreCertified.ing;

// Después:
const ventas_brutas = window._cierreCertified.venta_bruta;  // MONTO
const ventas_netas = window._cierreCertified.ing;            // MONTO_A_PAGAR
const comision = window._cierreCertified.comision_marketplace;
```

**NO hay post-procesamiento visual.** Los valores vienen pre-calculados desde la API.

## 8. Resumen de Cambios

| Componente | Archivos | Líneas Afectadas | Cambio |
|-----------|----------|-----------------|--------|
| Schema | `database.py` | ~88-99 | 2 ALTER TABLE |
| Backfill script | `scripts/paris_backfill_v2.py` | NUEVO | Leer XLSX, actualizar ledger |
| Clasificación | `marketplace_auditor.py` | 2 líneas | Nuevo concepto + grupo |
| Classification re-run | `marketplace_auditor.py` | RUN_CLASSIFICATION | Solo PARIS |
| Closing | `marketplace_auditor.py` | ~572 | Agregar comisiones_marketplace |
| API summary | `api/api.py` | ~520 | Agregar venta_bruta, comision_marketplace |
| API waterfall | `api/api.py` | ~590 | Agregar campos al response |
| Frontend | `dashboard.html`, `executive_dashboard.html` | Mínimo | Consumir nuevos campos |
