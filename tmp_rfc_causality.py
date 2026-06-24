import duckdb, sys, os
from datetime import datetime

db = duckdb.connect('data/db/meli_financial_v4.db')
fmt = lambda x: f"{x:>,.2f}"

MP = 'ML'
p_ini = '2025-04-01'
p_fin = '2025-04-30'

# 4 concepts under analysis
CONCEPTS = [
    'Ajuste por Arrepentimiento',
    'Ajuste por Compra Protegida (BPP)',
    'Ajuste por Talla/Garantía',
    'Ajuste Poscobro Conciliado'
]

# ============================================================
# FASE 1 — TRAZABILIDAD CAUSAL
# ============================================================
print("=" * 140)
print("FASE 1 — TRAZABILIDAD CAUSAL: RECONSTRUCCION DEL CICLO DE VIDA POR ORDER_ID")
print("=" * 140)

# 1A: Ordenes con UN SOLO concepto (standalone) - estas son eventos economicos puros
print("\n--- 1A: ORDENES STANDALONE (1 sola entrada en ajustes) ---")
standalone = db.execute("""
    SELECT clasificacion_operativa, 
           COUNT(DISTINCT id_orden) as orders,
           COUNT(*) as records,
           ROUND(SUM(monto), 2) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
      AND financial_group = 'ajustes'
      AND id_orden IN (
          SELECT id_orden FROM marketplace_ledger_v1
          WHERE marketplace = ? AND fecha BETWEEN ? AND ?
            AND financial_group = 'ajustes'
          GROUP BY id_orden
          HAVING COUNT(DISTINCT clasificacion_operativa) = 1
      )
      AND clasificacion_operativa IN ('Ajuste por Arrepentimiento', 'Ajuste por Compra Protegida (BPP)',
                                       'Ajuste por Talla/Garantía', 'Ajuste Poscobro Conciliado')
    GROUP BY clasificacion_operativa
    ORDER BY total DESC
""", [MP, p_ini, p_fin, MP, p_ini, p_fin]).fetchall()
for r in standalone:
    print(f"  {r[0]:45s} orders={r[1]:5d} records={r[2]:5d} total=${fmt(r[3])}")

# 1B: Ordenes con 2+ conceptos - el grafo de causalidad
print("\n--- 1B: ORDENES CON 2+ CONCEPTOS (pares causales) ---")
# Count how many orders have each concept AS THE FIRST (chronological)
# and AS PARTNER
# We need to build a matrix: for each concept, how many orders have it as:
# - standalone (only concept)
# - first concept (paired, chronological first)
# - second concept (paired, chronological second)

# For ordenes con pares, find first and last event by fecha
pairs_detail = db.execute("""
    WITH paired_orders AS (
        SELECT id_orden
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND clasificacion_operativa IN ('Ajuste por Arrepentimiento', 'Ajuste por Compra Protegida (BPP)',
                                           'Ajuste por Talla/Garantía', 'Ajuste Poscobro Conciliado')
        GROUP BY id_orden
        HAVING COUNT(DISTINCT clasificacion_operativa) >= 2
    ),
    ordered_entries AS (
        SELECT id_orden, clasificacion_operativa, monto, fecha,
               ROW_NUMBER() OVER (PARTITION BY id_orden ORDER BY fecha, id_transaccion) as seq_first,
               ROW_NUMBER() OVER (PARTITION BY id_orden ORDER BY fecha DESC, id_transaccion DESC) as seq_last
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND id_orden IN (SELECT id_orden FROM paired_orders)
    )
    SELECT 
        COALESCE(f.clasificacion_operativa, 'UNKNOWN') as first_concept,
        COALESCE(l.clasificacion_operativa, 'UNKNOWN') as last_concept,
        COUNT(DISTINCT f.id_orden) as orders
    FROM (SELECT * FROM ordered_entries WHERE seq_first = 1) f
    LEFT JOIN (SELECT * FROM ordered_entries WHERE seq_last = 1) l ON f.id_orden = l.id_orden
    GROUP BY first_concept, last_concept
    ORDER BY orders DESC
""", [MP, p_ini, p_fin, MP, p_ini, p_fin]).fetchall()

