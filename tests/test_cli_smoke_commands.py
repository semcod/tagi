"""Smoke tests for every command registered on the tagi typer app (PLF-185).

The PLF-180 coverage audit found the CLI command layer nearly untested
(utility_commands 14%, inspection_commands 18%, core_commands 22%,
executor/git.py 46%): ``test_cli_regression.py`` only asserts ``--help``
output, so runtime crashes like PLF-181/182/183 stayed invisible to a
green suite.

Every test here drives the real typer app through ``CliRunner`` against a
fixture git repository and asserts exit code 0 with no traceback. Commands
that would mutate git or talk to a provider run their dry-run/preview path,
or have the executor boundary replaced with a recording fake, so no real
git mutation ever leaves the fixture repository.
"""

import shutil
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from tagi.cli import app
from tagi.cli.scan_utils import scan_and_tag


def _git(repo: Path, *args: str) -> None:
    """Run git in the fixture repo, failing loudly on unexpected errors."""
    subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    )


@pytest.fixture(scope="session")
def repo_template(tmp_path_factory):
    """Build the pristine fixture repo once.

    The dirty tree is chosen so the heuristic tagger produces a known set
    of tags the smoke recipes rely on:

    - ``app.py``: tracked then modified, no path heuristic matches -> #small
    - ``README.md``: untracked -> #docs (+ #new)
    - ``tests/test_helper.py``: untracked -> #tests (+ #new)

    A github origin remote is configured so provider detection has something
    to find; nothing ever contacts it.
    """
    repo = tmp_path_factory.mktemp("tagi-smoke-template") / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "tagi-fixture@example.com")
    _git(repo, "config", "user.name", "Tagi Fixture")
    app_py = repo / "app.py"
    app_py.write_text("def main():\n    print('hello')\n")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "initial")
    app_py.write_text("def main():\n    print('hello')\n    print('world')\n")
    (repo / "README.md").write_text("# Fixture\n")
    tests = repo / "tests"
    tests.mkdir()
    (tests / "test_helper.py").write_text("def test_fixture():\n    assert True\n")
    _git(
        repo,
        "remote",
        "add",
        "origin",
        "https://github.com/tagi-fixture/fixture.git",
    )
    return repo


@pytest.fixture
def repo(repo_template, tmp_path):
    """Per-test pristine copy so command side effects never leak between tests."""
    copy = tmp_path / "repo"
    shutil.copytree(repo_template, copy)
    return copy


def _assert_clean_smoke(result, marker=None):
    """Assert a smoke invocation exited cleanly without any traceback."""
    assert result.exit_code == 0, result.output
    assert "Traceback" not in result.output
    if marker is not None:
        assert marker in result.output


# One smoke invocation per command registered on the typer app. The
# completeness test below fails when a command is registered without a case
# here (or vice versa), so the suite cannot drift away from the app surface.
SMOKE_ARGV = {
    "scan": lambda repo: ["scan", str(repo)],
    "list": lambda repo: ["list", str(repo)],
    "list-groups": lambda repo: ["list-groups", str(repo)],
    "stats": lambda repo: ["stats", str(repo)],
    "inspect": lambda repo: ["inspect", "docs", str(repo)],
    "filter": lambda repo: ["filter", "#docs,#tests", str(repo)],
    "file": lambda repo: ["file", "README.md", str(repo)],
    "send": lambda repo: ["send", "small", "--path", str(repo), "--dry-run"],
    "auto": lambda repo: ["auto", str(repo), "--dry-run"],
    "publish": lambda repo: ["publish", "docs", str(repo), "--dry-run"],
    "deploy": lambda repo: ["deploy", "docs", str(repo), "--dry-run"],
    "summary": lambda repo: ["summary", str(repo)],
    "draft": lambda repo: ["draft", "docs", str(repo)],
    "init": lambda repo: ["init", str(repo)],
    "hooks": lambda repo: ["hooks", str(repo)],
}

# Marker proving each command actually ran its body (exit 0 alone would also
# hold for a command that returns early on its "nothing to do" path).
SMOKE_MARKERS = {
    "scan": "Scanning",
    "list": "Available change groups",
    "list-groups": "Available change groups",
    "stats": "Statistics",
    "inspect": "Inspecting",
    "filter": "Filtering",
    "file": "File:",
    "send": "DRY-RUN",
    "auto": "Auto mode",
    "publish": "Dry run",
    "deploy": "Dry run",
    "summary": "Change Summary Report",
    "draft": "Draft commit message",
    "init": "Created tagi.toml",
    "hooks": "hooks",
}


def _registered_command_names():
    return {
        command.name or command.callback.__name__
        for command in app.registered_commands
    }


class TestRegisteredCommandSmoke:
    """Invoke every registered command against the fixture repo."""

    def test_every_registered_command_has_a_smoke_case(self):
        """The smoke table covers exactly the commands registered on the app."""
        assert _registered_command_names() == set(SMOKE_ARGV)

    @pytest.mark.parametrize("command", sorted(SMOKE_ARGV))
    def test_command_exits_cleanly(self, command, repo):
        result = CliRunner().invoke(app, SMOKE_ARGV[command](repo))
        _assert_clean_smoke(result, SMOKE_MARKERS[command])


