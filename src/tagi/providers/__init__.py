"""Providers module for Git hosting integrations."""

from .base import BaseProvider
from .detector import detect_git_provider, detect_provider, get_provider
from .github import GitHubProvider
from .gitlab import GitLabProvider

__all__ = [
    "BaseProvider",
    "GitHubProvider",
    "GitLabProvider",
    "detect_provider",
    "detect_git_provider",
    "get_provider",
]
