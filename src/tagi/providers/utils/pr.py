"""Pull request creation utilities."""

from typing import List, Optional
from subprocess import CompletedProcess


def build_pr_command(
    tool: str,
    pr_type: str,
    title: str,
    body: str,
    branch: str,
    base: str = "main",
    draft: bool = False,
    labels: Optional[List[str]] = None
) -> List[str]:
    """Build PR/MR creation command for gh or glab.
    
    Args:
        tool: CLI tool name ('gh' or 'glab')
        pr_type: Type of PR ('pr' for gh, 'mr' for glab)
        title: PR title
        body: PR body/description
        branch: Source branch
        base: Target branch
        draft: Whether to create as draft
        labels: Optional labels
        
    Returns:
        Command as list of strings
    """
    if tool == "gh":
        cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]
    elif tool == "glab":
        cmd = ["glab", "mr", "create", "--title", title, "--description", body, "--target-branch", base]
    else:
        raise ValueError(f"Unsupported tool: {tool}")
    
    if draft:
        cmd.append("--draft")
    if labels:
        cmd.extend(["--label", ",".join(labels)])
    
    return cmd


def execute_pr_command(result: CompletedProcess) -> str:
    """Execute PR command and return stdout or empty string on failure.
    
    Args:
        result: CompletedProcess from command execution
        
    Returns:
        stdout if successful, empty string otherwise
    """
    if result.returncode == 0:
        return result.stdout
    return ""
