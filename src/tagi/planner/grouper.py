"""Grouper module for organizing changes into groups."""

from collections import defaultdict
from typing import List, Dict

from tagi.models import Change, ChangeGroup, Tag


def group_changes(changes: List[Change]) -> List[ChangeGroup]:
    """Group changes by their primary tag."""
    grouped = defaultdict(list)
    
    for change in changes:
        if change.tags:
            # Use the highest priority tag as primary
            primary_tag = _get_primary_tag(change.tags)
            grouped[primary_tag].append(change)
        else:
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
    
    # Sort by risk score (safest first)
    return sorted(groups, key=lambda g: g.avg_risk)


def group_by_tag(changes: List[Change], tag: Tag) -> List[Change]:
    """Filter changes by a specific tag."""
    from tagi.planner.selector import select_changes_by_tag
    return select_changes_by_tag(changes, tag)


def group_by_risk(changes: List[Change], threshold: float = 0.5) -> Dict[str, List[Change]]:
    """Group changes by risk level."""
    low_risk = [c for c in changes if c.risk_score < threshold]
    high_risk = [c for c in changes if c.risk_score >= threshold]
    
    return {
        "low_risk": low_risk,
        "high_risk": high_risk
    }


def _get_primary_tag(tags: List[Tag]) -> Tag:
    """Get the primary tag based on priority."""
    # Priority order: RISKY > LARGE > DEPS > CONFIG > NEW > TESTS > DOCS > FEATURE > REFACTOR > SMALL
    priority = [
        Tag.RISKY,
        Tag.LARGE,
        Tag.DEPS,
        Tag.CONFIG,
        Tag.NEW,
        Tag.TESTS,
        Tag.DOCS,
        Tag.FEATURE,
        Tag.REFACTOR,
        Tag.SMALL
    ]
    
    for p in priority:
        if p in tags:
            return p
    
    return tags[0] if tags else Tag.SMALL
