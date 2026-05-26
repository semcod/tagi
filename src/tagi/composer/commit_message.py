"""Commit message module for generating commit messages."""

from typing import List

from tagi.models import Change, Tag
from tagi.config import Config


def generate_commit_message(changes: List[Change], template: str = "default", repo_path: str = ".", use_llm: bool = False) -> str:
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
        message = generate_conventional_message(changes)
    elif template == "detailed":
        message = generate_detailed_message(changes)
    elif template == "simple":
        message = generate_simple_message(changes)
    elif template == "oneline":
        message = generate_oneline_message(changes)
    elif template == "files":
        message = generate_files_message(changes)
    else:
        message = template.format(tag=tag, files=files_str, count=count)
    
    # Optionally improve with LLM
    if use_llm or config.llm_enabled:
        from tagi.llm import LlxAdapter
        llm = LlxAdapter(repo_path, enabled=True)
        context = f"Files: {files_str}, Tags: {[t.value for t in changes[0].tags] if changes else []}"
        message = llm.improve_message(message, context)
    
    return message


def generate_conventional_message(changes: List[Change]) -> str:
    """Generate a conventional commits format message."""
    if not changes:
        return "chore: empty commit"
    
    # Determine type from tags
    tags = changes[0].tags
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


def generate_simple_message(changes: List[Change]) -> str:
    """Generate a simple commit message."""
    if not changes:
        return "Empty commit"
    
    tag = changes[0].tags[0].value if changes and changes[0].tags else "small"
    files = [c.path for c in changes]
    
    if len(files) == 1:
        return f"{tag}: {files[0]}"
    else:
        return f"{tag}: {len(files)} files ({', '.join(files[:3])}{'...' if len(files) > 3 else ''})"


def generate_oneline_message(changes: List[Change]) -> str:
    """Generate a one-line commit message."""
    if not changes:
        return "empty commit"
    
    tag = changes[0].tags[0].value if changes and changes[0].tags else "small"
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
