"""Helper functions for publish command."""

from typing import List
from rich.console import Console
from tagi.models import Change, ChangeGroup, Tag
from tagi.utils.risk import average_risk, total_lines_changed


def create_publish_group(changes: List[Change], tag: str) -> ChangeGroup:
    """Create a ChangeGroup for publishing.
    
    Args:
        changes: Changes to include
        tag: Tag name
        
    Returns:
        ChangeGroup instance
    """
    tag_enum = Tag(tag)

    return ChangeGroup(
        name=tag,
        changes=changes,
        tags=[tag_enum],
        total_lines=total_lines_changed(changes),
        avg_risk=average_risk(changes)
    )
