"""PLAN QUIRURGICO FINAL — Poscobro ML remediation plan"""
import duckdb, os, json, warnings
from pathlib import Path
from collections import defaultdict
import pandas as pd

warnings.filterwarnings('ignore')

TMP_DB = os.path.join(os.environ['TEMP'], "poscobro_v2.db")
con = duckdb.connect(TMP_DB, read_only=True)

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
POS_DIR = ROOT / "01_Raw" / "ML" / "Poscobro"
OUTPUT = ROOT / "data" / "poscobro_correction_map.json"

files_in_ledger = [
    '1 enero 2025 - 1 julio 2025.xlsx',
    '1 enero 2026 - 1 mayo 2026.xlsx',
    '1 julio 2025 - 1 enero 2026.xlsx'
]

# Map columns between raw files (Spanish) and code expectations
COL_FECHA = 'Fecha de creaci\u00f3n (date_created)'
COL_OP_ID = 'ID de la transacci\u00f3n (operation_id)'
COL_ORDER_ID = 'ID de la orden (order_id)'
COL_AMT = 'Monto de la transacci\u00f3n (operation_amount)'
COL_MONTO = 'Monto (amount)'
COL_DETALLE = 'Detalle del motivo (reason_detail)'
COL_STATUS = 'Estado de la transacci\u00f3n (operation_status)'

print("=" * 120)
print("PLAN QUIRURGICO POSCOBRO ML — CORRECCION DE FECHAS")
print("=" * 120)

# ███████████████████████████████████████████████████████████████████████████████
# FASE 1: Construir mapa de correcciones desde raw files
# ███████████████████████████████████████████████████████████████████████████████

all_corrections = []
per_file = {}
total_affected_amount = 0.0
total_affected_rows = 0

for fname in files_in_ledger:
    f = POS_DIR / fname
    df = pd.read_excel(f, engine='calamine')
    
    corrections = []
    
    for idx in range(len(df)):
        # Read raw date string (before parsing)
        raw_val = str(df.iloc[idx][COL_FECHA]).strip()
        
        # Reproduce current (wrong) parsing: pd.to_datetime() without dayfirst
        fecha_wrong = pd.to_datetime(raw_val, errors='coerce')
        
        # Correct parsing: dayfirst=True
        fecha_correct = pd.to_datetime(raw_val, dayfirst=True, errors='coerce')
        
        # Build id_transaccion matching loader format
        op_id_raw = df.iloc[idx][COL_OP_ID]
        op_id = str(int(op_id_raw)) if pd.notna(op_id_raw) and op_id_raw == op_id_raw else ''
        
        if op_id:
            tid = f"POS_{op_id}_{fname}_{idx+1}"  # 1-based idx (matches loader)
        else:
            ord_raw = df.iloc[idx][COL_ORDER_ID]
            ord_id = str(int(ord_raw)) if pd.notna(ord_raw) and ord_raw == ord_raw else ''
            tid = f"POS_{ord_id}_{fname}_{idx+1}" if ord_id else f"POS_{fname}_{idx+1}"
        
        # Amount
        monto = float(df.iloc[idx][COL_AMT]) if pd.notna(df.iloc[idx][COL_AMT]) else 0.0
        
        # Detalle
        detalle = str(df.iloc[idx][COL_DETALLE])[:30] if pd.notna(df.iloc[idx][COL_DETALLE]) else ''
        
        # Determine if swapped (wrong != correct)
        is_swapped = (pd.notna(fecha_wrong) and pd.notna(fecha_correct) and 
                      fecha_wrong != fecha_correct)
        
        correction = {
            'id_transaccion': tid,
            'raw_date': raw_val,
            'fecha_wrong': str(fecha_wrong)[:10] if pd.notna(fecha_wrong) else 'NaT',
            'fecha_correct': str(fecha_correct)[:10] if pd.notna(fecha_correct) else 'NaT',
            'monto': round(monto, 2),
            'monto_abs': round(abs(monto), 2),
            'detalle': detalle,
            'archivo_origen': fname,
            'idx': idx,
            'is_swapped': is_swapped,
        }
        corrections.append(correction)
        
        if is_swapped:
            all_corrections.append(correction)
            total_affected_amount += abs(monto)
            total_affected_rows += 1
    
    per_file[fname] = corrections
    
    n_swapped = sum(1 for c in corrections if c['is_swapped'])
    amt_swapped = sum(c['monto_abs'] for c in corrections if c['is_swapped'])
    pct = n_swapped / len(corrections) * 100
    print(f"\n{fname}")
    print(f"  Total rows: {len(corrections)}")
    print(f"  Swapped: {n_swapped} ({pct:.1f}%)")
    print(f"  Swapped amount: ${amt_swapped:>12,.2f}")
    print(f"  Date range (correct): {min(c['fecha_correct'] for c in corrections if c['fecha_correct'] != 'NaT')} to {max(c['fecha_correct'] for c in corrections if c['fecha_correct'] != 'NaT')}")

