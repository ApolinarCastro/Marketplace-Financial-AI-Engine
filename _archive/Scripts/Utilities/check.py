from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
dte = set(db.query("SELECT folio FROM dte_truth_v1 WHERE marketplace='RIPLEY'")['folio'].astype(str))
led = set(db.query("SELECT folio_xml FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND folio_xml IS NOT NULL")['folio_xml'].astype(str))
intersect = dte.intersection(led)
print("Intersection:", len(intersect))
if len(intersect) > 0:
    print("Some:", list(intersect)[:5])
