import pandas as pd
import duckdb

def main():
    con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
    
    # Check 1: Ingresos Brutos concepts
    print("--- 1. INGRESOS BRUTOS CONCEPTS ---")
    q1 = """
    SELECT detalle, COUNT(*) as filas, SUM(monto) as total_monto,
           CASE 
             WHEN archivo_origen LIKE '%.xlsx' THEN 'SELLER'
             WHEN archivo_origen LIKE '%ff%.csv' THEN 'FULFILLMENT'
             WHEN archivo_origen LIKE '%-%-%-%-%' THEN 'CICLOS'
             WHEN archivo_origen LIKE '%.xml' THEN 'XML'
             ELSE 'OTRO'
           END as origen
    FROM marketplace_ledger_v1
    WHERE detalle IN ('Precio total', 'Subtotal', 'Importe del pedido')
    GROUP BY 1, 4
    """
    df1 = con.execute(q1).fetchdf()
    print(df1.to_string())

    # Check 2: Duplicidad IDs
    print("\n--- 2. DUPLICIDAD DE IDs ---")
    q2 = """
    WITH counts AS (
        SELECT id_orden, COUNT(DISTINCT detalle) as cnt_detalles, list_distinct(list(detalle)) as det_list
        FROM marketplace_ledger_v1
        WHERE detalle IN ('Precio total', 'Subtotal', 'Importe del pedido')
        GROUP BY id_orden
    )
    SELECT cnt_detalles, COUNT(*) as cant_ordenes, det_list
    FROM counts
    GROUP BY 1, 3
    """
    df2 = con.execute(q2).fetchdf()
    print(df2.to_string())

    # Check 3: Pedidos Reembolsados origin
    print("\n--- 3. PEDIDOS REEMBOLSADOS ---")
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
    WHERE detalle LIKE '%reembolso%' OR detalle LIKE '%reembolsado%' OR financial_group = 'devoluciones'
    GROUP BY 1, 4
    """
    df3 = con.execute(q3).fetchdf()
    print(df3.to_string())

    # Check 4: Check what get_financial_structure returns for ingresos
    print("\n--- 4. ESTADO DE LAS TABLAS ---")
    print(con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchdf())

if __name__ == '__main__':
    main()
