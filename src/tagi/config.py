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
