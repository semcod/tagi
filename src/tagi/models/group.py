"""ChangeGroup model."""

from dataclasses import dataclass, field
from typing import List

from .change import Change, Tag


@dataclass
class ChangeGroup:
    """Group of related changes."""
    name: str
    changes: List[Change]
    tags: List[Tag] = field(default_factory=list)
    total_lines: int = 0
    avg_risk: float = 0.0
