"""Generar BASELINE_ESTABLE_V6"""
from __future__ import annotations
import hashlib, json, shutil, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_SRC = ROOT / "data" / "db" / "meli_financial_v4.db"

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
SNAPSHOT_DIR = ROOT / "data" / "db" / f"snapshot_baseline_v6_{ts}"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

print(f"1. Snapshot -> {SNAPSHOT_DIR}")

# Copy DB
DB_DST = SNAPSHOT_DIR / "meli_financial_v4.db"
shutil.copy2(DB_SRC, DB_DST)
db_size = DB_DST.stat().st_size
print(f"   DB copied: {db_size:,} bytes")

# SHA256
sha = hashlib.sha256()
with open(DB_DST, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
        sha.update(chunk)
db_sha256 = sha.hexdigest()
print(f"   SHA256: {db_sha256}")

# Compute stats via DuckDB
import duckdb
conn = duckdb.connect(str(DB_DST))

total_rows = int(conn.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0])
total_sum = float(conn.execute("SELECT COALESCE(SUM(monto),0) FROM marketplace_ledger_v1").fetchone()[0])

# Global stats
fg_global = conn.execute("""
    SELECT COALESCE(financial_group, 'NULL') as fg,
           COUNT(*) as cnt,
           SUM(monto) as total
    FROM marketplace_ledger_v1
    GROUP BY fg ORDER BY total DESC
""").fetchall()
global_fg = {str(r[0]): {"rows": int(r[1]), "total": float(r[2])} for r in fg_global}

# Marketplace stats
marketplaces = {}
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    rows = int(conn.execute(f"SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchone()[0])
    sm = float(conn.execute(f"SELECT COALESCE(SUM(monto),0) FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchone()[0])
    null_fg = int(conn.execute(f"SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND financial_group IS NULL").fetchone()[0])
    null_co = int(conn.execute(f"SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND clasificacion_operativa IS NULL").fetchone()[0])
    no_clas = int(conn.execute(f"SELECT COUNT(*) FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}' AND clasificacion_operativa='NO_CLASIFICADO'").fetchone()[0])
    
    fg_mp = conn.execute(f"""
        SELECT COALESCE(financial_group, 'NULL') as fg,
               COUNT(*) as cnt, SUM(monto) as total
        FROM marketplace_ledger_v1 WHERE marketplace='{mp}'
        GROUP BY fg ORDER BY total DESC
    """).fetchall()
    fg_dist = {str(r[0]): {"rows": int(r[1]), "total": float(r[2])} for r in fg_mp}
    
    # Tipos de transaccion
    tipos = conn.execute(f"""
        SELECT detalle, clasificacion_operativa,
               COALESCE(financial_group, 'NULL') as fg,
               COUNT(*) as cnt, SUM(monto) as total
        FROM marketplace_ledger_v1 WHERE marketplace='{mp}'
        GROUP BY detalle, clasificacion_operativa, fg
        ORDER BY SUM(ABS(monto)) DESC
    """).fetchall()
    tipos_list = [{"detalle": str(r[0]), "clasificacion_operativa": str(r[1]), "financial_group": str(r[2]),
                    "cnt": int(r[3]), "total": float(r[4])} for r in tipos]
    
    marketplaces[mp] = {
        "total_rows": rows,
        "sum_monto": sm,
        "null_financial_group": null_fg,
        "null_clasificacion_operativa": null_co,
        "no_clasificado": no_clas,
        "financial_groups": fg_dist,
        "transaction_types": tipos_list
    }

conn.close()

# Also SHA256 the report
report_path = ROOT / "_REPORTE_FALABELLA_REBUILD.md"
report_sha = hashlib.sha256()
with open(report_path, "rb") as f:
    report_sha.update(f.read())
report_sha256 = report_sha.hexdigest()

manifest = {
    "baseline": "V6",
    "timestamp": ts,
    "datetime": datetime.datetime.now().isoformat(),
    "db_file": "meli_financial_v4.db",
    "db_size_bytes": db_size,
    "db_sha256": db_sha256,
    "report_file": "_REPORTE_FALABELLA_REBUILD.md",
    "report_sha256": report_sha256,
    "total_rows": total_rows,
    "total_sum": total_sum,
    "global_financial_group": global_fg,
    "marketplaces": {},
    "previous_baseline": "V5",
    "previous_baseline_label": "BASELINE_ESTABLE_V5 (SUPERSEDED)",
    "current_baseline_label": "BASELINE_ESTABLE_V6 (CURRENT_STABLE)"
}

# Copy report to snapshot dir
shutil.copy2(report_path, SNAPSHOT_DIR / "_REPORTE_FALABELLA_REBUILD.md")

# Copy manifest to snapshot dir + root
manifest_path = SNAPSHOT_DIR / "MANIFEST_V6.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# Also save a pretty stats file
stats_path = SNAPSHOT_DIR / "STATS_V6.md"
with open(stats_path, "w", encoding="utf-8") as f:
    f.write(f"# BASELINE_ESTABLE_V6 - STATS\n\n")
    f.write(f"Generated: {manifest['datetime']}\n")
    f.write(f"DB SHA256: {db_sha256}\n\n")
    f.write(f"## Global\n\n")
    f.write(f"| Metric | Value |\n|---|---:|\n")
    f.write(f"| Total rows | {total_rows:,} |\n")
    f.write(f"| Total SUM | ${total_sum:,.0f} |\n\n")
    f.write(f"### Financial Groups\n\n")
    f.write(f"| Group | Rows | Total |\n|---|---|---:|\n")
    for fg, data in sorted(global_fg.items(), key=lambda x: x[1]['total'], reverse=True):
        f.write(f"| {fg} | {data['rows']:,} | ${data['total']:,.0f} |\n")
    
    for mp, data in marketplaces.items():
        f.write(f"\n## {mp}\n\n")
        f.write(f"| Metric | Value |\n|---|---:|\n")
        f.write(f"| Rows | {data['total_rows']:,} |\n")
        f.write(f"| SUM | ${data['sum_monto']:,.0f} |\n")
        f.write(f"| NULL financial_group | {data['null_financial_group']} |\n")
        f.write(f"| NULL clasificacion_operativa | {data['null_clasificacion_operativa']} |\n")
        f.write(f"| NO_CLASIFICADO | {data['no_clasificado']} |\n\n")
        f.write(f"### Financial Groups\n\n")
        f.write(f"| Group | Rows | Total |\n|---|---|---:|\n")
        for fg, d in sorted(data['financial_groups'].items(), key=lambda x: x[1]['total'], reverse=True):
            f.write(f"| {fg} | {d['rows']:,} | ${d['total']:,.0f} |\n")
        f.write(f"\n### Transaction Types\n\n")
        f.write(f"| Detalle | Clasificación | FG | Rows | Total |\n|---|---|---|---:|---:|\n")
        for t in data['transaction_types']:
            f.write(f"| {t['detalle'][:60]} | {t['clasificacion_operativa'][:40]} | {t['financial_group'][:20]} | {t['cnt']:,} | ${t['total']:,.0f} |\n")

print(f"\n2. MANIFEST -> SNAPSHOT/MANIFEST_V6.json")
print(f"3. SHA256 DB: {db_sha256[:20]}...")
print(f"4. Global: {total_rows:,} rows, ${total_sum:,.0f}")
for mp, data in marketplaces.items():
    print(f"5. {mp}: {data['total_rows']:,} rows, ${data['sum_monto']:,.0f}")
print(f"\n6. Report copied to snapshot")
print(f"\nBASELINE_ESTABLE_V6 READY.")
