"""CLI interface for tagi."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from tagi.composer import generate_commit_message
from tagi.executor import commit_changes, push_changes, stage_changes
from tagi.heuristics import apply_tags
from tagi.models import Tag
from tagi.planner import group_changes
from tagi.providers import create_mr, create_pr, detect_provider
from tagi.scanner import scan_repo

app = typer.Typer(help="tagi - Git change orchestrator")
console = Console()


@app.command()
def scan(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """Scan repository for uncommitted changes."""
    console.print(f"[bold]Scanning[/bold] {repo_path}")
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        console.print("[red]Error: Not a git repository[/red]")
        raise typer.Exit(1)
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    
    if not changes:
        console.print("[green]No uncommitted changes found[/green]")
        return
    
    _display_changes(changes)


@app.command()
def list_groups(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """List available change groups."""
    console.print(f"[bold]Listing groups[/bold] in {repo_path}")
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    groups = group_changes(changes)
    
    if not groups:
        console.print("[yellow]No changes found[/yellow]")
        return
    
    _display_groups(groups)


@app.command()
def inspect(
    tag: str = typer.Argument(..., help="Tag to inspect (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """Inspect a specific change group."""
    console.print(f"[bold]Inspecting[/bold] {tag}")
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    
    # Filter changes by tag
    tag_enum = Tag(tag)
    filtered_changes = [c for c in changes if tag_enum in c.tags]
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    _display_changes(filtered_changes)


@app.command()
def draft(
    tag: str = typer.Argument(..., help="Tag to draft (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """Draft a commit message for a change group."""
    console.print(f"[bold]Drafting[/bold] {tag}")
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    groups = group_changes(changes)
    
    # Find group by tag
    tag_enum = Tag(tag)
    group = None
    for g in groups:
        if tag_enum in g.tags:
            group = g
            break
    
    if not group:
        console.print(f"[yellow]No group found for {tag}[/yellow]")
        return
    
    message = generate_commit_message(group)
    console.print("\n[bold cyan]Commit message draft:[/bold cyan]")
    console.print(message)


@app.command()
def send(
    tag: str = typer.Argument(..., help="Tag to send (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    push: bool = typer.Option(False, "--push", help="Push after commit"),
):
    """Stage, commit, and optionally push changes."""
    console.print(f"[bold]Sending[/bold] {tag}")
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    groups = group_changes(changes)
    
    # Find group by tag
    tag_enum = Tag(tag)
    group = None
    for g in groups:
        if tag_enum in g.tags:
            group = g
            break
    
    if not group:
        console.print(f"[yellow]No group found for {tag}[/yellow]")
        return
    
    # Generate commit message
    message = generate_commit_message(group)
    console.print("\n[bold cyan]Commit message:[/bold cyan]")
    console.print(message)
    
    if dry_run:
        console.print("\n[yellow][DRY-RUN] No changes will be made[/yellow]")
        return
    
    # Confirm
    if not typer.confirm("\nProceed with staging and committing?"):
        console.print("[yellow]Aborted[/yellow]")
        return
    
    # Stage changes
    console.print(f"\n[bold]Staging[/bold] {len(group.changes)} files...")
    if not stage_changes(group.changes, repo_path):
        console.print("[red]Error staging changes[/red]")
        raise typer.Exit(1)
    
    # Commit
    console.print("[bold]Committing[/bold]...")
    if not commit_changes(message, repo_path):
        console.print("[red]Error committing[/red]")
        raise typer.Exit(1)
    
    console.print("[green]✓ Changes committed[/green]")
    
    # Push if requested
    if push:
        console.print("[bold]Pushing[/bold]...")
        if not push_changes(repo_path):
            console.print("[red]Error pushing[/red]")
            raise typer.Exit(1)
        console.print("[green]✓ Changes pushed[/green]")


@app.command()
def publish(
    tag: str = typer.Argument(..., help="Tag to publish (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
):
    """Create a PR or MR for the changes."""
    console.print(f"[bold]Publishing[/bold] {tag}")
    
    changes = scan_repo(repo_path)
    changes = apply_tags(changes, repo_path)
    groups = group_changes(changes)
    
    # Find group by tag
    tag_enum = Tag(tag)
    group = None
    for g in groups:
        if tag_enum in g.tags:
            group = g
            break
    
    if not group:
        console.print(f"[yellow]No group found for {tag}[/yellow]")
        return
    
    # Detect provider
    provider = detect_provider(repo_path)
    if not provider:
        console.print("[yellow]Could not detect GitHub or GitLab provider[/yellow]")
        console.print("[yellow]Please ensure you have a remote configured[/yellow]")
        return
    
    console.print(f"[bold]Detected provider:[/bold] {provider}")
    
    # Generate commit message
    message = generate_commit_message(group)
    title = message.split('\n')[0]  # First line as title
    body = '\n'.join(message.split('\n')[1:])  # Rest as body
    
    console.print(f"\n[bold cyan]PR/MR Title:[/bold cyan]")
    console.print(title)
    console.print(f"\n[bold cyan]PR/MR Body:[/bold cyan]")
    console.print(body)
    
    if dry_run:
        console.print(f"\n[yellow][DRY-RUN] Would create {provider} PR/MR[/yellow]")
        return
    
    # Confirm
    if not typer.confirm(f"\nCreate {provider} PR/MR?"):
        console.print("[yellow]Aborted[/yellow]")
        return
    
    # Create PR/MR
    console.print(f"\n[bold]Creating {provider} PR/MR[/bold]...")
    if provider == "github":
        if not create_pr(title, body, repo_path):
            console.print("[red]Error creating PR[/red]")
            raise typer.Exit(1)
    elif provider == "gitlab":
        if not create_mr(title, body, repo_path):
            console.print("[red]Error creating MR[/red]")
            raise typer.Exit(1)
    
    console.print(f"[green]✓ {provider.capitalize()} PR/MR created[/green]")


def _display_changes(changes):
    """Display changes in a table."""
    table = Table(title="Changes")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Tags", style="green")
    
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        table.add_row(change.path, change.change_type.value, tags_str)
    
    console.print(table)


def _display_groups(groups):
    """Display groups in a table."""
    table = Table(title="Change Groups")
    table.add_column("Group", style="cyan")
    table.add_column("Files", style="magenta")
    table.add_column("Tags", style="green")
    
    for group in groups:
        tags_str = ", ".join([t.value for t in group.tags])
        table.add_row(group.name, str(len(group.changes)), tags_str)
    
    console.print(table)


if __name__ == "__main__":
    app()
