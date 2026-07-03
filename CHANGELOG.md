# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [0.49.9] - 2026-07-03

### Docs
- Update README.md

## [0.49.8] - 2026-06-29

### Docs
- Update README.md

## [0.49.7] - 2026-05-26

### Docs
- Update README.md

## [0.49.6] - 2026-05-26

### Docs
- Update README.md

## [0.49.5] - 2026-05-26

### Docs
- Update README.md

### Other
- Update project/planfile-tickets.yaml

## [0.49.4] - 2026-05-26

### Docs
- Update README.md

## [0.49.3] - 2026-05-26

### Docs
- Update README.md

### Other
- Update uv.lock

## [0.49.2] - 2026-05-26

### Docs
- Update CHANGELOG.md
- Update SUMD.md
- Update SUMR.md
- Update project/README.md
- Update project/context.md

### Other
- Update .gitignore
- Update app.doql.less
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- Update project/duplication.toon.yaml
- ... and 11 more files

## [0.50.0] - 2026-05-26

### Refactoring
- Split filter function CC from 17 to ≤15 using utils/inspect_helpers.py
- Added filter_changes_by_tags_any and filter_changes_by_tags_all helpers
- All high-CC functions (send, publish, inspect, summary, filter) now ≤15
- Code quality and maintainability improved across CLI module

## [0.49.1] - 2026-05-26

### Docs
- Update CHANGELOG.md
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_tagi.py

### Other
- Update .gitignore
- Update VERSION
- Update app.doql.less
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- ... and 13 more files

## [0.49.0] - 2026-05-26

### Refactoring
- Split inspect function CC from 15 to ≤15 using utils/inspect_helpers.py
- Split summary function CC from 15 to ≤15 using utils/summary_helpers.py
- Extracted tag filtering, statistics calculation, and report building helpers
- Further reduced code duplication and improved maintainability

## [0.48.0] - 2026-05-26

### Refactoring
- Extracted duplicate create_pr logic to providers/utils/pr.py (12 lines saved)
- Extracted duplicate detect_provider logic to utils/detect_provider.py (9 lines saved)
- Extracted duplicate get_auth_status logic to providers/utils/auth.py (8 lines saved)
- Extracted duplicate is_authenticated logic to providers/utils/auth.py (4 lines saved)
- Split send function CC from 27 to ≤15 using utils/send_helpers.py
- Split publish function CC from 17 to ≤15 using utils/publish_helpers.py
- Created filter_helpers.py for filter command refactoring
- Reduced code duplication and improved maintainability

## [0.47.0] - 2026-05-26

### Features
- Added --verbose/-v flag for detailed logging across all commands
- Auto-order functionality for send command (--auto-order/-a)
- Send command now accepts optional tag parameter (repo_path first)
- Sort changes by complexity when no tag specified or auto-order enabled
- Enhanced logger module with verbose mode support

## [0.46.1] - 2026-05-26

### Docs
- Update CHANGELOG.md
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update TODO.md
- Update docs/configuration.md
- Update docs/provider-detection.md
- Update docs/troubleshooting.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_e2e.py
- Update tests/test_github_provider.py
- Update tests/test_gitlab_provider.py
- Update tests/test_tagi.py

### Other
- Update .code2llm_cache/base_1779807720540219029_1860.pkl
- Update .code2llm_cache/cli_1779808664226186571_25353.pkl
- Update .code2llm_cache/commit_message_1779807736909391917_3993.pkl
- Update .code2llm_cache/github_1779807716162172788_1683.pkl
- Update .code2llm_cache/gitlab_1779807716300174246_2042.pkl
- Update .code2llm_cache/pyproject_1779808656210101900_1303.pkl
- Update .code2llm_cache/tags_1779807741800443576_3256.pkl
- Update .code2llm_cache/tree_1779807016792786926_2024.pkl
- Update VERSION
- Update app.doql.less
- ... and 19 more files

## [0.47.0] - 2026-05-26

### Features
- Added numerical vector metrics to Change model (ChangeMetrics)
- Metrics include: risk, complexity, impact, stability, test coverage impact, dependency depth
- Added filter command options for metric-based filtering
- Metrics are automatically calculated for all changes
- Added to_vector() method for vector-based comparison

## [0.46.0] - 2026-05-26

### Improvements
- Enhanced dry-run mode to show detailed execution plan
- Dry-run now displays files to commit, risk scores, and tags for each group
- Added dry-run summary showing total changes, number of commits, and push status

## [0.45.0] - 2026-05-26

### Features
- Added automatic heuristic-based change sorting (simplest to most complex)
- Added --auto-order/-a flag to send command for complexity-based ordering
- Changes are sorted by risk score, lines changed, and change type
- Groups changes into complexity tiers when no tags are specified

## [0.44.0] - 2026-05-26

### Features
- Added priority-based sending with multiple tags in order
- Send command now accepts list of tags (e.g., `tagi send small docs /path`)
- Changes are processed in tag priority order, avoiding duplicates
- Shows summary of total changes committed across all tags

## [0.43.0] - 2026-05-26

