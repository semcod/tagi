"""Shared case-insensitive path matching.

Single owner of the lowercased-path matching pattern, extracted to remove
the ``path_lower`` shotgun-surgery smell (PLF-146). Every path lookup goes
through :func:`path_key`, :func:`path_matches` or :func:`path_endswith`
so the normalization policy is defined once.
"""

from typing import Tuple


def path_key(path: str) -> str:
    """Return the canonical lowercase form of a path for matching."""
    return path.lower()


def path_matches(path: str, pattern: str) -> bool:
    """Check whether a path contains a pattern, case-insensitively."""
    return pattern.lower() in path_key(path)


def path_endswith(path: str, suffixes: Tuple[str, ...]) -> bool:
    """Check whether a path ends with any suffix, case-insensitively."""
    return path_key(path).endswith(suffixes)
