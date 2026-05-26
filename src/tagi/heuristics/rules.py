"""Rules module for custom tagging rules."""

from tagi.config import Config


def get_custom_rules(repo_path: str = "."):
    """Get custom rules from config."""
    config = Config(repo_path)
    return config.custom_rules


def get_custom_heuristics(repo_path: str = "."):
    """Get custom heuristics from config."""
    config = Config(repo_path)
    return config.custom_heuristics
