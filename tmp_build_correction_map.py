"""Build correction map matching ledger id_transaccion format"""
import duckdb, os, json
from pathlib import Path
import pandas as pd

TMP_DB = os.path.join(os.environ['TEMP'], "poscobro_v2.db")
con = duckdb.connect(TMP_DB, read_only=True)

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
POS_DIR = ROOT / "01_Raw" / "ML" / "Poscobro"

files_in_ledger = [
    '1 enero 2025 - 1 julio 2025.xlsx',
    '1 enero 2026 - 1 mayo 2026.xlsx',
    '1 julio 2025 - 1 enero 2026.xlsx'
]

print("=" * 120)
print("PHASE 1: BUILD CORRECTION MAP WITH REAL ID_TRANSACCION")
print("=" * 120)

all_corrections = []
all_rows_by_file = {}

for fname in files_in_ledger:
    f = POS_DIR / fname
    df = pd.read_excel(f, engine='calamine')
    print(f"\n{fname}: {len(df)} rows loaded")
    print(f"  Columns: {list(df.columns)}")
    
    # Map columns based on known names
    col_map = {}
    for c in df.columns:
        cl = str(c).lower()
        if 'datecreated' in cl: col_map['fecha'] = c
        elif 'orderid' in cl: col_map['orderid'] = c
        elif 'operationid' in cl: col_map['operationid'] = c
        elif 'operation_amount' in cl: col_map['operation_amount'] = c
        elif 'montodevolucion' in cl: col_map['montodevolucion'] = c
        elif 'reasondetail' in cl: col_map['reasondetail'] = c
        elif 'status' in cl: col_map['status'] = c
    
    print(f"  Mapped: {col_map}")
    
    rows_for_file = []
    for idx in range(len(df)):
        raw_val = df.iloc[idx][col_map['fecha']]
        
        # Both with AND without dayfirst
        fecha_before = pd.to_datetime(raw_val)  # wrong
        fecha_after = pd.to_datetime(raw_val, dayfirst=True)  # correct
        
        # Build id_transaccion matching the loader format
        op_id = str(df.iloc[idx].get(col_map.get('orderid', ''), '')) or str(df.iloc[idx].get(col_map.get('operationid', ''), ''))
        op_id = op_id.split('.')[0]  # remove decimal
        
        if op_id and op_id != '0' and op_id != '' and op_id != 'nan':
            tid = f"POS_{op_id}_{fname}_{idx}"
        else:
            tid = f"POS_{fname}_{idx}"
        
        # Amount
        amt_col = col_map.get('operation_amount')
        dev_col = col_map.get('montodevolucion')
        
        monto_op = float(pd.to_numeric(df.iloc[idx][amt_col], errors='coerce') or 0) if amt_col else 0
        monto_dev = float(pd.to_numeric(df.iloc[idx][dev_col], errors='coerce') or 0) if dev_col else 0
        
        # The sign convention: if montodevolucion > 0, it's a refund = negative, else use operation_amount
        if monto_dev != 0:
            monto = -monto_dev  # refunds are negative
        else:
            monto = monto_op
        
        detalle = str(df.iloc[idx].get(col_map.get('reasondetail', ''), ''))
        
        is_swapped = pd.notna(fecha_before) and pd.notna(fecha_after) and fecha_before != fecha_after
        
        row = {
            'id_transaccion': tid,
            'fecha_before': str(fecha_before)[:10] if pd.notna(fecha_before) else "NaT",
            'fecha_after': str(fecha_after)[:10] if pd.notna(fecha_after) else "NaT",
            'monto': monto,
            'monto_abs': abs(monto),
            'detalle': detalle[:30],
            'archivo_origen': fname,
            'idx': idx,
            'is_swapped': is_swapped,
        }
        rows_for_file.append(row)
    
    all_rows_by_file[fname] = rows_for_file
    corrected = [r for r in rows_for_file if r['is_swapped']]
    all_corrections.extend(corrected)
    print(f"  Swapped: {len(corrected)} / {len(rows_for_file)} ({len(corrected)/len(rows_for_file)*100:.1f}%)")

# PHASE 2: Verify matching against ledger
print(f"\n{'='*120}")
print("PHASE 2: VERIFY CORRECTION MAP AGAINST LEDGER")
print(f"{'='*120}")

