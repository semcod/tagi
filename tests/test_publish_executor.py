"""Unit tests for PublishExecutor PR/MR creation (PLF-183)."""

import os
import subprocess
import tempfile
from pathlib import Path

from click import unstyle
from typer.testing import CliRunner

from tagi.executor.publish import PrRequest, PublishExecutor
from tagi.models import Change, ChangeGroup, ChangeType, Tag
from tagi.providers.base import BaseProvider


runner = CliRunner()


class FakeProvider(BaseProvider):
    """In-memory provider recording every spec passed to create_pr."""

    name = "fake"

    def __init__(self, repo_path: str = "."):
        super().__init__(repo_path)
        self.specs = []

    def is_authenticated(self) -> bool:
        return True

    def get_auth_status(self) -> dict:
        return {"authenticated": True}

    def create_pr(self, spec) -> str:
        self.specs.append(spec)
        return f"https://example.fake/change-requests/{len(self.specs)}"

    def detect_remote(self) -> bool:
        return True


def _make_group() -> ChangeGroup:
    changes = [
        Change(
            path="src/a.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL],
            lines_changed=3,
        ),
        Change(
            path="src/b.py",
            change_type=ChangeType.ADDED,
            tags=[Tag.SMALL],
            lines_changed=5,
        ),
    ]
    return ChangeGroup(
        name="#small", changes=changes, tags=[Tag.SMALL], total_lines=8
    )


def _init_repo(tmpdir: str) -> None:
    """Initialize a git repository with an initial commit."""
    for cmd in (
        ["git", "init"],
        ["git", "config", "user.email", "test@test.com"],
        ["git", "config", "user.name", "Test User"],
    ):
        subprocess.run(cmd, cwd=tmpdir, capture_output=True)
    Path(tmpdir, "README.md").write_text("init\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmpdir, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmpdir, capture_output=True)


def test_create_github_pr_builds_spec_from_group():
    """create_github_pr builds a PrSpec and delegates to the provider."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        executor = PublishExecutor(tmpdir)
        fake = FakeProvider(tmpdir)

        url = executor.create_github_pr(PrRequest(_make_group(), provider=fake))

        assert url == "https://example.fake/change-requests/1"
        spec = fake.specs[0]
        assert spec.title == "#small: 2 files (src/a.py, src/b.py)"
        assert spec.body.startswith("#small: 2 files (src/a.py, src/b.py)")
        assert "Changes:" in spec.body
        assert "- src/a.py" in spec.body
        assert "- src/b.py" in spec.body
        assert spec.branch in ("main", "master")
        assert spec.base == "main"
        assert spec.draft is False
        assert spec.labels is None


def test_create_gitlab_mr_builds_spec_from_group():
    """create_gitlab_mr builds a PrSpec and delegates to the provider."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        executor = PublishExecutor(tmpdir)
        fake = FakeProvider(tmpdir)

        url = executor.create_gitlab_mr(PrRequest(_make_group(), provider=fake))

        assert url == "https://example.fake/change-requests/1"
        spec = fake.specs[0]
        assert spec.title == "#small: 2 files (src/a.py, src/b.py)"
        assert "- src/a.py" in spec.body
        assert "- src/b.py" in spec.body


def test_create_pr_template_selection_builtin():
    """The selected template drives the generated title."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        executor = PublishExecutor(tmpdir)
        fake = FakeProvider(tmpdir)

        executor.create_github_pr(PrRequest(_make_group(), template="simple", provider=fake))

        assert fake.specs[0].title == "#small: 2 files"


def test_create_pr_template_selection_custom():
    """Custom template strings are rendered through generate_commit_message."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        executor = PublishExecutor(tmpdir)
        fake = FakeProvider(tmpdir)

        executor.create_gitlab_mr(
            PrRequest(_make_group(), template="{tag}: {count} changed", provider=fake)
        )

        assert fake.specs[0].title == "#small: 2 changed"


def test_create_github_pr_defaults_to_github_provider(monkeypatch):
    """Without an injected provider, GitHubProvider is constructed and used."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        fake = FakeProvider(tmpdir)
        monkeypatch.setattr(
            "tagi.executor.publish.GitHubProvider", lambda path: fake
        )

        url = PublishExecutor(tmpdir).create_github_pr(PrRequest(_make_group()))

        assert url == "https://example.fake/change-requests/1"
        assert fake.specs[0].title == "#small: 2 files (src/a.py, src/b.py)"


def test_create_gitlab_mr_defaults_to_gitlab_provider(monkeypatch):
    """Without an injected provider, GitLabProvider is constructed and used."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        fake = FakeProvider(tmpdir)
        monkeypatch.setattr(
            "tagi.executor.publish.GitLabProvider", lambda path: fake
        )

        url = PublishExecutor(tmpdir).create_gitlab_mr(PrRequest(_make_group()))

        assert url == "https://example.fake/change-requests/1"
        assert fake.specs[0].title == "#small: 2 files (src/a.py, src/b.py)"


def test_publish_command_creates_pr_end_to_end(monkeypatch):
    """Regression: non-dry-run publish reaches the provider instead of crashing."""
    from tagi.cli import app

    def fake_scan_repo(_repo_path):
        return [Change(path="test.py", change_type=ChangeType.MODIFIED)]

    def fake_apply_tags(changes, _repo_path):
        changes[0].tags = [Tag.SMALL]
        return changes

    monkeypatch.setattr("tagi.cli.scan_repo", fake_scan_repo)
    monkeypatch.setattr("tagi.cli.apply_tags", fake_apply_tags)

    with tempfile.TemporaryDirectory() as tmpdir:
        _init_repo(tmpdir)
        os.system(
            f"cd {tmpdir} && git remote add origin https://github.com/test/repo.git > /dev/null 2>&1"
        )
        fake = FakeProvider(tmpdir)
        monkeypatch.setattr(
            "tagi.executor.publish.GitHubProvider", lambda path: fake
        )

        result = runner.invoke(app, ["publish", "small", tmpdir])

        assert result.exit_code == 0
        output = unstyle(result.stdout)
        assert "Pull request created" in output
        assert "https://example.fake/change-requests/1" in output
        assert fake.specs[0].title == "#small: 1 files (test.py)"
