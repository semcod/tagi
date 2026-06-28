"""CLI interface for tagi."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from tagi.models.change import Tag
from tagi.utils.logger import setup_logger

# Import command modules
from tagi.cli.core_commands import (
    scan_command, list_groups_command, list_command, stats_command
)
from tagi.cli.inspection_commands import (
    inspect_command, filter_command, file_command
)
from tagi.cli.git_operations import (
    send_command, auto_command
)
from tagi.cli.publishing_commands import (
    publish_command, deploy_command
)
from tagi.cli.utility_commands import (
    summary_command, draft_command, init_command, hooks_command
)
from tagi.cli.provider_commands import (
    detect_provider_command, create_pr, create_mr
)

app = typer.Typer(help="tagi - Git change orchestrator")
console = Console()
logger = None


@app.callback()
def setup_logging(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging", is_eager=True)):
    """Set up logging for all commands."""
    global logger
    logger = setup_logger(verbose=verbose)
    if verbose and logger:
        logger.debug("Verbose logging enabled")


def _configure_command_logging(verbose: bool) -> None:
    """Enable verbose logging for a single command invocation."""
    global logger
    if verbose:
        logger = setup_logger(verbose=True)
        logger.debug("Verbose logging enabled")


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag has # prefix."""
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def _is_known_tag(value: str) -> bool:
    """Return True when the value matches a supported tag."""
    try:
        Tag(_ensure_tag_prefix(value))
        return True
    except ValueError:
        return False


def _resolve_send_target(target: Optional[str], repo_path: str) -> tuple[str, Optional[str]]:
    """Resolve send positional input as either a tag or a repository path."""
    if target is None:
        return repo_path, None

    if repo_path != ".":
        return repo_path, target

    if _is_known_tag(target):
        return repo_path, target

    candidate = Path(target).expanduser()
    if candidate.exists():
        return str(candidate), None

    return repo_path, target


# Register core commands
app.command(name="scan")(scan_command)
app.command(name="list-groups")(list_groups_command)
app.command(name="list")(list_command)
app.command(name="stats")(stats_command)

# Register inspection commands
app.command(name="inspect")(inspect_command)
app.command(name="filter")(filter_command)
app.command(name="file")(file_command)

# Register git operations commands
app.command(name="send")(send_command)
app.command(name="auto")(auto_command)

# Register publishing commands
app.command(name="publish")(publish_command)
app.command(name="deploy")(deploy_command)

# Register utility commands
app.command(name="summary")(summary_command)
app.command(name="draft")(draft_command)
app.command(name="init")(init_command)
app.command(name="hooks")(hooks_command)


# Expose provider functions for backward compatibility
def detect_provider(repo_path: str = ".") -> str:
    """Detect Git provider (GitHub/GitLab) for the repository."""
    return detect_provider_command(repo_path)


# Make logger globally available for imported modules
def get_logger():
    """Get the global logger instance."""
    return logger
