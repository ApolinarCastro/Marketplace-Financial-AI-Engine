import duckdb, json
con = duckdb.connect('data/db/meli_financial_v4.db')

# 1. What is "A pagar"?
print("=== 1. 'A pagar' BASICS ===")
apagar = con.execute("""
    SELECT 
        COUNT(*) as total_rows,
        SUM(monto) as total_amount,
        MIN(monto) as min_amount,
        MAX(monto) as max_amount,
        AVG(monto) as avg_amount,
        COUNT(DISTINCT id_orden) as distinct_orders,
        MIN(fecha) as min_date,
        MAX(fecha) as max_date
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
""").fetchdf().iloc[0]
print(f"Rows: {apagar['total_rows']:,}")
print(f"Total: ${apagar['total_amount']:,.2f}")
print(f"Min: ${apagar['min_amount']:,.2f}, Max: ${apagar['max_amount']:,.2f}, Avg: ${apagar['avg_amount']:,.2f}")
print(f"Orders: {apagar['distinct_orders']:,}")
print(f"Date range: {apagar['min_date']} to {apagar['max_date']}")

# 2. Monthly breakdown
print("\n=== 2. MONTHLY BREAKDOWN ===")
monthly = con.execute("""
    SELECT strftime(fecha, '%Y-%m') as month,
        COUNT(*) as rows,
        SUM(monto) as total,
        COUNT(DISTINCT id_orden) as orders
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
    GROUP BY month
    ORDER BY month
""").fetchdf()
for _, r in monthly.iterrows():
    print(f"  {r['month']}: rows={r['rows']:>5d} ${r['total']:>12,.2f} orders={r['orders']:>5d}")
print(f"  TOTAL: {monthly['rows'].sum():>5d} ${monthly['total'].sum():>12,.2f}")

# 3. Compare against Importe del pedido - Comisiones - Costos - Reembolsos
print("\n=== 3. FORMULA CHECK: Apagar vs (Importe - Comisiones - Costos - Reembolsos) ===")
# Check if there's a 1:1 id_orden relationship
apagar_orders = con.execute("""
    SELECT id_orden, SUM(monto) as apagar_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
    GROUP BY id_orden
""").fetchdf()

importe_orders = con.execute("""
    SELECT id_orden, SUM(monto) as importe_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'Importe del pedido'
    GROUP BY id_orden
""").fetchdf()

comisiones_orders = con.execute("""
    SELECT id_orden, SUM(monto) as comision_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle IN ('Comisiones sobre pedidos', 'Comisiones sobre pedidos reembolsados')
    GROUP BY id_orden
""").fetchdf()

costos_orders = con.execute("""
    SELECT id_orden, SUM(monto) as costo_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle IN ('Envio', 'Envio reembolsado', 'Gastos de envio pagados por el operador', 
        'Gastos de envio reembolsados pagados por el operador', 'Descuento por costo logistico', 
        'Descuento por logistica inversa')
    GROUP BY id_orden
""").fetchdf()

reembolso_orders = con.execute("""
    SELECT id_orden, SUM(monto) as reembolso_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'Pedidos reembolsados'
    GROUP BY id_orden
""").fetchdf()

# Merge
merged = apagar_orders.merge(importe_orders, on='id_orden', how='left')
merged = merged.merge(comisiones_orders, on='id_orden', how='left')
merged = merged.merge(costos_orders, on='id_orden', how='left')
merged = merged.merge(reembolso_orders, on='id_orden', how='left')
merged = merged.fillna(0)
merged['expected_neto'] = merged['importe_amount'] + merged['comision_amount'] + merged['costo_amount'] + merged['reembolso_amount']
merged['delta'] = merged['apagar_amount'] - merged['expected_neto']
merged['match_pct'] = (merged['delta'].abs() / merged['apagar_amount'].abs() * 100).clip(0, 100)

exact_match = (merged['delta'].abs() < 0.01).sum()
total_orders = len(merged)
near_match = (merged['delta'].abs() < 0.01 * merged['apagar_amount'].abs()).sum()

print(f"Orders with 'A pagar': {total_orders}")
print(f"Exact matches (delta < $0.01): {exact_match} ({exact_match/total_orders*100:.1f}%)")
print(f"Near matches (delta < 1% of amount): {near_match} ({near_match/total_orders*100:.1f}%)")
print(f"Total delta: ${merged['delta'].sum():,.2f}")

# Distribution of deltas
print("\nDelta distribution:")
for pct in [(0,0.01), (0.01,1), (1,5), (5,10), (10,25), (25,50), (50,100)]:
    count = ((merged['delta'].abs() >= pct[0]/100*merged['apagar_amount'].abs()) & 
             (merged['delta'].abs() < pct[1]/100*merged['apagar_amount'].abs())).sum()
    if count > 0:
        print(f"  {pct[0]:.0f}-{pct[1]:.0f}% delta: {count} orders")

# 4. Show 10 real examples
print("\n\n=== 4. TEN REAL EXAMPLES ===")
examples = con.execute("""
    SELECT id_orden, fecha, monto
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
    ORDER BY monto DESC
    LIMIT 10
""").fetchdf()

