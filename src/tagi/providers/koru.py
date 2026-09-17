"""Koru integration provider for deployment priority analysis."""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from tagi.models.change import Change, Tag
from tagi.utils.logger import setup_logger

logger = setup_logger()


@dataclass
class KoruDeploymentPlan:
    """Deployment plan from Koru API."""
    priority_order: List[str]
    deployment_groups: List[Dict[str, Any]]
    risk_assessment: Dict[str, float]
    dependencies: Dict[str, List[str]]
    recommendations: List[str]


_DEPLOYMENT_GROUP_SPECS = [
    ("risky", Tag.RISKY, 1, "High-risk changes require careful deployment"),
    ("config", Tag.CONFIG, 2, "Configuration changes affect system behavior"),
    ("deps", Tag.DEPS, 3, "Dependency changes may affect other components"),
    ("large", Tag.LARGE, 4, "Large changes require careful testing"),
    ("feature", Tag.FEATURE, 5, "New features should be deployed after core changes"),
    ("refactor", Tag.REFACTOR, 6, "Refactoring changes should be deployed after features"),
    ("tests", Tag.TESTS, 7, "Test changes should be deployed with code changes"),
    ("docs", Tag.DOCS, 8, "Documentation changes have lowest priority"),
    ("small", Tag.SMALL, 9, "Small changes can be deployed last"),
]


class KoruProvider:
    """Integration with Koru API for deployment analysis."""
    
    def __init__(self, project_path: Path, koru_host: str = "127.0.0.1", koru_port: int = 8790):
        self.project_path = project_path
        self.koru_host = koru_host
        self.koru_port = koru_port
        self.base_url = f"http://{koru_host}:{koru_port}"
    
    def _make_api_request(self, integration_id: str, method: str = "run", payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Make request to Koru API."""
        try:
            import httpx
            
            request_data = {
                "integration_id": integration_id,
                "method": method,
                "project": str(self.project_path),
                "body": payload or {}
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(f"{self.base_url}/invoke", json=request_data)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.warning(f"Koru API request failed: {e}")
            return {}
    
    def get_topology(self) -> Dict[str, Any]:
        """Get project topology from Koru."""
        return self._make_api_request("topology.read", "read")
    
    def get_planfile_tickets(self) -> List[Dict[str, Any]]:
        """Get planfile tickets from Koru."""
        response = self._make_api_request("planfile.tickets", "list")
        return response.get("tickets", [])
    
    def run_quality_gates(self) -> Dict[str, Any]:
        """Run quality gates via Koru."""
        return self._make_api_request("mcp.quality_gates", "run")
    
    def get_context_brief(self) -> Dict[str, Any]:
        """Get LLM context brief from Koru."""
        return self._make_api_request("context.build", "build")
    
    @staticmethod
    def _build_deployment_group(name: str, tag: Tag, priority: int, reason: str, changes: List[Change]) -> Optional[tuple]:
        """Build one deployment group when any change carries the tag."""
        matching = [c for c in changes if tag in c.tags]
        if not matching:
            return None
        group = {
            "name": name,
            "changes": [c.path for c in matching],
            "priority": priority,
            "reason": reason,
        }
        risk = max(c.risk_score for c in matching)
        return group, risk

    def _build_deployment_groups(self, changes: List[Change]) -> tuple:
        """Group changes by tag into ordered deployment groups."""
        deployment_groups = []
        priority_order = []
        risk_assessment = {}
        for name, tag, priority, reason in _DEPLOYMENT_GROUP_SPECS:
            result = self._build_deployment_group(name, tag, priority, reason, changes)
            if result is None:
                continue
            group, risk = result
            deployment_groups.append(group)
            priority_order.append(name)
            risk_assessment[name] = risk
        return deployment_groups, priority_order, risk_assessment

    def _build_recommendations(self, topology: Dict[str, Any], tickets: List[Dict[str, Any]], quality_gates: Dict[str, Any], changes: List[Change]) -> List[str]:
        """Generate deployment recommendations from Koru context."""
        recommendations = []
        risky_changes = [c for c in changes if Tag.RISKY in c.tags]
        if quality_gates.get("errors"):
            recommendations.append("⚠️ Quality gates failed - fix issues before deployment")
        if tickets:
            recommendations.append(f"📋 {len(tickets)} open tickets in planfile - review before deployment")
        if topology.get("components"):
            recommendations.append(f"🏗️ {len(topology['components'])} components detected - consider impact")
        if risky_changes:
            recommendations.append("🚨 High-risk changes detected - deploy with caution")
        if not recommendations:
            recommendations.append("✅ All checks passed - ready for deployment")
        return recommendations

    def analyze_deployment_priority(self, changes: List[Change]) -> KoruDeploymentPlan:
        """Analyze deployment priority using Koru API."""
        # Get project context
        topology = self.get_topology()
        tickets = self.get_planfile_tickets()
        self.get_context_brief()
        quality_gates = self.run_quality_gates()

        deployment_groups, priority_order, risk_assessment = self._build_deployment_groups(changes)
        recommendations = self._build_recommendations(topology, tickets, quality_gates, changes)

        return KoruDeploymentPlan(
            priority_order=priority_order,
            deployment_groups=deployment_groups,
            risk_assessment=risk_assessment,
            dependencies={},
            recommendations=recommendations,
        )
    
    def deploy_group(self, group_name: str, changes: List[Change], dry_run: bool = True) -> bool:
        """Deploy a specific group using Koru deployment strategy."""
        try:
            # Use Koru's deployment strategy
            payload = {
                "group": group_name,
                "changes": [c.path for c in changes],
                "dry_run": dry_run
            }
            
            response = self._make_api_request("deploy.group", "deploy", payload)
            return response.get("success", False)
            
        except Exception as e:
            logger.error(f"Deployment failed for group {group_name}: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Koru API is available."""
        try:
            import httpx
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/")
                return response.status_code == 200
        except Exception:
            return False
