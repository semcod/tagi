"""Regression tests for tag-based change filtering (inspect_helpers split).

These tests pin the behavior of the filtering half of
``tagi.utils.inspect_helpers`` before and after its extraction into
``tagi.utils.change_filter``.
"""

from tagi.models import Change, ChangeType, Tag
from tagi.utils.inspect_helpers import (
    filter_changes_by_tag,
    filter_changes_by_tags_all,
    filter_changes_by_tags_any,
    resolve_filtered_changes,
)


def _change(path: str, tags, lines: int = 10, risk: float = 1.0) -> Change:
    return Change(
        path=path,
        change_type=ChangeType.MODIFIED,
        tags=list(tags),
        lines_changed=lines,
        risk_score=risk,
    )


def _sample_changes():
    return [
        _change("small.py", [Tag.SMALL]),
        _change("small_docs.py", [Tag.SMALL, Tag.DOCS]),
        _change("docs.md", [Tag.DOCS]),
        _change("large.c", [Tag.LARGE]),
    ]


def test_no_tags_returns_all_changes_unchanged():
    """tags=None is a pass-through: the same list object is returned."""
    changes = _sample_changes()
    assert resolve_filtered_changes(changes, None) is changes


def test_single_tag_with_prefix_filters():
    """A single '#'-prefixed tag string selects matching changes."""
    result = resolve_filtered_changes(_sample_changes(), "#small")
    assert [c.path for c in result] == ["small.py", "small_docs.py"]


def test_single_tag_without_prefix_is_normalized():
    """A bare tag string gets the '#' prefix added before matching."""
    assert resolve_filtered_changes(_sample_changes(), "small") == (
        resolve_filtered_changes(_sample_changes(), "#small")
    )


def test_single_unknown_tag_raises_value_error():
    """An unknown single tag raises ValueError (no silent ignore)."""
    try:
        resolve_filtered_changes(_sample_changes(), "#nope")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for unknown single tag")


def test_tag_list_ignores_unknown_tags():
    """Unknown tags inside a list are skipped; known ones still filter."""
    result = resolve_filtered_changes(_sample_changes(), ["#nope", "#docs"])
    assert [c.path for c in result] == ["small_docs.py", "docs.md"]


def test_tag_list_with_no_valid_tags_returns_all_changes():
    """When no tag in the list is valid, all changes are returned."""
    changes = _sample_changes()
    result = resolve_filtered_changes(changes, ["#nope", "#alsonope"])
    assert result == changes


def test_empty_tag_list_returns_all_changes():
    """An empty tag list is not None: all changes are returned."""
    changes = _sample_changes()
    assert resolve_filtered_changes(changes, []) == changes


def test_tag_list_default_mode_is_any():
    """Default mode matches changes carrying ANY of the valid tags."""
    result = resolve_filtered_changes(_sample_changes(), ["#small", "#large"])
    assert [c.path for c in result] == ["small.py", "small_docs.py", "large.c"]


def test_tag_list_mode_all_requires_every_tag():
    """mode='all' only keeps changes carrying ALL of the valid tags."""
    result = resolve_filtered_changes(
        _sample_changes(), ["#small", "#docs"], mode="all"
    )
    assert [c.path for c in result] == ["small_docs.py"]


def test_filter_changes_by_tag_wrapper():
    """filter_changes_by_tag delegates to the single-tag resolution."""
    result = filter_changes_by_tag(_sample_changes(), "#docs")
    assert [c.path for c in result] == ["small_docs.py", "docs.md"]


def test_filter_changes_by_tags_any_wrapper():
    """filter_changes_by_tags_any applies OR logic."""
    result = filter_changes_by_tags_any(_sample_changes(), ["#small", "#large"])
    assert [c.path for c in result] == ["small.py", "small_docs.py", "large.c"]


def test_filter_changes_by_tags_all_wrapper():
    """filter_changes_by_tags_all applies AND logic."""
    result = filter_changes_by_tags_all(_sample_changes(), ["#small", "#docs"])
    assert [c.path for c in result] == ["small_docs.py"]


def test_inspect_helpers_facade_reexports_change_filter():
    """The inspect_helpers facade re-exports the change_filter callables."""
    import tagi.utils.change_filter as change_filter
    import tagi.utils.inspect_helpers as facade

    assert facade.resolve_filtered_changes is change_filter.resolve_filtered_changes
    assert facade.filter_changes_by_tag is change_filter.filter_changes_by_tag
    assert (
        facade.filter_changes_by_tags_any
        is change_filter.filter_changes_by_tags_any
    )
    assert (
        facade.filter_changes_by_tags_all
        is change_filter.filter_changes_by_tags_all
    )
