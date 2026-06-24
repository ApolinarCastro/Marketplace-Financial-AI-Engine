import duckdb, sys, os

db = duckdb.connect('data/db/meli_financial_v4.db')
fmt = lambda x: f"{x:>,.2f}"

MP = 'ML'

print("=" * 140)
print("RFC_FINANCIAL_STRUCTURE_REDESIGN — READ ONLY FORENSIC ANALYSIS")
print("=" * 140)

# ============================================================
# CLASSIFICATION 1: FINANCIAL_STRUCTURE dictionary content
# ============================================================
print("\n--- FASE 1A: FINANCIAL STRUCTURE DICTIONARY (from marketplace_auditor.py) ---")
financial_structure = {
    "ingresos": [
        "Cargo por venta", "Cargo por venta (Venta)", "Venta", "Bonificación", "Rebate",
        "Compensación comercial", "Importe del pedido", "Pago",
        "Despacho", "Sale amount", "Gross sales",
        "Pago por precio del producto",
    ],
    "devoluciones": [
        "Pedidos reembolsados", "Devolución", "Devolución de venta", "Devolución de dinero",
        "Descuento por devolución de producto",
    ],
    "costos_operacionales": [
        "Cargo por envíos de Mercado Libre", "Cargo por Mercado Envíos",
        "Anulación del cargo por envíos de ML", "Anulación del cargo por Mercado Envíos",
        "Anulación del cargo por envíos de Mercado Libre",
        "Cargo por devolución", "Anulación del cargo por devolución",
    ],
    "costos_comerciales": [
        "Cargo por venta (Comisión)", "Anulación del cargo por venta",
        "Reembolso por comisión",
        "Cargo por campaña de publicidad - Product Ads",
        "Cargo por campaña de publicidad - Brand Ads",
        "Cargo por campaña de publicidad - Display",
        "Cargo por campaña de publicidad - Display programático",
        "Campañas de publicidad - Product Ads",
        "Campañas de publicidad - Brand Ads",
        "Campañas de publicidad - Display",
        "Cargo por mantenimiento de Mi página",
        "Cargo por Asesoría Comercial",
    ],
    "ajustes": [
        "Descuento por cancelación", "Otros descuentos",
        "Compensación logística", "Ajuste Inventario Activo",
        "Cobro por campaña", "Merma", "Multa", "Multa por stock",
        "Ajuste por Talla/Garantía", "Ajuste por Arrepentimiento",
        "Ajuste por Compra Protegida (BPP)",
        "Ajuste Poscobro Conciliado", "Ajuste Poscobro General",
        "Ajuste por Cambio de Dirección", "Ajuste por Diferencia de Publicación",
        "Ajuste por Disputa no Respondida", "Ajuste por Falla en Entrega",
        "Ajuste por Falta de Stock", "Ajuste por Producto Dañado/Vacío",
        "Ajuste por Retraso en Entrega", "Ajuste por Ítem Faltante",
        "Cargo por diferencias en las medidas y el peso del paquete",
        "Cargo por retiro de stock Full", "Cargo por servicio de almacenamiento Full",
        "Cargo por sobrepasar espacio Full", "Cargo por stock antiguo en Full",
        "Abono manual",
    ],
    "tesoreria": ["Retiro de dinero"]
}

# ============================================================
# CLASSIFICATION 2: ALL actual clasificacion_operativa in DB
# ============================================================
print("\n--- FASE 1B: ALL ACTUAL CONCEPTOS in DB (ML, with counts) ---")
all_concepts = db.execute("""
    SELECT clasificacion_operativa, financial_group,
           COUNT(*) as records,
           COUNT(DISTINCT id_orden) as orders,
           ROUND(SUM(monto), 2) as total,
           ROUND(AVG(monto), 2) as avg_monto,
           MIN(fecha) as first_seen,
           MAX(fecha) as last_seen,
           SUM(CASE WHEN include_in_operational_pnl = 1 THEN 1 ELSE 0 END) as in_pnl,
           SUM(CASE WHEN include_in_operational_pnl = 0 THEN 1 ELSE 0 END) as not_in_pnl
    FROM marketplace_ledger_v1
    WHERE marketplace = 'ML'
    GROUP BY clasificacion_operativa, financial_group
    ORDER BY financial_group, total DESC
""").fetchall()

