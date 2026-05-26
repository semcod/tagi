"""Preview module for showing execution plans."""

from typing import List

from tagi.models import Change, ChangeGroup


def preview_plan(changes: List[Change], tag: str = None) -> str:
    """Generate a preview of the execution plan."""
    if tag:
        from tagi.models import Tag
        tag_enum = Tag(tag)
        changes = [c for c in changes if tag_enum in c.tags]
    
    if not changes:
        return "No changes to preview."
    
    lines = []
    lines.append(f"Plan: {len(changes)} files")
    lines.append("-" * 40)
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    return "\n".join(lines)


def preview_changes(group: ChangeGroup) -> str:
    """Generate a preview for a change group."""
    lines = []
    lines.append(f"Group: {group.name}")
    lines.append(f"Files: {len(group.changes)}")
    lines.append(f"Total Lines: {group.total_lines}")
    lines.append(f"Avg Risk: {group.avg_risk:.2f}")
    lines.append("-" * 40)
    
    for change in group.changes:
        tags_str = ", ".join([t.value for t in change.tags])
        lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    return "\n".join(lines)
