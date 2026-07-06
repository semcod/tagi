"""Commit message module for generating commit messages."""

from typing import List
from collections import Counter

from tagi.models import Change, Tag
from tagi.config import Config


def generate_commit_message(changes: List[Change], template: str = "default", repo_path: str = ".", use_llm: bool = False) -> str:
    """Generate a commit message based on template."""
    config = Config(repo_path)

    # A configured custom template overrides the built-in name.
    template = config.get_template(template) or template

    tag = _summary_tag(changes)
    files_str = ", ".join(c.path for c in changes)
    message = _render_template(template, changes, tag=tag, files=files_str, count=len(changes))

    if use_llm or config.llm_enabled:
        message = _improve_with_llm(message, repo_path, files_str, changes)

    return message


def generate_conventional_message(changes: List[Change]) -> str:
    """Generate a conventional commits format message."""
    if not changes:
        return "chore: empty commit"
    
    # Determine type from tags
    tags = set(_all_tags(changes))
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
    scope = _infer_scope(changes)
    
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
    
    tag = _summary_tag(changes)
    files = [c.path for c in changes]
    
    if len(files) == 1:
        return f"{tag}: {files[0]}"
    else:
        return f"{tag}: {len(files)} files ({', '.join(files[:3])}{'...' if len(files) > 3 else ''})"


def generate_oneline_message(changes: List[Change]) -> str:
    """Generate a one-line commit message."""
    if not changes:
        return "empty commit"
    
    tag = _summary_tag(changes)
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


def _all_tags(changes: List[Change]) -> List[Tag]:
    """Return unique tags across all changes, preserving first-seen order."""
    tags = []
    seen = set()
    for change in changes:
        for tag in change.tags:
            if tag not in seen:
                tags.append(tag)
                seen.add(tag)
    return tags


def _all_tag_values(changes: List[Change]) -> List[str]:
    """Return unique tag values across all changes."""
    return [tag.value for tag in _all_tags(changes)]


def _summary_tag(changes: List[Change]) -> str:
    """Choose a stable tag prefix for a commit spanning one or more changes."""
    tags = _all_tags(changes)
    if not tags:
        return "#small"
    if len(tags) == 1:
        return tags[0].value
    return "#all"


_BUILTIN_TEMPLATES = {
    "default": "{tag}: {count} files ({files})",
    "simple": "{tag}: {count} files",
    "short": "{tag}: {files}",
}


def _render_template(
    template: str,
    changes: List[Change],
    *,
    tag: str,
    files: str,
    count: int,
) -> str:
    """Render a commit message from a built-in template name or a custom format string.

    ``template`` is either a known built-in name (``default``/``simple``/``short``)
    or a raw ``str.format`` template using ``{tag}``, ``{files}``, ``{count}``.
    """
    fmt = _BUILTIN_TEMPLATES.get(template, template)
    try:
        return fmt.format(tag=tag, files=files, count=count)
    except (KeyError, IndexError, ValueError):
        # Unknown placeholder in a custom template — fall back to a safe default.
        return f"{tag}: {count} files"


def _improve_with_llm(
    message: str,
    repo_path: str,
    files_str: str,
    changes: List[Change],
) -> str:
    """Best-effort LLM refinement of a commit message.

    Returns the original message unchanged if the optional LLM backend is
    unavailable or errors — LLM enhancement is optional, never required.
    """
    try:
        from tagi.llm import LlxAdapter

        adapter = LlxAdapter(repo_path=repo_path, enabled=True)
        return adapter.improve_message(message, context=files_str)
    except Exception:
        return message


def _infer_scope(changes: List[Change]) -> str:
    """Infer scope from file paths."""
    if not changes:
        return ""
    
    paths = [c.path.lower() for c in changes]
    
    # Check for common patterns using a mapping
    scope_patterns = [
        (["test"], "tests"),
        (["doc"], "docs"),
        (["config"], "config"),
        (["api"], "api"),
        (["cli"], "cli"),
        (["ui", "web", "frontend"], "ui"),
        (["db", "database"], "db"),
    ]
    
    for patterns, scope in scope_patterns:
        if any(pattern in p for p in paths for pattern in patterns):
            return scope
    
    return "general"
