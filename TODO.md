# TODO

## Completed (Version 0.12.0)

- [x] Auto-prefix for tags in all commands (send, publish, draft, inspect, filter)
- [x] Tag filtering instead of group filtering (allows sending by any tag, not just primary)
- [x] Provider auto-detection in publish command (GitHub/GitLab)
- [x] Template parameter in publish command (default, conventional, detailed)
- [x] Executor integration for git operations (GitExecutor, PublishExecutor)
- [x] Helper functions for PR/MR creation (create_pr, create_mr)

## Remaining Tasks

### High Priority

- [x] Update README.md with current command examples (tags without # prefix)
- [x] Add `list-groups` command implementation (already exists as `list-groups`)
- [x] Add `safe` command implementation (mentioned in README but not in CLI)
- [x] Add `init` command to generate tagi.toml.example
- [x] Add `auth` command for GitHub/GitLab authentication check

### Medium Priority

- [x] Improve error messages for failed PR/MR creation
- [x] Add interactive mode for selecting changes
- [x] Add support for custom tag definitions in config
- [x] Add more commit message templates
- [x] Add diff preview in inspect command

### Low Priority

- [x] Add `summary` command implementation
- [x] Add dependency graph analysis
- [x] Add branch-based change grouping
- [x] Add support for git hooks integration
- [x] Add metrics and analytics

### Documentation

- [x] Update README.md with all available commands
- [x] Add examples for all templates
- [x] Document provider detection logic
- [x] Document custom configuration options
- [x] Add troubleshooting guide

### Testing

- [x] Add integration tests for GitHub provider
- [x] Add integration tests for GitLab provider
- [x] Add tests for auto-prefix functionality
- [x] Add tests for tag filtering
- [x] Add end-to-end tests for send/publish workflow

### Refactoring

- [x] Extract provider detection to separate module
- [x] Consolidate tag prefix logic into helper function
- [x] Improve error handling across all commands
- [x] Add logging framework
- [x] Add type hints for all functions