class TestFixtureContract:
    """Pin the fixture tags the smoke recipes rely on."""

    def test_fixture_provides_expected_tags(self, repo):
        """If the heuristics change, fix the recipes here, not silently."""
        changes = scan_and_tag(str(repo))
        tags = {tag.value for change in changes for tag in change.tags}
        assert {"#small", "#docs", "#tests"} <= tags


class TestSmokeVariations:
    """Second-path coverage for options that change the code path taken."""

    def test_scan_grouped(self, repo):
        result = CliRunner().invoke(app, ["scan", str(repo), "--grouped"])
        _assert_clean_smoke(result, "Scanning")

    def test_stats_verbose(self, repo):
        result = CliRunner().invoke(app, ["stats", str(repo), "--verbose"])
        _assert_clean_smoke(result, "Detailed breakdown")

    def test_inspect_with_diff(self, repo):
        result = CliRunner().invoke(app, ["inspect", "small", str(repo), "--diff"])
        _assert_clean_smoke(result, "Diffs:")

    def test_file_with_diff(self, repo):
        result = CliRunner().invoke(
            app, ["file", "app.py", str(repo), "--diff"]
        )
        _assert_clean_smoke(result, "Diff:")

    def test_filter_mode_all(self, repo):
        result = CliRunner().invoke(
            app, ["filter", "#docs,#new", str(repo), "--mode", "all"]
        )
        _assert_clean_smoke(result, "Filtering")

    def test_send_all_changes_dry_run(self, repo):
        """Positional repository path (tag=None) also previews cleanly."""
        result = CliRunner().invoke(app, ["send", str(repo), "--dry-run"])
        _assert_clean_smoke(result, "DRY-RUN")

    def test_summary_writes_output_file(self, repo, tmp_path):
        report = tmp_path / "summary.md"
        result = CliRunner().invoke(
            app, ["summary", str(repo), "--output", str(report)]
        )
        _assert_clean_smoke(result, "Summary saved")
        assert "# Change Summary Report" in report.read_text()

    def test_init_is_idempotent_without_force(self, repo):
        runner = CliRunner()
        _assert_clean_smoke(runner.invoke(app, ["init", str(repo)]))
        again = runner.invoke(app, ["init", str(repo)])
        _assert_clean_smoke(again, "already exists")
        assert (repo / "tagi.toml").exists()

    def test_hooks_install_list_uninstall_cycle(self, repo):
        runner = CliRunner()
        _assert_clean_smoke(runner.invoke(app, ["hooks", str(repo)]))
        _assert_clean_smoke(
            runner.invoke(app, ["hooks", str(repo), "--install"]), "Installed tagi hooks"
        )
        _assert_clean_smoke(runner.invoke(app, ["hooks", str(repo), "--list"]))
        _assert_clean_smoke(
            runner.invoke(app, ["hooks", str(repo), "--uninstall"]),
            "Removed tagi hooks",
        )
        _assert_clean_smoke(
            runner.invoke(app, ["hooks", str(repo)]), "not installed"
        )


class TestExecutorBoundaries:
    """Exercise the mutating paths with the executor boundary faked."""

    def test_send_stages_and_commits_through_executor(self, repo, monkeypatch):
        """Real (non-dry-run) send goes through GitExecutor, which is faked."""
        calls = []

        class FakeGitExecutor:
            def __init__(self, repo_path):
                self.repo_path = repo_path

            def add(self, files):
                calls.append(("add", list(files)))
                return True

            def commit(self, message):
                calls.append(("commit", message))
                return True

        monkeypatch.setattr(
            "tagi.cli.git_operations.GitExecutor", FakeGitExecutor
        )
        result = CliRunner().invoke(app, ["send", "small", "--path", str(repo)])
        _assert_clean_smoke(result, "Committed 1 change(s)")
        assert [name for name, _ in calls] == ["add", "commit"]
        assert calls[0][1] == ["app.py"]
        assert calls[1][1]  # a commit message was produced

    def test_publish_creates_pr_through_executor(self, repo, monkeypatch):
        """Real (non-dry-run) publish goes through PublishExecutor, faked."""

        class FakePublishExecutor:
            def __init__(self, repo_path):
                self.repo_path = repo_path

            def create_github_pr(self, group, template="default"):
                return "https://github.com/tagi-fixture/fixture/pull/1"

        monkeypatch.setattr(
            "tagi.cli.publishing_commands.PublishExecutor", FakePublishExecutor
        )
        result = CliRunner().invoke(app, ["publish", "docs", str(repo)])
        _assert_clean_smoke(result, "Pull request created")

    def test_deploy_without_dry_run_is_placeholder(self, repo):
        result = CliRunner().invoke(app, ["deploy", "docs", str(repo)])
        _assert_clean_smoke(result, "not yet implemented")


class TestDetectProviderFunction:
    """detect-provider is a plain function, not a registered typer command."""

    def test_detects_github_remote(self, repo):
        from tagi.cli import detect_provider

        assert detect_provider(str(repo)) == "github"

    def test_returns_none_without_remote(self, repo):
        _git(repo, "remote", "remove", "origin")
        from tagi.cli import detect_provider

        assert detect_provider(str(repo)) is None


if __name__ == "__main__":
    pytest.main([__file__])
