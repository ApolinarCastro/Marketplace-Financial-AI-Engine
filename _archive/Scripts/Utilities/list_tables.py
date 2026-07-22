from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SHOW TABLES;"))
