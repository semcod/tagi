"""GitLab provider module."""

from typing import List, Optional

from tagi.providers.utils.pr import build_pr_command, execute_pr_command
from tagi.providers.utils.auth import get_auth_status_from_result, is_authenticated_from_result

from .base import BaseProvider, PrSpec


class GitLabProvider(BaseProvider):
    """GitLab provider using glab CLI."""

    name = "gitlab"

    def is_authenticated(self) -> bool:
        """Check if glab CLI is authenticated."""
        result = self._run_command(["glab", "auth", "status"])
        return is_authenticated_from_result(result)
    
    def get_auth_status(self) -> dict:
        """Get detailed authentication status."""
        result = self._run_command(["glab", "auth", "status"])
        return get_auth_status_from_result(result)
    
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
    
    def create_pr(self, spec: PrSpec) -> str:
        """Create a merge request using glab CLI."""
        return execute_pr_command(self._run_command(build_pr_command("glab", "mr", spec)))
    
    def detect_remote(self) -> bool:
        """Detect if the current repository is hosted on GitLab."""
        return self._check_git_remote_for_provider("gitlab")
