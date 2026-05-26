"""Scanner module for reading git repository state."""

from .status import parse_status, scan_repo
from .diff import get_diff, get_staged_diff
from .files import count_lines_changed

__all__ = [
    "parse_status",
    "scan_repo",
    "get_diff",
    "get_staged_diff",
    "count_lines_changed",
]
