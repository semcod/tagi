"""CLI package for tagi."""

from tagi.cli.main import app, detect_provider, create_pr, create_mr

__all__ = ["app", "detect_provider", "create_pr", "create_mr"]
