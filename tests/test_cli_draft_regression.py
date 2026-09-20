"""Regression tests for the ``tagi draft`` crash on ChangeGroup iteration (PLF-189).

``draft_command`` used to pass the whole ``ChangeGroup`` to
``generate_commit_message``, which expects ``List[Change]`` and iterates it,
so ``tagi draft <tag>`` crashed with
``TypeError: 'ChangeGroup' object is not iterable``. These tests run
``tagi draft`` end-to-end against a scratch git repo with a modified file so
the crash cannot recur.
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


def test_draft_command_renders_commit_message(tmp_path):
    """``tagi draft #small`` renders a draft message instead of crashing."""
    _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["draft", "#small", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "Draft commit message:" in result.output
    assert "TypeError" not in result.output
    assert "'ChangeGroup' object is not iterable" not in result.output


def test_draft_command_without_hash_prefix(tmp_path):
    """``tagi draft small`` normalizes the tag and still renders a message."""
    _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(app, ["draft", "small", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "Draft commit message:" in result.output


def test_draft_command_with_template(tmp_path):
    """``tagi draft --template conventional`` renders the chosen template."""
    mod_file = _make_repo_with_modified_file(str(tmp_path))

    result = runner.invoke(
        app, ["draft", "#small", str(tmp_path), "--template", "conventional"]
    )

    assert result.exit_code == 0, result.output
    assert "Draft commit message:" in result.output
    assert "Changes included: 1" in result.output
    assert mod_file.name in result.output
