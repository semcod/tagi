"""GitLab provider module."""

import subprocess

from .base import BaseProvider


class GitLabProvider(BaseProvider):
    """GitLab provider using glab CLI."""
    
    def is_authenticated(self) -> bool:
        """Check if glab CLI is authenticated."""
        cmd = ["glab", "auth", "status"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    
    def create_pr(self, title: str, body: str, branch: str) -> str:
        """Create a merge request using glab CLI."""
        cmd = ["glab", "mr", "create", "--title", title, "--description", body]
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
