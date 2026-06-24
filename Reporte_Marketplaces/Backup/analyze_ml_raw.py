import pandas as pd

def analyze_ml_raw(file_path):
    """
    Lee el archivo ML_Facturacion_RAW.xlsx y extrae los valores únicos 
    de la columna 'Detalle'.
    """
    try:
        # Leer el archivo Excel. Asumo que la hoja es la primera o la única.
        df = pd.read_excel(file_path)
        
        # Convertir los nombres de columna a mayúsculas para asegurar la coincidencia
        df.columns = [col.upper() for col in df.columns]
        
        # Extraer valores únicos de la columna 'DETALLE'
        if 'DETALLE' in df.columns:
            unique_details = df['DETALLE'].astype(str).unique()
            
            # Ordenar alfabéticamente para facilitar la revisión
            unique_details_sorted = sorted(unique_details)
            
            # Guardar los resultados en un archivo de texto
            output_path = "/home/ubuntu/unique_ml_details.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("Valores únicos de la columna 'Detalle' en ML_Facturacion_RAW:\n\n")
                for detail in unique_details_sorted:
                    f.write(f"{detail}\n")
            
            print(f"Análisis completado. Resultados guardados en {output_path}")
        else:
            print("Error: La columna 'Detalle' no se encontró en el archivo.")
            
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta: {file_path}")
    except Exception as e:
        print(f"Ocurrió un error durante el procesamiento: {e}")

# Ruta del archivo proporcionado por el usuario
file_path = "/home/ubuntu/upload/ML_Facturacion_RAW.xlsx"
analyze_ml_raw(file_path)
