"""Helper functions for send command."""

from typing import List, Optional
from tagi.models import Change, Tag, ChangeGroup


def create_change_group(
    filtered_changes: List[Change],
    tag: Optional[str]
) -> ChangeGroup:
    """Create a ChangeGroup from filtered changes.
    
    Args:
        filtered_changes: Changes to include in group
        tag: Tag name (None for "all")
        
    Returns:
        ChangeGroup instance
    """
    total_lines = sum(c.lines_changed for c in filtered_changes)
    avg_risk = sum(c.risk_score for c in filtered_changes) / len(filtered_changes) if filtered_changes else 0.0
    
    if tag is None:
        group_name = "all"
        group_tags = []
    else:
        group_name = tag
        tag_enum = Tag(tag)
        group_tags = [tag_enum]
    
    return ChangeGroup(
        name=group_name,
        changes=filtered_changes,
        tags=group_tags,
        total_lines=total_lines,
        avg_risk=avg_risk
    )
