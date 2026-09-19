"""Statistics aggregation and rendering for change sets.

Extracted from ``tagi.utils.inspect_helpers`` (PLF-130). Metric
computation lives in :func:`calculate_tag_statistics`; rendering lives in
:func:`display_statistics_table`.
"""

from typing import List

from rich.console import Console
from rich.table import Table

from tagi.models import Change
from tagi.utils.risk import average_risk, total_lines_changed


def calculate_tag_statistics(changes: List[Change]) -> tuple[int, float]:
    """Calculate statistics for a tag group.

    Args:
        changes: Changes in the tag group

    Returns:
        Tuple of (total_lines, avg_risk)
    """
    return total_lines_changed(changes), average_risk(changes)


def display_statistics_table(changes: List[Change], console: Console) -> None:
    """Display statistics table for changes.

    Args:
        changes: Changes to display statistics for
        console: Rich console instance
    """
    stats_table = Table()
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    stats_table.add_row("Files", str(len(changes)))
    stats_table.add_row("Total Lines", str(total_lines_changed(changes)))
    stats_table.add_row("Avg Risk Score", f"{average_risk(changes):.2f}")
    console.print(stats_table)
