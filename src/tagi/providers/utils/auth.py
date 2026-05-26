"""Authentication utilities for providers."""

from typing import Dict, Any
from subprocess import CompletedProcess


def get_auth_status_from_result(result: CompletedProcess) -> Dict[str, Any]:
    """Get authentication status from command result.
    
    Args:
        result: CompletedProcess from auth status command
        
    Returns:
        Dict with authenticated status, output, and error
    """
    return {
        "authenticated": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr if result.returncode != 0 else None
    }


def is_authenticated_from_result(result: CompletedProcess) -> bool:
    """Check if authenticated from command result.
    
    Args:
        result: CompletedProcess from auth status command
        
    Returns:
        True if authenticated, False otherwise
    """
    return result.returncode == 0
