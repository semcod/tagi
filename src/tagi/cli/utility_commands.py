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


def hooks_command(
    repo_path: str = typer.Argument(".", help="Path to repository"),
    install: bool = typer.Option(False, "--install", "-i", help="Install git hooks"),
    uninstall: bool = typer.Option(False, "--uninstall", "-u", help="Remove git hooks"),
    list_hooks: bool = typer.Option(False, "--list", "-l", help="List installed hooks"),
):
    """Manage git hooks integration for tagi."""
    from tagi.hooks import install_hooks as tagi_install_hooks
    from tagi.hooks import uninstall_hooks as tagi_uninstall_hooks
    from tagi.hooks import check_hooks_installed, list_hooks as tagi_list_hooks
    
    repo = Path(repo_path).resolve()
    
    if list_hooks:
        hooks = tagi_list_hooks(str(repo))
        if hooks:
            console.print("[bold]Installed hooks:[/bold]")
            for hook in hooks:
                marker = "[green]✓[/green]" if "tagi" in hook else "[dim]•[/dim]"
                console.print(f"  {marker} {hook}")
        else:
            console.print("[dim]No hooks installed[/dim]")
        return
    
    if install:
        if tagi_install_hooks(str(repo)):
            console.print(f"[green]✓ Installed tagi hooks in {repo}/.git/hooks[/green]")
        else:
            console.print("[red]Failed to install hooks[/red]")
            raise typer.Exit(1)
        return
    
    if uninstall:
        if tagi_uninstall_hooks(str(repo)):
            console.print(f"[green]✓ Removed tagi hooks from {repo}/.git/hooks[/green]")
        else:
            console.print("[red]Failed to uninstall hooks[/red]")
            raise typer.Exit(1)
        return
    
    # Default: show status
    installed = check_hooks_installed(str(repo))
    if installed:
        console.print(f"[green]✓ tagi hooks are installed in {repo}[/green]")
    else:
        console.print(f"[yellow]✗ tagi hooks are not installed in {repo}[/yellow]")
        console.print("[dim]Run: tagi hooks --install[/dim]")


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
        Tag(tag)  # validate that the tag is recognized
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