print(f"  {'Concepto':55s} {'FG':22s} {'Records':8s} {'Orders':7s} {'Total':15s} {'Avg':12s} {'inPNL':6s} {'notPNL':6s}")
print(f"  {'-'*55} {'-'*22} {'-'*8} {'-'*7} {'-'*15} {'-'*12} {'-'*6} {'-'*6}")
for r in all_concepts:
    fg = r[1] if r[1] else 'NULL'
    print(f"  {r[0]:55s} {fg:22s} {r[2]:8d} {r[3]:7d} ${fmt(r[4]):>12s} ${fmt(r[5]):>9s} {r[8]:6d} {r[9]:6d}")

# ============================================================
# FASE 1C: Classification of each concept
# ============================================================
print("\n\n--- FASE 1C: ECONOMIC CLASSIFICATION OF EACH CONCEPT (ML) ---")
print()

# Define classification for each concept based on RFC evidence
classifications = {}

for r in all_concepts:
    concept = r[0]
    fg = r[1]
    records = r[2]
    orders = r[3]
    total = r[4]
    in_pnl = r[8]
    not_pnl = r[9]
    pnl_pct = in_pnl / (in_pnl + not_pnl) * 100 if (in_pnl + not_pnl) > 0 else 0

    # Determine classification based on evidence from RFCs
    is_revenue = concept in ['Cargo por venta (Venta)', 'Cargo por venta', 'Venta', 'Importe del pedido', 'Pago', 'Sale amount', 'Gross sales', 'Pago por precio del producto']
    is_bonus = concept in ['Bonificación', 'Rebate', 'Compensación comercial', 'Despacho']
    is_refund = concept in ['Devolución de venta', 'Devolución de dinero', 'Devolución', 'Pedidos reembolsados', 'Descuento por devolución de producto']
    is_shipping = concept in ['Cargo por envíos de Mercado Libre', 'Cargo por Mercado Envíos', 'Anulación del cargo por envíos de Mercado Libre', 'Anulación del cargo por envíos de ML', 'Anulación del cargo por Mercado Envíos', 'Cargo por devolución', 'Anulación del cargo por devolución']
    is_commission = concept in ['Cargo por venta (Comisión)', 'Anulación del cargo por venta', 'Reembolso por comisión']
    is_ads = concept in ['Cargo por campaña de publicidad - Product Ads', 'Cargo por campaña de publicidad - Brand Ads', 'Cargo por campaña de publicidad - Display', 'Cargo por campaña de publicidad - Display programático', 'Campañas de publicidad - Product Ads', 'Campañas de publicidad - Brand Ads', 'Campañas de publicidad - Display']
    is_fixed_fees = concept in ['Cargo por mantenimiento de Mi página', 'Cargo por Asesoría Comercial']
    is_fulfillment = concept in ['Cargo por retiro de stock Full', 'Cargo por servicio de almacenamiento Full', 'Cargo por sobrepasar espacio Full', 'Cargo por stock antiguo en Full']
    is_size_issue = concept == 'Ajuste por Talla/Garantía'
    is_repentance = concept == 'Ajuste por Arrepentimiento'
    is_bpp = concept == 'Ajuste por Compra Protegida (BPP)'
    is_poscobro = concept in ['Ajuste Poscobro Conciliado', 'Ajuste Poscobro General']
    is_delivery_fail = concept in ['Ajuste por Falla en Entrega', 'Ajuste por Retraso en Entrega', 'Ajuste por Cambio de Dirección', 'Ajuste por Ítem Faltante', 'Ajuste por Producto Dañado/Vacío']
    is_adjustment = concept in ['Ajuste por Diferencia de Publicación', 'Ajuste por Disputa no Respondida', 'Ajuste por Falta de Stock', 'Abono manual', 'Cargo por diferencias en las medidas y el peso del paquete']
    
    if is_revenue:
        cls = "Evento Economico"
        detail = "Ingreso directo por venta de producto"
        show_pnl = True
        show_audit = False
    elif is_bonus:
        cls = "Evento Economico"
        detail = "Bonificacion/Rebate/Compensacion comercial"
        show_pnl = True
        show_audit = False
    elif is_refund:
        cls = "Evento Economico"
        detail = "Devolucion de venta (contraparte del ingreso)"
        show_pnl = True
        show_audit = False
    elif is_shipping:
        cls = "Evento Economico"
        detail = "Costo logistico operacional"
        show_pnl = True
        show_audit = False
    elif is_commission:
        cls = "Evento Economico"
        detail = "Comision ML por venta"
        show_pnl = True
        show_audit = False
    elif is_ads:
        cls = "Evento Economico"
        detail = "Gasto de publicidad"
        show_pnl = True
        show_audit = False
    elif is_fixed_fees:
        cls = "Evento Economico"
        detail = "Costo fijo comercial"
        show_pnl = True
        show_audit = False
    elif is_fulfillment:
        cls = "Evento Economico"
        detail = "Costo de fulfillment/logistica ML"
        show_pnl = True
        show_audit = False
    elif is_size_issue:
        cls = "Evento Economico Raiz (Postventa)"
        detail = "RFC probado: evento economico real con cash outflow"
        show_pnl = False  # Currently op_pnl=0 in most cases
        show_audit = True
    elif is_repentance:
        cls = "Evento Economico Raiz (Postventa)"
        detail = "RFC probado: evento economico real con cash outflow"
        show_pnl = True  # Currently op_pnl=1
        show_audit = True
    elif is_bpp:
        cls = "Mecanismo de Ejecucion"
        detail = "RFC probado: reserve contable, NETO CERO en cash, pareado 99.7%"
        show_pnl = False
        show_audit = True
    elif is_poscobro:
        cls = "Mecanismo de Ejecucion"
        detail = "RFC probado: intento de cobro, NETO CERO en cash cuando pareado"
        show_pnl = False if is_poscobro else True
        show_audit = True
    elif is_delivery_fail:
        cls = "Evento Economico Postventa"
        detail = "Ajuste postventa con impacto economico real"
        show_pnl = True
        show_audit = True
    elif is_adjustment:
        cls = "Ajuste Operacional"
        detail = "Otros ajustes varios"
        show_pnl = True
        show_audit = True
    else:
        cls = "No clasificado"
        detail = ""
        show_pnl = pnl_pct > 50
        show_audit = True
    
    classifications[concept] = (cls, detail, show_pnl, show_audit, total, records, orders)