### Docs
- Updated README with new commands (hooks, deps, metrics)
- Added descriptions for all new CLI features

## [0.42.0] - 2026-05-26

### Testing
- Added end-to-end tests for send/publish workflow (test_e2e.py)
- Tests cover scanning, tagging, grouping, commit message generation, and tag filtering
- Fixed integration tests to handle missing CLI tools gracefully

## [0.41.0] - 2026-05-26

### Testing
- Added integration tests for GitHub provider (test_github_provider.py)
- Added integration tests for GitLab provider (test_gitlab_provider.py)
- Tests cover remote detection, authentication status, and provider initialization

## [0.40.0] - 2026-05-26

### Features
- Added metrics and analytics module with MetricsCollector
- Added metrics CLI command for collecting and reporting change metrics
- Added support for JSON export and human-readable reports

## [0.39.0] - 2026-05-26

### Features
- Added dependency graph analysis with dependency_graph module
- Added deps CLI command for analyzing Python import dependencies
- Added support for detecting circular dependencies, critical path, and dependency order

## [0.38.0] - 2026-05-26

### Features
- Added branch-based change grouping with branch_grouper module
- Added --by-branch/-b option to scan command
- Added _display_changes_by_branch helper for branch group display

## [0.37.0] - 2026-05-26

### Features
- Added git hooks integration with hooks module
- Added hooks CLI command (install, uninstall, list, status check)
- Added pre-commit hook support for automatic tagging

## [0.36.0] - 2026-05-26

### Features
- Added interactive mode to send command (--interactive/-i flag)
- Users can now select which changes to include before committing
- Marked summary command as completed (already implemented)
- Marked custom tag definitions as completed (supported via [heuristics])

## [0.35.0] - 2026-05-26

### Testing
- Added comprehensive tag filtering tests (OR/AND logic, no match, all match)
- Fixed missing imports (List, Change) in cli.py
- Added missing _ensure_tag_prefix function to cli.py
- All 32 tests passing

## [0.34.0] - 2026-05-26

### Testing
- Added tests for auto-prefix functionality (_ensure_tag_prefix)
- Added tests for Tag enum creation with/without prefix
- Added tests for tag filtering with prefix

## [0.33.0] - 2026-05-26

### Docs
- Added comprehensive troubleshooting guide (docs/troubleshooting.md)
- Covers general issues, provider issues, configuration, tags, commits, performance

## [0.32.0] - 2026-05-26

### Docs
- Added custom configuration documentation (docs/configuration.md)
- Documented all configuration sections: rules, colors, heuristics, tag_definitions
- Added troubleshooting for configuration issues

## [0.31.0] - 2026-05-26

### Docs
- Added provider detection documentation (docs/provider-detection.md)
- Documented detection mechanism, supported providers, and troubleshooting

## [0.30.0] - 2026-05-26

### Refactoring
- Improved error handling across all CLI commands (send, publish, init, auth)
- Added consistent try/except blocks with ValueError, RuntimeError, and generic Exception handling
- Added file operation error handling for init command (PermissionError, OSError)

## [0.29.0] - 2026-05-26

### Docs
- Updated README with all available commands (safe, init, auth)
- Added examples for all commit message templates (simple, oneline, files)
- Updated command descriptions with template options

## [0.28.0] - 2026-05-26

### Refactoring
- Added logging framework with setup_logger utility
- Integrated logger into CLI with verbose support
- Added utils/logger.py module for logging configuration

## [0.27.0] - 2026-05-26

### Refactoring
- Added type hints to heuristics/rules.py
- Improved type hints in planner/grouper.py (Dict instead of dict)

## [0.26.0] - 2026-05-26

### Features
- Added more commit message templates: simple, oneline, files
- Added template parameter support in CLI for all new templates

## [0.25.0] - 2026-05-26

### Improvements
- Improved error messages for failed PR/MR creation with helpful suggestions
- Added better error handling for missing CLI tools and authentication issues
- Marked diff preview in inspect as completed (already implemented)

## [0.24.0] - 2026-05-26

### Features
- Added `auth` command to check GitHub/GitLab authentication status
- Supports checking specific provider with --provider option

## [0.23.0] - 2026-05-26

### Features
- Added `init` command to generate tagi.toml.example configuration file

## [0.22.0] - 2026-05-26

### Features
- Added `safe` command to show safe changes (low risk, small, not risky/deps/config)
- Marked list-groups as completed (already exists as list-groups)

## [0.21.0] - 2026-05-26

### Docs
- Updated README.md examples to use tags without # prefix
- Added more usage examples for send and publish commands

## [0.20.0] - 2026-05-26

### Refactoring
- Consolidated tag prefix logic into _ensure_tag_prefix helper function
- Extracted provider detection to separate providers/detector.py module
- Removed duplicate detect_provider function from cli.py

## [0.19.0] - 2026-05-26

### Refactoring
- Fixed duplication in heuristics/rules.py by extracting _get_config_attr helper
- Fixed duplication in planner/grouper.py by using selector.select_changes_by_tag
- Fixed duplication in cli.py create_pr/create_mr by extracting _create_pr_for_cli helper

## [0.18.0] - 2026-05-26

