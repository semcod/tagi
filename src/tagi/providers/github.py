"""GitHub provider module."""

from typing import List, Optional

from .base import BaseProvider


class GitHubProvider(BaseProvider):
    """GitHub provider using gh CLI."""
    
    def is_authenticated(self) -> bool:
        """Check if gh CLI is authenticated."""
        result = self._run_command(["gh", "auth", "status"])
        return result.returncode == 0
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        result = self._run_command(["gh", "auth", "status"])
        return {
            "authenticated": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def get_token(self) -> str:
        """Get the GitHub authentication token."""
        result = self._run_command(["gh", "auth", "token"])
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    
    def create_pr(self, title: str, body: str, branch: str, base: str = "main",
                  draft: bool = False, labels: Optional[List[str]] = None) -> str:
        """Create a pull request using gh CLI."""
        cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]
        if draft:
            cmd.append("--draft")
        if labels:
            cmd.extend(["--label", ",".join(labels)])
        result = self._run_command(cmd)
        if result.returncode == 0:
            return result.stdout
        return ""
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitHub."""
        return self._check_git_remote_for_provider("github.com")
