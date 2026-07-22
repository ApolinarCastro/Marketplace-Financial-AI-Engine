from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE
dev = set(FINANCIAL_STRUCTURE['devoluciones'])
aju = set(FINANCIAL_STRUCTURE['ajustes'])
print('Intersection:', dev.intersection(aju))
