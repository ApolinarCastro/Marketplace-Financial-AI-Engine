import os
import json
from pathlib import Path

with open('REPOSITORY_REGISTRY.json', 'r') as f:
    registry = json.load(f)

for item in registry:
    if item['classification'] == 'UNKNOWN':
        name = Path(item['file']).name.lower()
        if name == 'start_app.bat':
            item['classification'] = 'CORE'
        elif name == 'ledger_serialization_benchmark.py':
            item['classification'] = 'BENCHMARK'
        elif name == 'knowledge_index.yaml':
            item['classification'] = 'KNOWLEDGE'
        elif name == 'duckdb_manager.py' and 'database' in item['file']:
            item['classification'] = 'CORE'
        elif name == ']':
            item['classification'] = 'OBSOLETE'
        elif 'mypy_cache' in item['file']:
            item['classification'] = 'CONFIGURATION'
        elif name.endswith('.py') or name.endswith('.html') or name.endswith('.js'):
            # any remaining python files in root are scratch/obsolete/debug
            item['classification'] = 'OBSOLETE'
        else:
            item['classification'] = 'OBSOLETE'

with open('REPOSITORY_REGISTRY.json', 'w') as f:
    json.dump(registry, f, indent=2)

unknowns = [item['file'] for item in registry if item['classification'] == 'UNKNOWN']
print(f"Total UNKNOWN files: {len(unknowns)}")
