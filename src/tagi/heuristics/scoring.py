"""Scoring module for calculating risk scores."""

from typing import List

from tagi.models import Change, ChangeType, Tag

_TAG_RISK_WEIGHTS = {
    Tag.RISKY: 0.5,
    Tag.CONFIG: 0.2,
    Tag.DEPS: 0.3,
    Tag.LARGE: 0.2,
}

_CHANGE_TYPE_RISK_WEIGHTS = {
    ChangeType.DELETED: 0.3,
    ChangeType.RENAMED: 0.1,
}


def calculate_risk_score(change: Change, tags: List[Tag]) -> float:
    """Calculate a risk score for a change."""
    score = _lines_risk_weight(change.lines_changed)
    score += _tag_risk_weight(tags)
    score += _change_type_risk_weight(change.change_type)

    return min(score, 1.0)


def _lines_risk_weight(lines_changed: int) -> float:
    """Base score from lines changed."""
    return min(lines_changed / 100.0, 1.0) * 0.3


def _tag_risk_weight(tags: List[Tag]) -> float:
    """Sum of risk weights for the present tags."""
    return sum(weight for tag, weight in _TAG_RISK_WEIGHTS.items() if tag in tags)


def _change_type_risk_weight(change_type: ChangeType) -> float:
    """Risk weight for the change type."""
    return _CHANGE_TYPE_RISK_WEIGHTS.get(change_type, 0.0)
