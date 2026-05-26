"""CLI interface for tagi."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from tagi.composer.commit_message import generate_commit_message
from tagi.executor.git import GitExecutor
from tagi.executor.publish import PublishExecutor
from tagi.heuristics.tags import apply_tags
from tagi.heuristics.scoring import calculate_risk_score
from tagi.models.change import ChangeType, Tag
from tagi.planner.grouper import group_changes
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider
from tagi.providers.koru import KoruProvider
from tagi.scanner.status import scan_repo
from tagi.scanner.diff import get_diff
from tagi.utils.logger import setup_logger
from tagi.planner.sorter import sort_by_complexity
from tagi.utils.detect_provider import detect_git_provider
from tagi.utils.send_helpers import resolve_filtered_changes, create_change_group
from tagi.utils.publish_helpers import filter_changes_by_tag, create_publish_group
from tagi.utils.inspect_helpers import filter_changes_by_tag as inspect_filter_by_tag, calculate_tag_statistics, display_statistics_table, filter_changes_by_tags_any, filter_changes_by_tags_all

app = typer.Typer(help="tagi - Git change orchestrator")
console = Console()
logger = None


@app.callback()
def setup_logging(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging", is_eager=True)):
    """Set up logging for all commands."""
    global logger
    logger = setup_logger(verbose=verbose)
    if verbose and logger:
        logger.debug("Verbose logging enabled")


def _configure_command_logging(verbose: bool) -> None:
    """Enable verbose logging for a single command invocation."""
    global logger
    if verbose:
        logger = setup_logger(verbose=True)
        logger.debug("Verbose logging enabled")


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag has # prefix."""
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

    if repo_path != ".":
        return repo_path, target

    if _is_known_tag(target):
        return repo_path, target

    candidate = Path(target).expanduser()
    if candidate.exists():
        return str(candidate), None

    return repo_path, target


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
    _do_list_groups(repo_path)


@app.command("list")
def list_cmd(
    repo_path: str = typer.Argument(".", help="Path to repository"),
):
    """List available change groups (alias for list-groups)."""
    _do_list_groups(repo_path)


def _do_list_groups(repo_path: str) -> None:
    """Shared implementation for list and list-groups commands."""
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
    
    # Add # prefix if not present
    if not tag.startswith("#"):
        tag = f"#{tag}"
    
    # Filter changes by tag
    filtered_changes = inspect_filter_by_tag(changes, tag)
    
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
    tag_list = [t if t.startswith("#") else f"#{t}" for t in tag_list]
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
        filtered_changes = filter_changes_by_tags_all(changes, tag_list)
        console.print(f"[dim]Mode: Match ALL tags[/dim]")
    else:
        filtered_changes = filter_changes_by_tags_any(changes, tag_list)
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
    report_lines = build_report_header(repo_path, changes)
    report_lines.extend(build_statistics_section(changes))
    report_lines.extend(build_changes_by_type_section(changes))
    report_lines.extend(build_tag_distribution_section(changes, config))
    report_lines.extend(build_file_list_section(changes))
    
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
    
    # Add # prefix if not present
    if not tag.startswith("#"):
        tag = f"#{tag}"
    
    # Collect all changes with this tag
    tag_enum = Tag(tag)
    filtered_changes = [c for c in changes if tag_enum in c.tags]
    
    if not filtered_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    # Create a temporary group for the filtered changes
    from tagi.models import ChangeGroup
    total_lines = sum(c.lines_changed for c in filtered_changes)
    avg_risk = sum(c.risk_score for c in filtered_changes) / len(filtered_changes) if filtered_changes else 0.0
    group = ChangeGroup(
        name=tag,
        changes=filtered_changes,
        tags=[tag_enum],
        total_lines=total_lines,
        avg_risk=avg_risk
    )
    
    message = generate_commit_message(group.changes, template=template, repo_path=repo_path)
    console.print("\n[bold cyan]Commit message draft:[/bold cyan]")
    console.print(message)


