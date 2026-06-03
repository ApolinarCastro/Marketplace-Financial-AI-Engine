# RFC-001: RIPLEY TEMPORAL RECONSTRUCTION PLAN

**Estado:** DISEÑO — NO IMPLEMENTAR
**Régimen:** FORENSE — READ ONLY
**Clasificación incidente:** P1 (bug de fecha) — ver `RIPLEY_VALUE_CONSERVATION_CERTIFICATION.md`
**Diseñado por:** MFE Governance
**Fecha:** 2026-05-30

---

## 1. SNAPSHOT REQUERIDO

### 1.1 Pre-requisitos

| Elemento | Acción | Responsable |
|---|---|---|
| LIVE DB desbloqueado | PID 27988 debe liberar lock en `data/db/meli_financial_v4.db` | Infra |
| Confirmar DB_PATH | `engine/v4/database.py:12` → `data/db/meli_financial_v4.db` | Auditor |
| Backup de DB activo | DuckDB `COPY database TO` completo | Governance |

### 1.2 Snapshots a crear (PRE-fix, orden cronológico)

| # | Elemento | Método | Output | Validación |
|---|---|---|---|---|
| **S1** | Source XLSX (46 files) | SHA256 de cada archivo | `snapshot_pre_fix/S1_XLSX_MANIFEST.json` | Comparar con MD5 de auditoría A3 |
| **S2** | DB completa | `data/db/meli_financial_v4.db` → `data/db/snapshot_v6_pre_ripley_fix/` | Full DuckDB copy | SHA256 del archivo .db |
| **S3** | Ripley ledger export | `SELECT * FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'` | `snapshot_pre_fix/S3_RIPLEY_LEDGER.csv` | Row count 269,216; total $284,897,360 |
| **S4** | Ripley Importe del pedido totals by month | Query agrupada | `snapshot_pre_fix/S4_IMPORTE_BY_MONTH.csv` | 24 rows (2025-01 a 2026-12) |
| **S5** | Ventas marketplace RIPLEY | `SELECT * FROM ventas_marketplace WHERE marketplace='RIPLEY'` | `snapshot_pre_fix/S5_VENTAS.csv` | Row count 10,647 |
| **S6** | All 32 concepts by year | Query `GROUP BY detalle, strftime('%Y', fecha)` | `snapshot_pre_fix/S6_CONCEPTS_BY_YEAR.csv` | 64 rows (32 concepts × 2 years) |
| **S7** | All concept totals | `SELECT detalle, COUNT(*), SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' GROUP BY detalle` | `snapshot_pre_fix/S7_CONCEPT_TOTALS.csv` | 32 rows |
| **S8** | 14/14 regression tests | `pytest tests/test_regression_contracts.py -v` | `snapshot_pre_fix/S8_REGRESSION_PASS.log` | All PASS |
| **S9** | SQL=API=UI baseline | Query + API call + screenshot | `snapshot_pre_fix/S9_API_BASELINE/` | 5 KPIs documentados |
| **S10** | Git tag del estado PRE | `git tag RIPLEY_PRE_FIX_{YYYYMMDD_HHMMSS}` | Tag en repo | Confirmar `git tag -l` |

### 1.3 Manifest del snapshot

```json
{
  "plan": "RFC-001",
  "date": "2026-05-30",
  "pre_fix_state": {
    "s1_xlsx_sha256": {"file_count": 46, "manifest_path": "..."},
    "s2_db_sha256": "e1e341ef...",
    "s3_ledger_rows": 269216,
    "s3_ledger_total": 284897360.00,
    "s8_all_tests_pass": true
  }
}
```

---

## 2. ROLLBACK REQUERIDO

### 2.1 Escenarios de rollback

