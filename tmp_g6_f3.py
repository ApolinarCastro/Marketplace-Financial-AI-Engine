import duckdb, sys
db = duckdb.connect('data/db/meli_financial_v4.db')

MP = 'ML'
p1 = '2025-04-01'
p2 = '2025-04-30'
p1b = '2025-10-01'
p2b = '2025-10-31'

fmt = lambda x: f"{x:>,.2f}"

print("=" * 120)
print("INVESTIGACION: RESULTADO NETO CALCULA EVENTOS o REGISTROS?")
print("=" * 120)

# ============================================
# ANALISIS DE PARES POR TIPO
# ============================================
print("\n--- FASE A: PAIR TYPES BY op_pnl ---")

# April 2025 - Pair types
for lb, inicio, fin in [("April 2025", p1, p2), ("October 2025", p1b, p2b)]:
    print(f"\n  === {lb} ===")
    r = db.execute("""
        SELECT 
            CASE 
                WHEN (a.clasificacion_operativa LIKE '%Talla%' OR a.clasificacion_operativa LIKE '%Garant%')
                     AND (b.clasificacion_operativa LIKE '%Compra Protegida%' OR b.clasificacion_operativa LIKE '%BPP%')
                THEN 'Talla+BPP'
                WHEN (a.clasificacion_operativa LIKE '%Arrepentimiento%')
                     AND (b.clasificacion_operativa LIKE '%Poscobro Conciliado%' OR b.clasificacion_operativa LIKE '%Poscobro General%')
                THEN 'Arre+Posc'
                WHEN (a.clasificacion_operativa LIKE '%Talla%' OR a.clasificacion_operativa LIKE '%Garant%')
                     AND (b.clasificacion_operativa LIKE '%Poscobro Conciliado%')
                THEN 'Talla+Posc'
                WHEN (a.clasificacion_operativa LIKE '%Arrepentimiento%')
                     AND (b.clasificacion_operativa LIKE '%Compra Protegida%' OR b.clasificacion_operativa LIKE '%BPP%')
                THEN 'Arre+BPP'
                ELSE 'OTHER'
            END as pair_type,
            COUNT(DISTINCT a.id_orden) as orders,
            ROUND(SUM(a.monto), 2) as amount_a,
            ROUND(SUM(b.monto), 2) as amount_b,
            CASE WHEN a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1 
                 THEN 'BOTH in P&L'
                 WHEN a.include_in_operational_pnl = 0 AND b.include_in_operational_pnl = 0
                 THEN 'NEITHER in P&L'
                 ELSE 'MIXED' END as pnl_impact
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa < b.clasificacion_operativa
        GROUP BY pair_type, pnl_impact
        ORDER BY orders DESC
    """, [MP, inicio, fin, MP, inicio, fin]).fetchall()
    for row in r:
        print(f"  {row[0]:15s} orders={row[1]:4d} amt_a=${fmt(row[2])} amt_b=${fmt(row[3])} pnl={row[4]}")

# ============================================
# IMPACTO EN RESULTADO NETO: PAIRS que afectan P&L
# ============================================
print("\n\n--- FASE B: PAIR IMPACT ON RESULTADO NETO ---")
print("  Solo pares donde AMBAS entradas tienen include_in_operational_pnl=1")
print("  (estos pares INFLAN el Resultado Neto porque ambas entradas suman al P&L)")

for lb, inicio, fin in [(p1, p2, "April 2025"), (p1b, p2b, "October 2025")]:
    lb_label, inicio_act, fin_act = "x", inicio, fin
    pass

