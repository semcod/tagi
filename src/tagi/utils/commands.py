"""Shared subprocess command execution.

Single owner of the ``subprocess.run`` call pattern, extracted to remove
the ``result`` shotgun-surgery smell (PLF-141). Everything that shells out
goes through :func:`run_command` so execution behavior is defined once.
"""

import subprocess
from typing import List


def run_command(cmd: List[str], cwd: str = ".") -> subprocess.CompletedProcess:
    """Run a command in a directory and return the completed process."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
