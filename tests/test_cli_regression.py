"""Regression tests for CLI functionality before refactoring."""

import subprocess
import tempfile
from pathlib import Path
import pytest
from typer.testing import CliRunner

from tagi.cli import app


class TestCLIRegression:
    """Regression tests to ensure CLI functionality works before and after refactoring."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def test_cli_help(self):
        """Test CLI help command works."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tagi" in result.stdout
        assert "Git change orchestrator" in result.stdout
        
    def test_scan_command_help(self):
        """Test scan command help works."""
        result = self.runner.invoke(app, ["scan", "--help"])
        assert result.exit_code == 0
        assert "Scan repository" in result.stdout
        
    def test_send_command_help(self):
        """Test send command help works."""
        result = self.runner.invoke(app, ["send", "--help"])
        assert result.exit_code == 0
        assert "Stage, commit" in result.stdout
        
    def test_inspect_command_help(self):
        """Test inspect command help works."""
        result = self.runner.invoke(app, ["inspect", "--help"])
        assert result.exit_code == 0
        assert "Inspect a specific" in result.stdout
        
    def test_publish_command_help(self):
        """Test publish command help works."""
        result = self.runner.invoke(app, ["publish", "--help"])
        assert result.exit_code == 0
        assert "Create a PR" in result.stdout
        
    def test_auto_command_help(self):
        """Test auto command help works."""
        result = self.runner.invoke(app, ["auto", "--help"])
        assert result.exit_code == 0
        assert "Automatically" in result.stdout
        
    def test_deploy_command_help(self):
        """Test deploy command help works."""
        result = self.runner.invoke(app, ["deploy", "--help"])
        assert result.exit_code == 0
        assert "Deploy changes" in result.stdout
        
    def test_stats_command_help(self):
        """Test stats command help works."""
        result = self.runner.invoke(app, ["stats", "--help"])
        assert result.exit_code == 0
        assert "Show statistics" in result.stdout
        
    def test_filter_command_help(self):
        """Test filter command help works."""
        result = self.runner.invoke(app, ["filter", "--help"])
        assert result.exit_code == 0
        assert "Filter changes" in result.stdout
        
    def test_draft_command_help(self):
        """Test draft command help works."""
        result = self.runner.invoke(app, ["draft", "--help"])
        assert result.exit_code == 0
        assert "Draft a commit" in result.stdout
        
    def test_list_command_help(self):
        """Test list command help works."""
        result = self.runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "List available" in result.stdout
        
    def test_file_command_help(self):
        """Test file command help works."""
        result = self.runner.invoke(app, ["file", "--help"])
        assert result.exit_code == 0
        assert "Show detailed" in result.stdout and "file" in result.stdout
        
    def test_summary_command_help(self):
        """Test summary command help works."""
        result = self.runner.invoke(app, ["summary", "--help"])
        assert result.exit_code == 0
        assert "Generate a comprehensive" in result.stdout
        
    def test_detect_provider_function_exists(self):
        """Test detect_provider function exists and is importable."""
        from tagi.cli import detect_provider
        assert callable(detect_provider)
        
    def test_create_pr_function_exists(self):
        """Test create_pr function exists and is importable."""
        from tagi.cli import create_pr
        assert callable(create_pr)
        
    def test_create_mr_function_exists(self):
        """Test create_mr function exists and is importable."""
        from tagi.cli import create_mr
        assert callable(create_mr)


class TestCLICommandStructure:
    """Test that all expected CLI commands are present."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
        
    def test_all_commands_registered(self):
        """Test that all expected commands are registered."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        
        expected_commands = [
            "scan",
            "list", "list-groups",
            "stats",
            "inspect",
            "filter",
            "file",
            "summary",
            "draft",
            "send",
            "auto",
            "deploy",
            "publish"
        ]
        
        for command in expected_commands:
            assert command in result.stdout, f"Command {command} not found in help output"
            
    def test_command_aliases_work(self):
        """Test that command aliases work correctly."""
        # Test that 'list' is an alias for 'list-groups'
        result1 = self.runner.invoke(app, ["list", "--help"])
        result2 = self.runner.invoke(app, ["list-groups", "--help"])
        
        assert result1.exit_code == 0
        assert result2.exit_code == 0
        # Both should have similar content but may differ in command name display
        assert "List available" in result1.stdout
        assert "List available" in result2.stdout


if __name__ == "__main__":
    pytest.main([__file__])
