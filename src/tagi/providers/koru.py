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
        
        # Group changes by type and risk
        risky_changes = [c for c in changes if Tag.RISKY in c.tags]
        large_changes = [c for c in changes if Tag.LARGE in c.tags]
        config_changes = [c for c in changes if Tag.CONFIG in c.tags]
        deps_changes = [c for c in changes if Tag.DEPS in c.tags]
        test_changes = [c for c in changes if Tag.TESTS in c.tags]
        docs_changes = [c for c in changes if Tag.DOCS in c.tags]
        feature_changes = [c for c in changes if Tag.FEATURE in c.tags]
        refactor_changes = [c for c in changes if Tag.REFACTOR in c.tags]
        small_changes = [c for c in changes if Tag.SMALL in c.tags]
        
        # Build deployment plan based on Koru analysis
        if risky_changes:
            deployment_groups.append({
                "name": "risky",
                "changes": [c.path for c in risky_changes],
                "priority": 1,
                "reason": "High-risk changes require careful deployment"
            })
            priority_order.append("risky")
            risk_assessment["risky"] = max(c.risk_score for c in risky_changes)
        
        if config_changes:
            deployment_groups.append({
                "name": "config",
                "changes": [c.path for c in config_changes],
                "priority": 2,
                "reason": "Configuration changes affect system behavior"
            })
            priority_order.append("config")
            risk_assessment["config"] = max(c.risk_score for c in config_changes)
        
        if deps_changes:
            deployment_groups.append({
                "name": "deps",
                "changes": [c.path for c in deps_changes],
                "priority": 3,
                "reason": "Dependency changes may affect other components"
            })
            priority_order.append("deps")
            risk_assessment["deps"] = max(c.risk_score for c in deps_changes)
        
        if large_changes:
            deployment_groups.append({
                "name": "large",
                "changes": [c.path for c in large_changes],
                "priority": 4,
                "reason": "Large changes require careful testing"
            })
            priority_order.append("large")
            risk_assessment["large"] = max(c.risk_score for c in large_changes)
        
        if feature_changes:
            deployment_groups.append({
                "name": "feature",
                "changes": [c.path for c in feature_changes],
                "priority": 5,
                "reason": "New features should be deployed after core changes"
            })
            priority_order.append("feature")
            risk_assessment["feature"] = max(c.risk_score for c in feature_changes)
        
        if refactor_changes:
            deployment_groups.append({
                "name": "refactor",
                "changes": [c.path for c in refactor_changes],
                "priority": 6,
                "reason": "Refactoring changes should be deployed after features"
            })
            priority_order.append("refactor")
            risk_assessment["refactor"] = max(c.risk_score for c in refactor_changes)
        
        if test_changes:
            deployment_groups.append({
                "name": "tests",
                "changes": [c.path for c in test_changes],
                "priority": 7,
                "reason": "Test changes should be deployed with code changes"
            })
            priority_order.append("tests")
            risk_assessment["tests"] = max(c.risk_score for c in test_changes)
        
        if docs_changes:
            deployment_groups.append({
                "name": "docs",
                "changes": [c.path for c in docs_changes],
                "priority": 8,
                "reason": "Documentation changes have lowest priority"
            })
            priority_order.append("docs")
            risk_assessment["docs"] = max(c.risk_score for c in docs_changes)
        
        if small_changes:
            deployment_groups.append({
                "name": "small",
                "changes": [c.path for c in small_changes],
                "priority": 9,
                "reason": "Small changes can be deployed last"
            })
            priority_order.append("small")
            risk_assessment["small"] = max(c.risk_score for c in small_changes)
        
        # Generate recommendations based on Koru context
        recommendations = []
        
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