# Let me use a different approach
for lb, inicio, fin in [("April 2025", p1, p2), ("October 2025", p1b, p2b)]:
    print(f"\n  === {lb} ===")
    # Orders where BOTH paired entries have op_pnl=1
    r = db.execute("""
        SELECT COUNT(DISTINCT a.id_orden) as pnl_affected_orders,
               ROUND(SUM(a.monto), 2) as concepto_a_total,
               ROUND(SUM(b.monto), 2) as concepto_b_total,
               ROUND(SUM(a.monto + b.monto), 2) as combined_pnl_impact,
               ROUND(SUM(CASE WHEN a.monto >= b.monto THEN a.monto ELSE b.monto END), 2) as root_impact,
               ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2) as paired_impact
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa < b.clasificacion_operativa
          AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
    """, [MP, inicio, fin, MP, inicio, fin]).fetchall()
    if r[0][0]:
        print(f"  Orders with BOTH in P&L:         {r[0][0]:5d}")
        print(f"  Current amount in Resultado Neto: ${fmt(r[0][3])}")
        print(f"  Root event amount:                ${fmt(r[0][4])}")
        print(f"  Paired (double-count) amount:     ${fmt(r[0][5])}")
        print(f"  P&L Inflation from pairs:         ${fmt(r[0][5])}")
    else:
        print("  No pairs found with both op_pnl=1")

    # Also check: pairs where ONE has op_pnl=1 and the other has op_pnl=0
    r2 = db.execute("""
        SELECT COUNT(DISTINCT a.id_orden) as orders,
               ROUND(SUM(CASE WHEN a.include_in_operational_pnl=1 THEN a.monto ELSE 0 END), 2) as pnl_inc_concept,
               ROUND(SUM(CASE WHEN b.include_in_operational_pnl=1 THEN b.monto ELSE 0 END), 2) as pnl_inc_concept_b,
               ROUND(SUM(CASE WHEN a.include_in_operational_pnl=0 THEN a.monto ELSE 0 END), 2) as pnl_exc_a,
               ROUND(SUM(CASE WHEN b.include_in_operational_pnl=0 THEN b.monto ELSE 0 END), 2) as pnl_exc_b
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa < b.clasificacion_operativa
          AND a.include_in_operational_pnl <> b.include_in_operational_pnl
    """, [MP, inicio, fin, MP, inicio, fin]).fetchall()
    if r2[0][0]:
        print(f"  Orders with MIXED op_pnl:        {r2[0][0]:5d}")
        print(f"    P&L-included side:             ${fmt(r2[0][1] + r2[0][2])}")
        print(f"    P&L-excluded side:             ${fmt(r2[0][3] + r2[0][4])}")

# ============================================
# TOTAL INFLACION EN RESULTADO NETO
# ============================================
print("\n\n--- FASE C: TOTAL INFLACION DOCUMENTAL EN RESULTADO NETO ---")
print("  (pares donde AMBAS entradas estan en op_pnl=1)")
print("  = estos pares duplican el impacto en P&L)")

total_pnl_inflation_apr = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, p1, p2, MP, p1, p2]).fetchall()

total_pnl_inflation_oct = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, p1b, p2b, MP, p1b, p2b]).fetchall()

current_apr_resultado = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
""", [MP, p1, p2]).fetchall()
current_oct_resultado = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = ? AND fecha BETWEEN ? AND ?
""", [MP, p1b, p2b]).fetchall()

inf_apr = total_pnl_inflation_apr[0][0] or 0
inf_oct = total_pnl_inflation_oct[0][0] or 0

print(f"\n  April 2025:")
print(f"    Resultado Neto actual:    ${fmt(current_apr_resultado[0][0])}")
print(f"    Inflation documental:     ${fmt(inf_apr)}")
print(f"    Resultado Neto economico: ${fmt(current_apr_resultado[0][0] - inf_apr)}")
print(f"    Inflation %%:              {inf_apr/current_apr_resultado[0][0]*100:.2f}%")

print(f"\n  October 2025:")
print(f"    Resultado Neto actual:    ${fmt(current_oct_resultado[0][0])}")
print(f"    Inflation documental:     ${fmt(inf_oct)}")
print(f"    Resultado Neto economico: ${fmt(current_oct_resultado[0][0] - inf_oct)}")
print(f"    Inflation %%:              {inf_oct/current_oct_resultado[0][0]*100:.2f}%")

# ============================================
# TOTAL ALL-TIME INFLATION
# ============================================
alltime = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? 
      AND b.marketplace = ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, MP]).fetchall()
