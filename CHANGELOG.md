# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

