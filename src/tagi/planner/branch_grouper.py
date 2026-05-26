"""Branch-based change grouping module."""

from typing import Dict, List
from tagi.models.change import Change


def group_by_branch(changes: List[Change], repo_path: str = ".") -> Dict[str, List[Change]]:
    """Group changes by the git branch they were modified on.
    
    Args:
        changes: List of changes to group
        repo_path: Path to the git repository
        
    Returns:
        Dictionary mapping branch names to lists of changes
    """
    from tagi.executor.git import GitExecutor
    import subprocess
    
    executor = GitExecutor(repo_path)
    current_branch = executor.get_current_branch()
    
    # Get branch history for each file
    branch_groups: Dict[str, List[Change]] = {}
    
    for change in changes:
        try:
            # Get the branch where the file was last modified
            result = subprocess.run(
                ["git", "branch", "--contains", "HEAD", "--", change.path],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                branches = result.stdout.strip().split('\n')
                # Clean up branch names (remove * prefix)
                branches = [b.strip().replace('*', '').strip() for b in branches if b.strip()]
                
                if branches:
                    # Use the first branch found (typically the current branch)
                    branch = branches[0]
                else:
                    branch = current_branch
            else:
                branch = current_branch
        except Exception:
            branch = current_branch
        
        if branch not in branch_groups:
            branch_groups[branch] = []
        branch_groups[branch].append(change)
    
    return branch_groups


def get_branch_info(repo_path: str = ".") -> Dict[str, str]:
    """Get information about all branches in the repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        Dictionary mapping branch names to their latest commit hashes
    """
    import subprocess
    
    try:
        result = subprocess.run(
            ["git", "branch", "-a"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {}
        
        branches = {}
        for line in result.stdout.strip().split('\n'):
            branch = line.strip().replace('*', '').strip()
            if branch:
                branches[branch] = branch  # Could be extended to include commit hash
        
        return branches
    except Exception:
        return {}
