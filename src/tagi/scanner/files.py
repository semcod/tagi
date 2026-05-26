"""Files module for file-related operations."""

import subprocess


def count_lines_changed(file_path: str, repo_path: str = ".") -> int:
    """Count the number of lines changed in a file."""
    try:
        cmd = ["git", "diff", "--numstat", file_path]
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return 0
        
        # git diff --numstat output: additions deletions filename
        parts = result.stdout.strip().split()
        if len(parts) >= 2:
            additions = int(parts[0]) if parts[0] != '-' else 0
            deletions = int(parts[1]) if parts[1] != '-' else 0
            return additions + deletions
        
        return 0
    except (ValueError, IndexError, subprocess.SubprocessError):
        return 0