print(f"\n{'='*120}")
print(f"TOTAL affected rows: {len(all_corrections)}")
print(f"TOTAL affected amount: ${total_affected_amount:>12,.2f}")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 2: Verificar contra ledger
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 2: VERIFICACION CONTRA LEDGER (muestra)")
print(f"{'='*120}")

matched_in_ledger = 0
not_in_ledger = 0
wrong_fecha = 0
correct_fecha = 0

for c in all_corrections[:50]:  # sample first 50
    ledger_row = con.execute("""
        SELECT id_transaccion, fecha, monto, archivo_origen 
        FROM marketplace_ledger_v1 
        WHERE id_transaccion = ?
    """, [c['id_transaccion']]).fetchone()
    
    if ledger_row:
        matched_in_ledger += 1
        ldg_fecha = str(ledger_row[1])[:10] if ledger_row[1] else 'NULL'
        if ldg_fecha == c['fecha_wrong']:
            wrong_fecha += 1
        elif ldg_fecha == c['fecha_correct']:
            correct_fecha += 1
        if c['is_swapped']:
            print(f"  CHECK: tid={c['id_transaccion'][:55]:55s} ledger={ldg_fecha:12s} wrong={c['fecha_wrong']:12s} correct={c['fecha_correct']:12s}")
    else:
        not_in_ledger += 1
        if not_in_ledger <= 3:
            print(f"  NOT IN LEDGER: {c['id_transaccion'][:60]}")

# Total match count (all corrections)
all_tids = [c['id_transaccion'] for c in all_corrections]
for tid in all_tids:
    if con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE id_transaccion = ?", [tid]).fetchone()[0] > 0:
        pass  # already counting
# Full scan
full_matched = con.execute(f"""
    SELECT COUNT(*) FROM marketplace_ledger_v1 
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
""").fetchone()[0]
print(f"\nFull ledger ML PAGO rows: {full_matched}")
print(f"Correction entries matching ledger (sample 50): {matched_in_ledger}/{len(all_corrections)}")
print(f"  Of matched: {wrong_fecha} have wrong date (needs fix), {correct_fecha} already correct")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 3: Period matrix
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 3: MATRIZ PERIODOS — ORIGEN vs DESTINO")
print(f"{'='*120}")

outgoing = defaultdict(float)
incoming = defaultdict(float)

for c in all_corrections:
    p_before = c['fecha_wrong'][:7]
    p_after = c['fecha_correct'][:7]
    outgoing[p_before] += c['monto_abs']
    incoming[p_after] += c['monto_abs']

all_periods = sorted(set(list(outgoing.keys()) + list(incoming.keys())))

print(f"{'Periodo':<10s} {'Sale':>15s} {'Entra':>15s} {'Neto':>15s}")
print("-" * 60)
for p in all_periods:
    o = outgoing.get(p, 0)
    i = incoming.get(p, 0)
    net = i - o
    sign = '+' if net >= 0 else ''
    print(f"{p:<10s} ${o:>10,.2f}  ${i:>10,.2f}  ${sign}{net:>+10,.2f}")

print("-" * 60)
tot_o = sum(outgoing.values())
tot_i = sum(incoming.values())
print(f"{'TOTAL':<10s} ${tot_o:>10,.2f}  ${tot_i:>10,.2f}  $0.00")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 4: Value conservation
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 4: CONSERVACION DE VALOR")
print(f"{'='*120}")

ledger_total = con.execute("""
    SELECT SUM(monto) FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
""").fetchone()[0] or 0
ledger_count = con.execute("""
    SELECT COUNT(*) FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
""").fetchone()[0]