| Escenario | Disparador | Acción | Tiempo estimado |
|---|---|---|---|
| **R1 — Tests fallan** | Regression test FAIL | Restaurar DB desde S2 + `git revert` fix + re-tag `RIPLEY_PRE_FIX` | 5 min |
| **R2 — Totales no cuadran** | Delta > $1,000 entre total Ledger post-fix y XLSX correcto | Restaurar DB desde S2 | 10 min |
| **R3 — Contaminación de otro marketplace** | ML/PARIS/FALABELLA totals cambian | Restaurar DB desde S2 + investigar causa | 30 min |
| **R4 — DB corrupta** | DuckDB CHECKSUM mismatch | Restaurar DB desde S2 | 5 min |
| **R5 — API caída** | Dashboard 500 error | Restaurar DB desde S2 + `git revert` fix | 5 min |
| **R6 — Valor perdido** | Total post-fix < total XLSX target por > $10,000 | Restaurar DB desde S2 + NO hacer fix hasta investigar | 2 hr |

### 2.2 Procedimiento de rollback

```bash
# 1. Detener API
taskkill /F /IM python.exe  # O systemctl stop, según deployment

# 2. Restaurar DB
copy data/db/snapshot_v6_pre_ripley_fix/meli_financial_v4.db data/db/meli_financial_v4.db

# 3. Revertir fix
git checkout RIPLEY_PRE_FIX -- engine/v4/surgical_loader.py

# 4. Re-iniciar API
python api/api.py

# 5. Verificar
pytest tests/test_regression_contracts.py -v
# Confirmar: 14/14 PASS
```

### 2.3 Idempotencia garantizada

El procedimiento de recarga debe ser **idempotente**:
- `insert_df` con `dedup_cols=['id_transaccion']` en `marketplace_ledger_v1`
- `insert_df` con `dedup_cols=['order_id']` en `ventas_marketplace`
- Si la recarga se ejecuta 2 veces, el resultado debe ser idéntico

**Acción requerida previa:** Verificar que `insert_df` en `database_v4.py` tenga `dedup_cols` configurado para Ripley. Si no, se requiere DELETE + INSERT:

```sql
DELETE FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY';
DELETE FROM ventas_marketplace WHERE marketplace = 'RIPLEY';
```

Luego ejecutar `load_ripley()` normalmente.

---

## 3. VALIDACIONES PREVIAS

### 3.1 Verificación de datos fuente

| Validación | Método | Criterio |
|---|---|---|
| 46 XLSX existen | `Get-ChildItem 01_Raw/RIPLEY/Resumen financiero/*.xlsx` | Count = 46 |
| SHA256 no ha cambiado | Comparar con manifest de auditoría A3 | Sin cambios |
| Fechas en formato dd-mm-yyyy | `pd.read_excel()` → sample 10 filas por archivo | 100% formato string `dd-mm-yyyy` |
| Importe del pedido parseable | `pd.to_numeric(..., errors='coerce')` | NaN count = 0 |
| No hay archivos corruptos | `pd.read_excel(engine='openpyxl')` en los 46 | 0 errores |

### 3.2 Verificación del estado actual

| Validación | Query | Criterio |
|---|---|---|
| Ripley ledger row count | `SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'` | 269,216 |
| Ripley ledger total | `SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'` | $284,897,360 |
| Ripley Importe del pedido | `SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND detalle='Importe del pedido'` | $240,979,600 |
| ML ledger intacto | `SELECT COUNT(*), SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='ML'` | 101,603 rows, $842,342,536 |
| PARIS ledger intacto | `SELECT COUNT(*), SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='PARIS'` | 42,487 rows, $378,097,614 |
| FALABELLA ledger intacto | `SELECT COUNT(*), SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'` | 1,008 rows, $2,603,790 |
| 14/14 regression PASS | `pytest tests/test_regression_contracts.py -v` | All PASS |
| LIVE DB unlocked | DuckDB connect sin error | Conexión exitosa |

### 3.3 Verificación de la corrección (dayfirst=True)

En entorno de PRUEBA (NO producción), validar que el fix produce los resultados esperados:

