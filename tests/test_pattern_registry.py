"""Tests for PatternRegistry."""
import pytest
import tempfile
from pathlib import Path
from engine.v4.knowledge.pattern_registry import (
    PatternRegistry, Pattern, PatternCategory, PatternStatus,
    get_registry, reset_registry,
)


@pytest.fixture
def registry():
    """Create a fresh registry for testing."""
    reset_registry()
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp_path = Path(f.name)
    reg = PatternRegistry(tmp_path)
    yield reg
    tmp_path.unlink(missing_ok=True)


class TestPatternRegistry:
    """Test PatternRegistry CRUD operations."""
    
    def test_add_and_get(self, registry):
        p = Pattern(
            id="TEST-001",
            category=PatternCategory.DECISION,
            title="Test Decision",
            summary="A test decision",
            detail="Full detail here",
            tags=["test", "decision"],
            marketplace="ML",
        )
        registry.add(p)
        
        retrieved = registry.get("TEST-001")
        assert retrieved is not None
        assert retrieved.id == "TEST-001"
        assert retrieved.title == "Test Decision"
        assert retrieved.category == PatternCategory.DECISION
        assert retrieved.marketplace == "ML"
        assert "test" in retrieved.tags
    
    def test_update_existing(self, registry):
        p = Pattern(
            id="TEST-002",
            category=PatternCategory.BUG,
            title="Original Title",
            summary="Original summary",
        )
        registry.add(p)
        
        # Update
        p.title = "Updated Title"
        p.summary = "Updated summary"
        p.tags = ["updated"]
        registry.add(p)
        
        retrieved = registry.get("TEST-002")
        assert retrieved.title == "Updated Title"
        assert retrieved.summary == "Updated summary"
        assert "updated" in retrieved.tags
        # created_at should be preserved
        assert retrieved.created_at is not None
    
    def test_soft_delete(self, registry):
        p = Pattern(id="TEST-003", category=PatternCategory.LESSON, title="To Delete", summary="")
        registry.add(p)
        
        assert registry.delete("TEST-003") is True
        retrieved = registry.get("TEST-003")
        assert retrieved.status == PatternStatus.ARCHIVED
        assert registry.delete("NONEXISTENT") is False
    
    def test_search_by_query(self, registry):
        registry.add(Pattern(id="BUG-001", category=PatternCategory.BUG, title="Login Bug", summary="Login fails"))
        registry.add(Pattern(id="DEC-001", category=PatternCategory.DECISION, title="Auth Decision", summary="Use OAuth"))
        registry.add(Pattern(id="BUG-002", category=PatternCategory.BUG, title="Payment Bug", summary="Payment timeout"))
        
        results = registry.search("Bug")
        assert len(results) == 2
        assert all("Bug" in r.title for r in results)
    
    def test_search_by_category(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.DECISION, title="A", summary=""))
        registry.add(Pattern(id="B", category=PatternCategory.BUG, title="B", summary=""))
        registry.add(Pattern(id="C", category=PatternCategory.DECISION, title="C", summary=""))
        
        decisions = registry.search(category=PatternCategory.DECISION)
        assert len(decisions) == 2
        assert all(r.category == PatternCategory.DECISION for r in decisions)
    
    def test_search_by_marketplace(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.LESSON, title="A", summary="", marketplace="ML"))
        registry.add(Pattern(id="B", category=PatternCategory.LESSON, title="B", summary="", marketplace="PARIS"))
        registry.add(Pattern(id="C", category=PatternCategory.LESSON, title="C", summary="", marketplace="ALL"))
        
        ml_results = registry.search(marketplace="ML")
        assert len(ml_results) == 2  # ML + ALL
        
        paris_results = registry.search(marketplace="PARIS")
        assert len(paris_results) == 2  # PARIS + ALL
    
    def test_search_by_tags(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.LESSON, title="A", summary="", tags=["python", "api"]))
        registry.add(Pattern(id="B", category=PatternCategory.LESSON, title="B", summary="", tags=["sql", "api"]))
        registry.add(Pattern(id="C", category=PatternCategory.LESSON, title="C", summary="", tags=["python"]))
        
        api_results = registry.search(tags=["api"])
        assert len(api_results) == 2
        
        python_results = registry.search(tags=["python"])
        assert len(python_results) == 2
        
        both = registry.search(tags=["python", "api"])
        assert len(both) == 1
    
    def test_search_by_status(self, registry):
        p1 = Pattern(id="A", category=PatternCategory.LESSON, title="A", summary="", status=PatternStatus.ACTIVE)
        p2 = Pattern(id="B", category=PatternCategory.LESSON, title="B", summary="", status=PatternStatus.ARCHIVED)
        registry.add(p1)
        registry.add(p2)
        
        active = registry.search(status=PatternStatus.ACTIVE)
        assert len(active) == 1
        assert active[0].id == "A"
    
    def test_by_category(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.DECISION, title="A", summary=""))
        registry.add(Pattern(id="B", category=PatternCategory.BUG, title="B", summary=""))
        
        decisions = registry.by_category(PatternCategory.DECISION)
        assert len(decisions) == 1
    
    def test_by_marketplace(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.LESSON, title="A", summary="", marketplace="ML"))
        registry.add(Pattern(id="B", category=PatternCategory.LESSON, title="B", summary="", marketplace="ALL"))
        
        ml = registry.by_marketplace("ML")
        assert len(ml) == 2
    
    def test_by_status(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.LESSON, title="A", summary="", status=PatternStatus.ACTIVE))
        registry.add(Pattern(id="B", category=PatternCategory.LESSON, title="B", summary="", status=PatternStatus.SUPERSEDED))
        
        active = registry.by_status(PatternStatus.ACTIVE)
        assert len(active) == 1
    
    def test_related(self, registry):
        p1 = Pattern(id="A", category=PatternCategory.DECISION, title="A", summary="", related_ids=["B"])
        p2 = Pattern(id="B", category=PatternCategory.BUG, title="B", summary="", related_ids=["A"])
        registry.add(p1)
        registry.add(p2)
        
        related = registry.get_related("A")
        assert len(related) == 1
        assert related[0].id == "B"
    
    def test_stats(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.DECISION, title="A", summary="", marketplace="ML"))
        registry.add(Pattern(id="B", category=PatternCategory.BUG, title="B", summary="", marketplace="ML"))
        registry.add(Pattern(id="C", category=PatternCategory.DECISION, title="C", summary="", marketplace="PARIS", status=PatternStatus.ARCHIVED))
        
        stats = registry.stats()
        assert stats["total"] == 3
        assert stats["by_category"]["decision"] == 2
        assert stats["by_category"]["bug"] == 1
        assert stats["by_status"]["active"] == 2
        assert stats["by_status"]["archived"] == 1
        assert stats["by_marketplace"]["ML"] == 2
        assert stats["by_marketplace"]["PARIS"] == 1
    
    def test_persistence(self, registry):
        p = Pattern(id="PERSIST-001", category=PatternCategory.LESSON, title="Persist Test", summary="")
        registry.add(p)
        
        # Create new registry instance with same file
        new_registry = PatternRegistry(registry.path)
        retrieved = new_registry.get("PERSIST-001")
        assert retrieved is not None
        assert retrieved.title == "Persist Test"
    
    def test_to_knowledge_index(self, registry):
        registry.add(Pattern(id="A", category=PatternCategory.DECISION, title="A", summary="Active", status=PatternStatus.ACTIVE))
        registry.add(Pattern(id="B", category=PatternCategory.BUG, title="B", summary="Archived", status=PatternStatus.ARCHIVED))
        
        index = registry.to_knowledge_index()
        assert len(index) == 1
        assert index[0]["id"] == "A"
    
    def test_pattern_to_dict_roundtrip(self):
        p = Pattern(
            id="ROUND-001",
            category=PatternCategory.BENCHMARK,
            title="Benchmark",
            summary="Summary",
            detail="Detail",
            tags=["perf", "sql"],
            marketplace="ALL",
            metadata={"key": "value"},
        )
        
        d = p.to_dict()
        assert d["id"] == "ROUND-001"
        assert d["category"] == "benchmark"
        assert d["tags"] == ["perf", "sql"]
        
        p2 = Pattern.from_dict(d)
        assert p2.id == p.id
        assert p2.category == p.category
        assert p2.tags == p.tags
        assert p2.metadata == p.metadata