print("  (First concept -> Last concept in paired orders)")
for r in pairs_detail:
    print(f"  {r[0]:45s} -> {r[1]:45s} : {r[2]:5d} orders")

# 1C: Full lifecycle - sample orders with all their entries
print("\n--- 1C: CICLO DE VIDA COMPLETO — 5 ordenes de muestra ---")
sample_orders = db.execute("""
    SELECT id_orden, COUNT(DISTINCT clasificacion_operativa) as concepts
    FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
      AND financial_group = 'ajustes'
      AND clasificacion_operativa IN ('Ajuste por Arrepentimiento', 'Ajuste por Compra Protegida (BPP)',
                                       'Ajuste por Talla/Garantía', 'Ajuste Poscobro Conciliado')
    GROUP BY id_orden
    HAVING COUNT(DISTINCT clasificacion_operativa) >= 2
    ORDER BY COUNT(*) DESC
    LIMIT 5
""", [MP, p_ini, p_fin]).fetchall()

for oid_row in sample_orders:
    oid = oid_row[0]
    print(f"\n  ORDER {oid[:55]}")
    entries = db.execute("""
        SELECT fecha, clasificacion_operativa, monto, financial_group, 
               include_in_operational_pnl, detalle, id_transaccion
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND id_orden = ?
        ORDER BY fecha, id_transaccion
    """, [MP, oid]).fetchall()
    for e in entries:
        print(f"    {str(e[0])[:10]}  {e[1]:45s}  ${fmt(e[2]):>10s}  "
              f"fg={str(e[3]):20s}  op_pnl={e[4]}  det={str(e[5])[:40]}")

# ============================================================
# FASE 2 — GRAFO DE CAUSALIDAD
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 2 — GRAFO DE CAUSALIDAD")
print("=" * 140)

# 2A: Pairing matrix between all 4 concepts
print("\n--- 2A: MATRIZ DE APAREAMIENTO (ambos conceptos en misma orden, ajustes ML) ---")
concept_list = CONCEPTS

# For each pair of concepts, count shared orders
print(f"  {'':45s}", end="")
for c in concept_list:
    print(f"  {c[:25]:25s}", end="")
print()

# Get total standalone per concept
for c1 in concept_list:
    print(f"  {c1[:43]:43s}", end="")
    for c2 in concept_list:
        if c1 == c2:
            # Standalone count
            cnt = db.execute("""
                SELECT COUNT(*) FROM (
                    SELECT id_orden FROM marketplace_ledger_v1
                    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                      AND financial_group = 'ajustes'
                      AND id_orden IN (
                          SELECT id_orden FROM marketplace_ledger_v1
                          WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                            AND financial_group = 'ajustes'
                          GROUP BY id_orden
                          HAVING COUNT(DISTINCT clasificacion_operativa) = 1
                      )
                      AND clasificacion_operativa = ?
                    GROUP BY id_orden
                )
            """, [MP, p_ini, p_fin, MP, p_ini, p_fin, c1]).fetchall()
            print(f"  {'STANDALONE':>10s}  {cnt[0][0]:5d}o", end="")
        elif c1 < c2:
            # Count shared orders
            shared = db.execute("""
                SELECT COUNT(*) as shared_orders,
                       ROUND(SUM(a.monto), 2) as total_a,
                       ROUND(SUM(b.monto), 2) as total_b,
                       ROUND(SUM(CASE WHEN a.monto = b.monto THEN 1 ELSE 0 END) * 100.0 / 
                             NULLIF(COUNT(*), 0), 1) as exact_match_pct
                FROM marketplace_ledger_v1 a
                JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
                    AND a.id_transaccion <> b.id_transaccion
                WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
                  AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
                  AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
                  AND a.clasificacion_operativa = ? AND b.clasificacion_operativa = ?
            """, [MP, p_ini, p_fin, MP, p_ini, p_fin, c1, c2]).fetchall()
            if shared[0][0] > 0:
                print(f"  {shared[0][0]:5d}o ${fmt(shared[0][1])} {shared[0][3]:5.1f}%", end="")
            else:
                print(f"  {'—':>20s}", end="")
        else:
            print(f"  {'':>20s}", end="")
    print()

