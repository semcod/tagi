"""Change model."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ChangeType(str, Enum):
    """Type of git change."""
    MODIFIED = "modified"
    ADDED = "added"
    DELETED = "deleted"
    RENAMED = "renamed"


class Tag(str, Enum):
    """Hashtag categories for changes."""
    SMALL = "#small"
    LARGE = "#large"
    NEW = "#new"
    DEPS = "#deps"
    DOCS = "#docs"
    TESTS = "#tests"
    CONFIG = "#config"
    RISKY = "#risky"
    REFACTOR = "#refactor"
    FEATURE = "#feature"


@dataclass
class ChangeMetrics:
    """Numerical metrics for change analysis."""
    risk_score: float = 0.0
    complexity_score: float = 0.0
    impact_score: float = 0.0
    stability_score: float = 0.0
    test_coverage_impact: float = 0.0
    dependency_depth: int = 0
    
    def to_vector(self) -> List[float]:
        """Convert metrics to vector for comparison."""
        return [
            self.risk_score,
            self.complexity_score,
            self.impact_score,
            self.stability_score,
            self.test_coverage_impact,
            self.dependency_depth / 10.0  # Normalize depth
        ]


@dataclass
class Change:
    """Represents a single file change."""
    path: str
    change_type: ChangeType
    tags: List[Tag] = field(default_factory=list)
    lines_changed: int = 0
    risk_score: float = 0.0
    metrics: ChangeMetrics = field(default_factory=ChangeMetrics)
