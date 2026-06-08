"""Display utilities for CLI commands."""

from typing import Optional
from rich.console import Console
from rich.table import Table

from tagi.models.change import Change
from tagi.config import Config


console = Console()


def _display_changes(changes: list[Change], config: Optional[Config] = None) -> None:
    """Display changes in a simple list format."""
    if not changes:
        console.print("[yellow]No changes to display[/yellow]")
        return
    
    table = Table(title="Changes")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Tags", style="green")
    
    for change in changes:
        tags_str = ", ".join([tag.value for tag in change.tags]) if change.tags else "none"
        table.add_row(
            change.path,
            change.change_type.value,
            tags_str
        )
    
    console.print(table)


def _format_tags(tags: list[Change], config: Optional[Config] = None) -> str:
    """Format tags for display with descriptions if available."""
    if not tags:
        return "none"
    
    tag_strings = []
    for tag in tags:
        tag_str = tag.value
        if config:
            desc = config.get_tag_description(tag.value)
            if desc:
                tag_str += f" ({desc})"
        tag_strings.append(tag_str)
    
    return ", ".join(tag_strings)


def _display_groups(groups: dict[str, list[Change]]) -> None:
    """Display grouped changes."""
    if not groups:
        console.print("[yellow]No groups to display[/yellow]")
        return
    
    for tag, changes in groups.items():
        console.print(f"\n[bold cyan]{tag}[/bold cyan] ({len(changes)} changes)")
        for change in changes:
            tags_str = _format_tags(change.tags)
            console.print(f"  • {change.path} [{change.change_type.value}] {tags_str}")


def _display_changes_grouped(changes: list[Change]) -> None:
    """Display changes grouped by tag."""
    if not changes:
        console.print("[yellow]No changes to display[/yellow]")
        return
    
    # Group changes by their primary tag
    groups = {}
    for change in changes:
        if change.tags:
            primary_tag = change.tags[0].value
            if primary_tag not in groups:
                groups[primary_tag] = []
            groups[primary_tag].append(change)
    
    _display_groups(groups)
