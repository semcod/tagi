"""Selector module for choosing changes."""

from typing import List

from tagi.models import Change, Tag


def select_changes_by_tag(changes: List[Change], tag: Tag) -> List[Change]:
    """Select changes that have a specific tag."""
    return [c for c in changes if tag in c.tags]


def select_low_risk_changes(changes: List[Change], threshold: float = 0.5) -> List[Change]:
    """Select changes with risk score below threshold."""
    return [c for c in changes if c.risk_score < threshold]


def select_small_changes(changes: List[Change], max_lines: int = 100) -> List[Change]:
    """Select changes with lines changed below max_lines."""
    return [c for c in changes if c.lines_changed <= max_lines]
