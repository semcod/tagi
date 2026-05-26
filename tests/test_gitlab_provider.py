"""Integration tests for GitLab provider."""

import os
import tempfile

from tagi.providers.gitlab import GitLabProvider


def test_gitlab_provider_initialization():
    """Test GitLabProvider initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        provider = GitLabProvider(tmpdir)
        assert provider.repo_path == tmpdir


def test_gitlab_provider_detect_remote():
    """Test GitLab remote detection."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo with GitLab remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git remote add origin https://gitlab.com/test/repo.git > /dev/null 2>&1")
        
        provider = GitLabProvider(tmpdir)
        assert provider.detect_remote() is True


def test_gitlab_provider_detect_non_gitlab_remote():
    """Test GitLab remote detection with non-GitLab remote."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo with GitHub remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git remote add origin https://github.com/test/repo.git > /dev/null 2>&1")
        
        provider = GitLabProvider(tmpdir)
        assert provider.detect_remote() is False


def test_gitlab_provider_detect_no_remote():
    """Test GitLab remote detection with no remote."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo without remote
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitLabProvider(tmpdir)
        assert provider.detect_remote() is False


def test_gitlab_provider_get_auth_status():
    """Test getting authentication status."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitLabProvider(tmpdir)
        try:
            status = provider.get_auth_status()
            # Status should be a dict with 'authenticated' key
            assert isinstance(status, dict)
            assert 'authenticated' in status
        except FileNotFoundError:
            # glab CLI not installed - skip this test
            pass


def test_gitlab_provider_is_authenticated():
    """Test authentication check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        
        provider = GitLabProvider(tmpdir)
        try:
            # This should not raise an exception
            result = provider.is_authenticated()
            assert isinstance(result, bool)
        except FileNotFoundError:
            # glab CLI not installed - skip this test
            pass
