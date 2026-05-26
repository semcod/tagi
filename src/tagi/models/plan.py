"""Plan model."""

from dataclasses import dataclass, field
from typing import List

from .change import Change


@dataclass
class PlanStep:
    """A single step in an execution plan."""
    description: str
    command: str
    files: List[str] = field(default_factory=list)


@dataclass
class Plan:
    """An execution plan for shipping changes."""
    name: str
    changes: List[Change]
    steps: List[PlanStep] = field(default_factory=list)
    commit_message: str = ""
