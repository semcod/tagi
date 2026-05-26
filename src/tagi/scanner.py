"""Scanner module for reading git repository state."""

import subprocess
from typing import List

from tagi.models import Change, ChangeType


def scan_repo(repo_path: str = ".") -> List[Change]:
    """Scan repository for uncommitted changes using git status --porcelain."""
    cmd = ["git", "status", "--porcelain"]
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )
    
    changes = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        
        status = line[:2].strip()
        path = line[3:]
        
        change_type = _parse_status(status)
        changes.append(Change(
            path=path,
            change_type=change_type
        ))
    
    return changes


def _parse_status(status: str) -> ChangeType:
    """Parse git status code to ChangeType."""
    if status in ('A', 'AD'):
        return ChangeType.ADDED
    elif status in ('D', 'D '):
        return ChangeType.DELETED
    elif status in ('R', 'RD'):
        return ChangeType.RENAMED
    else:
        return ChangeType.MODIFIED
