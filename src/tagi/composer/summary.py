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
    
    return "\n".join(lines)
