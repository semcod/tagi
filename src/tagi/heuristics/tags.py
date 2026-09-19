"""Tags module for applying heuristic tags."""

from typing import List

from tagi.config import load_config
from tagi.models import Change, ChangeType, Tag
from tagi.scanner.files import count_lines_changed
from tagi.utils.paths import path_matches
from .scoring import calculate_risk_score
from .metrics import calculate_metrics


def apply_tags(changes: List[Change], repo_path: str = ".") -> List[Change]:
    """Apply heuristic tags to changes."""
    custom_tags_for = load_config(repo_path).get_tags_for_path

    for change in changes:
        _tag_change(change, repo_path, custom_tags_for)

    return changes


def _tag_change(change: Change, repo_path: str, custom_tags_for) -> None:
    """Apply all heuristic tags to a single change."""
    # Custom config tags come first (rule tag before heuristics)
    tags = _custom_config_tags(custom_tags_for, change.path)

    # Calculate lines changed for size heuristics
    lines_changed = count_lines_changed(change.path, repo_path)
    change.lines_changed = lines_changed

    # Apply path-based tags
    tags.extend(apply_path_tags(change, lines_changed))

    # Tag based on change type
    if change.change_type == ChangeType.ADDED:
        tags.append(Tag.NEW)

    # Calculate numerical metrics
    change.metrics = calculate_metrics(change, repo_path)

    # Size-based tagging (LARGE coexists with other tags)
    tags.extend(_size_tags(lines_changed, has_other_tags=bool(tags)))

    change.tags = tags
    change.risk_score = calculate_risk_score(change, tags)


def _custom_config_tags(custom_tags_for, path: str):
    """Convert configured custom tag names into valid Tag values."""
    valid_tags = []
    for custom_tag in custom_tags_for(path):
        try:
            valid_tags.append(Tag(custom_tag))
        except ValueError:
            pass  # Invalid tag, skip
    return valid_tags


def _size_tags(lines_changed: int, has_other_tags: bool):
    """Return the size tags for a change (zero or one entries)."""
    if lines_changed > 100:
        return [Tag.LARGE]
    if has_other_tags:
        # Small/medium changes only get a size tag when no other tag applies
        return []
    return [Tag.SMALL]


def apply_path_tags(change: Change, lines_changed: int) -> List[Tag]:
    """Apply path-based heuristic tags to a change."""
    # Pattern mapping for tag detection
    tag_patterns = [
        (['requirements', 'package.json', 'poetry.lock', 'pyproject.toml', 'cargo.toml', 'go.mod', 'yarn.lock', 'pnpm-lock.yaml', 'package-lock.json', 'gemfile', 'composer.json'], Tag.DEPS),
        (['readme', 'doc', 'md', 'rst', 'changelog', 'contributing', 'license', 'authors', 'change'], Tag.DOCS),
        (['test_', '_test.py', 'tests/', '__tests__', 'spec.', '.spec.', 'mock_', 'fixture'], Tag.TESTS),
        (['config', '.env', 'settings', 'yaml', 'toml', 'json', 'ini', 'cfg', 'conf'], Tag.CONFIG),
        (['auth', 'migration', 'infra', 'deploy', 'security', 'password', 'secret', 'key', 'token', 'credential', 'private'], Tag.RISKY),
        (['refactor', 'cleanup', 'deprecate', 'remove', 'delete', 'simplify'], Tag.REFACTOR),
        (['feature', 'add', 'new', 'implement', 'create', 'introduce'], Tag.FEATURE),
        (['fix', 'bug', 'patch', 'hotfix', 'correct', 'repair'], Tag.RISKY),
    ]
    
    return [
        tag
        for patterns, tag in tag_patterns
        if any(path_matches(change.path, pattern) for pattern in patterns)
    ]
