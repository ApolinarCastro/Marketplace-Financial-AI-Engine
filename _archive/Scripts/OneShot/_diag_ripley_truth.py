import pandas as pd
import glob
import json

def get_columns(file_path):
    if file_path.endswith('.csv'):
        # Try multiple encodings
        for enc in ['utf-8', 'latin1', 'utf-16']:
            try:
                df = pd.read_csv(file_path, nrows=5, encoding=enc, sep=None, engine='python')
                if len(df.columns) > 1:
                    return list(df.columns)
            except Exception:
                pass
        return []
    elif file_path.endswith('.xlsx'):
        try:
            df = pd.read_excel(file_path, nrows=5)
            return list(df.columns)
        except Exception:
            return []
    return []

def main():
    res = {}
    
    # 1. Historial
    h = glob.glob('01_Raw/RIPLEY/Resumen financiero/Historial de transacciones/*.csv')
    if h: res['Historial'] = get_columns(h[0])
    
    # 2. Ciclos
    c = glob.glob('01_Raw/RIPLEY/Resumen financiero/Ciclos de facturación/*.csv')
    if c: res['Ciclos'] = get_columns(c[0])
    
    # 3. Seller
    s = glob.glob('01_Raw/RIPLEY/Resumen financiero/Seller/*.xlsx')
    if s: res['Seller'] = get_columns(s[0])
    
    # 4. Fulfillment
    f = glob.glob('01_Raw/RIPLEY/Resumen financiero/Fulfillment/*.csv')
    if f: res['Fulfillment'] = get_columns(f[0])
    
    for k, v in res.items():
        print(f"--- {k} ---")
        for col in v:
            print(col)
        print()

if __name__ == '__main__':
    main()