# 2B: All-time pairing matrix  
print("\n--- 2B: MATRIZ DE APAREAMIENTO ALL-TIME ML ---")
for c1 in concept_list:
    for c2 in concept_list:
        if c1 >= c2:
            continue
        shared = db.execute("""
            SELECT COUNT(*) as shared_orders,
                   ROUND(SUM(a.monto), 2) as total_amt
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
                AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND b.marketplace = ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND a.clasificacion_operativa = ? AND b.clasificacion_operativa = ?
        """, [MP, MP, c1, c2]).fetchall()
        if shared[0][0] > 0:
            a_total = db.execute("""
                SELECT COUNT(*), ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 
                WHERE marketplace = ? AND financial_group = 'ajustes' AND clasificacion_operativa = ?
            """, [MP, c1]).fetchall()
            b_total = db.execute("""
                SELECT COUNT(*), ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 
                WHERE marketplace = ? AND financial_group = 'ajustes' AND clasificacion_operativa = ?
            """, [MP, c2]).fetchall()
            print(f"  {c1:45s} X {c2:45s}")
            print(f"    Shared orders:  {shared[0][0]:6d}")
            print(f"    Shared amount:  ${fmt(shared[0][1])}")
            print(f"    A total:        {a_total[0][0]:6d} rows  ${fmt(a_total[0][1])}")
            print(f"    B total:        {b_total[0][0]:6d} rows  ${fmt(b_total[0][1])}")
            pct_a = shared[0][0]/a_total[0][0]*100 if a_total[0][0] > 0 else 0
            pct_b = shared[0][0]/b_total[0][0]*100 if b_total[0][0] > 0 else 0
            print(f"    % of A paired:  {pct_a:.1f}%")
            print(f"    % of B paired:  {pct_b:.1f}%")

