import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

auditor = MarketplaceAuditorEngine()
for mp in ['ML', 'RIPLEY', 'FALABELLA', 'PARIS', 'LIDER']:
    auditor.run_financial_closing(mp, '1970-01-01', '2099-12-31')
