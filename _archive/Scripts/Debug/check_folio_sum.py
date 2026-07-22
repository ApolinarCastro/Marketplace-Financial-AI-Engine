import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT folio_xml, SUM(monto) as total_cargo FROM marketplace_ledger_v1 WHERE marketplace='ML' AND folio_xml='033-0008463012' GROUP BY folio_xml"))
