# System Architecture Analysis
<!-- generated in 0.00s -->

## Overview

- **Project**: /home/tom/github/semcod/tagi
- **Primary Language**: python
- **Languages**: python: 31, yaml: 2, txt: 1, shell: 1, toml: 1
- **Analysis Mode**: static
- **Total Functions**: 95
- **Total Classes**: 13
- **Modules**: 36
- **Entry Points**: 67

## Architecture by Module

### src.tagi.cli
- **Functions**: 25
- **File**: `cli.py`

### src.tagi.config
- **Functions**: 9
- **Classes**: 1
- **File**: `config.py`

### src.tagi.executor.git
- **Functions**: 8
- **Classes**: 1
- **File**: `git.py`

### src.tagi.providers.base
- **Functions**: 8
- **Classes**: 1
- **File**: `base.py`

### src.tagi.planner.selector
- **Functions**: 5
- **File**: `selector.py`

### src.tagi.providers.gitlab
- **Functions**: 5
- **Classes**: 1
- **File**: `gitlab.py`

### src.tagi.providers.github
- **Functions**: 5
- **Classes**: 1
- **File**: `github.py`

### src.tagi.planner.grouper
- **Functions**: 4
- **File**: `grouper.py`

### src.tagi.llm.llx_adapter
- **Functions**: 4
- **Classes**: 1
- **File**: `llx_adapter.py`

### src.tagi.executor.publish
- **Functions**: 4
- **Classes**: 1
- **File**: `publish.py`

### src.tagi.composer.commit_message
- **Functions**: 4
- **File**: `commit_message.py`

### src.tagi.planner.preview
- **Functions**: 2
- **File**: `preview.py`

### src.tagi.scanner.status
- **Functions**: 2
- **File**: `status.py`

### src.tagi.scanner.diff
- **Functions**: 2
- **File**: `diff.py`

### src.tagi.heuristics.rules
- **Functions**: 2
- **File**: `rules.py`

### src.tagi.composer.summary
- **Functions**: 2
- **File**: `summary.py`

### src.tagi.heuristics.tags
- **Functions**: 2
- **File**: `tags.py`

### src.tagi.scanner.files
- **Functions**: 1
- **File**: `files.py`

### src.tagi.heuristics.scoring
- **Functions**: 1
- **File**: `scoring.py`

### src.tagi.models.plan
- **Functions**: 0
- **Classes**: 2
- **File**: `plan.py`

## Key Entry Points

Main execution flows into the system:

### src.tagi.cli.stats
> Show statistics about changes.
- **Calls**: app.command, typer.Argument, console.print, len, sum, Counter, Table, table.add_column

### src.tagi.cli.inspect
> Inspect a specific change group.
- **Calls**: app.command, typer.Argument, typer.Argument, typer.Option, console.print, Config, Tag, config.get_tag_description

### src.tagi.cli.publish
> Create a PR or MR for the changes.
- **Calls**: app.command, typer.Argument, typer.Argument, typer.Option, typer.Option, console.print, src.tagi.scanner.status.scan_repo, src.tagi.heuristics.tags.apply_tags

### src.tagi.cli.send
> Stage, commit, and optionally push changes.
- **Calls**: app.command, typer.Argument, typer.Argument, typer.Option, typer.Option, typer.Option, console.print, src.tagi.scanner.status.scan_repo

### src.tagi.cli.summary
> Generate a comprehensive summary report of all changes.
- **Calls**: app.command, typer.Argument, typer.Option, console.print, Config, report_lines.extend, report_lines.extend, report_lines.extend

### src.tagi.cli.file
> Show detailed information about a specific file.
- **Calls**: app.command, typer.Argument, typer.Argument, console.print, Config, Table, table.add_column, table.add_column

### src.tagi.cli.draft
> Draft a commit message for a change group.
- **Calls**: app.command, typer.Argument, typer.Argument, typer.Option, console.print, Tag, sum, ChangeGroup

### src.tagi.cli.filter
> Filter changes by tags.
- **Calls**: app.command, typer.Argument, typer.Argument, typer.Option, console.print, _parse_tags, _filter_changes_by_tags, console.print

