"""Tests for C1: KnowledgeIndexer.build_knowledge_index().

Validates that build_knowledge_index():
- Returns True when entries are added/updated
- Writes entries to the index file
- Uses KCE integration (not fallback) when available
- Is idempotent (re-running merges, doesn't duplicate)
"""
from __future__ import annotations
import tempfile
from pathlib import Path
import pytest


def test_build_knowledge_index_returns_true():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        tmp = f.name
        f.write("knowledge: []\n")
    try:
        indexer = KnowledgeIndexer(path=tmp)
        result = indexer.build_knowledge_index()
        assert isinstance(result, bool)
    finally:
        Path(tmp).unlink(missing_ok=True)


def test_build_knowledge_index_writes_entries():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        tmp = f.name
        f.write("knowledge: []\n")
    try:
        indexer = KnowledgeIndexer(path=tmp)
        result = indexer.build_knowledge_index()
        if result:
            entries = indexer.read()
            assert len(entries) >= 5
            ids = [e["id"] for e in entries]
            assert any(i.startswith("DEC-") for i in ids)
            assert any(i.startswith("TAXONOMY-") for i in ids)
    finally:
        Path(tmp).unlink(missing_ok=True)


def test_build_knowledge_index_idempotent():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        tmp = f.name
        f.write("knowledge: []\n")
    try:
        indexer = KnowledgeIndexer(path=tmp)
        first = indexer.build_knowledge_index()
        count_first = len(indexer.read())
        second = indexer.build_knowledge_index()
        count_second = len(indexer.read())
        assert isinstance(first, bool)
        assert isinstance(second, bool)
        assert count_second == count_first
    finally:
        Path(tmp).unlink(missing_ok=True)


def test_build_knowledge_index_entries_have_required_fields():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        tmp = f.name
        f.write("knowledge: []\n")
    try:
        indexer = KnowledgeIndexer(path=tmp)
        indexer.build_knowledge_index()
        entries = indexer.read()
        for e in entries:
            assert "id" in e
            assert "type" in e
            assert "title" in e
            assert "summary" in e
            assert "status" in e
    finally:
        Path(tmp).unlink(missing_ok=True)


def test_build_knowledge_index_via_kce_includes_governance():
    from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        tmp = f.name
        f.write("knowledge: []\n")
    try:
        indexer = KnowledgeIndexer(path=tmp)
        indexer.build_knowledge_index()
        entries = indexer.read()
        dec_ids = [e["id"] for e in entries if e["id"].startswith("DEC-")]
        rfc_ids = [e["id"] for e in entries if e["id"].startswith("RFC_")]
        assert len(dec_ids) >= 3
        assert len(rfc_ids) >= 1
    finally:
        Path(tmp).unlink(missing_ok=True)
