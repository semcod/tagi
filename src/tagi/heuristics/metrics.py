"""Metrics calculation module for change analysis."""

import math
from typing import List
from tagi.models.change import Change, ChangeMetrics, ChangeType


_COMPLEXITY_EXTENSION_WEIGHTS = (
    ((".py",), 0.7),
    ((".js", ".ts", ".jsx", ".tsx"), 0.6),
    ((".md", ".txt", ".rst"), 0.2),
    ((".json", ".yaml", ".yml", ".toml", ".ini"), 0.4),
)
_DEFAULT_COMPLEXITY_EXTENSION_WEIGHT = 0.5

_IMPACT_EXTENSION_WEIGHTS = (
    ((".py", ".js", ".ts"), 0.8),
    ((".css", ".html", ".jsx", ".tsx"), 0.6),
    ((".md", ".txt", ".rst"), 0.2),
    ((".json", ".yaml", ".yml", ".toml", ".ini"), 0.7),
)
_DEFAULT_IMPACT_EXTENSION_WEIGHT = 0.5

_COMPLEXITY_TYPE_WEIGHTS = {
    ChangeType.MODIFIED: 0.3,
    ChangeType.ADDED: 0.6,
    ChangeType.DELETED: 0.8,
    ChangeType.RENAMED: 0.2,
}
_DEFAULT_COMPLEXITY_TYPE_WEIGHT = 0.5


def _extension_complexity_weight(path: str) -> float:
    """Return the complexity weight for a file path (first matching suffix wins)."""
    path_lower = path.lower()
    for suffixes, weight in _COMPLEXITY_EXTENSION_WEIGHTS:
        if path_lower.endswith(suffixes):
            return weight
    return _DEFAULT_COMPLEXITY_EXTENSION_WEIGHT


def _extension_impact_weight(path: str) -> float:
    """Return the impact weight for a file path (first matching suffix wins)."""
    path_lower = path.lower()
    for suffixes, weight in _IMPACT_EXTENSION_WEIGHTS:
        if path_lower.endswith(suffixes):
            return weight
    return _DEFAULT_IMPACT_EXTENSION_WEIGHT


def calculate_metrics(change: Change, repo_path: str = ".") -> ChangeMetrics:
    """Calculate numerical metrics for a change.
    
    Args:
        change: The change to calculate metrics for
        repo_path: Path to the repository
        
    Returns:
        ChangeMetrics object with calculated values
    """
    # Risk score (already calculated)
    risk_score = change.risk_score
    
    # Complexity score based on lines and type
    complexity_score = _calculate_complexity(change)
    
    # Impact score based on file type and change type
    impact_score = _calculate_impact(change)
    
    # Stability score based on change type
    stability_score = _calculate_stability(change)
    
    # Test coverage impact
    test_coverage_impact = _calculate_test_impact(change)
    
    # Dependency depth (simplified)
    dependency_depth = _calculate_dependency_depth(change)
    
    return ChangeMetrics(
        risk_score=risk_score,
        complexity_score=complexity_score,
        impact_score=impact_score,
        stability_score=stability_score,
        test_coverage_impact=test_coverage_impact,
        dependency_depth=dependency_depth
    )


def _calculate_complexity(change: Change) -> float:
    """Calculate complexity score (0-1)."""
    # Normalize lines changed (log scale)
    lines_score = min(math.log(max(change.lines_changed, 1)) / 10, 1.0)

    # Change type weight
    type_score = _COMPLEXITY_TYPE_WEIGHTS.get(
        change.change_type, _DEFAULT_COMPLEXITY_TYPE_WEIGHT
    )

    # File extension weight
    ext_score = _extension_complexity_weight(change.path)

    # Weighted average
    complexity = (lines_score * 0.5 + type_score * 0.3 + ext_score * 0.2)
    return min(complexity, 1.0)


def _calculate_impact(change: Change) -> float:
    """Calculate impact score (0-1)."""
    impact = _extension_impact_weight(change.path)

    # Adjust by lines changed
    lines_factor = min(change.lines_changed / 100, 1.0)
    impact = impact * (0.5 + lines_factor * 0.5)

    return min(impact, 1.0)


def _calculate_stability(change: Change) -> float:
    """Calculate stability score (0-1, higher = more stable)."""
    # Change type stability (higher is more stable)
    stability_weights = {
        ChangeType.MODIFIED: 0.8,
        ChangeType.ADDED: 0.6,
        ChangeType.DELETED: 0.3,
        ChangeType.RENAMED: 0.9,
    }
    stability = stability_weights.get(change.change_type, 0.5)
    
    # Adjust by risk (inverse relationship)
    stability = stability * (1.0 - change.risk_score * 0.5)
    
    return max(stability, 0.0)


def _calculate_test_impact(change: Change) -> float:
    """Calculate test coverage impact (0-1)."""
    path_lower = change.path.lower()
    
    # Test files have high impact on test coverage
    if 'test' in path_lower or 'spec' in path_lower:
        return 0.9
    
    # Source files have moderate impact
    if path_lower.endswith(('.py', '.js', '.ts')):
        return 0.6
    
    # Other files have low impact
    return 0.2


def _calculate_dependency_depth(change: Change) -> int:
    """Calculate dependency depth (simplified)."""
    # This is a simplified version - real implementation would parse imports
    path_lower = change.path.lower()
    
    if path_lower.endswith('.py'):
        # Python files typically have more dependencies
        return 3
    elif path_lower.endswith(('.js', '.ts', '.jsx', '.tsx')):
        return 2
    elif path_lower.endswith(('.json', '.yaml', '.yml')):
        return 1
    else:
        return 0


def filter_by_metrics(
    changes: List[Change],
    min_risk: float = 0.0,
    max_risk: float = 1.0,
    min_complexity: float = 0.0,
    max_complexity: float = 1.0,
    min_impact: float = 0.0,
    max_impact: float = 1.0,
) -> List[Change]:
    """Filter changes by numerical metrics.
    
    Args:
        changes: List of changes to filter
        min_risk: Minimum risk score
        max_risk: Maximum risk score
        min_complexity: Minimum complexity score
        max_complexity: Maximum complexity score
        min_impact: Minimum impact score
        max_impact: Maximum impact score
        
    Returns:
        Filtered list of changes
    """
    filtered = []
    for change in changes:
        metrics = change.metrics
        if (min_risk <= metrics.risk_score <= max_risk and
            min_complexity <= metrics.complexity_score <= max_complexity and
            min_impact <= metrics.impact_score <= max_impact):
            filtered.append(change)
    
    return filtered


def sort_by_metric(changes: List[Change], metric: str = "risk_score", ascending: bool = True) -> List[Change]:
    """Sort changes by a specific metric.
    
    Args:
        changes: List of changes to sort
        metric: Metric name to sort by
        ascending: Sort order
        
    Returns:
        Sorted list of changes
    """
    return sorted(changes, key=lambda c: getattr(c.metrics, metric, 0), reverse=not ascending)


def calculate_vector_distance(change1: Change, change2: Change) -> float:
    """Calculate Euclidean distance between two change vectors.
    
    Args:
        change1: First change
        change2: Second change
        
    Returns:
        Euclidean distance between the two change vectors
    """
    vec1 = change1.metrics.to_vector()
    vec2 = change2.metrics.to_vector()
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
