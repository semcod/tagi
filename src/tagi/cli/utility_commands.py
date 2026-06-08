"""Utility CLI commands: summary, draft."""

from typing import Optional
import typer
from rich.console import Console
from pathlib import Path

from tagi.composer.commit_message import generate_commit_message
from tagi.heuristics.tags import apply_tags
from tagi.models.change import Tag
from tagi.scanner.status import scan_repo
from tagi.utils.send_helpers import create_change_group
from tagi.utils.inspect_helpers import filter_changes_by_tag


console = Console()


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag starts with #."""
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def summary_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for summary report"),
):
    """Generate a comprehensive summary report of all changes."""
    console.print(f"[bold]Generating summary[/bold] for {repo_path}")
    
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
    
    # Generate summary content
    summary_lines = []
    summary_lines.append("# Change Summary Report")
    summary_lines.append(f"Repository: {Path(repo_path).absolute()}")
    summary_lines.append(f"Total changes: {len(changes)}")
    summary_lines.append("")
    
    # Group by tags
    from tagi.utils.inspect_helpers import calculate_tag_statistics
    tag_stats = calculate_tag_statistics(changes)
    
    summary_lines.append("## Changes by Tag")
    for tag, count in tag_stats.items():
        if count > 0:
            summary_lines.append(f"- {tag}: {count} change(s)")
    summary_lines.append("")
    
    # Detailed change list
    summary_lines.append("## Detailed Changes")
    for change in changes:
        tags_str = ", ".join([tag.value for tag in change.tags]) if change.tags else "none"
        summary_lines.append(f"- **{change.path}** [{change.change_type.value}]")
        summary_lines.append(f"  Tags: {tags_str}")
        if change.description:
            summary_lines.append(f"  Description: {change.description}")
        summary_lines.append("")
    
    summary_content = "\n".join(summary_lines)
    
    # Output summary
    if output:
        output_path = Path(output)
        output_path.write_text(summary_content)
        console.print(f"[green]✓ Summary saved to:[/green] {output_path}")
    else:
        console.print(summary_content)


def draft_command(
    tag: str = typer.Argument(..., help="Tag to draft (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
):
    """Draft a commit message for a change group."""
    console.print(f"[bold]Drafting[/bold] commit message for {tag}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    tag = _ensure_tag_prefix(tag)
    try:
        tag_enum = Tag(tag)
    except ValueError:
        console.print(f"[red]Unknown tag: {tag}[/red]")
        raise typer.Exit(1)
    
    filtered_changes = filter_changes_by_tag(changes, tag)
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    # Create change group
    group = create_change_group(filtered_changes, tag)
    
    # Generate commit message
    commit_message = generate_commit_message(group, template=template)
    
    console.print("\n[bold cyan]Draft commit message:[/bold cyan]")
    console.print(commit_message)
    
    console.print(f"\n[dim]Changes included: {len(filtered_changes)}[/dim]")
    for change in filtered_changes:
        console.print(f"  • {change.path}")
