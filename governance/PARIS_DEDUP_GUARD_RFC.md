# PARIS DEDUP GUARD RFC
**Date:** 2026-06-07
**Status:** Design only — NO IMPLEMENTAR

---

## 1. Candidate Key Definition

**Dedup Key (candidate key compuesta):**
```
(id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen)
```

**Justificación:** Esta clave identifica unívocamente un evento económico dentro de un archivo fuente. Dos filas con la misma clave representan el mismo evento económico cargado N veces.

---

## 2. Dedup Columns

| Columna | Tipo | Función |
|---|---|---|
| `id_orden` | VARCHAR | Identificador de orden |
| `fecha` | DATE | Fecha del evento |
| `monto` | DOUBLE | Monto del evento |
| `financial_group` | VARCHAR | Grupo financiero (ingresos, devoluciones, etc.) |
| `detalle` | VARCHAR | Descripción del concepto |
| `clasificacion_operativa` | VARCHAR | Clasificación operativa |
| `archivo_origen` | VARCHAR | Archivo fuente de origen |

**Columnas EXCLUIDAS del dedup key:**
- `id_transaccion` — Diferente para cada carga (cambio inocuo)
- `folio_xml` — Puede variar entre cargas (0 vs valor real)
- `estado_xml` — No afecta el evento económico
- `asociacion_xml` — No afecta el evento económico
- `include_in_operational_pnl` — Siempre TRUE para PARIS
- `load_ts` — Siempre diferente (timestamp de carga)
- `tipo_movimiento` — Puede variar (CARGO vs valor real)

---

## 3. Estrategia Determinista (KEEP 1, REMOVE N-1)

**Regla de selección:** `ROW_NUMBER() OVER (PARTITION BY <dedup_key> ORDER BY folio_xml DESC, id_transaccion ASC)`

**Prioridad:**
1. **Filas con `folio_xml ≠ 0` tienen prioridad** (tienen trazabilidad XML real)
2. **Filas con `folio_xml = 0` se eliminan** (son copias de archivos anuales sin XML)
3. **Tiebreaker:** `id_transaccion ASC` (primera transacción registrada gana)

**Efecto:** Por cada grupo de N filas idénticas, se conserva exactamente 1 (la de mejor calidad documental).

---

## 4. Rollback Strategy

**DELETE transaccional con snapshot previo:**

```sql
BEGIN TRANSACTION;

-- 1. Crear snapshot de las filas a eliminar
CREATE TABLE paris_dedup_backup_<timestamp> AS
SELECT * FROM marketplace_ledger_v1
WHERE (id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen)
IN (
    SELECT id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen
    FROM marketplace_ledger_v1
    WHERE marketplace='PARIS'
    GROUP BY id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen
    HAVING COUNT(*) > 1
)
AND id_transaccion NOT IN (
    SELECT MIN(id_transaccion)  -- Keep strategy: 1st by id_transaccion (or any deterministic rule)
    FROM marketplace_ledger_v1
    WHERE marketplace='PARIS'
    GROUP BY id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen
    HAVING COUNT(*) > 1
);

-- 2. DELETE con JOIN para eliminar solo las filas respaldadas
DELETE FROM marketplace_ledger_v1
WHERE (id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen, id_transaccion)
IN (
    SELECT id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen, id_transaccion
    FROM paris_dedup_backup_<timestamp>
);

COMMIT;
```

**Rollback:**
```sql
INSERT INTO marketplace_ledger_v1
SELECT * FROM paris_dedup_backup_<timestamp>;
```

---

## 5. Validaciones Post-Dedup

| Check | SQL | Expected |
|---|---|---|
| No más grupos duplicados | `SELECT COUNT(*), SUM(cnt-1) FROM (SELECT ..., COUNT(*) as cnt FROM ledger GROUP BY dedup_key HAVING cnt>1)` | 0 groups |
| Delta RN = -$21,238,958 | `SELECT SUM(monto) FROM ledger WHERE marketplace='PARIS'` vs backup | Delta exacto |
| Cross-MP intact | `SELECT SUM(monto) FROM ledger WHERE marketplace IN ('ML','RIPLEY','FALABELLA')` vs backup | $0 delta |
| Waterfall consistency | `SELECT ... SUM(CASE WHEN fg='ingresos'...` vs backup | Delta por FG exacto |
| 14/14 regression | `pytest tests/ -v` | PASS |

---

## 6. Compatibilidad

| Estándar | Compatible? | Nota |
|---|---|---|
| Seller P&L Truth | ✅ | Dedup solo opera sobre PARIS. P&L Truth cubre ML. |
| Single Financial Truth | ✅ | Ledger sigue siendo fuente única. Solo se corrigen duplicados. |
| DEC-019 | ✅ | No afecta ML ni `include_in_operational_pnl`. |
| Audit Ready | ✅ | Cada fila eliminada tiene backup con trazabilidad completa. |
| 14/14 Regression | ✅ | Waterfall endpoints retornan valores ~$21M menores. Tests deben actualizarse. |

---

## 7. Estrategia de Prevención (Loader Guard)

En el loader de PARIS, antes de INSERT:

```
1. Verificar si (id_orden, fecha, monto, financial_group, detalle, clasif_op, archivo_origen) ya existe
2. Si existe → SKIP (no insertar duplicado)
3. Si no existe → INSERT normalmente
```

**Costo:** 1 índice o hash lookup por fila. O(1) amortizado.
**Efecto:** Los archivos con solapamiento (FF anual + DS mensuales) no generan duplicados en el ledger.

---

## 8. Resumen

| Componente | Diseño |
|---|---|
| Dedup Key | 7 columnas (orden, fecha, monto, fg, detalle, clasif, source) |
| Keep Rule | folio_xml DESC, id_transaccion ASC |
| Rollback | Backup table + re-INSERT |
| Validation | 7 checks automáticos |
| Prevention | Loader dedup guard pre-INSERT |