### src.tagi.cli.scan
> Scan repository for uncommitted changes.
- **Calls**: app.command, typer.Argument, typer.Option, console.print, src.tagi.scanner.status.scan_repo, src.tagi.heuristics.tags.apply_tags, console.print, src.tagi.cli._display_changes_grouped

### src.tagi.cli.list_groups
> List available change groups.
- **Calls**: app.command, typer.Argument, console.print, src.tagi.cli._display_groups, Config, src.tagi.scanner.status.scan_repo, src.tagi.heuristics.tags.apply_tags, src.tagi.planner.grouper.group_changes

### src.tagi.composer.summary.generate_summary
> Generate a summary of changes.
- **Calls**: sum, lines.append, lines.append, sum, sum, sum, lines.append, None.join

### src.tagi.planner.preview.preview_changes
> Generate a preview for a change group.
- **Calls**: lines.append, lines.append, lines.append, lines.append, lines.append, None.join, None.join, lines.append

### src.tagi.config.Config._load_config
> Load configuration from tagi.toml if it exists.
- **Calls**: Path, config_path.exists, print, open, tomli.load, None.get, None.get, print

### src.tagi.planner.preview.preview_plan
> Generate a preview of the execution plan.
- **Calls**: lines.append, lines.append, None.join, Tag, None.join, lines.append, len

### src.tagi.composer.summary.generate_file_list
> Generate a formatted list of files.
- **Calls**: None.join, None.join, lines.append, len, lines.append, len

### src.tagi.config.Config.get_heuristics_for_path
> Get custom heuristic tags for a file path.
- **Calls**: path.lower, self.custom_heuristics.items, pattern.lower, tags.extend

### src.tagi.providers.gitlab.GitLabProvider.create_pr
> Create a merge request using glab CLI.
- **Calls**: self._run_command, cmd.append, cmd.extend, None.join

### src.tagi.providers.github.GitHubProvider.create_pr
> Create a pull request using gh CLI.
- **Calls**: self._run_command, cmd.append, cmd.extend, None.join

### src.tagi.config.Config.get_tag_for_path
> Get custom tag for a file path based on rules.
- **Calls**: path.lower, self.custom_rules.items, pattern.lower

### src.tagi.executor.git.GitExecutor.commit
> Commit staged changes.
- **Calls**: subprocess.run, cmd.append, RuntimeError

### src.tagi.executor.git.GitExecutor.push
> Push commits to remote.
- **Calls**: subprocess.run, cmd.append, RuntimeError

### src.tagi.executor.git.GitExecutor.has_staged_changes
> Check if there are staged changes.
- **Calls**: subprocess.run, bool, result.stdout.strip

### src.tagi.providers.base.BaseProvider._check_git_remote_for_provider
> Check if the git remote URL contains the provider name.
- **Calls**: self._get_git_remote_url, provider_name.lower, url.lower

### src.tagi.providers.gitlab.GitLabProvider.get_configured_host
> Get the configured GitLab host.
- **Calls**: self._run_command, json.loads, urlparse

### src.tagi.config.Config.should_ignore
> Check if a path should be ignored based on ignore patterns.
- **Calls**: path.lower, pattern.lower

### src.tagi.planner.selector.select_by_tags
> Select changes by tags (OR or AND logic).
- **Calls**: all, any

### src.tagi.planner.selector.select_safe_changes
> Select changes that are safe to ship first (low risk, small, not risky/deps/config).
- **Calls**: any, any

### src.tagi.executor.git.GitExecutor.add
> Stage files for commit.
- **Calls**: subprocess.run, RuntimeError

### src.tagi.executor.git.GitExecutor.get_current_branch
> Get the current branch name.
- **Calls**: subprocess.run, result.stdout.strip

### src.tagi.executor.git.GitExecutor.get_remote_url
> Get the remote URL.
- **Calls**: subprocess.run, result.stdout.strip

## Process Flows

Key execution flows identified:

### Flow 1: stats
```
stats [src.tagi.cli]
```

### Flow 2: inspect
```
inspect [src.tagi.cli]
```

### Flow 3: publish
```
publish [src.tagi.cli]
```

### Flow 4: send
```
send [src.tagi.cli]
```

### Flow 5: summary
```
summary [src.tagi.cli]
```

### Flow 6: file
```
file [src.tagi.cli]
```

