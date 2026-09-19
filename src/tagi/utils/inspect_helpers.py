"""Helper functions for inspect command.

Compatibility facade: the implementation was split (PLF-130) into cohesive
submodules and is re-exported here so existing imports keep working:

- :mod:`tagi.utils.change_filter` — tag-based change filtering;
- :mod:`tagi.utils.change_stats` — statistics aggregation and rendering.
"""

from tagi.utils.change_filter import (
    filter_changes_by_tag,
    filter_changes_by_tags_all,
    filter_changes_by_tags_any,
    resolve_filtered_changes,
)
from tagi.utils.change_stats import calculate_tag_statistics, display_statistics_table

__all__ = [
    "calculate_tag_statistics",
    "display_statistics_table",
    "filter_changes_by_tag",
    "filter_changes_by_tags_all",
    "filter_changes_by_tags_any",
    "resolve_filtered_changes",
]
