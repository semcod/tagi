"""Integration tests for GitHub provider."""

import os
import tempfile
from pathlib import Path

from tagi.providers.github import GitHubProvider
from tagi.executor.git import GitExecutor


def test_github_provider_initialization():
    """Test GitHubProvider initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        provider = GitHubProvider(tmpdir)
        assert provider.repo_path == tmpdir


def test_github_provider_detect_remote():
    """Test GitHub remote detection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo with GitHub remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git remote add origin https://github.com/test/repo.git > /dev/null 2>&1")
        
        provider = GitHubProvider(tmpdir)
        assert provider.detect_remote() is True


def test_github_provider_detect_non_github_remote():
    """Test GitHub remote detection with non-GitHub remote."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo with GitLab remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git remote add origin https://gitlab.com/test/repo.git > /dev/null 2>&1")
        
        provider = GitHubProvider(tmpdir)
        assert provider.detect_remote() is False


def test_github_provider_detect_no_remote():
    """Test GitHub remote detection with no remote."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo without remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitHubProvider(tmpdir)
        assert provider.detect_remote() is False


def test_github_provider_get_auth_status():
    """Test getting authentication status."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitHubProvider(tmpdir)
        try:
            status = provider.get_auth_status()
            # Status should be a dict with 'authenticated' key
            assert isinstance(status, dict)
            assert 'authenticated' in status
        except FileNotFoundError:
            # gh CLI not installed - skip this test
            pass


def test_github_provider_is_authenticated():
    """Test authentication check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitHubProvider(tmpdir)
        try:
            result = provider.is_authenticated()
            assert isinstance(result, bool)
        except FileNotFoundError:
            # gh CLI not installed - skip this test
            pass