# Print classification matrix
print(f"  {'Concepto':55s} {'Clasificacion':30s} {'Records':8s} {'Orders':7s} {'Total':15s} {'PNL?':6s} {'Audit?':6s}")
print(f"  {'-'*55} {'-'*30} {'-'*8} {'-'*7} {'-'*15} {'-'*6} {'-'*6}")
for concept, cls_data in sorted(classifications.items(), key=lambda x: (x[1][0], -abs(x[1][4]))):
    cls_name, detail, show_pnl, show_audit, total, records, orders = cls_data
    pnl_str = "SI" if show_pnl else "NO"
    aud_str = "SI" if show_audit else "NO"
    print(f"  {concept:55s} {cls_name:30s} {records:8d} {orders:7d} ${fmt(total):>12s} {pnl_str:6s} {aud_str:6s}")

# ============================================================
# FASE 2: CURRENT vs ECONOMIC MODEL
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 2 — MODELO ACTUAL vs MODELO ECONOMICO")
print("=" * 140)

for lb, p1, p2 in [("Abril 2025", '2025-04-01', '2025-04-30'), ("Octubre 2025", '2025-10-01', '2025-10-31'), ("All-time", '2024-01-01', '2026-12-31')]:
    print(f"\n  === {lb} ===")
    
    # Current model: ALL entries
    current_all = db.execute("""
        SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
    """, [MP, p1, p2]).fetchall()[0][0] or 0
    
    # Current model: by financial_group (all records)
    current_by_group = db.execute("""
        SELECT financial_group, ROUND(SUM(monto), 2) as total
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
        GROUP BY financial_group
        ORDER BY total DESC
    """, [MP, p1, p2]).fetchall()
    
    print(f"\n  MODELO ACTUAL (SUM de todos los registros):")
    print(f"    Resultado Neto: ${fmt(current_all)}")
    for g in current_by_group:
        print(f"    {g[0] or 'NULL':25s} ${fmt(g[1])}")
    
    # ECONOMIC MODEL:
    # Rule 1: Remove Mecanismos de Ejecucion (BPP, Poscobro Conciliado, Poscobro General)
    #   BUT only when they are PAIRED with a root event
    #   If they are STANDALONE, they ARE the economic event
    # Rule 2: Keep all Eventos Economicos as-is
    # Rule 3: Talla/Garantia and Arrepentimiento stay (they are the root events)
    
    # Economic model: SUM all entries MINUS paired mechanisms
    # Paired BPP entries = BPP entries where the same order also has Talla/Garantia
    # Paired Poscobro entries = Poscobro where same order also has Arrepentimiento or Talla/Garantia
    
    economic = db.execute("""
        WITH paired_mechanisms AS (
            SELECT DISTINCT a.id_transaccion
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND (
                  (a.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)' 
                   AND b.clasificacion_operativa = 'Ajuste por Talla/Garantía')
                  OR
                  (a.clasificacion_operativa LIKE '%Poscobro%' 
                   AND (b.clasificacion_operativa = 'Ajuste por Arrepentimiento' OR b.clasificacion_operativa = 'Ajuste por Talla/Garantía'))
              )
        )
        SELECT ROUND(SUM(monto), 2) as economic_neto
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND id_transaccion NOT IN (SELECT id_transaccion FROM paired_mechanisms)
    """, [MP, p1, p2, MP, p1, p2, MP, p1, p2]).fetchall()[0][0] or 0
    
    # Also calculate: standalone mechanisms (not paired) that SHOULD count as economic events
    standalone_mech = db.execute("""
        SELECT ROUND(SUM(monto), 2) as standalone_mech
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND (clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)' OR clasificacion_operativa LIKE '%Poscobro%')
          AND id_orden IN (
              SELECT id_orden FROM marketplace_ledger_v1
              WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                AND financial_group = 'ajustes'
              GROUP BY id_orden
              HAVING COUNT(DISTINCT clasificacion_operativa) = 1
          )
    """, [MP, p1, p2, MP, p1, p2]).fetchall()[0][0] or 0
    
    total_economic = economic + standalone_mech if economic and standalone_mech else (economic or standalone_mech or 0)
    
    # Paired mechanisms removed
    paired_removed = db.execute("""
        WITH paired_mechanisms AS (
            SELECT DISTINCT a.id_transaccion, a.monto
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND (
                  (a.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)' 
                   AND b.clasificacion_operativa = 'Ajuste por Talla/Garantía')
                  OR
                  (a.clasificacion_operativa LIKE '%Poscobro%' 
                   AND (b.clasificacion_operativa = 'Ajuste por Arrepentimiento' OR b.clasificacion_operativa = 'Ajuste por Talla/Garantía'))
              )
        )
        SELECT ROUND(SUM(monto), 2) FROM paired_mechanisms
    """, [MP, p1, p2, MP, p1, p2]).fetchall()[0][0] or 0
    
    print(f"\n  MODELO ECONOMICO (eventos economicos unicos):")
    print(f"    Resultado Neto: ${fmt(total_economic)}")
    print(f"    Mecanismos pareados eliminados: ${fmt(paired_removed)}")
    print(f"    Mecanismos standalone preservados: ${fmt(standalone_mech)}")
    print(f"    Delta (Actual - Economico): ${fmt(current_all - total_economic)}")
    print(f"    Inflation %%:         {(current_all - total_economic)/current_all*100:.2f}%" if current_all != 0 else "N/A")

