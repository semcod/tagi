"""Base provider module."""

import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from tagi.utils.commands import run_command


@dataclass
class PrSpec:
    """Pull/merge request parameters."""

    title: str
    body: str
    branch: str
    base: str = "main"
    draft: bool = False
    labels: Optional[List[str]] = field(default=None)


class BaseProvider(ABC):
    """Base class for Git hosting providers."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize provider with repository path."""
        self.repo_path = repo_path
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if the provider CLI is authenticated."""
        pass
    
    @abstractmethod
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        pass
    
    @abstractmethod
    def create_pr(self, spec: "PrSpec") -> str:
        """Create a pull/merge request."""
        pass
    
    @abstractmethod
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on this provider."""
        pass
    
    def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        return run_command(cmd, self.repo_path)

    def _get_git_remote_url(self) -> Optional[str]:
        """Get the git remote URL for the repository."""
        remote = self._run_command(["git", "remote", "get-url", "origin"])
        if remote.returncode == 0:
            return remote.stdout.strip()
        return None
    
    def _check_git_remote_for_provider(self, provider_name: str) -> bool:
        """Check if the git remote URL contains the provider name."""
        url = self._get_git_remote_url()
        if url:
            return provider_name.lower() in url.lower()
        return False
