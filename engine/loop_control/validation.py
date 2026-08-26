"""Zero-dependency JSON Schema subset validator.

The repository .venv has no `jsonschema` package and the mission forbids adding a
mandatory third-party dependency. This module implements exactly the subset used
by engine/loop_control/schemas/*.json:

  type, required, properties, additionalProperties, enum, pattern,
  minLength, minItems, minimum, items

Behaviour is FAIL CLOSED: anything not understood, or any violation, raises
SchemaValidationError. Invalid structured state is never silently repaired.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from .constants import SchemaValidationError

SCHEMA_DIR = Path(__file__).parent / "schemas"

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


@lru_cache(maxsize=32)
def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.schema.json"
    if not path.exists():
        raise SchemaValidationError(f"schema not found: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def _check_type(value: Any, expected: Any, loc: str) -> None:
    types = expected if isinstance(expected, list) else [expected]
    for t in types:
        py = _TYPE_MAP.get(t)
        if py is None:
            raise SchemaValidationError(f"{loc}: unsupported schema type '{t}'")
        # bool is a subclass of int in Python; keep them distinct.
        if t in ("integer", "number") and isinstance(value, bool):
            continue
        if isinstance(value, py):
            return
    raise SchemaValidationError(f"{loc}: expected type {types}, got {type(value).__name__}")


def _validate_node(value: Any, schema: dict[str, Any], loc: str) -> None:
    if "type" in schema:
        _check_type(value, schema["type"], loc)

    if "enum" in schema and value not in schema["enum"]:
        raise SchemaValidationError(f"{loc}: value {value!r} not in enum {schema['enum']}")

    if isinstance(value, str):
        if "pattern" in schema and not re.match(schema["pattern"], value):
            raise SchemaValidationError(f"{loc}: value {value!r} does not match {schema['pattern']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise SchemaValidationError(f"{loc}: shorter than minLength {schema['minLength']}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise SchemaValidationError(f"{loc}: below minimum {schema['minimum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise SchemaValidationError(f"{loc}: fewer than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(value):
                _validate_node(item, item_schema, f"{loc}[{i}]")

    if isinstance(value, dict):
        props: dict[str, Any] = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                raise SchemaValidationError(f"{loc}: missing required field '{key}'")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(props))
            if extra:
                raise SchemaValidationError(f"{loc}: unexpected fields {extra}")
        for key, sub in props.items():
            if key in value:
                _validate_node(value[key], sub, f"{loc}.{key}")


def validate(record: Any, schema_name: str) -> None:
    """Validate a record against a named schema. Raises SchemaValidationError."""
    _validate_node(record, load_schema(schema_name), schema_name)


def is_valid(record: Any, schema_name: str) -> bool:
    try:
        validate(record, schema_name)
        return True
    except SchemaValidationError:
        return False
