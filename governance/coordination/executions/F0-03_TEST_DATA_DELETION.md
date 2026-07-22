# F0-03 — TEST DATA DELETION AND BASELINE ESTABLE V7

**Estado:**
CERTIFICADO

**Fecha:** 2026-07-15
**Ejecutor:** OpenCode
**Ruta autorizada:** C (RECOVER_CURRENT_STATE_AND_CERTIFY)

---

## Resumen

Se eliminaron 52 filas de datos de prueba (`report_full.xlsx`, `report_drop.xlsx`, `fact_test.xlsx`, `pos_test.xlsx`) de `marketplace_ledger_v1` sobre la copia de trabajo `temp_working`. La copia limpia se promovió a `meli_financial_v4.db` (producción). Cero regresiones nuevas. Cero modificaciones a tablas certificadas. Cero impacto en clasificación y cierre financiero.

---

## Evidencia

### Proveniencia de datos de prueba

| Archivo | Filas | Valor | Marketplace | Período |
|---------|-------|-------|-------------|---------|
| `report_full.xlsx` | 20 | $400,000 | PARIS | 2026-04 |
| `report_drop.xlsx` | 20 | $300,000 | PARIS | 2026-04 |
| `fact_test.xlsx` | 9 | $16,500 | ML | 2026-03 |
| `pos_test.xlsx` | 3 | -$1,500 | ML | 2026-03 |
| **Total** | **52** | **$715,000** | | |

### Características de los datos eliminados

- Todos los IDs de transacción contienen prefijos de prueba: `TX-FULL-`, `TX-DROP-`, `_fact_test`, `_pos_test`
- Ninguna fila productiva comparte estos patrones de ID (0 falsos positivos)
- Ninguna fila de prueba existe en `marketplace_ledger_clasificado_v1` (0 impacto en P&L)
- Ninguna fila de prueba en `marketplace_cierre_financiero_v1` (0 impacto en cierre certificado)
- Ninguna fila de prueba en `marketplace_auditoria_v1`, `ripley_settlement_chain`, `ripley_traceability_graph`

### Datos no eliminados (retenidos intencionalmente)

| Origen | Filas | Motivo |
|--------|-------|--------|
| 15 archivos `Reporte_Facturacion_MercadoLibre_*.xlsx` | 79,644 | Datos reales de ML Facturacion cargados por sistema de ingesta (P40 FASE 1). No son datos de prueba. |
| ML Facturacion 2026-01 test.csv (4 registros) | 0 | No existen filas en ledger. La ingesta reportó records_inserted=4 por un bug de contador. |

### DB resultante

| Métrica | Pre-F0-03 | Post-F0-03 | Delta |
|---------|-----------|------------|-------|
| Ledger rows | 374,303 | 374,251 | -52 |
| Ledger value | $2,951,683,247.64 | $2,950,968,247.64 | -$715,000 |
| Clasificado rows | 294,607 | 294,607 | 0 |
| Cierre rows | 246 | 246 | 0 |
| SHA256 | `bf6ed7aec5410abe033b2a3c271011ddfce044f0e4c9008aba590ae48ba52aa6` | `990cb0f1476a1b4c882186fdffae84b78be8236c254a12ccf8a5f4e4f67c034b` | |

### Regresión de pruebas

**648 passed, 56 failed, 20 skipped** (pre-existing: 56/56 failures confirmados como pre-existentes mediante comparación forense contra copia inalterada).

### 0 nuevas regresiones.

| Test | Forensic | Temp_working | ¿Nuevo? |
|------|----------|-------------|---------|
| ML Ene 2026 op_pnl in clasificado | $0 | $0 | NO |
| ML 2026-04 Cargo venta ledger | 0 rows, $0 | 0 rows, $0 | NO |
| SQL_ALL=0.0 vs Panel=$27.9M | Mismo | Mismo | NO (pre-existing desde carga Jul 13) |

### Snapshot

- `baseline_estable_v7_20260715/MANIFEST_V7.json`
- `snapshot_pre_f003_cleaned_20260715/MANIFEST_PRE_F003.json`
- Backup: `data/db/meli_financial_v4.db.bak_pre_f003`

---

## Cumplimiento de reglas

- **No modificar RC1**: OK. Ningún cambio a engine/rc1/.
- **No modificar el Ledger desde conciliación**: OK. Deletion directa de filas de prueba identificadas por archivo origen. No se alteró lógica de conciliación.
- **No duplicar lógica financiera**: OK.
- **No duplicar SQL financiero**: OK.
- **No calcular cifras financieras en frontend**: OK.
- **No utilizar RAW como base operacional después de la ingesta**: OK.
- **No eliminar RAW como evidencia**: OK.
- **Cero costo monetario**: OK.
- **Cambios controlados y reversibles**: OK. Backup forense preservado en `snapshot_pre_f003_cleaned_20260715/`.

---

## Veredicto

**BASELINE_ESTABLE_V7 — CERTIFICADO**

El sistema operativo financiero queda estabilizado con:
- 374,251 filas de ledger
- $2,950,968,247.64 valor total
- 294,607 filas clasificadas (sin cambios)
- 246 filas de cierre (sin cambios)
- 0 filas de datos de prueba
- 0 nuevas regresiones
- 56 fallos pre-existentes documentados
