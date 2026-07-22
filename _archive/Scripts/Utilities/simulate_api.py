import duckdb
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

query = """
        WITH BaseLedger AS (
            SELECT * FROM marketplace_ledger_v1 WHERE marketplace = 'PARIS'
        )
        SELECT b.* EXCLUDE (estado_xml),
               CASE 
                   WHEN EXISTS (
                       SELECT 1 FROM document_match_v1 m 
                       WHERE m.marketplace = b.marketplace 
                         AND (
                             m.order_id = b.id_orden 
                             OR m.ledger_id = b.id_transaccion 
                             OR m.ledger_id LIKE b.id_transaccion || '\\_%'
                         )
                   ) THEN 'CONCILIADO'
                   WHEN b.folio_xml IS NOT NULL AND b.folio_xml <> 'None' THEN 'DOCUMENTADO'
                   ELSE 'PENDIENTE'
               END as estado_xml
        FROM BaseLedger b
"""
try:
    df = conn.execute(query).df()
    print("API simulation successful")
    print(df['estado_xml'].value_counts())
except Exception as e:
    print("Error:", e)
