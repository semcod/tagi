"""Provider detection and PR/MR creation utilities."""

from dataclasses import replace
from typing import Optional

from rich.console import Console

from tagi.providers.detector import get_provider
from tagi.providers.base import BaseProvider, PrSpec
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider


console = Console()


def detect_provider_command(repo_path: str = ".") -> Optional[str]:
    """Detect Git provider (GitHub/GitLab) for the repository."""
    provider = get_provider(repo_path)
    if provider is None:
        console.print("[yellow]Could not detect provider (no GitHub or GitLab remote found)[/yellow]")
        return None
    console.print(f"[green]Detected provider:[/green] {provider.name}")
    return provider.name


def _current_branch(repo_path: str) -> str:
    """Resolve the current git branch for the repository."""
    from tagi.utils.commands import run_command
    return run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        repo_path,
    ).stdout.strip() or "main"


def _pr_spec(spec: PrSpec, repo_path: str) -> PrSpec:
    """Fill in the current branch of a PR/MR specification."""
    return replace(spec, branch=_current_branch(repo_path))


def _create_request(provider_type: type[BaseProvider], spec: PrSpec, repo_path: str) -> bool:
    """Run the shared PR/MR creation flow with provider-specific messages."""
    provider = get_provider(repo_path)
    host, request_name, abbreviation = {
        GitHubProvider: ("GitHub", "pull request", "PR"),
        GitLabProvider: ("GitLab", "merge request", "MR"),
    }[provider_type]
    if not isinstance(provider, provider_type):
        console.print(f"[red]Repository is not hosted on {host}[/red]")
        return False

    try:
        url = provider.create_pr(_pr_spec(spec, repo_path))
        if url:
            console.print(f"[green]✓ {request_name.capitalize()} created:[/green] {url}")
            return True
        console.print(f"[red]Failed to create {request_name}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error creating {abbreviation}: {e}[/red]")
        return False


def create_pr(spec: PrSpec, repo_path: str = ".") -> bool:
    """Create a GitHub pull request."""
    return _create_request(GitHubProvider, spec, repo_path)


def create_mr(spec: PrSpec, repo_path: str = ".") -> bool:
    """Create a GitLab merge request."""
    return _create_request(GitLabProvider, spec, repo_path)
