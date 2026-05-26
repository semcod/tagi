"""Publish executor module for publishing changes."""

from typing import List

from .git import GitExecutor


class PublishExecutor:
    """Executor for publishing changes."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.git = GitExecutor(repo_path)
    
    def stage_and_commit(self, files: List[str], message: str) -> bool:
        """Stage files and commit them."""
        if not self.git.add(files):
            return False
        return self.git.commit(message)
    
    def publish(self, files: List[str], message: str, push: bool = False) -> bool:
        """Stage, commit, and optionally push changes."""
        if not self.stage_and_commit(files, message):
            return False
        if push:
            return self.git.push()
        return True
