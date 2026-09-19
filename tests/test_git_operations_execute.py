"""Regression tests for the tagi send execution path (_execute_git_operations).

Covers PLF-182: ``_execute_git_operations`` must stage and commit changes via
the real ``GitExecutor`` API (``add(files)``) instead of the non-existent
``stage(path)`` method.
"""

import subprocess
from pathlib import Path

import pytest

from tagi.cli.git_operations import _execute_git_operations
from tagi.models.change import Change, ChangeType


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
    """Create a git repository with one committed file."""
    _run_git("init", cwd=tmp_path)
    _run_git("config", "user.email", "test@example.com", cwd=tmp_path)
    _run_git("config", "user.name", "Test User", cwd=tmp_path)
    (tmp_path / "README.md").write_text("initial\n")
    _run_git("add", "README.md", cwd=tmp_path)
    _run_git("commit", "-m", "init", cwd=tmp_path)
    return tmp_path


def _last_commit_message(repo: Path) -> str:
    return _run_git("log", "-1", "--pretty=%B", cwd=repo).strip()


def _last_commit_files(repo: Path) -> list:
    output = _run_git("show", "--name-only", "--pretty=format:", "HEAD", cwd=repo)
    return [line for line in output.splitlines() if line]


def _status_is_clean(repo: Path) -> bool:
    status = _run_git("status", "--porcelain", cwd=repo)
    return status.strip() == ""


class TestExecuteGitOperations:
    def test_stages_and_commits_all_changes(self, tmp_repo):
        """Changes are batch-staged and committed in one commit (no push)."""
        (tmp_repo / "a.txt").write_text("alpha\n")
        (tmp_repo / "b.txt").write_text("beta\n")

        changes = [
            Change(path="a.txt", change_type=ChangeType.ADDED),
            Change(path="b.txt", change_type=ChangeType.ADDED),
        ]

        _execute_git_operations(
            changes, "test: send changes", push=False, repo_path=str(tmp_repo)
        )

        committed = _last_commit_files(tmp_repo)
        assert "a.txt" in committed
        assert "b.txt" in committed
        assert "README.md" not in committed
        assert _status_is_clean(tmp_repo)

    def test_uses_provided_commit_message(self, tmp_repo):
        """The generated commit message lands on the new commit."""
        (tmp_repo / "c.txt").write_text("gamma\n")

        changes = [Change(path="c.txt", change_type=ChangeType.ADDED)]

        _execute_git_operations(
            changes, "feat: add c.txt #small", push=False, repo_path=str(tmp_repo)
        )

        assert _last_commit_message(tmp_repo) == "feat: add c.txt #small"

    def test_modified_files_are_committed(self, tmp_repo):
        """Modifications to tracked files are staged and committed too."""
        (tmp_repo / "README.md").write_text("updated\n")

        changes = [Change(path="README.md", change_type=ChangeType.MODIFIED)]

        _execute_git_operations(
            changes, "docs: update readme", push=False, repo_path=str(tmp_repo)
        )

        assert "README.md" in _last_commit_files(tmp_repo)
        assert (tmp_repo / "README.md").read_text() == "updated\n"


if __name__ == "__main__":
    pytest.main([__file__])
