from __future__ import annotations
import json
from pathlib import Path

from tools.verify_coordination_interface import validate_root


REGISTRY = {
    'interface_name': 'codex-opencode-coordination',
    'version': '1.0.0',
    'owners': ['Codex', 'OpenCode'],
    'single_interface_root': 'governance/coordination',
    'canonical_files': [
        'governance/coordination/COORDINATION_CONTRACT.md',
        'governance/coordination/coordination_registry.json',
        'governance/coordination/coordination_state.json',
        'tools/verify_coordination_interface.py',
        'execution_board.json',
    ],
    'protected_core_paths': [
        'engine/rc1',
        'engine/v4',
        'data/db/meli_financial_v4.db',
    ],
    'coordination_permissions': {
        'may_update': ['governance/coordination/coordination_state.json', 'execution_board.json'],
        'may_read': ['governance/**', 'execution_board.json'],
        'must_not_use_as_coordination': ['chat-only state'],
    },
    'verification_command': '.venv\Scripts\python.exe tools\verify_coordination_interface.py',
}

STATE = {
    'interface_version': '1.0.0',
    'status': 'ACTIVE',
    'active_channel': 'governance/coordination',
    'current_owner': 'Codex',
    'peer_owner': 'OpenCode',
    'current_goal': 'Enforce canonical coordination only',
    'authoritative_inputs': {
        'execution_board': 'execution_board.json',
        'evidence_latest': 'evidence/fase_1b',
        'contract': 'governance/coordination/COORDINATION_CONTRACT.md',
    },
    'handoff': {
        'next_actor': 'OpenCode',
        'required_read_files': [
            'governance/coordination/COORDINATION_CONTRACT.md',
            'governance/coordination/coordination_registry.json',
            'governance/coordination/coordination_state.json',
            'execution_board.json',
        ],
        'blocked_by': [],
        'next_actions': ['Run verifier after coordination changes'],
    },
    'constraints': ['Do not coordinate outside governance/coordination'],
}

BOARD = {
    'summary': {'total_capabilities': 1},
    'capabilities': [],
}


def _build_repo(tmp_path: Path) -> Path:
    root = tmp_path / 'repo'
    (root / 'governance' / 'coordination').mkdir(parents=True)
    (root / 'tools').mkdir(parents=True)
    (root / 'engine' / 'v4').mkdir(parents=True)
    (root / 'engine' / 'rc1').mkdir(parents=True)
    (root / 'data' / 'db').mkdir(parents=True)
    (root / 'governance' / 'coordination' / 'COORDINATION_CONTRACT.md').write_text('contract', encoding='utf-8')
    (root / 'governance' / 'coordination' / 'coordination_registry.json').write_text(json.dumps(REGISTRY), encoding='utf-8')
    (root / 'governance' / 'coordination' / 'coordination_state.json').write_text(json.dumps(STATE), encoding='utf-8')
    (root / 'tools' / 'verify_coordination_interface.py').write_text('# verifier placeholder', encoding='utf-8')
    (root / 'execution_board.json').write_text(json.dumps(BOARD), encoding='utf-8')
    (root / 'data' / 'db' / 'meli_financial_v4.db').write_text('', encoding='utf-8')
    return root


def test_coordination_interface_passes(tmp_path):
    root = _build_repo(tmp_path)
    assert validate_root(root) == []


def test_fails_on_alternative_coordination_channel(tmp_path):
    root = _build_repo(tmp_path)
    alt = root / 'docs' / 'coordination_registry.json'
    alt.parent.mkdir(parents=True)
    alt.write_text('{}', encoding='utf-8')
    errors = validate_root(root)
    assert any('non-canonical coordination files detected' in e for e in errors)


def test_fails_on_missing_canonical_reference(tmp_path):
    root = _build_repo(tmp_path)
    data = json.loads((root / 'governance' / 'coordination' / 'coordination_registry.json').read_text(encoding='utf-8'))
    data['canonical_files'].append('governance/coordination/missing.json')
    (root / 'governance' / 'coordination' / 'coordination_registry.json').write_text(json.dumps(data), encoding='utf-8')
    errors = validate_root(root)
    assert any('canonical file missing' in e for e in errors)


