import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

print("="*70)
print("SURGICAL FINDINGS")
print("="*70)

# 1. Validate "A pagar" is the net payout (should match calculation)
print("\n--- RIPLEY: 'A pagar' validation ---")
net_check = db.query("""
    SELECT 
        SUM(CASE WHEN detalle = 'Importe del pedido' THEN monto ELSE 0 END) as ventas,
        SUM(CASE WHEN detalle = 'Envío' THEN monto ELSE 0 END) as envio,
        SUM(CASE WHEN detalle = 'Pedidos reembolsados' THEN monto ELSE 0 END) as devoluciones,
        SUM(CASE WHEN detalle = 'Comisiones sobre pedidos' THEN monto ELSE 0 END) as comisiones,
        SUM(CASE WHEN detalle = 'Gastos de envío pagados por el operador' THEN monto ELSE 0 END) as costo_envio,
        SUM(CASE WHEN detalle = 'Comisiones sobre pedidos reembolsados' THEN monto ELSE 0 END) as comisiones_reemb,
        SUM(CASE WHEN detalle = 'Descuento por costo logístico' THEN monto ELSE 0 END) as desc_log,
        SUM(CASE WHEN detalle = 'Envío reembolsado' THEN monto ELSE 0 END) as envio_reemb,
        SUM(CASE WHEN detalle = 'Gastos de envío reembolsados pagados por el operador' THEN monto ELSE 0 END) as gastos_envio_reemb,
        SUM(CASE WHEN detalle = 'Descuento por logística inversa' THEN monto ELSE 0 END) as desc_log_inv,
        SUM(CASE WHEN detalle = 'Descuento por cancelación' THEN monto ELSE 0 END) as desc_cancel,
        SUM(CASE WHEN detalle = 'Otros descuentos' THEN monto ELSE 0 END) as otros_desc,
        SUM(CASE WHEN detalle = 'A pagar' THEN monto ELSE 0 END) as a_pagar
    FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'
""").iloc[0]

print(f"  Ventas:                  ${net_check['ventas']:>12,.0f}")
print(f"  Envío:                   ${net_check['envio']:>12,.0f}")
print(f"  Devoluciones:            ${net_check['devoluciones']:>12,.0f}")
print(f"  Comisiones:              ${net_check['comisiones']:>12,.0f}")
print(f"  Costo envío:             ${net_check['costo_envio']:>12,.0f}")
print(f"  Comisiones reemb:        ${net_check['comisiones_reemb']:>12,.0f}")
print(f"  Desc. costo log:         ${net_check['desc_log']:>12,.0f}")
print(f"  Envío reembolsado:       ${net_check['envio_reemb']:>12,.0f}")
print(f"  Gastos envío reemb:      ${net_check['gastos_envio_reemb']:>12,.0f}")
print(f"  Desc. log inversa:       ${net_check['desc_log_inv']:>12,.0f}")
print(f"  Desc. cancel:            ${net_check['desc_cancel']:>12,.0f}")
print(f"  Otros desc:              ${net_check['otros_desc']:>12,.0f}")
net_calc = (
    net_check['ventas'] + net_check['envio'] + net_check['devoluciones'] +
    net_check['comisiones'] + net_check['costo_envio'] + net_check['comisiones_reemb'] +
    net_check['desc_log'] + net_check['envio_reemb'] + net_check['gastos_envio_reemb'] +
    net_check['desc_log_inv'] + net_check['desc_cancel'] + net_check['otros_desc']
)
print(f"\n  Calculated net:          ${net_calc:>12,.0f}")
print(f"  'A pagar':               ${net_check['a_pagar']:>12,.0f}")
print(f"  Match: {abs(net_calc - net_check['a_pagar']) < 1_000_000}")

# 2. Netting pairs
print("\n--- RIPLEY: Netting pairs check ---")
pairs = db.query("""
    SELECT 'Envío reembolsado vs Gastos envío reemb' as pair,
           SUM(CASE WHEN detalle = 'Envío reembolsado' THEN monto ELSE 0 END) as a,
           SUM(CASE WHEN detalle = 'Gastos de envío reembolsados pagados por el operador' THEN monto ELSE 0 END) as b
    FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'
    UNION ALL
    SELECT 'Envío vs Gastos de envío' as pair,
           SUM(CASE WHEN detalle = 'Envío' THEN monto ELSE 0 END) as a,
           SUM(CASE WHEN detalle = 'Gastos de envío pagados por el operador' THEN monto ELSE 0 END) as b
    FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY'
""")
for _, r in pairs.iterrows():
    net_sum = r['a'] + r['b']
    print(f"  {r['pair']:<40s} | A=${r['a']:>10,.0f} B=${r['b']:>10,.0f} NET=${net_sum:>10,.0f}")

