"""Configuration module for tagi.toml support."""

import os
from pathlib import Path
from typing import Dict, List, Optional

try:
    import tomli
except ImportError:
    try:
        import tomllib as tomli
    except ImportError:
        tomli = None


class Config:
    """Configuration loaded from tagi.toml."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.custom_tags: Dict[str, List[str]] = {}
        self.custom_rules: Dict[str, str] = {}
        self.tag_colors: Dict[str, str] = {}
        self.custom_heuristics: Dict[str, List[str]] = {}
        self.custom_tag_definitions: Dict[str, str] = {}
        self.custom_templates: Dict[str, str] = {}
        self.ignore_patterns: List[str] = []
        self._load_config()
    
    def _load_config(self):
        """Load configuration from tagi.toml if it exists."""
        config_path = Path(self.repo_path) / "tagi.toml"
        
        if not config_path.exists():
            return
        
        if tomli is None:
            print("Warning: tomli/tomllib not available, cannot load tagi.toml")
            return
        
        try:
            with open(config_path, "rb") as f:
                data = tomli.load(f)
            
            # Load custom tags
            if "tags" in data:
                self.custom_tags = data["tags"]
            
            # Load custom rules
            if "rules" in data:
                self.custom_rules = data["rules"]
            
            # Load custom tag colors
            if "colors" in data:
                self.tag_colors = data["colors"]
            
            # Load custom heuristics
            if "heuristics" in data:
                self.custom_heuristics = data["heuristics"]
            
            # Load custom tag definitions
            if "tag_definitions" in data:
                self.custom_tag_definitions = data["tag_definitions"]
            
            # Load custom templates
            if "templates" in data:
                self.custom_templates = data["templates"]
            
            # Load ignore patterns
            if "ignore" in data:
                self.ignore_patterns = data["ignore"]
                
        except Exception as e:
            print(f"Warning: Error loading tagi.toml: {e}")
    
    def get_tag_for_path(self, path: str) -> Optional[str]:
        """Get custom tag for a file path based on rules."""
        path_lower = path.lower()
        
        for pattern, tag in self.custom_rules.items():
            if pattern.lower() in path_lower:
                return tag
        
        return None
    
    def get_custom_tags_for_pattern(self, pattern: str) -> List[str]:
        """Get custom tags for a pattern."""
        return self.custom_tags.get(pattern, [])
    
    def get_tag_color(self, tag: str) -> Optional[str]:
        """Get custom color for a tag."""
        return self.tag_colors.get(tag)
    
    def get_heuristics_for_path(self, path: str) -> List[str]:
        """Get custom heuristic tags for a file path."""
        path_lower = path.lower()
        tags = []
        
        for pattern, pattern_tags in self.custom_heuristics.items():
            if pattern.lower() in path_lower:
                tags.extend(pattern_tags)
        
        return tags
    
    def get_tag_description(self, tag: str) -> Optional[str]:
        """Get custom description for a tag."""
        return self.custom_tag_definitions.get(tag)
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get custom template by name."""
        return self.custom_templates.get(template_name)
    
    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored based on ignore patterns."""
        path_lower = path.lower()
        
        for pattern in self.ignore_patterns:
            if pattern.lower() in path_lower:
                return True
        
        return False
