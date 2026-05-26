"""Tags module for applying heuristic tags."""

from typing import List

from tagi.config import Config
from tagi.models import Change, ChangeType, Tag
from tagi.scanner.files import count_lines_changed
from .scoring import calculate_risk_score


def apply_tags(changes: List[Change], repo_path: str = ".") -> List[Change]:
    """Apply heuristic tags to changes."""
    config = Config(repo_path)
    
    for change in changes:
        tags = []
        
        # Check custom config rules first
        custom_tag = config.get_tag_for_path(change.path)
        if custom_tag:
            try:
                tags.append(Tag(custom_tag))
            except ValueError:
                pass  # Invalid tag, skip
        
        # Apply custom heuristics from config
        custom_heuristics = config.get_heuristics_for_path(change.path)
        for custom_tag in custom_heuristics:
            try:
                tags.append(Tag(custom_tag))
            except ValueError:
                pass  # Invalid tag, skip
        
        # Calculate lines changed for size heuristics
        lines_changed = count_lines_changed(change.path, repo_path)
        change.lines_changed = lines_changed
        
        # Apply path-based tags
        tags.extend(apply_path_tags(change, lines_changed))
        
        # Tag based on change type
        if change.change_type == ChangeType.ADDED:
            tags.append(Tag.NEW)
        
        # Size-based tagging (can coexist with other tags)
        if lines_changed > 100:
            tags.append(Tag.LARGE)
        elif lines_changed < 10:
            if not tags:
                tags.append(Tag.SMALL)
        else:
            # Medium size changes don't get size tag unless they have no other tags
            if not tags:
                tags.append(Tag.SMALL)
        
        change.tags = tags
        change.risk_score = calculate_risk_score(change, tags)
    
    return changes


def apply_path_tags(change: Change, lines_changed: int) -> List[Tag]:
    """Apply path-based heuristic tags to a change."""
    tags = []
    path_lower = change.path.lower()
    
    if any(dep in path_lower for dep in ['requirements', 'package.json', 'poetry.lock', 'pyproject.toml', 'cargo.toml', 'go.mod', 'yarn.lock', 'pnpm-lock.yaml', 'package-lock.json', 'gemfile', 'composer.json']):
        tags.append(Tag.DEPS)
    if any(doc in path_lower for doc in ['readme', 'doc', 'md', 'rst', 'changelog', 'contributing', 'license', 'authors', 'change']):
        tags.append(Tag.DOCS)
    if any(test in path_lower for test in ['test_', '_test.py', 'tests/', '__tests__', 'spec.', '.spec.', 'mock_', 'fixture']):
        tags.append(Tag.TESTS)
    if any(config in path_lower for config in ['config', '.env', 'settings', 'yaml', 'toml', 'json', 'ini', 'cfg', 'conf']):
        tags.append(Tag.CONFIG)
    if any(risky in path_lower for risky in ['auth', 'migration', 'infra', 'deploy', 'security', 'password', 'secret', 'key', 'token', 'credential', 'private']):
        tags.append(Tag.RISKY)
    if any(ref in path_lower for ref in ['refactor', 'cleanup', 'deprecate', 'remove', 'delete', 'simplify']):
        tags.append(Tag.REFACTOR)
    if any(feat in path_lower for feat in ['feature', 'add', 'new', 'implement', 'create', 'introduce']):
        tags.append(Tag.FEATURE)
    if any(fix in path_lower for fix in ['fix', 'bug', 'patch', 'hotfix', 'correct', 'repair']):
        tags.append(Tag.RISKY)
    
    return tags
