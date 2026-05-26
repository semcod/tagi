"""Providers module for GitHub/GitLab integration."""

import subprocess
from typing import Optional


def create_pr(title: str, body: str, repo_path: str = ".", dry_run: bool = False) -> bool:
    """Create a pull request using GitHub CLI."""
    if dry_run:
        print(f"[DRY-RUN] Would create PR with title: {title}")
        return True
    
    # Check if gh is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI (gh) not found. Please install it first.")
        return False
    
    cmd = ["gh", "pr", "create", "--title", title, "--body", body]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"Error creating PR: {result.stderr}")
        return False
    
    return True


def create_mr(title: str, body: str, repo_path: str = ".", dry_run: bool = False) -> bool:
    """Create a merge request using GitLab CLI."""
    if dry_run:
        print(f"[DRY-RUN] Would create MR with title: {title}")
        return True
    
    # Check if glab is available
    try:
        subprocess.run(["glab", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitLab CLI (glab) not found. Please install it first.")
        return False
    
    cmd = ["glab", "mr", "create", "--title", title, "--description", body]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"Error creating MR: {result.stderr}")
        return False
    
    return True


def detect_provider(repo_path: str = ".") -> Optional[str]:
    """Detect if repository uses GitHub or GitLab."""
    # Check for GitHub
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )
    
    if "github.com" in result.stdout:
        return "github"
    elif "gitlab.com" in result.stdout:
        return "gitlab"
    
    return None
