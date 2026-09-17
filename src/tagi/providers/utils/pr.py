"""Pull request creation utilities."""

from subprocess import CompletedProcess
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from tagi.providers.base import PrSpec


def build_pr_command(tool: str, pr_type: str, spec: "PrSpec") -> List[str]:
    """Build PR/MR creation command for gh or glab.

    Args:
        tool: CLI tool name ('gh' or 'glab')
        pr_type: Type of PR ('pr' for gh, 'mr' for glab)
        spec: pull/merge request parameters

    Returns:
        Command as list of strings
    """
    if tool == "gh":
        cmd = ["gh", "pr", "create", "--title", spec.title, "--body", spec.body, "--base", spec.base]
    elif tool == "glab":
        cmd = ["glab", "mr", "create", "--title", spec.title, "--description", spec.body, "--target-branch", spec.base]
    else:
        raise ValueError(f"Unsupported tool: {tool}")

    if spec.draft:
        cmd.append("--draft")
    if spec.labels:
        cmd.extend(["--label", ",".join(spec.labels)])
    
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