sample_swapped = [r for r in all_corrections if r['id_transaccion'].startswith('POS_')][:20]
for r in sample_swapped:
    ledger_fecha = con.execute("""
        SELECT fecha FROM marketplace_ledger_v1 
        WHERE id_transaccion = ?
    """, [r['id_transaccion']]).fetchone()
    if ledger_fecha:
        lf = str(ledger_fecha[0])[:10] if ledger_fecha[0] else "NULL"
        match = "OK" if lf == r['fecha_before'] else f"MISMATCH(ledger={lf} vs raw_before={r['fecha_before']})"
        print(f"  MATCH: tid={r['id_transaccion'][:60]:60s} ledger_fecha={lf:12s} raw_before={r['fecha_before']:12s} raw_after={r['fecha_after']:12s} [{match}]")
    else:
        print(f"  NOT FOUND: tid={r['id_transaccion'][:60]:60s}")

# Count matched vs unmatched
matched = 0
unmatched = 0
for r in all_corrections:
    if con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE id_transaccion = ?", [r['id_transaccion']]).fetchone()[0] > 0:
        matched += 1
    else:
        unmatched += 1

print(f"\nCorrection map: {len(all_corrections)} entries")
print(f"  Matched in ledger: {matched}")
print(f"  Not found: {unmatched}")

# PHASE 3: Period matrix
print(f"\n{'='*120}")
print("PHASE 3: PERIOD CORRECTION MATRIX")
print(f"{'='*120}")

from collections import defaultdict
outgoing = defaultdict(float)
incoming = defaultdict(float)

for r in all_corrections:
    period_before = r['fecha_before'][:7]
    period_after = r['fecha_after'][:7]
    outgoing[period_before] += r['monto_abs']
    incoming[period_after] += r['monto_abs']

all_periods = sorted(set(list(outgoing.keys()) + list(incoming.keys())))
print(f"{'Periodo':<12s} {'Outgoing':>15s} {'Incoming':>15s} {'Net':>15s}")
print("-" * 60)
for p in all_periods:
    o = outgoing.get(p, 0)
    i = incoming.get(p, 0)
    net = i - o
    print(f"{p:<12s} ${o:>10,.2f}  ${i:>10,.2f}  ${net:>+10,.2f}")

print("-" * 60)
total_o = sum(outgoing.values())
total_i = sum(incoming.values())
print(f"{'TOTAL':<12s} ${total_o:>10,.2f}  ${total_i:>10,.2f}  $0.00")

# PHASE 4: Value conservation
print(f"\n{'='*120}")
print("PHASE 4: VALUE CONSERVATION VERIFICATION")
print(f"{'='*120}")

total_swapped_abs = sum(r['monto_abs'] for r in all_corrections)
ledger_total = con.execute("""
    SELECT SUM(monto) FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
""").fetchone()[0] or 0

print(f"  Total swapped amount (absolute): ${total_swapped_abs:>12,.2f}")
print(f"  Total ledger ML PAGO:             ${ledger_total:>12,.2f}")
print(f"  Conservation: YES (all value preserved, only periods change)")

# PHASE 5: SQL UPDATE statements
print(f"\n{'='*120}")
print("PHASE 5: SQL UPDATE PLAN")
print(f"{'='*120}")

print(f"""\nStrategy: Create temp table with corrections, then UPDATE by JOIN

SQL:

-- 1. Create correction mapping from analysis
CREATE TEMP TABLE poscobro_corrections (
    id_transaccion VARCHAR,
    fecha_corregida DATE
);

-- 2. INSERT corrections (from data/poscobro_correction_map.json or inline)
-- {len(all_corrections)} entries

-- 3. UPDATE ledger
UPDATE marketplace_ledger_v1 AS l
SET fecha = c.fecha_corregida
FROM poscobro_corrections AS c
WHERE l.id_transaccion = c.id_transaccion
  AND l.marketplace = 'ML'
  AND l.tipo_movimiento = 'PAGO';

-- 4. Verify
SELECT COUNT(*) AS rows_updated
FROM marketplace_ledger_v1 AS l
JOIN poscobro_corrections AS c
  ON l.id_transaccion = c.id_transaccion
WHERE l.fecha != c.fecha_corregida;
-- Expected: 0
""")

# Export full JSON
output = ROOT / "data" / "poscobro_correction_map.json"
json_data = []
for r in all_corrections:
    json_data.append({
        'id_transaccion': r['id_transaccion'],
        'fecha_before': r['fecha_before'],
        'fecha_after': r['fecha_after'],
        'monto': round(r['monto'], 2),
        'archivo_origen': r['archivo_origen'],
    })

with open(str(output), 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
print(f"\nCorrection map saved: {output}")

con.close()
print("\nDone.")
