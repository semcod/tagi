"""Tag-based change filtering.

Single owner of tag-based change filtering, extracted from
``tagi.utils.inspect_helpers`` (PLF-130). The public entry point is
:func:`resolve_filtered_changes`; the ``filter_changes_by_*`` helpers are
thin conveniences around it.
"""

from typing import List, Union

from tagi.models import Change, Tag


def _normalize_tag(value: str) -> str:
    """Return the tag value with a leading ``#`` ensured."""
    return value if value.startswith("#") else f"#{value}"


def _changes_matching_tag(changes: List[Change], tag_enum: Tag) -> List[Change]:
    """Return the changes carrying a single resolved tag."""
    return [c for c in changes if tag_enum in c.tags]


def _resolve_tag_enums(tags: List[str]) -> List[Tag]:
    """Resolve tag strings to Tag enums, ignoring unknown values."""
    tag_enums = []
    for t in tags:
        try:
            tag_enums.append(Tag(_normalize_tag(t)))
        except ValueError:
            continue
    return tag_enums


def _changes_matching_any(changes: List[Change], tag_enums: List[Tag]) -> List[Change]:
    """Return changes carrying at least one of the tags (OR logic)."""
    return [c for c in changes if any(tag in c.tags for tag in tag_enums)]


def _changes_matching_all(changes: List[Change], tag_enums: List[Tag]) -> List[Change]:
    """Return changes carrying every tag (AND logic)."""
    return [c for c in changes if all(tag in c.tags for tag in tag_enums)]


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
        return _changes_matching_tag(changes, Tag(_normalize_tag(tags)))

    tag_enums = _resolve_tag_enums(tags)
    if not tag_enums:
        return changes

    if mode == "all":
        return _changes_matching_all(changes, tag_enums)
    return _changes_matching_any(changes, tag_enums)


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