```python
# Script de verificación (entorno test-only)
import pandas as pd
test_dates = ['01-04-2026', '02-04-2026', '15-04-2026', '30-04-2026']
for d in test_dates:
    old = pd.to_datetime(d)
    new = pd.to_datetime(d, dayfirst=True)
    print(f"{d}: old={old} new={new}")
# Debe producir:
# 01-04-2026: old=2026-01-04 new=2026-04-01  ✓
# 02-04-2026: old=2026-02-04 new=2026-04-02  ✓
# 15-04-2026: old=2026-04-15 new=2026-04-15  ✓
# 30-04-2026: old=2026-04-30 new=2026-04-30  ✓
```

### 3.4 Identificación de la línea exacta a corregir

Dos líneas requieren `dayfirst=True`:

```
Line 382: pd.to_datetime(df[c_fecha], errors='coerce') if c_fecha else None
Line 400: pd.to_datetime(row[c_fecha]) if c_fecha else None
```

Ambas en `engine/v4/surgical_loader.py`, función `load_ripley()`.

Ninguna otra línea en el código base usa `pd.to_datetime()` sin `dayfirst=True` para Ripley.

---

## 4. ESTRATEGIA DE RECARGA

### 4.1 Flujo de ejecución

```
┌─────────────────────┐
│ 1. FREEZE DB        │  → Detener API, pausar cualquier ETL
├─────────────────────┤
│ 2. SNAPSHOT (S1-S10)│  → Ver sección 1
├─────────────────────┤
│ 3. FIX CODE         │  → dayfirst=True en líneas 382, 400
├─────────────────────┤
│ 4. DELETE RIPLEY    │  → DELETE FROM ledger y ventas (WHERE marketplace='RIPLEY')
├─────────────────────┤
│ 5. RECARGA          │  → Ejecutar load_ripley() completo
├─────────────────────┤
│ 6. VERIFICAR        │  → Row counts, totals, tests
├─────────────────────┤
│ 7. RECERTIFICAR     │  → Sprint B2.2 recert (5/5 KPIs)
├─────────────────────┤
│ 8. UNFREEZE         │  → Re-iniciar API
└─────────────────────┘
```

### 4.2 Paso 4: DELETE de datos RIPLEY existentes

```sql
BEGIN TRANSACTION;

-- Guardar verificación pre-delete
SELECT COUNT(*) as old_cnt, SUM(monto) as old_total
FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY';
-- Debe dar: 269,216 rows, $284,897,360

-- Eliminar datos
DELETE FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY';
DELETE FROM ventas_marketplace WHERE marketplace = 'RIPLEY';

-- Verificar delete
SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY';
-- Debe dar: 0

COMMIT;
```

**Riesgo:** DELETE sin transacción podría dejar la DB en estado inconsistente si falla la recarga. Solución: usar BEGIN/COMMIT con ROLLBACK si `load_ripley()` falla.

### 4.3 Paso 5: Recarga

El `load_ripley()` existente ya lee los 46 XLSX y produce rows en `marketplace_ledger_v1` y `ventas_marketplace`. Con el fix de `dayfirst=True`, las fechas se interpretan correctamente.

No se requiere ningún cambio en el pipeline de recarga — solo el fix de 1 línea.

### 4.4 Verificación post-recarga

```sql
-- Row count esperado
SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY';
-- Debe ser ≈ 541,000─542,000 rows (vs 269,216 pre-fix)
-- Cálculo: ~10,755 órdenes × 32 conceptos ≈ 344,160
-- Pero con _filter_old_years eliminando pre-2025 ≈ ~330,000
-- Y con conceptos $0 filtrados ≈ ~130,000
-- Total estimado: ~380,000─400,000

SELECT COUNT(*) FROM ventas_marketplace WHERE marketplace = 'RIPLEY';
-- Debe ser ≈ 10,755 (vs 10,647 pre-fix)
-- (se recuperan las ~108 órdenes que tenían fecha NaT)

-- Importe del pedido total
SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND detalle='Importe del pedido';
-- Target: ~$353,160,324 (XLSX correcto − $4.85M pre-2025)
-- Tolerancia: ±$1,000 (por engine difference openpyxl vs calamine)

-- Importe del pedido by month (sample)
SELECT strftime(fecha, '%Y-%m') as mes, SUM(monto) as total
FROM marketplace_ledger_v1
WHERE marketplace='RIPLEY' AND detalle='Importe del pedido'
GROUP BY mes ORDER BY mes;
-- Verificar que 2026-04 ≈ $16,460,180 (vs $1,500,432 pre-fix)
-- Verificar que NO hay meses fantasmas (2026-06 a 2026-12 deben ser 0 o muy bajos)
```

