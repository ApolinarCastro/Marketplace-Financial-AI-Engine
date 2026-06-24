import pandas as pd
import os

def run_radar():
    results = []
    
    # 1. Analizar París
    paris_file = "/home/ubuntu/upload/transactions_report_20251202_30918256.xlsx"
    paris_known = ["Venta", "Comisión", "Despacho", "Cobro por despacho", "Logística inversa", "Compensación logística", "Cargo", "Cobro por campaña", "Rebate", "Devolución"]
    
    if os.path.exists(paris_file):
        df_paris = pd.read_excel(paris_file)
        # Asumimos que la columna es 'TIPO' según guías anteriores
        if 'TIPO' in df_paris.columns:
            unknown_paris = df_paris[~df_paris['TIPO'].isin(paris_known)]['TIPO'].unique()
            for item in unknown_paris:
                results.append({"Marketplace": "París", "Concepto_Desconocido": item})
        else:
            results.append({"Marketplace": "París", "Error": f"Columna TIPO no encontrada. Columnas: {list(df_paris.columns)}"})

    # 2. Analizar Ripley
    ripley_file = "/home/ubuntu/upload/Historial_Nov2025.csv"
    ripley_known = ["Importe del pedido", "Comisiones", "Gastos de envío (RIPLEY)", "Impuesto sobre la comisión (IVA 0,00%)", "Importe de reembolso", "Abono manual", "Factura manual"]
    
    if os.path.exists(ripley_file):
        try:
            df_ripley = pd.read_csv(ripley_file)
            if 'Tipo' in df_ripley.columns:
                unknown_ripley = df_ripley[~df_ripley['Tipo'].isin(ripley_known)]['Tipo'].unique()
                for item in unknown_ripley:
                    results.append({"Marketplace": "Ripley", "Concepto_Desconocido": item})
            else:
                results.append({"Marketplace": "Ripley", "Error": f"Columna Tipo no encontrada. Columnas: {list(df_ripley.columns)}"})
        except Exception as e:
            results.append({"Marketplace": "Ripley", "Error": str(e)})

    # Guardar resultados
    pd.DataFrame(results).to_csv("/home/ubuntu/hallazgos_radar.csv", index=False)
    print("Radar ejecutado con éxito.")

if __name__ == "__main__":
    run_radar()