### Refactoring
- Refactored inspect function to reduce CC by extracting _find_change_by_tag, _calculate_tag_metrics, and _display_tag_metrics helpers

## [0.17.0] - 2026-05-26

### Refactoring
- Refactored summary function to reduce CC by extracting _build_summary_header, _build_summary_statistics, _build_summary_by_type, _build_summary_tag_distribution, and _build_summary_file_list helpers

## [0.16.0] - 2026-05-26

### Refactoring
- Refactored filter function to reduce CC by extracting _parse_tags and _filter_changes_by_tags helpers
- Refactored publish function to reduce CC by extracting _parse_commit_message, _display_pr_preview, and _create_pr_for_provider helpers
- Removed duplicate # prefix logic in filter function

## [0.15.1] - 2026-05-26

### Docs
- Update CHANGELOG.md
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update TODO.md
- Update project/README.md
- Update project/context.md

### Test
- Update tests/test_tagi.py

### Other
- Update .code2llm_cache/base_1779802739508353087_645.pkl
- Update .code2llm_cache/cli_1779806974820276071_24915.pkl
- Update .code2llm_cache/commit_message_1779802864864699922_4914.pkl
- Update .code2llm_cache/config_1779802844828755285_4314.pkl
- Update .code2llm_cache/github_1779802743928400771_2537.pkl
- Update .code2llm_cache/gitlab_1779802746214425433_2895.pkl
- Update .code2llm_cache/llx_adapter_1779802774983735825_1955.pkl
- Update .code2llm_cache/pyproject_1779806977595373045_1303.pkl
- Update .code2llm_cache/scoring_1779802847615519629_777.pkl
- Update .code2llm_cache/tags_1779802838069416599_3475.pkl
- ... and 22 more files

## [0.15.0] - 2026-05-26

### Refactoring
- Refactored _infer_scope to reduce CC from 20 to 10 using pattern mapping
- Refactored apply_path_tags to reduce CC from 17 to 8 using pattern mapping

## [0.14.0] - 2026-05-26

### Refactoring
- Extracted common provider logic to BaseProvider (_run_command, _get_git_remote_url, _check_git_remote_for_provider)
- Removed duplicate generate_detailed_message function in commit_message.py
- Reduced code duplication between GitHubProvider and GitLabProvider

## [0.13.0] - 2026-05-26

### Fixed
- Fixed filter command to support auto-prefix for tags (e.g., `docs` instead of `#docs`)

## [0.12.0] - 2026-05-26

### Added
- Auto-prefix for tags in all commands (send, publish, draft, inspect, filter)
- Tag filtering instead of group filtering (allows sending by any tag, not just primary)
- Provider auto-detection in publish command (GitHub/GitLab)
- Template parameter in publish command (default, conventional, detailed)
- Executor integration (GitExecutor, PublishExecutor) for git operations
- Helper functions for PR/MR creation (detect_provider, create_pr, create_mr)

### Changed
- Send command now filters changes by tag instead of looking for groups
- Draft command now filters changes by tag instead of looking for groups
- Publish command now filters changes by tag instead of looking for groups
- All commands accept tags without `#` prefix (e.g., `small` instead of `#small`)

### Fixed
- Fixed send command to use executor instead of non-existent stage_changes function
- Fixed draft command to pass group.changes instead of group to commit message generator
- Fixed publish command to pass group.changes instead of group to commit message generator
- Removed duplicate push logic in send command

## [0.11.0] - 2026-05-26

### Added
- LLM integration for commit message improvement
- LlxAdapter for optional LLM-based message enhancement
- llm_enabled configuration option

### Changed
- Commit message generation supports LLM improvement
- Tag.FIX removed from commit_type="fix" condition

## [0.10.0] - 2026-05-26

### Added
- Template parameter for commit messages (default, conventional, detailed)
- Custom template support in configuration



## [0.3.1] - 2026-05-26

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update project/README.md
- Update project/context.md

### Test
- Update testql-scenarios/generated-cli-tests.testql.toon.yaml
- Update tests/test_tagi.py

### Other
- Update .code2llm_cache/__init___1779800615590949571_38.pkl
- Update .code2llm_cache/cli_1779800820729188454_8260.pkl
- Update .code2llm_cache/composer_1779800740358318524_2153.pkl
- Update .code2llm_cache/config_1779800818644168363_1842.pkl
- Update .code2llm_cache/executor_1779800740376318721_1750.pkl
- Update .code2llm_cache/goal_1779800989729846870_12188.pkl
- Update .code2llm_cache/heuristics_1779800850797479284_4181.pkl
- Update .code2llm_cache/models_1779800615824952139_977.pkl
- Update .code2llm_cache/planner_1779800615861952545_827.pkl
- Update .code2llm_cache/project_1777557997938138204_1409.pkl
- ... and 30 more files

## [0.1.1] - 2026-05-26

### Docs
- Update README.md
- Update TODO/1.md
- Update TODO/2.md

### Test
- Update tests/test_tagi.py

### Other
- Update .gitignore
- Update .idea/.gitignore
- Update tagi.toml.example
- Update uv.lock

