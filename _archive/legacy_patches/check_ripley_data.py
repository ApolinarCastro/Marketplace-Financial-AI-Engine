import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')

from engine.v4.database import DatabaseV4
import pandas as pd

def check_db():
    db = DatabaseV4.get()
    
    # 1. Check if there are records in ledger for RIPLEY in 2025-01
    print("--- LEDGER RIPLEY 2025-01 ---")
    df1 = db.query("SELECT COUNT(*) as count, SUM(monto) as total FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND fecha >= '2025-01-01' AND fecha <= '2025-01-31'")
    print(df1)
    
    print("\n--- LEDGER RIPLEY ALL PERIODS ---")
    df2 = db.query("SELECT MIN(fecha), MAX(fecha), COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'")
    print(df2)
    
    print("\n--- CIERRE DESGLOSE FUNCTIONALITY (LIKE API) ---")
    sql = """
        SELECT 
            COALESCE(financial_group, 'sin_clasificar') as financial_group,
            SUM(COALESCE(monto, 0)) as total,
            COUNT(*) as cantidad
        FROM marketplace_ledger_v1
        WHERE marketplace = 'RIPLEY'
          AND fecha BETWEEN '2025-01-01' AND '2025-01-31'
        GROUP BY financial_group
    """
    df3 = db.query(sql)
    print(df3)

if __name__ == "__main__":
    check_db()
