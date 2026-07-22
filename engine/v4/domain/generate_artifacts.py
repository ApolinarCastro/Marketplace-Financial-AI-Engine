#!/usr/bin/env python3
"""Generate JSON Schema, Markdown docs, metrics inventory, and consumer contract
from canonical_semantics.py (the sole source of truth).

Usage:
    python -m engine.v4.domain.generate_artifacts [--check-only]

--check-only: Verify existing artifacts match contract without overwriting.
              Exit code 1 if mismatch.
"""

import json, sys, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

# ── Import canonical contract ──────────────────────────────────────────
sys.path.insert(0, str(REPO))
from engine.v4.domain.canonical_semantics import (
    FinancialGroup, CashRole, EventType, Marketplace, AmountSign,
    FINANCIAL_GROUP_META, MARKETPLACE_META, METRIC_REGISTRY, PNL_ORDER,
    UniquenessKey,
)


# ── Output paths ───────────────────────────────────────────────────────
OUTPUT_DIR = REPO / "engine" / "v4" / "domain" / "artifacts"
JSON_SCHEMA_PATH = OUTPUT_DIR / "canonical_semantics.schema.json"
MARKDOWN_PATH = OUTPUT_DIR / "CANONICAL_FINANCIAL_SEMANTICS.md"
METRICS_PATH = OUTPUT_DIR / "METRIC_REGISTRY.json"
CONSUMER_CONTRACT_PATH = OUTPUT_DIR / "consumer_contract.json"


# ── 1. JSON Schema ─────────────────────────────────────────────────────
def build_json_schema() -> dict:
    fg_items = [{"const": e.value, "title": e.name} for e in FinancialGroup]
    mp_items = [{"const": e.value, "title": e.name} for e in Marketplace]
    cr_items = [{"const": e.value, "title": e.name} for e in CashRole]
    et_items = [{"const": e.value, "title": e.name} for e in EventType]
    as_items = [{"const": e.value, "title": e.name} for e in AmountSign]

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "CanonicalFinancialSemantics",
        "description": "Single typed contract for all financial domains. Auto-generated from canonical_semantics.py.",
        "version": "1.0.0",
        "definitions": {
            "FinancialGroup": {
                "type": "string",
                "enum": [e.value for e in FinancialGroup],
                "description": "Certified financial groups",
                "oneOf": fg_items,
            },
            "CashRole": {
                "type": "string",
                "enum": [e.value for e in CashRole],
                "oneOf": cr_items,
            },
            "EventType": {
                "type": "string",
                "enum": [e.value for e in EventType],
                "oneOf": et_items,
            },
            "Marketplace": {
                "type": "string",
                "enum": [e.value for e in Marketplace],
                "oneOf": mp_items,
            },
            "AmountSign": {
                "type": "string",
                "enum": [e.value for e in AmountSign],
                "oneOf": as_items,
            },
            "UniquenessKey": {
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "key_fields": {"type": "array", "items": {"type": "string"}},
                    "rationale": {"type": "string"},
                },
                "required": ["table", "key_fields"],
            },
            "FinancialGroupMeta": {
                "type": "object",
                "properties": {
                    "display_name": {"type": "string"},
                    "pnl_order": {"type": "integer"},
                    "amount_sign": {"$ref": "#/definitions/AmountSign"},
                    "canonical_cash_role": {"$ref": "#/definitions/CashRole"},
                    "description": {"type": "string"},
                },
                "required": ["display_name", "pnl_order", "amount_sign", "canonical_cash_role"],
            },
            "MarketplaceMeta": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "display_name": {"type": "string"},
                    "ledger_uniqueness": {"$ref": "#/definitions/UniquenessKey"},
                    "has_signal_taxonomy": {"type": "boolean"},
                },
                "required": ["name", "display_name", "ledger_uniqueness"],
            },
            "MetricDefinition": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "display_name": {"type": "string"},
                    "description": {"type": "string"},
                    "source_table": {"type": "string"},
                    "granularity": {"type": "string"},
                    "formula_method": {"type": "string"},
                    "version": {"type": "string"},
                },
                "required": ["name", "display_name", "description", "source_table", "granularity", "formula_method"],
            },
        },
        "properties": {
            "financial_groups": {
                "type": "object",
                "additionalProperties": {
                    "oneOf": [{"$ref": "#/definitions/FinancialGroupMeta"}],
                },
                "propertyNames": {"$ref": "#/definitions/FinancialGroup"},
            },
            "marketplaces": {
                "type": "object",
                "additionalProperties": {
                    "oneOf": [{"$ref": "#/definitions/MarketplaceMeta"}],
                },
                "propertyNames": {"$ref": "#/definitions/Marketplace"},
            },
            "metrics": {
                "type": "object",
                "additionalProperties": {
                    "oneOf": [{"$ref": "#/definitions/MetricDefinition"}],
                },
            },
            "pnl_order": {
                "type": "array",
                "items": {"$ref": "#/definitions/FinancialGroup"},
            },
        },
    }