# ============================================================
# FASE 3: What goes in Financial Structure vs Drill Down
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 3 — ESTRUCTURA vs DRILL DOWN vs AUDITORIA")
print("=" * 140)

print("""
  JERARQUIA PROPUESTA:

  NIVEL 1 — FINANCIAL STRUCTURE (CORE P&L)
    Debe contener SOLO eventos economicos reales.
    Refleja la realidad economica del negocio.

  NIVEL 2 — DRILL DOWN (Postventa & Ajustes)
    Desglose de eventos postventa y ajustes.
    Separa Eventos Economicos de Mecanismos.

  NIVEL 3 — AUDITORIA (Trazabilidad)
    Trazabilidad completa incluyendo mecanismos.
    Permite reconciliar con archivos fuente de ML.
""")

# What should be in Financial Structure
print("\n  EN FINANCIAL STRUCTURE (P&L oficial):")
for concept, cls_data in classifications.items():
    cls_name, detail, show_pnl, show_audit, total, records, orders = cls_data
    if show_pnl:
        print(f"    {concept:55s} ${fmt(total):>12s}")

print("\n  EN DRILL DOWN / AUDITORIA (solo trazabilidad):")
for concept, cls_data in classifications.items():
    cls_name, detail, show_pnl, show_audit, total, records, orders = cls_data
    if show_audit and not show_pnl:
        print(f"    {concept:55s} ${fmt(total):>12s}")

