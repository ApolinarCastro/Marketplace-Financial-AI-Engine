"""Marketplace Pattern Registry — Unified knowledge consolidation.

Integrates KCE (audit/decision/taxonomy scanning) + Obsidian (governance model) 
+ Knowledge API (query interface) into a single permanent registry.

Stores:
- DEC, RFC, Auditorías
- Bugs históricos, Anti-patterns, Buenas prácticas
- Benchmarks, Skills, Taxonomías
- Experiencias externas, Lecciones aprendidas
"""
from __future__ import annotations
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum

from engine.v4.database import DatabaseV4
from engine.v4.knowledge.kce import KnowledgeConsolidationEngine, KCEConfig
from engine.v4.knowledge.audit_scanner import AuditScanner
from engine.v4.knowledge.decision_parser import DecisionParser
from engine.v4.knowledge.knowledge_indexer import KnowledgeIndexer
from engine.v4.knowledge.retention_manager import RetentionManager


class PatternCategory(Enum):
    """Categories of patterns in the registry."""
    DECISION = "decision"           # DEC, RFC
    AUDIT = "audit"                 # Auditoría findings
    BUG = "bug"                     # Historical bugs & fixes
    ANTI_PATTERN = "anti_pattern"   # Known anti-patterns
    BEST_PRACTICE = "best_practice" # Recommended patterns
    BENCHMARK = "benchmark"         # Performance benchmarks
    SKILL = "skill"                 # Reusable skills/modules
    TAXONOMY = "taxonomy"           # Marketplace taxonomies
    EXTERNAL = "external"           # External project learnings
    LESSON = "lesson"               # Lessons learned


class PatternStatus(Enum):
    """Lifecycle status of a pattern."""
    ACTIVE = "active"               # Currently applicable
    SUPERSEDED = "superseded"       # Replaced by newer pattern
    ARCHIVED = "archived"           # Historical reference only
    DEPRECATED = "deprecated"       # No longer recommended


@dataclass
class Pattern:
    """A single pattern entry in the registry."""
    id: str                         # Unique identifier (e.g., "DEC-019", "BUG-2026-06-001")
    category: PatternCategory
    title: str
    summary: str
    detail: str = ""
    status: PatternStatus = PatternStatus.ACTIVE
    tags: list[str] = field(default_factory=list)
    marketplace: str | None = None  # ML, PARIS, RIPLEY, FALABELLA, ALL
    source_file: str | None = None  # Origin governance file
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    related_ids: list[str] = field(default_factory=list)  # Links to other patterns
    metadata: dict = field(default_factory=dict)          # Extensible extra data
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d["category"] = self.category.value
        d["status"] = self.status.value
        return d
    
    @classmethod
    def from_dict(cls, data: dict) -> "Pattern":
        data = data.copy()
        data["category"] = PatternCategory(data["category"])
        data["status"] = PatternStatus(data["status"])
        return cls(**data)


