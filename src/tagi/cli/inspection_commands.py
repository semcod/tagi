"""Inspection CLI commands: inspect, filter, file."""

import typer
from rich.console import Console

from tagi.scanner.diff import get_diff
from tagi.utils.inspect_helpers import (
    resolve_filtered_changes,
    display_statistics_table,
)
from tagi.cli.display_utils import _display_changes, _format_tags
from tagi.cli.scan_utils import scan_and_tag
from tagi.config import load_config


console = Console()


def inspect_command(
    tag: str = typer.Argument(..., help="Tag to inspect (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    diff: bool = typer.Option(False, "--diff", help="Show diff for each change"),
):
    """Inspect a specific change group."""
    console.print(f"[bold]Inspecting[/bold] {tag}")
    
    config = load_config(repo_path)

    
    # Add # prefix if not present
    tag_value = tag if tag.startswith("#") else f"#{tag}"
    
    # Filter changes by tag
    tag_changes = resolve_filtered_changes(scan_and_tag(repo_path), tag_value)
    
    if not tag_changes:
        console.print(f"[yellow]No changes found for {tag_value}[/yellow]")
        return
    
    # Show tag description if available
    tag_desc = config.get_tag_description(tag_value)
    if tag_desc:
        console.print(f"[dim]{tag_desc}[/dim]")
    
    # Display statistics
    display_statistics_table(tag_changes, console)
    
    _display_changes(tag_changes, config)
    
    if diff:
        console.print("\n[bold cyan]Diffs:[/bold cyan]")
        for change in tag_changes[:5]:  # Limit to first 5 files
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
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",")]
    
    # Filter changes
    matching_changes = resolve_filtered_changes(scan_and_tag(repo_path), tag_list, mode)
    
    if not matching_changes:
        console.print(f"[yellow]No changes found for tags: {tags}[/yellow]")
        return
    
    # Display statistics
    display_statistics_table(matching_changes, console)
    
    _display_changes(matching_changes)
    
    if diff:
        console.print("\n[bold cyan]Diffs:[/bold cyan]")
        for change in matching_changes[:5]:  # Limit to first 5 files
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
    
    # Find the specific file
    file_changes = [c for c in scan_and_tag(repo_path) if c.path == file_path]
    
    if not file_changes:
        console.print(f"[yellow]File not found in changes: {file_path}[/yellow]")
        return
    
    file_change = file_changes[0]
    
    # Display file information
    console.print(f"[cyan]Type:[/cyan] {file_change.change_type.value}")
    
    console.print(f"[cyan]Tags:[/cyan] {_format_tags(file_change.tags)}")
    
    if file_change.description:
        console.print(f"[cyan]Description:[/cyan] {file_change.description}")
    
    if diff:
        console.print("\n[bold cyan]Diff:[/bold cyan]")
        diff_output = get_diff(file_path, repo_path)
        if diff_output:
            console.print(diff_output)
        else:
            console.print("[yellow]No diff available[/yellow]")
