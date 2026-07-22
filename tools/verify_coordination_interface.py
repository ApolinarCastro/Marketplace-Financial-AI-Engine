from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

CANONICAL_COORD_FILES = {
    'governance/coordination/COORDINATION_CONTRACT.md',
    'governance/coordination/coordination_registry.json',
    'governance/coordination/coordination_state.json',
    'tools/verify_coordination_interface.py',
}
FORBIDDEN_COORD_FILENAMES = {
    'coordination_contract.md',
    'coordination_registry.json',
    'coordination_state.json',
    'coordination_contract.json',
    'coordination_registry.md',
    'coordination_state.md',
}
FORBIDDEN_STATE_PATTERNS = [
    re.compile(r'CURRENT_TASK', re.IGNORECASE),
    re.compile(r'"handoff"', re.IGNORECASE),
    re.compile(r'"next_actor"', re.IGNORECASE),
    re.compile(r'"current_owner"', re.IGNORECASE),
]
ALLOWED_STATE_PATTERN_FILES = {
    'governance/coordination/coordination_state.json',
    'tests/test_coordination_interface.py',
    'tools/verify_coordination_interface.py',
    'governance/coordination/executions/GOV-R002_EXECUTION_REPORT.md',
    'governance/coordination/reviews/COORDINATION_VERIFIER_DISCOVERY.md',
    'governance/coordination/reviews/GOV-R002R3_OPENCODE_CLASSIFICATION.md',
    '.claude/helpers/swarm-hooks.sh',
}
ALLOWED_CANONICAL_OUTSIDE_COORD = {
    'execution_board.json',
    'execution_board.md',
    'tools/verify_coordination_interface.py',
    'tools/install_coordination_hook.ps1',
    '.claude/commands/agents/agent-coordination.md',
    'tests/test_coordination_interface.py',
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


EXCLUDED_RGLOB_DIRS = {
    '.git', '.venv', '__pycache__', '.pytest_cache', '.mypy_cache', 'node_modules',
    'data', '01_Raw', '_archive', 'backup_*', 'snapshot_*', 'uploads',
}


def _skip_rglob_dir(parts: tuple[str, ...]) -> bool:
    for p in parts:
        if p in EXCLUDED_RGLOB_DIRS:
            return True
        if p.startswith('backup_') or p.startswith('snapshot_'):
            return True
    return False


def find_duplicate_coordination_channels(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if _skip_rglob_dir(path.parts):
            continue
        rp = rel(root, path)
        lower_name = path.name.lower()
        if rp in CANONICAL_COORD_FILES or rp in ALLOWED_CANONICAL_OUTSIDE_COORD:
            continue
        if lower_name in FORBIDDEN_COORD_FILENAMES:
            hits.append(rp)
            continue
        if 'coordination' in lower_name and rp != 'governance/coordination/COORDINATION_CONTRACT.md':
            if not rp.startswith('governance/coordination/'):
                hits.append(rp)
    return sorted(set(hits))


def find_forbidden_state_markers(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if _skip_rglob_dir(path.parts):
            continue
        rp = rel(root, path)
        if rp in ALLOWED_STATE_PATTERN_FILES:
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for pat in FORBIDDEN_STATE_PATTERNS:
            if pat.search(text):
                hits.append(rp)
                break
    return sorted(set(hits))


def validate_changed_paths(changed_paths: Iterable[str], protected_paths: list[str], authorized_rfc_refs: Iterable[str] | None = None) -> list[str]:
    changed = [p.replace('\\', '/').strip() for p in changed_paths if p.strip()]
    authorized = [a for a in (authorized_rfc_refs or []) if a]
    errors: list[str] = []
    for path in changed:
        for protected in protected_paths:
            protected_norm = protected.rstrip('/').replace('\\', '/')
            if path == protected_norm or path.startswith(protected_norm + '/'):
                if not authorized:
                    errors.append(f'protected path modified without RFC authorization: {path}')
                break
    return errors


def validate_root(root: Path, changed_paths: Iterable[str] | None = None, authorized_rfc_refs: Iterable[str] | None = None) -> list[str]:
    errors: list[str] = []
    coord = root / 'governance' / 'coordination'
    registry_path = coord / 'coordination_registry.json'
    state_path = coord / 'coordination_state.json'
    contract_path = coord / 'COORDINATION_CONTRACT.md'
    execution_board_path = root / 'execution_board.json'

    required_paths = [coord, registry_path, state_path, contract_path, execution_board_path]
    missing = [rel(root, p) for p in required_paths if not p.exists()]
    if missing:
        errors.append(f'missing required paths: {missing}')
        return errors

    registry = load_json(registry_path)
    state = load_json(state_path)
    board = load_json(execution_board_path)

    for key in [
        'interface_name', 'version', 'owners', 'single_interface_root', 'canonical_files',
        'protected_core_paths', 'coordination_permissions', 'verification_command'
    ]:
        if key not in registry:
            errors.append(f'registry missing key: {key}')
    for key in [
        'interface_version', 'status', 'active_channel', 'current_owner', 'peer_owner',
        'current_goal', 'authoritative_inputs', 'handoff', 'constraints'
    ]:
        if key not in state:
            errors.append(f'state missing key: {key}')
    if errors:
        return errors

    if registry['single_interface_root'] != 'governance/coordination':
        errors.append('single_interface_root must be governance/coordination')
    if state['active_channel'] != registry['single_interface_root']:
        errors.append('state active_channel contradicts registry single_interface_root')
    if state['interface_version'] != registry['version']:
        errors.append('state interface_version contradicts registry version')
    if sorted(registry['owners']) != ['Codex', 'OpenCode']:
        errors.append('owners must be exactly Codex and OpenCode')
    owner_set = set(registry['owners'])
    if state['current_owner'] not in owner_set or state['peer_owner'] not in owner_set:
        errors.append('state owners must belong to registry owners')
    if state['current_owner'] == state['peer_owner']:
        errors.append('current_owner and peer_owner must be different')
    next_actor = state.get('handoff', {}).get('next_actor')
    if next_actor not in owner_set:
        errors.append('handoff.next_actor must belong to registry owners')

    for canonical in registry['canonical_files']:
        if not (root / canonical).exists():
            errors.append(f'canonical file missing: {canonical}')

    if 'summary' not in board:
        errors.append('execution_board.json missing summary block')
    if 'capabilities' not in board or not isinstance(board['capabilities'], list):
        errors.append('execution_board.json missing capabilities list')

    duplicate_channels = find_duplicate_coordination_channels(root)
    if duplicate_channels:
        errors.append(f'non-canonical coordination files detected: {duplicate_channels}')

    forbidden_markers = find_forbidden_state_markers(root)
    if forbidden_markers:
        errors.append(f'forbidden coordination state markers outside governance/coordination: {forbidden_markers}')

    protected_paths = registry['protected_core_paths']
    if any(p == 'governance/coordination' or p.startswith('governance/coordination/') for p in protected_paths):
        errors.append('registry protected_core_paths must not include governance/coordination')

    if changed_paths is not None:
        errors.extend(validate_changed_paths(changed_paths, protected_paths, authorized_rfc_refs))

    return errors


def staged_paths_from_git(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify canonical coordination interface.')
    parser.add_argument('--root', default='.', help='Repository root to validate')
    parser.add_argument('--staged-only', action='store_true', help='Validate only staged changes against protected paths')
    parser.add_argument('--changed-path', action='append', default=[], help='Explicit changed path to validate')
    parser.add_argument('--authorized-rfc', action='append', default=[], help='Authorized RFC reference for protected-path edits')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    changed_paths = None
    if args.staged_only:
        changed_paths = staged_paths_from_git(root)
    elif args.changed_path:
        changed_paths = args.changed_path

    errors = validate_root(root, changed_paths=changed_paths, authorized_rfc_refs=args.authorized_rfc)
    if errors:
        for err in errors:
            print(f'FAIL: {err}')
        return 1

    registry = load_json(root / 'governance' / 'coordination' / 'coordination_registry.json')
    state = load_json(root / 'governance' / 'coordination' / 'coordination_state.json')
    board = load_json(root / 'execution_board.json')
    print('PASS: coordination interface verified')
    print(json.dumps({
        'interface': registry['interface_name'],
        'version': registry['version'],
        'owners': registry['owners'],
        'active_channel': state['active_channel'],
        'current_owner': state['current_owner'],
        'next_actor': state['handoff']['next_actor'],
        'capability_summary': board['summary'],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
