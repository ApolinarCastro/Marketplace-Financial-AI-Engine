#!/usr/bin/env python3
"""
FDE Assurance Score Validator — Marketplace Financial Operating System

Computes the FDE Assurance Score (0-100) for a deliverable based on:
- Claim falsifiability (25 pts)
- Contradiction/known limits (25 pts)
- Evidence trail (30 pts)
- Anti-pattern compliance (20 pts)

Usage:
    python scripts/validate_fde_score.py --deliverable governance/RIPLEY_XML_COVERAGE_DISCOVERY.md
    python scripts/validate_fde_score.py --evidence-dir evidence/fase_1b/ --task TASK-XXXX
"""

import json
import re
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FDEScore:
    claim: int = 0          # 0-25
    contradiction: int = 0  # 0-25
    evidence: int = 0       # 0-30
    anti_patterns: int = 0  # 0-20
    total: int = 0
    verdict: str = ""
    details: Dict = None

    def __post_init__(self):
        self.total = self.claim + self.contradiction + self.evidence + self.anti_patterns
        if self.total >= 85:
            self.verdict = "ELIGIBLE_FOR_CERTIFICATION"
        elif self.total >= 70:
            self.verdict = "NEEDS_STRENGTHENING"
        else:
            self.verdict = "INSUFFICIENT"


