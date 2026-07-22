# P36.1 — MARKETPLACE PATTERN REGISTRY

**Fecha:** 2026-07-09
**Fase:** P36.1 — Surgical Knowledge & Validation Consolidation
**Fuente:** FASE 4 — Pattern Registry Implementation

---

## ARQUITECTURA DEL REGISTRO

```
┌─────────────────────────────────────────────────────────────────┐
│                    MARKETPLACE PATTERN REGISTRY                  │
│                     (Single Source of Truth)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │     KCE      │    │   OBSIDIAN   │    │ KNOWLEDGE    │       │
│  │  (Scanner)   │    │   (Vault)    │    │    API       │       │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PATTERN REGISTRY (JSON)                      │   │
│  │  knowledge/patterns.json  │  Singleton: get_registry()    │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Knowledge   │    │   Obsidian   │    │  Human Query │       │
│  │   Index      │    │   Sync       │    │  Interface   │       │
│  │  (API)       │    │  (Markdown)  │    │  (Search)    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ESQUEMA DE DATOS

### Pattern (Entrada principal)

```python
@dataclass
class Pattern:
    id: str                              # Unique: "DEC-019", "BUG-2026-06-001"
    category: PatternCategory            # 10 categorías
    title: str                           # Human readable
    summary: str                         # One-liner
    detail: str                          # Full markdown body
    status: PatternStatus                # ACTIVE/SUPERSEDED/ARCHIVED/DEPRECATED
    tags: list[str]                      # ["poscobro", "ml", "decision"]
    marketplace: str | None              # "ML", "PARIS", "RIPLEY", "FALABELLA", "ALL"
    source_file: str | None              # Origen: governance/, knowledge/, vault/
    created_at: str                      # ISO timestamp
    updated_at: str                      # ISO timestamp
    related_ids: list[str]               # ["DEC-019", "AUDIT-ML-001"]
    metadata: dict                       # Extensible extra data
```

### Categorías (PatternCategory)

| Enum Value | Descripción | Ejemplos reales |
|---|---|---|
| `DECISION` | DEC, RFC oficiales | DEC-019 (PosCobro), RFC_PARIS_ECONOMIC_MODEL |
| `AUDIT` | Hallazgos de auditoría | AUDIT-ML-001 (cargo_sin_respaldo), AUDIT-RIPLEY-FOLIO |
| `BUG` | Bugs históricos con fix | BUG-2026-06-001 (encoding), BUG-2026-05-012 (date parsing) |
| `ANTI_PATTERN` | Anti-patterns documentados | SELECT *, N+1, hardcoded marketplace |
| `BEST_PRACTICE` | Patrones recomendados | LOWER() mandatory, signal_mode=SIGNAL, Decimal for money |
| `BENCHMARK` | Baselines de performance | exec_summary: 45ms p50, waterfall: 38ms p50 |
| `SKILL` | Módulos reutilizables | query_guard, golden_tests, benchmark_runner |
| `TAXONOMY` | Taxonomías marketplace | ripley_v1.json (12S/20N), ml_v1.json (70S/1N) |
| `EXTERNAL` | Learnings externos | P36 QWED Finance Guard, AgentFactory plugins |
| `LESSON` | Lecciones aprendidas | "Always use LOWER()", "Period bug: end=None → YTD" |

### Estados (PatternStatus)

| Estado | Significado | Transiciones permitidas |
|---|---|---|
| `ACTIVE` | Vigente, aplicable | → SUPERSEDED, ARCHIVED, DEPRECATED |
| `SUPERSEDED` | Reemplazado por versión nueva | → ARCHIVED |
| `ARCHIVED` | Histórico, solo referencia | (terminal) |
| `DEPRECATED` | No recomendado, uso legacy | → ARCHIVED |

---

## OPERACIONES PRINCIPALES

### CRUD Básico

```python
from engine.v4.knowledge.pattern_registry import get_registry, Pattern, PatternCategory, PatternStatus

reg = get_registry()

# Create
p = Pattern(
    id="DEC-019",
    category=PatternCategory.DECISION,
    title="PosCobro PAIRED = SAME_EVENT",
    summary="3,663 paired rows flagged non-operational",
    detail="Full markdown...",
    tags=["poscobro", "ml", "decision"],
    marketplace="ML",
)
reg.add(p)

# Read
p = reg.get("DEC-019")

# Update (preserves created_at)
p.summary = "Updated summary"
reg.add(p)

# Soft delete (marks ARCHIVED)
reg.delete("DEC-019")
```

### Búsqueda Avanzada

```python
# Texto libre (título, summary, detail, tags)
reg.search("poscobro")

# Por categoría
reg.search(category=PatternCategory.DECISION)

# Por marketplace (incluye "ALL")
reg.search(marketplace="ML")

# Por tags (AND logic)
reg.search(tags=["poscobro", "ml"])

# Por estado
reg.search(status=PatternStatus.ACTIVE)

# Combinado
reg.search("encoding", category=PatternCategory.BUG, marketplace="RIPLEY", tags=["2026"])
```

### Filtros Directos

```python
reg.by_category(PatternCategory.BUG)       # Todos los bugs
reg.by_marketplace("ML")                   # ML + ALL
reg.by_status(PatternStatus.ACTIVE)        # Solo activos
reg.get_related("DEC-019")                 # Patrones vinculados
```

### Estadísticas

```python
stats = reg.stats()
# {
#   "total": 1247,
#   "by_category": {"decision": 45, "audit": 234, "bug": 89, ...},
#   "by_status": {"active": 1100, "archived": 147, "superseded": 0},
#   "by_marketplace": {"ALL": 800, "ML": 234, "PARIS": 112, "RIPLEY": 98, "FALABELLA": 45}
# }
```

---

## SINCRONIZACIÓN AUTOMÁTICA

### Desde KCE (Knowledge Consolidation Engine)

```python
kce = KnowledgeConsolidationEngine(db=db)
result = kce.consolidate()  # Escanea auditorías, governance, taxonomías

