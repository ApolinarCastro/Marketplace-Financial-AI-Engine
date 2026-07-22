import duckdb
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()
classes = db.execute("SELECT marketplace, match_status, COUNT(*) FROM document_match_v1 GROUP BY marketplace, match_status").fetchall()
for row in classes:
    print(row)
