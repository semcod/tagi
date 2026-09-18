"""Preview module for showing execution plans."""

from typing import List

from tagi.models import Change, ChangeGroup
from tagi.utils.line_builder import LineBuilder


def preview_plan(changes: List[Change], tag: str = None) -> str:
    """Generate a preview of the execution plan."""
    if tag:
        from tagi.models import Tag
        tag_enum = Tag(tag)
        changes = [c for c in changes if tag_enum in c.tags]
    
    if not changes:
        return "No changes to preview."
    
    builder = LineBuilder()
    builder.add(f"Plan: {len(changes)} files")
    builder.add("-" * 40)
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        builder.add(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    return builder.text()


def preview_changes(group: ChangeGroup) -> str:
    """Generate a preview for a change group."""
    builder = LineBuilder()
    builder.add(f"Group: {group.name}")
    builder.add(f"Files: {len(group.changes)}")
    builder.add(f"Total Lines: {group.total_lines}")
    builder.add(f"Avg Risk: {group.avg_risk:.2f}")
    builder.add("-" * 40)
    
    for change in group.changes:
        tags_str = ", ".join([t.value for t in change.tags])
        builder.add(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    return builder.text()