reg = get_registry()
added = reg.sync_from_kce(result)
# Convierte:
# - audit_entries → PatternCategory.AUDIT
# - decision_entries → PatternCategory.DECISION  
# - taxonomy_entries → PatternCategory.TAXONOMY
```

### Desde Obsidian Vault

```python
reg = get_registry()
added = reg.sync_from_obsidian(Path("docs/vault"))
# Lee *.md con frontmatter YAML:
# ---
# tags: [decision, poscobro]
# marketplace: ML
# ---
# # DEC-019 PosCobro SAME_EVENT
# ...
```

### Hacia Knowledge API

```python
index = reg.to_knowledge_index()
# Returns list[dict] compatible con /api/v4/knowledge
```

### Hacia Obsidian (Markdown)

```python
written = reg.to_obsidian(Path("docs/vault"))
# Escribe *.md con frontmatter YAML + body markdown
```

---

## ELIMINACIÓN DE DUPLICIDAD DOCUMENTAL

### Antes (Fragmentado)
| Fuente | Formato | Ejemplos |
|---|---|---|
| `governance/*.md` | Markdown | 500+ archivos, sin índice unificado |
| `knowledge_index.yaml` | YAML | 19 entradas manuales |
| `knowledge/taxonomy/*.json` | JSON | 4 archivos, sin metadata |
| KCE scanner | Runtime | No persistía resultados |
| Obsidian vault | Markdown | Desconectado del código |

### Después (Unificado)
| Atributo | Implementación |
|---|---|
| **Single source** | `knowledge/patterns.json` |
| **Schema enforced** | Pattern dataclass + validation |
| **Queryable** | Search by text, category, MP, tags, status |
| **Sync automated** | KCE + Obsidian → Registry (unidireccional) |
| **Export ready** | Knowledge API, Obsidian markdown, Stats |
| **Deduplicated** | ID único, merge inteligente (tags, related_ids) |
| **Lifecycle managed** | Status transitions, soft delete |

### Deduplicación en Merge
```python
# Al añadir patrón existente:
existing = reg.get("DEC-019")
new = Pattern(id="DEC-019", tags=["poscobro", "ml", "decision", "same_event"])
reg.add(new)
# Resultado:
# - created_at: preservado (original)
# - updated_at: now
# - tags: union (deduplicado)
# - related_ids: union
# - detail: sobrescrito si más largo
```

---

## INTEGRACIÓN CON COMPONENTES P36.1

| Componente | Patrón generado | Categoría |
|---|---|---|
| **Golden Tests** | `SKILL-GOLDEN-TESTS` | SKILL |
| **Benchmark Framework** | `SKILL-BENCHMARK`, `BENCH-EXEC-SUMMARY` | SKILL, BENCHMARK |
| **QueryGuard** | `SKILL-QUERY-GUARD`, `ANTI-PATTERN-SELECT-STAR` | SKILL, ANTI_PATTERN |
| **KCE** | Auto-sync de auditorías/DECs/taxonomías | AUDIT, DECISION, TAXONOMY |

---

## RUTAS Y ARCHIVOS

| Ruta | Descripción |
|---|---|
| `knowledge/patterns.json` | Registro persistente (JSON) |
| `engine/v4/knowledge/pattern_registry.py` | Implementación |
| `tests/test_pattern_registry.py` | 19 tests |
| `docs/vault/` | Obsidian sync target |

---

## EJEMPLO DE ENTRADA REAL

```json
{
  "id": "DEC-019",
  "category": "decision",
  "title": "PosCobro PAIRED = SAME_EVENT",
  "summary": "3,663 paired PosCobro rows flagged non-operational ($94.4M)",
  "detail": "# DEC-019 Execution Report\n\n## Context\nPosCobro paired mechanisms (BPP + Poscobro Conciliado) represent the same economic event as devoluciones...\n\n## Decision\nUPDATE marketplace_ledger_v1 SET include_in_operational_pnl=0 WHERE paired_condition...\n\n## Impact\nRN operational: $719.9M → $625.6M (-$94.4M). $0 delta SFT.",
  "status": "active",
  "tags": ["poscobro", "ml", "decision", "paired", "same_event"],
  "marketplace": "ML",
  "source_file": "governance/DEC019_EXECUTION_REPORT.md",
  "created_at": "2026-06-07T16:13:24",
  "updated_at": "2026-06-07T16:13:24",
  "related_ids": ["AUDIT-ML-POSCOBRO", "ECONOMIC_EVENT_TRUTH_CERTIFICATION", "POSCOBRO_DELETION_DECISION"],
  "metadata": {
    "rows_affected": 3663,
    "amount_millions": 94.4,
    "rn_before": 719.9,
    "rn_after": 625.6
  }
}
```

---

## PRÓXIMOS PASOS (Post-P36.1)

1. **Poblar Registry:** `kce.consolidate()` → `reg.sync_from_kce()` → `reg.sync_from_obsidian()`
2. **CI/CD Hook:** Validar que nuevos governance files generen patterns automáticamente
3. **Knowledge API:** Exponer `/api/v4/patterns` con filtros
4. **Dashboard:** Visualizador de patrones por categoría/marketplace/status
5. **Alertas:** Notificar cuando pattern status cambie a SUPERSEDED/DEPRECATED