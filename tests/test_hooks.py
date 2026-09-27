"""Unit tests for ``tagi.hooks`` (PLF-191).

Locks the git-hook integration module behind direct unit tests against a
temporary git repository: hook installation (including hooks-directory
bootstrap and idempotence), listing (executable files only, sorted),
``run_hook`` dispatch (execution with the repository as cwd, exit-code
propagation, missing-hook error, running the installed tagi hook) and
uninstall semantics, plus the OSError failure branches of
install/uninstall that the CLI-level tests cannot reach.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

from tagi.hooks import (
    check_hooks_installed,
    install_hooks,
    list_hooks,
    run_hook,
    uninstall_hooks,
)


def _git(cwd, *args):
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def _make_repo(tmpdir):
    """Create a minimal git repository and return it as a str path."""
    _git(tmpdir, "init", "-q")
    _git(tmpdir, "config", "user.email", "test@test.com")
    _git(tmpdir, "config", "user.name", "Test User")
    return str(tmpdir)


def _write_hook(repo, name, body):
    """Write an executable hook script into the repository's hooks dir."""
    hook = Path(repo) / ".git" / "hooks" / name
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(body)
    hook.chmod(0o755)
    return hook


# ---------------------------------------------------------------------------
# install_hooks / check_hooks_installed
# ---------------------------------------------------------------------------


def test_install_creates_executable_pre_commit_hook(tmp_path):
    """Installing writes an executable pre-commit hook containing tagi."""
    repo = _make_repo(tmp_path)
    assert install_hooks(repo) is True

    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    assert hook.exists()
    assert "tagi" in hook.read_text()
    assert hook.stat().st_mode & 0o111
    assert check_hooks_installed(repo) is True


def test_install_bootstraps_missing_hooks_dir(tmp_path):
    """A missing .git/hooks directory is created on install."""
    repo = _make_repo(tmp_path)
    shutil.rmtree(tmp_path / ".git" / "hooks")

    assert install_hooks(repo) is True
    assert (tmp_path / ".git" / "hooks" / "pre-commit").exists()


def test_install_is_idempotent(tmp_path):
    """Reinstalling overwrites the hook with identical content."""
    repo = _make_repo(tmp_path)
    assert install_hooks(repo) is True
    first = (tmp_path / ".git" / "hooks" / "pre-commit").read_text()

    assert install_hooks(repo) is True
    assert (tmp_path / ".git" / "hooks" / "pre-commit").read_text() == first


def test_install_returns_false_when_hook_cannot_be_written(tmp_path):
    """An unwritable hook path makes install_hooks report failure."""
    repo = _make_repo(tmp_path)
    (tmp_path / ".git" / "hooks" / "pre-commit").mkdir()

    assert install_hooks(repo) is False


def test_check_hooks_installed_ignores_foreign_hook(tmp_path):
    """A pre-commit hook without tagi content does not count as installed."""
    repo = _make_repo(tmp_path)
    _write_hook(repo, "pre-commit", "#!/bin/bash\nexit 0\n")

    assert check_hooks_installed(repo) is False


# ---------------------------------------------------------------------------
# uninstall_hooks
# ---------------------------------------------------------------------------


def test_uninstall_removes_installed_hook(tmp_path):
    """Uninstalling deletes the hook and flips the installed check."""
    repo = _make_repo(tmp_path)
    install_hooks(repo)

    assert uninstall_hooks(repo) is True
    assert not (tmp_path / ".git" / "hooks" / "pre-commit").exists()
    assert check_hooks_installed(repo) is False


def test_uninstall_without_hook_succeeds(tmp_path):
    """Uninstalling when no hook exists is a no-op that still succeeds."""
    repo = _make_repo(tmp_path)

    assert uninstall_hooks(repo) is True
    assert not (tmp_path / ".git" / "hooks" / "pre-commit").exists()


def test_uninstall_returns_false_when_unlink_fails(tmp_path):
    """A hook path that cannot be unlinked makes uninstall report failure."""
    repo = _make_repo(tmp_path)
    hook_dir = tmp_path / ".git" / "hooks" / "pre-commit"
    hook_dir.mkdir()
    (hook_dir / "payload.txt").write_text("x")

    assert uninstall_hooks(repo) is False


# ---------------------------------------------------------------------------
# list_hooks
# ---------------------------------------------------------------------------


def test_list_hooks_empty_without_hooks_dir(tmp_path):
    """A missing hooks directory yields an empty hook list."""
    repo = _make_repo(tmp_path)
    shutil.rmtree(tmp_path / ".git" / "hooks")

    assert list_hooks(repo) == []


def test_list_hooks_reports_only_executable_files_sorted(tmp_path):
    """Only executable hooks are listed, in sorted order."""
    repo = _make_repo(tmp_path)
    shutil.rmtree(tmp_path / ".git" / "hooks")
    install_hooks(repo)
    _write_hook(repo, "pre-push", "#!/bin/bash\nexit 0\n")
    plain = tmp_path / ".git" / "hooks" / "commit-msg"
    plain.write_text("#!/bin/bash\nexit 0\n")
    plain.chmod(0o644)

    assert list_hooks(repo) == ["pre-commit", "pre-push"]


# ---------------------------------------------------------------------------
# run_hook
# ---------------------------------------------------------------------------


def test_run_hook_executes_hook_with_repo_as_cwd(tmp_path):
    """run_hook executes the hook, captures stdout and uses the repo as cwd."""
    repo = _make_repo(tmp_path)
    _write_hook(
        repo,
        "pre-push",
        "#!/bin/bash\necho hook-ran\ntouch hook-cwd-marker.txt\n",
    )

    result = run_hook("pre-push", repo)

    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 0
    assert "hook-ran" in result.stdout
    assert (tmp_path / "hook-cwd-marker.txt").exists()


def test_run_hook_propagates_non_zero_exit_code(tmp_path):
    """A failing hook is reported through the exit code, not an exception."""
    repo = _make_repo(tmp_path)
    _write_hook(repo, "pre-push", "#!/bin/bash\nexit 42\n")

    result = run_hook("pre-push", repo)

    assert result.returncode == 42


def test_run_hook_missing_hook_raises(tmp_path):
    """Running an unknown hook name raises FileNotFoundError."""
    repo = _make_repo(tmp_path)

    with pytest.raises(FileNotFoundError, match="no-such-hook"):
        run_hook("no-such-hook", repo)


def test_run_installed_tagi_pre_commit_hook_exits_zero(tmp_path):
    """The installed tagi hook is valid bash and always exits 0."""
    repo = _make_repo(tmp_path)
    install_hooks(repo)

    result = run_hook("pre-commit", repo)

    assert result.returncode == 0
