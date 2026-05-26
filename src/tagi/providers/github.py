"""GitHub provider module."""

from typing import List, Optional
from tagi.providers.utils.pr import build_pr_command, execute_pr_command
from tagi.providers.utils.auth import get_auth_status_from_result, is_authenticated_from_result

from .base import BaseProvider


class GitHubProvider(BaseProvider):
    """GitHub provider using gh CLI."""
    
    def is_authenticated(self) -> bool:
        """Check if gh CLI is authenticated."""
        result = self._run_command(["gh", "auth", "status"])
        return is_authenticated_from_result(result)
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        result = self._run_command(["gh", "auth", "status"])
        return get_auth_status_from_result(result)
    
    def get_token(self) -> str:
        """Get the GitHub authentication token."""
        result = self._run_command(["gh", "auth", "token"])
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    
    def create_pr(self, title: str, body: str, branch: str, base: str = "main",
                  draft: bool = False, labels: Optional[List[str]] = None) -> str:
        """Create a pull request using gh CLI."""
        cmd = build_pr_command("gh", "pr", title, body, branch, base, draft, labels)
        result = self._run_command(cmd)
        return execute_pr_command(result)
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitHub."""
        return self._check_git_remote_for_provider("github.com")
