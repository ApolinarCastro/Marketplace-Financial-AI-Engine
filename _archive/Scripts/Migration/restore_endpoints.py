import re

with open('api/api.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoints = '''
@app.get("/api/v4/exec/ux12_summary")
def get_exec_ux12_summary(periodo: str | None = None, marketplace: str | None = None):
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    if date_end is None:
        mx = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx_val = mx.iloc[0]['mx']
        import pandas as pd
        if pd.notna(mx_val):
            mx_dt = pd.to_datetime(mx_val)
            import calendar
            last_day = calendar.monthrange(mx_dt.year, mx_dt.month)[1]
            ytd_end = f"{mx_dt.year}-{mx_dt.month:02d}-{last_day}"
        else:
            ytd_end = date_start
        dt_where, dt_params = "periodo_inicio >= ? AND periodo_fin <= ?", [date_start, ytd_end]
        ld_where, ld_params = "fecha >= ?", [date_start]
    else:
        dt_where, dt_params = "periodo_inicio >= ? AND periodo_fin <= ?", [date_start, date_end]
        ld_where, ld_params = "fecha BETWEEN ? AND ?", [date_start, date_end]

    if marketplace and marketplace.upper() != 'ALL':
        ld_where += " AND marketplace = ?"
        ld_params.append(marketplace.upper())

    ledger_pnl = db.query(f"""
        SELECT 
            COALESCE(SUM(CASE WHEN financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as gross,
            COALESCE(SUM(CASE WHEN financial_group='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as returns,
            COALESCE(SUM(CASE WHEN financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes', 'recuperaciones_y_bonificaciones') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costs
        FROM marketplace_ledger_v1
        WHERE {ld_where}
    """, ld_params)
    
    gross_sales = float(ledger_pnl.iloc[0]['gross'])
    returns = float(ledger_pnl.iloc[0]['returns'])
    marketplace_costs = float(ledger_pnl.iloc[0]['costs'])
    net_profit = gross_sales + returns + marketplace_costs

    cash_flow = {
        "available_balance": net_profit,
        "releases": 0,
        "holds": 0,
        "transfers": 0
    }

    return_reasons_df = db.query(f"""
        SELECT detalle, COUNT(*) as casos, SUM(monto) as total_monto 
        FROM marketplace_ledger_v1 
        WHERE financial_group = 'devoluciones' AND {ld_where} 
        GROUP BY detalle 
        ORDER BY total_monto ASC LIMIT 5
    """, ld_params)
    
    total_devoluciones = returns if returns != 0 else 1 # avoid div by zero
    
    return_reasons = []
    for _, r in return_reasons_df.iterrows():
        monto = float(r['total_monto'])
        participacion = abs(monto / total_devoluciones) * 100 if total_devoluciones < 0 else 0
        r_detalle = str(r['detalle'])
        
        # Get top SKUs affected
        det_params = list(ld_params)
        det_params.append(r_detalle)
        products_df = db.query(f"""
            SELECT v.sku, COUNT(c.id_transaccion) as p_casos 
            FROM marketplace_ledger_v1 c
            JOIN ventas_marketplace v ON c.id_orden = v.order_id
            WHERE c.financial_group = 'devoluciones' AND {ld_where.replace('fecha', 'c.fecha').replace('marketplace', 'c.marketplace')} AND c.detalle = ? AND v.sku != 'UNKNOWN'
            GROUP BY v.sku
            ORDER BY p_casos DESC LIMIT 3
        """, det_params)
        
        top_products = [str(pr['sku']) for _, pr in products_df.iterrows()]
        
        return_reasons.append({
            "reason": r_detalle,
            "cases": int(r['casos']),
            "impact": monto,
            "participation": round(participacion, 1),
            "top_products": top_products
        })

    ai_narrative = []
    mp_text = marketplace if marketplace and marketplace != 'ALL' else "Todos los Marketplaces"
    if return_reasons:
        principal = return_reasons[0]
        ai_narrative.append(f"El principal motivo operativo de {mp_text} corresponde a {principal['reason']}.")
        ai_narrative.append(f"Representa el {principal['participation']:.1f}% del impacto económico del período.")
        ai_narrative.append(f"Generó un impacto de ${abs(principal['impact']):,.0f}.")
        ai_narrative.append(f"Afectó a {principal['cases']} operaciones.")
        if principal["top_products"]:
            ai_narrative.append(f"Mostrando concentración en productos/SKU como: {', '.join(principal['top_products'][:3])}.")
    else:
        ai_narrative.append(f"No se registraron incidencias operativas para {mp_text} en este período.")

    return {
        "period": label,
        "financial_pnl": {
            "gross_sales": gross_sales,
            "returns": returns,
            "marketplace_costs": marketplace_costs,
            "net_profit": net_profit
        },
        "cash_flow": cash_flow,
        "operational_intelligence": {
            "top_return_reasons": return_reasons,
            "delivery_incidents": 0,
            "chargeback_incidents": 0,
            "ai_narrative": ai_narrative
        }
    }

@app.get("/api/v4/exec/operational_intelligence")
def get_exec_operational_intelligence(periodo: str | None = None, marketplace: str | None = None):
    return get_exec_ux12_summary(periodo, marketplace).get("operational_intelligence", {})
'''

# Remove any existing implementation if it accidentally matches
content = re.sub(r'@app\.get\("/api/v4/exec/ux12_summary"\).*?def get_exec_ux12_summary.*?(?=@app\.get|$)', '', content, flags=re.DOTALL)
content = re.sub(r'@app\.get\("/api/v4/exec/operational_intelligence"\).*?def get_exec_operational_intelligence.*?(?=@app\.get|$)', '', content, flags=re.DOTALL)

with open('api/api.py', 'w', encoding='utf-8') as f:
    f.write(content + "\n" + new_endpoints)
