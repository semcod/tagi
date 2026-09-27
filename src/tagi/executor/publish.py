"""Publish executor module for publishing changes."""

from dataclasses import dataclass
from typing import List, Optional

from tagi.composer.commit_message import generate_commit_message
from tagi.models import ChangeGroup
from tagi.providers.base import BaseProvider, PrSpec
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider

from .git import GitExecutor


@dataclass
class PrRequest:
    """Inputs that travel together when opening a PR/MR for a change group."""

    group: ChangeGroup
    template: str = "default"
    provider: Optional[BaseProvider] = None


class PublishExecutor:
    """Executor for publishing changes."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.git = GitExecutor(repo_path)
    
    def stage_and_commit(self, files: List[str], message: str, allow_empty: bool = False) -> bool:
        """Stage files and commit them."""
        if not self.git.add(files):
            return False
        return self.git.commit(message, allow_empty=allow_empty)
    
    def publish(self, files: List[str], message: str, push: bool = False, 
                remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> bool:
        """Stage, commit, and optionally push changes."""
        if not self.stage_and_commit(files, message):
            return False
        if push:
            return self.git.push(remote, branch, force)
        return True
    
    def dry_run(self, files: List[str], message: str) -> dict:
        """Preview what would be executed without actually running it."""
        return {
            "files": files,
            "message": message,
            "commands": [
                f"git add {' '.join(files)}",
                f"git commit -m '{message}'"
            ]
        }

    def create_github_pr(self, request: PrRequest) -> str:
        """Create a GitHub pull request for a change group."""
        return self._create_change_request(GitHubProvider, request)

    def create_gitlab_mr(self, request: PrRequest) -> str:
        """Create a GitLab merge request for a change group."""
        return self._create_change_request(GitLabProvider, request)

    def _create_change_request(self, provider_cls: type, request: PrRequest) -> str:
        """Build a PrSpec from the request and delegate to the provider."""
        message = generate_commit_message(
            request.group.changes,
            template=request.template,
            repo_path=self.repo_path,
        )
        title = message.splitlines()[0] if message else request.group.name
        spec = PrSpec(
            title=title,
            body=self._build_body(request.group, message),
            branch=self.git.get_current_branch(),
        )
        active = (
            request.provider
            if request.provider is not None
            else provider_cls(self.repo_path)
        )
        return active.create_pr(spec)

    @staticmethod
    def _build_body(group: ChangeGroup, message: str) -> str:
        """Render the PR/MR description from the commit message and file list."""
        lines = [message, "", "Changes:"]
        lines.extend(f"- {change.path}" for change in group.changes)
        return "\n".join(lines)
