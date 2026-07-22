import duckdb
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

print("--- dte_truth_v1 ---")
print(conn.execute("SELECT marketplace, COUNT(*) FROM dte_truth_v1 GROUP BY marketplace").df())

print("\n--- document_match_v1 ---")
print(conn.execute("SELECT marketplace, COUNT(*) FROM document_match_v1 GROUP BY marketplace").df())

print("\n--- marketplace_auditoria_v1 ---")
print(conn.execute("SELECT marketplace, COUNT(*) FROM marketplace_auditoria_v1 GROUP BY marketplace").df())

print("\n--- marketplace_ledger_v1 estado_xml ---")
print(conn.execute("SELECT marketplace, estado_xml, COUNT(*) FROM marketplace_ledger_v1 GROUP BY marketplace, estado_xml").df())

print("\n--- marketplace_ledger_v1 folio_xml ---")
print(conn.execute("SELECT marketplace, count(folio_xml) as folios_not_null FROM marketplace_ledger_v1 WHERE folio_xml IS NOT NULL and folio_xml <> 'None' GROUP BY marketplace").df())