### Flow 7: draft
```
draft [src.tagi.cli]
```

### Flow 8: filter
```
filter [src.tagi.cli]
```

### Flow 9: scan
```
scan [src.tagi.cli]
  └─ →> scan_repo
```

### Flow 10: list_groups
```
list_groups [src.tagi.cli]
  └─> _display_groups
      └─> _format_tags
```

## Key Classes

### src.tagi.config.Config
> Configuration loaded from tagi.toml.
- **Methods**: 9
- **Key Methods**: src.tagi.config.Config.__init__, src.tagi.config.Config._load_config, src.tagi.config.Config.get_tag_for_path, src.tagi.config.Config.get_custom_tags_for_pattern, src.tagi.config.Config.get_tag_color, src.tagi.config.Config.get_heuristics_for_path, src.tagi.config.Config.get_tag_description, src.tagi.config.Config.get_template, src.tagi.config.Config.should_ignore

### src.tagi.executor.git.GitExecutor
> Executor for git commands.
- **Methods**: 8
- **Key Methods**: src.tagi.executor.git.GitExecutor.__init__, src.tagi.executor.git.GitExecutor.add, src.tagi.executor.git.GitExecutor.commit, src.tagi.executor.git.GitExecutor.push, src.tagi.executor.git.GitExecutor.status, src.tagi.executor.git.GitExecutor.get_current_branch, src.tagi.executor.git.GitExecutor.get_remote_url, src.tagi.executor.git.GitExecutor.has_staged_changes

### src.tagi.providers.base.BaseProvider
> Base class for Git hosting providers.
- **Methods**: 8
- **Key Methods**: src.tagi.providers.base.BaseProvider.__init__, src.tagi.providers.base.BaseProvider.is_authenticated, src.tagi.providers.base.BaseProvider.get_auth_status, src.tagi.providers.base.BaseProvider.create_pr, src.tagi.providers.base.BaseProvider.detect_remote, src.tagi.providers.base.BaseProvider._run_command, src.tagi.providers.base.BaseProvider._get_git_remote_url, src.tagi.providers.base.BaseProvider._check_git_remote_for_provider
- **Inherits**: ABC

### src.tagi.providers.gitlab.GitLabProvider
> GitLab provider using glab CLI.
- **Methods**: 5
- **Key Methods**: src.tagi.providers.gitlab.GitLabProvider.is_authenticated, src.tagi.providers.gitlab.GitLabProvider.get_auth_status, src.tagi.providers.gitlab.GitLabProvider.get_configured_host, src.tagi.providers.gitlab.GitLabProvider.create_pr, src.tagi.providers.gitlab.GitLabProvider.detect_remote
- **Inherits**: BaseProvider

### src.tagi.providers.github.GitHubProvider
> GitHub provider using gh CLI.
- **Methods**: 5
- **Key Methods**: src.tagi.providers.github.GitHubProvider.is_authenticated, src.tagi.providers.github.GitHubProvider.get_auth_status, src.tagi.providers.github.GitHubProvider.get_token, src.tagi.providers.github.GitHubProvider.create_pr, src.tagi.providers.github.GitHubProvider.detect_remote
- **Inherits**: BaseProvider

### src.tagi.llm.llx_adapter.LlxAdapter
> Adapter for LLX library for optional LLM integration.
- **Methods**: 4
- **Key Methods**: src.tagi.llm.llx_adapter.LlxAdapter.__init__, src.tagi.llm.llx_adapter.LlxAdapter.is_available, src.tagi.llm.llx_adapter.LlxAdapter.improve_message, src.tagi.llm.llx_adapter.LlxAdapter.improve_description

### src.tagi.executor.publish.PublishExecutor
> Executor for publishing changes.
- **Methods**: 4
- **Key Methods**: src.tagi.executor.publish.PublishExecutor.__init__, src.tagi.executor.publish.PublishExecutor.stage_and_commit, src.tagi.executor.publish.PublishExecutor.publish, src.tagi.executor.publish.PublishExecutor.dry_run

### src.tagi.models.plan.PlanStep
> A single step in an execution plan.
- **Methods**: 0

### src.tagi.models.plan.Plan
> An execution plan for shipping changes.
- **Methods**: 0

