"""GitHub provider module."""

from typing import List, Optional
from tagi.providers.utils.pr import build_pr_command, execute_pr_command
from tagi.providers.utils.auth import get_auth_status_from_result, is_authenticated_from_result

from .base import BaseProvider, PrSpec


class GitHubProvider(BaseProvider):
    """GitHub provider using gh CLI."""

    name = "github"

    def is_authenticated(self) -> bool:
        """Check if gh CLI is authenticated."""
        return is_authenticated_from_result(self._run_command(["gh", "auth", "status"]))

    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        return get_auth_status_from_result(self._run_command(["gh", "auth", "status"]))

    def get_token(self) -> str:
        """Get the GitHub authentication token."""
        token = self._run_command(["gh", "auth", "token"])
        if token.returncode == 0:
            return token.stdout.strip()
        return ""
    
    def create_pr(self, spec: PrSpec) -> str:
        """Create a pull request using gh CLI."""
        return execute_pr_command(self._run_command(build_pr_command("gh", "pr", spec)))
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitHub."""
        return self._check_git_remote_for_provider("github.com")
