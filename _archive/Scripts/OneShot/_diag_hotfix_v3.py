import pandas as pd
import duckdb

def main():
    con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
    
    q = """
    SELECT detalle, 
           CASE 
             WHEN archivo_origen LIKE '%.xlsx' THEN 'SELLER'
             WHEN archivo_origen LIKE '%ff%.csv' THEN 'FULFILLMENT'
             WHEN archivo_origen LIKE '%-%-%-%-%' THEN 'CICLOS'
             WHEN archivo_origen LIKE '%.xml' THEN 'XML'
             ELSE 'OTRO'
           END as origen,
           sum(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY 1, 2
    HAVING sum(monto) BETWEEN -16000000 AND -12000000
    """
    print("--- Searching for ~14M refund ---")
    print(con.execute(q).fetchdf())

if __name__ == '__main__':
    main()
