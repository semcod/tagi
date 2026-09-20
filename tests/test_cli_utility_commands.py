"""CLI tests for ``tagi.cli.utility_commands`` (PLF-211).

Covers the ``summary``, ``init``, ``hooks`` and ``draft`` command paths
end-to-end through the Typer app: report rendering and ``--output``
handling, config bootstrap (copy example vs. default fallback, ``--force``
overwrite), git-hook install/uninstall/list/status branches including
failure exits, draft tag resolution, and missing-argument usage errors.
"""

import shutil
import subprocess

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


def _make_repo(tmpdir):
    """Create a minimal git repository."""
    _git(tmpdir, "init", "-q")
    _git(tmpdir, "config", "user.email", "test@test.com")
    _git(tmpdir, "config", "user.name", "Test User")


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
# summary
# ---------------------------------------------------------------------------


def test_summary_no_changes(monkeypatch):
    """An empty change set prints a notice and exits successfully."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["summary", "."])
    assert result.exit_code == 0
    assert "No changes found" in result.output


def test_summary_renders_report_to_stdout(monkeypatch):
    """The summary report lists totals, per-tag counts and file details."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["summary", "."])
    assert result.exit_code == 0
    assert "# Change Summary Report" in result.output
    assert "Total changes: 2" in result.output
    assert "- #small: 2 change(s)" in result.output
    assert "- #tests: 1 change(s)" in result.output
    assert "**a.py**" in result.output
    assert "**b.py**" in result.output
    assert "Tags: #small, #tests" in result.output


def test_summary_writes_output_file(monkeypatch, tmp_path):
    """``--output`` writes the report to a file instead of stdout."""
    _install_fake_scan(monkeypatch, _sample_changes())
    out_file = tmp_path / "summary.md"
    result = runner.invoke(app, ["summary", ".", "--output", str(out_file)])
    assert result.exit_code == 0
    assert "Summary saved to:" in result.output
    content = out_file.read_text()
    assert "# Change Summary Report" in content
    assert "Total changes: 2" in content


def test_summary_includes_change_description(monkeypatch):
    """A change exposing a ``description`` attribute renders it in the report."""

    class DescribedChange(Change):
        description = "Reworks the parsing loop"

    changes = [
        DescribedChange(
            path="a.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL],
        )
    ]
    _install_fake_scan(monkeypatch, changes)
    result = runner.invoke(app, ["summary", "."])
    assert result.exit_code == 0
    assert "Description: Reworks the parsing loop" in result.output


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


def test_init_creates_config_in_fresh_repo(tmp_path):
    """``tagi init`` creates a tagi.toml in the target repository."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    result = runner.invoke(app, ["init", str(repo)])
    assert result.exit_code == 0
    assert "Created tagi.toml at" in result.output
    assert (repo / "tagi.toml").exists()
    assert (repo / "tagi.toml").read_text().strip() != ""


def test_init_existing_config_without_force(tmp_path):
    """An existing tagi.toml without ``--force`` is left untouched."""
    repo = tmp_path / "repo"
    repo.mkdir()
    config = repo / "tagi.toml"
    config.write_text("# existing config\n")
    result = runner.invoke(app, ["init", str(repo)])
    assert result.exit_code == 0
    assert "tagi.toml already exists" in result.output
    assert "Use --force to overwrite" in result.output
    assert config.read_text() == "# existing config\n"


def test_init_force_overwrites_existing_config(tmp_path):
    """``--force`` overwrites an existing tagi.toml."""
    repo = tmp_path / "repo"
    repo.mkdir()
    config = repo / "tagi.toml"
    config.write_text("# old\n")
    result = runner.invoke(app, ["init", str(repo), "--force"])
    assert result.exit_code == 0
    assert "Created tagi.toml" in result.output
    assert "already exists" not in result.output
    assert config.read_text() != "# old\n"


def test_init_falls_back_to_default_config(monkeypatch, tmp_path):
    """Without a bundled example, init writes the built-in default config."""
    # Point the module at a tree guaranteed to contain no tagi.toml example.
    fake_module = tmp_path / "a" / "b" / "c" / "utility_commands.py"
    fake_module.parent.mkdir(parents=True)
    fake_module.write_text("")
    monkeypatch.setattr("tagi.cli.utility_commands.__file__", str(fake_module))

    repo = tmp_path / "repo"
    repo.mkdir()
    result = runner.invoke(app, ["init", str(repo)])
    assert result.exit_code == 0
    config = repo / "tagi.toml"
    assert config.exists()
    content = config.read_text()
    assert "# tagi configuration" in content
    assert "[tags]" in content
    assert "[colors]" in content


# ---------------------------------------------------------------------------
# hooks
# ---------------------------------------------------------------------------


def test_hooks_status_not_installed(tmp_path):
    """Default hooks command reports the not-installed status."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    result = runner.invoke(app, ["hooks", str(repo)])
    assert result.exit_code == 0
    assert "tagi hooks are not installed" in result.output
    assert "Run: tagi hooks --install" in result.output


