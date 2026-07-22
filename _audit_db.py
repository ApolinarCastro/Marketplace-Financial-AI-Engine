# -*- coding: utf-8 -*-
import duckdb, os

DB = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db'
con = duckdb.connect(DB, read_only=True)

print("=== TABLES IN DB ===")
tables = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
for t in tables:
    col = con.execute(f"PRAGMA table_info('{t[0]}')").fetchall()
    cnt = con.execute(f"SELECT COUNT(*) FROM \"{t[0]}\"").fetchone()[0]
    print(f"  {t[0]}: {cnt} rows, {len(col)} cols")
    for c in col:
        print(f"    {c[1]} ({c[2]})")

print("\n=== LEDGER BY MARKETPLACE ===")
mps = con.execute("SELECT marketplace, COUNT(*), SUM(total_amount) FROM marketplace_ledger_v1 GROUP BY marketplace ORDER BY COUNT(*) DESC").fetchall()
for r in mps:
    print(f"  {r[0]}: {r[1]} rows, ${r[2]:,.2f}" if r[2] else f"  {r[0]}: {r[1]} rows, NULL")

print("\n=== LEDGER YEARS ===")
yrs = con.execute("SELECT DISTINCT EXTRACT(YEAR FROM fecha) as year FROM marketplace_ledger_v1 ORDER BY year").fetchall()
print(f"  Years: {[int(r[0]) for r in yrs]}")

print("\n=== FOLIO_XML COVERAGE ===")
dte = con.execute("SELECT COUNT(DISTINCT folio_xml) FROM marketplace_ledger_v1 WHERE folio_xml IS NOT NULL AND folio_xml != ''").fetchone()[0]
total = con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0]
print(f"  Rows with folio_xml: {dte}/{total} ({100*dte/total:.1f}%)")

print("\n=== DTE TRUTH TABLE ===")
dte_t = con.execute("SELECT COUNT(*), COUNT(DISTINCT folio) FROM dte_truth_v1").fetchone()
print(f"  dte_truth_v1: {dte_t[0]} rows, {dte_t[1]} unique folios")

print("\n=== CIERRE PERIODS ===")
per = con.execute("SELECT periodo_cierre, COUNT(*) as c FROM marketplace_cierre_financiero_v1 GROUP BY periodo_cierre ORDER BY c DESC LIMIT 20").fetchall()
print(f"  Total periods: {len(per)}")
for p in per:
    print(f"  {p[0]}: {p[1]} rows")

print("\n=== INDEXES ===")
idx = con.execute("SELECT * FROM duckdb_indexes() WHERE database_name='meli_financial_v4'").fetchall()
print(f"  Indexes: {len(idx)}")
for i in idx:
    print(f"  {i}")

print("\n=== DB SIZE ===")
size_bytes = os.path.getsize(DB)
print(f"  Size: {size_bytes/(1024*1024):.1f} MB")

con.close()
