"""Tests for the Koru deployment priority provider."""

from pathlib import Path

from tagi.models import Change, ChangeType, Tag
from tagi.providers.koru import KoruProvider


def _change(path, tag, risk_score=0.0):
    change = Change(path=path, change_type=ChangeType.MODIFIED)
    change.tags = [tag]
    change.risk_score = risk_score
    return change


def _provider(monkeypatch, *, topology=None, tickets=None, quality_gates=None):
    provider = KoruProvider(Path("/tmp"))
    monkeypatch.setattr(provider, "get_topology", lambda: topology if topology is not None else {})
    monkeypatch.setattr(provider, "get_planfile_tickets", lambda: tickets if tickets is not None else [])
    monkeypatch.setattr(provider, "get_context_brief", lambda: {})
    monkeypatch.setattr(provider, "run_quality_gates", lambda: quality_gates if quality_gates is not None else {})
    return provider


def test_analyze_deployment_priority_orders_groups_by_risk(monkeypatch):
    provider = _provider(
        monkeypatch,
        topology={"components": ["a", "b"]},
        tickets=[{"id": "PLF-1"}, {"id": "PLF-2"}],
    )
    changes = [
        _change("a.py", Tag.RISKY, 0.9),
        _change("b.py", Tag.CONFIG, 0.2),
        _change("c.py", Tag.DEPS, 0.3),
        _change("d.py", Tag.LARGE, 0.4),
        _change("e.py", Tag.FEATURE, 0.1),
        _change("f.py", Tag.REFACTOR, 0.05),
        _change("g.py", Tag.TESTS, 0.01),
        _change("h.py", Tag.DOCS, 0.0),
        _change("i.py", Tag.SMALL, 0.0),
    ]

    plan = provider.analyze_deployment_priority(changes)

    assert plan.priority_order == [
        "risky", "config", "deps", "large", "feature", "refactor", "tests", "docs", "small",
    ]
    assert [group["priority"] for group in plan.deployment_groups] == list(range(1, 10))
    assert [group["changes"] for group in plan.deployment_groups] == [
        ["a.py"], ["b.py"], ["c.py"], ["d.py"], ["e.py"], ["f.py"], ["g.py"], ["h.py"], ["i.py"],
    ]
    assert plan.risk_assessment == {
        "risky": 0.9, "config": 0.2, "deps": 0.3, "large": 0.4, "feature": 0.1,
        "refactor": 0.05, "tests": 0.01, "docs": 0.0, "small": 0.0,
    }
    assert plan.dependencies == {}
    assert any("High-risk" in rec for rec in plan.recommendations)
    assert any("2 components" in rec for rec in plan.recommendations)
    assert any("2 open tickets" in rec for rec in plan.recommendations)


def test_analyze_deployment_priority_no_changes_is_all_clear(monkeypatch):
    provider = _provider(monkeypatch)

    plan = provider.analyze_deployment_priority([])

    assert plan.priority_order == []
    assert plan.deployment_groups == []
    assert any("All checks passed" in rec for rec in plan.recommendations)


def test_analyze_deployment_priority_reports_quality_gate_failures(monkeypatch):
    provider = _provider(monkeypatch, quality_gates={"errors": ["boom"]})

    plan = provider.analyze_deployment_priority([])

    assert any("Quality gates failed" in rec for rec in plan.recommendations)