### 4.5 Orden de carga

Los 46 XLSX deben cargarse en orden cronológico por fecha de archivo (no alfabético):

```python
files = sorted(glob.glob('01_Raw/RIPLEY/Resumen financiero/*.xlsx'), key=os.path.getmtime)
for f in files:
    load_ripley(f)  # Con dayfirst=True
```

Esto asegura que los `dedup_cols` mantengan la última versión de cada orden si hay duplicados entre archivos.

---

## 5. ESTRATEGIA DE RECERTIFICACIÓN

### 5.1 Batería de tests post-fix

| Test | Método | Criterio |
|---|---|---|
| **T1 — 14/14 regression** | `pytest tests/test_regression_contracts.py -v` | ALL PASS |
| **T2 — Ripley Importe total** | SQL query vs XLSX correct (year>=2025) | Delta < $1,000 |
| **T3 — Apr 2026 específico** | SQL query = $16,460,180 ± $1,000 | Match |
| **T4 — Months without phantom** | Jun-Dec 2026 Importe = $0 ± $1,000 | Clean |
| **T5 — Other marketplaces intact** | ML/PARIS/FALABELLA totals unchanged | Delta = $0 |
| **T6 — Ventas marketplace count** | `COUNT(*) WHERE marketplace='RIPLEY'` | 10,755 |
| **T7 — Zero $0-concepts** | `COUNT(DISTINCT detalle) WHERE monto!=0` | 14 concepts (no change) |
| **T8 — Date distribution sanity** | No dates before 2025 (except filtered) | Year >= 2025 |

### 5.2 Recertificación Sprint B2.2 (Dashboard vs DB)

Repetir la certificación de `DASHBOARD_DATABASE_CERTIFICATION.md` con los datos corregidos:

| KPI | Antes (pre-fix) | Después (target) |
|---|---|---|
| Ingresos Brutos Ripley 2025 | $205.5M | **$281.2M** |
| Ingresos Brutos Ripley 2026 | $35.5M | **$72.0M** |
| Ingresos Brutos Ripley Abr 2026 | $1.5M | **$16.5M** |
| SQL = API = UI diff | $0 | **$0** (debe mantenerse) |

### 5.3 Recertificación Sprint B2.1 (Dashboard Reconciliation)

Re-ejecutar el bridge D360 vs Auditor con datos corregidos. El delta de $11.4M (D360=$12.4M vs Ledger=$1.0M) debe reducirse a ~$0 una vez que el ledger refleje correctamente Apr 2026.

### 5.4 Recertificación Sprint A3 (RIPLEY Trust Score)

Re-calcular Ripley Trust Score:

| Barrera | Pre-fix | Post-fix |
|---|---|---|
| Loader ausente | −25 pts | **−0 pts (resuelto)** |
| $142M sin clasificar | −15 pts | **−15 pts** (no cambia) |
| 7 facturas no cargadas | −5 pts | **−5 pts** (no cambia) |
| Bug de fecha | −20 pts | **−0 pts (resuelto)** |
| Sin folio_xml | −5 pts | **−5 pts** (no cambia) |
| Sin DTEIndexer | −5 pts | **−5 pts** (no cambia) |
| Sin certificación | −5 pts | **−5 pts** (no cambia) |
| **Total** | **~5/100** | **~60/100** |

---

## 6. KPIS ESPERADOS

### 6.1 Comparación antes/después

