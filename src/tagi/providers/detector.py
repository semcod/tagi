"""Provider detection module.

Owns provider selection from git remotes. Lives in ``tagi.providers`` so
that ``tagi.utils`` never imports back from ``tagi.providers`` (PLF-198);
the dependency stays one-way: ``tagi.providers -> tagi.utils``.
"""

from typing import Optional

from tagi.providers.base import BaseProvider
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider
from tagi.utils.commands import run_command


def get_provider(repo_path: str = ".") -> Optional[BaseProvider]:
    """Return the provider instance matching the detected remote.

    Args:
        repo_path: Path to the repository

    Returns:
        GitHubProvider, GitLabProvider, or None if unknown
    """
    detected = detect_git_provider(repo_path)
    if detected == "github":
        return GitHubProvider(repo_path)
    if detected == "gitlab":
        return GitLabProvider(repo_path)
    return None


def detect_git_provider(repo_path: str = ".") -> Optional[str]:
    """Detect which Git provider is used for the repository.

    Args:
        repo_path: Path to the repository

    Returns:
        'github', 'gitlab', or None if unknown
    """
    try:
        remotes = run_command(["git", "remote", "-v"], repo_path)

        if remotes.returncode != 0:
            return None

        output = remotes.stdout.lower()

        if "github.com" in output:
            return "github"
        elif "gitlab.com" in output:
            return "gitlab"
        return None
    except FileNotFoundError:
        return None


def detect_provider(repo_path: str = ".") -> str:
    """Detect the Git hosting provider from remotes."""
    github = GitHubProvider(repo_path)
    gitlab = GitLabProvider(repo_path)
    if github.detect_remote():
        return "github"
    if gitlab.detect_remote():
        return "gitlab"
    return ""
