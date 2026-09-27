"""Utility CLI commands: summary, draft."""

from typing import Optional
import typer
from rich.console import Console
from pathlib import Path

from tagi.composer.commit_message import generate_commit_message
from tagi.utils.send_helpers import create_change_group
from tagi.utils.inspect_helpers import count_changes_by_tag, resolve_filtered_changes
from tagi.cli.display_utils import _format_tags
from tagi.cli.scan_utils import scan_and_tag
from tagi.cli.tag_targets import _ensure_tag_prefix


console = Console()


def _summary_overview_lines(repo_path: str, all_changes) -> list:
    """Report header plus the per-tag change counts section."""
    tag_stats = count_changes_by_tag(all_changes)
    return [
        "# Change Summary Report",
        f"Repository: {Path(repo_path).absolute()}",
        f"Total changes: {len(all_changes)}",
        "",
        "## Changes by Tag",
        *(f"- {tag}: {count} change(s)" for tag, count in tag_stats.items() if count > 0),
        "",
    ]


def _describe_change(change) -> list:
    """Summary block for a single change."""
    description = getattr(change, "description", None)
    lines = [
        f"- **{change.path}** [{change.change_type.value}]",
        f"  Tags: {_format_tags(change.tags)}",
    ]
    if description:
        lines.append(f"  Description: {description}")
    lines.append("")
    return lines


def _detailed_change_lines(all_changes) -> list:
    """Detailed per-change listing section."""
    lines = ["## Detailed Changes"]
    for change in all_changes:
        lines.extend(_describe_change(change))
    return lines


def _write_summary(output: Optional[str], summary_content: str) -> None:
    """Save the report to ``output`` or print it to the console."""
    if output:
        output_path = Path(output)
        output_path.write_text(summary_content)
        console.print(f"[green]✓ Summary saved to:[/green] {output_path}")
    else:
        console.print(summary_content)


def summary_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for summary report"),
):
    """Generate a comprehensive summary report of all changes."""
    console.print(f"[bold]Generating summary[/bold] for {repo_path}")

    all_changes = scan_and_tag(repo_path)

    if not all_changes:
        console.print("[yellow]No changes found[/yellow]")
        return

    summary_lines = [
        *_summary_overview_lines(repo_path, all_changes),
        *_detailed_change_lines(all_changes),
    ]
    _write_summary(output, "\n".join(summary_lines))


def init_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
):
    """Initialize tagi configuration in the repository."""
    import shutil
    
    repo = Path(repo_path).resolve()
    config_path = repo / "tagi.toml"
    
    if config_path.exists() and not force:
        console.print(f"[yellow]tagi.toml already exists at {config_path}[/yellow]")
        console.print("[dim]Use --force to overwrite[/dim]")
        return
    
    # Find example config
    example_paths = [
        Path(__file__).parents[3] / "tagi.toml.example",
        Path(__file__).parents[3] / "tagi.toml",
    ]
    
    example_found = False
    for example_path in example_paths:
        if example_path.exists():
            shutil.copy(example_path, config_path)
            example_found = True
            break
    
    if not example_found:
        # Create minimal default config
        config_path.write_text("""# tagi configuration
[tags]
frontend = ["frontend/", "client/", "web/", "ui/"]
backend = ["backend/", "server/", "api/"]

[rules]
"frontend/" = "#frontend"
"backend/" = "#backend"

[colors]
"#frontend" = "blue"
"#backend" = "green"
"#risky" = "red"
"#small" = "cyan"
"#docs" = "yellow"
"#tests" = "magenta"
"#config" = "bright_yellow"
"#deps" = "bright_red"

[ignore]
["node_modules/", ".git/", "__pycache__/", "*.pyc", ".idea/", ".vscode/", ".venv/", "venv/"]
""")
    
    console.print(f"[green]✓ Created tagi.toml at {config_path}[/green]")


def _hooks_list(repo: Path) -> None:
    """Print the hooks currently installed in the repository."""
    from tagi.hooks import list_hooks as tagi_list_hooks

    hooks = tagi_list_hooks(str(repo))
    if hooks:
        console.print("[bold]Installed hooks:[/bold]")
        for hook in hooks:
            marker = "[green]✓[/green]" if "tagi" in hook else "[dim]•[/dim]"
            console.print(f"  {marker} {hook}")
    else:
        console.print("[dim]No hooks installed[/dim]")


def _hooks_install(repo: Path) -> None:
    """Install tagi git hooks or exit with an error."""
    from tagi.hooks import install_hooks as tagi_install_hooks

    if tagi_install_hooks(str(repo)):
        console.print(f"[green]✓ Installed tagi hooks in {repo}/.git/hooks[/green]")
    else:
        console.print("[red]Failed to install hooks[/red]")
        raise typer.Exit(1)


def _hooks_uninstall(repo: Path) -> None:
    """Remove tagi git hooks or exit with an error."""
    from tagi.hooks import uninstall_hooks as tagi_uninstall_hooks

    if tagi_uninstall_hooks(str(repo)):
        console.print(f"[green]✓ Removed tagi hooks from {repo}/.git/hooks[/green]")
    else:
        console.print("[red]Failed to uninstall hooks[/red]")
        raise typer.Exit(1)


def _hooks_status(repo: Path) -> None:
    """Report whether tagi hooks are installed."""
    from tagi.hooks import check_hooks_installed

    if check_hooks_installed(str(repo)):
        console.print(f"[green]✓ tagi hooks are installed in {repo}[/green]")
    else:
        console.print(f"[yellow]✗ tagi hooks are not installed in {repo}[/yellow]")
        console.print("[dim]Run: tagi hooks --install[/dim]")


def hooks_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    install: bool = typer.Option(False, "--install", "-i", help="Install git hooks"),
    uninstall: bool = typer.Option(False, "--uninstall", "-u", help="Remove git hooks"),
    list_hooks: bool = typer.Option(False, "--list", "-l", help="List installed hooks"),
):
    """Manage git hooks integration for tagi."""
    repo = Path(repo_path).resolve()

    if list_hooks:
        _hooks_list(repo)
    elif install:
        _hooks_install(repo)
    elif uninstall:
        _hooks_uninstall(repo)
    else:
        # Default: show status
        _hooks_status(repo)


def draft_command(
    tag: str = typer.Argument(..., help="Tag to draft (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
):
    """Draft a commit message for a change group."""
    console.print(f"[bold]Drafting[/bold] commit message for {tag}")
    
    tagged_changes = scan_and_tag(repo_path)
    normalized_tag = _ensure_tag_prefix(tag)
    try:
        draft_changes = resolve_filtered_changes(tagged_changes, normalized_tag)
    except ValueError:
        console.print(f"[red]Unknown tag: {normalized_tag}[/red]")
        raise typer.Exit(1)
    
    if not draft_changes:
        console.print(f"[yellow]No changes found for {normalized_tag}[/yellow]")
        return
    
    # Create change group
    group = create_change_group(draft_changes, normalized_tag)
    
    # Generate commit message
    commit_message = generate_commit_message(
        group.changes, template=template, repo_path=repo_path
    )
    
    console.print("\n[bold cyan]Draft commit message:[/bold cyan]")
    console.print(commit_message)
    
    console.print(f"\n[dim]Changes included: {len(draft_changes)}[/dim]")
    for change in draft_changes:
        console.print(f"  • {change.path}")
