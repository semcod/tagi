"""Git hooks integration for tagi."""

import os
import subprocess
from pathlib import Path
from typing import List, Optional


def install_hooks(repo_path: str = ".") -> bool:
    """Install tagi pre-commit hook in the repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        True if successful, False otherwise
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    pre_commit_hook = hooks_dir / "pre-commit"
    
    hook_content = """#!/bin/bash
# tagi pre-commit hook
# Automatically tags changes before commit

if command -v tagi &> /dev/null; then
    # Scan and tag changes (dry run, no modifications)
    tagi scan . > /dev/null 2>&1 || true
fi

exit 0
"""
    
    try:
        pre_commit_hook.write_text(hook_content)
        pre_commit_hook.chmod(0o755)
        return True
    except (OSError, PermissionError):
        return False


def uninstall_hooks(repo_path: str = ".") -> bool:
    """Remove tagi hooks from the repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        True if successful, False otherwise
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    pre_commit_hook = hooks_dir / "pre-commit"
    
    try:
        if pre_commit_hook.exists():
            pre_commit_hook.unlink()
        return True
    except OSError:
        return False


def check_hooks_installed(repo_path: str = ".") -> bool:
    """Check if tagi hooks are installed.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        True if hooks are installed, False otherwise
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    pre_commit_hook = hooks_dir / "pre-commit"
    
    if not pre_commit_hook.exists():
        return False
    
    content = pre_commit_hook.read_text()
    return "tagi" in content


def list_hooks(repo_path: str = ".") -> List[str]:
    """List all git hooks in the repository.
    
    Args:
        repo_path: Path to the git repository
        
    Returns:
        List of hook names
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    
    if not hooks_dir.exists():
        return []
    
    hooks = []
    for hook_file in hooks_dir.iterdir():
        if hook_file.is_file() and hook_file.stat().st_mode & 0o111:
            hooks.append(hook_file.name)
    
    return sorted(hooks)


def run_hook(hook_name: str, repo_path: str = ".") -> subprocess.CompletedProcess:
    """Run a specific git hook.
    
    Args:
        hook_name: Name of the hook to run (e.g., "pre-commit")
        repo_path: Path to the git repository
        
    Returns:
        CompletedProcess result
    """
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    hook_file = hooks_dir / hook_name
    
    if not hook_file.exists():
        raise FileNotFoundError(f"Hook {hook_name} not found")
    
    return subprocess.run(
        [str(hook_file)],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
