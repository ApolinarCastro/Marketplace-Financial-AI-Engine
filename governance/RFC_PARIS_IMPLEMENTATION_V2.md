# RFC — PARIS Economic Model Implementation V2

**RFC ID:** RFC_PARIS_IMPLEMENTATION_V2
**Estado:** APROBADO PARA IMPLEMENTACIÓN
**Fecha:** 2026-06-11
**Verdad Económica:** PARIS = 3P Marketplace (DEC-023)

---

## 1. Objetivo

Corregir el modelo económico de PARIS para reflejar la verdad económica certificada:

| Variable | Definición Oficial | Origen |
|----------|-------------------|--------|
| Venta Bruta | `MONTO` (gross) | Columna en XLSX fuente |
| Comisión Marketplace | `MONTO - MONTO_A_PAGAR` | Diferencia calculada |
| Neto Liquidado | `MONTO_A_PAGAR` | Columna en XLSX fuente |

Actualmente `marketplace_ledger_v1.monto` = `MONTO_A_PAGAR` (neto). Se debe agregar `monto_bruto` y `comision_marketplace` para preservar la verdad económica 3P.

## 2. Archivos Afectados

| Archivo | Cambio | Tipo |
|---------|--------|------|
| `engine/v4/database.py` | Schema: ADD COLUMN `monto_bruto`, `comision_marketplace` | ALTER TABLE |
| `engine/v4/surgical_loader.py` | Loader PARIS: leer MONTO + MONTO_A_PAGAR, escribir ambos | Modificación |
| `engine/v4/marketplace_auditor.py` | Clasificación: comision_marketplace → nuevo concepto | Modificación menor |
| `api/api.py` | Endpoints: exponer Venta Bruta, Comisión Marketplace | Nuevos campos |
| `templates/executive_dashboard.html` | Frontend: mostrar gross y commission en lugar de net | Consume API |
| `templates/dashboard.html` | Frontend: idem | Consume API |

## 3. Funciones Afectadas

### 3.1 `surgical_loader.py` — `load_paris()` (L284-348)

**Cambio:** Leer columna `MONTO` (gross) además de `MONTO_A_PAGAR`.

```python
# Actual:
c_monto = get_col_name(df, ['monto a pagar', 'monto'])      # → monto (neto)

# Nuevo:
c_monto_pagar = get_col_name(df, ['monto a pagar'])          # → monto (neto) = MONTO_A_PAGAR
c_monto_bruto = get_col_name(df, ['monto'])                  # → monto_bruto (gross) = MONTO
```

En el ledger:
```python
monto = float(row[c_monto_pagar]) if MONTO_A_PAGAR existe else float(row[c_monto_bruto])
monto_bruto = float(row[c_monto_bruto])
comision = monto_bruto - monto
```

### 3.2 `database.py` — `_create_schema()` y ALTER TABLE

Agregar columnas a `marketplace_ledger_v1`:

```python
# En _create_schema() o como hot-migration:
"ALTER TABLE marketplace_ledger_v1 ADD COLUMN monto_bruto DOUBLE"
"ALTER TABLE marketplace_ledger_v1 ADD COLUMN comision_marketplace DOUBLE"
```

Agregar a `LEDGER_COLS` en `surgical_loader.py` (L14):
```python
LEDGER_COLS = ['marketplace', 'id_transaccion', 'id_orden', 'fecha', 'detalle', 
               'monto', 'tipo_movimiento', 'archivo_origen', 'folio_xml',
               'monto_bruto', 'comision_marketplace']
```

### 3.3 `marketplace_auditor.py` — Clasificación

Agregar concepto `Comisión Marketplace` a `RAW_TO_CLASSIFICATION_MAP` y a `FINANCIAL_STRUCTURE['costos_operacionales']` o nuevo grupo `comisiones_marketplace`.

**Opción recomendada:** Nuevo financial_group `comisiones_marketplace` para que no se mezcle con costos operacionales existentes.

```python
# RAW_TO_CLASSIFICATION_MAP
"Comisión Marketplace": "Comisión Marketplace",

# FINANCIAL_STRUCTURE — nuevo grupo
"comisiones_marketplace": [
    "Comisión Marketplace",
],
```

### 3.4 `api/api.py` — Endpoints

| Endpoint | Cambio |
|----------|--------|
| `/api/v4/exec/summary` | Agregar `venta_bruta` y `comision_marketplace` para PARIS |
| `/api/v4/exec/waterfall` | Agregar campos opcionales `gross_sales`, `commission` |
| `/api/v4/exec/gross-revenue` (NUEVO) | Endpoint específico para gross revenue por MP |
| `/api/v4/cierre/desglose` | Agregar `comisiones_marketplace` como grupo nuevo |

### 3.5 Frontend

**Mínimo cambio:** Los KPIs de Ventas Brutas y Comisión Marketplace se sirven desde nuevos campos API. Frontend solo consume. Sin post-procesamiento.

## 4. Loaders Afectados

| Loader | Cambio |
|--------|--------|
| `load_paris()` | Leer MONTO + MONTO_A_PAGAR; escribir monto_bruto y comision_marketplace |
| Otros loaders (ML, RIPLEY, FALABELLA) | **SIN CAMBIOS** |

## 5. Impacto Esperado

### 5.1 Invariantes (Delta = 0)

| Variable | Explicación |
|----------|-------------|
| Resultado Neto | RN = MONTO_A_PAGAR - costos. MONTO_A_PAGAR no cambia → RN invariante |
| Disponible | = RN. Mismo cálculo → invariante |
| Waterfall | Ventas - Devoluciones - Costos = RN. MONTO_A_PAGAR usado para RN → invariante |
| Flujo Caja | Basado en RN → invariante |

### 5.2 Variables que Cambian

| Variable | Antes | Después | Diferencia |
|----------|-------|---------|------------|
| Venta Bruta (PARIS) | $484.2M (neto = MONTO_A_PAGAR) | ~$598.0M (gross = MONTO) | +$113.8M (15%) |
| Comisión Marketplace | $0 (implícita) | ~$113.8M (explícita) | Nuevo concepto |
| Neto Liquidado | $484.2M | $484.2M (sin cambio) | $0 |
| Margen Bruto | N/A | 19.0% (commission/gross) | Nueva métrica |

### 5.3 KPIs Afectados

| KPI | Impacto |
|-----|---------|
| Venta Bruta | +15% (gross, no neto) |
| Comisión Marketplace | Nuevo KPI = $113.8M |
| Margen Neto | Sin cambio (RN invariante) |
| Take Rate | ~19.0% (commission/gross) |

### 5.4 Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Frontend muestra valores incorrectos | API sirve ambos (gross + net). Frontend consume campo correcto |
| Confusión usuarios entre Venta Bruta vs Neto | Tooltips de explicabilidad en frontend |
| Otros MPs contaminados | Exclusivamente PARIS. NO modificar otros MPs |
| DEC-019 alterado | NO modificar. DEC-019 solo afecta ML |

## 6. Estrategia de Reproceso

1. Tomar snapshot de DB antes de cambios
2. Agregar columnas vía ALTER TABLE (migration segura)
3. Ejecutar script de backfill: leer XLSX fuente, actualizar `monto_bruto` y `comision_marketplace`
4. Actualizar clasificación (nuevo concepto comisiones_marketplace)
5. Re-ejecutar financial closing solo para PARIS
6. Verificar invariantes
7. Actualizar API y frontend