### src.tagi.models.change.ChangeType
> Type of git change.
- **Methods**: 0
- **Inherits**: str, Enum

### src.tagi.models.change.Tag
> Hashtag categories for changes.
- **Methods**: 0
- **Inherits**: str, Enum

### src.tagi.models.change.Change
> Represents a single file change.
- **Methods**: 0

### src.tagi.models.group.ChangeGroup
> Group of related changes.
- **Methods**: 0

## Data Transformation Functions

Key functions that process and transform data:

### src.tagi.scanner.status.parse_status
> Parse git status code to ChangeType.

### src.tagi.cli._parse_commit_message
> Parse commit message into title and body.
- **Output to**: message.split, None.join, len

### src.tagi.cli._format_tags
> Format tags with color coding.
- **Output to**: None.join, formatted.append, config.get_tag_color, tag_colors.get

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.tagi.cli.stats` - 43 calls
- `src.tagi.cli.inspect` - 42 calls
- `src.tagi.cli.publish` - 33 calls
- `src.tagi.cli.send` - 32 calls
- `src.tagi.cli.summary` - 30 calls
- `src.tagi.cli.file` - 26 calls
- `src.tagi.cli.draft` - 22 calls
- `src.tagi.cli.filter` - 21 calls
- `src.tagi.scanner.status.scan_repo` - 15 calls
- `src.tagi.cli.scan` - 15 calls
- `src.tagi.heuristics.tags.apply_tags` - 15 calls
- `src.tagi.cli.list_groups` - 13 calls
- `src.tagi.composer.commit_message.generate_detailed_message` - 12 calls
- `src.tagi.planner.grouper.group_changes` - 11 calls
- `src.tagi.composer.summary.generate_summary` - 11 calls
- `src.tagi.planner.preview.preview_changes` - 9 calls
- `src.tagi.composer.commit_message.generate_commit_message` - 9 calls
- `src.tagi.planner.preview.preview_plan` - 7 calls
- `src.tagi.scanner.files.count_lines_changed` - 7 calls
- `src.tagi.composer.summary.generate_file_list` - 6 calls
- `src.tagi.cli.create_pr` - 5 calls
- `src.tagi.cli.create_mr` - 5 calls
- `src.tagi.config.Config.get_heuristics_for_path` - 4 calls
- `src.tagi.cli.detect_provider` - 4 calls
- `src.tagi.providers.gitlab.GitLabProvider.create_pr` - 4 calls
- `src.tagi.providers.github.GitHubProvider.create_pr` - 4 calls
- `src.tagi.config.Config.get_tag_for_path` - 3 calls
- `src.tagi.executor.git.GitExecutor.commit` - 3 calls
- `src.tagi.executor.git.GitExecutor.push` - 3 calls
- `src.tagi.executor.git.GitExecutor.has_staged_changes` - 3 calls
- `src.tagi.providers.gitlab.GitLabProvider.get_configured_host` - 3 calls
- `src.tagi.heuristics.tags.apply_path_tags` - 3 calls
- `src.tagi.config.Config.should_ignore` - 2 calls
- `src.tagi.planner.selector.select_by_tags` - 2 calls
- `src.tagi.planner.selector.select_safe_changes` - 2 calls
- `src.tagi.heuristics.scoring.calculate_risk_score` - 2 calls
- `src.tagi.executor.git.GitExecutor.add` - 2 calls
- `src.tagi.executor.git.GitExecutor.get_current_branch` - 2 calls
- `src.tagi.executor.git.GitExecutor.get_remote_url` - 2 calls
- `src.tagi.executor.publish.PublishExecutor.stage_and_commit` - 2 calls

## System Interactions

How components interact:

```mermaid
graph TD
    stats --> command
    stats --> Argument
    stats --> print
    stats --> len
    stats --> sum
    inspect --> command
    inspect --> Argument
    inspect --> Option
    inspect --> print
    publish --> command
    publish --> Argument
    publish --> Option
    send --> command
    send --> Argument
    send --> Option
    summary --> command
    summary --> Argument
    summary --> Option
    summary --> print
    summary --> Config
    file --> command
    file --> Argument
    file --> print
    file --> Config
    draft --> command
    draft --> Argument
    draft --> Option
    draft --> print
    filter --> command
    filter --> Argument
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.