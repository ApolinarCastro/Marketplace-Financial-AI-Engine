import sys

content = open('api/api.py', 'r', encoding='utf-8').read()

missing_code = '''
import calendar

_MONTHS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def _resolve_period_range(periodo: str | None) -> tuple:
    import pandas as pd
    from engine.v4.database import DatabaseV4
    if not periodo or periodo.upper() == 'YTD':
        db = DatabaseV4.get()
        import pandas as pd
        df = db.query('SELECT MAX(periodo_inicio) as max_p FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0')
        if not df.empty and pd.notna(df.iloc[0]['max_p']):
            mx = pd.to_datetime(df.iloc[0]['max_p'])
            return f'{mx.year}-01-01', None, 'Year to Date'
        else:
            return '2024-01-01', None, 'Year to Date'
    
    try:
        y, m = map(int, periodo.split('-'))
        last_day = calendar.monthrange(y, m)[1]
        start_date = f'{y}-{m:02d}-01'
        end_date = f'{y}-{m:02d}-{last_day}'
        label = f'{_MONTHS[m - 1]} {y}'
        return start_date, end_date, label
    except:
        return '2024-01-01', None, 'Year to Date'
'''

if '_MONTHS = [' not in content:
    content = content.replace('@app.get("/api/v4/periodos")', missing_code + '\n@app.get("/api/v4/periodos")')
    
    old_for_loop = '''for _, r in df.iterrows():
        p = pd.to_datetime(r['periodo_inicio'])
        label = f"{_MONTHS[p.month - 1]} {p.year}"'''
        
    new_for_loop = '''for _, r in df.iterrows():
        p = pd.to_datetime(r['periodo_inicio'])
        if pd.isna(p):
            continue
        label = f"{_MONTHS[p.month - 1]} {p.year}"'''
        
    content = content.replace(old_for_loop, new_for_loop)
    
    with open('api/api.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed api.py')
else:
    print('Already fixed')
