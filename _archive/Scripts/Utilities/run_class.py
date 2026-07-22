import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

auditor = MarketplaceAuditorEngine()
auditor.run_classification()
