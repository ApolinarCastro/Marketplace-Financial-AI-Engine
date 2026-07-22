import re

with open('api/api.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = '''@app.get("/api/v4/cierre/desglose")
def get_marketplace_cierre_desglose(
    marketplace: str = "ML", 
    periodo: str | None = None,
    exclude_non_operational: bool = False
):
    db = DatabaseV4.get()

    if not periodo or periodo in ["ALL", "YTD"]:
        p_ini = "2000-01-01"
        p_fin = "2100-12-31"
    else:
        year, month = periodo.split("-")
        import calendar
        last_day = calendar.monthrange(int(year), int(month))[1]
        p_ini = f"{year}-{month}-01"
        p_fin = f"{year}-{month}-{last_day}"

    exclude_clause = ""
    if exclude_non_operational:
        exclude_clause = " AND COALESCE(c.include_in_operational_pnl, 1) = 1"

    sql = f"""
        SELECT 
            COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
            l.detalle,
            l.tipo_movimiento,
            c.clasificacion_operativa,
            CASE 
                   WHEN l.id_transaccion LIKE 'RIP_TH_%' THEN 'TH'
                   WHEN l.id_transaccion LIKE 'RIP_FF_%' THEN 'FF'
                   WHEN l.id_transaccion LIKE 'RIP_CSV_%' THEN 'CICLOS'
                   WHEN l.archivo_origen LIKE '%.xlsx' THEN 'SELLER'
                   WHEN l.archivo_origen LIKE '%.xml' THEN 'XML'
                   ELSE 'OTRO'
            END as origen_capa,
            CASE 
                   WHEN l.id_transaccion LIKE 'RIP_TH_%' THEN 'TRANSACTION'
                   WHEN l.id_transaccion LIKE 'RIP_FF_%' THEN 'LOGISTICS'
                   WHEN l.id_transaccion LIKE 'RIP_CSV_%' THEN 'SETTLEMENT'
                   WHEN l.archivo_origen LIKE '%.xlsx' THEN 'OPERATIONAL'
                   WHEN l.archivo_origen LIKE '%.xml' THEN 'TAX'
                   ELSE 'UNKNOWN'
            END as truth_type,
            SUM(COALESCE(l.monto, 0)) as total,
            COUNT(*) as cantidad
        FROM marketplace_ledger_v1 l
        LEFT JOIN marketplace_ledger_clasificado_v1 c
               ON l.marketplace = c.marketplace 
             AND l.id_transaccion = c.id_transaccion
        WHERE l.marketplace = ?
          AND l.fecha BETWEEN ? AND ?
          {exclude_clause}
          AND COALESCE(c.financial_group, 'sin_clasificar') NOT IN ('tesoreria', 'recuperaciones_y_bonificaciones')
        GROUP BY c.financial_group, l.detalle, l.tipo_movimiento, c.clasificacion_operativa, origen_capa, truth_type
        ORDER BY total ASC
    """
    
    df = db.query(sql, [marketplace, p_ini, p_fin])

    records = []
    for _, row in df.iterrows():
        r_detalle = str(row['detalle']) if not pd.isna(row['detalle']) else ""
        r_clasificacion = str(row['clasificacion_operativa']) if not pd.isna(row['clasificacion_operativa']) else r_detalle
        r_total = float(row['total'])
        
        if marketplace == 'PARIS' and r_detalle == 'Venta':
            pass
            
        records.append({
            "detalle": f"{r_detalle} [{row['origen_capa']}][{row['truth_type']}]" if marketplace == 'RIPLEY' else r_detalle,
            "clasificacion_operativa": r_clasificacion,
            "tipo_movimiento": row['tipo_movimiento'],
            "total": r_total,
            "cantidad": int(row['cantidad']),
            "categoria": str(row['financial_group']),
            "origen_capa": row['origen_capa'],
            "truth_type": row['truth_type'],
            "is_legacy_360": True
        })

    if marketplace == 'PARIS':
        sql_paris = f"""
            SELECT 
                COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
                l.detalle,
                l.tipo_movimiento,
                c.clasificacion_operativa,
                l.monto, l.monto_bruto, l.comision_marketplace,
                CASE 
                       WHEN l.archivo_origen LIKE '%.xlsx' THEN 'SELLER'
                       ELSE 'OTRO'
                END as origen_capa,
                CASE 
                       WHEN l.archivo_origen LIKE '%.xlsx' THEN 'OPERATIONAL'
                       ELSE 'UNKNOWN'
                END as truth_type
            FROM marketplace_ledger_v1 l
            LEFT JOIN marketplace_ledger_clasificado_v1 c
                   ON l.marketplace = c.marketplace 
                 AND l.id_transaccion = c.id_transaccion
            WHERE l.marketplace = ?
              AND l.fecha BETWEEN ? AND ?
              {exclude_clause}
              AND COALESCE(c.financial_group, 'sin_clasificar') NOT IN ('tesoreria', 'recuperaciones_y_bonificaciones')
        """
        df_p = db.query(sql_paris, [marketplace, p_ini, p_fin])
        
        agg = {}
        for _, row in df_p.iterrows():
            fg = row['financial_group']
            det = row['detalle']
            tm = row['tipo_movimiento']
            co = row['clasificacion_operativa']
            monto = row['monto']
            bruto = row['monto_bruto']
            com = row['comision_marketplace']
            oc = row['origen_capa']
            tt = row['truth_type']
            
            if det == 'Venta':
                key_venta = (fg, det, tm, 'Venta Bruta', oc, tt)
                agg[key_venta] = agg.get(key_venta, 0.0) + float(bruto if pd.notna(bruto) else monto)
                if pd.notna(com) and float(com) > 0:
                    key_com = ('costos_comerciales', 'Comisión Marketplace', 'egreso', 'Comisión Marketplace', oc, tt)
                    agg[key_com] = agg.get(key_com, 0.0) - float(com)
            else:
                key = (fg, det, tm, co, oc, tt)
                agg[key] = agg.get(key, 0.0) + float(monto)
                
        records = []
        for k, v in agg.items():
            records.append({
                "categoria": k[0],
                "detalle": k[1],
                "tipo_movimiento": k[2],
                "clasificacion_operativa": k[3],
                "total": v,
                "cantidad": 1,
                "origen_capa": k[4],
                "truth_type": k[5],
                "is_legacy_360": True
            })

    # RIPLEY taxonomy mapping fallback
    if marketplace == 'RIPLEY':
        for r in records:
            cat = str(r.get('clasificacion_operativa', ''))
            if cat.upper() == 'COMISIONES':
                r['categoria'] = 'costos_comerciales'
            elif cat.upper() == 'DEVOLUCIONES':
                r['categoria'] = 'devoluciones'
            elif 'DESPACHO' in cat.upper():
                r['categoria'] = 'costos_operacionales'
            elif cat.upper() == 'VENTAS':
                r['categoria'] = 'ingresos'

    return records'''

# Replace the old function
content = re.sub(
    r'@app\.get\("/api/v4/cierre/desglose"\)\ndef get_marketplace_cierre_desglose.*?return records',
    new_func,
    content,
    flags=re.DOTALL
)

with open('api/api.py', 'w', encoding='utf-8') as f:
    f.write(content)
