"""Git executor module for running git commands."""

import subprocess
from subprocess import CompletedProcess
from typing import List, Optional


class GitExecutor:
    """Executor for git commands."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run_command(self, command: list[str]) -> CompletedProcess:
        """Run a command in the repository and return the result."""
        return subprocess.run(
            command,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False
        )

    def add(self, files: List[str]) -> bool:
        """Stage files for commit."""
        if not files:
            return False
        result = self._run_command(["git", "add", *files])
        if result.returncode != 0:
            raise RuntimeError(f"Failed to stage files: {result.stderr}")
        return True

    def commit(self, message: str, allow_empty: bool = False) -> bool:
        """Commit staged changes."""
        result = self._run_command(
            ["git", "commit", "-m", message] + (["--allow-empty"] if allow_empty else [])
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to commit: {result.stderr}")
        return True

    def push(self, remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> bool:
        """Push commits to remote."""
        result = self._run_command(
            (["git", "push", remote, branch] if branch else ["git", "push"])
            + (["--force"] if force else [])
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to push: {result.stderr}")
        return True

    def status(self) -> str:
        """Get git status."""
        return self._run_command(["git", "status"]).stdout

    def get_current_branch(self) -> str:
        """Get the current branch name."""
        result = self._run_command(["git", "branch", "--show-current"])
        if result.returncode == 0:
            return result.stdout.strip()
        return "main"

    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get the remote URL."""
        result = self._run_command(["git", "remote", "get-url", remote])
        if result.returncode == 0:
            return result.stdout.strip()
        return None

    def has_staged_changes(self) -> bool:
        """Check if there are staged changes."""
        return bool(self._run_command(["git", "diff", "--cached", "--name-only"]).stdout.strip())
