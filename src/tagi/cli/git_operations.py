"""Git operations CLI commands: send, auto."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console

from tagi.executor.git import GitExecutor
from tagi.models.change import Tag
from tagi.planner.sorter import sort_by_complexity
from tagi.utils.send_helpers import create_change_group
from tagi.utils.detect_provider import detect_git_provider


console = Console()


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag starts with #."""
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

    # An explicit --repo-path means the positional argument is always a tag.
    if repo_path != ".":
        return repo_path, target

    # Known tags are treated as tags.
    if _is_known_tag(target):
        return repo_path, target

    # An existing filesystem path is treated as the repository path.
    candidate = Path(target).expanduser()
    if candidate.exists():
        return str(candidate), None

    # Otherwise treat the value as a (possibly unknown) tag so the caller can
    # report it cleanly instead of failing on a missing path.
    return repo_path, target


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

    logger = _cli.main.get_logger()
    if logger:
        logger.debug(f"Send command called with tag={tag}, repo_path={repo_path}, auto_order={auto_order}, dry_run={dry_run}, push={push}")

    if tag is None:
        console.print("[bold]Sending[/bold] all changes")
    else:
        console.print(f"[bold]Sending[/bold] {tag}")

    try:
        changes = _cli.scan_repo(repo_path)
        changes = _cli.apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)

    if not changes:
        console.print("[yellow]No changes found[/yellow]")
        return

    if tag is None:
        filtered_changes = changes
    else:
        tag = _ensure_tag_prefix(tag)
        try:
            tag_enum = Tag(tag)
        except ValueError:
            console.print(f"[red]Unknown tag: {tag}[/red]")
            raise typer.Exit(1)
        filtered_changes = [c for c in changes if tag_enum in c.tags]

    # Auto-order if requested
    if auto_order:
        console.print("[bold]Sorting changes by complexity (simplest first)[/bold]")
        filtered_changes = sort_by_complexity(filtered_changes)

    if not filtered_changes:
        if tag is None:
            console.print("[yellow]No changes found[/yellow]")
        else:
            console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return

    # Create change group
    group = create_change_group(filtered_changes, tag)

    # Generate commit message
    commit_message = _cli.generate_commit_message(
        group.changes, template=template, repo_path=repo_path
    )
    console.print("\n[bold cyan]Commit message:[/bold cyan]")
    console.print(commit_message)

    if dry_run:
        console.print("\n[yellow][DRY-RUN] No changes will be made[/yellow]")
        return

    # Execute git operations
    git_executor = GitExecutor(repo_path)

    try:
        # Stage changes
        for change in filtered_changes:
            git_executor.stage(change.path)

        # Commit
        git_executor.commit(commit_message)
        console.print(f"[green]✓ Committed {len(filtered_changes)} change(s)[/green]")

        # Push if requested
        if push:
            provider = detect_git_provider(repo_path)
            if provider:
                git_executor.push()
                console.print("[green]✓ Pushed to remote[/green]")
            else:
                console.print("[yellow]Warning: Could not detect provider, skipping push[/yellow]")

    except Exception as e:
        console.print(f"[red]Error during git operations: {e}[/red]")
        raise typer.Exit(1)


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