# ── 2. Markdown documentation ──────────────────────────────────────────
def build_markdown() -> str:
    lines = [
        "# Canonical Financial Semantics",
        "",
        "Auto-generated from `engine/v4/domain/canonical_semantics.py`.",
        "**Do not edit manually.** Run `python -m engine.v4.domain.generate_artifacts` to regenerate.",
        "",
        "---",
        "",
        "## Financial Groups",
        "",
        "| Enum Value | Display Name | P&L Order | Amount Sign | Cash Role | Description |",
        "|---|---|---|---|---|---|",
    ]
    for fg, meta in sorted(FINANCIAL_GROUP_META.items(), key=lambda x: x[1].pnl_order):
        lines.append(
            f"| `{fg.value}` | {meta.display_name} | {meta.pnl_order} | "
            f"{meta.amount_sign.value} | {meta.canonical_cash_role.value} | {meta.description} |"
        )

    lines += [
        "",
        "---",
        "",
        "## P&L Order",
        "",
    ]
    for i, name in enumerate(PNL_ORDER, 1):
        lines.append(f"{i}. `{name}`")

    lines += [
        "",
        "---",
        "",
        "## Marketplaces",
        "",
        "| Marketplace | Display Name | Uniqueness Key | Rationale | Signal Taxonomy |",
        "|---|---|---|---|---|",
    ]
    for mp, meta in sorted(MARKETPLACE_META.items(), key=lambda x: x[0].value):
        key = ", ".join(meta.ledger_uniqueness.key_fields)
        lines.append(
            f"| `{mp.value}` | {meta.display_name} | `{key}` | "
            f"{meta.ledger_uniqueness.rationale} | {'Yes' if meta.has_signal_taxonomy else 'No'} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Metric Registry",
        "",
        "| Metric | Display Name | Source Table | Granularity | Formula Method | Version | Evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, m in sorted(METRIC_REGISTRY.items()):
        lines.append(
            f"| `{name}` | {m.display_name} | `{m.source_table}` | {m.granularity} | "
            f"`{m.formula_method}` | {m.version} | {m.evidence} |"
        )

    return "\n".join(lines) + "\n"


# ── 3. Metrics inventory (JSON) ────────────────────────────────────────
def build_metrics_inventory() -> dict:
    return {
        "version": "1.0.0",
        "generated_from": "engine/v4/domain/canonical_semantics.py",
        "metrics": {
            name: {
                "name": m.name,
                "display_name": m.display_name,
                "description": m.description,
                "source_table": m.source_table,
                "granularity": m.granularity,
                "dimensions": list(m.dimensions),
                "exclusions": list(m.exclusions),
                "sign_convention": m.sign_convention,
                "formula_method": m.formula_method,
                "version": m.version,
                "owner": m.owner,
                "evidence": m.evidence,
                "is_derived": m.is_derived,
            }
            for name, m in METRIC_REGISTRY.items()
        },
    }


# ── 4. Consumer contract (list form) ──────────────────────────────────
def build_consumer_contract() -> dict:
    return {
        "contract_version": "1.0.0",
        "source": "engine/v4/domain/canonical_semantics.py",
        "enums": {
            "FinancialGroup": [e.value for e in FinancialGroup],
            "CashRole": [e.value for e in CashRole],
            "EventType": [e.value for e in EventType],
            "Marketplace": [e.value for e in Marketplace],
            "AmountSign": [e.value for e in AmountSign],
        },
        "registry_counts": {
            "financial_group_meta": len(FINANCIAL_GROUP_META),
            "pnl_order": len(PNL_ORDER),
            "marketplace_meta": len(MARKETPLACE_META),
            "metric_definitions": len(METRIC_REGISTRY),
        },
        "consumers": [
            {"name": "FinancialEngine", "uses": ["financial_group meta", "marketplace uniqueness", "metric definitions"]},
            {"name": "TraceabilityEngine", "uses": ["marketplace uniqueness", "validate helpers"]},
            {"name": "MarketplaceAuditor", "uses": ["financial_group values"]},
            {"name": "API", "uses": ["metric definitions", "financial_group meta", "pnl_order"]},
            {"name": "Dashboard", "uses": ["pnl_order", "financial_group meta"]},
            {"name": "Copilot", "uses": ["metric definitions", "financial_group meta"]},
            {"name": "EvidenceOrchestrator", "uses": ["metric definitions", "validate helpers"]},
        ],
    }


def write_artifact(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  Wrote {path.relative_to(REPO)}")


def write_json_artifact(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Wrote {path.relative_to(REPO)}")


def check_artifact(path: Path, expected: str) -> bool:
    if not path.exists():
        print(f"  MISSING {path.relative_to(REPO)}")
        return False
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        print(f"  MISMATCH {path.relative_to(REPO)}")
        return False
    print(f"  OK {path.relative_to(REPO)}")
    return True


def check_json_artifact(path: Path, expected: dict) -> bool:
    if not path.exists():
        print(f"  MISSING {path.relative_to(REPO)}")
        return False
    try:
        actual = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"  INVALID JSON {path.relative_to(REPO)}")
        return False
    if actual != expected:
        print(f"  MISMATCH {path.relative_to(REPO)}")
        return False
    print(f"  OK {path.relative_to(REPO)}")
    return True


def main():
    check_only = "--check-only" in sys.argv

    artifacts = [
        (JSON_SCHEMA_PATH, build_json_schema(), write_json_artifact, check_json_artifact),
        (MARKDOWN_PATH, build_markdown(), write_artifact, check_artifact),
        (METRICS_PATH, build_metrics_inventory(), write_json_artifact, check_json_artifact),
        (CONSUMER_CONTRACT_PATH, build_consumer_contract(), write_json_artifact, check_json_artifact),
    ]

    all_ok = True
    for path, content, writer, checker in artifacts:
        expected_text = json.dumps(content, indent=2, ensure_ascii=False) if isinstance(content, dict) else content
        if check_only:
            if isinstance(content, dict):
                ok = check_json_artifact(path, content)
            else:
                ok = check_artifact(path, content)
            if not ok:
                all_ok = False
        else:
            if isinstance(content, dict):
                write_json_artifact(path, content)
            else:
                write_artifact(path, content)

    if check_only:
        if all_ok:
            print("\nAll artifacts match contract.")
            return 0
        else:
            print("\nArtifacts DO NOT match contract. Run without --check-only to regenerate.")
            return 1
    else:
        print("\nArtifacts regenerated from canonical_semantics.py")
        return 0


if __name__ == "__main__":
    sys.exit(main())
