"""Behavior of provider command dispatch, request contents and error reporting."""

from io import StringIO
from unittest.mock import Mock

import pytest
from rich.console import Console

from tagi.cli import provider_commands as commands
from tagi.providers.base import PrSpec
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider


@pytest.fixture(params=[
    (commands.create_pr, GitHubProvider, GitLabProvider, "GitHub", "pull request", "PR"),
    (commands.create_mr, GitLabProvider, GitHubProvider, "GitLab", "merge request", "MR"),
], ids=["github", "gitlab"])
def request_case(request, monkeypatch):
    command, provider_type, other_type, host, name, abbreviation = request.param
    output = StringIO()
    monkeypatch.setattr(commands, "console", Console(file=output, width=120))
    provider = provider_type("checkout")
    create = Mock(return_value="https://example.test/request/42")
    monkeypatch.setattr(provider, "create_pr", create)
    detect = Mock(return_value=provider)
    branch = Mock(return_value="feature/topic")
    monkeypatch.setattr(commands, "get_provider", detect)
    monkeypatch.setattr(commands, "_current_branch", branch)
    spec = PrSpec("Title", "Body", "original", base="release", draft=True, labels=["fix"])
    return command, other_type, host, name, abbreviation, output, create, detect, branch, spec


def test_creation_preserves_content_and_resolves_branch_without_mutating_input(request_case):
    command, _, _, name, _, output, create, detect, branch, spec = request_case

    assert command(spec, "checkout") is True

    detect.assert_called_once_with("checkout")
    branch.assert_called_once_with("checkout")
    sent = create.call_args.args[0]
    create.assert_called_once()
    assert sent == PrSpec("Title", "Body", "feature/topic", base="release", draft=True, labels=["fix"])
    assert sent is not spec
    assert spec.branch == "original"
    assert output.getvalue() == f"✓ {name.capitalize()} created: https://example.test/request/42\n"


@pytest.mark.parametrize("result", ["", None])
def test_empty_creation_result_is_reported_as_failure(request_case, result):
    command, _, _, name, _, output, create, _, _, spec = request_case
    create.return_value = result

    assert command(spec) is False
    assert output.getvalue() == f"Failed to create {name}\n"


@pytest.mark.parametrize("detected", ["none", "other"])
def test_wrong_provider_stops_before_branch_lookup_or_request(request_case, detected):
    command, other, host, _, _, output, create, detect, branch, spec = request_case
    detect.return_value = None if detected == "none" else other("checkout")

    assert command(spec) is False

    branch.assert_not_called()
    create.assert_not_called()
    assert output.getvalue() == f"Repository is not hosted on {host}\n"


@pytest.mark.parametrize("failure_at", ["branch", "creation"])
def test_branch_and_creation_errors_keep_provider_specific_message(request_case, failure_at):
    command, _, _, _, abbreviation, output, create, _, branch, spec = request_case
    failing_call = branch if failure_at == "branch" else create
    failing_call.side_effect = RuntimeError("request failed")

    assert command(spec) is False
    assert spec.branch == "original"
    assert output.getvalue() == f"Error creating {abbreviation}: request failed\n"
    if failure_at == "branch":
        create.assert_not_called()


def test_provider_detection_errors_propagate_before_creation(request_case):
    command, _, _, _, _, output, create, detect, branch, spec = request_case
    detect.side_effect = RuntimeError("detection failed")

    with pytest.raises(RuntimeError, match="detection failed"):
        command(spec)

    branch.assert_not_called()
    create.assert_not_called()
    assert output.getvalue() == ""
