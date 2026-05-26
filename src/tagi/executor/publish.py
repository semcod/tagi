"""Publish executor module for publishing changes."""

from typing import List, Optional

from .git import GitExecutor


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
