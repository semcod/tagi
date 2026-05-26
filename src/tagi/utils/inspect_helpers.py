"""Helper functions for inspect command."""

from typing import List
from rich.table import Table
from rich.console import Console
from tagi.models import Change, Tag


def filter_changes_by_tag(changes: List[Change], tag: str) -> List[Change]:
    """Filter changes by tag.
    
    Args:
        changes: All changes
        tag: Tag to filter by
        
    Returns:
        Filtered changes
    """
    tag_enum = Tag(tag)
    return [c for c in changes if tag_enum in c.tags]


def calculate_tag_statistics(changes: List[Change]) -> tuple[int, float]:
    """Calculate statistics for a tag group.
    
    Args:
        changes: Changes in the tag group
        
    Returns:
        Tuple of (total_lines, avg_risk)
    """
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    avg_risk = sum(getattr(c, 'risk_score', 0) for c in changes) / len(changes) if changes else 0.0
    return total_lines, avg_risk


def display_statistics_table(changes: List[Change], console: Console) -> None:
    """Display statistics table for changes.
    
    Args:
        changes: Changes to display statistics for
        console: Rich console instance
    """
    total_lines, avg_risk = calculate_tag_statistics(changes)
    
    stats_table = Table()
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    stats_table.add_row("Files", str(len(changes)))
    stats_table.add_row("Total Lines", str(total_lines))
    stats_table.add_row("Avg Risk Score", f"{avg_risk:.2f}")
    console.print(stats_table)
