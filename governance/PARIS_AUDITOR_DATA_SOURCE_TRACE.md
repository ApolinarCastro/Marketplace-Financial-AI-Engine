# PARIS — Auditor Data Source Trace

**Fecha:** 2026-06-11
**FASE 1** — RFC PARIS ECONOMIC MODEL FINAL FIX

---

## 1. Marketplace Auditor v3.5 — Data Sources

El dashboard Auditor (`templates/dashboard.html`) consume 4 endpoints:

| Endpoint | Responsabilidad | Query SQL Clave |
|----------|----------------|----------------|
| `GET /api/v4/cierre/desglose` | Estructura financiera detallada (Ingresos, Devoluciones, Costos, Ajustes) | `SELECT financial_group, detalle, SUM(monto) FROM marketplace_ledger_v1 GROUP BY financial_group, detalle` |
| `GET /api/v4/exec/waterfall` | Waterfall visual + RN operacional | `SELECT SUM(CASE WHEN financial_group='ingresos' THEN monto ELSE 0 END) as ingresos, ...` |
| `GET /api/v4/ledger` | Ledger detalle (tabla de transacciones) | `SELECT * FROM marketplace_ledger_v1 WHERE marketplace=?` |
| `GET /api/v4/auditoria` | Alertas de auditoría | `SELECT * FROM marketplace_auditoria_v1 WHERE marketplace=?` |

## 2. Endpoint: `/api/v4/cierre/desglose` (L240-294)

**Archivo:** `api/api.py`

**SQL exacto (L264-278):**
```sql
SELECT 
    COALESCE(financial_group, 'sin_clasificar') as financial_group,
    detalle,
    tipo_movimiento,
    clasificacion_operativa,
    SUM(COALESCE(monto, 0)) as total,
    COUNT(*) as cantidad
FROM marketplace_ledger_v1
WHERE marketplace = ?
  AND fecha BETWEEN ? AND ?
  [exclude_clause]
GROUP BY financial_group, detalle, tipo_movimiento, clasificacion_operativa
ORDER BY total ASC
```

**Response:** Array de objetos con `{detalle, clasificacion_operativa, tipo_movimiento, total, cantidad, categoria}`

**Para PARIS Ene 2026**, el response actual es:
```json
[
  {"detalle": "Ajuste Inventario Activo", "total": 647108, "categoria": "ajustes", ...},
  {"detalle": "Cobro por despacho", "total": -853024, "categoria": "costos_operacionales", ...},
  {"detalle": "Despacho", "total": 0, "categoria": "ingresos", ...},
  {"detalle": "Venta", "total": 16251515, "categoria": "ingresos", ...},
  {"detalle": "Devolución", "total": -9008635, "categoria": "devoluciones", ...},
  {"detalle": "Logística inversa", "total": -293490, "categoria": "costos_operacionales", ...},
  ...
]
```

## 3. Endpoint: `/api/v4/exec/waterfall` (L575-633)

**Archivo:** `api/api.py`

**SQL exacto (L606-615):**
```sql
SELECT
    COALESCE(SUM(CASE WHEN financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ingresos,
    COALESCE(SUM(CASE WHEN financial_group='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as devoluciones,
    COALESCE(SUM(CASE WHEN financial_group='costos_operacionales' ... THEN monto ELSE 0 END), 0) as costos_op,
    COALESCE(SUM(CASE WHEN financial_group='costos_comerciales' ... THEN monto ELSE 0 END), 0) as costos_com,
    COALESCE(SUM(CASE WHEN financial_group IN ('ajustes', ...) ... THEN monto ELSE 0 END), 0) as ajustes,
    COALESCE(SUM(CASE WHEN financial_group='ingresos' ... THEN COALESCE(monto_bruto, monto / 0.85) ELSE 0 END), 0) as venta_bruta,
    COALESCE(SUM(CASE WHEN financial_group='ingresos' ... THEN COALESCE(comision_marketplace, monto * 0.15 / 0.85) ELSE 0 END), 0) as comision_marketplace
FROM marketplace_ledger_v1
WHERE {ledger_where}
```

**Nota:** Ya incluye `venta_bruta` y `comision_marketplace` desde RFC anterior.

## 4. Endpoint: `/api/v4/ledger` (L145-219)

```python
sql = f"""
    SELECT marketplace, id_transaccion, id_orden, fecha, detalle, monto, 
           tipo_movimiento, archivo_origen, folio_xml, 
           financial_group, clasificacion_operativa
    FROM marketplace_ledger_v1
    WHERE marketplace = ?
      AND fecha BETWEEN ? AND ?
      {exclude_clause}
    ORDER BY fecha DESC
    LIMIT ?
"""
```

**Nota:** `monto` se devuelve sin transformación = MONTO_A_PAGAR (neto).

## 5. Endpoint: `/api/v4/exec/ux12_summary` (L832-945)

```python
SELECT 
    COALESCE(SUM(CASE WHEN {ing_filter} THEN monto ELSE 0 END), 0) as gross_sales,
    COALESCE(SUM(CASE WHEN {dev_filter} THEN monto ELSE 0 END), 0) as returns,
    COALESCE(SUM(CASE WHEN {cop_filter} THEN monto ELSE 0 END), 0) as marketplace_costs,
    COALESCE(SUM(CASE WHEN {ajuste_filter} THEN monto ELSE 0 END), 0) as net_profit
FROM marketplace_ledger_v1 ...
```

**Nota:** `gross_sales` = SUM(monto) WHERE financial_group='ingresos' = NETO (MONTO_A_PAGAR).

## 6. Auditor Frontend — Cómo Consume (dashboard.html)

| Sección | Endpoint | Campo Usado |
|---------|----------|-------------|
| KPIs | `ux12_summary` | `gross_sales`, `net_profit` |
| Tabla estructura financiera | `cierre/desglose` | `categoria`, `detalle`, `total` |
| Waterfall | `exec/waterfall` | `values` array |
| Ledger detalle | `ledger` | `monto`, `detalle`, `financial_group` |

## 7. Conclusión

El campo `monto` en `marketplace_ledger_v1` = **MONTO_A_PAGAR** (neto comisión) para PARIS. Todos los endpoints financieros usan `SUM(monto)`, por lo que toda la estructura financiera del Auditor muestra valores netos, no brutos. La Venta Bruta (MONTO) y Comisión Marketplace solo existen en los nuevos campos `venta_bruta` y `comision_marketplace` de `exec/waterfall`.
