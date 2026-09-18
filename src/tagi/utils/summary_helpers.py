"""Helper functions for summary command."""

from typing import List
from collections import Counter
from tagi.models import Change, ChangeType
from tagi.config import Config
from tagi.utils.line_builder import LineBuilder
from tagi.utils.risk import average_risk


def build_report_header(repo_path: str, changes: List[Change]) -> List[str]:
    """Build report header section.
    
    Args:
        repo_path: Repository path
        changes: All changes
        
    Returns:
        List of header lines
    """
    builder = LineBuilder()
    builder.add("=" * 60)
    builder.add("TAGI SUMMARY REPORT")
    builder.add("=" * 60)
    builder.add(f"Repository: {repo_path}")
    builder.add(f"Total files changed: {len(changes)}")
    builder.add("")
    return builder.as_list()


def build_statistics_section(changes: List[Change]) -> List[str]:
    """Build overall statistics section.
    
    Args:
        changes: All changes
        
    Returns:
        List of statistics lines
    """
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)
    avg_risk = average_risk(changes)
    
    builder = LineBuilder()
    builder.add("OVERALL STATISTICS")
    builder.add("-" * 40)
    builder.add(f"Total lines changed: {total_lines}")
    builder.add(f"Average risk score: {avg_risk:.2f}")
    builder.add("")
    return builder.as_list()


def build_changes_by_type_section(changes: List[Change]) -> List[str]:
    """Build changes by type section.
    
    Args:
        changes: All changes
        
    Returns:
        List of type distribution lines
    """
    by_type = Counter(c.change_type.value for c in changes)
    
    builder = LineBuilder()
    builder.add("CHANGES BY TYPE")
    builder.add("-" * 40)
    for ct, count in sorted(by_type.items()):
        builder.add(f"  {ct}: {count}")
    builder.add("")
    return builder.as_list()


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
    
    builder = LineBuilder()
    builder.add("TAG DISTRIBUTION")
    builder.add("-" * 40)
    for tag, count in tag_counts.most_common():
        desc = config.get_tag_description(tag)
        if desc:
            builder.add(f"  {tag} ({count}): {desc}")
        else:
            builder.add(f"  {tag}: {count}")
    builder.add("")
    return builder.as_list()


def build_file_list_section(changes: List[Change]) -> List[str]:
    """Build file list section.
    
    Args:
        changes: All changes
        
    Returns:
        List of file lines
    """
    builder = LineBuilder()
    builder.add("FILES CHANGED")
    builder.add("-" * 40)
    for change in changes:
        tags_str = ", ".join([t.value for t in change.tags])
        builder.add(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    return builder.as_list()
