"""Configuration module for tagi.toml support."""

import os
from pathlib import Path
from typing import Dict, List, Optional

from tagi.utils.paths import path_matches

try:
    import tomli
except ImportError:
    try:
        import tomllib as tomli
    except ImportError:
        tomli = None


_SECTION_ATTRIBUTES = {
    "tags": "custom_tags",
    "rules": "custom_rules",
    "colors": "tag_colors",
    "heuristics": "custom_heuristics",
    "tag_definitions": "custom_tag_definitions",
    "templates": "custom_templates",
    "ignore": "ignore_patterns",
}


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
        self.llm_enabled: bool = False
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
        except Exception as e:
            print(f"Warning: Error loading tagi.toml: {e}")
            return

        self._apply_sections(data)

    def _apply_sections(self, data):
        """Copy recognised tagi.toml sections onto config attributes."""
        for section, attribute in _SECTION_ATTRIBUTES.items():
            if section in data:
                setattr(self, attribute, data[section])

        if "llm" in data:
            self.llm_enabled = data["llm"].get("enabled", False)

    
    def get_tag_for_path(self, path: str) -> Optional[str]:
        """Get custom tag for a file path based on rules."""
        for pattern, tag in self.custom_rules.items():
            if path_matches(path, pattern):
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
        tags = []

        for pattern, pattern_tags in self.custom_heuristics.items():
            if path_matches(path, pattern):
                tags.extend(pattern_tags)

        return tags

    def get_tags_for_path(self, path: str) -> List[str]:
        """Get all custom tags for a file path: rule tag first, then heuristic tags."""
        tag = self.get_tag_for_path(path)
        return ([tag] if tag else []) + self.get_heuristics_for_path(path)
    
    def get_tag_description(self, tag: str) -> Optional[str]:
        """Get custom description for a tag."""
        return self.custom_tag_definitions.get(tag)
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get custom template by name."""
        return self.custom_templates.get(template_name)
    
    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored based on ignore patterns."""
        return any(path_matches(path, pattern) for pattern in self.ignore_patterns)


def load_config(repo_path: str = ".") -> Config:
    """Load the repository configuration (single construction point)."""
    return Config(repo_path)
