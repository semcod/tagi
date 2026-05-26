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

- [ ] Update README.md with current command examples (tags without # prefix)
- [ ] Add `list-groups` command implementation (currently shows error)
- [ ] Add `safe` command implementation (mentioned in README but not in CLI)
- [ ] Add `init` command to generate tagi.toml.example
- [ ] Add `auth` command for GitHub/GitLab authentication check

### Medium Priority

- [ ] Improve error messages for failed PR/MR creation
- [ ] Add interactive mode for selecting changes
- [ ] Add support for custom tag definitions in config
- [ ] Add more commit message templates
- [ ] Add diff preview in inspect command

### Low Priority

- [ ] Add `summary` command implementation
- [ ] Add dependency graph analysis
- [ ] Add branch-based change grouping
- [ ] Add support for git hooks integration
- [ ] Add metrics and analytics

### Documentation

- [ ] Update README.md with all available commands
- [ ] Add examples for all templates
- [ ] Document provider detection logic
- [ ] Document custom configuration options
- [ ] Add troubleshooting guide

### Testing

- [ ] Add integration tests for GitHub provider
- [ ] Add integration tests for GitLab provider
- [ ] Add tests for auto-prefix functionality
- [ ] Add tests for tag filtering
- [ ] Add end-to-end tests for send/publish workflow

### Refactoring

- [ ] Extract provider detection to separate module
- [ ] Consolidate tag prefix logic into helper function
- [ ] Improve error handling across all commands
- [ ] Add logging framework
- [ ] Add type hints for all functions