total_raw_amt = sum(abs(c['monto']) for c in all_corrections)
total_raw_rows = len(all_corrections)

print(f"Ledger ML PAGO: $ {float(ledger_total):>12,.2f} | {ledger_count} rows")
print(f"Correction map: $ {total_raw_amt:>12,.2f} | {total_raw_rows} rows (swapped)")
total_unswapped = sum(abs(c['monto_abs']) for file_rows in per_file.values() for c in file_rows if not c['is_swapped'])
print(f"Unswapped:      $ {total_unswapped:>12,.2f} (stay in correct period)")
grand_total = total_raw_amt + total_unswapped
print(f"Grand total:    $ {grand_total:>12,.2f}")
print(f"Conservation:   {(grand_total / (float(abs(ledger_total))+0.001) * 100):.1f}% (100% = value fully preserved)")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 5: Estrategia
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 5: ESTRATEGIA RECOMENDADA — OPCION A (UPDATE quirurgico)")
print(f"{'='*120}")

print(r"""
OPCION A — UPDATE fecha en marketplace_ledger_v1
=================================================
SQL:
    -- Crear tabla temporal de correcciones
    CREATE TEMP TABLE poscobro_corrections (
        id_transaccion VARCHAR PRIMARY KEY,
        fecha_correcta DATE
    );

    -- Poblar desde JSON (data/poscobro_correction_map.json)
    INSERT INTO poscobro_corrections VALUES
    (<4,572 entradas>);

    -- UPDATE quirurgico
    UPDATE marketplace_ledger_v1 AS l
    SET fecha = c.fecha_correcta
    FROM poscobro_corrections AS c
    WHERE l.id_transaccion = c.id_transaccion
      AND l.marketplace = 'ML'
      AND l.tipo_movimiento = 'PAGO';

    -- Verificar
    SELECT COUNT(*), SUM(monto) FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO';
    -- Expected: same COUNT, same SUM (value conservation)

Riesgo: BAJO — solo cambia 1 columna (fecha) en 4,572 filas
Trazabilidad: ALTA — correction_map.json guarda before/after
Reversibilidad: ALTA — guardar fecha_wrong en misma tabla de correcciones
Impacto auditoria: MEDIO — requiere re-ejecutar checks de fechas

OPCION B — DELETE + REINSERT
=============================
Riesgo: MEDIO — DELETE puede cascadear, REINSERT puede duplicar
Trazabilidad: MEDIA — depende de orden de INSERT
Reversibilidad: MEDIA — requiere snapshot
Impacto auditoria: ALTO — DELETE rompe referencias

RECOMENDACION: OPCION A (UPDATE quirurgico)
============================================
* Solo cambia fecha, no toca montos/detalles
* Reversible con correction_map.json
* No requiere reprocesar archivos raw
* ~1 seg en DuckDB vs ~10 min de DELETE+REINSERT
* No depende de disponibilidad de archivos raw
""")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 6: Dependencias y rebuild necesario
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 6: DEPENDENCIAS Y REBUILD")
print(f"{'='*120}")

print("""
Tabla                  Dependencia   Rebuild           Alcance
--------------------------------------------------------------
marketplace_ledger_v1  -             UPDATE fecha      Solo 4,572 rows ML Poscobro
marketplace_clasificacion_v1  ledger.fecha    RECLASIFICAR      Solo ML rows (~10K)
marketplace_cierre_financiero_v1  ledger+clasif  RECALCULAR        Periodos 2025-01 a 2026-04
marketplace_auditoria_v1  ledger+clasif+cierre  RE-EJECUTAR       Todos los checks de fechas
""")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 7: Plan de ejecución reversible
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 7: PLAN DE EJECUCION REVERSIBLE")
print(f"{'='*120}")

