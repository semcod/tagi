"""Regression tests for the ``tagi file`` crash on missing Change.description (PLF-188).

``file_command`` used to read ``file_change.description``, but the ``Change``
dataclass (``src/tagi/models/change.py``) has no ``description`` field, so
``tagi file <path>`` crashed with
``AttributeError: 'Change' object has no attribute 'description'`` on any
scanned file. These tests run ``tagi file`` end-to-end against a scratch git
repo with a modified file so the crash cannot recur.
"""

import subprocess
from pathlib import Path

from typer.testing import CliRunner

from tagi.cli import app


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


def test_file_command_on_modified_file(tmp_path):
    """``tagi file`` on a modified file renders details instead of crashing."""
    mod_file = _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["file", mod_file.name, str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "File not found" not in result.output
    assert f"File: {mod_file.name}" in result.output
    assert "Type: modified" in result.output
    assert "Tags:" in result.output
    assert "AttributeError" not in result.output


def test_file_command_with_diff_on_modified_file(tmp_path):
    """``tagi file --diff`` shows the working-tree diff without crashing."""
    mod_file = _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["file", mod_file.name, str(tmp_path), "--diff"])

    assert result.exit_code == 0, result.output
    assert "Diff:" in result.output
    assert "print('world')" in result.output
    assert "AttributeError" not in result.output


def test_file_command_unknown_file(tmp_path):
    """``tagi file`` reports a clean message for files outside the change set."""
    _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["file", "missing.py", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "File not found in changes: missing.py" in result.output
