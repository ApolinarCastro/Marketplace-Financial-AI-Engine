"""PLAN QUIRURGICO — genera mapa id_transaccion -> fecha_corregida desde raw files"""
import duckdb, os, json
from pathlib import Path
import pandas as pd

TMP_DB = Path(os.environ['TEMP']) / "poscobro_v2.db"
con = duckdb.connect(str(TMP_DB), read_only=True)

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
POS_DIR = ROOT / "01_Raw" / "ML" / "Poscobro"

files_in_ledger = [
    '1 enero 2025 - 1 julio 2025.xlsx',
    '1 enero 2026 - 1 mayo 2026.xlsx',
    '1 julio 2025 - 1 enero 2026.xlsx'
]

print("=" * 100)
print("PLAN QUIRURGICO POSCOBRO — MAPA DE CORRECCION")
print("=" * 100)

all_corrections = []

for fname in files_in_ledger:
    f = POS_DIR / fname
    df = pd.read_excel(f, engine='calamine')
    
    c_dat = None
    for c in df.columns:
        if 'datecreated' in str(c).lower() or 'fecha' in str(c).lower():
            c_dat = c
            break
    
    c_ord = None
    for c in df.columns:
        if 'orderid' in str(c).lower() or 'orden' in str(c).lower() or 'transaccion' in str(c).lower():
            c_ord = c
            break
    
    c_op = None
    for c in df.columns:
        if 'operationid' in str(c).lower() or 'operacionid' in str(c).lower():
            c_op = c
            break
    
    c_amt = None
    for c in df.columns:
        if 'operation_amount' in str(c).lower():
            c_amt = c
            break
    
    c_dev = None
    for c in df.columns:
        if 'montodevolucion' in str(c).lower():
            c_dev = c
            break
    
    c_det = None
    for c in df.columns:
        if 'reasondetail' in str(c).lower() or 'motivo' in str(c).lower() or 'detalle' in str(c).lower():
            c_det = c
            break
    
    row_data = []
    for idx in range(len(df)):
        raw_val = df.iloc[idx][c_dat]
        try:
            fecha_before = pd.to_datetime(raw_val)
        except:
            fecha_before = None
        fecha_after = pd.to_datetime(raw_val, dayfirst=True, errors="coerce")
        
        monto_raw = float(pd.to_numeric(df.iloc[idx][c_amt], errors='coerce') or 0) if c_amt else 0
        monto_dev = float(pd.to_numeric(df.iloc[idx][c_dev], errors='coerce') or 0) if c_dev else 0
        monto = monto_dev * -1 if monto_dev != 0 else monto_raw
        
        c_op_val = str(df.iloc[idx][c_op]).strip() if c_op and pd.notna(df.iloc[idx][c_op]) else ""
        if c_op_val and c_op_val.lower() not in ['', '0', '0.0', 'nan', 'none']:
            trans_id = f"POS_{c_op_val}_{fname}_{idx}"
        else:
            trans_id = f"POS_{fname}_{idx}"
        
        raw_det = str(df.iloc[idx][c_det]).strip() if c_det and pd.notna(df.iloc[idx][c_det]) else "Ajuste Poscobro"
        raw_ord = str(df.iloc[idx][c_ord]) if c_ord else ""
        
        is_swapped = pd.notna(fecha_before) and pd.notna(fecha_after) and fecha_before != fecha_after
        
        row_data.append({
            'id_transaccion': trans_id,
            'fecha_before': fecha_before,
            'fecha_after': fecha_after,
            'fecha_before_str': str(fecha_before)[:10] if pd.notna(fecha_before) else "NaT",
            'fecha_after_str': str(fecha_after)[:10] if pd.notna(fecha_after) else "NaT",
            'monto': monto,
            'detalle': raw_det[:30],
            'archivo_origen': fname,
            'idx': idx,
            'is_swapped': is_swapped,
        })
    
    all_corrections.extend(row_data)
    
    # Per-file summary
    swapped = [r for r in row_data if r['is_swapped']]
    swapped_amt = sum(abs(r['monto']) for r in swapped)
    print(f"\n{fname}")
    print(f"  Total rows: {len(row_data)}")
    print(f"  Swapped: {len(swapped)} ({len(swapped)/len(row_data)*100:.1f}%)")
    print(f"  Swapped amount: ${swapped_amt:>12,.2f}")

# Verify: can we match these back to ledger?
print(f"\n{'='*100}")
print("VERIFYING LEDGER MATCH (sample 10 corrections vs ledger)")
print(f"{'='*100}")

sample = [r for r in all_corrections if r['is_swapped']][:10]
for r in sample:
    tid = r['id_transaccion']
    ldg = con.execute("""
        SELECT id_transaccion, fecha, monto, archivo_origen
        FROM marketplace_ledger_v1
        WHERE id_transaccion = ?
    """, [tid]).fetchone()
    if ldg:
        ldg_date = str(ldg[1])[:10] if ldg[1] else "NULL"
        match = "OK" if ldg_date == r['fecha_before_str'] else "MISMATCH"
        print(f"  id={str(tid)[:40]:40s} ledger_fecha={ldg_date} raw_before={r['fecha_before_str']} after={r['fecha_after_str']} [{match}]")
    else:
        print(f"  id={str(tid)[:40]:40s} NOT FOUND IN LEDGER")

# Export the correction map as JSON
correction_map = [r for r in all_corrections if r['is_swapped']]
print(f"\n{'='*100}")
print(f"EXPORT: {len(correction_map)} correction entries")
print(f"{'='*100}")

# Group by archivo_origen for stats
from collections import defaultdict
by_file = defaultdict(list)
for r in correction_map:
    by_file[r['archivo_origen']].append(r)

for fname, entries in sorted(by_file.items()):
    print(f"\n{fname}: {len(entries)} corrections")
    amt = sum(abs(e['monto']) for e in entries)
    print(f"  Total amount: ${amt:>12,.2f}")
    # Show periods affected
    periods = defaultdict(float)
    for e in entries:
        periods[e['fecha_before_str'][:7]] += abs(e['monto'])
    print(f"  Per period (outgoing):")
    for p in sorted(periods):
        print(f"    {p}: ${periods[p]:>10,.2f}")
    periods_dest = defaultdict(float)
    for e in entries:
        periods_dest[e['fecha_after_str'][:7]] += abs(e['monto'])
    print(f"  Per period (incoming):")
    for p in sorted(periods_dest):
        print(f"    {p}: ${periods_dest[p]:>10,.2f}")

# Write JSON mapping
output = ROOT / "data" / "poscobro_correction_map.json"
# Convert datetime to string for JSON
json_data = []
for r in correction_map:
    json_data.append({
        'id_transaccion': r['id_transaccion'],
        'fecha_before': r['fecha_before_str'],
        'fecha_after': r['fecha_after_str'],
        'monto': r['monto'],
        'archivo_origen': r['archivo_origen'],
    })

with open(str(output), 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
print(f"\nCorrection map saved: {output}")

con.close()
print("\nDone.")
