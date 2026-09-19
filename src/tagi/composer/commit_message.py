"""Commit message orchestration.

The public message generators are re-exported here for backward compatibility;
their implementations live in focused submodules around stable responsibilities:

- ``_tags.py`` — tag/scope analysis
- ``_templates.py`` — template rendering
- ``formats.py`` — concrete message-format generators
"""

from typing import List

from tagi.models import Change
from tagi.config import load_config

from ._tags import summary_tag
from ._templates import render_template
from .formats import (
    generate_conventional_message,
    generate_detailed_message,
    generate_simple_message,
    generate_oneline_message,
    generate_files_message,
)

__all__ = [
    "generate_commit_message",
    "generate_conventional_message",
    "generate_detailed_message",
    "generate_simple_message",
    "generate_oneline_message",
    "generate_files_message",
]


def generate_commit_message(changes: List[Change], template: str = "default", repo_path: str = ".", use_llm: bool = False) -> str:
    """Generate a commit message based on template."""
    config = load_config(repo_path)

    # A configured custom template overrides the built-in name.
    template = config.get_template(template) or template

    files_str = ", ".join(c.path for c in changes)
    message = render_template(
        template, tag=summary_tag(changes), files=files_str, count=len(changes)
    )

    if use_llm or config.llm_enabled:
        message = _improve_with_llm(message, repo_path, files_str)

    return message


def _improve_with_llm(message: str, repo_path: str, files_str: str) -> str:
    """Best-effort LLM refinement of a commit message.

    Returns the original message unchanged if the optional LLM backend is
    unavailable or errors — LLM enhancement is optional, never required.
    """
    try:
        from tagi.llm import LlxAdapter

        adapter = LlxAdapter(repo_path=repo_path, enabled=True)
        return adapter.improve_message(message, context=files_str)
    except Exception:
        return message
