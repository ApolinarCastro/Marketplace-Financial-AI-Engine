"""Claims and leases.

Two agents may never hold the same (goal_id, todo_id) simultaneously.
Expired leases are recoverable through a deterministic procedure; the previous
claim is moved to history and never deleted.
"""

from __future__ import annotations

from typing import Any

from .constants import DEFAULT_LEASE_SECONDS, ClaimConflictError, LoopControlError
from .scope import overlapping_pairs, scopes_overlap
from .state_store import StateStore, future_iso, iso, parse_iso, utcnow
from .validation import validate


class ClaimManager:
    def __init__(self, store: StateStore) -> None:
        self.store = store

    def _load(self) -> dict[str, Any]:
        return self.store.read("claims")

    def _save(self, data: dict[str, Any]) -> None:
        self.store.write("claims", data)

    # ------------------------------------------------------------- reads

    def active_claims(self) -> list[dict[str, Any]]:
        return list(self._load()["active"])

    def history(self) -> list[dict[str, Any]]:
        return list(self._load()["history"])

    def find_active(self, goal_id: str, todo_id: str) -> dict[str, Any] | None:
        for claim in self._load()["active"]:
            if claim["goal_id"] == goal_id and claim["todo_id"] == todo_id:
                return claim
        return None

    @staticmethod
    def is_expired(claim: dict[str, Any]) -> bool:
        return parse_iso(claim["expires_at"]) <= utcnow()

    # ------------------------------------------------------------ writes

    def claim(
        self,
        goal_id: str,
        todo_id: str,
        agent_id: str,
        write_scope: list[str],
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
        idempotency_key: str | None = None,
        force_stale_takeover: bool = False,
    ) -> dict[str, Any]:
        """Acquire a lease. Raises ClaimConflictError with a canonical code."""
        data = self._load()

        if idempotency_key:
            for claim in data["active"]:
                if claim.get("idempotency_key") == idempotency_key:
                    return claim

        for idx, existing in enumerate(list(data["active"])):
            if existing["goal_id"] == goal_id and existing["todo_id"] == todo_id:
                if existing["agent_id"] == agent_id:
                    return existing
                if self.is_expired(existing):
                    if not force_stale_takeover:
                        raise ClaimConflictError(
                            "STALE_LEASE",
                            f"todo {todo_id} held by {existing['agent_id']} with an expired lease "
                            f"(expired {existing['expires_at']}); recover with force_stale_takeover=True",
                        )
                    stale = dict(existing)
                    stale["released_at"] = iso()
                    stale["release_reason"] = "STALE_LEASE_RECOVERED"
                    data["history"].append(stale)
                    data["active"].pop(idx)
                    break
                raise ClaimConflictError(
                    "ACTIVE_CONFLICT",
                    f"todo {todo_id} is actively claimed by {existing['agent_id']} until {existing['expires_at']}",
                )

        for existing in data["active"]:
            if existing["goal_id"] != goal_id or existing["agent_id"] == agent_id:
                continue
            if scopes_overlap(existing["write_scope"], write_scope):
                pairs = overlapping_pairs(existing["write_scope"], write_scope)
                raise ClaimConflictError(
                    "WRITE_SCOPE_OVERLAP",
                    f"write scope collides with todo {existing['todo_id']} held by "
                    f"{existing['agent_id']}: {pairs}",
                )

        now = utcnow()
        claim = {
            "goal_id": goal_id,
            "todo_id": todo_id,
            "agent_id": agent_id,
            "claimed_at": iso(now),
            "expires_at": future_iso(lease_seconds, now),
            "heartbeat_at": iso(now),
            "released_at": None,
            "write_scope": list(write_scope),
            "revision": 0,
            "idempotency_key": idempotency_key,
        }
        validate(claim, "claim")
        data["active"].append(claim)
        self._save(data)
        return claim

    def heartbeat(self, goal_id: str, todo_id: str, agent_id: str, lease_seconds: int = DEFAULT_LEASE_SECONDS) -> dict[str, Any]:
        data = self._load()
        for idx, claim in enumerate(data["active"]):
            if claim["goal_id"] == goal_id and claim["todo_id"] == todo_id:
                if claim["agent_id"] != agent_id:
                    raise ClaimConflictError("ACTIVE_CONFLICT", f"claim held by {claim['agent_id']}")
                now = utcnow()
                claim["heartbeat_at"] = iso(now)
                claim["expires_at"] = future_iso(lease_seconds, now)
                claim["revision"] = int(claim.get("revision", 0)) + 1
                validate(claim, "claim")
                data["active"][idx] = claim
                self._save(data)
                return claim
        raise LoopControlError(f"no active claim for {goal_id}/{todo_id}")

    def release(self, goal_id: str, todo_id: str, agent_id: str, reason: str = "RELEASED") -> dict[str, Any] | None:
        data = self._load()
        for idx, claim in enumerate(data["active"]):
            if claim["goal_id"] == goal_id and claim["todo_id"] == todo_id:
                if claim["agent_id"] != agent_id:
                    raise ClaimConflictError("ACTIVE_CONFLICT", f"claim held by {claim['agent_id']}")
                released = dict(claim)
                released["released_at"] = iso()
                released["release_reason"] = reason
                data["history"].append(released)
                data["active"].pop(idx)
                self._save(data)
                return released
        return None

    def detect_conflicts(self) -> list[dict[str, Any]]:
        """Return canonical conflict codes for the current claim table."""
        conflicts: list[dict[str, Any]] = []
        active = self._load()["active"]
        for claim in active:
            if self.is_expired(claim):
                conflicts.append(
                    {
                        "code": "STALE_LEASE",
                        "goal_id": claim["goal_id"],
                        "todo_id": claim["todo_id"],
                        "agent_id": claim["agent_id"],
                        "expires_at": claim["expires_at"],
                    }
                )
        for i, a in enumerate(active):
            for b in active[i + 1 :]:
                if a["goal_id"] != b["goal_id"] or a["agent_id"] == b["agent_id"]:
                    continue
                if scopes_overlap(a["write_scope"], b["write_scope"]):
                    conflicts.append(
                        {
                            "code": "WRITE_SCOPE_OVERLAP",
                            "goal_id": a["goal_id"],
                            "todos": [a["todo_id"], b["todo_id"]],
                            "agents": [a["agent_id"], b["agent_id"]],
                        }
                    )
        return conflicts
