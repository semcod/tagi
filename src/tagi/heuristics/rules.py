"""Rules module for custom tagging rules."""

from typing import Any, Optional

from tagi.config import Config


def _get_config_attr(repo_path: str, attr_name: str) -> Any:
    """Helper to get config attribute."""
    config = Config(repo_path)
    return getattr(config, attr_name, None)


def get_custom_rules(repo_path: str = ".") -> Optional[Any]:
    """Get custom rules from config."""
    return _get_config_attr(repo_path, "custom_rules")


def get_custom_heuristics(repo_path: str = ".") -> Optional[Any]:
    """Get custom heuristics from config."""
    return _get_config_attr(repo_path, "custom_heuristics")
