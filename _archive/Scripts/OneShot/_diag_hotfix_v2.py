import pandas as pd
import duckdb

def main():
    con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
    
    q = """
    SELECT detalle, financial_group, sum(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY 1, 2
    HAVING sum(monto) > -14060000 AND sum(monto) < -14050000
    """
    print("--- Exact match for -14,059,100 ---")
    print(con.execute(q).fetchdf())

    q2 = """
    SELECT 
        SUM(CASE WHEN detalle = 'Pedidos reembolsados' AND marketplace='RIPLEY' THEN monto ELSE 0 END) as pedidos_reemb,
        SUM(CASE WHEN detalle LIKE '%reembolso%' AND marketplace='RIPLEY' THEN monto ELSE 0 END) as all_reemb
    FROM marketplace_ledger_v1
    """
    print("\n--- RIPLEY total reembolsos ---")
    print(con.execute(q2).fetchdf())
    
    q3 = """
    SELECT detalle, COUNT(*) as filas, SUM(monto) as total_monto,
           CASE 
             WHEN archivo_origen LIKE '%.xlsx' THEN 'SELLER'
             WHEN archivo_origen LIKE '%ff%.csv' THEN 'FULFILLMENT'
             WHEN archivo_origen LIKE '%-%-%-%-%' THEN 'CICLOS'
             WHEN archivo_origen LIKE '%.xml' THEN 'XML'
             ELSE 'OTRO'
           END as origen
    FROM marketplace_ledger_v1
    WHERE marketplace='RIPLEY' AND detalle = 'refund_order_amount'
    GROUP BY 1, 4
    """
    print("\n--- RIPLEY refund_order_amount ---")
    print(con.execute(q3).fetchdf())

if __name__ == '__main__':
    main()
