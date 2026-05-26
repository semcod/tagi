"""Provider detection module."""

from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider


def detect_provider(repo_path: str = ".") -> str:
    """Detect the Git hosting provider from remotes."""
    github = GitHubProvider(repo_path)
    gitlab = GitLabProvider(repo_path)
    if github.detect_remote():
        return "github"
    if gitlab.detect_remote():
        return "gitlab"
    return ""
