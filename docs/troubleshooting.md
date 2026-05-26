# Troubleshooting Guide

This guide covers common issues and their solutions when using tagi.

## General Issues

### Command Not Found

**Problem**: `tagi: command not found`

**Solutions**:
1. Ensure tagi is installed:
   ```bash
   pip install tagi
   # or
   uv pip install tagi
   ```
2. Check installation:
   ```bash
   which tagi
   ```
3. If using development version:
   ```bash
   cd /path/to/tagi
   uv pip install -e .
   ```

### No Changes Detected

**Problem**: `tagi scan` shows "No uncommitted changes found" but files are modified

**Solutions**:
1. Check git status:
   ```bash
   git status
   ```
2. Ensure files are tracked by git:
   ```bash
   git add <file>
   ```
3. Tagi only detects uncommitted changes, not untracked files

### Permission Denied

**Problem**: `Permission denied` errors when running tagi

**Solutions**:
1. Check file permissions on repository
2. Ensure you have write access to `.git` directory
3. Run with appropriate permissions if needed

## Provider Issues

### Provider Not Detected

**Problem**: `publish` command shows "Could not detect GitHub or GitLab provider"

**Solutions**:
1. Check if remote is configured:
   ```bash
   git remote -v
   ```
2. Add remote if missing:
   ```bash
   git remote add origin <repository-url>
   ```
3. Ensure URL contains provider domain (github.com or gitlab.com)

### GitHub CLI Not Found

**Problem**: `GitHub CLI not found` error

**Solutions**:
1. Install GitHub CLI:
   ```bash
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   # or
   sudo dnf install gh
   
   # Windows
   winget install --id GitHub.cli
   ```
2. Verify installation:
   ```bash
   gh --version
   ```

### GitLab CLI Not Found

**Problem**: `GitLab CLI not found` error

**Solutions**:
1. Install GitLab CLI:
   ```bash
   # macOS
   brew install glab
   
   # Linux
   sudo apt install glab
   # or
   sudo dnf install glab
   ```
2. Verify installation:
   ```bash
   glab --version
   ```

### Authentication Failed

**Problem**: Authentication errors when creating PR/MR

**Solutions**:
1. Check authentication status:
   ```bash
   tagi auth --provider github
   # or
   tagi auth --provider gitlab
   ```
2. Authenticate with provider CLI:
   ```bash
   # For GitHub
   gh auth login
   
   # For GitLab
   glab auth login
   ```
3. Ensure you have proper permissions on the repository

## Configuration Issues

### Configuration Not Applied

**Problem**: Custom rules not being used

**Solutions**:
1. Ensure file is named `tagi.toml` (not `tagi.toml.example`)
2. Check file is in repository root
3. Verify TOML syntax is valid
4. Check for typos in section names

### Invalid TOML Syntax

**Problem**: Configuration file causing errors

**Solutions**:
1. Use a TOML validator to check syntax
2. Ensure strings are quoted: `"value"` not `value`
3. Check for proper array syntax: `["a", "b"]` not `[a, b]`
4. Verify section headers: `[section]` not `[section]`

### Tags Not Showing Colors

**Problem**: Custom colors not appearing

**Solutions**:
1. Verify color names are valid Rich colors
2. Check terminal supports colors
3. Ensure tag names in `[colors]` match tags in `[rules]`
4. Try standard colors: `red`, `green`, `blue`, etc.

## Tag Issues

### Tags Not Auto-Prefixed

**Problem**: Tags without `#` prefix not working

**Solutions**:
1. Tagi should auto-prefix tags - this should work automatically
2. If not, ensure you're using version 0.20.0 or later
3. Check that `_ensure_tag_prefix` helper is being used in the command

### Tag Filtering Not Working

**Problem**: `filter` command not returning expected results

**Solutions**:
1. Check tag spelling (case-sensitive)
2. Use comma separation for multiple tags: `small,docs`
3. Use `--all` flag for AND logic (default is OR)
4. Verify tags are actually assigned to files using `tagi inspect`

## Commit Issues

### Commit Failed

**Problem**: `send` command fails during commit

**Solutions**:
1. Check if git is properly initialized:
   ```bash
   git status
   ```
2. Ensure you have git user configured:
   ```bash
   git config user.name "Your Name"
   git config user.email "your@email.com"
   ```
3. Check for merge conflicts
4. Ensure files are not locked by another process

### Push Failed

**Problem**: `send --push` fails

**Solutions**:
1. Check remote URL is correct:
   ```bash
   git remote -v
   ```
2. Ensure you have push permissions
3. Check for authentication issues
4. Verify branch exists remotely

## Performance Issues

### Slow Scanning

**Problem**: `tagi scan` takes a long time

**Solutions**:
1. Large repositories may take longer - this is expected
2. Check if `.gitignore` is properly configured
3. Consider using `--grouped` flag for faster grouping
4. Check disk I/O performance

### High Memory Usage

**Problem**: Tagi using excessive memory

**Solutions**:
1. This is usually only an issue with very large repositories
2. Consider scanning specific directories instead of entire repo
3. Check for memory leaks (report if found)

## Getting Help

If you encounter an issue not covered here:

1. Check the documentation:
   - [README](../README.md)
   - [Provider Detection](./provider-detection.md)
   - [Configuration](./configuration.md)

2. Enable verbose logging:
   ```bash
   tagi --verbose scan /path/to/repo
   ```

3. Report the issue:
   - Include error messages
   - Provide steps to reproduce
   - Specify tagi version: `tagi --version`
   - Include OS and Python version

## Common Error Messages

### `Error: Not a git repository`

**Cause**: Running tagi outside of a git repository

**Solution**: Run tagi from within a git repository

### `Error: No remote configured`

**Cause**: No git remote is set up

**Solution**: Add a remote: `git remote add origin <url>`

### `Error: Permission denied`

**Cause**: Insufficient permissions for file operations

**Solution**: Check file/directory permissions

### `Error: Value error`

**Cause**: Invalid input or configuration

**Solution**: Check input values and configuration syntax
