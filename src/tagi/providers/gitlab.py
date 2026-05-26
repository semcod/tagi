"""GitLab provider module."""

import subprocess
from typing import List

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
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        cmd = ["glab", "auth", "status"]
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
    
    def get_configured_host(self) -> str:
        """Get the configured GitLab host."""
        cmd = ["glab", "api", "/user"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            # Parse host from API response
            import json
            try:
                data = json.loads(result.stdout)
                if "web_url" in data:
                    from urllib.parse import urlparse
                    return urlparse(data["web_url"]).netloc
            except (json.JSONDecodeError, KeyError):
                pass
        return "gitlab.com"
    
    def create_pr(self, title: str, body: str, branch: str, base: str = "main",
                  draft: bool = False, labels: List[str] = None) -> str:
        """Create a merge request using glab CLI."""
        cmd = ["glab", "mr", "create", "--title", title, "--description", body, "--target-branch", base]
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
        """Detect if the current repository is hosted on GitLab."""
        cmd = ["git", "remote", "get-url", "origin"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return "gitlab" in result.stdout.lower()
        return False
