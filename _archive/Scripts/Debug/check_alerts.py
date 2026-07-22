import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from pydantic.json import pydantic_encoder
import json

engine = ReconciliationEngine()
res = engine.validate_marketplace_consistency('RIPLEY', 'YTD')
print(json.dumps(res, default=pydantic_encoder, indent=2))
