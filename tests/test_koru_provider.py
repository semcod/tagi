"""Unit tests for Koru provider (no network)."""

from pathlib import Path

import pytest

import httpx

from tagi.models.change import Change, ChangeType, Tag
from tagi.providers.koru import KoruDeploymentPlan, KoruProvider


class FakeResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json_data = json_data if json_data is not None else {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "server error", request=None, response=None
            )

    def json(self):
        return self._json_data


class FakeClient:
    post_responses = []
    get_responses = []
    post_calls = []
    get_calls = []

    def __init__(self, timeout=None):
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def post(self, url, json=None):
        FakeClient.post_calls.append({"url": url, "json": json})
        response = FakeClient.post_responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    def get(self, url):
        FakeClient.get_calls.append({"url": url})
        response = FakeClient.get_responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def fake_httpx(monkeypatch):
    FakeClient.post_responses = []
    FakeClient.get_responses = []
    FakeClient.post_calls = []
    FakeClient.get_calls = []
    monkeypatch.setattr(httpx, "Client", FakeClient)
    return FakeClient


def make_change(path, tags, risk_score=0.0):
    return Change(
        path=path,
        change_type=ChangeType.MODIFIED,
        tags=list(tags),
        risk_score=risk_score,
    )


def test_koru_provider_initialization():
    provider = KoruProvider(Path("/tmp/proj"), koru_host="localhost", koru_port=9000)
    assert provider.project_path == Path("/tmp/proj")
    assert provider.koru_host == "localhost"
    assert provider.koru_port == 9000
    assert provider.base_url == "http://localhost:9000"


def test_defaults():
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.koru_host == "127.0.0.1"
    assert provider.koru_port == 8790
    assert provider.base_url == "http://127.0.0.1:8790"


def test_make_api_request_success(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"result": "ok"})]
    provider = KoruProvider(Path("/tmp/proj"))
    response = provider._make_api_request("topology.read", "read", {"k": "v"})
    assert response == {"result": "ok"}
    call = fake_httpx.post_calls[0]
    assert call["url"] == "http://127.0.0.1:8790/invoke"
    assert call["json"] == {
        "integration_id": "topology.read",
        "method": "read",
        "project": "/tmp/proj",
        "body": {"k": "v"},
    }


def test_make_api_request_default_method_and_payload(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"result": 1})]
    provider = KoruProvider(Path("/tmp/proj"))
    provider._make_api_request("mcp.quality_gates")
    call = fake_httpx.post_calls[0]
    assert call["json"]["method"] == "run"
    assert call["json"]["body"] == {}


def test_make_api_request_error_returns_empty(fake_httpx):
    fake_httpx.post_responses = [RuntimeError("connection refused")]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider._make_api_request("topology.read") == {}


def test_make_api_request_http_error_returns_empty(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({}, status_code=500)]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider._make_api_request("topology.read") == {}


def test_get_topology(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"components": ["a", "b"]})]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.get_topology() == {"components": ["a", "b"]}
    assert fake_httpx.post_calls[0]["json"]["integration_id"] == "topology.read"
    assert fake_httpx.post_calls[0]["json"]["method"] == "read"


def test_get_planfile_tickets(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"tickets": [{"id": "PLF-1"}]})]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.get_planfile_tickets() == [{"id": "PLF-1"}]
    assert fake_httpx.post_calls[0]["json"]["integration_id"] == "planfile.tickets"
    assert fake_httpx.post_calls[0]["json"]["method"] == "list"


def test_get_planfile_tickets_missing_key(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({})]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.get_planfile_tickets() == []


def test_run_quality_gates(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"errors": ["gate failed"]})]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.run_quality_gates() == {"errors": ["gate failed"]}
    assert fake_httpx.post_calls[0]["json"]["integration_id"] == "mcp.quality_gates"
    assert fake_httpx.post_calls[0]["json"]["method"] == "run"


def test_get_context_brief(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"brief": "ctx"})]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.get_context_brief() == {"brief": "ctx"}
    assert fake_httpx.post_calls[0]["json"]["integration_id"] == "context.build"
    assert fake_httpx.post_calls[0]["json"]["method"] == "build"


def _api_responses(fake_httpx, *, tickets=None, topology=None, gates=None):
    fake_httpx.post_responses = [
        FakeResponse(topology if topology is not None else {}),
        FakeResponse({"tickets": tickets if tickets is not None else []}),
        FakeResponse({}),
        FakeResponse(gates if gates is not None else {}),
    ]


