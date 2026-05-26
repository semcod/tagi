"""Summary module for generating change summaries."""

from typing import List

from tagi.models import Change


def generate_summary(changes: List[Change]) -> str:
    """Generate a summary of changes."""
    if not changes:
        return "No changes"
    
    total_lines = sum(c.lines_changed for c in changes)
    avg_risk = sum(c.risk_score for c in changes) / len(changes) if changes else 0.0
    
    lines = []
    lines.append(f"Summary: {len(changes)} files, {total_lines} lines changed")
    lines.append(f"Average risk score: {avg_risk:.2f}")
    
    # Add risk breakdown
    low_risk = sum(1 for c in changes if c.risk_score < 0.3)
    medium_risk = sum(1 for c in changes if 0.3 <= c.risk_score < 0.7)
    high_risk = sum(1 for c in changes if c.risk_score >= 0.7)
    
    lines.append(f"Risk breakdown: {low_risk} low, {medium_risk} medium, {high_risk} high")
    
    return "\n".join(lines)


def generate_file_list(changes: List[Change], max_files: int = 20) -> str:
    """Generate a formatted list of files."""
    if not changes:
        return "No files"
    
    lines = []
    display_changes = changes[:max_files]
    
    for change in display_changes:
        tags_str = ", ".join([t.value for t in change.tags])
        lines.append(f"  [{change.change_type.value:8}] {change.path:40} ({tags_str})")
    
    if len(changes) > max_files:
        lines.append(f"  ... and {len(changes) - max_files} more files")
    
    return "\n".join(lines)
