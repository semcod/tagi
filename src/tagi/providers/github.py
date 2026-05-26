"""GitHub provider module."""

import subprocess

from .base import BaseProvider


class GitHubProvider(BaseProvider):
    """GitHub provider using gh CLI."""
    
    def is_authenticated(self) -> bool:
        """Check if gh CLI is authenticated."""
        cmd = ["gh", "auth", "status"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    
    def create_pr(self, title: str, body: str, branch: str) -> str:
        """Create a pull request using gh CLI."""
        cmd = ["gh", "pr", "create", "--title", title, "--body", body]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout
        return ""