# 2C: Unpaired concept totals
print("\n--- 2C: CONCEPTOS STANDALONE (sin pareja) ---")
for c in CONCEPTS:
    total_recs = db.execute("""
        SELECT COUNT(*) FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes' AND clasificacion_operativa = ?
    """, [MP, p_ini, p_fin, c]).fetchall()
    
    paired_recs = db.execute("""
        SELECT COUNT(DISTINCT a.id_orden)
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa = ? AND b.clasificacion_operativa <> a.clasificacion_operativa
    """, [MP, p_ini, p_fin, MP, p_ini, p_fin, c]).fetchall()
    
    standalone_orders = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT id_orden FROM marketplace_ledger_v1
            WHERE marketplace = ? AND fecha BETWEEN ? AND ?
              AND financial_group = 'ajustes' AND clasificacion_operativa = ?
              AND id_orden IN (
                  SELECT id_orden FROM marketplace_ledger_v1
                  WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                    AND financial_group = 'ajustes'
                  GROUP BY id_orden
                  HAVING COUNT(DISTINCT clasificacion_operativa) = 1
              )
        )
    """, [MP, p_ini, p_fin, c, MP, p_ini, p_fin]).fetchall()
    
    total_orders = db.execute("""
        SELECT COUNT(DISTINCT id_orden) FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes' AND clasificacion_operativa = ?
    """, [MP, p_ini, p_fin, c]).fetchall()
    
    print(f"  {c:45s}")
    print(f"    Total orders:    {total_orders[0][0]:5d}")
    print(f"    Paired orders:   {paired_recs[0][0]:5d} ({paired_recs[0][0]/total_orders[0][0]*100:.1f}%)")
    print(f"    Standalone:      {standalone_orders[0][0]:5d} ({standalone_orders[0][0]/total_orders[0][0]*100:.1f}%)")

# ============================================================
# FASE 3 — PRUEBA DE SUPERVIVENCIA
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 3 — PRUEBA DE SUPERVIVENCIA")
print("=" * 140)

# For each concept, simulate removing it and measure:
# - Information loss (rows removed)
# - Economic loss (monto removed)
# - Unique orders that would lose ALL traceability

print("\n--- 3A: CONCEPTO COMO LADO UNICO ---")
for c in CONCEPTS:
    # Orders that have ONLY this concept (no other partner concept)
    unique_to_this = db.execute("""
        SELECT COUNT(*) as lost_orders,
               ROUND(SUM(monto), 2) as lost_amount,
               COUNT(*) as lost_records
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND clasificacion_operativa = ?
          AND id_orden IN (
              SELECT id_orden FROM marketplace_ledger_v1
              WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                AND financial_group = 'ajustes'
              GROUP BY id_orden
              HAVING COUNT(DISTINCT clasificacion_operativa) = 1
          )
    """, [MP, p_ini, p_fin, c, MP, p_ini, p_fin]).fetchall()
    
    # Orders where this concept is the FIRST chronological entry
    first_entries = db.execute("""
        WITH ranked AS (
            SELECT id_orden, clasificacion_operativa, monto,
                   ROW_NUMBER() OVER (PARTITION BY id_orden ORDER BY fecha, id_transaccion) as seq
            FROM marketplace_ledger_v1
            WHERE marketplace = ? AND fecha BETWEEN ? AND ?
              AND financial_group = 'ajustes'
        )
        SELECT COUNT(*) as as_first,
               ROUND(SUM(monto), 2) as first_amount
        FROM ranked
        WHERE seq = 1 AND clasificacion_operativa = ?
    """, [MP, p_ini, p_fin, c]).fetchall()
    
    # Orders where this concept is the LAST chronological entry
    last_entries = db.execute("""
        WITH ranked AS (
            SELECT id_orden, clasificacion_operativa, monto,
                   ROW_NUMBER() OVER (PARTITION BY id_orden ORDER BY fecha DESC, id_transaccion DESC) as seq
            FROM marketplace_ledger_v1
            WHERE marketplace = ? AND fecha BETWEEN ? AND ?
              AND financial_group = 'ajustes'
        )
        SELECT COUNT(*) as as_last,
               ROUND(SUM(monto), 2) as last_amount
        FROM ranked
        WHERE seq = 1 AND clasificacion_operativa = ?
    """, [MP, p_ini, p_fin, c]).fetchall()
    
    print(f"\n  {c:50s}")
    print(f"    Unique (standalone):       {unique_to_this[0][0]:5d} orders, ${fmt(unique_to_this[0][1])} loss")
    print(f"    As first chronological:    {first_entries[0][0]:5d} orders (CAUSA INICIAL)")
    print(f"    As last chronological:     {last_entries[0][0]:5d} orders (RESULTADO FINAL)")

# 3B: Scenario analysis
print("\n--- 3B: ESCENARIOS DE ELIMINACION CONCEPTUAL ---")
scenarios = [
    ("ESCENARIO A: Eliminar BPP", 
     "", "'Ajuste por Compra Protegida (BPP)'"),
    ("ESCENARIO B: Eliminar Talla/Garantía", 
     "'Ajuste por Talla/Garantía'", ""),
    ("ESCENARIO C: Eliminar Poscobro Conciliado", 
     "", "'Ajuste Poscobro Conciliado'"),
    ("ESCENARIO D: Eliminar Arrepentimiento", 
     "'Ajuste por Arrepentimiento'", ""),
]

for scenario_name, removed_concept, keep_concept_if in scenarios:
    # Simulate: for orders that have the removed concept AND a partner,
    # what survives?
    print(f"\n  {scenario_name}")
    
    # Orders where removing this concept = total information loss
    if keep_concept_if:
        # Removing BPP or Poscobro — keep the partner
        surviving_orders_data = db.execute(f"""
            SELECT COUNT(DISTINCT a.id_orden) as surviving_orders,
                   ROUND(SUM(a.monto), 2) as surviving_amount
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND a.clasificacion_operativa = {keep_concept_if}
              AND b.clasificacion_operativa <> a.clasificacion_operativa
        """, [MP, p_ini, p_fin, MP, p_ini, p_fin]).fetchall()
    else:
        # Removing Talla or Arrepentimiento — keep BPP or Poscobro
        surviving_orders_data = db.execute(f"""
            SELECT COUNT(DISTINCT a.id_orden) as surviving_orders,
                   ROUND(SUM(a.monto), 2) as surviving_amount
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND a.clasificacion_operativa = {removed_concept.replace("'", "'")}
              AND b.clasificacion_operativa <> a.clasificacion_operativa
        """, [MP, p_ini, p_fin, MP, p_ini, p_fin]).fetchall()
    
    # Orders completely lost (standalone)
    lost_standalone = db.execute(f"""
        SELECT COUNT(*) as lost_orders,
               ROUND(SUM(monto), 2) as lost_amount
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND clasificacion_operativa = {keep_concept_if or removed_concept.replace("'", "'")}
          AND id_orden IN (
              SELECT id_orden FROM marketplace_ledger_v1
              WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                AND financial_group = 'ajustes'
              GROUP BY id_orden
              HAVING COUNT(DISTINCT clasificacion_operativa) = 1
          )
    """, [MP, p_ini, p_fin, MP, p_ini, p_fin]) if keep_concept_if else \
    db.execute(f"""
        SELECT COUNT(*) as lost_orders,
               ROUND(SUM(monto), 2) as lost_amount
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND clasificacion_operativa = ?
          AND id_orden IN (
              SELECT id_orden FROM marketplace_ledger_v1
              WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                AND financial_group = 'ajustes'
              GROUP BY id_orden
              HAVING COUNT(DISTINCT clasificacion_operativa) = 1
          )
    """, [MP, p_ini, p_fin, removed_concept.strip("'"), MP, p_ini, p_fin])
    
    print(f"    Surviving orders (partner data preserved): {surviving_orders_data[0][0]:5d}")
    print(f"    Surviving amount:                          ${fmt(surviving_orders_data[0][1])}")
    print(f"    Lost standalone orders:                    {lost_standalone[0][0]:5d}")
    print(f"    Lost amount:                               ${fmt(lost_standalone[0][1])}")

# ============================================================
# FASE 4 — VALIDACION CONTRA LIBERACIONES
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 4 — VALIDACION CONTRA LIBERACIONES (cash trace)")
print("=" * 140)

# Load Liberaciones file
import pandas as pd
lib_path = '01_Raw/ML/Liberaciones/2025-04 Abril/Abril 2025.xlsx'
if os.path.exists(lib_path):
    lib = pd.read_excel(lib_path)
    print(f"\n  Liberaciones file loaded: {lib.shape[0]} rows")
    
    # Map col 1 as ID_OPERACION_MP (order/transaction reference)
    # Map col 6 as DESCRIPCION (description)
    lib_cols = {i: str(lib.columns[i]) for i in range(len(lib.columns))}
    print(f"  Columns available: {lib_cols}")
    
    # Use column 0 as date, column 1 as ID, column 6 as description
    # Check column names
    for idx, col_name in enumerate(lib.columns[:10]):
        print(f"    Col {idx}: '{col_name}'")
else:
    print(f"\n  Liberaciones file NOT FOUND at {lib_path}")

# FASE 4: Take sample of paired orders and trace each entry in Liberaciones
print("\n--- 4A: SAMPLE TRACE — Paired orders in Liberaciones ---")

# Get paired orders from ledger
paired_orders = db.execute("""
    SELECT DISTINCT a.id_orden, 
           a.clasificacion_operativa as concept_a,
           b.clasificacion_operativa as concept_b,
           a.monto as amount
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa IN ('Ajuste por Arrepentimiento', 'Ajuste por Talla/Garantía')
      AND b.clasificacion_operativa IN ('Ajuste por Compra Protegida (BPP)', 'Ajuste Poscobro Conciliado')
    ORDER BY a.monto DESC
    LIMIT 15
