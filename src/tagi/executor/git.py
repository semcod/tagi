"""Git executor module for running git commands."""

import subprocess
from typing import List, Optional


class GitExecutor:
    """Executor for git commands."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def add(self, files: List[str]) -> bool:
        """Stage files for commit."""
        if not files:
            return False
        cmd = ["git", "add"] + files
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to stage files: {result.stderr}")
        return True
    
    def commit(self, message: str, allow_empty: bool = False) -> bool:
        """Commit staged changes."""
        cmd = ["git", "commit", "-m", message]
        if allow_empty:
            cmd.append("--allow-empty")
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to commit: {result.stderr}")
        return True
    
    def push(self, remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> bool:
        """Push commits to remote."""
        if branch:
            cmd = ["git", "push", remote, branch]
        else:
            cmd = ["git", "push"]
        if force:
            cmd.append("--force")
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to push: {result.stderr}")
        return True
    
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
    
    def get_current_branch(self) -> str:
        """Get the current branch name."""
        cmd = ["git", "branch", "--show-current"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "main"
    
    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get the remote URL."""
        cmd = ["git", "remote", "get-url", remote]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    
    def has_staged_changes(self) -> bool:
        """Check if there are staged changes."""
        cmd = ["git", "diff", "--cached", "--name-only"]
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        return bool(result.stdout.strip())
