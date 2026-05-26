"""Planner module for grouping changes."""

from collections import defaultdict
from typing import List

from tagi.models import Change, ChangeGroup, Tag


def group_changes(changes: List[Change]) -> List[ChangeGroup]:
    """Group changes by their tags."""
    tag_to_changes = defaultdict(list)
    
    for change in changes:
        for tag in change.tags:
            tag_to_changes[tag].append(change)
    
    groups = []
    for tag, tag_changes in tag_to_changes.items():
        group = ChangeGroup(
            name=tag.value,
            changes=tag_changes,
            tags=[tag],
            total_lines=sum(c.lines_changed for c in tag_changes),
            avg_risk=sum(c.risk_score for c in tag_changes) / len(tag_changes) if tag_changes else 0.0
        )
        groups.append(group)
    
    return groups
