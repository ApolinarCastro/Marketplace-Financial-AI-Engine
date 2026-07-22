import os
import json
from pathlib import Path

def get_class(filepath):
    path_str = filepath.as_posix().lower()
    name = filepath.name.lower()
    
    # Core directories - exact match on prefix directory
    parts = list(filepath.parts)
    if len(parts) > 0:
        first = parts[0].lower()
        if first in ['engine', 'api', 'templates', 'frontend', 'run_app.py', 'config.py']:
            return 'CORE'
        if first == 'data':
            return 'DATA'
        if first in ['knowledgebase', 'knowledge']:
            return 'KNOWLEDGE'
        if first == 'scratch':
            return 'EXPERIMENTAL'
        if first == '00_config':
            return 'CONFIGURATION'
        if first == '01_raw':
            return 'DATA'
        if first == 'docs':
            return 'KNOWLEDGE'
        if first == 'releases':
            return 'PRODUCTION'
        if first == 'taxonomy':
            return 'CONFIGURATION'
        if first == 'tests':
            return 'DEBUG'
        if first == 'discovery':
            return 'EXPERIMENTAL'
        if first == 'governance':
            return 'KNOWLEDGE'
        if first == 'reporte_marketplaces':
            return 'OBSOLETE'
        if first == '_archive':
            return 'HISTORICAL'
        if first == 'logs':
            return 'DEBUG'

    if name in ['.env', '.gitignore', 'pyproject.toml', 'requirements.txt', 'package.json', 'skills-lock.json', '.mcp.json']:
        return 'CONFIGURATION'
    if name in ['readme.md', 'master_knowledge_index.md', 'backlog.md']:
        return 'KNOWLEDGE'
    if 'baseline' in name or 'manifest' in name:
        return 'HISTORICAL'
    if name.endswith('.md'):
        return 'KNOWLEDGE'
        
    # Heuristics for root scripts and tmp files
    if name.startswith('check_') or name.startswith('test_') or name.startswith('debug_') or name.startswith('verify_') or name.startswith('val_'):
        return 'DEBUG'
    if name.startswith('_'):
        return 'ONE_SHOT'
    if name.startswith('tmp_') or name.endswith('.jsonl') or name.endswith('.diff') or name.endswith('.patch') or name.endswith('_old.html') or 'before' in name or 'history' in name or name.endswith('_log.txt') or name == 'diff.txt':
        return 'OBSOLETE'
    if 'backup' in path_str:
        return 'HISTORICAL'
    if name.endswith('.db') or name.endswith('.duckdb') or name.endswith('.sqlite') or name.endswith('.sqlite3'):
        return 'DATA'
    if name.startswith('generate_'):
        return 'PLAYBOOK'
    if name.startswith('migrate_') or name.startswith('update_'):
        return 'MIGRATION'
    if name.startswith('audit_') or name.startswith('investigate_') or name.startswith('trace_') or name.startswith('find_') or name.startswith('query_'):
        return 'FORENSIC'
    if name.startswith('fix_') or name.startswith('patch_') or name.startswith('apply_') or name.startswith('rewrite_') or name.startswith('restore_') or name.startswith('certify_'):
        return 'MIGRATION'
    if name.startswith('analyze_') or name.startswith('extract_') or name.startswith('show_') or name.startswith('list_') or name.startswith('run_'):
        return 'UTILITIES'
    if name.endswith('.json') or name.endswith('.txt'):
        return 'DATA'
    if name.endswith('.png'):
        return 'KNOWLEDGE'
        
    return 'UNKNOWN'

registry = []
root = Path('.')
ignored_dirs = {'.git', '.venv', '__pycache__', '.pytest_cache', '.ruff_cache', '.claude', '.claude-flow', '.agent', '.agents', '.swarm', '.github', 'Lib', 'Include', 'Scripts'}

for r, d, f in os.walk(root):
    d[:] = [dirname for dirname in d if dirname not in ignored_dirs]
    for file in f:
        file_path = Path(r) / file
        rel_path = file_path.relative_to(root)
        cls = get_class(rel_path)
        registry.append({
            'file': str(rel_path.as_posix()),
            'classification': cls
        })

with open('REPOSITORY_REGISTRY.json', 'w') as f:
    json.dump(registry, f, indent=2)

unknowns = [item['file'] for item in registry if item['classification'] == 'UNKNOWN']
print(f"Total UNKNOWN files: {len(unknowns)}")
if len(unknowns) < 20:
    for u in unknowns:
        print(u)
