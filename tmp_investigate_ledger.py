"""Investigate Poscobro ML rows in ledger — find real id_transaccion pattern"""
import duckdb, os

TMP_DB = os.path.join(os.environ['TEMP'], "poscobro_v2.db")
con = duckdb.connect(TMP_DB, read_only=True)

print("=== Poscobro rows in ledger (ML + PAGO) ===")
rows = con.execute("""
    SELECT id_transaccion, fecha, monto, archivo_origen, detalle
    FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
    LIMIT 25
""").fetchall()
for r in rows:
    tid = str(r[0])[:60] if r[0] else "(NULL)"
    fecha = str(r[1])[:10] if r[1] else "NULL"
    monto = float(r[2]) if r[2] else 0
    archivo = str(r[3])[:40] if r[3] else "(NULL)"
    detalle = str(r[4])[:40] if r[4] else "(NULL)"
    print(f"  id={tid:60s} fecha={fecha:12s} monto=${monto:>10,.2f} archivo={archivo:40s} detalle={detalle}")

print(f"\nTotal ML PAGO: {con.execute('SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace=\"ML\" AND tipo_movimiento=\"PAGO\"').fetchone()[0]}")

print("\n=== Distinct archivo_origen for ML PAGO ===")
archivos = con.execute("""
    SELECT DISTINCT archivo_origen, COUNT(*) as cnt
    FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
    GROUP BY archivo_origen
    ORDER BY cnt DESC
""").fetchall()
for a in archivos:
    print(f"  {str(a[0])[:60]:60s} rows={a[1]}")

print("\n=== Sample id_transaccion patterns ===")
patterns = con.execute("""
    SELECT DISTINCT LEFT(id_transaccion, 20) as prefix, COUNT(*) as cnt
    FROM marketplace_ledger_v1
    WHERE marketplace='ML' AND tipo_movimiento='PAGO'
    GROUP BY prefix
    ORDER BY cnt DESC
    LIMIT 20
""").fetchall()
for p in patterns:
    print(f"  prefix={str(p[0]):20s} count={p[1]}")

con.close()
print("\nDone.")
