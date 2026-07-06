"""Core CLI commands: scan, list, stats."""

import typer
from rich.console import Console

from tagi.heuristics.tags import apply_tags
from tagi.scanner.status import scan_repo
from tagi.utils.inspect_helpers import calculate_tag_statistics, display_statistics_table
from tagi.cli.display_utils import _display_changes, _display_changes_grouped


console = Console()


def scan_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    grouped: bool = typer.Option(False, "--grouped", "-g", help="Group changes by tag"),
):
    """Scan repository for uncommitted changes."""
    console.print(f"[bold]Scanning[/bold] {repo_path}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    if not changes:
        console.print("[green]No uncommitted changes found[/green]")
        return
    
    if grouped:
        _display_changes_grouped(changes)
    else:
        _display_changes(changes)


def list_groups_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """List available change groups."""
    _do_list_groups(repo_path)


def list_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """List available change groups (alias for list-groups)."""
    _do_list_groups(repo_path)


def _do_list_groups(repo_path: str) -> None:
    """Shared implementation for list and list-groups commands."""
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
    
    # Calculate and display statistics
    stats = calculate_tag_statistics(changes)
    display_statistics_table(changes, console)
    
    console.print("\n[bold]Available change groups:[/bold]")
    for tag, count in stats.items():
        if count > 0:
            console.print(f"  {tag}: {count} change(s)")


def stats_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed statistics"),
):
    """Show statistics about changes."""
    console.print(f"[bold]Statistics[/bold] for {repo_path}")
    
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
    
    # Display statistics table
    display_statistics_table(changes, console)
    
    if verbose:
        console.print("\n[bold]Detailed breakdown:[/bold]")
        from tagi.utils.inspect_helpers import filter_changes_by_tags_any
        
        # Group by tags and show details
        tag_stats = calculate_tag_statistics(changes)
        for tag, count in tag_stats.items():
            if count > 0:
                console.print(f"\n[cyan]{tag}[/cyan] ({count} changes):")
                tag_changes = filter_changes_by_tags_any(changes, [tag])
                for change in tag_changes[:5]:  # Limit to first 5
                    console.print(f"  • {change.path}")
                if len(tag_changes) > 5:
                    console.print(f"  ... and {len(tag_changes) - 5} more")
