"""CLI package for tagi."""

from tagi.cli.main import (
    app,
    detect_provider,
    _ensure_tag_prefix,
    _is_known_tag,
    _resolve_send_target,
    _configure_command_logging,
)
from tagi.cli.provider_commands import create_pr, create_mr

# Re-export the underlying operations so they can be referenced (and patched in
# tests) via the ``tagi.cli`` namespace, matching the historical single-module
# layout that the test-suite was written against.
from tagi.scanner.status import scan_repo
from tagi.heuristics.tags import apply_tags
from tagi.composer.commit_message import generate_commit_message

__all__ = [
    "app",
    "detect_provider",
    "create_pr",
    "create_mr",
    "_ensure_tag_prefix",
    "_is_known_tag",
    "_resolve_send_target",
    "_configure_command_logging",
    "scan_repo",
    "apply_tags",
    "generate_commit_message",
]
