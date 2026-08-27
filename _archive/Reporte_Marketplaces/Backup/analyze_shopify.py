import pandas as pd

def analyze_shopify(file_path):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        
        # Mostrar las primeras filas y las columnas para el análisis
        print("--- Columnas de Shopify ---")
        print(df.columns.tolist())
        print("\n--- Primeras 5 filas ---")
        print(df.head().to_markdown(index=False))
        
        # Identificar las columnas clave para Venta, Costos y Devoluciones
        # Asumiendo que las columnas de interés son las que contienen "brutas", "descuento", "envío", "impuesto", "reembolso"
        
        relevant_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ["brutas", "descuento", "envío", "impuesto", "reembolso", "comisión", "neto"])]
        
        print("\n--- Columnas Relevantes para Hechos ---")
        print(relevant_cols)
        
        # Conclusión de la lógica de hechos
        print("\n--- Lógica de Hechos (Inferencia) ---")
        print("Venta Bruta: 'Ventas brutas'")
        print("Descuentos: 'Descuentos'")
        print("Envío: 'Costo de envío'")
        print("Impuestos: 'Impuestos'")
        print("Reembolsos: 'Reembolsos'")
        print("Ganancia Neta: 'Ventas netas'")
        
    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")

analyze_shopify("/home/ubuntu/upload/Ventasbrutasporpedido-2025-01-01-2025-11-30.csv")
