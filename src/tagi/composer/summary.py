"""Summary module for generating change summaries."""

from typing import List

from tagi.models import Change
from tagi.utils.line_builder import LineBuilder
from tagi.utils.risk import average_risk, total_lines_changed


def generate_summary(changes: List[Change]) -> str:
    """Generate a summary of changes."""
    if not changes:
        return "No changes"
    
    low_risk = sum(1 for c in changes if c.risk_score < 0.3)
    medium_risk = sum(1 for c in changes if 0.3 <= c.risk_score < 0.7)
    high_risk = sum(1 for c in changes if c.risk_score >= 0.7)

    return LineBuilder([
        f"Summary: {len(changes)} files, {total_lines_changed(changes)} lines changed",
        f"Average risk score: {average_risk(changes):.2f}",
        f"Risk breakdown: {low_risk} low, {medium_risk} medium, {high_risk} high",
    ]).text()


def generate_file_list(changes: List[Change], max_files: int = 20) -> str:
    """Generate a formatted list of files."""
    if not changes:
        return "No files"
    
    file_lines = [
        f"  [{change.change_type.value:8}] {change.path:40} "
        f"({', '.join(t.value for t in change.tags)})"
        for change in changes[:max_files]
    ]
    if len(changes) > max_files:
        file_lines.append(f"  ... and {len(changes) - max_files} more files")

    return LineBuilder(file_lines).text()