# ============================================================
# FASE 4: Proof of reconciliation for Shopify certification
# ============================================================
print("\n\n" + "=" * 140)
print("FASE 4 — VERIFICACION PARA CERTIFICACION SHOPIFY")
print("=" * 140)

# Check: How many concepts in current ajustes are ACTUALLY economic events vs mechanisms?
print("\n--- 4A: AJUSTES BREAKDOWN (All-time ML) ---")
ajustes_total = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND financial_group = 'ajustes'
""").fetchall()[0][0] or 0

# Economic events in ajustes
ajustes_economic = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND financial_group = 'ajustes'
      AND clasificacion_operativa IN (
          'Ajuste por Talla/Garantía', 'Ajuste por Arrepentimiento',
          'Ajuste por Falla en Entrega', 'Ajuste por Retraso en Entrega',
          'Ajuste por Producto Dañado/Vacío', 'Ajuste por Cambio de Dirección',
          'Ajuste por Ítem Faltante'
      )
""").fetchall()[0][0] or 0

# Mechanisms in ajustes
ajustes_mech = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND financial_group = 'ajustes'
      AND clasificacion_operativa IN (
          'Ajuste por Compra Protegida (BPP)',
          'Ajuste Poscobro Conciliado', 'Ajuste Poscobro General'
      )
""").fetchall()[0][0] or 0

# Other adjustments
ajustes_other = db.execute("""
    SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
    WHERE marketplace = 'ML' AND financial_group = 'ajustes'
      AND clasificacion_operativa NOT IN (
          'Ajuste por Talla/Garantía', 'Ajuste por Arrepentimiento',
          'Ajuste por Falla en Entrega', 'Ajuste por Retraso en Entrega',
          'Ajuste por Producto Dañado/Vacío', 'Ajuste por Cambio de Dirección',
          'Ajuste por Ítem Faltante',
          'Ajuste por Compra Protegida (BPP)',
          'Ajuste Poscobro Conciliado', 'Ajuste Poscobro General'
      )
""").fetchall()[0][0] or 0

print(f"  Total ajustes:            ${fmt(ajustes_total)}")
print(f"  Economic events in ajust: ${fmt(ajustes_economic)} (${fmt(ajustes_economic/ajustes_total*100)}%)")
print(f"  Mechanisms in ajust:      ${fmt(ajustes_mech)} (${fmt(ajustes_mech/ajustes_total*100)}%)")
print(f"  Other ajustes:            ${fmt(ajustes_other)} (${fmt(ajustes_other/ajustes_total*100)}%)")

# Check: Reconciliation pass
print("\n--- 4B: RECONCILIATION TEST — Economic Model vs Current ---")
for lb, p1, p2 in [("Abril 2025", '2025-04-01', '2025-04-30'), ("Octubre 2025", '2025-10-01', '2025-10-31'), ("All-time", '2024-01-01', '2026-12-31')]:
    current = db.execute("""
        SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
    """, [MP, p1, p2]).fetchall()[0][0] or 0
    
    # Economic = current - paired mechanisms + standalone mechanisms
    paired_removed = db.execute("""
        WITH paired_mechanisms AS (
            SELECT DISTINCT a.id_transaccion, a.monto
            FROM marketplace_ledger_v1 a
            JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden AND a.id_transaccion <> b.id_transaccion
            WHERE a.marketplace = ? AND a.fecha BETWEEN ? AND ?
              AND b.marketplace = ? AND b.fecha BETWEEN ? AND ?
              AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
              AND (
                  (a.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)' 
                   AND b.clasificacion_operativa = 'Ajuste por Talla/Garantía')
                  OR
                  (a.clasificacion_operativa LIKE '%Poscobro%' 
                   AND (b.clasificacion_operativa = 'Ajuste por Arrepentimiento' OR b.clasificacion_operativa = 'Ajuste por Talla/Garantía'))
              )
        )
        SELECT ROUND(SUM(monto), 2) FROM paired_mechanisms
    """, [MP, p1, p2, MP, p1, p2]).fetchall()[0][0] or 0
    
    standalone_mech = db.execute("""
        SELECT ROUND(SUM(monto), 2) FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
          AND financial_group = 'ajustes'
          AND (clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)' OR clasificacion_operativa LIKE '%Poscobro%')
          AND id_orden IN (
              SELECT id_orden FROM marketplace_ledger_v1
              WHERE marketplace = ? AND fecha BETWEEN ? AND ?
                AND financial_group = 'ajustes'
              GROUP BY id_orden
              HAVING COUNT(DISTINCT clasificacion_operativa) = 1
          )
    """, [MP, p1, p2, MP, p1, p2]).fetchall()[0][0] or 0
    
    economic = current - paired_removed + standalone_mech
    
    print(f"\n  {lb}")
    print(f"    Current RN:           ${fmt(current)}")
    print(f"    Paired removed:       ${fmt(paired_removed)}")
    print(f"    Standalone preserved: ${fmt(standalone_mech)}")
    print(f"    Economic RN:          ${fmt(economic)}")
    print(f"    Delta:                ${fmt(current - economic)}")
    if current != 0:
        print(f"    Adj %%:               {(current - economic)/current*100:.2f}%")

# ============================================================
# FINAL VERDICT
# ============================================================
print("\n\n" + "=" * 140)
print("FINAL VERDICT")
print("=" * 140)

print("""
PREGUNTA 1: 
  La estructura financiera actual representa la realidad economica?

