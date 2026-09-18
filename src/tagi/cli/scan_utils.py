"""Shared change-loading helper for CLI commands."""

import typer
from rich.console import Console


console = Console()


def scan_and_tag(repo_path: str):
    """Scan repo and apply tags; exits(1) with a user-facing error on failure.

    Resolves ``scan_repo``/``apply_tags`` through the ``tagi.cli`` namespace at
    call time so tests can keep patching them there.
    """
    import tagi.cli as _cli
    try:
        changes = _cli.scan_repo(repo_path)
        return _cli.apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
