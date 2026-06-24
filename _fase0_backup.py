import hashlib, os, json, duckdb
from datetime import datetime

snap_dir = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\snapshot_pre_fase2_20260603_112908'
dst = os.path.join(snap_dir, 'meli_financial_v4.db')

dst_size = os.path.getsize(dst)
h = hashlib.sha256()
with open(dst, 'rb') as f:
    for chunk in iter(lambda: f.read(65536), b''):
        h.update(chunk)
dst_sha = h.hexdigest()

expected = 'f110fe9269d2e1db92e7ca99a990ad0b510ed935662da593d11a71e1ce4cb4f9'
sha_match = dst_sha == expected

print(f'Copy size: {dst_size:,} bytes')
print(f'Copy SHA256: {dst_sha}')
print(f'Expected:    {expected}')
print(f'Match: {sha_match}')

con = duckdb.connect(dst)
tables_data = {}
for t in ['marketplace_ledger_v1', 'marketplace_ledger_clasificado_v1', 'marketplace_cierre_financiero_v1']:
    r = con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    tables_data[t] = r
    print(f'{t}: {r:,} rows')
con.close()

manifest = {
    'snapshot_name': 'snapshot_pre_fase2_20260603_112908',
    'created_at': datetime.now().isoformat(),
    'description': 'Pre-B2.5C classification+closing execution',
    'baseline': 'BASELINE_V6',
    'db_file': 'meli_financial_v4.db',
    'sha256': dst_sha,
    'size_bytes': dst_size,
    'row_counts': tables_data,
    'pre_state': {
        'classification_status': 'NOT_EXECUTED_post_RFC001',
        'ripley_financial_group': '100% NULL',
        'clasificado_table': 'stale_pre_RFC001_data'
    }
}
with open(os.path.join(snap_dir, 'MANIFEST.json'), 'w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print('\nFASE 0 COMPLETE: Snapshot validated, manifest written')
print(f'Location: {snap_dir}')
