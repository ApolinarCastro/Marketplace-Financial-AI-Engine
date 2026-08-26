"""Path glob matching and write-scope overlap detection.

Deliberately simple and deterministic: no filesystem access, pure string logic,
so scope decisions are reproducible on any machine.
"""

from __future__ import annotations

import fnmatch


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip().lstrip("./")


def matches(path: str, pattern: str) -> bool:
    """True if `path` falls under `pattern`.

    Supports a trailing /** to mean "this directory and everything under it".
    """
    p = normalize(path)
    pat = normalize(pattern)
    if not pat:
        return False
    if pat.endswith("/**"):
        base = pat[:-3]
        return p == base or p.startswith(base + "/")
    if fnmatch.fnmatch(p, pat):
        return True
    # A bare directory pattern also covers its contents.
    if not any(ch in pat for ch in "*?[") and p.startswith(pat.rstrip("/") + "/"):
        return True
    return False


def matches_any(path: str, patterns) -> bool:
    return any(matches(path, pat) for pat in patterns)


def matched_pattern(path: str, patterns) -> str | None:
    for pat in patterns:
        if matches(path, pat):
            return pat
    return None


def _prefix(pattern: str) -> str:
    pat = normalize(pattern)
    if pat.endswith("/**"):
        return pat[:-3]
    out: list[str] = []
    for part in pat.split("/"):
        if any(ch in part for ch in "*?["):
            break
        out.append(part)
    return "/".join(out)


def scopes_overlap(a, b) -> bool:
    """True if two write scopes can touch a common path region."""
    for pa in a:
        for pb in b:
            na, nb = normalize(pa), normalize(pb)
            if na == nb:
                return True
            fa, fb = _prefix(pa), _prefix(pb)
            if not fa or not fb:
                # One side is effectively unbounded (e.g. '**').
                return True
            if fa == fb or fa.startswith(fb + "/") or fb.startswith(fa + "/"):
                return True
    return False


def overlapping_pairs(a, b) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for pa in a:
        for pb in b:
            if scopes_overlap([pa], [pb]):
                pairs.append((pa, pb))
    return pairs
