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
    
    return LineBuilder([
        f"Plan: {len(changes)} files",
        "-" * 40,
        *(
            f"  [{change.change_type.value:8}] {change.path:40} "
            f"({', '.join(t.value for t in change.tags)})"
            for change in changes
        ),
    ]).text()


def preview_changes(group: ChangeGroup) -> str:
    """Generate a preview for a change group."""
    return LineBuilder([
        f"Group: {group.name}",
        f"Files: {len(group.changes)}",
        f"Total Lines: {group.total_lines}",
        f"Avg Risk: {group.avg_risk:.2f}",
        "-" * 40,
        *(
            f"  [{change.change_type.value:8}] {change.path:40} "
            f"({', '.join(t.value for t in change.tags)})"
            for change in group.changes
        ),
    ]).text()
