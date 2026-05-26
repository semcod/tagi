"""GitHub provider module."""

import subprocess
from typing import List

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
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        cmd = ["gh", "auth", "status"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "authenticated": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def get_token(self) -> str:
        """Get the GitHub authentication token."""
        cmd = ["gh", "auth", "token"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    
    def create_pr(self, title: str, body: str, branch: str, base: str = "main", 
                  draft: bool = False, labels: List[str] = None) -> str:
        """Create a pull request using gh CLI."""
        cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]
        if draft:
            cmd.append("--draft")
        if labels:
            cmd.extend(["--label", ",".join(labels)])
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
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitHub."""
        cmd = ["git", "remote", "get-url", "origin"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return "github.com" in result.stdout.lower()
        return False
