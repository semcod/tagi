"""Provider detection and PR/MR creation utilities."""

from dataclasses import replace
from typing import Optional

from rich.console import Console

from tagi.utils.detect_provider import get_provider
from tagi.providers.base import PrSpec
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


def create_pr(spec: PrSpec, repo_path: str = ".") -> bool:
    """Create a GitHub pull request."""
    github_provider = get_provider(repo_path)
    if not isinstance(github_provider, GitHubProvider):
        console.print("[red]Repository is not hosted on GitHub[/red]")
        return False

    try:
        pr_url = github_provider.create_pr(_pr_spec(spec, repo_path))
        if pr_url:
            console.print(f"[green]✓ Pull request created:[/green] {pr_url}")
            return True
        else:
            console.print("[red]Failed to create pull request[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error creating PR: {e}[/red]")
        return False


def create_mr(spec: PrSpec, repo_path: str = ".") -> bool:
    """Create a GitLab merge request."""
    gitlab_provider = get_provider(repo_path)
    if not isinstance(gitlab_provider, GitLabProvider):
        console.print("[red]Repository is not hosted on GitLab[/red]")
        return False

    try:
        mr_url = gitlab_provider.create_pr(_pr_spec(spec, repo_path))
        if mr_url:
            console.print(f"[green]✓ Merge request created:[/green] {mr_url}")
            return True
        else:
            console.print("[red]Failed to create merge request[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error creating MR: {e}[/red]")
        return False
