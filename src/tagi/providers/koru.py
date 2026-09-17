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
    
    _GROUP_ORDER = (
        (Tag.RISKY, "risky", 1, "High-risk changes require careful deployment"),
        (Tag.CONFIG, "config", 2, "Configuration changes affect system behavior"),
        (Tag.DEPS, "deps", 3, "Dependency changes may affect other components"),
        (Tag.LARGE, "large", 4, "Large changes require careful testing"),
        (Tag.FEATURE, "feature", 5, "New features should be deployed after core changes"),
        (Tag.REFACTOR, "refactor", 6, "Refactoring changes should be deployed after features"),
        (Tag.TESTS, "tests", 7, "Test changes should be deployed with code changes"),
        (Tag.DOCS, "docs", 8, "Documentation changes have lowest priority"),
        (Tag.SMALL, "small", 9, "Small changes can be deployed last"),
    )

    def _deployment_recommendations(
        self,
        quality_gates: Dict[str, Any],
        tickets: List[Dict[str, Any]],
        topology: Dict[str, Any],
        has_risky: bool,
    ) -> List[str]:
        """Generate recommendations based on Koru context."""
        recommendations = []
        if quality_gates.get("errors"):
            recommendations.append("⚠️ Quality gates failed - fix issues before deployment")
        if tickets:
            recommendations.append(f"📋 {len(tickets)} open tickets in planfile - review before deployment")
        if topology.get("components"):
            recommendations.append(f"🏗️ {len(topology['components'])} components detected - consider impact")
        if has_risky:
            recommendations.append("🚨 High-risk changes detected - deploy with caution")
        if not recommendations:
            recommendations.append("✅ All checks passed - ready for deployment")
        return recommendations

    def analyze_deployment_priority(self, changes: List[Change]) -> KoruDeploymentPlan:
        """Analyze deployment priority using Koru API."""
        # Get project context
        topology = self.get_topology()
        tickets = self.get_planfile_tickets()
        context = self.get_context_brief()
        quality_gates = self.run_quality_gates()

        # Analyze changes with Koru context
        deployment_groups = []
        priority_order = []
        risk_assessment = {}
        dependencies = {}

        # Group changes by tag and emit deployment groups in priority order
        by_tag = {tag: [c for c in changes if tag in c.tags] for tag, *_ in self._GROUP_ORDER}
        for tag, name, priority, reason in self._GROUP_ORDER:
            group_changes = by_tag[tag]
            if not group_changes:
                continue
            deployment_groups.append({
                "name": name,
                "changes": [c.path for c in group_changes],
                "priority": priority,
                "reason": reason,
            })
            priority_order.append(name)
            risk_assessment[name] = max(c.risk_score for c in group_changes)

        recommendations = self._deployment_recommendations(
            quality_gates, tickets, topology, bool(by_tag[Tag.RISKY])
        )

        return KoruDeploymentPlan(
            priority_order=priority_order,
            deployment_groups=deployment_groups,
            risk_assessment=risk_assessment,
            dependencies=dependencies,
            recommendations=recommendations
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
