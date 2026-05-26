"""Git executor module for running git commands."""

import subprocess
from typing import List


class GitExecutor:
    """Executor for git commands."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def add(self, files: List[str]) -> bool:
        """Stage files for commit."""
        cmd = ["git", "add"] + files
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    
    def commit(self, message: str) -> bool:
        """Commit staged changes."""
        cmd = ["git", "commit", "-m", message]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    
    def push(self, remote: str = "origin", branch: str = None) -> bool:
        """Push commits to remote."""
        if branch:
            cmd = ["git", "push", remote, branch]
        else:
            cmd = ["git", "push"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    
    def status(self) -> str:
        """Get git status."""
        cmd = ["git", "status"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout
