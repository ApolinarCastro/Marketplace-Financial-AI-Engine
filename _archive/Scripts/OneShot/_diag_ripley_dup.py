import duckdb
import pandas as pd

def main():
    conn = duckdb.connect('data/db/meli_financial_v4.db')
    
    # Registros que son ventas netas/brutas
    query = """
    WITH seller AS (
        SELECT id_orden, SUM(monto) as monto_seller, COUNT(*) as c_seller
        FROM marketplace_ledger_v1
        WHERE marketplace='RIPLEY' 
        AND archivo_origen LIKE '%.xlsx'
        AND detalle = 'Importe del pedido'
        GROUP BY id_orden
    ),
    ciclos AS (
        SELECT id_orden, SUM(monto) as monto_ciclos, COUNT(*) as c_ciclos
        FROM marketplace_ledger_v1
        WHERE marketplace='RIPLEY'
        AND archivo_origen LIKE '%-%-%-%-%'
        AND detalle = 'Subtotal'
        GROUP BY id_orden
    )
    SELECT 
        COUNT(*) as ordenes_duplicadas,
        SUM(c_seller + c_ciclos) as registros_duplicados,
        SUM(monto_seller) as impacto_monetario_seller,
        SUM(monto_ciclos) as impacto_monetario_ciclos
    FROM seller s
    JOIN ciclos c ON s.id_orden = c.id_orden
    """
    
    df = conn.execute(query).fetchdf()
    print(df.to_string())

if __name__ == '__main__':
    main()