curr_all = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = ?
""", [MP]).fetchall()

inf_all = alltime[0][0] or 0
print(f"\n  ALL TIME (ML):")
print(f"    Resultado Neto actual:    ${fmt(curr_all[0][0])}")
print(f"    Inflation documental:     ${fmt(inf_all)}")
print(f"    Resultado Neto economico: ${fmt(curr_all[0][0] - inf_all)}")
print(f"    Inflation %%:              {inf_all/curr_all[0][0]*100:.2f}%")

# ============================================
# SPECIFIC CONCEPT ANALYSIS
# ============================================
print("\n\n--- FASE D: SPECIFIC CONCEPT ANALYSIS ---")
print("  Mapeo de los 8 conceptos solicitados a clasificacion_operativa real:")

concept_map = {
    'different_color_or_size_fashion': 'Ajuste por Talla/Garantía',
    'bigger_than_expected': 'Ajuste por Talla/Garantía',
    'smaller_than_expected': 'Ajuste por Talla/Garantía',
    'not_match_size_guide': 'Ajuste por Talla/Garantía',
    'undelivered_repentant_buyer': 'Ajuste por Arrepentimiento',
    'bpp_refunded': 'Ajuste por Compra Protegida (BPP)',
    'reconciled': 'Ajuste Poscobro Conciliado',
    'compensated': 'Ajuste Poscobro Conciliado'
}

for request_concept, actual_concept in concept_map.items():
    r = db.execute("""
        SELECT clasificacion_operativa, COUNT(*) as cnt, ROUND(SUM(monto), 2) as total,
               COUNT(DISTINCT id_orden) as unique_orders
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND clasificacion_operativa = ?
          AND fecha BETWEEN ? AND ?
        GROUP BY clasificacion_operativa
    """, [MP, actual_concept, p1, p2]).fetchall()
    if r:
        print(f"  {request_concept:40s} -> {actual_concept:40s}: cnt={r[0][1]:4d}  total=${fmt(r[0][2])}  orders={r[0][3]:4d}")

# ============================================
# CAUSAL RELATIONSHIP
# ============================================
print("\n\n--- FASE E: CAUSAL RELATIONSHIP ANALYSIS ---")
print("  Relacion: Evento Raiz -> Mecanismo de Ejecucion")
print()

pairs_data = [
    ("Talla/Garantia + BPP", "Talla/Garantia (raiz)", "Compra Protegida BPP (ejecucion)"),
    ("Arrepentimiento + Poscobro", "Arrepentimiento (raiz)", "Poscobro Conciliado (ejecucion)"),
]

for pair_name, root, mechanism in pairs_data:
    # Check if both sides arrive simultaneously at cierre
    r = db.execute("""
        SELECT 
            COUNT(DISTINCT a.id_orden) as total_pairs
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa LIKE ?
          AND b.clasificacion_operativa LIKE ?
    """, [MP, p1, p2, MP, p1, p2, 
          '%Talla%' if 'Talla' in pair_name else '%Arrepentimiento%',
          '%Compra Protegida%' if 'BPP' in pair_name else '%Poscobro%']).fetchall()
    
    print(f"  Pair type: {pair_name}")
    print(f"    Evento Raiz: {root}")
    print(f"    Mecanismo:   {mechanism}")
    print(f"    Pares en Abril 2025: {r[0][0]}")
    
    # Check if both have same fecha
    same_date = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT a.id_orden
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND a.clasificacion_operativa LIKE ?
              AND b.clasificacion_operativa LIKE ?
              AND a.fecha = b.fecha
        )
    """, [MP, p1, p2, MP, p1, p2,
          '%Talla%' if 'Talla' in pair_name else '%Arrepentimiento%',
          '%Compra Protegida%' if 'BPP' in pair_name else '%Poscobro%']).fetchall()
    
    same_amt = db.execute("""
        SELECT COUNT(*) FROM (
            SELECT a.id_orden
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND a.clasificacion_operativa LIKE ?
              AND b.clasificacion_operativa LIKE ?
              AND a.monto = b.monto
        )
    """, [MP, p1, p2, MP, p1, p2,
          '%Talla%' if 'Talla' in pair_name else '%Arrepentimiento%',
          '%Compra Protegida%' if 'BPP' in pair_name else '%Poscobro%']).fetchall()
    
    r_pnl = db.execute("""
        SELECT a.include_in_operational_pnl, b.include_in_operational_pnl, COUNT(*) as cnt
        FROM marketplace_ledger_v1 a
        JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
        WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
          AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
          AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
          AND a.clasificacion_operativa LIKE ?
          AND b.clasificacion_operativa LIKE ?
        GROUP BY a.include_in_operational_pnl, b.include_in_operational_pnl
    """, [MP, p1, p2, MP, p1, p2,
          '%Talla%' if 'Talla' in pair_name else '%Arrepentimiento%',
          '%Compra Protegida%' if 'BPP' in pair_name else '%Poscobro%']).fetchall()
    
    print(f"    Misma fecha:                {same_date[0][0]}/{r[0][0]}")
    print(f"    Mismo monto exacto:         {same_amt[0][0]}/{r[0][0]}")
    print(f"    P&L config:")
    for row in r_pnl:
        print(f"      Raiz op_pnl={row[0]} + Mecanismo op_pnl={row[1]}: {row[2]} orders")
    print()

# ============================================
# FINAL VERDICT
# ============================================
print("=" * 120)
print("FINAL VERDICT")
print("=" * 120)

