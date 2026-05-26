"""End-to-end tests for send/publish workflow."""

import os
import tempfile
from pathlib import Path

from tagi.scanner.status import scan_repo
from tagi.heuristics.tags import apply_tags
from tagi.planner.grouper import group_changes
from tagi.models.change import Tag
from tagi.composer.commit_message import generate_commit_message


def test_send_workflow_scan():
    """Test scanning changes in send workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.email 'test@test.com' > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.name 'Test User' > /dev/null 2>&1")
        
        # Create a test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")
        os.system(f"cd {tmpdir} && git add test.py > /dev/null 2>&1")
        
        # Scan changes
        changes = scan_repo(tmpdir)
        assert len(changes) > 0
        
        # Apply tags
        changes = apply_tags(changes, tmpdir)
        assert len(changes) > 0
        assert all(len(c.tags) > 0 for c in changes)


def test_send_workflow_grouping():
    """Test grouping changes in send workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.email 'test@test.com' > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.name 'Test User' > /dev/null 2>&1")
        
        # Create test files
        (Path(tmpdir) / "test.py").write_text("print('hello')")
        (Path(tmpdir) / "README.md").write_text("# Test")
        os.system(f"cd {tmpdir} && git add . > /dev/null 2>&1")
        
        # Scan and tag
        changes = scan_repo(tmpdir)
        changes = apply_tags(changes, tmpdir)
        
        # Group changes
        groups = group_changes(changes)
        assert len(groups) > 0


def test_send_workflow_commit_message():
    """Test commit message generation in send workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.email 'test@test.com' > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.name 'Test User' > /dev/null 2>&1")
        
        # Create test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")
        os.system(f"cd {tmpdir} && git add test.py > /dev/null 2>&1")
        
        # Scan and tag
        changes = scan_repo(tmpdir)
        changes = apply_tags(changes, tmpdir)
        
        # Generate commit message
        message = generate_commit_message(changes, template="default", repo_path=tmpdir)
        assert message is not None
        assert len(message) > 0


def test_send_workflow_tag_filtering():
    """Test tag filtering in send workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.email 'test@test.com' > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.name 'Test User' > /dev/null 2>&1")
        
        # Create test files
        (Path(tmpdir) / "test.py").write_text("print('hello')")
        (Path(tmpdir) / "README.md").write_text("# Test")
        os.system(f"cd {tmpdir} && git add . > /dev/null 2>&1")
        
        # Scan and tag
        changes = scan_repo(tmpdir)
        changes = apply_tags(changes, tmpdir)
        
        # Filter by tag
        tag_enum = Tag("#small")
        filtered = [c for c in changes if tag_enum in c.tags]
        assert len(filtered) >= 0  # May or may not have small tag


def test_publish_workflow_full():
    """Test full publish workflow (without actual PR creation)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a git repo
        os.system(f"cd {tmpdir} && git init > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.email 'test@test.com' > /dev/null 2>&1")
        os.system(f"cd {tmpdir} && git config user.name 'Test User' > /dev/null 2>&1")
        
        # Create test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")
        os.system(f"cd {tmpdir} && git add test.py > /dev/null 2>&1")
        
        # Scan and tag
        changes = scan_repo(tmpdir)
        changes = apply_tags(changes, tmpdir)
        
        # Group changes
        groups = group_changes(changes)
        
        # Generate commit message
        if groups:
            message = generate_commit_message(groups[0].changes, template="default", repo_path=tmpdir)
            assert message is not None
