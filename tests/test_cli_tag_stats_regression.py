"""Regression tests for the per-tag counting crash in list/stats/summary (PLF-181).

``calculate_tag_statistics`` returns a ``(total_lines, avg_risk)`` tuple —
pinned by ``tests/test_change_stats.py`` — while the ``list``, ``stats
--verbose`` and ``summary`` commands need per-tag counts. These tests pin the
``count_changes_by_tag`` helper and run the three CLI commands end-to-end so
the ``AttributeError: 'tuple' object has no attribute 'items'`` crash cannot
recur.
"""

from typer.testing import CliRunner

from tagi.cli import app
from tagi.models import Change, ChangeType, Tag
from tagi.utils.change_stats import count_changes_by_tag


runner = CliRunner()


def _sample_changes():
    return [
        Change(
            path="a.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL, Tag.TESTS],
            lines_changed=10,
            risk_score=1.0,
        ),
        Change(
            path="b.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL],
            lines_changed=40,
            risk_score=3.0,
        ),
        Change(
            path="docs.md",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.DOCS],
            lines_changed=5,
            risk_score=0.5,
        ),
    ]


def _install_fake_scan(monkeypatch):
    """Patch the scan pipeline to return deterministic tagged changes."""

    def fake_scan_repo(_repo_path):
        return _sample_changes()

    def fake_apply_tags(changes, _repo_path):
        return changes

    monkeypatch.setattr("tagi.cli.scan_repo", fake_scan_repo)
    monkeypatch.setattr("tagi.cli.apply_tags", fake_apply_tags)


def test_count_changes_by_tag_counts_every_tag():
    """Each tag on each change is counted, including multi-tag changes."""
    counts = count_changes_by_tag(_sample_changes())
    assert counts == {"#small": 2, "#tests": 1, "#docs": 1}


def test_count_changes_by_tag_empty_group():
    """An empty change group yields an empty mapping without raising."""
    assert count_changes_by_tag([]) == {}


def test_count_changes_by_tag_untagged_change():
    """Untagged changes contribute no entries."""
    counts = count_changes_by_tag(
        [Change(path="a.py", change_type=ChangeType.MODIFIED)]
    )
    assert counts == {}


def test_list_command_reports_tag_counts(monkeypatch):
    """``tagi list`` renders per-tag counts instead of crashing."""
    _install_fake_scan(monkeypatch)
    result = runner.invoke(app, ["list", "."])
    assert result.exit_code == 0
    assert "Available change groups" in result.stdout
    assert "#small: 2 change(s)" in result.stdout
    assert "#tests: 1 change(s)" in result.stdout
    assert "#docs: 1 change(s)" in result.stdout


def test_stats_verbose_breaks_down_by_tag(monkeypatch):
    """``tagi stats --verbose`` renders a per-tag breakdown instead of crashing."""
    _install_fake_scan(monkeypatch)
    result = runner.invoke(app, ["stats", ".", "--verbose"])
    assert result.exit_code == 0
    assert "Detailed breakdown" in result.stdout
    assert "#small" in result.stdout and "2 changes" in result.stdout
    assert "a.py" in result.stdout and "b.py" in result.stdout


def test_summary_includes_changes_by_tag(monkeypatch):
    """``tagi summary`` renders "Changes by Tag" instead of crashing."""
    _install_fake_scan(monkeypatch)
    result = runner.invoke(app, ["summary", "."])
    assert result.exit_code == 0
    assert "Changes by Tag" in result.stdout
    assert "- #small: 2 change(s)" in result.stdout
    assert "- #docs: 1 change(s)" in result.stdout
