"""
taxonomy_loader.py — YAML-based taxonomy loader.

Read-only. Zero financial logic. Single responsibility: load and validate.
"""
from __future__ import annotations
from pathlib import Path
import yaml
import unicodedata
import re
from typing import Any


ROOT = Path(__file__).resolve().parent
RULES_PATH = ROOT / "taxonomy_rules.yaml"
MAPPINGS_PATH = ROOT / "taxonomy_mappings.yaml"


def _fix_mojibake(text: str) -> str:
    """Fix double-encoded UTF-8 mojibake (e.g. 'Ã³' -> 'ó', 'Ã±' -> 'ñ')."""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def normalize_detail(text: str) -> str:
    """Normalize a detail string for lookup (exact replica of marketplace_auditor.normalize_detail)."""
    if not isinstance(text, str):
        return ""
    t = _fix_mojibake(text.strip()).lower()
    t = ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
    t = re.sub(r'[^a-z0-9\s_]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def load_rules() -> dict[str, dict[str, Any]]:
    """Load taxonomy rules from YAML."""
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        rules: dict = yaml.safe_load(f)
    return rules or {}


def load_mappings() -> dict[str, dict[str, Any]]:
    """Load raw detail -> concept mappings from YAML."""
    with open(MAPPINGS_PATH, "r", encoding="utf-8") as f:
        mappings: dict = yaml.safe_load(f)
    return mappings or {}


def build_concept_to_group_map(rules: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Build reverse map: concept -> financial_group from rules."""
    result = {}
    for group_name, group_data in rules.items():
        for concept in group_data.get("concepts", []):
            result[concept] = group_name
    return result


def build_normalized_mappings(mappings: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Build normalized_detail -> concept map from mappings."""
    result = {}
    for raw_detail, entry in mappings.items():
        norm = normalize_detail(raw_detail)
        if norm:
            result[norm] = entry["concept"]
    return result


def resolve_financial_group(concept: str, rules: dict[str, dict[str, Any]] | None = None) -> str | None:
    """Resolve a concept to its financial group. Returns None if unknown."""
    if rules is None:
        rules = load_rules()
    for group_name, group_data in rules.items():
        if concept in group_data.get("concepts", []):
            return group_name
    return None


def validate_taxonomy(rules: dict[str, dict[str, Any]] | None = None,
                      mappings: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Validate taxonomy consistency. Returns report dict."""
    if rules is None:
        rules = load_rules()
    if mappings is None:
        mappings = load_mappings()

    issues = []
    concept_to_group = build_concept_to_group_map(rules)
    all_concepts_in_rules = set(concept_to_group.keys())

    # Check all mapped concepts have a financial group in rules
    # Some concepts (e.g., "Pago", "Devolución de dinero\nEnvío") are 
    # dynamically resolved via payout_rule or compound-concept handling -- expected.
    missing_groups = []
    for raw, entry in mappings.items():
        concept = entry["concept"]
        if concept not in all_concepts_in_rules:
            missing_groups.append(raw)

    if missing_groups:
        issues.append(f"{len(missing_groups)} concepts not in rules (dynamically resolved: Pago, Devolución de dinero\\nEnvío)")

    # Check required rule fields
    required_fields = ["order", "sign_behavior", "include_in_operational_pnl"]
    for group_name, gd in rules.items():
        for f in required_fields:
            if f not in gd:
                issues.append(f"Group '{group_name}' missing required field '{f}'")

    return {
        "valid": len(issues) == 0,
        "groups": len(rules),
        "raw_mappings": len(mappings),
        "total_concepts": len(all_concepts_in_rules),
        "issues": issues,
    }
