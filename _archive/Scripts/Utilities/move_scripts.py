import os
import shutil
from pathlib import Path

root = Path('.')
scripts_dir = root / 'Scripts'
categories = ['Debug', 'Migration', 'OneShot', 'SQL', 'Forensic', 'Utilities', 'Playbook', 'Benchmark']

for c in categories:
    (scripts_dir / c).mkdir(parents=True, exist_ok=True)

py_files = [f for f in root.iterdir() if f.is_file() and f.suffix == '.py' and f.name not in ('run_app.py', 'config.py')]

for f in py_files:
    name = f.name.lower()
    dest = None
    if 'benchmark' in name:
        dest = 'Benchmark'
    elif name.startswith('check_') or name.startswith('test_') or name.startswith('val_') or name.startswith('debug_') or name.startswith('verify_'):
        dest = 'Debug'
    elif name.startswith('fix_') or name.startswith('patch_') or name.startswith('apply_') or name.startswith('migrate_') or name.startswith('update_') or name.startswith('restore_') or name.startswith('rewrite_') or name.startswith('certify_'):
        dest = 'Migration'
    elif name.startswith('_'):
        dest = 'OneShot'
    elif name.startswith('query') or name.startswith('sql_'):
        dest = 'SQL'
    elif name.startswith('investigate') or name.startswith('trace') or name.startswith('find') or name.startswith('audit'):
        dest = 'Forensic'
    elif name.startswith('analyze') or name.startswith('extract') or name.startswith('list') or name.startswith('show') or name.startswith('run_'):
        dest = 'Utilities'
    elif name.startswith('generate_'):
        dest = 'Playbook'
    else:
        dest = 'Utilities' # fallback
        
    shutil.move(str(f), str(scripts_dir / dest / f.name))

print("Scripts moved successfully.")
