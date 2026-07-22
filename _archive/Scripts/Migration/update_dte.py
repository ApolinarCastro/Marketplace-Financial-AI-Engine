import duckdb

try:
    db = duckdb.connect('data/db/meli_financial_v4.db')

    print('Before update:')
    res = db.execute('SELECT emisor_rut, COUNT(*) FROM dte_truth_v1 WHERE marketplace IS NULL GROUP BY emisor_rut').fetchall()
    print(res)

    if len(res) > 0:
        print('Executing update...')
        db.execute("UPDATE dte_truth_v1 SET marketplace = 'ML' WHERE emisor_rut = '77398220-1' AND marketplace IS NULL")
        db.execute("UPDATE dte_truth_v1 SET marketplace = 'FALABELLA' WHERE emisor_rut = '76212492-0' AND marketplace IS NULL")
        
        print('After update:')
        res = db.execute('SELECT COUNT(*) FROM dte_truth_v1 WHERE marketplace IS NULL').fetchall()
        print('NULL marketplaces:', res[0][0])
    else:
        print('No records to update.')

except Exception as e:
    print(f"Error: {e}")
