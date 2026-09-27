"""CLI tests for ``tagi.cli.publishing_commands`` (PLF-211).

Covers the ``publish`` and ``deploy`` command paths end-to-end through the
Typer app, including tag normalization, unknown/empty tag handling, dry
runs, provider detection branches (github/gitlab/none/unsupported),
executor failures, and missing-argument usage errors.

The scan pipeline is faked through the ``tagi.cli`` namespace (the same
pattern as ``tests/test_cli_tag_stats_regression.py``) so the command
logic is exercised without a real repository.
"""

from typing import ClassVar

import pytest
from typer.testing import CliRunner

from tagi.cli import app
from tagi.models import Change, ChangeType, Tag

runner = CliRunner()


def _sample_changes():
    return [
        Change(
            path="a.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL],
            lines_changed=10,
            risk_score=1.0,
        ),
        Change(
            path="b.py",
            change_type=ChangeType.MODIFIED,
            tags=[Tag.SMALL],
            lines_changed=20,
            risk_score=2.0,
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


class FakeProvider:
    def __init__(self, name):
        self.name = name


def _install_provider(monkeypatch, name):
    provider = FakeProvider(name)
    monkeypatch.setattr(
        "tagi.cli.publishing_commands.get_provider", lambda _repo: provider
    )
    return provider


class RecordingPublishExecutor:
    """Fake PublishExecutor capturing calls and returning canned results."""

    calls: ClassVar[list] = []
    github_result: ClassVar[str] = "https://github.com/example/pr/1"
    gitlab_result: ClassVar[str] = "https://gitlab.com/example/mr/1"
    raise_on_call: ClassVar[bool] = False

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def create_github_pr(self, request):
        RecordingPublishExecutor.calls.append(("github", request))
        if RecordingPublishExecutor.raise_on_call:
            raise RuntimeError("boom")
        return RecordingPublishExecutor.github_result

    def create_gitlab_mr(self, request):
        RecordingPublishExecutor.calls.append(("gitlab", request))
        if RecordingPublishExecutor.raise_on_call:
            raise RuntimeError("boom")
        return RecordingPublishExecutor.gitlab_result


@pytest.fixture(autouse=True)
def _reset_recording_executor():
    RecordingPublishExecutor.calls = []
    RecordingPublishExecutor.github_result = "https://github.com/example/pr/1"
    RecordingPublishExecutor.gitlab_result = "https://gitlab.com/example/mr/1"
    RecordingPublishExecutor.raise_on_call = False
    yield


def _install_executor(monkeypatch):
    monkeypatch.setattr(
        "tagi.cli.publishing_commands.PublishExecutor", RecordingPublishExecutor
    )


# ---------------------------------------------------------------------------
# publish: usage errors and tag resolution
# ---------------------------------------------------------------------------


def test_publish_missing_tag_argument_is_usage_error():
    """``tagi publish`` without a tag fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["publish"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_publish_unknown_tag_exits_nonzero(monkeypatch):
    """An unrecognized tag reports an error and exits with code 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["publish", "#nope", "."])
    assert result.exit_code == 1
    assert "Unknown tag: #nope" in result.output


def test_publish_no_changes_for_tag(monkeypatch):
    """A known tag with no matching changes exits cleanly with a notice."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 0
    assert "No changes found for #small" in result.output


def test_publish_normalizes_tag_without_hash_prefix(monkeypatch):
    """``tagi publish small`` behaves like ``#small``."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["publish", "small", "."])
    assert result.exit_code == 0
    assert "No changes found for #small" in result.output


# ---------------------------------------------------------------------------
# publish: provider detection and dry run
# ---------------------------------------------------------------------------


def test_publish_without_provider_returns_zero(monkeypatch):
    """No detectable provider prints guidance and exits successfully."""
    _install_fake_scan(monkeypatch, _sample_changes())
    monkeypatch.setattr("tagi.cli.publishing_commands.get_provider", lambda _repo: None)
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 0
    assert "Could not detect GitHub or GitLab provider" in result.output
    assert "remote configured" in result.output


def test_publish_dry_run_previews_without_executor(monkeypatch):
    """Dry run lists the tagged changes and never touches the executor."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    _install_executor(monkeypatch)
    result = runner.invoke(app, ["publish", "#small", ".", "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run - would create PR/MR with:" in result.output
    assert "Tag: #small" in result.output
    assert "Changes: 2" in result.output
    assert "a.py" in result.output
    assert "b.py" in result.output
    assert RecordingPublishExecutor.calls == []


def test_publish_dry_run_normalizes_tag(monkeypatch):
    """Dry run reports the normalized ``#``-prefixed tag."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    result = runner.invoke(app, ["publish", "small", ".", "--dry-run"])
    assert result.exit_code == 0
    assert "Tag: #small" in result.output


# ---------------------------------------------------------------------------
# publish: executor branches
# ---------------------------------------------------------------------------


def test_publish_github_pr_created(monkeypatch):
    """A detected GitHub provider creates a PR and prints its URL."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    _install_executor(monkeypatch)
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 0
    assert "Pull request created: https://github.com/example/pr/1" in result.output
    assert len(RecordingPublishExecutor.calls) == 1
    kind, request = RecordingPublishExecutor.calls[0]
    assert kind == "github"
    assert request.template == "default"
    assert request.group.name == "#small"
    assert len(request.group.changes) == 2


def test_publish_github_pr_failure_exits(monkeypatch):
    """A falsy PR result reports failure and exits with code 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    _install_executor(monkeypatch)
    RecordingPublishExecutor.github_result = None
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 1
    assert "Failed to create pull request" in result.output


def test_publish_gitlab_mr_created(monkeypatch):
    """A detected GitLab provider creates an MR and prints its URL."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "gitlab")
    _install_executor(monkeypatch)
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 0
    assert "Merge request created: https://gitlab.com/example/mr/1" in result.output
    kind, _request = RecordingPublishExecutor.calls[0]
    assert kind == "gitlab"


def test_publish_gitlab_mr_failure_exits(monkeypatch):
    """A falsy MR result reports failure and exits with code 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "gitlab")
    _install_executor(monkeypatch)
    RecordingPublishExecutor.gitlab_result = None
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 1
    assert "Failed to create merge request" in result.output


