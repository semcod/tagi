"""Helper functions for send command."""

from typing import List, Optional
from tagi.models import Change, Tag, ChangeGroup
from tagi.utils.risk import average_risk


def create_change_group(
    changes: List[Change],
    tag: Optional[str]
) -> ChangeGroup:
    """Create a ChangeGroup from filtered changes.
    
    Args:
        changes: Changes to include in group
        tag: Tag name (None for "all")
        
    Returns:
        ChangeGroup instance
    """
    total_lines = sum(c.lines_changed for c in changes)

    if tag is None:
        group_name = "all"
        group_tags = []
    else:
        group_name = tag
        tag_enum = Tag(tag)
        group_tags = [tag_enum]
    
    return ChangeGroup(
        name=group_name,
        changes=changes,
        tags=group_tags,
        total_lines=total_lines,
        avg_risk=average_risk(changes)
    )
