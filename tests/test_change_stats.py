"""Regression tests for change statistics (inspect_helpers split).

These tests pin the behavior of the statistics half of
``tagi.utils.inspect_helpers`` before and after its extraction into
``tagi.utils.change_stats``.
"""

import io

from rich.console import Console

from tagi.models import Change, ChangeType, Tag
from tagi.utils.inspect_helpers import calculate_tag_statistics, display_statistics_table


def _change(path: str, lines: int, risk: float) -> Change:
    return Change(
        path=path,
        change_type=ChangeType.MODIFIED,
        tags=[Tag.SMALL],
        lines_changed=lines,
        risk_score=risk,
    )


def test_calculate_tag_statistics_returns_totals():
    """Statistics are (total lines, average risk) over the group."""
    changes = [
        _change("a.py", 10, 1.0),
        _change("b.py", 30, 3.0),
    ]
    total_lines, avg_risk = calculate_tag_statistics(changes)
    assert total_lines == 40
    assert abs(avg_risk - 2.0) < 1e-9


def test_calculate_tag_statistics_empty_group():
    """An empty group yields zero lines and 0.0 risk without raising."""
    assert calculate_tag_statistics([]) == (0, 0.0)


def _render_statistics(changes) -> str:
    buffer = io.StringIO()
    console = Console(file=buffer, width=120, force_terminal=False)
    display_statistics_table(changes, console)
    return buffer.getvalue()


def test_display_statistics_table_renders_all_metrics():
    """The table shows file count, total lines and average risk."""
    output = _render_statistics(
        [
            _change("a.py", 10, 1.0),
            _change("b.py", 30, 3.0),
            _change("c.py", 5, 2.0),
        ]
    )
    assert "Metric" in output
    assert "Files" in output and "3" in output
    assert "Total Lines" in output and "45" in output
    assert "Avg Risk Score" in output and "2.00" in output


def test_display_statistics_table_empty_group():
    """An empty change group renders zeroed metrics without raising."""
    output = _render_statistics([])
    assert "Files" in output and "0" in output
    assert "Total Lines" in output and "0" in output
    assert "Avg Risk Score" in output and "0.00" in output


def test_inspect_helpers_facade_reexports_change_stats():
    """The inspect_helpers facade re-exports the change_stats callables."""
    import tagi.utils.change_stats as change_stats
    import tagi.utils.inspect_helpers as facade

    assert (
        facade.calculate_tag_statistics is change_stats.calculate_tag_statistics
    )
    assert (
        facade.display_statistics_table is change_stats.display_statistics_table
    )
