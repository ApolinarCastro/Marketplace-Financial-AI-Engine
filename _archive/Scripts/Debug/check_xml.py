import sys
from api.api import DatabaseV4
import pandas as pd

def run():
    db = DatabaseV4.get()
    df = db.query("SELECT marketplace, order_id, ledger_id, folio_xml, tipo_documento FROM document_match_v1 WHERE marketplace='PARIS' LIMIT 10", [])
    print(df)

if __name__ == "__main__":
    run()
