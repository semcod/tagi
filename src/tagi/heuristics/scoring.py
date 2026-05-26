"""Scoring module for calculating risk scores."""

from typing import List

from tagi.models import Change, Tag


def calculate_risk_score(change: Change, tags: List[Tag]) -> float:
    """Calculate a risk score for a change."""
    score = 0.0
    
    # Base score from lines changed
    score += min(change.lines_changed / 100.0, 1.0) * 0.3
    
    # Risk from tags
    if Tag.RISKY in tags:
        score += 0.5
    if Tag.CONFIG in tags:
        score += 0.2
    if Tag.DEPS in tags:
        score += 0.3
    if Tag.LARGE in tags:
        score += 0.2
    
    # Risk from change type
    if change.change_type == ChangeType.DELETED:
        score += 0.3
    elif change.change_type == ChangeType.RENAMED:
        score += 0.1
    
    return min(score, 1.0)
