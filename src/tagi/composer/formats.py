"""Commit message format generators.

Each generator is a stable, independently testable responsibility: it turns a
set of tagged changes into a specific commit-message format.
"""

from typing import List
from collections import Counter

from tagi.models import Change, Tag

from ._tags import all_tags, summary_tag, infer_scope
from tagi.utils.line_builder import LineBuilder


_COMMIT_TYPES: "tuple[tuple[Tag, str], ...]" = (
    (Tag.FEATURE, "feat"),
    (Tag.RISKY, "fix"),
    (Tag.DOCS, "docs"),
    (Tag.TESTS, "test"),
    (Tag.DEPS, "chore"),
    (Tag.REFACTOR, "refactor"),
    (Tag.CONFIG, "config"),
)


def _commit_type(tags: "set[Tag]") -> str:
    """Pick the highest-priority conventional commit type for a tag set."""
    for tag, commit_type in _COMMIT_TYPES:
        if tag in tags:
            return commit_type
    return "chore"


def _describe_changes(changes: List[Change]) -> str:
    """Summarize the changed file count or single path."""
    if len(changes) == 1:
        return f"update {changes[0].path}"
    return f"update {len(changes)} files"


def generate_conventional_message(changes: List[Change]) -> str:
    """Generate a conventional commits format message."""
    if not changes:
        return "chore: empty commit"

    # Determine type from tags
    tag_set = set(all_tags(changes))
    commit_type = _commit_type(tag_set)

    # Determine scope from file paths
    scope = infer_scope(changes)

    # Generate description
    description = _describe_changes(changes)

    # Add optional breaking change indicator
    breaking = "!" if Tag.RISKY in tag_set else ""

    if scope:
        return f"{commit_type}({scope}){breaking}: {description}"
    else:
        return f"{commit_type}{breaking}: {description}"


def _count_tags(changes: List[Change]) -> Counter:
    """Count tag occurrences across all changes."""
    tag_counts: Counter = Counter()
    for change in changes:
        for tag in change.tags:
            tag_counts[tag.value] += 1
    return tag_counts


def _detailed_file_lines(changes: List[Change]) -> "list[str]":
    """Render one aligned line per changed file with its tags."""
    return [
        f"  [{change.change_type.value:8}] {change.path:40} "
        f"({', '.join(t.value for t in change.tags)})"
        for change in changes
    ]


def generate_detailed_message(changes: List[Change]) -> str:
    """Generate a detailed commit message."""
    if not changes:
        return "Empty commit"

    tag_counts = _count_tags(changes)

    return LineBuilder([
        f"Commit: {len(changes)} files changed",
        "",
        "Tags:",
        *(f"  - {tag}: {count}" for tag, count in tag_counts.most_common()),
        "",
        "Files:",
        *_detailed_file_lines(changes),
    ]).text()


def generate_simple_message(changes: List[Change]) -> str:
    """Generate a simple commit message."""
    if not changes:
        return "Empty commit"

    files = [c.path for c in changes]

    if len(files) == 1:
        return f"{summary_tag(changes)}: {files[0]}"
    else:
        return f"{summary_tag(changes)}: {len(files)} files ({', '.join(files[:3])}{'...' if len(files) > 3 else ''})"


def generate_oneline_message(changes: List[Change]) -> str:
    """Generate a one-line commit message."""
    if not changes:
        return "empty commit"

    count = len(changes)
    files_str = ", ".join([c.path for c in changes[:3]])
    if count > 3:
        files_str += f" and {count - 3} more"

    return f"{summary_tag(changes)}: {files_str}"


def generate_files_message(changes: List[Change]) -> str:
    """Generate a file-focused commit message."""
    if not changes:
        return "Empty commit"

    return LineBuilder([
        f"Changes ({len(changes)} files):",
        "",
        *(
            f"  {change.change_type.value:8} {change.path:40} "
            f"[{' '.join(t.value for t in change.tags)}]"
            for change in changes
        ),
    ]).text()
