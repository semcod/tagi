"""Executor module for running git commands."""

import subprocess
from typing import List

from tagi.models import Change


def stage_changes(changes: List[Change], repo_path: str = ".", dry_run: bool = False) -> bool:
    """Stage changes using git add."""
    file_paths = [c.path for c in changes]
    
    if dry_run:
        print(f"[DRY-RUN] Would stage: {', '.join(file_paths[:5])}")
        if len(file_paths) > 5:
            print(f"[DRY-RUN] ... and {len(file_paths) - 5} more files")
        return True
    
    cmd = ["git", "add"] + file_paths
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"Error staging files: {result.stderr}")
        return False
    
    return True


def commit_changes(message: str, repo_path: str = ".", dry_run: bool = False) -> bool:
    """Commit staged changes."""
    if dry_run:
        print(f"[DRY-RUN] Would commit with message:")
        print(f"[DRY-RUN] {message}")
        return True
    
    cmd = ["git", "commit", "-m", message]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"Error committing: {result.stderr}")
        return False
    
    return True


def push_changes(repo_path: str = ".", dry_run: bool = False) -> bool:
    """Push changes to remote."""
    if dry_run:
        print("[DRY-RUN] Would push to remote")
        return True
    
    cmd = ["git", "push"]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"Error pushing: {result.stderr}")
        return False
    
    return True