class TestPatternRegistryIntegration:
    """Integration tests with KCE and Obsidian."""
    
    def test_sync_from_kce(self, registry):
        """Test syncing from KCE result."""
        from types import SimpleNamespace
        from dataclasses import dataclass, field
        
        @dataclass
        class KCEResult:
            audit_entries: list = field(default_factory=list)
            decision_entries: list = field(default_factory=list)
            taxonomy_entries: list = field(default_factory=list)
        
        kce_result = KCEResult(
            audit_entries=[
                {"id": "AUDIT-ML-001", "type": "audit", "title": "ML Audit Gap", "summary": "Missing audit rows", "status": "OPEN", "file": "governance/AUDIT_M.md"},
            ],
            decision_entries=[
                {"id": "DEC-019", "type": "decision", "title": "PosCobro SAME_EVENT", "summary": "Flag paired as non-operational", "status": "ACTIVE", "file": "governance/DEC019.md"},
            ],
            taxonomy_entries=[
                {"id": "TAXONOMY-RIPLEY", "type": "taxonomy", "title": "Ripley Signal/Noise", "summary": "12 SIGNAL / 20 NOISE", "status": "CERTIFIED", "file": "knowledge/taxonomy/ripley_v1.json"},
            ],
        )
        
        added = registry.sync_from_kce(kce_result)
        assert added == 3
        
        # Verify patterns created
        assert registry.get("AUDIT-ML-001").category == PatternCategory.AUDIT
        assert registry.get("DEC-019").category == PatternCategory.DECISION
        assert registry.get("TAXONOMY-RIPLEY").category == PatternCategory.TAXONOMY
    
    def test_obsidian_sync(self, registry):
        """Test syncing from Obsidian markdown files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            
            # Create test markdown files
            (vault / "DEC-019.md").write_text("""---
