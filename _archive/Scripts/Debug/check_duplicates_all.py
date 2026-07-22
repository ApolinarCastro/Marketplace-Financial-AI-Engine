from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE
keys = ['ingresos', 'devoluciones', 'costos_operacionales', 'costos_comerciales', 'ajustes']
for i in range(len(keys)):
    for j in range(i+1, len(keys)):
        k1, k2 = keys[i], keys[j]
        intersect = set(FINANCIAL_STRUCTURE[k1]).intersection(set(FINANCIAL_STRUCTURE[k2]))
        if intersect:
            print(f'Duplicate between {k1} and {k2}: {intersect}')
