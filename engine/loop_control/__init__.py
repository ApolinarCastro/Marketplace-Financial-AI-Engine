"""Loop Engineering Protocol V1 — durable, agent-agnostic control plane.

Specification: governance/LOOP_ENGINEERING_PROTOCOL_V1.md
Runtime state: .loopx/ (git-ignored)

This package contains NO financial logic and issues NO SQL. It coordinates
agents; it does not compute money.
"""

from .claim_manager import ClaimManager
from .constants import (
    CONFLICT_CODES,
    GATE_TYPES,
    GOAL_STATUSES,
    PROTOCOL_VERSION,
    RECOVERY_DECISIONS,
    TODO_STATUSES,
    TURN_RESULTS,
    ClaimConflictError,
    GateRequiredError,
    LoopControlError,
    QuotaExhaustedError,
    SchemaValidationError,
    StateTransitionError,
)
from .evidence_manager import EvidenceManager
from .gate_manager import GateManager
from .goal_manager import GoalManager
from .handoff_manager import HandoffManager
from .kernel import LoopKernel
from .quota_manager import QuotaManager
from .recovery import RecoveryEngine
from .state_store import StateStore
from .todo_manager import TodoManager

__all__ = [
    "PROTOCOL_VERSION",
    "GOAL_STATUSES",
    "TODO_STATUSES",
    "TURN_RESULTS",
    "CONFLICT_CODES",
    "GATE_TYPES",
    "RECOVERY_DECISIONS",
    "LoopKernel",
    "StateStore",
    "GoalManager",
    "TodoManager",
    "ClaimManager",
    "GateManager",
    "QuotaManager",
    "EvidenceManager",
    "HandoffManager",
    "RecoveryEngine",
    "LoopControlError",
    "SchemaValidationError",
    "StateTransitionError",
    "ClaimConflictError",
    "GateRequiredError",
    "QuotaExhaustedError",
]
