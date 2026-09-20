"""CLI tests for ``tagi.cli.inspection_commands`` (PLF-211).

Covers the ``inspect``, ``filter`` and ``file`` command paths end-to-end
through the Typer app, including tag normalization, statistics/changes
rendering, tag descriptions from ``tagi.toml``, ``--diff`` rendering,
any/all filter modes, no-match notices and missing-argument usage errors.

Logic paths run against a faked scan pipeline (the pattern from
``tests/test_cli_tag_stats_regression.py``); diff paths run against real
scratch git repositories (the pattern from
``tests/test_cli_file_regression.py``).
"""

import subprocess
from pathlib import Path

from typer.testing import CliRunner

from tagi.cli import app
from tagi.models import Change, ChangeType, Tag

runner = CliRunner()


def _git(cwd, *args):
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def _make_repo_with_modified_file(tmpdir):
    """Create a git repo containing one committed-then-modified file."""
    _git(tmpdir, "init", "-q")
    _git(tmpdir, "config", "user.email", "test@test.com")
    _git(tmpdir, "config", "user.name", "Test User")

    mod_file = Path(tmpdir) / "mod.py"
    mod_file.write_text("print('hello')\n")
    _git(tmpdir, "add", "mod.py")
    _git(tmpdir, "commit", "-qm", "init")
    mod_file.write_text("print('hello')\nprint('world')\n")
    return mod_file


def _sample_changes():
    return [
        Change(
            path="a.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL, Tag.DOCS],
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
    ]


def _install_fake_scan(monkeypatch, changes):
    """Patch the scan pipeline to return deterministic tagged changes."""

    def fake_scan_repo(_repo_path):
        return changes

    def fake_apply_tags(scanned, _repo_path):
        return scanned

    monkeypatch.setattr("tagi.cli.scan_repo", fake_scan_repo)
    monkeypatch.setattr("tagi.cli.apply_tags", fake_apply_tags)


# ---------------------------------------------------------------------------
# inspect
# ---------------------------------------------------------------------------


def test_inspect_missing_tag_argument_is_usage_error():
    """``tagi inspect`` without a tag fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["inspect"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_inspect_no_changes_for_tag(monkeypatch):
    """A tag with no matching changes prints a notice and exits cleanly."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["inspect", "#small", "."])
    assert result.exit_code == 0
    assert "No changes found for #small" in result.output


def test_inspect_renders_statistics_and_changes(monkeypatch):
    """``tagi inspect #small`` shows the stats table and the change list."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["inspect", "#small", "."])
    assert result.exit_code == 0
    assert "Inspecting #small" in result.output
    assert "Files" in result.output
    assert "Total Lines" in result.output
    assert "Avg Risk Score" in result.output
    assert "a.py" in result.output
    assert "b.py" in result.output


def test_inspect_normalizes_tag_without_hash_prefix(monkeypatch):
    """``tagi inspect small`` filters by ``#small`` after normalization."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["inspect", "small", "."])
    assert result.exit_code == 0
    assert "Inspecting small" in result.output
    assert "a.py" in result.output


def test_inspect_shows_tag_description_from_config(tmp_path):
    """A ``tagi.toml`` tag definition is rendered as the tag description."""
    mod_file = _make_repo_with_modified_file(str(tmp_path))
    (tmp_path / "tagi.toml").write_text(
        '[tag_definitions]\n"#small" = "Small-scoped changes"\n'
    )

    result = runner.invoke(app, ["inspect", "#small", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "Small-scoped changes" in result.output
    assert mod_file.name in result.output


def test_inspect_diff_flag_renders_diffs(tmp_path):
    """``--diff`` appends the per-file git diff, capped at five files."""
    _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["inspect", "#small", str(tmp_path), "--diff"])

    assert result.exit_code == 0, result.output
    assert "Diffs:" in result.output
    assert "print('world')" in result.output


# ---------------------------------------------------------------------------
# filter
# ---------------------------------------------------------------------------


def test_filter_missing_tags_argument_is_usage_error():
    """``tagi filter`` without tags fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["filter"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_filter_no_matching_changes(monkeypatch):
    """No matching changes prints a notice and exits cleanly."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["filter", "#small,#docs", "."])
    assert result.exit_code == 0
    assert "No changes found for tags: #small,#docs" in result.output


def test_filter_any_mode_matches_union(monkeypatch):
    """Default ``any`` mode matches changes carrying at least one tag."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["filter", "#small,#docs", "."])
    assert result.exit_code == 0
    assert "Filtering changes by tags: #small,#docs" in result.output
    assert "a.py" in result.output
    assert "b.py" in result.output


def test_filter_all_mode_requires_every_tag(monkeypatch):
    """``--mode all`` only matches changes carrying every requested tag."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["filter", "#small,#docs", ".", "--mode", "all"])
    assert result.exit_code == 0
    assert "a.py" in result.output
    assert "b.py" not in result.output


def test_filter_strips_whitespace_around_tags(monkeypatch):
    """Comma-separated tags are trimmed before matching."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["filter", " #small , #docs ", ".", "--mode", "all"])
    assert result.exit_code == 0
    assert "a.py" in result.output
    assert "b.py" not in result.output


def test_filter_diff_flag_renders_diffs(tmp_path):
    """``--diff`` appends the git diff for matched changes."""
    _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["filter", "#small", str(tmp_path), "--diff"])

    assert result.exit_code == 0, result.output
    assert "Diffs:" in result.output
    assert "print('world')" in result.output


# ---------------------------------------------------------------------------
# file
# ---------------------------------------------------------------------------


def test_file_missing_path_argument_is_usage_error():
    """``tagi file`` without a path fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["file"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_file_not_in_change_set(tmp_path):
    """A path outside the change set reports a notice and exits cleanly."""
    _make_repo_with_modified_file(str(tmp_path))
    result = runner.invoke(app, ["file", "missing.py", str(tmp_path)])
    assert result.exit_code == 0
    assert "File not found in changes: missing.py" in result.output


def test_file_diff_reports_no_diff_when_staged(tmp_path):
    """``--diff`` on a fully staged file reports that no diff is available."""
    mod_file = _make_repo_with_modified_file(str(tmp_path))
    _git(str(tmp_path), "add", mod_file.name)

    result = runner.invoke(app, ["file", mod_file.name, str(tmp_path), "--diff"])

    assert result.exit_code == 0, result.output
    assert "Diff:" in result.output
    assert "No diff available" in result.output
