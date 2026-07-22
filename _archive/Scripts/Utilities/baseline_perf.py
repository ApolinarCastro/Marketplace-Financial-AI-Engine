import time
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.dte_indexer import DTEIndexer
from engine.v4.surgical_xml_justifier import XMLJustifier
from engine.v4.surgical_loader import SurgicalLoader

def measure(name, func):
    t0 = time.time()
    func()
    t1 = time.time()
    print(f'{name}: {t1 - t0:.2f} s')

print('--- Baseline V4 Performance ---')
db = DatabaseV4.get()

loader = SurgicalLoader()
measure('Ledger Ingestion', loader.run)

indexer = DTEIndexer()
measure('Document Engine (DTEIndexer)', indexer.run)

justifier = XMLJustifier()
measure('Auditoría Justifier', justifier.run)

engine = MarketplaceAuditorEngine()
measure('Marketplace Auditor (Classification)', engine.run_classification)
