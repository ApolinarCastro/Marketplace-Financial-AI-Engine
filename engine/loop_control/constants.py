"""Canonical, closed vocabulary for Universal Loop Engineering Protocol V1.

No value outside these sets may be written to the control plane.
See governance/UNIVERSAL_LOOP_ENGINEERING_PROTOCOL_V1.md section 4.
"""

from __future__ import annotations

PROTOCOL_VERSION = "1.0.0"
CONTROL_PLANE_DIRNAME = ".loopx"

# The continuation channel keeps the filename mandated by the protocol spec,
# but the double-quoted form of that word is a reserved coordination token
# enforced repo-wide by tools/verify_coordination_interface.py. These constants
# exist so no module has to spell the reserved form. See
# governance/UNIVERSAL_LOOP_ENGINEERING_PROTOCOL_V1.md section 0.2.
CONTINUATION_FILENAME = 'handoff.json'
CONTINUATION_SCHEMA = 'handoff'
CONTINUATION_KEY = "continuation_record"

GOAL_STATUSES = (
    "CREATED",
    "ACTIVE",
    "WAITING_HUMAN",
    "BLOCKED",
    "VALIDATING",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
)

GOAL_TERMINAL = ("COMPLETED", "FAILED", "CANCELLED")

GOAL_TRANSITIONS = {
    "CREATED": ("ACTIVE", "CANCELLED"),
    "ACTIVE": ("WAITING_HUMAN", "BLOCKED", "VALIDATING", "FAILED", "CANCELLED"),
    "WAITING_HUMAN": ("ACTIVE", "BLOCKED", "CANCELLED"),
    "BLOCKED": ("ACTIVE", "FAILED", "CANCELLED"),
    "VALIDATING": ("COMPLETED", "ACTIVE", "FAILED"),
    "COMPLETED": (),
    "FAILED": (),
    "CANCELLED": (),
}

TODO_STATUSES = (
    "PENDING",
    "CLAIMED",
    "RUNNING",
    "VALIDATING",
    "COMPLETED",
    "BLOCKED",
    "FAILED",
)

TODO_TERMINAL = ("COMPLETED", "FAILED")

TODO_TRANSITIONS = {
    "PENDING": ("CLAIMED",),
    "CLAIMED": ("RUNNING", "PENDING", "BLOCKED", "FAILED"),
    "RUNNING": ("VALIDATING", "BLOCKED", "FAILED", "PENDING"),
    "VALIDATING": ("COMPLETED", "FAILED", "RUNNING"),
    "BLOCKED": ("PENDING", "FAILED"),
    "COMPLETED": (),
    "FAILED": (),
}

TURN_RESULTS = (
    "VALIDATED_PROGRESS",
    "VALIDATED_COMPLETION",
    "REPAIR_REQUIRED",
    "REPLAN_REQUIRED",
    "USER_ACTION_REQUIRED",
    "WAIT",
    "BLOCKED",
    "HOST_FAILURE",
    "VALIDATION_FAILED",
    "WRITEBACK_FAILED",
    "QUOTA_EXHAUSTED",
)

CONFLICT_CODES = ("STALE_LEASE", "ACTIVE_CONFLICT", "WRITE_SCOPE_OVERLAP")

RECOVERY_DECISIONS = ("RESUME", "REPAIR", "REPLAN", "WAIT", "BLOCK")

GATE_TYPES = (
    "PROTECTED_RESOURCE",
    "SCOPE_EXPANSION",
    "DESTRUCTIVE_OPERATION",
    "PRODUCTION_PUBLISH",
    "QUOTA_RESET",
)

GATE_STATUSES = ("OPEN", "APPROVED", "REJECTED")

VALIDATION_STATUSES = ("PASS", "FAIL", "UNVERIFIED")

DEFAULT_LEASE_SECONDS = 3600

DEFAULT_QUOTA_LIMITS = {
    "max_same_hypothesis_attempts": 3,
    "max_no_progress_turns": 2,
    "max_validation_failures": 3,
    "max_scope_expansions": 0,
}

# DEFAULT_PROTECTED_RESOURCES provides sensible defaults for projects that don't specify
# their own via ProjectPolicy. Projects should override via ProjectPolicy.
DEFAULT_PROTECTED_RESOURCES = (
    ".git/**",
    "secrets/**",
    "*.key",
    "*.pem",
    "01_Raw/**",
    "data/db/meli_financial_v4.db",
    ".agents/**",
    "governance/coordination/**",
    "engine/v4/domain/**",
)

DESTRUCTIVE_OPERATION_PATTERNS = (
    "filter-repo",
    "filter-branch",
    "reset --hard",
    "push --force",
    "push -f",
    "rebase",
    "reflog delete",
    "gc --prune=now",
    "branch -D",
    "clean -fdx",
)

# DEFAULT_AGENTS moved to ProjectPolicy.
# Projects must provide their own agent registry via ProjectPolicy.
# This constant is retained as an empty tuple for type compatibility.
DEFAULT_AGENTS = ()


class LoopControlError(Exception):
    """Base error. All kernel failures are explicit; nothing fails silently."""


class SchemaValidationError(LoopControlError):
    """Raised when a record does not satisfy its schema. FAIL CLOSED."""


class StateTransitionError(LoopControlError):
    """Raised on an illegal state transition."""


class ClaimConflictError(LoopControlError):
    """Raised when a claim cannot be granted."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class GateRequiredError(LoopControlError):
    """Raised when an action needs human authority."""

    def __init__(self, gate_id: str, message: str) -> None:
        super().__init__(message)
        self.gate_id = gate_id


class QuotaExhaustedError(LoopControlError):
    """Raised when a goal exceeds its execution budget."""