""", [MP, p_ini, p_fin, MP, p_ini, p_fin]).fetchall()

if os.path.exists(lib_path):
    for po in paired_orders:
        oid = po[0]
        order_num = ''.join(filter(str.isdigit, str(oid)))[:15]
        
        # Search Liberaciones for this order
        lib_matches = lib[lib.iloc[:, 1].astype(str).str.contains(order_num, na=False)]
        
        print(f"\n  ORDER {str(oid)[:50]}")
        print(f"    Ledger: {po[1]} + {po[2]} = ${fmt(po[3])}")
        
        if len(lib_matches) > 0:
            for _, lrow in lib_matches.iterrows():
                desc = str(lrow.iloc[6])[:40] if len(lib.columns) > 6 else ''
                acr = lrow.iloc[3] if len(lib.columns) > 3 else 0
                deb = lrow.iloc[4] if len(lib.columns) > 4 else 0
                fecha = str(lrow.iloc[0])[:10]
                print(f"    Liberaciones: {fecha}  {desc:40s}  acr=${fmt(acr)}  deb=${fmt(deb)}")
            
            # Check the cash net
            net = lib_matches.iloc[:, 3].sum() - lib_matches.iloc[:, 4].sum()
            print(f"    CASH NETO: ${fmt(net)}")
        else:
            print(f"    Liberaciones: NOT FOUND")

# ============================================================
# FASE 5 — CLASIFICACION FINAL
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 5 — CLASIFICACION FINAL DE CADA CONCEPTO")
print("=" * 140)

# Statistical summary for classification
print("\n--- EVIDENCIA PARA CLASIFICACION ---")
for c in CONCEPTS:
    # Total in ledger
    total = db.execute("""
        SELECT COUNT(*) as recs, 
               ROUND(SUM(monto), 2) as total,
               COUNT(DISTINCT id_orden) as orders
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND financial_group = 'ajustes' AND clasificacion_operativa = ?
    """, [MP, c]).fetchall()
    
    # Paired %
    paired = db.execute("""
        SELECT COUNT(DISTINCT a.id_orden) as paired_orders
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND b.marketplace = ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa = ? AND b.clasificacion_operativa <> a.clasificacion_operativa
    """, [MP, MP, c]).fetchall()
    
    # Ops in P&L
    pnl_dist = db.execute("""
        SELECT include_in_operational_pnl, COUNT(*) as cnt
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND financial_group = 'ajustes' AND clasificacion_operativa = ?
        GROUP BY include_in_operational_pnl
    """, [MP, c]).fetchall()
    
    # Time coverage (first appearance, last appearance)
    time_range = db.execute("""
        SELECT MIN(fecha) as first_seen, MAX(fecha) as last_seen
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND financial_group = 'ajustes' AND clasificacion_operativa = ?
    """, [MP, c]).fetchall()
    
    pct_paired = paired[0][0]/total[0][2]*100 if total[0][2] > 0 else 0
    
    print(f"\n  {c:50s}")
    print(f"    Total all-time:  {total[0][0]:6d} records, ${fmt(total[0][1])}, {total[0][2]:5d} orders")
    print(f"    Paired orders:   {paired[0][0]:6d} ({pct_paired:.1f}%)")
    print(f"    Time range:      {str(time_range[0][0])[:10]} to {str(time_range[0][1])[:10]}")
    pnl_str = "; ".join([f"op_pnl={r[0]}: {r[1]} rows" for r in pnl_dist])
    print(f"    P&L config:      {pnl_str}")

db.close()
print("\n\nDone.")
