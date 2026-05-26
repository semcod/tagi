"""Helper functions for publish command."""

from typing import List
from rich.console import Console
from tagi.models import Change, ChangeGroup, Tag
from tagi.providers.github import GitHubProvider
from tagi.providers.gitlab import GitLabProvider
from tagi.providers.detector import detect_provider


def detect_and_get_provider(repo_path: str):
    """Detect provider and return appropriate instance.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Provider instance or None
    """
    provider_type = detect_provider(repo_path)
    if provider_type == "github":
        return GitHubProvider(repo_path)
    elif provider_type == "gitlab":
        return GitLabProvider(repo_path)
    return None


def filter_changes_by_tag(changes: List[Change], tag: str) -> List[Change]:
    """Filter changes by tag.
    
    Args:
        changes: All changes
        tag: Tag to filter by (with # prefix)
        
    Returns:
        Filtered changes
    """
    tag_enum = Tag(tag)
    return [c for c in changes if tag_enum in c.tags]


def create_publish_group(changes: List[Change], tag: str) -> ChangeGroup:
    """Create a ChangeGroup for publishing.
    
    Args:
        changes: Changes to include
        tag: Tag name
        
    Returns:
        ChangeGroup instance
    """
    total_lines = sum(c.lines_changed for c in changes)
    avg_risk = sum(c.risk_score for c in changes) / len(changes) if changes else 0.0
    tag_enum = Tag(tag)
    
    return ChangeGroup(
        name=tag,
        changes=changes,
        tags=[tag_enum],
        total_lines=total_lines,
        avg_risk=avg_risk
    )
