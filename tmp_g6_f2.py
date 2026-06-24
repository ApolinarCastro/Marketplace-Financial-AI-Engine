import duckdb, sys
db = duckdb.connect('data/db/meli_financial_v4.db')

MP = 'ML'
p1 = '2025-04-01'
p2 = '2025-04-30'
p1b = '2025-10-01'
p2b = '2025-10-31'

print("=" * 120)
print("FASE 1: ALL ML CLASIFICACION_OPERATIVA VALUES (unique)")
print("=" * 120)
r = db.execute("""
    SELECT DISTINCT clasificacion_operativa
    FROM marketplace_ledger_v1
    WHERE marketplace = ?
    ORDER BY clasificacion_operativa
""", [MP]).fetchall()
for row in r:
    print("  " + row[0])

print("\n" + "=" * 120)
print("FASE 2: RECORDS vs EVENTS — ML APRIL 2025")
print("=" * 120)

# Step 1: Total rows and sum by financial_group for April 2025
print("\n--- 2A: Total by financial_group (April 2025) ---")
r = db.execute("""
    SELECT financial_group, COUNT(*) as cnt, ROUND(SUM(monto), 2) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
    GROUP BY financial_group
    ORDER BY total DESC
""", [MP, p1, p2]).fetchall()
for row in r:
    print("  %-25s cnt=%5d  $%s" % (row[0], row[1], f"{row[2]:,.2f}"))

# Step 2: Find concepts involved in double-count pairs (Talla+BPP, Arre+Posc)
print("\n--- 2B: Concepts with paired orders (same id_orden, different clasificacion_operativa) ---")
r = db.execute("""
    SELECT a.clasificacion_operativa as concept_a, 
           b.clasificacion_operativa as concept_b,
           COUNT(DISTINCT a.id_orden) as paired_orders,
           ROUND(SUM(DISTINCT a.monto), 2) as amount_per_order
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
    GROUP BY a.clasificacion_operativa, b.clasificacion_operativa
    HAVING COUNT(DISTINCT a.id_orden) >= 3
    ORDER BY paired_orders DESC
""", [MP, p1, p2, MP, p1, p2]).fetchall()
for row in r:
    print("  %-40s + %-40s: %d orders, $%s each" % (row[0], row[1], row[2], f"{row[3]:,.2f}"))

# Step 3: Count records vs unique events for AJUSTES only (where double-count lives)
print("\n--- 2C: AJUSTES — Records vs Unique Economic Events (April 2025) ---")
# A 'record' is each row. An 'economic event' is one per unique id_orden + financial_group + detalle
# But paired events have SAME id_orden, DIFFERENT clasificacion_operativa
# So a true economic event is: root event = one per unique id_orden