# 3. Check per-order netting for Envío concepts
order_envio = db.query("""
    SELECT l.id_orden, 
           SUM(CASE WHEN l.detalle = 'Envío reembolsado' THEN l.monto ELSE 0 END) as envio_reemb,
           SUM(CASE WHEN l.detalle = 'Gastos de envío reembolsados pagados por el operador' THEN l.monto ELSE 0 END) as gastos_reemb
    FROM marketplace_ledger_v1 l
    WHERE l.marketplace = 'RIPLEY'
    GROUP BY l.id_orden
    HAVING envio_reemb != 0 OR gastos_reemb != 0
    ORDER BY ABS(envio_reemb + gastos_reemb) DESC
    LIMIT 5
""")
print("\n--- RIPLEY: Per-order envio netting (top 5 mismatches) ---")
for _, r in order_envio.iterrows():
    net = r['envio_reemb'] + r['gastos_reemb']
    print(f"  Order {r['id_orden']:>15s} | envío_reemb=${r['envio_reemb']:>8,.0f} | gastos_reemb=${r['gastos_reemb']:>8,.0f} | NET=${net:>8,.0f}")

# 4. ML "Cargo" concept
print("\n--- ML: 'Cargo' concept deep dive ---")
cargo = db.query("""
    SELECT id_transaccion, id_orden, detalle, monto, fecha, archivo_origen, folio_xml
    FROM marketplace_ledger_v1 
    WHERE marketplace = 'ML' AND detalle = 'Cargo'
    ORDER BY ABS(monto) DESC
    LIMIT 10
""")
if len(cargo) > 0:
    for _, r in cargo.iterrows():
        print(f"  ID={r['id_transaccion']:<40s} | orden={str(r['id_orden'])[:15]:<15s} | ${r['monto']:>8,.0f} | fecha={str(r['fecha'])[:10]} | archivo={str(r['archivo_origen'])[:30]}")
    totals = db.query("SELECT SUM(monto) as total, COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace = 'ML' AND detalle = 'Cargo'").iloc[0]
    print(f"  TOTAL: cnt={totals['cnt']} | ${totals['total']:,.0f}")

# 5. ML Poscobro concepts — check historic filter
print("\n--- ML POSCOBRO: Checking historic classification ---")
pos_historic = db.query("""
    SELECT COUNT(*) as cnt, 
           SUM(CASE WHEN fecha < '2026-01-01' THEN 1 ELSE 0 END) as pre_2026,
           SUM(CASE WHEN fecha >= '2026-01-01' THEN 1 ELSE 0 END) as post_2026,
           SUM(monto) as total
    FROM marketplace_ledger_v1 
    WHERE marketplace = 'ML' AND archivo_origen LIKE '%Poscobro%'
""").iloc[0]
print(f"  Total Poscobro: {pos_historic['cnt']} rows | ${pos_historic['total']:,.0f}")
print(f"  Pre-2026: {pos_historic['pre_2026']} | Post-2026: {pos_historic['post_2026']}")

# Show Poscobro concepts with dates
pos_concepts = db.query("""
    SELECT l.detalle, COUNT(*) as cnt, SUM(l.monto) as total,
           MIN(l.fecha) as first_date, MAX(l.fecha) as last_date,
           MIN(c.clasificacion_operativa) as clasif
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace = 'ML' AND l.archivo_origen LIKE '%Poscobro%'
    GROUP BY l.detalle
    ORDER BY SUM(ABS(l.monto)) DESC
""")
for _, r in pos_concepts.iterrows():
    print(f"  {str(r['detalle'])[:40]:<40s} | cnt={r['cnt']:>4d} | ${r['total']:>10,.0f} | dates={str(r['first_date'])[:10]}->{str(r['last_date'])[:10]} | {r['clasif']}")

# 6. Marketplaces with NO_CLASIFICADO after reclassification
print("\n--- FINAL CLASSIFICATION QUALITY ---")
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    noclas = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ? AND clasificacion_operativa = 'NO_CLASIFICADO'", [mp]).iloc[0]['c']
    total = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ?", [mp]).iloc[0]['c']
    pct = (noclas / total * 100) if total > 0 else 0
    print(f"  {mp}: {noclas}/{total} NO_CLASIFICADO ({pct:.2f}%)")
