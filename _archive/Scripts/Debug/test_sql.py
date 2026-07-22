import requests, urllib.parse
sql = """SELECT COALESCE(c.financial_group, 'sin_clasificar') as financial_group, l.detalle, l.tipo_movimiento, c.clasificacion_operativa, l.monto, l.monto_bruto, l.comision_marketplace FROM marketplace_ledger_v1 l LEFT JOIN marketplace_ledger_clasificado_v1 c ON l.marketplace = c.marketplace AND l.id_transaccion = c.id_transaccion WHERE l.marketplace = 'PARIS' AND c.financial_group IS NOT NULL AND COALESCE(c.include_in_operational_pnl, TRUE) = TRUE LIMIT 5"""
q = urllib.parse.quote(sql)
print(requests.get(f'http://127.0.0.1:8003/api/v4/debug/query?query={q}').text)
