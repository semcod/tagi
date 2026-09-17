"""Regression tests for commit message composition.

These tests cover the stable responsibilities behind `tagi.composer.commit_message`:
tag/scope analysis, template rendering, and the message-format generators. They are
written against the public surface so the module can be split into focused
submodules without changing behaviour.
"""

import tempfile
from pathlib import Path

import pytest

from tagi.models import Change, ChangeType, Tag
from tagi.composer.commit_message import (
    generate_commit_message,
    generate_conventional_message,
    generate_detailed_message,
    generate_simple_message,
    generate_oneline_message,
    generate_files_message,
)


def make_change(path, tag=None, change_type=ChangeType.MODIFIED):
    """Build a single-tag Change for a deterministic message."""
    change = Change(path=path, change_type=change_type)
    if tag is not None:
        change.tags = [tag]
    return change


class TestGenerateCommitMessage:
    def test_default_template(self):
        changes = [make_change("src/a.py", Tag.SMALL), make_change("src/b.py", Tag.SMALL)]
        assert generate_commit_message(changes, template="default") == (
            "#small: 2 files (src/a.py, src/b.py)"
        )

    def test_mixed_tags_use_all(self):
        changes = [make_change("a.py", Tag.SMALL), make_change("b.py", Tag.RISKY)]
        assert generate_commit_message(changes, template="default").startswith("#all:")

    def test_empty_changes(self):
        assert generate_commit_message([], template="default") == "#small: 0 files ()"

    def test_custom_template_from_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "tagi.toml").write_text(
                '[templates]\ncustom = "{tag} changed {count} files"\n'
            )
            changes = [make_change("a.py", Tag.SMALL)]
            assert generate_commit_message(changes, template="custom", repo_path=tmpdir) == (
                "#small changed 1 files"
            )

    def test_llm_fallback_returns_original(self):
        changes = [make_change("a.py", Tag.SMALL)]
        assert generate_commit_message(changes, use_llm=True) == generate_commit_message(changes)


class TestConventionalMessage:
    @pytest.mark.parametrize(
        "tag,commit_type",
        [
            (Tag.FEATURE, "feat"),
            (Tag.RISKY, "fix"),
            (Tag.DOCS, "docs"),
            (Tag.TESTS, "test"),
            (Tag.DEPS, "chore"),
            (Tag.REFACTOR, "refactor"),
            (Tag.CONFIG, "config"),
        ],
    )
    def test_type_from_tag(self, tag, commit_type):
        assert generate_conventional_message([make_change("a.py", tag)]).startswith(commit_type)

    def test_empty_changes(self):
        assert generate_conventional_message([]) == "chore: empty commit"

    def test_breaking_change(self):
        assert generate_conventional_message([make_change("a.py", Tag.RISKY)]) == (
            "fix(general)!: update a.py"
        )

    @pytest.mark.parametrize(
        "path,scope",
        [
            ("test_x.py", "tests"),
            ("docs/readme.md", "docs"),
            ("config.yaml", "config"),
            ("api.py", "api"),
            ("cli.py", "cli"),
            ("ui/web.py", "ui"),
            ("db.py", "db"),
            ("src/foo.py", "general"),
        ],
    )
    def test_scope_inference(self, path, scope):
        message = generate_conventional_message([make_change(path, Tag.FEATURE)])
        assert f"feat({scope}):" in message

    def test_multiple_files_description(self):
        changes = [make_change("a.py", Tag.FEATURE), make_change("b.py", Tag.FEATURE)]
        assert "update 2 files" in generate_conventional_message(changes)


class TestFormatGenerators:
    def test_detailed_message(self):
        changes = [make_change("a.py", Tag.SMALL), make_change("b.py", Tag.RISKY)]
        message = generate_detailed_message(changes)
        assert "Commit: 2 files changed" in message
        assert "  - #small: 1" in message
        assert "  - #risky: 1" in message
        assert "a.py" in message and "b.py" in message

    def test_simple_message_single(self):
        assert generate_simple_message([make_change("a.py", Tag.SMALL)]) == "#small: a.py"

    def test_simple_message_multiple_truncates(self):
        changes = [
            make_change("a.py", Tag.SMALL),
            make_change("b.py", Tag.SMALL),
            make_change("c.py", Tag.SMALL),
            make_change("d.py", Tag.SMALL),
        ]
        assert generate_simple_message(changes) == "#small: 4 files (a.py, b.py, c.py...)"

    def test_oneline_message_single(self):
        assert generate_oneline_message([make_change("a.py", Tag.SMALL)]) == "#small: a.py"

    def test_oneline_message_multiple(self):
        changes = [
            make_change("a.py", Tag.SMALL),
            make_change("b.py", Tag.SMALL),
            make_change("c.py", Tag.SMALL),
            make_change("d.py", Tag.SMALL),
        ]
        assert generate_oneline_message(changes) == "#small: a.py, b.py, c.py and 1 more"

    def test_files_message(self):
        message = generate_files_message([make_change("a.py", Tag.SMALL)])
        assert message.startswith("Changes (1 files):")
        assert "a.py" in message

    @pytest.mark.parametrize(
        "generator,expected",
        [
            (generate_detailed_message, "Empty commit"),
            (generate_simple_message, "Empty commit"),
            (generate_oneline_message, "empty commit"),
            (generate_files_message, "Empty commit"),
        ],
    )
    def test_empty_changes(self, generator, expected):
        assert generator([]) == expected
