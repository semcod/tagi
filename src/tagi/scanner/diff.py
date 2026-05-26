"""Diff module for getting git diffs."""

import subprocess


def get_diff(file_path: str, repo_path: str = ".") -> str:
    """Get the diff for a specific file."""
    cmd = ["git", "diff", file_path]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )
    
    return result.stdout


def get_staged_diff(file_path: str, repo_path: str = ".") -> str:
    """Get the staged diff for a specific file."""
    cmd = ["git", "diff", "--cached", file_path]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )
    
    return result.stdout
