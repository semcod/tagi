"""Aggregate metric helpers for change sets."""

from typing import List

from tagi.models import Change


def total_lines_changed(changes: List[Change]) -> int:
    """Return the summed lines_changed across changes, or 0 for an empty set.

    Single owner of the total-lines computation for change sets.

    Args:
        changes: Changes to total

    Returns:
        Sum of lines_changed (0 when changes is empty)
    """
    return sum(c.lines_changed for c in changes)


def average_risk(changes: List[Change]) -> float:
    """Return the mean risk score across changes, or 0.0 for an empty set.

    Args:
        changes: Changes to average

    Returns:
        Mean risk score (0.0 when changes is empty)
    """
    if not changes:
        return 0.0
    return sum(c.risk_score for c in changes) / len(changes)
