import pandas as pd

def list_columns(file_path):
    """
    Lee el archivo Excel y lista todas las columnas.
    """
    try:
        df = pd.read_excel(file_path)
        # Convertir nombres de columna a mayúsculas para asegurar la coincidencia
        df.columns = [col.upper() for col in df.columns]
        
        output_path = "/home/ubuntu/paris_columns.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Columnas del archivo de París:\n")
            for col in df.columns:
                f.write(f"- {col}\n")
        
        print(f"Columnas listadas en {output_path}")
        
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta: {file_path}")
    except Exception as e:
        print(f"Ocurrió un error durante el procesamiento: {e}")

file_path = "/home/ubuntu/upload/transactions_report_20251202_30918256.xlsx"
list_columns(file_path)