def test_analyze_deployment_priority_groups_and_order(fake_httpx):
    _api_responses(fake_httpx)
    provider = KoruProvider(Path("/tmp/proj"))
    changes = [
        make_change("src/feat.py", [Tag.FEATURE, Tag.LARGE], risk_score=3.0),
        make_change("docs/readme.md", [Tag.DOCS, Tag.SMALL], risk_score=1.0),
        make_change("src/risky.py", [Tag.RISKY], risk_score=9.0),
    ]
    plan = provider.analyze_deployment_priority(changes)

    assert isinstance(plan, KoruDeploymentPlan)
    assert plan.priority_order == ["risky", "large", "feature", "docs", "small"]
    names = [g["name"] for g in plan.deployment_groups]
    assert names == plan.priority_order
    risky_group = plan.deployment_groups[0]
    assert risky_group["name"] == "risky"
    assert risky_group["priority"] == 1
    assert risky_group["changes"] == ["src/risky.py"]
    assert risky_group["reason"] == "High-risk changes require careful deployment"
    large_group = plan.deployment_groups[1]
    assert large_group["changes"] == ["src/feat.py"]
    feature_group = plan.deployment_groups[2]
    assert feature_group["changes"] == ["src/feat.py"]
    docs_group = plan.deployment_groups[3]
    assert docs_group["changes"] == ["docs/readme.md"]
    small_group = plan.deployment_groups[4]
    assert small_group["changes"] == ["docs/readme.md"]
    assert plan.dependencies == {}


def test_analyze_deployment_priority_risk_is_max_per_group(fake_httpx):
    _api_responses(fake_httpx)
    provider = KoruProvider(Path("/tmp/proj"))
    changes = [
        make_change("src/a.py", [Tag.FEATURE], risk_score=2.5),
        make_change("src/b.py", [Tag.FEATURE, Tag.TESTS], risk_score=7.5),
        make_change("src/c.py", [Tag.FEATURE], risk_score=4.0),
    ]
    plan = provider.analyze_deployment_priority(changes)
    assert plan.risk_assessment["feature"] == 7.5
    assert plan.risk_assessment["tests"] == 7.5
    assert "risky" not in plan.risk_assessment


def test_analyze_deployment_priority_empty_changes(fake_httpx):
    _api_responses(fake_httpx)
    provider = KoruProvider(Path("/tmp/proj"))
    plan = provider.analyze_deployment_priority([])
    assert plan.priority_order == []
    assert plan.deployment_groups == []
    assert plan.risk_assessment == {}
    assert plan.recommendations == [
        "✅ All checks passed - ready for deployment"
    ]


@pytest.mark.parametrize(
    "tickets,topology,gates,has_risky,expected",
    [
        (
            [],
            {},
            {},
            False,
            ["✅ All checks passed - ready for deployment"],
        ),
        (
            [{"id": "PLF-1"}, {"id": "PLF-2"}],
            {"components": ["c1", "c2", "c3"]},
            {"errors": ["lint"]},
            True,
            [
                "⚠️ Quality gates failed - fix issues before deployment",
                "📋 2 open tickets in planfile - review before deployment",
                "🏗️ 3 components detected - consider impact",
                "🚨 High-risk changes detected - deploy with caution",
            ],
        ),
    ],
)
def test_deployment_recommendations_branches(
    fake_httpx, tickets, topology, gates, has_risky, expected
):
    recommendations = KoruProvider(Path("/tmp/proj"))._deployment_recommendations(
        gates, tickets, topology, has_risky
    )
    assert recommendations == expected


def test_analyze_deployment_priority_all_recommendations(fake_httpx):
    _api_responses(
        fake_httpx,
        tickets=[{"id": "PLF-1"}],
        topology={"components": ["c1"]},
        gates={"errors": ["e"]},
    )
    provider = KoruProvider(Path("/tmp/proj"))
    plan = provider.analyze_deployment_priority(
        [make_change("src/x.py", [Tag.RISKY], risk_score=5.0)]
    )
    assert plan.recommendations == [
        "⚠️ Quality gates failed - fix issues before deployment",
        "📋 1 open tickets in planfile - review before deployment",
        "🏗️ 1 components detected - consider impact",
        "🚨 High-risk changes detected - deploy with caution",
    ]


def test_deploy_group_success(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({"success": True})]
    provider = KoruProvider(Path("/tmp/proj"))
    changes = [make_change("src/a.py", [Tag.FEATURE])]
    assert provider.deploy_group("feature", changes, dry_run=False) is True
    call = fake_httpx.post_calls[0]
    assert call["json"]["integration_id"] == "deploy.group"
    assert call["json"]["method"] == "deploy"
    assert call["json"]["body"] == {
        "group": "feature",
        "changes": ["src/a.py"],
        "dry_run": False,
    }


def test_deploy_group_defaults_to_dry_run_and_failure(fake_httpx):
    fake_httpx.post_responses = [FakeResponse({})]
    provider = KoruProvider(Path("/tmp/proj"))
    changes = [make_change("src/a.py", [Tag.DOCS])]
    assert provider.deploy_group("docs", changes) is False
    assert fake_httpx.post_calls[0]["json"]["body"]["dry_run"] is True


def test_deploy_group_error_returns_false(fake_httpx):
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.deploy_group("docs", None) is False
    assert fake_httpx.post_calls == []


def test_is_available_true(fake_httpx):
    fake_httpx.get_responses = [FakeResponse({}, status_code=200)]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.is_available() is True
    assert fake_httpx.get_calls[0]["url"] == "http://127.0.0.1:8790/"


def test_is_available_non_200(fake_httpx):
    fake_httpx.get_responses = [FakeResponse({}, status_code=404)]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.is_available() is False


def test_is_available_error(fake_httpx):
    fake_httpx.get_responses = [ConnectionError("no server")]
    provider = KoruProvider(Path("/tmp/proj"))
    assert provider.is_available() is False