tags: [decision, poscobro]
marketplace: ML
---

# DEC-019 PosCobro SAME_EVENT

PosCobro paired mechanisms are the same economic event as devoluciones.

## Detail

Flag 3,663 rows with include_in_operational_pnl=0.
""", encoding="utf-8")
            
            (vault / "BUG-2026-06-001.md").write_text("""---
tags: [bug, encoding]
marketplace: RIPLEY
---

# BUG: Encoding Issue

XLSX files read with wrong encoding.

## Detail

pd.read_excel without encoding caused mojibake.
""", encoding="utf-8")
            
            added = registry.sync_from_obsidian(vault)
            assert added == 2
            
            dec = registry.get("DEC-019")
            assert dec.category == PatternCategory.DECISION
            assert "poscobro" in dec.tags
            assert dec.marketplace == "ML"
            
            bug = registry.get("BUG-2026-06-001")
            assert bug.category == PatternCategory.BUG
            assert bug.marketplace == "RIPLEY"


class TestSingleton:
    """Test singleton behavior."""
    
    def test_singleton(self):
        reset_registry()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            tmp = Path(f.name)
        
        try:
            r1 = get_registry(tmp)
            r2 = get_registry(tmp)
            assert r1 is r2
            
            r1.add(Pattern(id="SINGLE-001", category=PatternCategory.LESSON, title="Test", summary=""))
            assert r2.get("SINGLE-001") is not None
        finally:
            tmp.unlink(missing_ok=True)
            reset_registry()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])