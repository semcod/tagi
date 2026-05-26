"""Base provider module."""

import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional


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
    def create_pr(self, title: str, body: str, branch: str, base: str = "main",
                  draft: bool = False, labels: Optional[List[str]] = None) -> str:
        """Create a pull/merge request."""
        pass
    
    @abstractmethod
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on this provider."""
        pass
    
    def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        return subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
    
    def _get_git_remote_url(self) -> Optional[str]:
        """Get the git remote URL for the repository."""
        result = self._run_command(["git", "remote", "get-url", "origin"])
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    
    def _check_git_remote_for_provider(self, provider_name: str) -> bool:
        """Check if the git remote URL contains the provider name."""
        url = self._get_git_remote_url()
        if url:
            return provider_name.lower() in url.lower()
        return False