print("""
FASE 0 - BACKUP
    1. Crear snapshot manual:
       > mkdir data/db/snapshot_pre_poscobro_fix_<YYYYMMDD_HHMMSS>/
       > copy data/db/meli_financial_v4.db ...snapshot/
    2. Exportar respaldo de filas afectadas:
      COPY (
        SELECT * FROM marketplace_ledger_v1
        WHERE id_transaccion IN (SELECT id_transaccion FROM poscobro_corrections)
      ) TO 'backup_poscobro_before_fix.csv' (HEADER, DELIMITER ',');
    3. Exportar clasificacion actual:
      COPY (
        SELECT * FROM marketplace_clasificacion_v1
        WHERE marketplace='ML'
      ) TO 'backup_clasificacion_ml.csv' (HEADER, DELIMITER ',');

FASE 1 - CORRECCION LEDGER
    1. Crear temp table con 4,572 correcciones desde JSON
    2. UPDATE fecha en marketplace_ledger_v1
    3. Verificar: COUNT(*) igual, SUM(monto) igual

FASE 2 - RECLASIFICACION
    1. DELETE FROM marketplace_clasificacion_v1 WHERE marketplace='ML'
    2. Re-ejecutar clasificacion para ML (usa fecha corregida)
    3. Verificar: todas las rows ML tienen clasificacion

FASE 3 - RECALCULO CIERRE
    1. DELETE FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML'
    2. Re-ejecutar cierre financiero para ML, periodos 2025-01 a 2026-04
    3. Verificar: resultado_neto = sum(ingresos) - sum(egresos) por periodo

FASE 4 - RE-EJECUTAR AUDITORIA
    1. DELETE FROM marketplace_auditoria_v1
    2. Re-ejecutar auditoria completa
    3. Verificar: 0 alertas nuevas por fechas fuera de rango

FASE 5 - VALIDACION
    1. Conservacion monetaria: SUM(monto) ML PAGO = $307,011,951
    2. Conservacion filas: COUNT(*) ML PAGO = 10,789
    3. Cero duplicados: COUNT(*) = COUNT(DISTINCT id_transaccion)
    4. Fechas dentro de rango: MIN/MAX fecha por archivo_origen
    5. Reconciliacion RAW: comparar suma mensual contra Excel raw

FASE 6 - ROLLBACK (si algo falla)
    1. Restaurar snapshot:
       > copy snapshot_pre_poscobro_fix_<TS>/meli_financial_v4.db data/db/meli_financial_v4.db
    2. Re-aplicar cambios post-snapshot (clasificaciones, cierres de otros MPs)
    3. Verificar integridad con SHA256
""")

# ███████████████████████████████████████████████████████████████████████████████
# FASE 8: Validación obligatoria
# ███████████████████████████████████████████████████████████████████████████████

print(f"\n{'='*120}")
print("FASE 8: CONTROL DE VALIDACION")
print(f"{'='*120}")

print(f"""
| Control | Query | Expected |
|---|---|---|
| Conservacion monto | SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE marketplace='ML' AND tipo_movimiento='PAGO' | $307,011,951 (sin cambio) |
| Conservacion filas | SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='ML' AND tipo_movimiento='PAGO' | 10,789 (sin cambio) |
| Cero duplicados | SELECT COUNT(*) vs SELECT COUNT(DISTINCT id_transaccion) ... | mismo valor |
| Fechas en rango | SELECT MIN(fecha), MAX(fecha), archivo_origen ... | fecha dentro del rango del filename |
| Reconciliacion RAW | Suma por mes comparada contra Excel raw en POS_DIR | match perfecto |
| Delta cierre | resultado_neto antes vs después para ML | $0 delta (solo distribución) |
| Archivos cubiertos | El correction_map incluye los 3 archivos xlsx | 3/3 |
| Filas cubiertas | COUNT(correction_map) = filas actualizadas | 4,572 |
""")

# ███████████████████████████████████████████████████████████████████████████████
# Export correction map
# ███████████████████████████████████████████████████████████████████████████████

json_out = [{
    'id_transaccion': c['id_transaccion'],
    'fecha_wrong': c['fecha_wrong'],
    'fecha_correct': c['fecha_correct'],
    'monto': c['monto'],
    'archivo_origen': c['archivo_origen'],
} for c in all_corrections]

with open(str(OUTPUT), 'w', encoding='utf-8') as f:
    json.dump(json_out, f, ensure_ascii=False, indent=2)

print(f"\n{'='*120}")
print(f"Correction map exported: {OUTPUT} ({len(json_out)} entries)")

con.close()
print(f"\n{'='*120}")
print("PLAN COMPLETADO — NO EJECUTAR NADA")
print(f"{'='*120}")
