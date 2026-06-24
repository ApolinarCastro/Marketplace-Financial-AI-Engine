import pandas as pd

def analyze_ripley_orders(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, encoding='utf-8', sep=';')
        
        # Mostrar las primeras filas y la información de las columnas
        print("--- Primeras 5 filas del archivo de pedidos de Ripley ---")
        print(df.head().to_markdown(index=False, numalign="left", stralign="left"))
        print("\n--- Información de las columnas ---")
        df.info()
        
        # Columnas clave para aristas
        print("\n--- Valores únicos de la columna 'Estado' ---")
        print(df['Estado'].unique())
        
        print("\n--- Columnas numéricas clave (posibles aristas) ---")
        numeric_cols = ['Importe', 'Comision (sin impuestos)', 'Costo de envío', 'Importe de reembolso', 'Importe de devolución']
        for col in numeric_cols:
            if col in df.columns:
                print(f"- {col}")
                print(f"  - Suma: {df[col].sum()}")
                print(f"  - Conteo de valores > 0: {df[df[col] > 0].shape[0]}")
            else:
                print(f"- Columna '{col}' no encontrada.")

    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")

analyze_ripley_orders("/home/ubuntu/upload/orders_ENE_Nov2025.csv")
