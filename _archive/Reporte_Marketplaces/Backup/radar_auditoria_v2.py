import pandas as pd
import os

def run_radar():
    results = []
    
    # 1. Analizar París
    paris_file = "/home/ubuntu/upload/transactions_report_20251202_30918256.xlsx"
    # Términos conocidos (normalizados a minúsculas para comparar)
    paris_known = [x.lower() for x in ["Venta", "Comisión", "Despacho", "Cobro por despacho", "Logística inversa", "Compensación logística", "Cargo", "Cobro por campaña", "Rebate", "Devolución"]]
    
    if os.path.exists(paris_file):
        df_paris = pd.read_excel(paris_file)
        # El archivo parece tener columnas en minúsculas
        col_name = 'tipo' if 'tipo' in df_paris.columns else 'TIPO'
        if col_name in df_paris.columns:
            # Convertimos a string y quitamos espacios para comparar
            df_paris[col_name] = df_paris[col_name].astype(str).str.strip()
            unknown_paris = df_paris[~df_paris[col_name].str.lower().isin(paris_known)][col_name].unique()
            for item in unknown_paris:
                results.append({"Marketplace": "París", "Concepto_Desconocido": item})
        else:
            results.append({"Marketplace": "París", "Error": f"Columna 'tipo' no encontrada."})

    # 2. Analizar Ripley
    ripley_file = "/home/ubuntu/upload/Historial_Nov2025.csv"
    ripley_known = [x.lower() for x in ["Importe del pedido", "Comisiones", "Gastos de envío (RIPLEY)", "Impuesto sobre la comisión (IVA 0,00%)", "Importe de reembolso", "Abono manual", "Factura manual"]]
    
    if os.path.exists(ripley_file):
        try:
            # Intentamos leer con separador punto y coma si falla el coma
            df_ripley = pd.read_csv(ripley_file, sep=None, engine='python')
            col_name = 'Tipo' if 'Tipo' in df_ripley.columns else 'tipo'
            if col_name in df_ripley.columns:
                df_ripley[col_name] = df_ripley[col_name].astype(str).str.strip()
                unknown_ripley = df_ripley[~df_ripley[col_name].str.lower().isin(ripley_known)][col_name].unique()
                for item in unknown_ripley:
                    results.append({"Marketplace": "Ripley", "Concepto_Desconocido": item})
            else:
                results.append({"Marketplace": "Ripley", "Error": f"Columna 'Tipo' no encontrada."})
        except Exception as e:
            results.append({"Marketplace": "Ripley", "Error": str(e)})

    # Guardar resultados
    pd.DataFrame(results).to_csv("/home/ubuntu/hallazgos_radar_v2.csv", index=False)
    print("Radar V2 ejecutado con éxito.")

if __name__ == "__main__":
    run_radar()
