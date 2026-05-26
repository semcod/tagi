"""Helper functions for send command."""

from typing import List, Optional
from tagi.models import Change, Tag, ChangeGroup
from tagi.composer.commit_message import generate_commit_message


def resolve_filtered_changes(
    changes: List[Change],
    tag: Optional[str],
    auto_order: bool,
    sort_by_complexity_func
) -> tuple[List[Change], Optional[str]]:
    """Resolve filtered changes based on tag and auto_order.
    
    Args:
        changes: All changes
        tag: Optional tag to filter by
        auto_order: Whether to sort by complexity
        sort_by_complexity_func: Function to sort by complexity
        
    Returns:
        Tuple of (filtered_changes, final_tag)
    """
    if tag is None:
        filtered_changes = changes
    else:
        from tagi.cli import _ensure_tag_prefix
        tag = _ensure_tag_prefix(tag)
        tag_enum = Tag(tag)
        filtered_changes = [c for c in changes if tag_enum in c.tags]
    
    if auto_order:
        filtered_changes = sort_by_complexity_func(filtered_changes)
        tag = None  # Mark as no tag filtering
    
    return filtered_changes, tag


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
