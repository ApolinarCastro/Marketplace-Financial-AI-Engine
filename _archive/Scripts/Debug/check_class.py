import sys
sys.path.append('c:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')
from engine.v4.marketplace_auditor import CLASIFICACION_TO_FINANCIAL_GROUP, MASTER_DICTIONARY_V1
import pandas as pd

series = pd.Series(['Comisiones'])
clasif = series.map(lambda x: MASTER_DICTIONARY_V1.get(x, x))
print(clasif)
financial_group_col = clasif.map(CLASIFICACION_TO_FINANCIAL_GROUP)
print(financial_group_col)
