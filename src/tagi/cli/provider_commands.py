"""Provider detection and PR/MR creation utilities."""

from rich.console import Console

from tagi.utils.detect_provider import detect_git_provider
from tagi.providers.base import PrSpec
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider


console = Console()


def detect_provider_command(repo_path: str = ".") -> str:
    """Detect Git provider (GitHub/GitLab) for the repository."""
    provider = detect_git_provider(repo_path)
    if provider:
        console.print(f"[green]Detected provider:[/green] {provider}")
    else:
        console.print("[yellow]Could not detect provider (no GitHub or GitLab remote found)[/yellow]")
    return provider


def _current_branch(repo_path: str) -> str:
    """Resolve the current git branch for the repository."""
    import subprocess
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path, capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() or "main"


def _pr_spec(title: str, body: str, repo_path: str) -> PrSpec:
    return PrSpec(title=title, body=body, branch=_current_branch(repo_path))


def create_pr(title: str, body: str, repo_path: str = ".") -> bool:
    """Create a GitHub pull request."""
    provider = detect_git_provider(repo_path)
    if provider != "github":
        console.print("[red]Repository is not hosted on GitHub[/red]")
        return False
    
    try:
        github_provider = GitHubProvider(repo_path)
        pr_url = github_provider.create_pr(_pr_spec(title, body, repo_path))
        if pr_url:
            console.print(f"[green]✓ Pull request created:[/green] {pr_url}")
            return True
        else:
            console.print("[red]Failed to create pull request[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error creating PR: {e}[/red]")
        return False


def create_mr(title: str, body: str, repo_path: str = ".") -> bool:
    """Create a GitLab merge request."""
    provider = detect_git_provider(repo_path)
    if provider != "gitlab":
        console.print("[red]Repository is not hosted on GitLab[/red]")
        return False
    
    try:
        gitlab_provider = GitLabProvider(repo_path)
        mr_url = gitlab_provider.create_pr(_pr_spec(title, body, repo_path))
        if mr_url:
            console.print(f"[green]✓ Merge request created:[/green] {mr_url}")
            return True
        else:
            console.print("[red]Failed to create merge request[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error creating MR: {e}[/red]")
        return False
