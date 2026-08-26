"""Project Policy Contract — universal interface + Marketplace implementation.

This module defines the ProjectPolicy ABC that every project must implement,
and provides the MarketplaceProjectPolicy as a concrete example extracted
from the certified pilot.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from engine.loop_control.constants import DEFAULT_QUOTA_LIMITS


@dataclass(frozen=True)
class QuotaLimits:
    max_same_hypothesis_attempts: int = DEFAULT_QUOTA_LIMITS["max_same_hypothesis_attempts"]
    max_no_progress_turns: int = DEFAULT_QUOTA_LIMITS["max_no_progress_turns"]
    max_validation_failures: int = DEFAULT_QUOTA_LIMITS["max_validation_failures"]
    max_scope_expansions: int = DEFAULT_QUOTA_LIMITS["max_scope_expansions"]


class ProjectPolicy(abc.ABC):
    """Abstract base class. Every project MUST implement this."""

    @property
    @abc.abstractmethod
    def project_id(self) -> str: ...

    @property
    @abc.abstractmethod
    def project_root(self) -> Path: ...

    @property
    @abc.abstractmethod
    def protected_resources(self) -> list[str]: ...

    @property
    @abc.abstractmethod
    def allowed_write_scopes(self) -> dict[str, list[str]]: ...

    @property
    @abc.abstractmethod
    def validation_commands(self) -> dict[str, list[str]]: ...

    @property
    @abc.abstractmethod
    def evidence_root(self) -> Path: ...

    @property
    @abc.abstractmethod
    def runtime_state_root(self) -> Path: ...

    @property
    @abc.abstractmethod
    def human_gate_actions(self) -> dict[str, Callable]: ...

    @property
    @abc.abstractmethod
    def quota_limits(self) -> QuotaLimits: ...

    @abc.abstractmethod
    def resolve_gate(self, gate_type: str, question: str, target: str) -> str:
        """Human resolution of a gate. Must return 'APPROVED' or 'REJECTED'."""
        ...

    @abc.abstractmethod
    def validate_project(self) -> bool:
        """Run project-specific validation. Return True if PASS."""
        ...


@dataclass
class AgentConfig:
    agent_id: str
    runtime: str
    capabilities: list[str]
    allowed_write_scope: list[str]
    protected_write_scope: list[str]
    status: str = "AVAILABLE"


class MarketplaceProjectPolicy(ProjectPolicy):
    """Concrete implementation for the Marketplace Financial AI Engine."""

    def __init__(self, project_root: Path | None = None):
        self._root = (project_root or Path.cwd()).resolve()

    @property
    def project_id(self) -> str:
        return "marketplace-financial-ai-engine"

    @property
    def project_root(self) -> Path:
        return self._root

    @property
    def protected_resources(self) -> list[str]:
        return [
            "01_Raw/**",
            "data/db/meli_financial_v4.db",
            ".git/**",
            ".agents/**",
            "governance/coordination/**",
            "engine/v4/domain/**",
        ]

    @property
    def allowed_write_scopes(self) -> dict[str, list[str]]:
        return {
            "OPENCODE_ENGINEER": [
                "engine/loop_control/**",
                "tests/**",
                "evidence/**",
                "governance/**",
                "tools/**",
            ],
            "CODEX_ENGINEER": [
                "engine/loop_control/**",
                "tests/**",
                "evidence/**",
                "governance/**",
                "tools/**",
            ],
            "AUDITOR": [
                "evidence/**",
                "governance/**",
            ],
            "QA": [
                "tests/**",
                "evidence/**",
            ],
            "RESEARCHER": [
                "evidence/**",
            ],
        }

    @property
    def validation_commands(self) -> dict[str, list[str]]:
        return {
            "LOOP-00": ["python tools/loop_precheck.py"],
            "LOOP-01": ["python tools/loop_dep_inventory.py"],
            "LOOP-02": ["python tools/loop_domain_coupling.py"],
            "LOOP-03": ["python -m engine.loop_control validate"],
            "LOOP-04": ["python -m engine.loop_control validate"],
            "LOOP-05": ["python -m pytest tests/test_universal_loop_kernel.py -q"],
            "LOOP-06": ["python tools/loop_schema_audit.py"],
            "LOOP-07": ["python -m pytest tests/test_universal_adapters.py -q"],
            "LOOP-08": ["python -m pytest tests/test_universal_agents.py -q"],
            "LOOP-09": ["python -m pytest tests/test_universal_continuation.py -q"],
            "LOOP-10": ["python -m pytest tests/test_universal_state_portable.py -q"],
            "LOOP-11": ["python -m pytest tests/test_universal_evidence.py -q"],
            "LOOP-12": ["python -m pytest tests/test_universal_gates.py -q"],
            "LOOP-13": ["python -m pytest tests/test_universal_quota.py -q"],
            "LOOP-14": ["python -m pytest tests/test_universal_concurrency.py -q"],
            "LOOP-15": ["python -m pytest tests/test_universal_recovery.py -q"],
            "LOOP-16": ["python -m pytest tests/test_universal_idempotency.py -q"],
            "LOOP-17": ["python tools/bootstrap_loop_engineering.py --help"],
            "LOOP-18": ["python -m engine.loop_control doctor"],
            "LOOP-19": ["python tools/test_project_a.py"],
            "LOOP-20": ["python tools/test_project_b.py"],
            "LOOP-21": ["python -m pytest tests/test_loop_control.py -q"],
            "LOOP-22": ["python -m pytest tests -q --tb=no"],
            "LOOP-23": ["python tools/universal_dogfood.py"],
            "LOOP-24": ["python tools/certify_multi_project.py"],
        }

    @property
    def evidence_root(self) -> Path:
        return self._root / "evidence" / "universal_loop_v1"

    @property
    def runtime_state_root(self) -> Path:
        return self._root / ".loopx"

    @property
    def human_gate_actions(self) -> dict[str, Callable]:
        return {
            "PROTECTED_RESOURCE": lambda q, t: input(f"GATE {q}\n> ").strip().upper(),
            "SCOPE_EXPANSION": lambda q, t: input(f"GATE {q}\n> ").strip().upper(),
            "DESTRUCTIVE_OPERATION": lambda q, t: input(f"GATE {q}\n> ").strip().upper(),
            "PRODUCTION_PUBLISH": lambda q, t: input(f"GATE {q}\n> ").strip().upper(),
            "QUOTA_RESET": lambda q, t: input(f"GATE {q}\n> ").strip().upper(),
        }

    @property
    def quota_limits(self) -> QuotaLimits:
        return QuotaLimits()

    def resolve_gate(self, gate_type: str, question: str, target: str) -> str:
        handler = self.human_gate_actions.get(gate_type)
        if handler:
            return handler(question, target)
        raise ValueError(f"no handler for gate type: {gate_type}")

    def validate_project(self) -> bool:
        """Run Marketplace-specific validation suite."""
        import subprocess
        result = subprocess.run(
            [".venv/Scripts/python.exe", "-m", "pytest", "tests/test_loop_control.py", "-q"],
            cwd=self._root, capture_output=True, text=True, timeout=300,
        )
        return result.returncode == 0


class SyntheticProjectAPolicy(ProjectPolicy):
    """Synthetic Project A: text-only code project."""

    def __init__(self, project_root: Path):
        self._root = project_root.resolve()

    @property
    def project_id(self) -> str:
        return "synthetic-project-a"

    @property
    def project_root(self) -> Path:
        return self._root

    @property
    def protected_resources(self) -> list[str]:
        return [
            ".git/**",
            "secrets/**",
            "*.key",
            "*.pem",
        ]

    @property
    def allowed_write_scopes(self) -> dict[str, list[str]]:
        return {
            "OPENCODE_ENGINEER": ["src/**", "tests/**", "docs/**"],
            "CODEX_ENGINEER": ["src/**", "tests/**", "docs/**"],
        }

    @property
    def validation_commands(self) -> dict[str, list[str]]:
        return {
            "LOOP-00": ["python -m py_compile src/**/*.py"],
            "LOOP-01": ["python -m pytest tests/ -q"],
        }

    @property
    def evidence_root(self) -> Path:
        return self._root / "evidence" / "loop"

    @property
    def runtime_state_root(self) -> Path:
        return self._root / ".loopx"

    @property
    def human_gate_actions(self) -> dict[str, Callable]:
        return {
            "PROTECTED_RESOURCE": lambda q, t: "APPROVED",
            "SCOPE_EXPANSION": lambda q, t: "APPROVED",
        }

    @property
    def quota_limits(self) -> QuotaLimits:
        return QuotaLimits()

    def resolve_gate(self, gate_type: str, question: str, target: str) -> str:
        return "APPROVED"

    def validate_project(self) -> bool:
        return True


class SyntheticProjectBPolicy(ProjectPolicy):
    """Synthetic Project B: research project with papers/experiments."""

    def __init__(self, project_root: Path):
        self._root = project_root.resolve()

    @property
    def project_id(self) -> str:
        return "synthetic-project-b"

    @property
    def project_root(self) -> Path:
        return self._root

    @property
    def protected_resources(self) -> list[str]:
        return [
            ".git/**",
            "data/raw/**",
            "credentials/**",
        ]

    @property
    def allowed_write_scopes(self) -> dict[str, list[str]]:
        return {
            "OPENCODE_ENGINEER": ["papers/**", "experiments/**", "results/**"],
            "CODEX_ENGINEER": ["papers/**", "experiments/**", "results/**"],
            "RESEARCHER": ["papers/**", "experiments/**"],
        }

    @property
    def validation_commands(self) -> dict[str, list[str]]:
        return {
            "LOOP-00": ["python tools/check_reproducibility.py"],
            "LOOP-01": ["python tools/verify_experiments.py"],
        }

    @property
    def evidence_root(self) -> Path:
        return self._root / "evidence" / "loop"

    @property
    def runtime_state_root(self) -> Path:
        return self._root / ".loopx"

    @property
    def human_gate_actions(self) -> dict[str, Callable]:
        return {
            "PROTECTED_RESOURCE": lambda q, t: "APPROVED",
            "SCOPE_EXPANSION": lambda q, t: "APPROVED",
        }

    @property
    def quota_limits(self) -> QuotaLimits:
        return QuotaLimits()

    def resolve_gate(self, gate_type: str, question: str, target: str) -> str:
        return "APPROVED"

    def validate_project(self) -> bool:
        return True


def load_policy(project_id: str, project_root: Path | None = None) -> ProjectPolicy:
    """Factory function to load the appropriate policy."""
    policies = {
        "marketplace-financial-ai-engine": MarketplaceProjectPolicy,
        "synthetic-project-a": SyntheticProjectAPolicy,
        "synthetic-project-b": SyntheticProjectBPolicy,
    }
    cls = policies.get(project_id)
    if cls is None:
        raise ValueError(f"unknown project_id: {project_id}")
    return cls(project_root)