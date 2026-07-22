from engine.v4.database import DatabaseV4
from engine.v4.certification.ecc.ecc_adapter import ECCAdapter
import json

db = DatabaseV4.get()
df = db.query("SELECT file_path, marketplace, folio FROM dte_truth_v1 WHERE marketplace='FALABELLA' LIMIT 1")

adapter = ECCAdapter()

fp = df.iloc[0]['file_path']
mp = df.iloc[0]['marketplace']
print(f"Testing {mp} folio {df.iloc[0]['folio']} file {fp}")
try:
    from engine.v4.certification.electronic_certification.xml_reader import XMLReader
    xml, audit_metadata = XMLReader.read_xml(fp)
            
    payload = adapter.process(xml, marketplace=mp)
    print(json.dumps(payload.electronic_certificate, indent=2))
except Exception as e:
    print("FAIL (Exception)")
    import traceback
    traceback.print_exc()