| KPI | Antes (pre-fix) | Después (target) | Delta |
|---|---|---|---|
| **Ripley Importe del pedido (all)** | $240,979,600 | ~$353,160,324 | **+$112,180,724 (+46.5%)** |
| **Ripley Importe 2025** | $205,499,578 | ~$281,188,982 | **+$75,689,404 (+36.8%)** |
| **Ripley Importe 2026** | $35,480,022 | ~$71,971,342 | **+$36,491,320 (+102.8%)** |
| **Ripley Importe Abr 2026** | $1,500,432 | ~$16,460,180 | **+$14,959,748 (+997%)** |
| **Ledger total rows (Ripley)** | 269,216 | ~380,000─400,000 | **+~110,000─130,000 rows** |
| **Ventas marketplace rows** | 10,647 | ~10,755 | **+108 rows** |
| **Trust Score (global)** | ~63/100 | **~70/100** | **+7 pts** |
| **Ripley Trust Score** | ~5/100 | **~60/100** | **+55 pts** |
| **Audit Readiness Score** | 58/100 | **~65-70/100** | **+7-12 pts** |

### 6.2 Lo que NO cambia

| Aspecto | Razón |
|---|---|
| ML totals | No afectado por el fix (ML no usa `load_ripley()`) |
| PARIS totals | No afectado (formato de fecha diferente en fuente) |
| FALABELLA totals | No afectado (misma razón) |
| $142M sin clasificar | La clasificación (`marketplace_ledger_clasificado_v1`) es un proceso separado |
| folio_xml=0% | Ripley no tiene XMLs (no hay DTEIndexer) |
| 7 facturas no cargadas | Es un problema diferente del loading de XLSX |
| 14/14 regresión | Debe mantenerse en 14/14 PASS |

### 6.3 Dashboard visual verification

```json
// GET /api/v4/ingresos/brutos/marketplace?anio=2026&mes=4
// ANTES:  {"marketplace":"RIPLEY","total":1500432.00}
// DESPUES: {"marketplace":"RIPLEY","total":16460180.00}  ✓
```

---

## 7. RIESGOS

### 7.1 Matriz de riesgos

| # | Riesgo | Probabilidad | Severidad | Mitigación |
|---|---|---|---|---|
| **R01** | `dedup_cols` no configurado → duplicados | **ALTA** | ALTA | Verificar `insert_df` antes de ejecutar. Si no hay dedup, usar DELETE+INSERT |
| **R02** | DB locked por PID 27988 | **ALTA** | MEDIA | Resolver bloqueo antes de iniciar. Si persiste, considerar snapshot en DB alterna |
| **R03** | Engine difference: calamine vs openpyxl → valores distintos | **MEDIA** | BAJA | Tolerancia de $1,000 en validación. El pipeline usa calamine, no openpyxl |
| **R04** | Otra instancia del loader corriendo concurrentemente | **BAJA** | ALTA | Freeze DB antes de cualquier operación. Verificar que no hay procesos Python activos |
| **R05** | DELETE exitoso pero INSERT falla a medio camino | **BAJA** | ALTA | Transacción completa: BEGIN + DELETE + INSERT + COMMIT. Si INSERT falla, ROLLBACK |
| **R06** | `_filter_old_years` elimina datos que deberían conservarse | **BAJA** | MEDIA | Verificar año mínimo post-fix. Debe ser 2025 (sin cambio) |
| **R07** | API devuelve error por datos nuevos (valores más grandes) | **BAJA** | BAJA | API acepta float64 sin límite superior. No debería impactar |
| **R08** | Dashboard muestra saltos visuales (ej: Abr 2026 sube 10x) | **MEDIA** | BAJA | Esperado y correcto. Comunicar a stakeholders antes del cambio |
| **R09** | Stakeholders cuestionan datos históricos corregidos | **ALTA** | MEDIA | Documentación completa + trazabilidad (RIPLEY_VALUE_CONSERVATION_CERTIFICATION.md) |
| **R10** | Re-auditoría requerida por cambio en BASELINE_V6 | **BAJA** | MEDIA | BASELINE_V6 sigue siendo el tag oficial. Post-fix sería BASELINE_V7 |

### 7.2 Riesgo crítico: Dedup