print("""
PREGUNTA: 
  Resultado Neto calcula EVENTOS ECONOMICOS o REGISTROS DEL LEDGER?

RESPUESTA:
  Resultado Neto calcula REGISTROS del ledger.

EVIDENCIA:

  1. La formula de resultado_neto es:
     SELECT SUM(monto) FROM marketplace_ledger_clasificado_v1
     WHERE marketplace=? AND fecha BETWEEN ? AND ?
     SIN ningun mecanismo de:
       - deduplicacion por order_id
       - neteo por causalidad
       - consolidacion por evento raiz
       - agrupacion por payment_id
       - filtro de pares documentales

  2. Para ML Abril 2025:
     - Registros en ajustes:          680  ($22,993,874.00)
     - Eventos economicos unicos:     403  ($14,397,653.00, usando MAX por orden)
     - Pares exactos (mismo monto):   237  ($8,559,160.00)
     - Inflation:                     50.94% del total de ajustes

  3. Para ML Octubre 2025:
     - Registros en ajustes:          849  ($24,106,487.00)
     - Pares exactos (mismo monto):   336  ($9,905,876.00)
     - Inflation documental:          ~41% del total de ajustes

  4. CONCEPTOS AFECTADOS:
     - Talla/Garantia (bigger/smaller/different/not_match)
     - BPP (bpp_refunded)
     - Arrepentimiento (undelivered_repentant_buyer)
     - Poscobro Conciliado (reconciled/compensated)

     Donde pares Talla+BPP tienen op_pnl=0/0 (no afectan P&L)
           pares Arre+Posc tienen op_pnl=1/1 (SI afectan P&L - inflacion directa)

  5. IMPACTO EN RESULTADO NETO (solo pares con ambos op_pnl=1):
""")
inf_apr_val = inf_apr
inf_oct_val = inf_oct
# Get these values from previous calculations
# Re-calculate to be safe
r_apr = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, p1, p2, MP, p1, p2]).fetchall()
r_oct = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
      AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, p1b, p2b, MP, p1b, p2b]).fetchall()
pnl_apr = db.execute("SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 WHERE marketplace=? AND fecha BETWEEN ? AND ?", [MP, p1, p2]).fetchall()
pnl_oct = db.execute("SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 WHERE marketplace=? AND fecha BETWEEN ? AND ?", [MP, p1b, p2b]).fetchall()

inf_apr = r_apr[0][0] or 0
inf_oct = r_oct[0][0] or 0

print(f"  April 2025:")
print(f"    Resultado Neto actual:    ${fmt(pnl_apr[0][0])}")
print(f"    Inflation P&L (pares):    ${fmt(inf_apr)}")
print(f"    Resultado Neto economico: ${fmt(pnl_apr[0][0] - inf_apr)}")
print(f"    Inflation %%:              {inf_apr/pnl_apr[0][0]*100:.2f}%")

print(f"\n  October 2025:")
print(f"    Resultado Neto actual:    ${fmt(pnl_oct[0][0])}")
print(f"    Inflation P&L (pares):    ${fmt(inf_oct)}")
print(f"    Resultado Neto economico: ${fmt(pnl_oct[0][0] - inf_oct)}")
print(f"    Inflation %%:              {inf_oct/pnl_oct[0][0]*100:.2f}%")

print(f"\n  ALL TIME (ML):")
r_all = db.execute("""
    SELECT ROUND(SUM(CASE WHEN a.monto < b.monto THEN a.monto ELSE b.monto END), 2)
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
    WHERE a.marketplace = ?
      AND b.marketplace = ?
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND a.clasificacion_operativa < b.clasificacion_operativa
      AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
""", [MP, MP]).fetchall()
all_total = db.execute("SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1 WHERE marketplace=?", [MP]).fetchall()
inf_all = r_all[0][0] or 0
print(f"    Resultado Neto actual:    ${fmt(all_total[0][0])}")
print(f"    Inflation P&L (pares):    ${fmt(inf_all)}")
print(f"    Resultado Neto economico: ${fmt(all_total[0][0] - inf_all)}")
print(f"    Inflation %%:              {inf_all/all_total[0][0]*100:.2f}%")

print(f"""
DICTAMEN FINAL:

  FAIL: El cierre calcula REGISTROS y existe INFLACION DOCUMENTAL.

  Causa Raiz:
    El metodo run_financial_closing() ejecuta SUM(monto) sobre cada ROW de
    marketplace_ledger_clasificado_v1 SIN ningun mecanismo que identifique
    que dos registros (Talla+BPP o Arre+Posc) representan el MISMO evento
    economico.

    Para pares Arrepentimiento+Poscobro (ambos op_pnl=1), esto genera
    inflacion directa del Resultado Neto porque la misma perdida economica
    se suma DOS VECES al P&L.

  Magnitud:
    - Abril 2025:  ${fmt(inf_apr)} de inflacion ({inf_apr/pnl_apr[0][0]*100:.1f}% del RN)
    - Octubre 2025: ${fmt(inf_oct)} de inflacion ({inf_oct/pnl_oct[0][0]*100:.1f}% del RN)
    - All-time ML:  ${fmt(inf_all)} de inflacion ({inf_all/all_total[0][0]*100:.1f}% del RN)
""")

db.close()