class FDEValidator:
    """Validates FDE Assurance Score for Marketplace deliverables."""
    
    # Anti-patterns specific to Marketplace Financial OS
    ANTI_PATTERNS = [
        (r"just use (AI|ML|TimesFM)", "buzzword_inflation"),
        (r"trust me", "trust_me_bro"),
        (r"(magic number|hardcoded|hard-coded)\s*[=:]\s*\d+\.?\d*", "magic_number"),
        (r"CERTIFIED|PASS|VERIFIED.*(?!(execution_id|commit|evidence))", "self_certification"),
        (r"agentic|autonomous|swarm", "buzzword_inflation"),
        (r"https?://[^\s]+\.(ai|io|dev|app)", "fake_url"),
        (r"mapDetalleToConcept|calculateWaterfall|computeMargin", "frontend_financial_logic"),
        (r"RAW|01_Raw.*(read|load|parse)", "raw_dependency_post_ingestion"),
        (r"PosCobro.*(include|pnl|revenue)", "dec019_violation"),
        (r"marketplace.*(ML|PARIS|FALABELLA|RIPLEY).*marketplace", "cross_mp_contamination"),
    ]
    
    # Required evidence fields (FASE 1B-R5)
    REQUIRED_EVIDENCE_FIELDS = [
        "execution_id", "commit", "timestamp", "harness_version",
        "repository", "branch", "unique_tests", "aggregate_executions",
        "execution_groups", "implementation_status", "validation_status",
        "certification_status", "classification"
    ]

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.evidence_dir = repo_root / "evidence" / "fase_1b"

    def validate_deliverable(self, deliverable_path: Path) -> FDEScore:
        """Validate a single deliverable (markdown report)."""
        content = deliverable_path.read_text(encoding='utf-8')
        
        score = FDEScore()
        score.details = {
            "file": str(deliverable_path),
            "claim_checks": [],
            "contradiction_checks": [],
            "evidence_checks": [],
            "anti_pattern_violations": []
        }
        
        # 1. CLAIM (falsifiable, specific, quantified)
        score.claim = self._score_claim(content, score.details)
        
        # 2. CONTRADICTION (known limits, coverage gaps, assumptions)
        score.contradiction = self._score_contradiction(content, score.details)
        
        # 3. EVIDENCE TRAIL (file:line + SHA-256 + execution_id)
        score.evidence = self._score_evidence(content, deliverable_path, score.details)
        
        # 4. ANTI-PATTERNS
        score.anti_patterns = self._score_anti_patterns(content, score.details)
        
        score.__post_init__()
        return score

    def _score_claim(self, content: str, details: Dict) -> int:
        """Score claim falsifiability (0-25)."""
        points = 0
        checks = []
        
        # Specific financial metric mentioned
        if re.search(r"\$[\d,]+\.?\d*\s*(M|B|millones?|billones?)", content, re.IGNORECASE):
            points += 5
            checks.append("✅ Specific monetary amount")
        else:
            checks.append("❌ No specific monetary amount")
        
        # Specific marketplace(s)
        mps = re.findall(r"\b(ML|PARIS|FALABELLA|RIPLEY|MERCADO LIBRE|MERCADOLIBRE)\b", content, re.IGNORECASE)
        if mps:
            points += 5
            checks.append(f"✅ Marketplace(s) identified: {set(m.upper() for m in mps)}")
        else:
            checks.append("❌ No specific marketplace")
        
        # Specific period(s)
        if re.search(r"\b(202[0-9]-(0[1-9]|1[0-2])|Q[1-4]\s*202[0-9]|[A-Z][a-z]+\s+202[0-9])\b", content):
            points += 5
            checks.append("✅ Specific period identified")
        else:
            checks.append("❌ No specific period")
        
        # Delta vs baseline / certified value
        if re.search(r"(delta|diferencia|variación|gap|overstatement|understatement).*\$[\d,]", content, re.IGNORECASE):
            points += 5
            checks.append("✅ Quantified delta vs baseline")
        else:
            checks.append("❌ No quantified delta")
        
        # Falsifiable condition (can be proven wrong)
        if re.search(r"(certif|reconcili|concili|valid|audit|gate).*(pass|fail|0 delta|\$0)", content, re.IGNORECASE):
            points += 5
            checks.append("✅ Falsifiable certification condition")
        else:
            checks.append("❌ No falsifiable condition")
        
        details["claim_checks"] = checks
        return min(points, 25)

    def _score_contradiction(self, content: str, details: Dict) -> int:
        """Score contradiction/known limits disclosure (0-25)."""
        points = 0
        checks = []
        
        # Explicit limitations section
        if re.search(r"(limitaciones?|supuestos?|cobertura|gap|no\s+certif|pending|⚠️|warning)", content, re.IGNORECASE):
            points += 8
            checks.append("✅ Explicit limitations/assumptions disclosed")
        else:
            checks.append("❌ No explicit limitations section")
        
        # Coverage gaps acknowledged
        if re.search(r"(cobertura|coverage).*(\d+%|parcial|incompleto|falta|missing)", content, re.IGNORECASE):
            points += 6
            checks.append("✅ Coverage gaps quantified")
        else:
            checks.append("❌ Coverage gaps not quantified")
        
        # Data quality caveats
        if re.search(r"(calidad|quality|outlier|anomal|dirty|noise|ruido)", content, re.IGNORECASE):
            points += 5
            checks.append("✅ Data quality caveats mentioned")
        else:
            checks.append("❌ No data quality caveats")
        
        # Assumptions listed
        if re.search(r"(supuest|asum|assum|hipótesis|hypothesis).*[:=]", content, re.IGNORECASE):
            points += 6
            checks.append("✅ Assumptions explicitly listed")
        else:
            checks.append("❌ Assumptions not listed")
        
        details["contradiction_checks"] = checks
        return min(points, 25)

    def _score_evidence(self, content: str, deliverable_path: Path, details: Dict) -> int:
        """Score evidence trail (0-30)."""
        points = 0
        checks = []
        
        # References to governance/*.md with line numbers or sections
        gov_refs = re.findall(r"governance/[A-Z_]+_CERTIFICATION\.md|governance/[A-Z_]+_REPORT\.md", content)
        if gov_refs:
            points += 8
            checks.append(f"✅ Governance evidence cited: {len(gov_refs)} refs")
        else:
            checks.append("❌ No governance evidence citations")
        
        # References to evidence/fase_1b/*.json
        evidence_refs = re.findall(r"evidence/fase_1b/[A-Z0-9_]+\.json", content)
        if evidence_refs:
            points += 8
            checks.append(f"✅ FASE 1B evidence cited: {len(evidence_refs)} refs")
        else:
            checks.append("❌ No FASE 1B evidence citations")
        
        # execution_id mentioned
        exec_ids = re.findall(r"execution[_\-]?id[\"':\s]+([a-f0-9\-]{36})", content, re.IGNORECASE)
        if exec_ids:
            points += 5
            checks.append(f"✅ execution_id present: {exec_ids[0]}")
        else:
            checks.append("❌ No execution_id")
        
        # Git commit SHA
        commits = re.findall(r"(commit|sha)[\"':\s]+([a-f0-9]{7,40})", content, re.IGNORECASE)
        if commits:
            points += 5
            checks.append(f"✅ Commit SHA: {commits[0][1][:7]}")
        else:
            checks.append("❌ No commit SHA")
        
        # Timestamp
        timestamps = re.findall(r"\b(202[0-9]-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d[Z+-])", content)
        if timestamps:
            points += 4
            checks.append(f"✅ ISO timestamp: {timestamps[0]}")
        else:
            checks.append("❌ No ISO timestamp")
        
        details["evidence_checks"] = checks
        return min(points, 30)

    def _score_anti_patterns(self, content: str, details: Dict) -> int:
        """Score anti-pattern compliance (0-20, higher = fewer violations)."""
        violations = []
        for pattern, name in self.ANTI_PATTERNS:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for m in matches[:3]:  # Limit reported matches
                    violations.append(f"{name}: '{m.group()[:80]}' at pos {m.start()}")
        
        points = 20 - min(len(violations) * 2, 20)  # -2 per violation, floor at 0
        
        if violations:
            details["anti_pattern_violations"] = violations
        else:
            details["anti_pattern_violations"] = ["✅ No anti-pattern violations detected"]
        
        return max(points, 0)

    def validate_evidence_directory(self, task_id: str) -> Tuple[FDEScore, List[Path]]:
        """Validate all evidence JSONs for a task."""
        evidence_files = list(self.evidence_dir.glob(f"*{task_id}*.json"))
        if not evidence_files:
            evidence_files = list(self.evidence_dir.glob("*.json"))
        
        score = FDEScore()
        score.details = {"evidence_files": [str(f) for f in evidence_files], "checks": []}
        
        if not evidence_files:
            score.details["checks"].append("❌ No evidence files found")
            score.evidence = 0
            score.__post_init__()
            return score, evidence_files
        
        total_files = len(evidence_files)
        valid_files = 0
        
        for ef in evidence_files:
            try:
                with open(ef, 'r') as f:
                    data = json.load(f)
                
                # Check required fields
                missing = [field for field in self.REQUIRED_EVIDENCE_FIELDS if field not in data]
                if not missing:
                    valid_files += 1
                    score.details["checks"].append(f"✅ {ef.name}: All required fields present")
                else:
                    score.details["checks"].append(f"❌ {ef.name}: Missing {missing}")
                
                # Check classification is auto-computed
                if data.get("classification") in ("IMPLEMENTED", "VALIDATED", "VERIFIED", "CERTIFIED", "NOT_CERTIFIED"):
                    score.details["checks"].append(f"✅ {ef.name}: Valid classification")
                else:
                    score.details["checks"].append(f"❌ {ef.name}: Invalid classification '{data.get('classification')}'")
                    
            except json.JSONDecodeError:
                score.details["checks"].append(f"❌ {ef.name}: Invalid JSON")
        
        # Score evidence based on validity ratio
        if total_files > 0:
            score.evidence = int(30 * (valid_files / total_files))
        
        # Claim: evidence exists
        score.claim = 15 if valid_files > 0 else 0
        
        # Contradiction: any missing fields disclosed
        score.contradiction = 15 if valid_files == total_files else 10
        
        # Anti-patterns: evidence structure compliance
        score.anti_patterns = 20 if valid_files == total_files else 10
        
        score.__post_init__()
        return score, evidence_files


