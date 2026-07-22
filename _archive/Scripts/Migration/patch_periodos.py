import codecs

code = '''import calendar

def _resolve_period_range(periodo: str | None) -> tuple:
    if not periodo or periodo.upper() == 'YTD':
        db = DatabaseV4.get()
        latest = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx = latest.iloc[0]['mx']
        import pandas as pd
        if pd.notna(mx):
            mx = pd.to_datetime(mx)
            return (f"{mx.year}-01-01", None, f"{mx.year}-YTD")
        return ("2026-01-01", None, "2026-YTD")
    year, month = periodo.split('-')
    y, m = int(year), int(month)
    last_day = calendar.monthrange(y, m)[1]
    return (f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last_day}", periodo)

_MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

@app.get("/api/v4/periodos")
def get_periodos():
    db = DatabaseV4.get()
    import pandas as pd
    df = db.query("""
        SELECT DISTINCT periodo_inicio
        FROM marketplace_cierre_financiero_v1
        WHERE resultado_neto != 0
        ORDER BY periodo_inicio DESC
    """)
    periodos = [{"value": "YTD", "label": "Year to Date"}]
    for _, r in df.iterrows():
        p = pd.to_datetime(r['periodo_inicio'])
        label = f"{_MONTHS[p.month - 1]} {p.year}"
        periodos.append({"value": f"{p.year}-{p.month:02d}", "label": label})
    return periodos
'''

with codecs.open('api/api.py', 'r', 'utf-8') as f:
    content = f.read()

if 'def get_periodos()' not in content:
    with codecs.open('api/api.py', 'a', 'utf-8') as f:
        f.write('\n' + code + '\n')
