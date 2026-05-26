"""Grouper module for organizing changes into groups."""

from collections import defaultdict
from typing import List

from tagi.models import Change, ChangeGroup, Tag


def group_changes(changes: List[Change]) -> List[ChangeGroup]:
    """Group changes by their primary tag."""
    grouped = defaultdict(list)
    
    for change in changes:
        if change.tags:
            primary_tag = change.tags[0]
            grouped[primary_tag].append(change)
        else:
            from tagi.models import Tag
            grouped[Tag.SMALL].append(change)
    
    groups = []
    for tag, tag_changes in grouped.items():
        total_lines = sum(c.lines_changed for c in tag_changes)
        avg_risk = sum(c.risk_score for c in tag_changes) / len(tag_changes) if tag_changes else 0.0
        
        group = ChangeGroup(
            name=tag.value,
            changes=tag_changes,
            tags=[tag],
            total_lines=total_lines,
            avg_risk=avg_risk
        )
        groups.append(group)
    
    return sorted(groups, key=lambda g: g.avg_risk)


def group_by_tag(changes: List[Change], tag: Tag) -> List[Change]:
    """Filter changes by a specific tag."""
    return [c for c in changes if tag in c.tags]