def main():
    parser = argparse.ArgumentParser(description="FDE Assurance Score Validator")
    parser.add_argument("--deliverable", type=Path, help="Path to deliverable markdown file")
    parser.add_argument("--evidence-dir", type=Path, help="Path to evidence directory")
    parser.add_argument("--task", type=str, help="Task ID for evidence validation")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    validator = FDEValidator(args.repo_root)
    
    if args.deliverable:
        score = validator.validate_deliverable(args.deliverable)
        result = {
            "type": "deliverable",
            "file": str(args.deliverable),
            "score": asdict(score)
        }
    elif args.task:
        score, files = validator.validate_evidence_directory(args.task)
        result = {
            "type": "evidence",
            "task_id": args.task,
            "evidence_files": [str(f) for f in files],
            "score": asdict(score)
        }
    else:
        parser.error("Must specify --deliverable or --task")
        return 1
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        s = result["score"]
        print(f"\n{'='*50}")
        print(f"FDE ASSURANCE SCORE: {s['total']}/100")
        print(f"Verdict: {s['verdict']}")
        print(f"{'='*50}")
        print(f"  Claim (falsifiable):        {s['claim']}/25")
        print(f"  Contradiction (limits):     {s['contradiction']}/25")
        print(f"  Evidence trail:             {s['evidence']}/30")
        print(f"  Anti-pattern compliance:    {s['anti_patterns']}/20")
        print(f"{'='*50}")
        if s['details']:
            print("\nDetails:")
            for k, v in s['details'].items():
                if isinstance(v, list):
                    print(f"  {k}:")
                    for item in v:
                        print(f"    {item}")
                else:
                    print(f"  {k}: {v}")
    
    # Exit code based on verdict
    if s['verdict'] == "ELIGIBLE_FOR_CERTIFICATION":
        return 0
    elif s['verdict'] == "NEEDS_STRENGTHENING":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())