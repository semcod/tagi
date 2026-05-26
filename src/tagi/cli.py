"""CLI interface for tagi."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from tagi.composer.commit_message import generate_commit_message
from tagi.executor.publish import PublishExecutor
from tagi.heuristics.tags import apply_tags
from tagi.heuristics.scoring import calculate_risk_score
from tagi.models.change import ChangeType, Tag
from tagi.planner.grouper import group_changes
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider
from tagi.scanner.status import scan_repo
from tagi.scanner.diff import get_diff

app = typer.Typer(help="tagi - Git change orchestrator")
console = Console()


@app.command()
def scan(
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


@app.command()
def list_groups(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """List available change groups."""
    console.print(f"[bold]Listing groups[/bold] in {repo_path}")
    
    try:
        from tagi.config import Config
        config = Config(repo_path)
        
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
        groups = group_changes(changes)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    if not groups:
        console.print("[yellow]No changes found[/yellow]")
        return
    
    _display_groups(groups, config)


@app.command()
def stats(
    repo_path: str = typer.Argument(".", help="Path to repository"),
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
    
    # Calculate statistics
    total_files = len(changes)
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    avg_risk = sum(getattr(c, 'risk_score', 0) for c in changes) / total_files if total_files else 0
    
    # Count by type
    from tagi.models.change import ChangeType
    by_type = {}
    for change in changes:
        ct = change.change_type
        by_type[ct] = by_type.get(ct, 0) + 1
    
    # Count by tag
    from collections import Counter
    tag_counts = Counter()
    for change in changes:
        for tag in change.tags:
            tag_counts[tag.value] += 1
    
    # Display statistics
    table = Table(title="Change Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total files", str(total_files))
    table.add_row("Total lines changed", str(total_lines))
    table.add_row("Average risk score", f"{avg_risk:.2f}")
    
    console.print(table)
    
    # Type distribution
    console.print("\n[bold cyan]Change Types:[/bold cyan]")
    type_table = Table()
    type_table.add_column("Type", style="cyan")
    type_table.add_column("Count", style="magenta")
    
    for ct, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        type_table.add_row(ct.value, str(count))
    
    console.print(type_table)
    
    # Tag distribution
    console.print("\n[bold cyan]Tag Distribution:[/bold cyan]")
    tag_table = Table()
    tag_table.add_column("Tag")
    tag_table.add_column("Count", style="magenta")
    
    for tag, count in tag_counts.most_common():
        tag_table.add_row(tag, str(count))
    
    console.print(tag_table)


@app.command()
def inspect(
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
    
    from tagi.config import Config
    config = Config(repo_path)
    
    # Filter changes by tag
    tag_enum = Tag(tag)
    filtered_changes = [c for c in changes if tag_enum in c.tags]
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    # Show tag description if available
    tag_desc = config.get_tag_description(tag)
    if tag_desc:
        console.print(f"[dim]{tag_desc}[/dim]")
    
    # Calculate statistics for this tag
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in filtered_changes)
    avg_risk = sum(getattr(c, 'risk_score', 0) for c in filtered_changes) / len(filtered_changes)
    
    stats_table = Table()
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")
    stats_table.add_row("Files", str(len(filtered_changes)))
    stats_table.add_row("Total Lines", str(total_lines))
    stats_table.add_row("Avg Risk Score", f"{avg_risk:.2f}")
    console.print(stats_table)
    
    _display_changes(filtered_changes, config)
    
    if diff:
        console.print("\n[bold cyan]Diffs:[/bold cyan]")
        for change in filtered_changes[:5]:  # Limit to first 5 files
            diff_output = get_diff(change.path, repo_path)
            if diff_output:
                console.print(f"\n[bold]{change.path}[/bold]")
                console.print(diff_output[:500])  # Limit diff output
                if len(diff_output) > 500:
                    console.print("... (truncated)")
        
        if len(filtered_changes) > 5:
            console.print(f"\n... and {len(filtered_changes) - 5} more files")


@app.command()
def filter(
    tags: str = typer.Argument(..., help="Tags to filter by (comma-separated, e.g., #small,#docs)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    match_all: bool = typer.Option(False, "--all", "-a", help="Match all tags instead of any"),
):
    """Filter changes by tags."""
    console.print(f"[bold]Filtering[/bold] by tags: {tags}")
    
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
    tag_list = [t.strip() for t in tags.split(',')]
    tag_enums = []
    for t in tag_list:
        try:
            tag_enums.append(Tag(t))
        except ValueError:
            console.print(f"[yellow]Warning: Invalid tag '{t}', skipping[/yellow]")
    
    if not tag_enums:
        console.print("[red]No valid tags provided[/red]")
        raise typer.Exit(1)
    
    # Filter changes
    if match_all:
        filtered_changes = [c for c in changes if all(t in c.tags for t in tag_enums)]
        console.print(f"[dim]Mode: Match ALL tags[/dim]")
    else:
        filtered_changes = [c for c in changes if any(t in c.tags for t in tag_enums)]
        console.print(f"[dim]Mode: Match ANY tag[/dim]")
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found matching tags: {tags}[/yellow]")
        return
    
    from tagi.config import Config
    config = Config(repo_path)
    
    console.print(f"[green]Found {len(filtered_changes)} files[/green]")
    _display_changes(filtered_changes, config)


@app.command()
def file(
    file_path: str = typer.Argument(..., help="File path to inspect"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """Show detailed information about a specific file."""
    console.print(f"[bold]File Details:[/bold] {file_path}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
    # Find the file
    change = None
    for c in changes:
        if c.path == file_path or c.path.endswith(file_path):
            change = c
            break
    
    if not change:
        console.print(f"[yellow]File not found in changes: {file_path}[/yellow]")
        return
    
    from tagi.config import Config
    config = Config(repo_path)
    
    # Display file details
    table = Table()
    table.add_column("Property", style="cyan")
    table.add_column("Value")
    
    table.add_row("Path", change.path)
    table.add_row("Type", change.change_type.value)
    table.add_row("Tags", _format_tags(change.tags, config))
    table.add_row("Lines Changed", str(getattr(change, 'lines_changed', 0)))
    table.add_row("Risk Score", f"{getattr(change, 'risk_score', 0):.2f}")
    
    console.print(table)


@app.command()
def summary(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    output: str = typer.Option(None, "--output", "-o", help="Output file for summary report"),
):
    """Generate a comprehensive summary report of all changes."""
    console.print(f"[bold]Generating summary report[/bold] for {repo_path}")
    
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
    
    from tagi.config import Config
    config = Config(repo_path)
    
    # Build summary report
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("TAGI SUMMARY REPORT")
    report_lines.append("=" * 60)
    report_lines.append(f"Repository: {repo_path}")
    report_lines.append(f"Total files changed: {len(changes)}")
    report_lines.append("")
    
    # Overall statistics
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    avg_risk = sum(getattr(c, 'risk_score', 0) for c in changes) / len(changes)
    report_lines.append("OVERALL STATISTICS")
    report_lines.append("-" * 40)
    report_lines.append(f"Total lines changed: {total_lines}")
    report_lines.append(f"Average risk score: {avg_risk:.2f}")
    report_lines.append("")
    
    # Changes by type
    from collections import Counter
    from tagi.models.change import ChangeType
    by_type = Counter(c.change_type.value for c in changes)
    report_lines.append("CHANGES BY TYPE")
    report_lines.append("-" * 40)
    for ct, count in sorted(by_type.items()):
        report_lines.append(f"  {ct}: {count}")
    report_lines.append("")
    
    # Tag distribution
    tag_counts = Counter()
    for change in changes:
        for tag in change.tags:
            tag_counts[tag.value] += 1
    
    report_lines.append("TAG DISTRIBUTION")
    report_lines.append("-" * 40)
    for tag, count in tag_counts.most_common():
        desc = config.get_tag_description(tag)
        if desc:
            report_lines.append(f"  {tag} ({count}): {desc}")
        else:
            report_lines.append(f"  {tag}: {count}")
    report_lines.append("")
    
    # File list
    report_lines.append("FILES CHANGED")
    report_lines.append("-" * 40)
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        report_lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    report_lines.append("")
    report_lines.append("=" * 60)
    
    report_text = "\n".join(report_lines)
    
    if output:
        with open(output, "w") as f:
            f.write(report_text)
        console.print(f"[green]Summary report saved to {output}[/green]")
    else:
        console.print("\n" + report_text)


@app.command()
def draft(
    tag: str = typer.Argument(..., help="Tag to draft (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
):
    """Draft a commit message for a change group."""
    console.print(f"[bold]Drafting[/bold] {tag}")
    
    try:
        changes = scan_repo(repo_path)
        changes = apply_tags(changes, repo_path)
        groups = group_changes(changes)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)
    
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
    
    message = generate_commit_message(group, template=template)
    console.print("\n[bold cyan]Commit message draft:[/bold cyan]")
    console.print(message)


@app.command()
def send(
    tag: str = typer.Argument(..., help="Tag to send (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    push: bool = typer.Option(False, "--push", help="Push after commit"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
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
    message = generate_commit_message(group, template=template)
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
    message = generate_commit_message(group, template=template)
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


def _display_changes(changes, config=None):
    """Display changes in a table."""
    table = Table(title="Changes")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Tags")
    
    for change in changes:
        tags_str = _format_tags(change.tags, config)
        table.add_row(change.path, change.change_type.value, tags_str)
    
    console.print(table)


def _format_tags(tags, config=None):
    """Format tags with color coding."""
    from tagi.models.change import Tag
    
    tag_colors = {
        Tag.SMALL: "green",
        Tag.LARGE: "red",
        Tag.NEW: "blue",
        Tag.DEPS: "yellow",
        Tag.DOCS: "cyan",
        Tag.TESTS: "magenta",
        Tag.CONFIG: "bright_yellow",
        Tag.RISKY: "red",
        Tag.REFACTOR: "blue",
        Tag.FEATURE: "green",
    }
    
    formatted = []
    for tag in tags:
        # Check for custom color from config
        color = None
        if config:
            custom_color = config.get_tag_color(tag.value)
            if custom_color:
                color = custom_color
        
        # Fall back to default colors
        if color is None:
            color = tag_colors.get(tag, "white")
        
        formatted.append(f"[{color}]{tag.value}[/{color}]")
    
    return ", ".join(formatted)


def _display_groups(groups):
    """Display groups in a table."""
    table = Table(title="Change Groups")
    table.add_column("Group")
    table.add_column("Files", style="magenta")
    
    for group in groups:
        tags_str = _format_tags(group.tags)
        table.add_row(tags_str, str(len(group.changes)))
    
    console.print(table)


def _display_changes_grouped(changes):
    """Display changes grouped by tag."""
    from collections import defaultdict
    from tagi.models.change import Tag
    
    # Group by primary tag
    grouped = defaultdict(list)
    for change in changes:
        primary_tag = change.tags[0] if change.tags else Tag.SMALL
        grouped[primary_tag].append(change)
    
    # Display each group
    for tag in sorted(grouped.keys(), key=lambda t: t.value):
        tag_changes = grouped[tag]
        console.print(f"\n[bold]{_format_tags([tag])}[/bold] ({len(tag_changes)} files)")
        
        table = Table()
        table.add_column("File", style="cyan")
        table.add_column("Type", style="magenta")
        
        for change in tag_changes:
            table.add_row(change.path, change.change_type.value)
        
        console.print(table)


if __name__ == "__main__":
    app()
