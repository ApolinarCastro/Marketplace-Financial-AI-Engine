import duckdb
import pandas as pd
conn = duckdb.connect("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db", read_only=True)

df = conn.execute("""
    SELECT detalle, financial_group, clasificacion_operativa, COUNT(1) as qty 
    FROM marketplace_ledger_v1 
    WHERE detalle IN ('Arrepentimiento', 'Talla/Garantía', 'Producto Dañado', 'Retraso Entrega', 'Item Faltante', 'repentant_buyer', 'delivery_date_was_not_met', 'missing_item', 'broken_item_fashion', 'smaller_than_expected_fashion')
    GROUP BY detalle, financial_group, clasificacion_operativa
""").df()
print(df.to_string())