def test_hooks_install_uninstall_and_status(tmp_path):
    """Installing creates the pre-commit hook; uninstalling removes it."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    hook = repo / ".git" / "hooks" / "pre-commit"

    result = runner.invoke(app, ["hooks", str(repo), "--install"])
    assert result.exit_code == 0
    assert "Installed tagi hooks in" in result.output
    assert hook.exists()
    assert "tagi" in hook.read_text()

    result = runner.invoke(app, ["hooks", str(repo)])
    assert result.exit_code == 0
    assert "tagi hooks are installed" in result.output

    result = runner.invoke(app, ["hooks", str(repo), "--uninstall"])
    assert result.exit_code == 0
    assert "Removed tagi hooks from" in result.output
    assert not hook.exists()


def test_hooks_list_empty_when_no_hooks(tmp_path):
    """``--list`` reports when no hooks exist."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    # A fresh git init ships only *.sample hooks; drop them to get an empty
    # hooks directory.
    shutil.rmtree(repo / ".git" / "hooks")
    result = runner.invoke(app, ["hooks", str(repo), "--list"])
    assert result.exit_code == 0
    assert "No hooks installed" in result.output


def test_hooks_list_shows_installed_hooks(tmp_path):
    """``--list`` after install shows the tagi pre-commit hook."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    runner.invoke(app, ["hooks", str(repo), "--install"])
    result = runner.invoke(app, ["hooks", str(repo), "--list"])
    assert result.exit_code == 0
    assert "Installed hooks:" in result.output
    assert "pre-commit" in result.output


def test_hooks_install_failure_exits(monkeypatch, tmp_path):
    """A failing install reports the error and exits with code 1."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    monkeypatch.setattr("tagi.hooks.install_hooks", lambda _repo: False)
    result = runner.invoke(app, ["hooks", str(repo), "--install"])
    assert result.exit_code == 1
    assert "Failed to install hooks" in result.output


def test_hooks_uninstall_failure_exits(monkeypatch, tmp_path):
    """A failing uninstall reports the error and exits with code 1."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _make_repo(str(repo))
    monkeypatch.setattr("tagi.hooks.uninstall_hooks", lambda _repo: False)
    result = runner.invoke(app, ["hooks", str(repo), "--uninstall"])
    assert result.exit_code == 1
    assert "Failed to uninstall hooks" in result.output


# ---------------------------------------------------------------------------
# draft
# ---------------------------------------------------------------------------


def test_draft_missing_tag_argument_is_usage_error():
    """``tagi draft`` without a tag fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["draft"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_draft_unknown_tag_exits_nonzero(monkeypatch):
    """An unrecognized tag reports an error and exits with code 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["draft", "#nope", "."])
    assert result.exit_code == 1
    assert "Unknown tag: #nope" in result.output


def test_draft_no_changes_for_tag(monkeypatch):
    """A known tag with no matching changes exits cleanly with a notice."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["draft", "#small", "."])
    assert result.exit_code == 0
    assert "No changes found for #small" in result.output


def test_draft_renders_commit_message(monkeypatch):
    """A matched tag drafts a commit message and lists the changes."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["draft", "#small", "."])
    assert result.exit_code == 0
    assert "Draft commit message:" in result.output
    assert "Changes included: 2" in result.output
    assert "a.py" in result.output
    assert "b.py" in result.output
