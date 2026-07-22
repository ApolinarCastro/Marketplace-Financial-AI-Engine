"""Tests for Phase 12.6 — Knowledge System."""
from __future__ import annotations
import pytest
import yaml
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_knowledge_index_exists():
    path = ROOT / "knowledge_index.yaml"
    assert path.exists()


def test_knowledge_index_valid_yaml():
    path = ROOT / "knowledge_index.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None
    assert "knowledge" in data


def test_knowledge_has_entries():
    path = ROOT / "knowledge_index.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data["knowledge"]
    assert len(entries) >= 10


def test_knowledge_entries_have_required_fields():
    path = ROOT / "knowledge_index.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for entry in data["knowledge"]:
        assert "id" in entry
        assert "type" in entry
        assert "title" in entry
        assert "summary" in entry
        assert "status" in entry
        assert entry["type"] in ("governance", "certification", "audit", "taxonomy", "decision")


def test_knowledge_searchable():
    path = ROOT / "knowledge_index.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    gov = [e for e in data["knowledge"] if e["type"] == "governance"]
    cert = [e for e in data["knowledge"] if e["type"] == "certification"]
    audit = [e for e in data["knowledge"] if e["type"] == "audit"]
    assert len(gov) >= 2
    assert len(cert) >= 1
    assert len(audit) >= 1
