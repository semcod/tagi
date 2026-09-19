"""Tag and scope analysis helpers for commit message composition."""

from typing import List

from tagi.models import Change, Tag


def all_tags(changes: List[Change]) -> List[Tag]:
    """Return unique tags across all changes, preserving first-seen order."""
    return list(
        dict.fromkeys(tag for change in changes for tag in change.tags)
    )


def all_tag_values(changes: List[Change]) -> List[str]:
    """Return unique tag values across all changes."""
    return [tag.value for tag in all_tags(changes)]


def summary_tag(changes: List[Change]) -> str:
    """Choose a stable tag prefix for a commit spanning one or more changes."""
    unique_tags = all_tags(changes)
    if not unique_tags:
        return "#small"
    if len(unique_tags) == 1:
        return unique_tags[0].value
    return "#all"


_SCOPE_PATTERNS = [
    (["test"], "tests"),
    (["doc"], "docs"),
    (["config"], "config"),
    (["api"], "api"),
    (["cli"], "cli"),
    (["ui", "web", "frontend"], "ui"),
    (["db", "database"], "db"),
]


def infer_scope(changes: List[Change]) -> str:
    """Infer a conventional-commit scope from file paths."""
    if not changes:
        return ""

    paths = [c.path.lower() for c in changes]

    for patterns, scope in _SCOPE_PATTERNS:
        if any(pattern in p for p in paths for pattern in patterns):
            return scope

    return "general"
