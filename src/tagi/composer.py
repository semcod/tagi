"""Composer module for generating commit messages."""

from typing import List

from tagi.models import Change, ChangeGroup, ChangeType, Tag


def generate_commit_message(group: ChangeGroup) -> str:
    """Generate a commit message for a change group."""
    # Count changes by type
    added = sum(1 for c in group.changes if c.change_type == ChangeType.ADDED)
    modified = sum(1 for c in group.changes if c.change_type == ChangeType.MODIFIED)
    deleted = sum(1 for c in group.changes if c.change_type == ChangeType.DELETED)
    
    # Build title based on dominant tag
    main_tag = group.tags[0] if group.tags else Tag.SMALL
    title = _build_title(main_tag, len(group.changes))
    
    # Build body
    body_parts = []
    body_parts.append(f"Changes: {len(group.changes)} files")
    
    if added:
        body_parts.append(f"  - Added: {added}")
    if modified:
        body_parts.append(f"  - Modified: {modified}")
    if deleted:
        body_parts.append(f"  - Deleted: {deleted}")
    
    body_parts.append(f"\nTags: {', '.join(t.value for t in group.tags)}")
    
    # List affected files (limit to 10)
    files = group.changes[:10]
    body_parts.append("\nFiles:")
    for change in files:
        body_parts.append(f"  - {change.path}")
    
    if len(group.changes) > 10:
        body_parts.append(f"  ... and {len(group.changes) - 10} more")
    
    return f"{title}\n\n" + "\n".join(body_parts)


def _build_title(tag: Tag, count: int) -> str:
    """Build commit message title based on tag."""
    titles = {
        Tag.SMALL: f"Small changes ({count} files)",
        Tag.LARGE: f"Large changes ({count} files)",
        Tag.NEW: f"Add new files ({count} files)",
        Tag.DEPS: f"Update dependencies ({count} files)",
        Tag.DOCS: f"Update documentation ({count} files)",
        Tag.TESTS: f"Update tests ({count} files)",
        Tag.CONFIG: f"Update configuration ({count} files)",
        Tag.RISKY: f"Risky changes ({count} files)",
        Tag.REFACTOR: f"Refactor code ({count} files)",
        Tag.FEATURE: f"Add features ({count} files)",
    }
    return titles.get(tag, f"Changes ({count} files)")