@app.command()
def send(
    target: Optional[str] = typer.Argument(None, help="Tag to send (e.g., small) or repository path. If not specified, sends all changes"),
    repo_path: str = typer.Option(".", "--repo-path", "--path", help="Path to repository"),
    auto_order: bool = typer.Option(False, "--auto-order", "-a", help="Automatically order changes by complexity (simplest first)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    push: bool = typer.Option(False, "--push", help="Push after commit"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Stage, commit, and optionally push changes."""
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

    if auto_order:
        console.print("[bold]Sorting changes by complexity (simplest first)[/bold]")
        filtered_changes = sort_by_complexity(filtered_changes)
    
    if not filtered_changes:
        if tag is None:
            console.print("[yellow]No changes found[/yellow]")
        else:
            console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return
    
    # Create a temporary group for the filtered changes
    from tagi.models import ChangeGroup
    total_lines = sum(c.lines_changed for c in filtered_changes)
    avg_risk = sum(c.risk_score for c in filtered_changes) / len(filtered_changes) if filtered_changes else 0.0
    
    if tag is None:
        group_name = "all"
        group_tags = []
    else:
        group_name = tag
        tag_enum = Tag(tag)
        group_tags = [tag_enum]
    
    group = ChangeGroup(
        name=group_name,
        changes=filtered_changes,
        tags=group_tags,
        total_lines=total_lines,
        avg_risk=avg_risk
    )

    # Generate commit message
    message = generate_commit_message(group.changes, template=template, repo_path=repo_path)
    console.print("\n[bold cyan]Commit message:[/bold cyan]")
    console.print(message)
    
    if dry_run:
        console.print("\n[yellow][DRY-RUN] No changes will be made[/yellow]")
        return
    # Stage and commit changes
    executor = PublishExecutor(repo_path)
    files = [c.path for c in group.changes]
    
    try:
        if not executor.stage_and_commit(files, message):
            console.print("[red]Error staging and committing changes[/red]")
            raise typer.Exit(1)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    
    console.print("[green]✓ Changes committed[/green]")
    
    # Push if requested
    if push:
        console.print("[bold]Pushing[/bold]...")
        if not executor.git.push():
            console.print("[yellow]Push failed, but changes are committed[/yellow]")
        else:
            console.print("[green]✓ Changes pushed[/green]")


@app.command()
def auto(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Automatically scan and send all changes with auto-order and push."""
    _configure_command_logging(verbose)

    console.print("[bold]Auto mode:[/bold] Scanning and sending all changes")
    
    # First scan
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
    
    # Display scan results
    console.print(f"[green]✓ Found {len(changes)} changes[/green]")
    
    # Sort by complexity and send with push
    filtered_changes = sort_by_complexity(changes)
    console.print("[bold]Sorting changes by complexity (simplest first)[/bold]")
    
    # Create group for all changes
    from tagi.models import ChangeGroup
    total_lines = sum(c.lines_changed for c in filtered_changes)
    avg_risk = sum(c.risk_score for c in filtered_changes) / len(filtered_changes) if filtered_changes else 0.0
    
    group = ChangeGroup(
        name="all",
        changes=filtered_changes,
        tags=[],
        total_lines=total_lines,
        avg_risk=avg_risk
    )

    # Generate commit message
    message = generate_commit_message(group.changes, template=template, repo_path=repo_path)
    console.print("\n[bold cyan]Commit message:[/bold cyan]")
    console.print(message)
    
    if dry_run:
        console.print("\n[yellow][DRY-RUN] No changes will be made[/yellow]")
        return
    
    # Stage and commit changes
    executor = PublishExecutor(repo_path)
    files = [c.path for c in group.changes]
    
    try:
        if not executor.stage_and_commit(files, message):
            console.print("[red]Error staging and committing changes[/red]")
            raise typer.Exit(1)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    
    console.print("[green]✓ Changes committed[/green]")
    
    # Push changes
    console.print("[bold]Pushing[/bold]...")
    if not executor.git.push():
        console.print("[yellow]Push failed, but changes are committed[/yellow]")
    else:
        console.print("[green]✓ Changes pushed[/green]")


@app.command()
def deploy(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview deployment without executing"),
    koru_host: str = typer.Option("127.0.0.1", "--koru-host", help="Koru API host"),
    koru_port: int = typer.Option(8790, "--koru-port", help="Koru API port"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Deploy changes using Koru API for priority analysis."""
    _configure_command_logging(verbose)

    console.print("[bold]Deploy mode:[/bold] Analyzing deployment priority with Koru")
    
    # Initialize Koru provider
    koru = KoruProvider(Path(repo_path), koru_host, koru_port)
    
    if not koru.is_available():
        console.print("[red]Koru API is not available[/red]")
        console.print(f"Make sure Koru is running on {koru_host}:{koru_port}")
        raise typer.Exit(1)
    
    # Scan changes
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
    
    console.print(f"[green]✓ Found {len(changes)} changes[/green]")
    
    # Analyze deployment priority with Koru
    deployment_plan = koru.analyze_deployment_priority(changes)
    
    console.print("\n[bold cyan]Deployment Priority Analysis:[/bold cyan]")
    console.print(f"Priority order: {' → '.join(deployment_plan.priority_order)}")
    
    console.print("\n[bold cyan]Deployment Groups:[/bold cyan]")
    for group in deployment_plan.deployment_groups:
        console.print(f"\n[yellow]{group['name'].upper()}[/yellow] (Priority: {group['priority']})")
        console.print(f"Reason: {group['reason']}")
        console.print(f"Files: {', '.join(group['changes'])}")
        if group['name'] in deployment_plan.risk_assessment:
            console.print(f"Risk score: {deployment_plan.risk_assessment[group['name']]:.2f}")
    
    console.print("\n[bold cyan]Recommendations:[/bold cyan]")
    for rec in deployment_plan.recommendations:
        console.print(f"• {rec}")
    
    if dry_run:
        console.print("\n[yellow][DRY-RUN] No deployment actions will be taken[/yellow]")
        return
    
    # Ask for confirmation
    if not typer.confirm("\nProceed with deployment according to priority order?"):
        console.print("[yellow]Deployment cancelled[/yellow]")
        return
    
    # Deploy groups in priority order
    console.print("\n[bold]Starting deployment...[/bold]")
    
    for group_name in deployment_plan.priority_order:
        group = next((g for g in deployment_plan.deployment_groups if g['name'] == group_name), None)
        if not group:
            continue
        
        console.print(f"\n[yellow]Deploying {group_name}...[/yellow]")
        
        # Get changes for this group
        group_changes = [c for c in changes if c.path in group['changes']]
        
        # Deploy using Koru
        success = koru.deploy_group(group_name, group_changes, dry_run=False)
        
        if success:
            console.print(f"[green]✓ {group_name} deployed successfully[/green]")
        else:
            console.print(f"[red]✗ {group_name} deployment failed[/red]")
            if not typer.confirm(f"Continue with next group?"):
                break
    
    console.print("\n[green]Deployment completed[/green]")


@app.command()
def publish(
    tag: str = typer.Argument(..., help="Tag to publish (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Create a PR or MR for the changes."""
    _configure_command_logging(verbose)

    console.print(f"[bold]Publishing[/bold] {tag}")

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
    group = create_publish_group(filtered_changes, tag)
    
    # Detect provider
    provider = detect_provider(repo_path)
    if not provider:
        console.print("[yellow]Could not detect GitHub or GitLab provider[/yellow]")
        console.print("[yellow]Please ensure you have a remote configured[/yellow]")
        return
    
    console.print(f"[bold]Detected provider:[/bold] {provider}")
    
    # Generate commit message
    message = generate_commit_message(group.changes, template=template, repo_path=repo_path)
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


def detect_provider(repo_path: str = ".") -> str:
    """Detect the Git hosting provider from remotes."""
    github = GitHubProvider(repo_path)
    gitlab = GitLabProvider(repo_path)
    if github.detect_remote():
        return "github"
    if gitlab.detect_remote():
        return "gitlab"
    return ""


def create_pr(title: str, body: str, repo_path: str = ".") -> bool:
    """Create a pull request using GitHub CLI."""
    provider = GitHubProvider(repo_path)
    executor = GitExecutor(repo_path)
    branch = executor.get_current_branch()
    try:
        result = provider.create_pr(title, body, branch)
        return bool(result)
    except RuntimeError:
        return False


def create_mr(title: str, body: str, repo_path: str = ".") -> bool:
    """Create a merge request using GitLab CLI."""
    provider = GitLabProvider(repo_path)
    executor = GitExecutor(repo_path)
    branch = executor.get_current_branch()
    try:
        result = provider.create_pr(title, body, branch)
        return bool(result)
    except RuntimeError:
        return False


if __name__ == "__main__":
    app()
