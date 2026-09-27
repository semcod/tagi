"""Branch-based change grouping module."""

from typing import Dict, List
from tagi.models.change import Change


def _branches_for_change(change: Change, repo_path: str) -> List[str]:
    """Return cleaned branch names containing the change path, or an empty list."""
    from tagi.utils.commands import run_command

    contains = run_command(
        ["git", "branch", "--contains", "HEAD", "--", change.path],
        repo_path,
    )

    if contains.returncode != 0:
        return []

    # Clean up branch names (remove * prefix)
    return [b.strip().replace('*', '').strip() for b in contains.stdout.strip().split('\n') if b.strip()]


def _resolve_branch(change: Change, repo_path: str, default_branch: str) -> str:
    """Pick the branch a change is attributed to, falling back to default_branch."""
    try:
        branches = _branches_for_change(change, repo_path)
    except Exception:
        return default_branch

    # Use the first branch found (typically the current branch)
    return branches[0] if branches else default_branch


def group_by_branch(changes: List[Change], repo_path: str = ".") -> Dict[str, List[Change]]:
    """Group changes by the git branch they were modified on.

    Args:
        changes: List of changes to group
        repo_path: Path to the git repository

    Returns:
        Dictionary mapping branch names to lists of changes
    """
    from tagi.executor.git import GitExecutor

    executor = GitExecutor(repo_path)
    current_branch = executor.get_current_branch()

    branch_groups: Dict[str, List[Change]] = {}

    for change in changes:
        branch = _resolve_branch(change, repo_path, current_branch)
        branch_groups.setdefault(branch, []).append(change)

    return branch_groups


def get_branch_info(repo_path: str = ".") -> Dict[str, str]:
    """Get information about all branches in the repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        Dictionary mapping branch names to their latest commit hashes
    """
    from tagi.utils.commands import run_command

    try:
        branch_listing = run_command(["git", "branch", "-a"], repo_path)

        if branch_listing.returncode != 0:
            return {}

        branches = {}
        for line in branch_listing.stdout.strip().split('\n'):
            branch = line.strip().replace('*', '').strip()
            if branch:
                branches[branch] = branch  # Could be extended to include commit hash
        
        return branches
    except Exception:
        return {}
