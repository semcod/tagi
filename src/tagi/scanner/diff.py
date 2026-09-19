"""Diff module for getting git diffs."""

from tagi.utils.commands import run_command


def get_diff(file_path: str, repo_path: str = ".") -> str:
    """Get the diff for a specific file."""
    return run_command(["git", "diff", file_path], repo_path).stdout


def get_staged_diff(file_path: str, repo_path: str = ".") -> str:
    """Get the staged diff for a specific file."""
    return run_command(["git", "diff", "--cached", file_path], repo_path).stdout
