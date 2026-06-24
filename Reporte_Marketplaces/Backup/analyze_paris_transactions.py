import pandas as pd
import numpy as np

def analyze_paris_transactions(file_path):
    """
    Analiza el archivo de transacciones de París para identificar nuevos tipos de transacción 
    y verificar la lógica de cálculo de la comisión.
    """
    try:
        # Leer el archivo Excel. Asumo que la hoja es la primera o la única.
        df = pd.read_excel(file_path)
        
        # Convertir nombres de columna a mayúsculas para asegurar la coincidencia
        df.columns = [col.upper() for col in df.columns]
        
        # 1. Identificar valores únicos en la columna 'TIPO'
        if 'TIPO' in df.columns:
            unique_types = df['TIPO'].astype(str).unique()
            unique_types_output = "\n".join(sorted(unique_types))
            
            # 2. Verificar la lógica de la comisión
            # Buscamos filas donde 'TIPO' sea 'VENTA' o similar, y donde 'COMISION' y 'MONTO' existan.
            commission_check = df[df['TIPO'].str.contains('VENTA', na=False)]
            
            # Asumo que 'MONTO' es el valor de la venta y 'COMISION' es el porcentaje.
            # El valor de la comisión debería ser MONTO * COMISION_PORCENTAJE / 100
            
            # Creamos una columna para el valor de la comisión calculado
            commission_check['COMISION_CALCULADA'] = commission_check['MONTO'] * commission_check['COMISION'] / 100
            
            # Buscamos la columna que contiene el valor de la comisión real (puede ser 'MONTO_A_PAGAR' o similar)
            # Como no tengo el nombre exacto de la columna de la comisión real, buscaré columnas que contengan 'COMISION' o 'PAGAR'
            
            commission_value_col = [col for col in df.columns if 'COMISION' in col or 'PAGAR' in col]
            
            analysis_output = f"Valores únicos en la columna 'TIPO':\n{unique_types_output}\n\n"
            analysis_output += "Columnas relacionadas con la comisión o pago:\n"
            analysis_output += ", ".join(commission_value_col) + "\n\n"
            
            # Si existe una columna de valor de comisión, la comparamos
            if 'MONTO_A_PAGAR' in df.columns and 'MONTO' in df.columns and 'COMISION' in df.columns:
                # El monto a pagar es MONTO - COMISION_CALCULADA - otros cargos
                # Para simplificar, solo mostraremos una muestra de la relación entre MONTO, COMISION y MONTO_A_PAGAR
                
                sample_data = commission_check[['MONTO', 'COMISION', 'COMISION_CALCULADA', 'MONTO_A_PAGAR']].head(5)
                analysis_output += "Muestra de cálculo de comisión (MONTO * COMISION %):\n"
                analysis_output += sample_data.to_string()
            
            # Guardar los resultados en un archivo de texto
            output_path = "/home/ubuntu/paris_analysis_results.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(analysis_output)
            
            print(f"Análisis completado. Resultados guardados en {output_path}")
        else:
            print("Error: La columna 'TIPO' no se encontró en el archivo.")
            
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta: {file_path}")
    except Exception as e:
        print(f"Ocurrió un error durante el procesamiento: {e}")

# Ruta del archivo proporcionado por el usuario
file_path = "/home/ubuntu/upload/transactions_report_20251202_30918256.xlsx"
analyze_paris_transactions(file_path)
