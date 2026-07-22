# DEC-025: Taxonomy YAML Authority

**Status**: CERTIFIED  
**Date**: 2026-06-16  
**Author**: System (Phase 11)

## Decision

`taxonomy/taxonomy_rules.yaml` and `taxonomy/taxonomy_mappings.yaml` are the **single source of taxonomy truth**. All classification logic must derive from YAML, not hardcoded Python maps.

## Rationale

- 8 financial groups, 163 concepts, 285 raw detail → concept mappings
- Dual-mode with `USE_YAML_TAXONOMY` flag for instant rollback (< 1 min)
- 18 taxonomy equivalence tests PASS — $0 delta, 207,600 rows verified
- `taxonomy/taxonomy_loader.py` is read-only (load, validate, resolve)

## Scope

- Taxonomy rules: sign_behavior, order, pnl flags → taxonomy_rules.yaml
- Mappings: raw_detail → concept + financial_group → taxonomy_mappings.yaml
- Legacy Python maps `_LEGACY_CONCEPT_MAP` kept READ-ONLY for rollback

## Frozen Interface

```python
class TaxonomyLoader:
    def load_rules() -> dict       # reads taxonomy_rules.yaml
    def load_mappings() -> dict    # reads taxonomy_mappings.yaml
    def resolve_financial_group(detalle) -> tuple
    def validate_taxonomy() -> list
    def normalize_detail(detalle) -> str
```

## Rollback

Set `USE_YAML_TAXONOMY = False` in `financial_engine.py`. System falls back to `_LEGACY_CONCEPT_MAP` instantly.
