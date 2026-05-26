"""Helper functions for summary command."""

from typing import List
from collections import Counter
from tagi.models import Change, ChangeType
from tagi.config import Config


def build_report_header(repo_path: str, changes: List[Change]) -> List[str]:
    """Build report header section.
    
    Args:
        repo_path: Repository path
        changes: All changes
        
    Returns:
        List of header lines
    """
    lines = []
    lines.append("=" * 60)
    lines.append("TAGI SUMMARY REPORT")
    lines.append("=" * 60)
    lines.append(f"Repository: {repo_path}")
    lines.append(f"Total files changed: {len(changes)}")
    lines.append("")
    return lines


def build_statistics_section(changes: List[Change]) -> List[str]:
    """Build overall statistics section.
    
    Args:
        changes: All changes
        
    Returns:
        List of statistics lines
    """
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    avg_risk = sum(getattr(c, 'risk_score', 0) for c in changes) / len(changes) if changes else 0.0
    
    lines = []
    lines.append("OVERALL STATISTICS")
    lines.append("-" * 40)
    lines.append(f"Total lines changed: {total_lines}")
    lines.append(f"Average risk score: {avg_risk:.2f}")
    lines.append("")
    return lines


def build_changes_by_type_section(changes: List[Change]) -> List[str]:
    """Build changes by type section.
    
    Args:
        changes: All changes
        
    Returns:
        List of type distribution lines
    """
    by_type = Counter(c.change_type.value for c in changes)
    
    lines = []
    lines.append("CHANGES BY TYPE")
    lines.append("-" * 40)
    for ct, count in sorted(by_type.items()):
        lines.append(f"  {ct}: {count}")
    lines.append("")
    return lines


def build_tag_distribution_section(changes: List[Change], config: Config) -> List[str]:
    """Build tag distribution section.
    
    Args:
        changes: All changes
        config: Configuration instance
        
    Returns:
        List of tag distribution lines
    """
    tag_counts = Counter()
    for change in changes:
        for tag in change.tags:
            tag_counts[tag.value] += 1
    
    lines = []
    lines.append("TAG DISTRIBUTION")
    lines.append("-" * 40)
    for tag, count in tag_counts.most_common():
        desc = config.get_tag_description(tag)
        if desc:
            lines.append(f"  {tag} ({count}): {desc}")
        else:
            lines.append(f"  {tag}: {count}")
    lines.append("")
    return lines


def build_file_list_section(changes: List[Change]) -> List[str]:
    """Build file list section.
    
    Args:
        changes: All changes
        
    Returns:
        List of file lines
    """
    lines = []
    lines.append("FILES CHANGED")
    lines.append("-" * 40)
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    return lines