def test_publish_unsupported_provider_exits(monkeypatch):
    """Any provider other than github/gitlab is rejected with exit 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "gitea")
    _install_executor(monkeypatch)
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 1
    assert "Unsupported provider: gitea" in result.output


def test_publish_executor_exception_exits(monkeypatch):
    """An executor crash is reported as a publish error with exit 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    _install_executor(monkeypatch)
    RecordingPublishExecutor.raise_on_call = True
    result = runner.invoke(app, ["publish", "#small", "."])
    assert result.exit_code == 1
    assert "Error during publish: boom" in result.output


def test_publish_forwards_template_option(monkeypatch):
    """``--template`` is forwarded to the publish executor."""
    _install_fake_scan(monkeypatch, _sample_changes())
    _install_provider(monkeypatch, "github")
    _install_executor(monkeypatch)
    result = runner.invoke(
        app, ["publish", "#small", ".", "--template", "conventional"]
    )
    assert result.exit_code == 0
    _kind, request = RecordingPublishExecutor.calls[0]
    assert request.template == "conventional"


# ---------------------------------------------------------------------------
# deploy
# ---------------------------------------------------------------------------


def test_deploy_missing_tag_argument_is_usage_error():
    """``tagi deploy`` without a tag fails with a usage error (exit 2)."""
    result = runner.invoke(app, ["deploy"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_deploy_unknown_tag_exits_nonzero(monkeypatch):
    """An unrecognized tag reports an error and exits with code 1."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["deploy", "#nope", "."])
    assert result.exit_code == 1
    assert "Unknown tag: #nope" in result.output


def test_deploy_no_changes_for_tag(monkeypatch):
    """A known tag with no matching changes exits cleanly with a notice."""
    _install_fake_scan(monkeypatch, [])
    result = runner.invoke(app, ["deploy", "#small", "."])
    assert result.exit_code == 0
    assert "No changes found for #small" in result.output


def test_deploy_dry_run_previews_changes(monkeypatch):
    """Dry run lists the changes that would be deployed."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["deploy", "#small", ".", "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run - would deploy:" in result.output
    assert "Tag: #small" in result.output
    assert "Environment: staging" in result.output
    assert "Changes: 2" in result.output
    assert "a.py" in result.output


def test_deploy_dry_run_honors_env_option(monkeypatch):
    """``--env production`` is reflected in the dry-run preview."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(
        app, ["deploy", "#small", ".", "--env", "production", "--dry-run"]
    )
    assert result.exit_code == 0
    assert "Environment: production" in result.output


def test_deploy_dry_run_normalizes_tag(monkeypatch):
    """Dry run reports the normalized ``#``-prefixed tag."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["deploy", "small", ".", "--dry-run"])
    assert result.exit_code == 0
    assert "Tag: #small" in result.output


def test_deploy_without_dry_run_is_placeholder(monkeypatch):
    """A real deploy currently reports the not-yet-implemented placeholder."""
    _install_fake_scan(monkeypatch, _sample_changes())
    result = runner.invoke(app, ["deploy", "#small", "."])
    assert result.exit_code == 0
    assert "Deploy functionality is not yet implemented" in result.output
    assert "Would deploy 2 changes to staging" in result.output
