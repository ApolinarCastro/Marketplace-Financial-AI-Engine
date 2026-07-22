import pandas as pd
import duckdb

def main():
    con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
    
    q = """
    SELECT detalle, sum(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
      AND detalle LIKE '%reembols%'
    GROUP BY 1
    """
    print(con.execute(q).fetchdf())

if __name__ == '__main__':
    main()
