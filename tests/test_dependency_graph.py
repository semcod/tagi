"""Unit tests for the dependency graph analysis module.

These tests exercise the pure graph algorithms used by planning:
``build_dependency_graph``, ``find_dependency_order``, ``detect_cycles``
and ``get_critical_path``, plus the level-by-level Kahn partitioning.
"""

import ast

from tagi.analyzer.dependency_graph import (
    _collect_import_names,
    _LevelOrder,
    analyze_python_imports,
    build_dependency_graph,
    detect_cycles,
    find_dependency_order,
    get_critical_path,
)
from tagi.models import Change, ChangeType


def _py_change(path: str) -> Change:
    return Change(path=path, change_type=ChangeType.MODIFIED)


def _parse(source: str) -> ast.AST:
    return ast.parse(source)


class TestCollectImportNames:
    """_collect_import_names edge cases over parsed ASTs."""

    def test_plain_and_dotted_imports(self):
        names = _collect_import_names(_parse("import os\nimport os.path\n"))
        assert names == ["os", "os.path"]

    def test_aliased_import_uses_module_name(self):
        names = _collect_import_names(_parse("import numpy as np\n"))
        assert names == ["numpy"]

    def test_multiple_aliases_in_one_statement(self):
        names = _collect_import_names(_parse("import a, b\n"))
        assert names == ["a", "b"]

    def test_from_import_joins_module_and_name(self):
        names = _collect_import_names(_parse("from collections import OrderedDict\n"))
        assert names == ["collections.OrderedDict"]

    def test_from_import_multiple_names(self):
        names = _collect_import_names(_parse("from collections import deque, defaultdict\n"))
        assert names == ["collections.deque", "collections.defaultdict"]

    def test_relative_import_without_module_prefixes_dot(self):
        names = _collect_import_names(_parse("from . import sibling\n"))
        assert names == [".sibling"]

    def test_relative_import_drops_dots(self):
        names = _collect_import_names(_parse("from .rel import helper\nfrom ..pkg import mod\n"))
        assert names == ["rel.helper", "pkg.mod"]

    def test_no_imports_yields_empty_list(self):
        assert _collect_import_names(_parse("x = 1\nprint(x)\n")) == []


class TestAnalyzePythonImports:
    """analyze_python_imports reads files under repo_path."""

    def test_returns_collected_imports(self, tmp_path):
        module = tmp_path / "pkg" / "mod.py"
        module.parent.mkdir()
        module.write_text("import os\nfrom tagi.models import change\n")
        assert analyze_python_imports("pkg/mod.py", str(tmp_path)) == [
            "os",
            "tagi.models.change",
        ]

    def test_missing_file_returns_empty_list(self, tmp_path):
        assert analyze_python_imports("gone.py", str(tmp_path)) == []

    def test_syntax_error_returns_empty_list(self, tmp_path):
        broken = tmp_path / "broken.py"
        broken.write_text("def oops(:\n")
        assert analyze_python_imports("broken.py", str(tmp_path)) == []


class TestBuildDependencyGraph:
    """build_dependency_graph maps change paths to import dependencies."""

    def test_python_changes_carry_import_dependencies(self, tmp_path):
        module = tmp_path / "pkg" / "mod.py"
        module.parent.mkdir()
        module.write_text("import os\nfrom tagi.models import change\n")
        changes = [
            _py_change("pkg/mod.py"),
            _py_change("pkg/other.py"),
        ]
        (tmp_path / "pkg" / "other.py").write_text("import json\n")
        graph = build_dependency_graph(changes, repo_path=str(tmp_path))
        assert graph == {
            "pkg/mod.py": {"os", "tagi.models.change"},
            "pkg/other.py": {"json"},
        }

    def test_non_python_changes_have_no_dependencies(self, tmp_path):
        (tmp_path / "README.md").write_text("docs")
        changes = [
            _py_change("README.md"),
            Change(path="data/config.yaml", change_type=ChangeType.ADDED),
        ]
        graph = build_dependency_graph(changes, repo_path=str(tmp_path))
        assert graph == {"README.md": set(), "data/config.yaml": set()}

    def test_missing_python_file_yields_empty_dependency_set(self, tmp_path):
        graph = build_dependency_graph([_py_change("gone.py")], repo_path=str(tmp_path))
        assert graph == {"gone.py": set()}

    def test_empty_change_list_yields_empty_graph(self, tmp_path):
        assert build_dependency_graph([], repo_path=str(tmp_path)) == {}


