"""GitLab provider module."""

from typing import List, Optional

from .base import BaseProvider


class GitLabProvider(BaseProvider):
    """GitLab provider using glab CLI."""
    
    def is_authenticated(self) -> bool:
        """Check if glab CLI is authenticated."""
        result = self._run_command(["glab", "auth", "status"])
        return result.returncode == 0
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        result = self._run_command(["glab", "auth", "status"])
        return {
            "authenticated": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def get_configured_host(self) -> str:
        """Get the configured GitLab host."""
        result = self._run_command(["glab", "api", "/user"])
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
                  draft: bool = False, labels: Optional[List[str]] = None) -> str:
        """Create a merge request using glab CLI."""
        cmd = ["glab", "mr", "create", "--title", title, "--description", body, "--target-branch", base]
        if draft:
            cmd.append("--draft")
        if labels:
            cmd.extend(["--label", ",".join(labels)])
        result = self._run_command(cmd)
        if result.returncode == 0:
            return result.stdout
        return ""
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitLab."""
        return self._check_git_remote_for_provider("gitlab")
