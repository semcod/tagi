"""Commit message module for generating commit messages."""

from typing import List

from tagi.models import Change, Tag
from tagi.config import Config


def generate_commit_message(changes: List[Change], template: str = "default", repo_path: str = ".") -> str:
    """Generate a commit message based on template."""
    config = Config(repo_path)
    
    # Check for custom template
    custom_template = config.get_template(template)
    if custom_template:
        template = custom_template
    
    files_str = ", ".join([c.path for c in changes])
    count = len(changes)
    tag = changes[0].tags[0].value if changes and changes[0].tags else "#small"
    
    if template == "conventional":
        return generate_conventional_message(changes)
    elif template == "detailed":
        return generate_detailed_message(changes)
    else:
        return template.format(tag=tag, files=files_str, count=count)


def generate_conventional_message(changes: List[Change]) -> str:
    """Generate a conventional commits format message."""
    if not changes:
        return "chore: empty commit"
    
    # Determine type from tags
    tags = changes[0].tags
    if Tag.FEATURE in tags:
        commit_type = "feat"
    elif Tag.FIX in tags or Tag.RISKY in tags:
        commit_type = "fix"
    elif Tag.DOCS in tags:
        commit_type = "docs"
    elif Tag.TESTS in tags:
        commit_type = "test"
    elif Tag.DEPS in tags:
        commit_type = "chore"
    elif Tag.REFACTOR in tags:
        commit_type = "refactor"
    else:
        commit_type = "chore"
    
    scope = "general"
    files_count = len(changes)
    description = f"update {files_count} file{'s' if files_count != 1 else ''}"
    
    return f"{commit_type}({scope}): {description}"


def generate_detailed_message(changes: List[Change]) -> str:
    """Generate a detailed commit message."""
    if not changes:
        return "Empty commit"
    
    lines = []
    lines.append(f"Commit: {len(changes)} files changed")
    lines.append("")
    
    # Group by tag
    from collections import Counter
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
