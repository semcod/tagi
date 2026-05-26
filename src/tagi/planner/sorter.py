"""Heuristic-based change sorting module."""

from typing import List
from tagi.models.change import Change


def sort_by_complexity(changes: List[Change]) -> List[Change]:
    """Sort changes by complexity (simplest first).
    
    Complexity is calculated based on:
    - Risk score (lower is simpler)
    - Lines changed (fewer lines is simpler)
    - Change type (MODIFIED is simpler than ADDED or DELETED)
    
    Args:
        changes: List of changes to sort
        
    Returns:
        Sorted list of changes (simplest first)
    """
    def complexity_score(change: Change) -> float:
        """Calculate complexity score (lower = simpler)."""
        # Risk score (0-1) - higher is more complex
        risk_weight = 0.5
        # Lines changed - more lines is more complex
        lines_weight = 0.3
        # Change type weight
        type_weight = 0.2
        
        # Change type scoring
        type_scores = {
            "modified": 0,
            "added": 1,
            "deleted": 2,
            "renamed": 0.5,
        }
        type_score = type_scores.get(change.change_type.value, 1)
        
        # Normalize lines (log scale to reduce impact of very large files)
        import math
        lines_score = math.log(max(change.lines_changed, 1)) / 10
        
        total_score = (
            change.risk_score * risk_weight +
            lines_score * lines_weight +
            type_score * type_weight
        )
        
        return total_score
    
    return sorted(changes, key=complexity_score)


def sort_by_tag_priority(changes: List[Change], tag_order: List[str]) -> List[Change]:
    """Sort changes by tag priority.
    
    Args:
        changes: List of changes to sort
        tag_order: List of tags in priority order (with # prefix)
        
    Returns:
        Sorted list of changes by tag priority
    """
    from tagi.models.change import Tag
    
    # Map tags to their priority index
    tag_priority = {tag: i for i, tag in enumerate(tag_order)}
    
    def get_tag_priority(change: Change) -> int:
        """Get the priority of the first matching tag."""
        for tag in change.tags:
            if tag.value in tag_priority:
                return tag_priority[tag.value]
        return len(tag_order)  # Lowest priority if no match
    
    # Sort by tag priority, then by complexity within same tag
    return sorted(changes, key=lambda c: (get_tag_priority(c), c.risk_score))


def group_by_complexity(changes: List[Change], num_groups: int = 3) -> List[List[Change]]:
    """Group changes into complexity tiers (simple, medium, complex).
    
    Args:
        changes: List of changes to group
        num_groups: Number of complexity groups
        
    Returns:
        List of change groups (simplest first)
    """
    sorted_changes = sort_by_complexity(changes)
    
    if not sorted_changes:
        return []
    
    groups = []
    group_size = max(1, len(sorted_changes) // num_groups)
    
    for i in range(num_groups):
        start = i * group_size
        end = start + group_size if i < num_groups - 1 else len(sorted_changes)
        if start < len(sorted_changes):
            groups.append(sorted_changes[start:end])
    
    return groups
