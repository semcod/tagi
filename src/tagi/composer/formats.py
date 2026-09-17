"""Commit message format generators.

Each generator is a stable, independently testable responsibility: it turns a
set of tagged changes into a specific commit-message format.
"""

from typing import List
from collections import Counter

from tagi.models import Change, Tag

from ._tags import all_tags, summary_tag, infer_scope


def generate_conventional_message(changes: List[Change]) -> str:
    """Generate a conventional commits format message."""
    if not changes:
        return "chore: empty commit"

    # Determine type from tags
    tags = set(all_tags(changes))
    if Tag.FEATURE in tags:
        commit_type = "feat"
    elif Tag.RISKY in tags:
        commit_type = "fix"
    elif Tag.DOCS in tags:
        commit_type = "docs"
    elif Tag.TESTS in tags:
        commit_type = "test"
    elif Tag.DEPS in tags:
        commit_type = "chore"
    elif Tag.REFACTOR in tags:
        commit_type = "refactor"
    elif Tag.CONFIG in tags:
        commit_type = "config"
    else:
        commit_type = "chore"

    # Determine scope from file paths
    scope = infer_scope(changes)

    # Generate description
    files_count = len(changes)
    if files_count == 1:
        description = f"update {changes[0].path}"
    else:
        description = f"update {files_count} files"

    # Add optional breaking change indicator
    breaking = "!" if Tag.RISKY in tags else ""

    if scope:
        return f"{commit_type}({scope}){breaking}: {description}"
    else:
        return f"{commit_type}{breaking}: {description}"


def generate_detailed_message(changes: List[Change]) -> str:
    """Generate a detailed commit message."""
    if not changes:
        return "Empty commit"

    lines = []
    lines.append(f"Commit: {len(changes)} files changed")
    lines.append("")

    # Group by tag
    tag_counts = Counter()
    for change in changes:
        for tag in change.tags:
            tag_counts[tag.value] += 1

    lines.append("Tags:")
    for tag, count in tag_counts.most_common():
        lines.append(f"  - {tag}: {count}")
    lines.append("")

    lines.append("Files:")
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")

    return "\n".join(lines)


def generate_simple_message(changes: List[Change]) -> str:
    """Generate a simple commit message."""
    if not changes:
        return "Empty commit"

    tag = summary_tag(changes)
    files = [c.path for c in changes]

    if len(files) == 1:
        return f"{tag}: {files[0]}"
    else:
        return f"{tag}: {len(files)} files ({', '.join(files[:3])}{'...' if len(files) > 3 else ''})"


def generate_oneline_message(changes: List[Change]) -> str:
    """Generate a one-line commit message."""
    if not changes:
        return "empty commit"

    tag = summary_tag(changes)
    count = len(changes)
    files_str = ", ".join([c.path for c in changes[:3]])
    if count > 3:
        files_str += f" and {count - 3} more"

    return f"{tag}: {files_str}"


def generate_files_message(changes: List[Change]) -> str:
    """Generate a file-focused commit message."""
    if not changes:
        return "Empty commit"

    lines = []
    lines.append(f"Changes ({len(changes)} files):")
    lines.append("")

    for change in changes:
        tags_str = " ".join([t.value for t in change.tags])
        lines.append(f"  {change.change_type.value:8} {change.path:40} [{tags_str}]")

    return "\n".join(lines)