for _, r in examples.iterrows():
    oid = r['id_orden']
    imp = importe_orders.loc[importe_orders['id_orden'] == oid, 'importe_amount'].values
    com = comisiones_orders.loc[comisiones_orders['id_orden'] == oid, 'comision_amount'].values
    cos = costos_orders.loc[costos_orders['id_orden'] == oid, 'costo_amount'].values
    rem = reembolso_orders.loc[reembolso_orders['id_orden'] == oid, 'reembolso_amount'].values
    imp = imp[0] if len(imp) > 0 else 0
    com = com[0] if len(com) > 0 else 0
    cos = cos[0] if len(cos) > 0 else 0
    rem = rem[0] if len(rem) > 0 else 0
    expected = imp + com + cos + rem
    apagar_amt = r['monto']
    d = apagar_amt - expected
    pct = abs(d) / abs(apagar_amt) * 100 if apagar_amt != 0 else 0
    print(f"\n  Order: {oid}")
    print(f"    A pagar:           ${apagar_amt:>10,.2f}")
    print(f"    Importe pedido:    ${imp:>10,.2f}")
    print(f"    Comisiones:        ${com:>10,.2f}")
    print(f"    Costos logisticos: ${cos:>10,.2f}")
    print(f"    Reembolsos:        ${rem:>10,.2f}")
    print(f"    Expected:          ${expected:>10,.2f}")
    print(f"    Delta:             ${d:>10,.2f} ({pct:.1f}%)")
    print(f"    Date: {r['fecha']}")

# 5. Check uniqueness
print("\n\n=== 5. ID_TRANSACCION ANALYSIS ===")
id_check = con.execute("""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT id_transaccion) as distinct_tx,
        COUNT(DISTINCT id_orden) as distinct_orders
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
""").fetchdf().iloc[0]
print(f"A pagar rows: {id_check['total_rows']:,}")
print(f"Distinct id_transaccion: {id_check['distinct_tx']:,}")
print(f"Distinct id_orden: {id_check['distinct_orders']:,}")

# 6. Does same id_orden also have Importe del pedido?
overlap = con.execute("""
    SELECT 
        COUNT(DISTINCT a.id_orden) as both_have,
        COUNT(DISTINCT i.id_orden) as importe_has
    FROM marketplace_ledger_v1 a
    FULL JOIN marketplace_ledger_v1 i ON a.id_orden = i.id_orden AND i.detalle = 'Importe del pedido'
    WHERE a.marketplace = 'RIPLEY' AND a.detalle = 'A pagar'
""").fetchdf().iloc[0]
print(f"\nOrders with BOTH A pagar AND Importe del pedido: {overlap['both_have']:,}")
print(f"Orders with Importe del pedido (any): {overlap['importe_has']:,}")

# 7. Id_orden that have A pagar but NO importe
missing_importe = con.execute("""
    SELECT a.id_orden, a.monto, a.fecha
    FROM marketplace_ledger_v1 a
    LEFT JOIN marketplace_ledger_v1 i ON a.id_orden = i.id_orden AND i.detalle = 'Importe del pedido'
    WHERE a.marketplace = 'RIPLEY' AND a.detalle = 'A pagar'
        AND i.id_orden IS NULL
    ORDER BY a.monto DESC
    LIMIT 10
""").fetchdf()
print(f"\nA pagar orders WITHOUT Importe del pedido: {len(missing_importe)}")
if len(missing_importe) > 0:
    for _, r in missing_importe.iterrows():
        print(f"  {r['id_orden']}: ${r['monto']:,.2f} ({r['fecha']})")

# 8. By month: A pagar vs total ledger
print("\n\n=== 6. MONTHLY: A pagar vs REST OF LEDGER ===")
by_month = con.execute("""
    SELECT 
        strftime(fecha, '%Y-%m') as month,
        SUM(CASE WHEN detalle = 'A pagar' THEN monto ELSE 0 END) as apagar,
        SUM(CASE WHEN detalle != 'A pagar' THEN monto ELSE 0 END) as rest,
        SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY month
    ORDER BY month
""").fetchdf()
for _, r in by_month.iterrows():
    apagar_pct = r['apagar'] / r['total'] * 100 if r['total'] else 0
    print(f"  {r['month']}: apagar=${r['apagar']:>12,.2f} rest=${r['rest']:>12,.2f} total=${r['total']:>12,.2f} apagar%={apagar_pct:.1f}%")

# 9. Sign distribution
print("\n\n=== 7. SIGN ANALYSIS ===")
signs = con.execute("""
    SELECT 
        CASE WHEN monto > 0 THEN 'POSITIVE' WHEN monto < 0 THEN 'NEGATIVE' ELSE 'ZERO' END as sign,
        COUNT(*) as rows,
        SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
    GROUP BY sign
""").fetchdf()
for _, r in signs.iterrows():
    print(f"  {r['sign']:8s}: rows={r['rows']:>6d} total=${r['total']:>14,.2f}")

con.close()
