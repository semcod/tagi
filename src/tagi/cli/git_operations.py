"""Git operations CLI commands: send, auto."""

from typing import Optional
import typer
from rich.console import Console

from tagi.executor.git import GitExecutor
from tagi.planner.sorter import sort_by_complexity
from tagi.utils.inspect_helpers import resolve_filtered_changes
from tagi.utils.logger import get_logger
from tagi.utils.send_helpers import create_change_group
from tagi.providers.detector import get_provider
from tagi.cli.scan_utils import scan_and_tag
from tagi.cli.tag_targets import (
    _ensure_tag_prefix,
    _resolve_send_target,
)


console = Console()


def _filter_by_tag(changes, tag: Optional[str]):
    """Filter changes to ``tag``; returns all changes when tag is None."""
    if tag is None:
        return changes
    try:
        return resolve_filtered_changes(changes, tag)
    except ValueError:
        console.print(f"[red]Unknown tag: {_ensure_tag_prefix(tag)}[/red]")
        raise typer.Exit(1)


def _execute_git_operations(changes, commit_message: str, push: bool, repo_path: str) -> None:
    """Stage, commit and optionally push; exits(1) on failure."""
    git_executor = GitExecutor(repo_path)
    try:
        git_executor.add([change.path for change in changes])
        git_executor.commit(commit_message)
        console.print(f"[green]✓ Committed {len(changes)} change(s)[/green]")

        if push:
            if get_provider(repo_path) is not None:
                git_executor.push()
                console.print("[green]✓ Pushed to remote[/green]")
            else:
                console.print("[yellow]Warning: Could not detect provider, skipping push[/yellow]")
    except Exception as e:
        console.print(f"[red]Error during git operations: {e}[/red]")
        raise typer.Exit(1)


def _collect_changes(repo_path: str, tag: Optional[str], auto_order: bool):
    """Print the send header, scan and filter by tag; returns changes to send (may be empty)."""
    if tag is None:
        console.print("[bold]Sending[/bold] all changes")
    else:
        console.print(f"[bold]Sending[/bold] {tag}")

    tagged_changes = scan_and_tag(repo_path)
    if not tagged_changes:
        console.print("[yellow]No changes found[/yellow]")
        return []

    changes = _filter_by_tag(tagged_changes, tag)

    # Auto-order if requested
    if auto_order:
        console.print("[bold]Sorting changes by complexity (simplest first)[/bold]")
        changes = sort_by_complexity(changes)

    if not changes:
        if tag is None:
            console.print("[yellow]No changes found[/yellow]")
        else:
            console.print(f"[yellow]No changes found for {tag}[/yellow]")
    return changes


def _send_changes(changes, tag: Optional[str], template: str, repo_path: str, dry_run: bool, push: bool) -> None:
    """Generate and preview the commit message, then stage/commit/push unless dry-run."""
    import tagi.cli as _cli

    # Create change group
    group = create_change_group(changes, tag)

    # Generate commit message
    commit_message = _cli.generate_commit_message(
        group.changes, template=template, repo_path=repo_path
    )
    console.print("\n[bold cyan]Commit message:[/bold cyan]")
    console.print(commit_message)

    if dry_run:
        console.print("\n[yellow][DRY-RUN] No changes will be made[/yellow]")
        return

    _execute_git_operations(changes, commit_message, push, repo_path)


def send_command(
    target: Optional[str] = typer.Argument(None, help="Tag to send (e.g., small) or repository path. If not specified, sends all changes"),
    repo_path: str = typer.Option(".", "--repo-path", "--path", help="Path to repository"),
    auto_order: bool = typer.Option(False, "--auto-order", "-a", help="Automatically order changes by complexity (simplest first)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    push: bool = typer.Option(False, "--push", help="Push after commit"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Stage, commit, and optionally push changes."""
    import tagi.cli as _cli
    _cli._configure_command_logging(verbose)

    repo_path, tag = _resolve_send_target(target, repo_path)
    if tag is not None:
        # create_change_group builds Tag values directly, so the documented
        # unprefixed form (``tagi send small``) must be normalized here.
        tag = _ensure_tag_prefix(tag)

    get_logger().debug(f"Send command called with tag={tag}, repo_path={repo_path}, auto_order={auto_order}, dry_run={dry_run}, push={push}")

    changes_to_send = _collect_changes(repo_path, tag, auto_order)
    if not changes_to_send:
        return

    _send_changes(changes_to_send, tag, template, repo_path, dry_run, push)


def auto_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    push: bool = typer.Option(True, "--push/--no-push", help="Push after commit (default: push)"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Automatically scan, order, and send all changes."""
    from tagi.cli import _configure_command_logging
    _configure_command_logging(verbose)

    console.print("[bold]Auto mode:[/bold] scanning, ordering, and sending all changes")

    # Use send command with auto_order=True and no specific tag
    send_command(
        target=None,
        repo_path=repo_path,
        auto_order=True,
        dry_run=dry_run,
        push=push,
        template=template,
        verbose=verbose
    )
