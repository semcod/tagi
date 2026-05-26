"""Status module for parsing git status."""

import os
import subprocess
from typing import List

from tagi.models import Change, ChangeType
from tagi.config import Config


def scan_repo(repo_path: str = ".") -> List[Change]:
    """Scan repository for uncommitted changes using git status --porcelain."""
    if not os.path.exists(os.path.join(repo_path, ".git")):
        raise ValueError(f"Not a git repository: {repo_path}")
    
    config = Config(repo_path)
    
    cmd = ["git", "status", "--porcelain"]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to scan repository: {result.stderr}")
    
    changes = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        
        # git status --porcelain format: XY PATH
        # X = staged status, Y = working tree status
        # There's a space between XY and PATH
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue
        
        status = parts[0].strip()
        path = parts[1]
        
        # Skip ignored paths
        if config.should_ignore(path):
            continue
        
        change_type = parse_status(status)
        changes.append(Change(
            path=path,
            change_type=change_type
        ))
    
    return changes


def parse_status(status: str) -> ChangeType:
    """Parse git status code to ChangeType."""
    if status in ('A', 'AD'):
        return ChangeType.ADDED
    elif status in ('D', 'D '):
        return ChangeType.DELETED
    elif status in ('R', 'RD'):
        return ChangeType.RENAMED
    else:
        return ChangeType.MODIFIED
