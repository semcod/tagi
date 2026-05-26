"""Metrics and analytics module."""

from typing import Dict, List
from tagi.models.change import Change
from datetime import datetime
import json


class MetricsCollector:
    """Collect and analyze metrics about changes."""
    
    def __init__(self):
        self.metrics = {
            "total_changes": 0,
            "by_type": {},
            "by_tag": {},
            "by_risk": {"low": 0, "medium": 0, "high": 0},
            "total_lines": 0,
            "avg_risk": 0.0,
            "timeline": []
        }
    
    def collect(self, changes: List[Change]) -> Dict:
        """Collect metrics from changes.
        
        Args:
            changes: List of changes to analyze
            
        Returns:
            Dictionary of collected metrics
        """
        if not changes:
            return self.metrics
        
        self.metrics["total_changes"] = len(changes)
        
        # Count by type
        for change in changes:
            ctype = change.change_type.value
            self.metrics["by_type"][ctype] = self.metrics["by_type"].get(ctype, 0) + 1
        
        # Count by tag
        for change in changes:
            for tag in change.tags:
                tval = tag.value
                self.metrics["by_tag"][tval] = self.metrics["by_tag"].get(tval, 0) + 1
        
        # Risk distribution
        for change in changes:
            risk = change.risk_score
            if risk < 0.3:
                self.metrics["by_risk"]["low"] += 1
            elif risk < 0.7:
                self.metrics["by_risk"]["medium"] += 1
            else:
                self.metrics["by_risk"]["high"] += 1
        
        # Lines and risk
        self.metrics["total_lines"] = sum(c.lines_changed for c in changes)
        self.metrics["avg_risk"] = sum(c.risk_score for c in changes) / len(changes)
        
        # Timeline
        self.metrics["timeline"] = [{
            "file": c.path,
            "type": c.change_type.value,
            "lines": c.lines_changed,
            "risk": c.risk_score,
            "tags": [t.value for t in c.tags]
        } for c in changes]
        
        return self.metrics
    
    def to_json(self) -> str:
        """Convert metrics to JSON string.
        
        Returns:
            JSON string of metrics
        """
        return json.dumps(self.metrics, indent=2)
    
    def save(self, filepath: str) -> bool:
        """Save metrics to file.
        
        Args:
            filepath: Path to save metrics
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                f.write(self.to_json())
            return True
        except Exception:
            return False


def generate_report(metrics: Dict) -> str:
    """Generate a human-readable metrics report.
    
    Args:
        metrics: Metrics dictionary
        
    Returns:
        Formatted report string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("METRICS REPORT")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append(f"Total Changes: {metrics['total_changes']}")
    lines.append(f"Total Lines Changed: {metrics['total_lines']}")
    lines.append(f"Average Risk Score: {metrics['avg_risk']:.2f}")
    lines.append("")
    
    lines.append("Changes by Type:")
    for ctype, count in metrics['by_type'].items():
        lines.append(f"  {ctype}: {count}")
    lines.append("")
    
    lines.append("Changes by Tag:")
    for tag, count in sorted(metrics['by_tag'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {tag}: {count}")
    lines.append("")
    
    lines.append("Risk Distribution:")
    lines.append(f"  Low (<0.3): {metrics['by_risk']['low']}")
    lines.append(f"  Medium (0.3-0.7): {metrics['by_risk']['medium']}")
    lines.append(f"  High (>0.7): {metrics['by_risk']['high']}")
    lines.append("")
    
    return "\n".join(lines)


def compare_metrics(metrics1: Dict, metrics2: Dict) -> Dict:
    """Compare two metrics sets.
    
    Args:
        metrics1: First metrics set
        metrics2: Second metrics set
        
    Returns:
        Dictionary of differences
    """
    diff = {
        "total_changes_delta": metrics2["total_changes"] - metrics1["total_changes"],
        "lines_delta": metrics2["total_lines"] - metrics1["total_lines"],
        "risk_delta": metrics2["avg_risk"] - metrics1["avg_risk"]
    }
    
    return diff
