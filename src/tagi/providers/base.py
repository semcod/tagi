"""Base provider module for Git hosting integrations."""

from abc import ABC, abstractmethod
from typing import List


class BaseProvider(ABC):
    """Base class for Git hosting providers."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if the provider is authenticated."""
        pass
    
    @abstractmethod
    def create_pr(self, title: str, body: str, branch: str, base: str = "main",
                  draft: bool = False, labels: List[str] = None) -> str:
        """Create a pull/merge request."""
        pass