class TestFindDependencyOrder:
    """find_dependency_order returns level groups, dependencies first."""

    def test_empty_graph_returns_empty_list(self):
        assert find_dependency_order({}) == []

    def test_order_is_deterministic_for_insertion_ordered_graph(self):
        graph = {
            "app.py": {"lib.py"},
            "lib.py": {"core.py"},
            "core.py": set(),
            "doc.md": set(),
        }
        assert find_dependency_order(graph) == [
            ["core.py", "doc.md"],
            ["lib.py"],
            ["app.py"],
        ]

    def test_independent_files_share_one_level(self):
        assert find_dependency_order({"a.py": set(), "b.py": set(), "c.py": set()}) == [
            ["a.py", "b.py", "c.py"]
        ]

    def test_dependencies_appear_in_earlier_levels_than_dependents(self):
        graph = {
            "a.py": set(),
            "b.py": {"a.py"},
            "c.py": {"a.py"},
            "d.py": {"b.py", "c.py"},
            "e.py": set(),
        }
        levels = find_dependency_order(graph)
        level_of = {
            file: index for index, level in enumerate(levels) for file in level
        }
        assert sorted(level_of) == ["a.py", "b.py", "c.py", "d.py", "e.py"]
        for file, deps in graph.items():
            for dep in deps:
                assert level_of[dep] < level_of[file]

    def test_chain_gets_one_file_per_level(self):
        graph = {"c.py": {"b.py"}, "b.py": {"a.py"}, "a.py": set()}
        assert find_dependency_order(graph) == [["a.py"], ["b.py"], ["c.py"]]


class TestDetectCycles:
    """detect_cycles reports gray-on-gray DFS back edges as cycles."""

    def test_acyclic_graph_returns_empty_list(self):
        graph = {"a.py": {"b.py"}, "b.py": {"c.py"}, "c.py": set()}
        assert detect_cycles(graph) == []

    def test_empty_graph_returns_empty_list(self):
        assert detect_cycles({}) == []

    def test_two_node_cycle_is_reported(self):
        graph = {"a.py": {"b.py"}, "b.py": {"a.py"}}
        assert detect_cycles(graph) == [["a.py", "b.py"]]

    def test_three_node_cycle_is_reported_in_path_order(self):
        graph = {"a.py": {"b.py"}, "b.py": {"c.py"}, "c.py": {"a.py"}}
        assert detect_cycles(graph) == [["a.py", "b.py", "c.py"]]

    def test_self_loop_is_reported(self):
        assert detect_cycles({"a.py": {"a.py"}}) == [["a.py"]]

    def test_two_cycles_sharing_a_node_are_both_reported(self):
        graph = {"a.py": {"b.py", "c.py"}, "b.py": {"a.py"}, "c.py": {"a.py"}}
        cycles = detect_cycles(graph)
        assert sorted(tuple(cycle) for cycle in cycles) == [
            ("a.py", "b.py"),
            ("a.py", "c.py"),
        ]

    def test_dependencies_outside_graph_are_ignored(self):
        assert detect_cycles({"a.py": {"os"}}) == []

    def test_finished_node_revisited_via_second_edge_records_no_cycle(self):
        graph = {
            "a.py": {"b.py", "c.py"},
            "b.py": {"d.py"},
            "c.py": {"d.py"},
            "d.py": set(),
        }
        assert detect_cycles(graph) == []


class TestGetCriticalPath:
    """get_critical_path walks the longest dependency chain."""

    def test_empty_graph_returns_empty_list(self):
        assert get_critical_path({}) == []

    def test_single_node_graph_returns_that_node(self):
        assert get_critical_path({"a.py": set()}) == ["a.py"]

    def test_diamond_graph_returns_longest_leg(self):
        graph = {
            "top.py": {"left.py", "right.py"},
            "left.py": {"base.py"},
            "right.py": {"mid.py"},
            "mid.py": {"base.py"},
            "base.py": set(),
        }
        assert get_critical_path(graph) == ["top.py", "right.py", "mid.py", "base.py"]

    def test_symmetric_diamond_returns_three_node_path(self):
        graph = {
            "top.py": {"left.py", "right.py"},
            "left.py": {"base.py"},
            "right.py": {"base.py"},
            "base.py": set(),
        }
        path = get_critical_path(graph)
        assert len(path) == 3
        assert path[0] == "top.py"
        assert path[-1] == "base.py"
        assert path[1] in {"left.py", "right.py"}
        assert len(set(path)) == 3

    def test_dependencies_outside_graph_are_ignored(self):
        assert get_critical_path({"a.py": {"os"}, "b.py": set()}) == ["a.py"]


class TestLevelOrderPartitioning:
    """_LevelOrder.levels/_drain_level split the graph into commit groups."""

    def test_levels_returns_one_list_per_level(self):
        graph = {"a.py": set(), "b.py": {"a.py"}, "c.py": {"b.py"}}
        assert _LevelOrder(graph).levels() == [["a.py"], ["b.py"], ["c.py"]]

    def test_levels_skips_empty_drains(self):
        assert _LevelOrder({}).levels() == []

    def test_drain_level_returns_one_group_per_call(self):
        order = _LevelOrder({"a.py": set(), "b.py": set(), "c.py": {"a.py", "b.py"}})
        assert sorted(order._drain_level()) == ["a.py", "b.py"]
        assert order._drain_level() == ["c.py"]
        assert order._drain_level() == []

    def test_levels_groups_unblocked_files_together(self):
        graph = {"a.py": set(), "b.py": set(), "c.py": {"a.py"}, "d.py": {"a.py", "b.py"}}
        levels = _LevelOrder(graph).levels()
        assert len(levels) == 2
        assert sorted(levels[0]) == ["a.py", "b.py"]
        assert sorted(levels[1]) == ["c.py", "d.py"]
