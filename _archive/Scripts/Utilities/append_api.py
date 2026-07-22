import os

append_content = """

@app.get("/api/v4/exec/summary-v3")
def get_exec_summary_v3(periodo: str | None = None, marketplace: str | None = None):
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    mp_filter = ""
    mp_params: list = []
    if marketplace and marketplace.upper() != 'ALL':
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace.upper()]

    if date_end is None:
        mx = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx_val = mx.iloc[0]['mx']
        if pd.notna(mx_val):
            mx_dt = pd.to_datetime(mx_val)
            import calendar
            last_day = calendar.monthrange(mx_dt.year, mx_dt.month)[1]
            ytd_end = f"{mx_dt.year}-{mx_dt.month:02d}-{last_day}"
        else:
            ytd_end = date_start
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params

    # 1. CAPA OPERACIONAL
    q_op_mp = f\"\"\"
        SELECT COALESCE(SUM(monto), 0) as total
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%.xlsx'
          AND detalle IN ('Precio total', 'Importe del pedido', 'order_amount', 'Subtotal')
          AND {ld_where}
    \"\"\"
    venta_mp = float(db.query(q_op_mp, ld_params).iloc[0]['total'])

    q_op_ff = f\"\"\"
        SELECT COALESCE(SUM(monto), 0) as total
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%ff%.csv'
          AND detalle IN ('transfer_amount')
          AND {ld_where}
    \"\"\"
    venta_ff = float(db.query(q_op_ff, ld_params).iloc[0]['total'])

    q_ord_mp = f\"\"\"
        SELECT COUNT(DISTINCT id_orden) as total
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%.xlsx' AND {ld_where}
    \"\"\"
    ordenes_mp = int(db.query(q_ord_mp, ld_params).iloc[0]['total'])

    q_ord_ff = f\"\"\"
        SELECT COUNT(DISTINCT id_orden) as total
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%ff%.csv' AND {ld_where}
    \"\"\"
    ordenes_ff = int(db.query(q_ord_ff, ld_params).iloc[0]['total'])

    # 2. CAPA LIQUIDACION
    q_liq = f\"\"\"
        SELECT 
            SUM(CASE WHEN detalle='Subtotal' THEN monto ELSE 0 END) as venta_liquidada,
            SUM(CASE WHEN detalle='Comisión' THEN monto ELSE 0 END) as comision_liquidada,
            SUM(CASE WHEN detalle='Amount transferred to tienda' THEN monto ELSE 0 END) as liquidacion_neta,
            SUM(CASE WHEN detalle NOT IN ('Subtotal', 'Comisión', 'Amount transferred to tienda') THEN monto ELSE 0 END) as ajustes_liquidacion
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%-%-%-%-%' AND archivo_origen LIKE '%.csv'
          AND {ld_where}
    \"\"\"
    liq_df = db.query(q_liq, ld_params)
    liq = liq_df.iloc[0] if not liq_df.empty else pd.Series({'venta_liquidada':0, 'comision_liquidada':0, 'liquidacion_neta':0, 'ajustes_liquidacion':0})
    
    # 3. CAPA TESORERIA
    q_tes = f\"\"\"
        SELECT 
            SUM(CASE WHEN financial_group='tesoreria' THEN monto ELSE 0 END) as disponible,
            SUM(CASE WHEN financial_group='tesoreria' AND detalle LIKE '%transferencia%' THEN monto ELSE 0 END) as transferencias,
            SUM(CASE WHEN financial_group='tesoreria' AND detalle LIKE '%pago%' THEN monto ELSE 0 END) as pagos_recibidos
        FROM marketplace_ledger_v1
        WHERE {ld_where}
    \"\"\"
    tes_df = db.query(q_tes, ld_params)
    tes = tes_df.iloc[0] if not tes_df.empty else pd.Series({'disponible':0, 'transferencias':0, 'pagos_recibidos':0})
    
    return {
        "period": label,
        "marketplace": marketplace or "ALL",
        "operacional": {
            "venta_mp": venta_mp,
            "venta_ff": venta_ff,
            "venta_operacional_consolidada": venta_mp + venta_ff,
            "ordenes_mp": ordenes_mp,
            "ordenes_ff": ordenes_ff
        },
        "liquidacion": {
            "venta_liquidada": float(liq['venta_liquidada'] if pd.notna(liq['venta_liquidada']) else 0),
            "comision_liquidada": float(liq['comision_liquidada'] if pd.notna(liq['comision_liquidada']) else 0),
            "ajustes_liquidacion": float(liq['ajustes_liquidacion'] if pd.notna(liq['ajustes_liquidacion']) else 0),
            "liquidacion_neta": float(liq['liquidacion_neta'] if pd.notna(liq['liquidacion_neta']) else 0)
        },
        "tesoreria": {
            "disponible": float(tes['disponible'] if pd.notna(tes['disponible']) else 0),
            "transferencias": float(tes['transferencias'] if pd.notna(tes['transferencias']) else 0),
            "pagos_recibidos": float(tes['pagos_recibidos'] if pd.notna(tes['pagos_recibidos']) else 0)
        }
    }

@app.get("/api/v4/exec/waterfall-v3")
def get_exec_waterfall_v3(marketplace: str | None = None, periodo: str | None = None):
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    mp_filter = ""
    mp_params: list = []
    if marketplace and marketplace.upper() != 'ALL':
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace.upper()]

    if date_end is None:
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params

    # Waterfall Operacional (Seller + FF)
    q_op = f\"\"\"
        SELECT
            SUM(CASE WHEN archivo_origen LIKE '%.xlsx' AND detalle IN ('Precio total', 'Importe del pedido', 'order_amount') THEN monto ELSE 0 END) as venta_seller,
            SUM(CASE WHEN archivo_origen LIKE '%ff%.csv' AND detalle='transfer_amount' THEN monto ELSE 0 END) as venta_ff,
            SUM(CASE WHEN archivo_origen LIKE '%.xlsx' AND financial_group='devoluciones' THEN monto ELSE 0 END) as devoluciones_seller,
            SUM(CASE WHEN (archivo_origen LIKE '%ff%.csv' OR archivo_origen LIKE '%.xlsx') AND financial_group IN ('costos_operacionales', 'costos_comerciales') THEN monto ELSE 0 END) as costos_op
        FROM marketplace_ledger_v1
        WHERE {ld_where}
    \"\"\"
    op_df = db.query(q_op, ld_params)
    r_op = op_df.iloc[0] if not op_df.empty else pd.Series({'venta_seller':0, 'venta_ff':0, 'devoluciones_seller':0, 'costos_op':0})

    # Waterfall Liquidacion (Ciclos)
    q_liq = f\"\"\"
        SELECT 
            SUM(CASE WHEN detalle='Subtotal' THEN monto ELSE 0 END) as subtotal,
            SUM(CASE WHEN detalle='Comisión' THEN monto ELSE 0 END) as comisiones,
            SUM(CASE WHEN detalle NOT IN ('Subtotal', 'Comisión', 'Amount transferred to tienda') THEN monto ELSE 0 END) as ajustes,
            SUM(CASE WHEN detalle='Amount transferred to tienda' THEN monto ELSE 0 END) as pago_neto
        FROM marketplace_ledger_v1
        WHERE archivo_origen LIKE '%-%-%-%-%' AND archivo_origen LIKE '%.csv'
          AND {ld_where}
    \"\"\"
    liq_df = db.query(q_liq, ld_params)
    r_liq = liq_df.iloc[0] if not liq_df.empty else pd.Series({'subtotal':0, 'comisiones':0, 'ajustes':0, 'pago_neto':0})

    return {
        "period": label,
        "marketplace": marketplace or "ALL",
        "operacional": {
            "labels": ["Venta MP", "Venta FF", "Devoluciones MP", "Costos Op y Com"],
            "values": [
                float(r_op['venta_seller'] if pd.notna(r_op['venta_seller']) else 0), 
                float(r_op['venta_ff'] if pd.notna(r_op['venta_ff']) else 0), 
                float(r_op['devoluciones_seller'] if pd.notna(r_op['devoluciones_seller']) else 0), 
                float(r_op['costos_op'] if pd.notna(r_op['costos_op']) else 0)
            ],
            "neto": float((r_op['venta_seller'] if pd.notna(r_op['venta_seller']) else 0) + (r_op['venta_ff'] if pd.notna(r_op['venta_ff']) else 0) + (r_op['devoluciones_seller'] if pd.notna(r_op['devoluciones_seller']) else 0) + (r_op['costos_op'] if pd.notna(r_op['costos_op']) else 0))
        },
        "liquidacion": {
            "labels": ["Subtotal Liquidado", "Comisiones", "Ajustes"],
            "values": [
                float(r_liq['subtotal'] if pd.notna(r_liq['subtotal']) else 0), 
                float(r_liq['comisiones'] if pd.notna(r_liq['comisiones']) else 0), 
                float(r_liq['ajustes'] if pd.notna(r_liq['ajustes']) else 0)
            ],
            "neto": float(r_liq['pago_neto'] if pd.notna(r_liq['pago_neto']) else 0)
        }
    }
"""

with open('api/api.py', 'a', encoding='utf-8') as f:
    f.write(append_content)
