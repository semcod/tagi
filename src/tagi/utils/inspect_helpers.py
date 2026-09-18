"""Helper functions for inspect command."""

from typing import List, Union
from rich.table import Table
from rich.console import Console
from tagi.models import Change, Tag
from tagi.utils.risk import average_risk


def resolve_filtered_changes(
    changes: List[Change],
    tags: Union[str, List[str], None] = None,
    mode: str = "any",
) -> List[Change]:
    """Resolve the changes a command operates on, filtered by tags.

    Single owner of tag-based change filtering:

    - ``tags`` is None: all changes are returned;
    - ``tags`` is a single tag string: the ``#`` prefix is normalized and an
      unknown tag raises ``ValueError``;
    - ``tags`` is a list: unknown tags are ignored and changes matching any
      (``mode="any"``, the default) or all (``mode="all"``) of the valid tags
      are returned; all changes are returned when no tag is valid.

    Args:
        changes: All changes
        tags: Tag or tags to filter by
        mode: Match mode for tag lists: "any" or "all"

    Returns:
        Filtered changes
    """
    if tags is None:
        return changes

    if isinstance(tags, str):
        tag_value = tags if tags.startswith("#") else f"#{tags}"
        tag_enum = Tag(tag_value)
        return [c for c in changes if tag_enum in c.tags]

    tag_enums = []
    for t in tags:
        try:
            tag_enums.append(Tag(t if t.startswith("#") else f"#{t}"))
        except ValueError:
            continue

    if not tag_enums:
        return changes

    if mode == "all":
        return [c for c in changes if all(tag in c.tags for tag in tag_enums)]
    return [c for c in changes if any(tag in c.tags for tag in tag_enums)]


def filter_changes_by_tag(changes: List[Change], tag: str) -> List[Change]:
    """Filter changes by tag.

    Args:
        changes: All changes
        tag: Tag to filter by

    Returns:
        Filtered changes
    """
    return resolve_filtered_changes(changes, tag)


def filter_changes_by_tags_any(changes: List[Change], tags: List[str]) -> List[Change]:
    """Filter changes by tags (OR logic).

    Args:
        changes: All changes
        tags: List of tags to filter by

    Returns:
        Changes matching any of the tags
    """
    return resolve_filtered_changes(changes, tags, mode="any")


def filter_changes_by_tags_all(changes: List[Change], tags: List[str]) -> List[Change]:
    """Filter changes by tags (AND logic).

    Args:
        changes: All changes
        tags: List of tags to filter by

    Returns:
        Changes matching all of the tags
    """
    return resolve_filtered_changes(changes, tags, mode="all")


def calculate_tag_statistics(changes: List[Change]) -> tuple[int, float]:
    """Calculate statistics for a tag group.
    
    Args:
        changes: Changes in the tag group
        
    Returns:
        Tuple of (total_lines, avg_risk)
    """
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    return total_lines, average_risk(changes)


def display_statistics_table(changes: List[Change], console: Console) -> None:
    """Display statistics table for changes.
    
    Args:
        changes: Changes to display statistics for
        console: Rich console instance
    """
    total_lines, group_avg_risk = calculate_tag_statistics(changes)

    stats_table = Table()
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    stats_table.add_row("Files", str(len(changes)))
    stats_table.add_row("Total Lines", str(total_lines))
    stats_table.add_row("Avg Risk Score", f"{group_avg_risk:.2f}")
    console.print(stats_table)
