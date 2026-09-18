"""Publishing CLI commands: publish, deploy."""

import typer
from rich.console import Console

from tagi.executor.publish import PublishExecutor
from tagi.utils.inspect_helpers import resolve_filtered_changes
from tagi.utils.publish_helpers import create_publish_group
from tagi.utils.detect_provider import detect_git_provider


console = Console()


def _ensure_tag_prefix(tag: str) -> str:
    """Ensure tag starts with #."""
    if not tag.startswith("#"):
        return f"#{tag}"
    return tag


def publish_command(
    tag: str = typer.Argument(..., help="Tag to publish (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    template: str = typer.Option("default", "--template", "-t", help="Commit message template (default, conventional, detailed)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Create a PR or MR for the changes."""
    import tagi.cli as _cli
    _cli._configure_command_logging(verbose)

    console.print(f"[bold]Publishing[/bold] {tag}")

    try:
        changes = _cli.scan_repo(repo_path)
        changes = _cli.apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)

    tag = _ensure_tag_prefix(tag)
    try:
        publish_changes = resolve_filtered_changes(changes, tag)
    except ValueError:
        console.print(f"[red]Unknown tag: {tag}[/red]")
        raise typer.Exit(1)

    if not publish_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return

    # Create change group
    group = create_publish_group(publish_changes, tag)
    
    # Detect provider
    provider = detect_git_provider(repo_path)
    if not provider:
        console.print("[yellow]Could not detect GitHub or GitLab provider[/yellow]")
        console.print("[yellow]Please ensure you have a remote configured[/yellow]")
        return
    
    console.print(f"[bold]Detected provider:[/bold] {provider}")
    
    if dry_run:
        console.print("\n[bold cyan]Dry run - would create PR/MR with:[/bold cyan]")
        console.print(f"  Tag: {tag}")
        console.print(f"  Changes: {len(publish_changes)}")
        for change in publish_changes:
            console.print(f"    • {change.path}")
        return

    # Create PR/MR
    try:
        publish_executor = PublishExecutor(repo_path)
        
        if provider == "github":
            pr_url = publish_executor.create_github_pr(group, template=template)
            if pr_url:
                console.print(f"[green]✓ Pull request created:[/green] {pr_url}")
            else:
                console.print("[red]Failed to create pull request[/red]")
                raise typer.Exit(1)
                
        elif provider == "gitlab":
            mr_url = publish_executor.create_gitlab_mr(group, template=template)
            if mr_url:
                console.print(f"[green]✓ Merge request created:[/green] {mr_url}")
            else:
                console.print("[red]Failed to create merge request[/red]")
                raise typer.Exit(1)
        else:
            console.print(f"[red]Unsupported provider: {provider}[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Error during publish: {e}[/red]")
        raise typer.Exit(1)


def deploy_command(
    tag: str = typer.Argument(..., help="Tag to deploy (e.g., #small)"),
    repo_path: str = typer.Argument(".", help="Path to repository"),
    environment: str = typer.Option("staging", "--env", "-e", help="Target environment (staging, production)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without executing"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """Deploy changes to target environment."""
    import tagi.cli as _cli
    _cli._configure_command_logging(verbose)

    console.print(f"[bold]Deploying[/bold] {tag} to {environment}")

    try:
        changes = _cli.scan_repo(repo_path)
        changes = _cli.apply_tags(changes, repo_path)
    except (ValueError, RuntimeError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)

    tag = _ensure_tag_prefix(tag)
    try:
        deploy_changes = resolve_filtered_changes(changes, tag)
    except ValueError:
        console.print(f"[red]Unknown tag: {tag}[/red]")
        raise typer.Exit(1)

    if not deploy_changes:
        console.print(f"[yellow]No changes found for {tag}[/yellow]")
        return

    if dry_run:
        console.print("\n[bold cyan]Dry run - would deploy:[/bold cyan]")
        console.print(f"  Tag: {tag}")
        console.print(f"  Environment: {environment}")
        console.print(f"  Changes: {len(deploy_changes)}")
        for change in deploy_changes:
            console.print(f"    • {change.path}")
        return

    # For now, deploy is a placeholder that would integrate with deployment systems
    console.print("[yellow]Deploy functionality is not yet implemented[/yellow]")
    console.print(f"[yellow]Would deploy {len(deploy_changes)} changes to {environment}[/yellow]")
    
    # TODO: Implement actual deployment logic
    # This could integrate with:
    # - CI/CD pipelines
    # - Kubernetes deployments
    # - Cloud provider deployment APIs
    # - Custom deployment scripts
