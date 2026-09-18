"""Line accumulation for text report generation."""

from collections.abc import Iterable
from typing import List


class LineBuilder:
    """Single place where report line lists are created and mutated."""

    def __init__(self, lines: Iterable[str] = ()) -> None:
        self._lines: List[str] = list(lines)

    def add(self, *items: str) -> None:
        """Append one or more lines."""
        self._lines.extend(items)

    def as_list(self) -> List[str]:
        """Return the accumulated lines."""
        return self._lines

    def text(self) -> str:
        """Join the accumulated lines with newlines."""
        return "\n".join(self._lines)
