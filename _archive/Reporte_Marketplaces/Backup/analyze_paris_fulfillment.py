import pandas as pd

def analyze_paris_fulfillment(file_path):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path)
        
        # Mostrar las primeras filas y las columnas para el análisis
        print("--- Columnas de París Fulfillment ---")
        print(df.columns.tolist())
        print("\n--- Primeras 5 filas ---")
        print(df.head().to_markdown(index=False))
        
        # Identificar las columnas clave para Venta, Costos y Devoluciones
        # Asumiendo que las columnas de interés son las que contienen "venta", "costo", "comisión", "despacho", "logística"
        
        relevant_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ["venta", "costo", "comisión", "despacho", "logística", "monto", "tipo"])]
        
        print("\n--- Columnas Relevantes para Hechos ---")
        print(relevant_cols)
        
        # Conclusión de la lógica de hechos
        print("\n--- Lógica de Hechos (Inferencia) ---")
        print("Este archivo parece ser un reporte de transacciones detallado, similar al RAW de París, pero específico para Fulfillment.")
        print("Se usará la columna 'TIPO' para clasificar las transacciones de Venta y Costos de Fulfillment.")
        
    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")

analyze_paris_fulfillment("/home/ubuntu/upload/transactions_report_20251206_52376863.xlsx")
