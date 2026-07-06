"""Inspection CLI commands: inspect, filter, file."""

import typer
from rich.console import Console

from tagi.heuristics.tags import apply_tags
from tagi.scanner.status import scan_repo
from tagi.scanner.diff import get_diff
from tagi.utils.inspect_helpers import (
    filter_changes_by_tag, 
    display_statistics_table,
    filter_changes_by_tags_any,
    filter_changes_by_tags_all
)
from tagi.cli.display_utils import _display_changes
from tagi.config import Config


console = Console()


def inspect_command(
    tag: str = typer.Argument(..., help="Tag to inspect (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    diff: bool = typer.Option(False, "--diff", help="Show diff for each change"),
):
    """Inspect a specific change group."""
    console.print(f"[bold]Inspecting[/bold] {tag}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    config = Config(repo_path)
    
    # Add # prefix if not present
    if not tag.startswith("#"):
        tag = f"#{tag}"
    
    # Filter changes by tag
    filtered_changes = filter_changes_by_tag(changes, tag)
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    # Show tag description if available
    tag_desc = config.get_tag_description(tag)
    if tag_desc:
        console.print(f"[dim]{tag_desc}[/dim]")
    
    # Display statistics
    display_statistics_table(filtered_changes, console)
    
    _display_changes(filtered_changes, config)
    
    if diff:
        console.print("\n[bold cyan]Diffs:[/bold cyan]")
        for change in filtered_changes[:5]:  # Limit to first 5 files
            diff_output = get_diff(change.path, repo_path)
            if diff_output:
                console.print(f"\n[bold]{change.path}:[/bold]")
                console.print(diff_output)


def filter_command(
    tags: str = typer.Argument(..., help="Tags to filter (comma-separated, e.g., #small,#docs)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    mode: str = typer.Option("any", "--mode", "-m", help="Filter mode: any (match any tag) or all (match all tags)"),
    diff: bool = typer.Option(False, "--diff", help="Show diff for each change"),
):
    """Filter changes by tags."""
    console.print(f"[bold]Filtering[/bold] changes by tags: {tags}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",")]
    tag_list = [tag if tag.startswith("#") else f"#{tag}" for tag in tag_list]
    
    # Filter changes
    if mode == "all":
        filtered_changes = filter_changes_by_tags_all(changes, tag_list)
    else:  # default to "any"
        filtered_changes = filter_changes_by_tags_any(changes, tag_list)
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for tags: {tags}[/yellow]")
        return
    
    # Display statistics
    display_statistics_table(filtered_changes, console)
    
    _display_changes(filtered_changes)
    
    if diff:
        console.print("\n[bold cyan]Diffs:[/bold cyan]")
        for change in filtered_changes[:5]:  # Limit to first 5 files
            diff_output = get_diff(change.path, repo_path)
            if diff_output:
                console.print(f"\n[bold]{change.path}:[/bold]")
                console.print(diff_output)


def file_command(
    file_path: str = typer.Argument(..., help="File path to inspect"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    diff: bool = typer.Option(False, "--diff", help="Show diff for the file"),
):
    """Show detailed information about a specific file."""
    console.print(f"[bold]File:[/bold] {file_path}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    # Find the specific file
    file_changes = [c for c in changes if c.path == file_path]
    
    if not file_changes:
        console.print(f"[yellow]File not found in changes: {file_path}[/yellow]")
        return
    
    file_change = file_changes[0]
    
    # Display file information
    console.print(f"[cyan]Type:[/cyan] {file_change.change_type.value}")
    
    tags_str = ", ".join([tag.value for tag in file_change.tags]) if file_change.tags else "none"
    console.print(f"[cyan]Tags:[/cyan] {tags_str}")
    
    if file_change.description:
        console.print(f"[cyan]Description:[/cyan] {file_change.description}")
    
    if diff:
        console.print("\n[bold cyan]Diff:[/bold cyan]")
        diff_output = get_diff(file_path, repo_path)
        if diff_output:
            console.print(diff_output)
        else:
            console.print("[yellow]No diff available[/yellow]")
