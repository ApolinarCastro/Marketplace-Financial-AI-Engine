import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, FINANCIAL_STRUCTURE

db = DatabaseV4.get()

print("=" * 80)
print("SURGICAL DB REVIEW — FULL DIAGNOSTIC")
print("=" * 80)

# 1. Overall state
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    total = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp]).iloc[0]['c']
    classified = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ?", [mp]).iloc[0]['c']
    noclas = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ? AND clasificacion_operativa = 'NO_CLASIFICADO'", [mp]).iloc[0]['c']
    corrections = db.query("SELECT COUNT(*) as c FROM marketplace_correcciones_v1 WHERE id_transaccion LIKE ?", [f'{mp[:2]}%']).iloc[0]['c']
    print(f"\n{mp}: Total={total} | Classified={classified} | NO_CLASIFICADO={noclas} | Corrections={corrections}")

# 2. Ripley deep dive
print(f"\n{'='*80}")
print("RIPLEY DEEP DIVE")
print(f"{'='*80}")

ripley_detail = db.query("""
    SELECT detalle, COUNT(*) as cnt, SUM(monto) as total,
           SUM(CASE WHEN monto > 0 THEN monto ELSE 0 END) as pago,
           SUM(CASE WHEN monto < 0 THEN monto ELSE 0 END) as cargo
    FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'
    GROUP BY detalle ORDER BY SUM(ABS(monto)) DESC
""")
print(f"\nRipley RAW concepts ({len(ripley_detail)}):")
for _, r in ripley_detail.iterrows():
    clasif = db.query("SELECT clasificacion_operativa FROM marketplace_ledger_clasificado_v1 WHERE marketplace = 'RIPLEY' AND detalle = ? LIMIT 1", [r['detalle']])
    cls = clasif.iloc[0]['clasificacion_operativa'] if len(clasif) > 0 else 'NO_CLASIFICADO'
    flag = " <<< WARN" if cls == 'NO_CLASIFICADO' else ""
    print(f"  {str(r['detalle'])[:55]:<55s} | cnt={r['cnt']:>5d} | ${r['total']:>12,.0f} | {cls}{flag}")

# 3. ML concepts with corrections
print(f"\n{'='*80}")
print("ML CONCEPTS — RAW vs CLASSIFIED vs CORRECTIONS")
print(f"{'='*80}")

ml_detail = db.query("""
    SELECT l.detalle as raw_detalle,
           COUNT(*) as cnt,
           SUM(l.monto) as total,
           MIN(c.clasificacion_operativa) as clasif
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'ML'
    GROUP BY l.detalle
    ORDER BY SUM(ABS(l.monto)) DESC
""")
print(f"\nML concepts ({len(ml_detail)}):")
for _, r in ml_detail.iterrows():
    flag = " <<< NO_CLAS" if r['clasif'] == 'NO_CLASIFICADO' else ""
    print(f"  {str(r['raw_detalle'])[:55]:<55s} | cnt={r['cnt']:>5d} | ${r['total']:>12,.0f} | {r['clasif']}{flag}")

# 4. NO_CLASIFICADO details
print(f"\n{'='*80}")
print("NO_CLASIFICADO — FULL LIST")
print(f"{'='*80}")
noclas = db.query("""
    SELECT l.marketplace, l.detalle, COUNT(*) as cnt, SUM(l.monto) as total
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE c.clasificacion_operativa = 'NO_CLASIFICADO'
    GROUP BY l.marketplace, l.detalle
    ORDER BY l.marketplace, SUM(ABS(l.monto)) DESC
""")
if len(noclas) > 0:
    for _, r in noclas.iterrows():
        print(f"  [{r['marketplace']}] {str(r['detalle'])[:60]:<60s} | cnt={r['cnt']:>5d} | ${r['total']:>12,.0f}")
else:
    print("  (none)")

# 5. ML Poscobro concepts — check if they're being properly classified
print(f"\n{'='*80}")
print("ML POSCOBRO — TRAZABILIDAD & CLASIFICACION")
print(f"{'='*80}")
poscobro = db.query("""
    SELECT l.detalle, COUNT(*) as cnt, SUM(l.monto) as total,
           COUNT(CASE WHEN l.id_orden IS NOT NULL AND l.id_orden != 'None' AND l.id_orden != '' THEN 1 END) as con_orden,
           MIN(c.clasificacion_operativa) as clasif
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'ML' AND l.archivo_origen LIKE '%Poscobro%'
    GROUP BY l.detalle
    ORDER BY SUM(ABS(l.monto)) DESC
""")
for _, r in poscobro.iterrows():
    sin_orden = r['cnt'] - r['con_orden']
    print(f"  {str(r['detalle'])[:55]:<55s} | cnt={r['cnt']:>4d} | ${r['total']:>10,.0f} | ordenes={r['con_orden']:>4d} | sin_orden={sin_orden:>4d} | {r['clasif']}")

# 6. Check corrections table
print(f"\n{'='*80}")
print("MANUAL CORRECTIONS TABLE")
print(f"{'='*80}")
corrs = db.query("SELECT * FROM marketplace_correcciones_v1 ORDER BY fecha_creacion DESC LIMIT 20")
if len(corrs) > 0:
    for _, r in corrs.iterrows():
        print(f"  {r.get('id_transaccion',''):<40s} | {str(r.get('detalle_original',''))[:40]:<40s} -> {str(r.get('detalle_corregido',''))[:40]:<40s} | {r.get('motivo','')}")
else:
    print("  (empty)")

# 7. Summary stats
print(f"\n{'='*80}")
print("SUMMARY STATS")
print(f"{'='*80}")
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    stats = db.query(f"""
        SELECT c.clasificacion_operativa, COUNT(*) as cnt, SUM(l.monto) as total
        FROM marketplace_ledger_v1 l
        JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
        WHERE l.marketplace = '{mp}'
        GROUP BY c.clasificacion_operativa
        ORDER BY SUM(ABS(l.monto)) DESC
    """)
    print(f"\n{mp} by classification:")
    for _, r in stats.iterrows():
        print(f"  {str(r['clasificacion_operativa'])[:30]:<30s} | cnt={r['cnt']:>6d} | ${r['total']:>12,.0f}")