RESPUESTA: 
  FAIL.

  La estructura financiera actual mezcla EVENTOS ECONOMICOS REALES con 
  MECANISMOS DE EJECUCION DE ML en la misma categoria 'ajustes'. Esto 
  produce que el Resultado Neto incluya transacciones que representan 
  el mismo evento economico dos veces.

  Conceptos que deberian estar en 'ajustes' como eventos economicos:
    - Ajuste por Talla/Garantia (evento raiz postventa)
    - Ajuste por Arrepentimiento (evento raiz postventa)
    - Ajuste por Falla en Entrega (evento raiz postventa)
    - Ajuste por Retraso en Entrega
    - Ajuste por Producto Danado/Vacio
    - (otros eventos postventa con impacto cash real)

  Conceptos que deberian estar SOLO en trazabilidad/auditoria:
    - Ajuste por Compra Protegida (BPP) -> mecanismo, no evento
    - Ajuste Poscobro Conciliado -> mecanismo, no evento
    - Ajuste Poscobro General -> mecanismo, no evento

  Impacto de la reclasificacion:
    - Abril 2025:  $259,180 de inflacion documental (0.39% del RN)
    - Octubre 2025: $283,878 de inflacion documental (0.40% del RN)
    - All-time ML:  $2,202,507 de inflacion documental (0.26% del RN)

PREGUNTA 2:
  Puede certificarse para Shopify?

RESPUESTA:
  FAIL condicional — NO en estado actual.

  Shopify requiere que cada transaccion represente un evento economico 
  unico. La presencia de mecanismos de ejecucion (BPP, Poscobro) que 
  duplican eventos economicos REALES es incompatible con:
    - Single Source of Truth contable
    - Auditoria financiera GAAP/IFRS
    - Trail balance sin inflacion documental

  La certificacion Shopify requeria:
    1. Separar Eventos Economicos de Mecanismos de Ejecucion
    2. Crear categoria 'Eventos Postventa' en el P&L
    3. Mover BPP y Poscobro a tabla de trazabilidad exclusivamente
    4. Asegurar que Resultado Neto refleje SOLO eventos unicos

  Con las correcciones descritas en FASE 3-4, el modelo ECONOMICO 
  si seria certificable.

MATRIZ FINAL:
""")

print(f"  {'Concepto':55s} {'Evento':12s} {'Mecanismo':12s} {'P&L':6s} {'Audit':6s}")
print(f"  {'-'*55} {'-'*12} {'-'*12} {'-'*6} {'-'*6}")
for concept, cls_data in sorted(classifications.items(), key=lambda x: (x[1][0], -abs(x[1][4]))):
    cls_name, detail, show_pnl, show_audit, total, records, orders = cls_data
    is_event = "SI" if "Evento" in cls_name else "NO"
    is_mech = "SI" if "Mecanismo" in cls_name else "NO"
    pnl_str = "SI" if show_pnl else "NO"
    aud_str = "SI" if show_audit else "NO"
    print(f"  {concept:55s} {is_event:12s} {is_mech:12s} {pnl_str:6s} {aud_str:6s}")

db.close()
print("\nDone.")
