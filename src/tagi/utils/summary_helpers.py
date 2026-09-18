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
    return LineBuilder([
        "=" * 60,
        "TAGI SUMMARY REPORT",
        "=" * 60,
        f"Repository: {repo_path}",
        f"Total files changed: {len(changes)}",
        "",
    ]).as_list()


def build_statistics_section(changes: List[Change]) -> List[str]:
    """Build overall statistics section.
    
    Args:
        changes: All changes
        
    Returns:
        List of statistics lines
    """
    total_lines = sum(getattr(c, 'lines_changed', 0) for c in changes)

    return LineBuilder([
        "OVERALL STATISTICS",
        "-" * 40,
        f"Total lines changed: {total_lines}",
        f"Average risk score: {average_risk(changes):.2f}",
        "",
    ]).as_list()


def build_changes_by_type_section(changes: List[Change]) -> List[str]:
    """Build changes by type section.
    
    Args:
        changes: All changes
        
    Returns:
        List of type distribution lines
    """
    by_type = Counter(c.change_type.value for c in changes)

    return LineBuilder([
        "CHANGES BY TYPE",
        "-" * 40,
        *(f"  {ct}: {count}" for ct, count in sorted(by_type.items())),
        "",
    ]).as_list()


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

    return LineBuilder([
        "TAG DISTRIBUTION",
        "-" * 40,
        *(
            f"  {tag} ({count}): {desc}"
            if (desc := config.get_tag_description(tag))
            else f"  {tag}: {count}"
            for tag, count in tag_counts.most_common()
        ),
        "",
    ]).as_list()


def build_file_list_section(changes: List[Change]) -> List[str]:
    """Build file list section.
    
    Args:
        changes: All changes
        
    Returns:
        List of file lines
    """
    return LineBuilder([
        "FILES CHANGED",
        "-" * 40,
        *(
            f"  [{change.change_type.value:8}] {change.path:40} "
            f"({', '.join(t.value for t in change.tags)})"
            for change in changes
        ),
    ]).as_list()