# Total rows in ajustes
r = db.execute("""
    SELECT COUNT(*) as total_records,
           ROUND(SUM(monto), 2) as total_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
""", [MP, p1, p2]).fetchall()
print("  Total records in ajustes:       %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))

# Unique id_orden (economic events)
r = db.execute("""
    SELECT COUNT(DISTINCT id_orden) as unique_orders,
           ROUND(SUM(monto), 2) as total_if_deduplicated
    FROM (
        SELECT id_orden, monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden, monto
    )
""", [MP, p1, p2]).fetchall()
print("  Unique id_orden:                 %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))

# Detect PAIRED orders: same id_orden appears with >=2 different concepts
print("\n--- 2D: PAIRED ORDERS DETECTION (April 2025) ---")
r = db.execute("""
    SELECT COUNT(*) as paired_orders,
           ROUND(SUM(max_monto), 2) as root_amount,
           ROUND(SUM(total_monto - max_monto), 2) as paired_amount
    FROM (
        SELECT id_orden, 
               COUNT(*) as concept_count,
               COUNT(DISTINCT clasificacion_operativa) as distinct_concepts,
               MAX(monto) as max_monto,
               SUM(monto) as total_monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden
        HAVING COUNT(DISTINCT clasificacion_operativa) >= 2
    )
""", [MP, p1, p2]).fetchall()
print("  Orders with 2+ concepts:          %5d" % r[0][0])
print("  Root event amount (MAX monto):    $%s" % f"{r[0][1]:,.2f}")
print("  Paired amount (total - root):     $%s" % f"{r[0][2]:,.2f}")
print("  Inflation ratio:                   %.2f%%" % (r[0][2]/(r[0][1]+r[0][2])*100 if (r[0][1]+r[0][2]) > 0 else 0))

# Step 4: Count orders where the SAME amount appears under 2+ concepts (exact match)
print("\n--- 2E: EXACT-AMOUNT PAIRS (same id_orden, same monto, different concept) ---")
r = db.execute("""
    SELECT COUNT(*) as exact_pairs,
           ROUND(SUM(a.monto), 2) as total_pair_amount
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.monto = b.monto AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
""", [MP, p1, p2, MP, p1, p2]).fetchall()
print("  Exact-amount paired entries:      %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))

# Unique orders with exact pairs
r = db.execute("""
    SELECT COUNT(DISTINCT a.id_orden) as unique_orders
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.monto = b.monto AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
""", [MP, p1, p2, MP, p1, p2]).fetchall()
print("  Unique orders with exact pairs:   %5d" % r[0][0])

print("\n" + "=" * 120)
print("FASE 3: RECORDS vs EVENTS — ML OCTOBER 2025")
print("=" * 120)

# Same analysis for October 2025
print("\n--- 3A: AJUSTES — Records vs Unique Economic Events (October 2025) ---")
r = db.execute("""
    SELECT COUNT(*) as total_records,
           ROUND(SUM(monto), 2) as total_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
""", [MP, p1b, p2b]).fetchall()
print("  Total records in ajustes:       %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))

print("\n--- 3B: PAIRED ORDERS DETECTION (October 2025) ---")
r = db.execute("""
    SELECT COUNT(*) as paired_orders,
           ROUND(SUM(max_monto), 2) as root_amount,
           ROUND(SUM(total_monto - max_monto), 2) as paired_amount
    FROM (
        SELECT id_orden, 
               COUNT(*) as concept_count,
               COUNT(DISTINCT clasificacion_operativa) as distinct_concepts,
               MAX(monto) as max_monto,
               SUM(monto) as total_monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden
        HAVING COUNT(DISTINCT clasificacion_operativa) >= 2
    )
""", [MP, p1b, p2b]).fetchall()
print("  Orders with 2+ concepts:         %5d" % r[0][0])
print("  Root event amount (MAX monto):   $%s" % f"{r[0][1]:,.2f}")
print("  Paired amount (total - root):    $%s" % f"{r[0][2]:,.2f}")

print("\n--- 3C: EXACT-AMOUNT PAIRS (October 2025) ---")
r = db.execute("""
    SELECT COUNT(*) as exact_pairs,
           ROUND(SUM(a.monto), 2) as total_pair_amount
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.monto = b.monto AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
""", [MP, p1b, p2b, MP, p1b, p2b]).fetchall()
print("  Exact-amount paired entries:     %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))

r = db.execute("""
    SELECT COUNT(DISTINCT a.id_orden) as unique_orders
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.monto = b.monto AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
""", [MP, p1b, p2b, MP, p1b, p2b]).fetchall()
print("  Unique orders with exact pairs:  %5d" % r[0][0])

print("\n" + "=" * 120)
print("FASE 4: DETAILED CONCEPT ANALYSIS (8 specific concepts)")
print("=" * 120)

# The 8 concepts to analyze
concepts = [
    'different_color_or_size_fashion',
    'bigger_than_expected',
    'smaller_than_expected',
    'not_match_size_guide',
    'undelivered_repentant_buyer',
    'bpp_refunded',
    'reconciled',
    'compensated'
]

# First, find how these map to actual clasificacion_operativa values
print("\n--- 4A: Mapping concepts to actual clasificacion_operativa ---")
for c in concepts:
    r = db.execute("""
        SELECT DISTINCT clasificacion_operativa, detalle
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND LOWER(clasificacion_operativa) LIKE ?
        LIMIT 5
    """, [MP, '%' + c.lower().replace('_', '%') + '%']).fetchall()
    if r:
        for row in r:
            print("  %-45s -> %s" % (c, row[0]))
    else:
        # Try broader match
        r2 = db.execute("""
            SELECT DISTINCT clasificacion_operativa
            FROM marketplace_ledger_v1
            WHERE marketplace = ? AND (
                LOWER(clasificacion_operativa) LIKE '%' || ? || '%'
                OR LOWER(detalle) LIKE '%' || ? || '%'
            )
            LIMIT 5
        """, [MP, c.lower().replace('_', ' '), c.lower().replace('_', ' ')]).fetchall()
        if r2:
            for row in r2:
                print("  %-45s -> %s (from detalle match)" % (c, row[0]))
        else:
            print("  %-45s -> NOT FOUND in DB" % c)

# Now find the ACTUAL clasificacion_operativa values that exist
print("\n--- 4B: All AJUSTES concepts in ML (with counts and totals) ---")
r = db.execute("""
    SELECT clasificacion_operativa, 
           COUNT(*) as cnt,
           ROUND(SUM(monto), 2) as total,
           ROUND(AVG(monto), 2) as avg_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
    GROUP BY clasificacion_operativa
    ORDER BY total DESC
""", [MP, p1, p2]).fetchall()
for row in r:
    print("  %-55s cnt=%4d  total=$%s  avg=$%s" % (row[0][:55], row[1], f"{row[2]:>,.2f}", f"{row[3]:>,.2f}"))

# For each concept, count how many orders also appear in ANOTHER concept
print("\n--- 4C: OVERLAP ANALYSIS — Each concept's orders shared with other concepts ---")
r = db.execute("""
    SELECT a.clasificacion_operativa,
           COUNT(DISTINCT a.id_orden) as total_orders_in_concept,
           COUNT(DISTINCT CASE WHEN b.id_orden IS NOT NULL THEN a.id_orden END) as shared_with_other_concept,
           ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.id_orden IS NOT NULL THEN a.id_orden END) / 
                 NULLIF(COUNT(DISTINCT a.id_orden), 0), 1) as overlap_pct
    FROM marketplace_ledger_v1 a
    LEFT JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
        AND a.clasificacion_operativa <> b.clasificacion_operativa
        AND b.financial_group = 'ajustes'
        AND b.marketplace = a.marketplace AND b.fecha BETWEEN ? AND ?
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ? AND a.financial_group = 'ajustes'
    GROUP BY a.clasificacion_operativa
    ORDER BY overlap_pct DESC
""", [p1, p2, MP, p1, p2]).fetchall()
for row in r:
    print("  %-55s total=%4d shared=%4d (%.1f%%)" % (row[0][:55], row[1], row[2], row[3]))

print("\n" + "=" * 120)
print("FASE 5: ECONOMIC EVENT AGGREGATION TEST")
print("=" * 120)

# Test: what if we GROUP BY id_orden and take MAX(monto) per order?
print("\n--- 5A: Resultado Neto if computed by ECONOMIC EVENT (1 per id_orden) ---")
# This simulates what would happen if the closing deduplicated by order
r = db.execute("""
    WITH by_order AS (
        SELECT id_orden, 
               MAX(monto) as event_monto,
               COUNT(*) as records_for_this_order
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden
    )
    SELECT COUNT(*) as event_count,
           ROUND(SUM(records_for_this_order), 0) as total_records,
           ROUND(SUM(event_monto), 2) as economic_sum
    FROM by_order
""", [MP, p1, p2]).fetchall()
total_records = db.execute("""
    SELECT COUNT(*), ROUND(SUM(monto), 2)
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
""", [MP, p1, p2]).fetchall()

print("  Records (current method):          %5d  $%s" % (total_records[0][0], f"{total_records[0][1]:,.2f}"))
print("  Economic Events (by id_orden):     %5d  $%s" % (r[0][0], f"{r[0][1]:,.2f}"))
print("  Delta:                              %5d  $%s" % (total_records[0][0] - r[0][0], f"{total_records[0][1] - r[0][1]:,.2f}"))
print("  Record Inflation:                  %.2f%%" % ((total_records[0][0] / r[0][0] - 1) * 100 if r[0][0] > 0 else 0))

print("\n--- 5B: FULL RESULTADO NETO — RECORDS vs EVENTS (April 2025) ---")
# Current method: SUM of all records
current = db.execute("""
    SELECT ROUND(SUM(monto), 2)
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
""", [MP, p1, p2]).fetchall()

# Events method: for ajustes, take MAX per order (root event); for others, keep as-is
events = db.execute("""
    WITH ajustes_dedup AS (
        SELECT id_orden, MAX(monto) as event_monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden
    ),
    non_ajustes AS (
        SELECT monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND (financial_group IS NULL OR financial_group <> 'ajustes')
    )
    SELECT ROUND(COALESCE((SELECT SUM(event_monto) FROM ajustes_dedup), 0) + 
                 COALESCE((SELECT SUM(monto) FROM non_ajustes), 0), 2) as economic_resultado_neto
""", [MP, p1, p2, MP, p1, p2]).fetchall()

print("  Current Resultado Neto (ALL records):  $%s" % f"{current[0][0]:,.2f}")
print("  Economic Resultado Neto (events):      $%s" % f"{events[0][0]:,.2f}")
print("  Delta:                                  $%s" % f"{current[0][0] - events[0][0]:,.2f}")
print("  Inflation:                              %.2f%%" % ((current[0][0] / events[0][0] - 1) * 100 if events[0][0] != 0 else 0))

print("\n--- 5C: FULL RESULTADO NETO — RECORDS vs EVENTS (October 2025) ---")
current2 = db.execute("""
    SELECT ROUND(SUM(monto), 2)
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
""", [MP, p1b, p2b]).fetchall()

events2 = db.execute("""
    WITH ajustes_dedup AS (
        SELECT id_orden, MAX(monto) as event_monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND financial_group = 'ajustes'
        GROUP BY id_orden
    ),
    non_ajustes AS (
        SELECT monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ? AND (financial_group IS NULL OR financial_group <> 'ajustes')
    )
    SELECT ROUND(COALESCE((SELECT SUM(event_monto) FROM ajustes_dedup), 0) + 
                 COALESCE((SELECT SUM(monto) FROM non_ajustes), 0), 2) as economic_resultado_neto
""", [MP, p1b, p2b, MP, p1b, p2b]).fetchall()

print("  Current Resultado Neto (ALL records):  $%s" % f"{current2[0][0]:,.2f}")
print("  Economic Resultado Neto (events):      $%s" % f"{events2[0][0]:,.2f}")
print("  Delta:                                  $%s" % f"{current2[0][0] - events2[0][0]:,.2f}")
print("  Inflation:                              %.2f%%" % ((current2[0][0] / events2[0][0] - 1) * 100 if events2[0][0] != 0 else 0))

print("\n--- 5D: AFFECTED ORDERS — ALL TIME ---")
# Count of ALL paired orders across ALL time periods for ML
r = db.execute("""
    SELECT COUNT(*) as paired_orders,
           ROUND(SUM(max_monto), 2) as root_amount,
           ROUND(SUM(total_monto - max_monto), 2) as excess_amount
    FROM (
        SELECT id_orden, 
               COUNT(*) as concept_count,
               COUNT(DISTINCT clasificacion_operativa) as distinct_concepts,
               MAX(monto) as max_monto,
               SUM(monto) as total_monto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND financial_group = 'ajustes'
        GROUP BY id_orden
        HAVING COUNT(DISTINCT clasificacion_operativa) >= 2
    )
""", [MP]).fetchall()
print("  Total paired orders (all time):       %5d" % r[0][0])
print("  Root amount:                           $%s" % f"{r[0][1]:,.2f}")
print("  Excess (inflation) amount:             $%s" % f"{r[0][2]:,.2f}")
print("  %% of total ajustes that is inflation:  %.2f%%" % (
    r[0][2] / (db.execute("SELECT ROUND(SUM(monto),2) FROM marketplace_ledger_v1 WHERE marketplace=? AND financial_group='ajustes'", [MP]).fetchall()[0][0]) * 100
    if db.execute("SELECT ROUND(SUM(monto),2) FROM marketplace_ledger_v1 WHERE marketplace=? AND financial_group='ajustes'", [MP]).fetchall()[0][0] != 0 else 0
))

db.close()
print("\nDone.")
