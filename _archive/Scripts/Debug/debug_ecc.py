import os
from engine.v4.database import DatabaseV4
from engine.v4.certification.ecc.ecc_adapter import ECCAdapter
import traceback
import json

db = DatabaseV4.get()
df = db.query("SELECT file_path, marketplace, folio FROM dte_truth_v1 LIMIT 1")

adapter = ECCAdapter()

for _, row in df.iterrows():
    fp = row['file_path']
    mp = row['marketplace']
    print(f"Testing {mp} folio {row['folio']} file {fp}")
    try:
        from engine.v4.certification.electronic_certification.xml_reader import XMLReader
        xml, audit_metadata = XMLReader.read_xml(fp)
                
        payload = adapter.process(xml, marketplace=mp)
        print(json.dumps(payload.electronic_certificate, indent=2))
    except Exception as e:
        print("FAIL (Exception)")
        traceback.print_exc()
