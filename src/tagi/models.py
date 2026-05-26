"""Data models for tagi."""

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
class Change:
    """Represents a single file change."""
    path: str
    change_type: ChangeType
    tags: List[Tag] = field(default_factory=list)
    lines_changed: int = 0
    risk_score: float = 0.0


@dataclass
class ChangeGroup:
    """Group of related changes."""
    name: str
    changes: List[Change]
    tags: List[Tag] = field(default_factory=list)
    total_lines: int = 0
    avg_risk: float = 0.0
