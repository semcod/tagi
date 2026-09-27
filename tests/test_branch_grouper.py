"""Unit tests for tagi.planner.branch_grouper (PLF-192).

Covers ``group_by_branch``/``get_branch_info`` against real temporary git
repositories: branch detection, change grouping per branch, detached HEAD,
missing branch metadata, and the ``run_command`` failure paths both
functions guard with try/except.

Behavior locked in by these tests (verified against git 2.51):

- ``git branch --contains HEAD -- <path>`` does not filter by pathspec;
  git treats the trailing argument as a branch-name *pattern*. Ordinary
  file paths match no branch, so ``group_by_branch`` falls back to the
  current branch for every change. Only a change whose path coincides
  with a branch name resolves to that branch.
- ``git branch --show-current`` exits 0 with empty output on a detached
  HEAD, so the fallback branch key is the empty string.
- ``git branch -a`` on a detached HEAD lists a ``(HEAD detached at <sha>)``
  pseudo-entry, which ``get_branch_info`` reports like a real branch.
"""

import subprocess
from pathlib import Path

import pytest

from tagi.models.change import Change, ChangeType
from tagi.planner.branch_grouper import get_branch_info, group_by_branch
from tagi.utils import commands


def _run_git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Create a git repository on ``main`` with a ``feature`` branch."""
    _run_git("init", "-b", "main", cwd=tmp_path)
    _run_git("config", "user.email", "test@example.com", cwd=tmp_path)
    _run_git("config", "user.name", "Test User", cwd=tmp_path)
    (tmp_path / "README.md").write_text("initial\n")
    _run_git("add", "README.md", cwd=tmp_path)
    _run_git("commit", "-m", "init", cwd=tmp_path)
    _run_git("checkout", "-b", "feature", cwd=tmp_path)
    (tmp_path / "feature.txt").write_text("feature work\n")
    _run_git("add", "feature.txt", cwd=tmp_path)
    _run_git("commit", "-m", "feat", cwd=tmp_path)
    _run_git("checkout", "main", cwd=tmp_path)
    return tmp_path


def _change(path: str) -> Change:
    return Change(path=path, change_type=ChangeType.MODIFIED)


def _raise(cmd, cwd="."):
    raise RuntimeError("git unavailable")


class TestGroupByBranch:
    def test_no_changes_returns_empty_grouping(self, tmp_repo):
        assert group_by_branch([], repo_path=str(tmp_repo)) == {}

    def test_groups_changes_under_current_branch(self, tmp_repo):
        """Paths matching no branch name fall back to the current branch."""
        changes = [_change("README.md"), _change("src/app.py")]

        groups = group_by_branch(changes, repo_path=str(tmp_repo))

        assert set(groups) == {"main"}
        assert groups["main"] == changes

    def test_groups_under_checked_out_branch(self, tmp_repo):
        _run_git("checkout", "feature", cwd=tmp_repo)

        groups = group_by_branch([_change("feature.txt")], repo_path=str(tmp_repo))

        assert set(groups) == {"feature"}

    def test_path_matching_branch_name_resolves_to_that_branch(self, tmp_repo):
        """git treats the change path as a branch-name pattern, so a file
        literally named like a branch groups under that branch."""
        (tmp_repo / "release").write_text("named like a branch\n")
        _run_git("add", "release", cwd=tmp_repo)
        _run_git("commit", "-m", "add file named like a branch", cwd=tmp_repo)
        _run_git("branch", "release", cwd=tmp_repo)

        release_change = _change("release")
        other_change = _change("other.txt")
        groups = group_by_branch(
            [release_change, other_change], repo_path=str(tmp_repo)
        )

        assert groups["release"] == [release_change]
        assert groups["main"] == [other_change]

    def test_detached_head_groups_under_empty_branch_key(self, tmp_repo):
        """``git branch --show-current`` succeeds with empty output when
        detached, so the fallback branch key is the empty string."""
        _run_git("checkout", "--detach", "HEAD", cwd=tmp_repo)

        groups = group_by_branch([_change("README.md")], repo_path=str(tmp_repo))

        assert set(groups) == {""}

    def test_not_a_repository_falls_back_to_main(self, tmp_path):
        """Outside a repository both git calls fail (rc != 0) and changes
        group under the get_current_branch fallback name."""
        groups = group_by_branch([_change("a.txt")], repo_path=str(tmp_path))

        assert set(groups) == {"main"}

    def test_run_command_failure_falls_back_to_current_branch(
        self, tmp_repo, monkeypatch
    ):
        """A raising run_command is swallowed per change; the current branch
        still resolves because GitExecutor bound run_command at import time."""
        monkeypatch.setattr(commands, "run_command", _raise)

        groups = group_by_branch([_change("README.md")], repo_path=str(tmp_repo))

        assert set(groups) == {"main"}


class TestGetBranchInfo:
    def test_lists_local_and_remote_branches(self, tmp_repo, tmp_path):
        remote = tmp_path / "origin.git"
        remote.mkdir()
        _run_git("init", "--bare", "-b", "main", cwd=remote)
        _run_git("remote", "add", "origin", str(remote), cwd=tmp_repo)
        _run_git("push", "-q", "origin", "main", cwd=tmp_repo)
        _run_git("push", "-q", "origin", "feature", cwd=tmp_repo)
        _run_git("fetch", "-q", "origin", cwd=tmp_repo)

        info = get_branch_info(str(tmp_repo))

        assert set(info) == {
            "main",
            "feature",
            "remotes/origin/HEAD -> origin/main",
            "remotes/origin/main",
            "remotes/origin/feature",
        }
        assert set(info.values()) == set(info)

    def test_detached_head_includes_pseudo_branch(self, tmp_repo):
        sha = _run_git("rev-parse", "--short", "HEAD", cwd=tmp_repo).strip()
        _run_git("checkout", "--detach", "HEAD", cwd=tmp_repo)

        info = get_branch_info(str(tmp_repo))

        assert "main" in info
        assert "feature" in info
        assert info[f"(HEAD detached at {sha})"] == f"(HEAD detached at {sha})"

    def test_unborn_repository_returns_no_branches(self, tmp_path):
        """A freshly initialized repo has no commits and lists no branches."""
        _run_git("init", "-b", "main", cwd=tmp_path)

        assert get_branch_info(str(tmp_path)) == {}

    def test_not_a_repository_returns_empty(self, tmp_path):
        assert get_branch_info(str(tmp_path)) == {}

    def test_run_command_failure_returns_empty(self, tmp_repo, monkeypatch):
        monkeypatch.setattr(commands, "run_command", _raise)

        assert get_branch_info(str(tmp_repo)) == {}


if __name__ == "__main__":
    pytest.main([__file__])
