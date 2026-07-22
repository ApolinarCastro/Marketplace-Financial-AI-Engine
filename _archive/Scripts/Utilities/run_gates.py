import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from engine.v4.certification.certification_engine import CertificationEngine
from pydantic.json import pydantic_encoder
import json

engine = CertificationEngine()
res = engine.certify('RIPLEY', 'YTD')
print(json.dumps(res, default=pydantic_encoder, indent=2))
