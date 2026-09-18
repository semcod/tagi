"""Summary module for generating change summaries."""

from typing import List

from tagi.models import Change
from tagi.utils.line_builder import LineBuilder


def generate_summary(changes: List[Change]) -> str:
    """Generate a summary of changes."""
    if not changes:
        return "No changes"
    
    total_lines = sum(c.lines_changed for c in changes)
    avg_risk = sum(c.risk_score for c in changes) / len(changes) if changes else 0.0
    
    builder = LineBuilder()
    builder.add(f"Summary: {len(changes)} files, {total_lines} lines changed")
    builder.add(f"Average risk score: {avg_risk:.2f}")
    
    # Add risk breakdown
    low_risk = sum(1 for c in changes if c.risk_score < 0.3)
    medium_risk = sum(1 for c in changes if 0.3 <= c.risk_score < 0.7)
    high_risk = sum(1 for c in changes if c.risk_score >= 0.7)
    
    builder.add(f"Risk breakdown: {low_risk} low, {medium_risk} medium, {high_risk} high")
    
    return builder.text()


def generate_file_list(changes: List[Change], max_files: int = 20) -> str:
    """Generate a formatted list of files."""
    if not changes:
        return "No files"
    
    builder = LineBuilder()
    display_changes = changes[:max_files]
    
    for change in display_changes:
        tags_str = ", ".join([t.value for t in change.tags])
        builder.add(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    if len(changes) > max_files:
        builder.add(f"  ... and {len(changes) - max_files} more files")
    
    return builder.text()
