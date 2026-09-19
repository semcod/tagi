"""Dependency graph analysis module."""

from collections import defaultdict, deque
from typing import Dict, List, Optional, Set
from tagi.models.change import Change
import ast
import re


def _collect_import_names(tree: ast.AST) -> List[str]:
    """Collect imported module paths from a parsed AST.

    Args:
        tree: Parsed AST of a Python file

    Returns:
        List of imported module paths
    """
    imports: List[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ''
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    return imports


def analyze_python_imports(file_path: str, repo_path: str = ".") -> List[str]:
    """Analyze Python file for import dependencies.

    Args:
        file_path: Path to the Python file
        repo_path: Path to the repository

    Returns:
        List of imported module paths
    """
    try:
        full_path = f"{repo_path}/{file_path}"
        with open(full_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)
        return _collect_import_names(tree)
    except Exception:
        return []


def build_dependency_graph(changes: List[Change], repo_path: str = ".") -> Dict[str, Set[str]]:
    """Build a dependency graph from changes.
    
    Args:
        changes: List of changes to analyze
        repo_path: Path to the repository
        
    Returns:
        Dictionary mapping file paths to their dependencies
    """
    graph = {}
    
    for change in changes:
        if change.path.endswith('.py'):
            deps = analyze_python_imports(change.path, repo_path)
            graph[change.path] = set(deps)
        else:
            graph[change.path] = set()
    
    return graph


class _LevelOrder:
    """Level-by-level topological order over a dependency graph (Kahn's algorithm)."""

    def __init__(self, graph: Dict[str, Set[str]]) -> None:
        """Index reverse edges and in-degrees, then seed the pending queue.

        Args:
            graph: Dependency graph mapping files to their dependencies
        """
        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)
        self.in_degree: Dict[str, int] = defaultdict(int)

        for file, deps in graph.items():
            for dep in deps:
                self.reverse_graph[dep].add(file)
                self.in_degree[file] += 1

        self.queue: "deque[str]" = deque(
            [f for f in graph if self.in_degree[f] == 0]
        )

    def levels(self) -> List[List[str]]:
        """Drain the pending queue level by level into commit groups.

        Returns:
            List of levels, each containing files that can be committed together
        """
        result: List[List[str]] = []

        while self.queue:
            level = self._drain_level()
            if level:
                result.append(level)

        return result

    def _drain_level(self) -> List[str]:
        """Pop one queue level and enqueue dependents that become unblocked.

        Returns:
            Files drained from the current queue level
        """
        level: List[str] = []

        for _ in range(len(self.queue)):
            file = self.queue.popleft()
            level.append(file)

            for dependent in self.reverse_graph[file]:
                self.in_degree[dependent] -= 1
                if self.in_degree[dependent] == 0:
                    self.queue.append(dependent)

        return level


def find_dependency_order(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find the dependency order using topological sort.
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of lists, where each inner list contains files that can be committed together
    """
    return _LevelOrder(graph).levels()


_WHITE, _GRAY, _BLACK = 0, 1, 2


def _mark(node: str, color: Dict[str, int], value: int) -> None:
    """Set the DFS color of a node."""
    color[node] = value


def _cycle_from(node: str, path: List[str]) -> List[str]:
    """Return the slice of path that forms the cycle starting at node."""
    cycle_start = path.index(node)
    return path[cycle_start:]


def _dfs_visit(
    node: str,
    graph: Dict[str, Set[str]],
    color: Dict[str, int],
    path: List[str],
    cycles: List[List[str]],
) -> None:
    """Depth-first visit of a node, recording cycles among in-progress nodes."""
    if color[node] == _GRAY:
        cycles.append(_cycle_from(node, path))
        return

    if color[node] == _BLACK:
        return

    _mark(node, color, _GRAY)
    path.append(node)

    for neighbor in graph.get(node, []):
        if neighbor in color:
            _dfs_visit(neighbor, graph, color, path, cycles)

    path.pop()
    _mark(node, color, _BLACK)


def detect_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Detect circular dependencies in the graph.
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of cycles found
    """
    color = {node: _WHITE for node in graph}
    cycles: List[List[str]] = []

    for node in graph:
        if color[node] == _WHITE:
            _dfs_visit(node, graph, color, [], cycles)

    return cycles


def _longest_path_length(
    node: str,
    graph: Dict[str, Set[str]],
    memo: Dict[str, int],
) -> int:
    """Return the length of the longest dependency chain starting at node."""
    if node in memo:
        return memo[node]

    max_len = 0
    for dep in graph.get(node, []):
        if dep in graph:
            max_len = max(max_len, _longest_path_length(dep, graph, memo))

    memo[node] = max_len + 1
    return memo[node]


def _find_longest_start(graph: Dict[str, Set[str]], memo: Dict[str, int]) -> str:
    """Return the node starting the longest dependency chain."""
    return max(graph, key=lambda node: _longest_path_length(node, graph, memo))


def _next_critical_node(
    node: str,
    graph: Dict[str, Set[str]],
    memo: Dict[str, int],
    visited: Set[str],
) -> Optional[str]:
    """Return the unvisited dependency of node with the longest chain."""
    next_node = None
    max_next = 0

    for dep in graph.get(node, []):
        if dep in graph and dep not in visited and memo.get(dep, 0) > max_next:
            max_next = memo[dep]
            next_node = dep

    return next_node


def _reconstruct_critical_path(
    start_node: str,
    graph: Dict[str, Set[str]],
    memo: Dict[str, int],
) -> List[str]:
    """Walk greedily from start_node along the longest chains."""
    path: List[str] = []
    visited: Set[str] = set()

    current: Optional[str] = start_node
    while current and current not in visited:
        path.append(current)
        visited.add(current)
        current = _next_critical_node(current, graph, memo, visited)

    return path


def get_critical_path(graph: Dict[str, Set[str]]) -> List[str]:
    """Find the critical path (longest dependency chain).
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of files in the critical path
    """
    if not graph:
        return []

    memo: Dict[str, int] = {}
    start_node = _find_longest_start(graph, memo)
    return _reconstruct_critical_path(start_node, graph, memo)
