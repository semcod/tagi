# Provider Detection

## Overview

Tagi automatically detects which Git hosting provider (GitHub or GitLab) is being used for the current repository. This is primarily used by the `publish` command to determine whether to create a Pull Request (GitHub) or Merge Request (GitLab).

## Detection Mechanism

The detection is implemented in `src/tagi/providers/detector.py`:

```python
def detect_provider(repo_path: str = ".") -> str:
    """Detect the Git hosting provider from remotes."""
    github = GitHubProvider(repo_path)
    gitlab = GitLabProvider(repo_path)
    if github.detect_remote():
        return "github"
    if gitlab.detect_remote():
        return "gitlab"
    return ""
```

## How It Works

1. **GitHub Detection**: Checks if the git remote URL contains "github.com"
2. **GitLab Detection**: Checks if the git remote URL contains "gitlab.com"
3. **Order**: GitHub is checked first, then GitLab
4. **Fallback**: Returns empty string if neither is detected

## Usage Examples

### Automatic Detection (publish command)

```bash
# Automatically detects provider based on remote URL
tagi publish small /path/to/repo
```

The command will:
1. Check `git remote get-url origin`
2. Detect if URL contains "github.com" → use GitHub
3. Detect if URL contains "gitlab.com" → use GitLab
4. Show error if neither is found

### Manual Provider Check (auth command)

```bash
# Check both providers
tagi auth /path/to/repo

# Check only GitHub
tagi auth /path/to/repo --provider github

# Check only GitLab
tagi auth /path/to/repo --provider gitlab
```

## Supported Providers

### GitHub

- **CLI Required**: `gh` (GitHub CLI)
- **Remote Patterns**: `github.com`, `git@github.com`
- **Authentication**: Uses `gh auth status`
- **PR Creation**: Uses `gh pr create`

### GitLab

- **CLI Required**: `glab` (GitLab CLI)
- **Remote Patterns**: `gitlab.com`, `git@gitlab.com`
- **Authentication**: Uses `glab auth status`
- **MR Creation**: Uses `glab mr create`

## Error Handling

If provider detection fails:
- The `publish` command will show a warning
- Suggestion to ensure a remote is configured
- User can manually check with `tagi auth` command

## Troubleshooting

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

### Authentication Issues

**Problem**: Provider detected but authentication fails

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

### CLI Not Found

**Problem**: Provider detected but CLI tool not installed

**Solutions**:
1. Install GitHub CLI:
   ```bash
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   ```
2. Install GitLab CLI:
   ```bash
   # macOS
   brew install glab
   
   # Linux
   sudo apt install glab
   ```
