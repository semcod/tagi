"""Provider detection utilities."""

from typing import Optional
from pathlib import Path
import subprocess


def detect_git_provider(repo_path: str = ".") -> Optional[str]:
    """Detect which Git provider is used for the repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        'github', 'gitlab', or None if unknown
    """
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.lower()
        
        if "github.com" in output:
            return "github"
        elif "gitlab.com" in output:
            return "gitlab"
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