def test_fails_when_state_contradicts_registry(tmp_path):
    root = _build_repo(tmp_path)
    data = json.loads((root / 'governance' / 'coordination' / 'coordination_state.json').read_text(encoding='utf-8'))
    data['active_channel'] = 'docs/coordination'
    (root / 'governance' / 'coordination' / 'coordination_state.json').write_text(json.dumps(data), encoding='utf-8')
    errors = validate_root(root)
    assert any('state active_channel contradicts registry' in e for e in errors)


def test_fails_on_protected_path_change_without_rfc(tmp_path):
    root = _build_repo(tmp_path)
    errors = validate_root(root, changed_paths=['engine/v4/copilot/copilot_engine.py'])
    assert any('protected path modified without RFC authorization' in e for e in errors)


def test_fails_on_forbidden_state_marker_outside_coordination(tmp_path):
    root = _build_repo(tmp_path)
    rogue = root / 'notes.md'
    rogue.write_text('CURRENT_TASK = do something', encoding='utf-8')
    errors = validate_root(root)
    assert any('forbidden coordination state markers outside governance/coordination' in e for e in errors)


def test_verifier_runs_via_subprocess(tmp_path, monkeypatch):
    """verify_coordination_interface.py runs as CLI (pytest integration)."""
    import subprocess
    root = _build_repo(tmp_path)
    monkeypatch.chdir(root)
    result = subprocess.run(
        ['python', str(root / 'tools' / 'verify_coordination_interface.py'), '--root', str(root)],
        capture_output=True, text=True, timeout=15,
    )
    assert result.returncode == 0, f'verifier failed: {result.stderr}'


def test_fails_on_protected_core_path_mod_in_subdir(tmp_path):
    """Modifying a file inside a protected path without RFC authorization fails."""
    root = _build_repo(tmp_path)
    errors = validate_root(root, changed_paths=['engine/v4/ingestion/upload_handler.py'])
    assert any('protected path modified without RFC authorization' in e for e in errors)


def test_fails_on_protected_db_path(tmp_path):
    """Modifying the official DB file without RFC authorization fails."""
    root = _build_repo(tmp_path)
    errors = validate_root(root, changed_paths=['data/db/meli_financial_v4.db'])
    assert any('protected path modified without RFC authorization' in e for e in errors)


def test_passes_with_authorized_rfc(tmp_path):
    """Protected path modification with authorized RFC passes."""
    root = _build_repo(tmp_path)
    errors = validate_root(root, changed_paths=['engine/v4/ingestion/upload_handler.py'],
                           authorized_rfc_refs=['RFC-040'])
    assert errors == []


def test_passes_on_non_protected_path(tmp_path):
    """Non-protected path modification passes without RFC."""
    root = _build_repo(tmp_path)
    errors = validate_root(root, changed_paths=['templates/dashboard.html'])
    assert errors == []


def test_fails_on_owner_mismatch(tmp_path):
    """State owner outside registry owners fails."""
    root = _build_repo(tmp_path)
    state = json.loads((root / 'governance' / 'coordination' / 'coordination_state.json').read_text(encoding='utf-8'))
    state['current_owner'] = 'UnknownAgent'
    (root / 'governance' / 'coordination' / 'coordination_state.json').write_text(json.dumps(state), encoding='utf-8')
    errors = validate_root(root)
    assert any('state owners must belong to registry owners' in e for e in errors)


def test_fails_on_same_owner_and_peer(tmp_path):
    """current_owner and peer_owner must differ."""
    root = _build_repo(tmp_path)
    state = json.loads((root / 'governance' / 'coordination' / 'coordination_state.json').read_text(encoding='utf-8'))
    state['current_owner'] = 'Codex'
    state['peer_owner'] = 'Codex'
    (root / 'governance' / 'coordination' / 'coordination_state.json').write_text(json.dumps(state), encoding='utf-8')
    errors = validate_root(root)
    assert any('current_owner and peer_owner must be different' in e for e in errors)