El método `insert_df` en `database_v4.py` debe soportar `dedup_cols` para evitar duplicados en la recarga. Si no lo soporta, el DELETE+INSERT es obligatorio.

```python
# Verificar en database_v4.py: insert_df() acepta dedup_cols
# Si no: implementar como:
#   connection.execute("DELETE FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'")
#   connection.execute("DELETE FROM ventas_marketplace WHERE marketplace='RIPLEY'")
```

### 7.3 Riesgo: Rollback sin snapshot

Si no se crean los snapshots S1-S10 antes del fix, no hay vuelta atrás. El snapshot es **obligatorio**, no opcional.

---

## 8. CRITERIOS DE ACEPTACIÓN

### 8.1 Criterios mínimos (gate)

```
[  ] 14/14 regression tests PASS
[  ] Ripley Importe del pedido total = $353,160,324 ± $1,000
[  ] Apr 2026 Importe = $16,460,180 ± $1,000
[  ] Jun-Dic 2026 Importe = $0 ± $1,000 (no phantom months)
[  ] ML ledger unchanged (COUNT, SUM)
[  ] PARIS ledger unchanged (COUNT, SUM)
[  ] FALABELLA ledger unchanged (COUNT, SUM)
[  ] SQL = API = UI diff = $0.00 (5 KPIs)
[  ] Ventas marketplace RIPLEY = ~10,755 rows
[  ] No errores en log del loader
```

### 8.2 Criterios deseables

```
[  ] Ripley Trust Score ≥ 50/100 (desde ~5/100)
[  ] Trust Score global ≥ 70/100 (desde ~63/100)
[  ] Dashboard reconciliation bridge delta = $0
[  ] Date range: no fechas antes de 2025-01-01
[  ] Git tag RIPLEY_POST_FIX creado
```

### 8.3 Criterios de rechazo (NO ACEPTAR)

```
[  ] Cualquier regression test FALLA
[  ] Delta > $1,000 en Importe total vs XLSX correct
[  ] Cualquier marketplace NO-RIPLEY cambia su total
[  ] SQL ≠ API (endpoint devuelve valor diferente al ledger)
[  ] DB no se puede abrir después del fix (corrupción)
[  ] Rollback no funciona (no se puede restaurar snapshot)
```

### 8.4 Checklist de ejecución

```
□ S1 — SHA256 de 46 XLSX
□ S2 — Snapshot de DB
□ S3 — Ripley ledger export
□ S4 — Importe by month
□ S5 — Ventas export
□ S6 — Concepts by year
□ S7 — Concept totals
□ S8 — 14/14 regression baseline
□ S9 — API baseline
□ S10 — Git tag RIPLEY_PRE_FIX
□ Fix aplicado (dayfirst=True en líneas 382, 400)
□ DELETE + INSERT de Ripley
□ Verificación post-fix (row counts, totals)
□ 14/14 regression PASS
□ SQL = API = UI = $0 diff
□ Recertificación emitida
□ Git tag RIPLEY_POST_FIX
□ Rollback capability verificada
□ Stakeholder notification enviada
```

---

## ANEXO A: Líneas a modificar

```diff
  # engine/v4/surgical_loader.py:382
- sale_date': pd.to_datetime(df[c_fecha], errors='coerce') if c_fecha else None,
+ sale_date': pd.to_datetime(df[c_fecha], dayfirst=True, errors='coerce') if c_fecha else None,

  # engine/v4/surgical_loader.py:400
- try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
+ try: fecha = pd.to_datetime(row[c_fecha], dayfirst=True) if c_fecha else None
```

## ANEXO B: Script de verificación pre-fix

