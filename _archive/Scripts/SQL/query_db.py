import sys
from api.api import DatabaseV4
import pandas as pd

def run():
    db = DatabaseV4.get()
    
    # Check ingresos
    df = db.query("SELECT detalle, sum(monto_bruto) as mb, sum(comision_marketplace) as cm FROM marketplace_ledger_v1 WHERE marketplace='PARIS' AND financial_group='ingresos' GROUP BY detalle", [])
    print("INGRESOS:")
    print(df)
    
    # Check devoluciones
    df2 = db.query("SELECT detalle, sum(monto_bruto) as mb, sum(comision_marketplace) as cm FROM marketplace_ledger_v1 WHERE marketplace='PARIS' AND financial_group='devoluciones' GROUP BY detalle", [])
    print("\nDEVOLUCIONES:")
    print(df2)

if __name__ == "__main__":
    run()
