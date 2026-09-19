"""Shared tag-target helpers for the cli command modules."""

from pathlib import Path
from typing import Optional

from tagi.models.change import Tag


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag starts with #."""
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def _is_known_tag(value: str) -> bool:
    """Return True when the value matches a supported tag."""
    try:
        Tag(_ensure_tag_prefix(value))
        return True
    except ValueError:
        return False


def _resolve_send_target(target: Optional[str], repo_path: str) -> tuple[str, Optional[str]]:
    """Resolve send positional input as either a tag or a repository path."""
    if target is None:
        return repo_path, None

    # An explicit --repo-path means the positional argument is always a tag.
    if repo_path != ".":
        return repo_path, target

    # Known tags are treated as tags.
    if _is_known_tag(target):
        return repo_path, target

    # An existing filesystem path is treated as the repository path.
    candidate = Path(target).expanduser()
    if candidate.exists():
        return str(candidate), None

    # Otherwise treat the value as a (possibly unknown) tag so the caller can
    # report it cleanly instead of failing on a missing path.
    return repo_path, target