```python
"""Pre-fix validation script — run BEFORE any changes"""
import duckdb, hashlib, json, os, glob

db = duckdb.connect(r'data/db/meli_financial_v4.db')
results = {}

# 1. Baseline totals per marketplace
for mp in ['RIPLEY', 'ML', 'PARIS', 'FALABELLA']:
    r = db.execute(f"SELECT COUNT(*), COALESCE(SUM(monto),0) FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchone()
    results[f'{mp}_ledger'] = {'rows': r[0], 'total': float(r[1])}

# 2. Ripley Importe del pedido by month
r = db.execute("""
    SELECT strftime(fecha, '%Y-%m') as m, SUM(monto) as t
    FROM marketplace_ledger_v1
    WHERE marketplace='RIPLEY' AND detalle='Importe del pedido'
    GROUP BY m ORDER BY m
""").fetchdf()
results['ripley_importe_by_month'] = {str(r['m'][i]): float(r['t'][i]) for i in range(len(r))}

# 3. Ventas count
r = db.execute("SELECT COUNT(*) FROM ventas_marketplace WHERE marketplace='RIPLEY'").fetchone()
results['ventas_count'] = r[0]

# 4. XLSX SHA256
xlsx_dir = r'01_Raw/RIPLEY/Resumen financiero'
results['xlsx_count'] = len(glob.glob(os.path.join(xlsx_dir, '*.xlsx')))

# 5. All concepts
r = db.execute("""
    SELECT detalle, SUM(monto) as t FROM marketplace_ledger_v1
    WHERE marketplace='RIPLEY' GROUP BY detalle ORDER BY t DESC
""").fetchdf()
results['concepts'] = {str(r['detalle'][i]): float(r['t'][i]) for i in range(len(r))}

with open('pre_fix_baseline.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(json.dumps(results, indent=2, default=str))
db.close()
```

## ANEXO C: Script de verificación post-fix

```python
"""Post-fix validation script — run AFTER reload"""
import duckdb, json

db = duckdb.connect(r'data/db/meli_financial_v4.db')
with open('pre_fix_baseline.json') as f:
    pre = json.load(f)

# 1. Unchanged marketplaces
for mp in ['ML', 'PARIS', 'FALABELLA']:
    r = db.execute(f"SELECT COUNT(*), COALESCE(SUM(monto),0) FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchone()
    post_rows, post_total = r[0], float(r[1])
    assert post_rows == pre[f'{mp}_ledger']['rows'], f"{mp} rows changed: {post_rows} vs {pre[f'{mp}_ledger']['rows']}"
    assert abs(post_total - pre[f'{mp}_ledger']['total']) < 1, f"{mp} total changed"
    print(f"  {mp}: OK (rows={post_rows}, total=${post_total:,.2f})")

# 2. Ripley corrected
r = db.execute("""
    SELECT strftime(fecha, '%Y-%m') as m, SUM(monto) as t
    FROM marketplace_ledger_v1
    WHERE marketplace='RIPLEY' AND detalle='Importe del pedido'
    GROUP BY m ORDER BY m
""").fetchdf()
print(f"\n  RIPLEY Importe del pedido post-fix:")
total_correct = 0.0
for _, row in r.iterrows():
    total_correct += float(row['t'])
    pre_val = pre['ripley_importe_by_month'].get(str(row['m']), 0)
    delta = float(row['t']) - pre_val
    print(f"    {row['m']}: ${float(row['t']):>12,.2f} (Δ vs pre: ${delta:>12,.2f})")
print(f"    TOTAL post-fix: ${total_correct:,.2f}")
print(f"    Target (year>=2025): $353,160,324")
print(f"    Delta vs target: ${total_correct - 353160324:,.2f}")

# 3. Phantom months check
for m in ['2026-06','2026-07','2026-08','2026-09','2026-10','2026-11','2026-12']:
    val = pre['ripley_importe_by_month'].get(m, 0)
    print(f"    Pre-fix phantom {m}: ${val:,.2f}")
    val_post = float(r[r['m'] == m]['t'].iloc[0]) if m in r['m'].values else 0
    print(f"    Post-fix {m}: ${val_post:,.2f}")

db.close()
```

---

**Fin del RFC-001**

Este documento es un diseño de corrección controlada. **NO EJECUTAR** sin autorización explícita del CEO/CTO. El fix es trivial (2 caracteres: `dayfirst=True`), pero el impacto en el pipeline financiero requiere gobernanza.