class PatternRegistry:
    """Unified registry for all marketplace patterns.
    
    Single source of truth combining:
    - KCE auto-discovered knowledge
    - Obsidian governance model
    - Knowledge API queryable entries
    """
    
    def __init__(self, registry_path: str | Path = "knowledge/patterns.json"):
        self.path = Path(registry_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._patterns: dict[str, Pattern] = {}
        self._load()
    
    def _load(self):
        """Load patterns from JSON file."""
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        return
                    data = json.loads(content)
                for pdata in data.get("patterns", []):
                    p = Pattern.from_dict(pdata)
                    self._patterns[p.id] = p
            except json.JSONDecodeError:
                # Corrupted file - start fresh
                pass
    
    def _save(self):
        """Persist patterns to JSON file."""
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "patterns": [p.to_dict() for p in self._patterns.values()]
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # ═══════════════════════════════════════════════════════════════════
    # CRUD OPERATIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def add(self, pattern: Pattern) -> Pattern:
        """Add or update a pattern."""
        existing = self._patterns.get(pattern.id)
        if existing:
            # Preserve created_at, update updated_at
            pattern.created_at = existing.created_at
            pattern.updated_at = datetime.now().isoformat()
        self._patterns[pattern.id] = pattern
        self._save()
        return pattern
    
    def get(self, pattern_id: str) -> Pattern | None:
        """Retrieve a pattern by ID."""
        return self._patterns.get(pattern_id)
    
    def delete(self, pattern_id: str) -> bool:
        """Delete a pattern (soft delete - marks ARCHIVED)."""
        if pattern_id in self._patterns:
            self._patterns[pattern_id].status = PatternStatus.ARCHIVED
            self._patterns[pattern_id].updated_at = datetime.now().isoformat()
            self._save()
            return True
        return False
    
    # ═══════════════════════════════════════════════════════════════════
    # QUERY OPERATIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def search(
        self,
        query: str = "",
        category: PatternCategory | None = None,
        status: PatternStatus | None = None,
        marketplace: str | None = None,
        tags: list[str] | None = None,
    ) -> list[Pattern]:
        """Search patterns with filters."""
        results = []
        q_lower = query.lower()
        
        for p in self._patterns.values():
            if status and p.status != status:
                continue
            if category and p.category != category:
                continue
            if marketplace and p.marketplace and p.marketplace != "ALL" and p.marketplace != marketplace:
                continue
            if tags and not all(t in p.tags for t in tags):
                continue
            if query:
                haystack = f"{p.title} {p.summary} {p.detail} {' '.join(p.tags)}".lower()
                if q_lower not in haystack:
                    continue
            results.append(p)
        
        # Sort by relevance (exact ID match first, then title match, then date)
        results.sort(key=lambda p: (
            0 if q_lower == p.id.lower() else
            1 if q_lower in p.title.lower() else
            2,
            -datetime.fromisoformat(p.updated_at).timestamp()
        ))
        return results
    
    def by_category(self, category: PatternCategory) -> list[Pattern]:
        return [p for p in self._patterns.values() if p.category == category]
    
    def by_marketplace(self, mp: str) -> list[Pattern]:
        return [p for p in self._patterns.values() 
                if p.marketplace in (mp, "ALL")]
    
    def by_status(self, status: PatternStatus) -> list[Pattern]:
        return [p for p in self._patterns.values() if p.status == status]
    
    def get_related(self, pattern_id: str) -> list[Pattern]:
        """Get patterns related to the given pattern."""
        p = self._patterns.get(pattern_id)
        if not p:
            return []
        return [self._patterns[rid] for rid in p.related_ids if rid in self._patterns]
    
    def get_all(self) -> list[Pattern]:
        return list(self._patterns.values())
    
    def stats(self) -> dict:
        """Registry statistics."""
        by_cat = {}
        by_status = {}
        by_mp = {}
        
        for p in self._patterns.values():
            by_cat[p.category.value] = by_cat.get(p.category.value, 0) + 1
            by_status[p.status.value] = by_status.get(p.status.value, 0) + 1
            if p.marketplace:
                by_mp[p.marketplace] = by_mp.get(p.marketplace, 0) + 1
        
        return {
            "total": len(self._patterns),
            "by_category": by_cat,
            "by_status": by_status,
            "by_marketplace": by_mp,
        }
    
    # ═══════════════════════════════════════════════════════════════════
    # KCE INTEGRATION
    # ═══════════════════════════════════════════════════════════════════
    
    def sync_from_kce(self, kce_result) -> int:
        """Sync patterns from KCE consolidation result.
        
        Converts KCE entries (audit, decision, taxonomy) to Pattern objects.
        """
        added = 0
        
        # Map KCE entry types to Pattern categories
        type_map = {
            "audit": PatternCategory.AUDIT,
            "decision": PatternCategory.DECISION,
            "taxonomy": PatternCategory.TAXONOMY,
        }
        
        for entry in (kce_result.audit_entries + kce_result.decision_entries + 
                      kce_result.taxonomy_entries):
            kid = entry.get("id", "")
            if not kid:
                continue
            
            cat = type_map.get(entry.get("type", ""), PatternCategory.LESSON)
            
            # Check if pattern exists
            if kid in self._patterns:
                # Update existing
                p = self._patterns[kid]
                p.summary = entry.get("summary", p.summary)
                p.detail = entry.get("summary", p.detail)  # KCE doesn't have detail
                p.status = PatternStatus.ACTIVE if entry.get("status") == "CERTIFIED" else PatternStatus.ACTIVE
                p.tags = list(set(p.tags + [entry.get("type", ""), p.marketplace or "ALL"]))
                p.updated_at = datetime.now().isoformat()
            else:
                # Create new
                p = Pattern(
                    id=kid,
                    category=cat,
                    title=entry.get("title", kid),
                    summary=entry.get("summary", ""),
                    detail="",
                    status=PatternStatus.ACTIVE,
                    tags=[entry.get("type", ""), "ALL"],
                    marketplace="ALL",
                    source_file=entry.get("file", ""),
                )
                self.add(p)
                added += 1
        
        return added
    
    def sync_from_obsidian(self, vault_path: Path) -> int:
        """Sync patterns from Obsidian vault (markdown files).
        
        Reads governance/*.md files and creates/updates patterns.
        """
        added = 0
        if not vault_path.exists():
            return 0
        
        for md_file in vault_path.glob("*.md"):
            # Parse markdown frontmatter and content
            content = md_file.read_text(encoding="utf-8")
            pattern = self._parse_obsidian_note(md_file.stem, content)
            if pattern:
                if pattern.id in self._patterns:
                    self._patterns[pattern.id].detail = pattern.detail
                    self._patterns[pattern.id].summary = pattern.summary
                    self._patterns[pattern.id].tags = list(
                        set(self._patterns[pattern.id].tags + pattern.tags)
                    )
                    self._patterns[pattern.id].updated_at = datetime.now().isoformat()
                else:
                    self.add(pattern)
                    added += 1
        
        self._save()
        return added
    
    def _parse_obsidian_note(self, filename: str, content: str) -> Pattern | None:
        """Parse Obsidian markdown note into Pattern."""
        # Extract frontmatter if present
        frontmatter = {}
        body = content
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                import yaml
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except:
                    pass
        
        # Determine category from filename/tags
        cat = PatternCategory.LESSON
        fname_lower = filename.lower()
        if "dec-" in fname_lower or "rfc_" in fname_lower:
            cat = PatternCategory.DECISION
        elif "audit" in fname_lower:
            cat = PatternCategory.AUDIT
        elif "bug" in fname_lower:
            cat = PatternCategory.BUG
        elif "benchmark" in fname_lower:
            cat = PatternCategory.BENCHMARK
        elif "taxonomy" in fname_lower:
            cat = PatternCategory.TAXONOMY
        
        # Extract first paragraph as summary
        summary = ""
        for line in body.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                summary = line[:200]
                break
        
        # Generate ID from filename
        pid = filename.upper().replace(" ", "_")
        
        return Pattern(
            id=pid,
            category=cat,
            title=filename.replace("_", " ").replace("-", " "),
            summary=summary,
            detail=body[:5000],  # Limit detail length
            tags=list(frontmatter.get("tags", [])) + [cat.value],
            marketplace=frontmatter.get("marketplace", "ALL"),
            source_file=str(md_file) if 'md_file' in locals() else filename,
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # EXPORT / INTEGRATION
    # ═══════════════════════════════════════════════════════════════════
    
    def to_knowledge_index(self) -> list[dict]:
        """Export to Knowledge API compatible format."""
        return [
            {
                "id": p.id,
                "type": p.category.value,
                "title": p.title,
                "summary": p.summary,
                "status": p.status.value,
                "tags": p.tags,
                "marketplace": p.marketplace,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in self._patterns.values()
            if p.status == PatternStatus.ACTIVE
        ]
    
    def to_obsidian(self, vault_path: Path) -> int:
        """Export patterns as Obsidian markdown files."""
        vault_path.mkdir(parents=True, exist_ok=True)
        written = 0
        
        for p in self._patterns.values():
            if p.status == PatternStatus.ARCHIVED:
                continue
            
            fname = vault_path / f"{p.id}.md"
            content = f"""---
id: {p.id}
category: {p.category.value}
status: {p.status.value}
tags: {p.tags}
marketplace: {p.marketplace or "ALL"}
created: {p.created_at}
updated: {p.updated_at}
related: {p.related_ids}
source: {p.source_file or "registry"}
---

# {p.title}

{p.summary}

## Detail

{p.detail}

## Metadata

- **Category:** {p.category.value}
- **Status:** {p.status.value}
- **Marketplace:** {p.marketplace or "ALL"}
- **Tags:** {", ".join(p.tags)}
- **Related:** {", ".join(p.related_ids) or "None"}
"""
            fname.write_text(content, encoding="utf-8")
            written += 1
        
        return written


# ═══════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE
# ═══════════════════════════════════════════════════════════════════

_registry_instance: PatternRegistry | None = None

def get_registry(path: str | Path = "knowledge/patterns.json") -> PatternRegistry:
    """Get singleton PatternRegistry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = PatternRegistry(path)
    return _registry_instance


def reset_registry():
    """Reset singleton for testing."""
    global _registry_instance
    _registry_instance = None