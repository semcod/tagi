"""Git operations CLI commands: send, auto."""

from typing import Optional
import typer
from rich.console import Console

from tagi.composer.commit_message import generate_commit_message
from tagi.executor.git import GitExecutor
from tagi.heuristics.tags import apply_tags
from tagi.models.change import Tag
from tagi.scanner.status import scan_repo
from tagi.planner.sorter import sort_by_complexity
from tagi.utils.send_helpers import resolve_filtered_changes, create_change_group
from tagi.utils.detect_provider import detect_git_provider


console = Console()


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag starts with #."""
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def _resolve_send_target(target: Optional[str], repo_path: str) -> tuple[str, Optional[str]]:
    """Resolve send target to repo_path and tag."""
    if target is None:
        return repo_path, None
    
    # Check if target is a tag (starts with # or is a known tag)
    if target.startswith("#"):
        return repo_path, target
    
    # Check if it's a known tag without #
    try:
        Tag(f"#{target}")
        return repo_path, f"#{target}"
    except ValueError:
        # Assume it's a repository path
        return target, None


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
    from tagi.cli import _configure_command_logging
    _configure_command_logging(verbose)

    repo_path, tag = _resolve_send_target(target, repo_path)

    global logger
    if logger:
        logger.debug(f"Send command called with tag={tag}, repo_path={repo_path}, auto_order={auto_order}, dry_run={dry_run}, push={push}")

    if tag is None:
        console.print("[bold]Sending[/bold] all changes")
    else:
        console.print(f"[bold]Sending[/bold] {tag}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
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

    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return

    # Auto-order if requested
    if auto_order:
        filtered_changes = sort_by_complexity(filtered_changes)
        console.print("[green]Changes ordered by complexity[/green]")

    # Create change group
    group = create_change_group(filtered_changes, tag)

    # Generate commit message
    commit_message = generate_commit_message(group, template=template)

    if dry_run:
        console.print("\n[bold cyan]Dry run - changes that would be committed:[/bold cyan]")
        for change in filtered_changes:
            console.print(f"  • {change.path} [{change.change_type.value}]")
        console.print(f"\n[bold]Commit message:[/bold]\n{commit_message}")
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
