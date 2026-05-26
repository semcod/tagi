"""Heuristics module for tagging changes."""

import os
import subprocess
from typing import List

from tagi.config import Config
from tagi.models import Change, ChangeType, Tag


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
        
        # Calculate lines changed for size heuristics
        lines_changed = _count_lines_changed(change.path, repo_path)
        change.lines_changed = lines_changed
        
        # Tag based on file path patterns
        path_lower = change.path.lower()
        
        if any(dep in path_lower for dep in ['requirements', 'package.json', 'poetry.lock', 'pyproject.toml', 'cargo.toml', 'go.mod', 'yarn.lock', 'pnpm-lock.yaml']):
            tags.append(Tag.DEPS)
        elif any(doc in path_lower for doc in ['readme', 'doc', 'md', 'rst', 'changelog', 'contributing']):
            tags.append(Tag.DOCS)
        elif any(test in path_lower for test in ['test_', '_test.py', 'tests/', '__tests__', 'spec.', '.spec.']):
            tags.append(Tag.TESTS)
        elif any(config in path_lower for config in ['config', '.env', 'settings', 'yaml', 'toml', 'json', 'ini', 'cfg']):
            tags.append(Tag.CONFIG)
        elif any(risky in path_lower for risky in ['auth', 'migration', 'infra', 'deploy', 'security', 'password', 'secret', 'key']):
            tags.append(Tag.RISKY)
        elif any(ref in path_lower for ref in ['refactor', 'cleanup', 'deprecate', 'remove']):
            tags.append(Tag.REFACTOR)
        elif any(feat in path_lower for feat in ['feature', 'add', 'new', 'implement']):
            tags.append(Tag.FEATURE)
        
        # Tag based on change type
        if change.change_type == ChangeType.ADDED:
            tags.append(Tag.NEW)
        
        # Size-based tagging
        if lines_changed > 100:
            tags.append(Tag.LARGE)
        elif lines_changed < 10 and not tags:
            tags.append(Tag.SMALL)
        
        # Default to small if no other tags
        if not tags:
            tags.append(Tag.SMALL)
        elif len(tags) > 2:
            tags.append(Tag.LARGE)
        
        # Calculate risk score
        change.risk_score = _calculate_risk_score(change, tags)
        
        change.tags = tags
    
    return changes


def _count_lines_changed(file_path: str, repo_path: str) -> int:
    """Count the number of lines changed in a file."""
    try:
        cmd = ["git", "diff", "--numstat", file_path]
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return 0
        
        # git diff --numstat output: additions deletions filename
        parts = result.stdout.strip().split()
        if len(parts) >= 2:
            additions = int(parts[0]) if parts[0] != '-' else 0
            deletions = int(parts[1]) if parts[1] != '-' else 0
            return additions + deletions
        
        return 0
    except (ValueError, IndexError, subprocess.SubprocessError):
        return 0


def _calculate_risk_score(change: Change, tags: List[Tag]) -> float:
    """Calculate a risk score for a change."""
    score = 0.0
    
    # Base score from lines changed
    score += min(change.lines_changed / 100.0, 1.0) * 0.3
    
    # Risk from tags
    if Tag.RISKY in tags:
        score += 0.5
    if Tag.CONFIG in tags:
        score += 0.2
    if Tag.DEPS in tags:
        score += 0.3
    if Tag.LARGE in tags:
        score += 0.2
    
    # Risk from change type
    if change.change_type == ChangeType.DELETED:
        score += 0.3
    elif change.change_type == ChangeType.RENAMED:
        score += 0.1
    
    return min(score, 1.0)
