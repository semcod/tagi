"""Dependency graph analysis module."""

from typing import Dict, List, Set, Tuple
from tagi.models.change import Change
import ast
import re


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
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        return imports
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


def find_dependency_order(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find the dependency order using topological sort.
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of lists, where each inner list contains files that can be committed together
    """
    from collections import defaultdict, deque
    
    # Build reverse graph (what depends on what)
    reverse_graph = defaultdict(set)
    in_degree = defaultdict(int)
    
    for file, deps in graph.items():
        for dep in deps:
            reverse_graph[dep].add(file)
            in_degree[file] += 1
    
    # Find files with no dependencies
    queue = deque([f for f in graph if in_degree[f] == 0])
    result = []
    
    while queue:
        level = []
        for _ in range(len(queue)):
            file = queue.popleft()
            level.append(file)
            
            for dependent in reverse_graph[file]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        if level:
            result.append(level)
    
    return result


def detect_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Detect circular dependencies in the graph.
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of cycles found
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    cycles = []
    
    def dfs(node: str, path: List[str]):
        if color[node] == GRAY:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:])
            return
        
        if color[node] == BLACK:
            return
        
        color[node] = GRAY
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor in color:
                dfs(neighbor, path)
        
        path.pop()
        color[node] = BLACK
    
    for node in graph:
        if color[node] == WHITE:
            dfs(node, [])
    
    return cycles


def get_critical_path(graph: Dict[str, Set[str]]) -> List[str]:
    """Find the critical path (longest dependency chain).
    
    Args:
        graph: Dependency graph mapping files to their dependencies
        
    Returns:
        List of files in the critical path
    """
    memo = {}
    
    def longest_path(node: str) -> int:
        if node not in memo:
            max_len = 0
            for dep in graph.get(node, []):
                if dep in graph:
                    max_len = max(max_len, longest_path(dep))
            memo[node] = max_len + 1
        return memo[node]
    
    # Find node with longest path
    max_length = 0
    start_node = None
    
    for node in graph:
        length = longest_path(node)
        if length > max_length:
            max_length = length
            start_node = node
    
    # Reconstruct path
    if not start_node:
        return []
    
    path = []
    current = start_node
    visited = set()
    
    while current and current not in visited:
        path.append(current)
        visited.add(current)
        
        next_node = None
        max_next = 0
        for dep in graph.get(current, []):
            if dep in graph and dep not in visited:
                if memo.get(dep, 0) > max_next:
                    max_next = memo[dep]
                    next_node = dep
        
        current = next_node
    
    return path
