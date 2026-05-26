"""tagi - Git change orchestrator."""

from .models import Change, ChangeType, Tag, ChangeGroup, Plan, PlanStep
from .scanner import scan_repo, get_diff, get_staged_diff, count_lines_changed
from .heuristics import apply_tags, calculate_risk_score
from .planner import group_changes, group_by_tag, select_changes_by_tag
from .composer import generate_commit_message, generate_summary
from .executor import GitExecutor, PublishExecutor
from .providers import BaseProvider, GitHubProvider, GitLabProvider
from .llm import LlxAdapter
from .config import Config

__all__ = [
    # Models
    "Change",
    "ChangeType",
    "Tag",
    "ChangeGroup",
    "Plan",
    "PlanStep",
    # Scanner
    "scan_repo",
    "get_diff",
    "get_staged_diff",
    "count_lines_changed",
    # Heuristics
    "apply_tags",
    "calculate_risk_score",
    # Planner
    "group_changes",
    "group_by_tag",
    "select_changes_by_tag",
    # Composer
    "generate_commit_message",
    "generate_summary",
    # Executor
    "GitExecutor",
    "PublishExecutor",
    # Providers
    "BaseProvider",
    "GitHubProvider",
    "GitLabProvider",
    # LLM
    "LlxAdapter",
    # Config
    "Config",
]
