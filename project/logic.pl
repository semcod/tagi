% ── Project Metadata ─────────────────────────────────────
project_metadata('tagi', '0.47.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 29, 'less').
project_file('project.sh', 48, 'shell').
project_file('src/tagi/__init__.py', 48, 'python').
project_file('src/tagi/analyzer/dependency_graph.py', 196, 'python').
project_file('src/tagi/analyzer/metrics.py', 154, 'python').
project_file('src/tagi/cli.py', 806, 'python').
project_file('src/tagi/composer/__init__.py', 13, 'python').
project_file('src/tagi/composer/commit_message.py', 184, 'python').
project_file('src/tagi/composer/summary.py', 46, 'python').
project_file('src/tagi/config.py', 130, 'python').
project_file('src/tagi/executor/__init__.py', 10, 'python').
project_file('src/tagi/executor/git.py', 115, 'python').
project_file('src/tagi/executor/publish.py', 40, 'python').
project_file('src/tagi/heuristics/__init__.py', 14, 'python').
project_file('src/tagi/heuristics/metrics.py', 215, 'python').
project_file('src/tagi/heuristics/rules.py', 22, 'python').
project_file('src/tagi/heuristics/scoring.py', 32, 'python').
project_file('src/tagi/heuristics/tags.py', 88, 'python').
project_file('src/tagi/hooks.py', 126, 'python').
project_file('src/tagi/llm/__init__.py', 8, 'python').
project_file('src/tagi/llm/llx_adapter.py', 56, 'python').
project_file('src/tagi/models/__init__.py', 15, 'python').
project_file('src/tagi/models/change.py', 61, 'python').
project_file('src/tagi/models/group.py', 17, 'python').
project_file('src/tagi/models/plan.py', 24, 'python').
project_file('src/tagi/planner/__init__.py', 19, 'python').
project_file('src/tagi/planner/branch_grouper.py', 89, 'python').
project_file('src/tagi/planner/grouper.py', 77, 'python').
project_file('src/tagi/planner/preview.py', 42, 'python').
project_file('src/tagi/planner/selector.py', 45, 'python').
project_file('src/tagi/planner/sorter.py', 105, 'python').
project_file('src/tagi/providers/__init__.py', 12, 'python').
project_file('src/tagi/providers/base.py', 59, 'python').
project_file('src/tagi/providers/detector.py', 16, 'python').
project_file('src/tagi/providers/github.py', 48, 'python').
project_file('src/tagi/providers/gitlab.py', 56, 'python').
project_file('src/tagi/scanner/__init__.py', 14, 'python').
project_file('src/tagi/scanner/diff.py', 32, 'python').
project_file('src/tagi/scanner/files.py', 31, 'python').
project_file('src/tagi/scanner/status.py', 68, 'python').
project_file('src/tagi/utils/logger.py', 72, 'python').
project_file('tests/test_e2e.py', 129, 'python').
project_file('tests/test_github_provider.py', 78, 'python').
project_file('tests/test_gitlab_provider.py', 77, 'python').
project_file('tests/test_tagi.py', 483, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('src/tagi/analyzer/dependency_graph.py', 'analyze_python_imports', 2, 8, 6).
python_function('src/tagi/analyzer/dependency_graph.py', 'build_dependency_graph', 2, 3, 3).
python_function('src/tagi/analyzer/dependency_graph.py', 'find_dependency_order', 1, 10, 8).
python_function('src/tagi/analyzer/dependency_graph.py', 'detect_cycles', 1, 4, 5).
python_function('src/tagi/analyzer/dependency_graph.py', 'get_critical_path', 1, 10, 6).
python_function('src/tagi/analyzer/metrics.py', 'generate_report', 1, 3, 4).
python_function('src/tagi/analyzer/metrics.py', 'compare_metrics', 2, 1, 0).
python_function('src/tagi/cli.py', 'setup_logging', 1, 3, 4).
python_function('src/tagi/cli.py', '_ensure_tag_prefix', 1, 2, 1).
python_function('src/tagi/cli.py', 'scan', 2, 6, 9).
python_function('src/tagi/cli.py', 'list_groups', 1, 4, 9).
python_function('src/tagi/cli.py', 'stats', 1, 12, 18).
python_function('src/tagi/cli.py', 'inspect', 3, 15, 20).
python_function('src/tagi/cli.py', 'filter', 3, 17, 17).
python_function('src/tagi/cli.py', 'file', 2, 7, 14).
python_function('src/tagi/cli.py', 'summary', 2, 15, 20).
python_function('src/tagi/cli.py', 'draft', 3, 10, 14).
python_function('src/tagi/cli.py', 'send', 6, 27, 19).
python_function('src/tagi/cli.py', 'publish', 4, 17, 20).
python_function('src/tagi/cli.py', '_display_changes', 2, 2, 5).
python_function('src/tagi/cli.py', '_format_tags', 2, 5, 4).
python_function('src/tagi/cli.py', '_display_groups', 1, 2, 7).
python_function('src/tagi/cli.py', '_display_changes_grouped', 1, 5, 10).
python_function('src/tagi/cli.py', 'detect_provider', 1, 3, 3).
python_function('src/tagi/cli.py', 'create_pr', 3, 2, 5).
python_function('src/tagi/cli.py', 'create_mr', 3, 2, 5).
python_function('src/tagi/composer/commit_message.py', 'generate_commit_message', 4, 14, 12).
python_function('src/tagi/composer/commit_message.py', 'generate_conventional_message', 1, 12, 2).
python_function('src/tagi/composer/commit_message.py', 'generate_detailed_message', 1, 7, 5).
python_function('src/tagi/composer/commit_message.py', 'generate_simple_message', 1, 7, 2).
python_function('src/tagi/composer/commit_message.py', 'generate_oneline_message', 1, 6, 2).
python_function('src/tagi/composer/commit_message.py', 'generate_files_message', 1, 4, 3).
python_function('src/tagi/composer/commit_message.py', '_infer_scope', 1, 7, 2).
python_function('src/tagi/composer/summary.py', 'generate_summary', 1, 11, 4).
python_function('src/tagi/composer/summary.py', 'generate_file_list', 2, 5, 3).
python_function('src/tagi/heuristics/metrics.py', 'calculate_metrics', 2, 1, 6).
python_function('src/tagi/heuristics/metrics.py', '_calculate_complexity', 1, 5, 6).
python_function('src/tagi/heuristics/metrics.py', '_calculate_impact', 1, 5, 3).
python_function('src/tagi/heuristics/metrics.py', '_calculate_stability', 1, 1, 2).
python_function('src/tagi/heuristics/metrics.py', '_calculate_test_impact', 1, 4, 2).
python_function('src/tagi/heuristics/metrics.py', '_calculate_dependency_depth', 1, 4, 2).
python_function('src/tagi/heuristics/metrics.py', 'filter_by_metrics', 7, 5, 1).
python_function('src/tagi/heuristics/metrics.py', 'sort_by_metric', 3, 1, 2).
python_function('src/tagi/heuristics/metrics.py', 'calculate_vector_distance', 2, 2, 4).
python_function('src/tagi/heuristics/rules.py', '_get_config_attr', 2, 1, 2).
python_function('src/tagi/heuristics/rules.py', 'get_custom_rules', 1, 1, 1).
python_function('src/tagi/heuristics/rules.py', 'get_custom_heuristics', 1, 1, 1).
python_function('src/tagi/heuristics/scoring.py', 'calculate_risk_score', 2, 7, 1).
python_function('src/tagi/heuristics/tags.py', 'apply_tags', 2, 11, 10).
python_function('src/tagi/heuristics/tags.py', 'apply_path_tags', 2, 4, 3).
python_function('src/tagi/hooks.py', 'install_hooks', 1, 2, 4).
python_function('src/tagi/hooks.py', 'uninstall_hooks', 1, 3, 3).
python_function('src/tagi/hooks.py', 'check_hooks_installed', 1, 2, 3).
python_function('src/tagi/hooks.py', 'list_hooks', 1, 5, 7).
python_function('src/tagi/hooks.py', 'run_hook', 2, 2, 5).
python_function('src/tagi/planner/branch_grouper.py', 'group_by_branch', 2, 8, 7).
python_function('src/tagi/planner/branch_grouper.py', 'get_branch_info', 1, 5, 4).
python_function('src/tagi/planner/grouper.py', 'group_changes', 1, 7, 8).
python_function('src/tagi/planner/grouper.py', 'group_by_tag', 2, 1, 1).
python_function('src/tagi/planner/grouper.py', 'group_by_risk', 2, 5, 0).
python_function('src/tagi/planner/grouper.py', '_get_primary_tag', 1, 4, 0).
python_function('src/tagi/planner/preview.py', 'preview_plan', 2, 7, 4).
python_function('src/tagi/planner/preview.py', 'preview_changes', 1, 3, 3).
python_function('src/tagi/planner/selector.py', 'select_changes_by_tag', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_low_risk_changes', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_small_changes', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_by_tags', 3, 8, 2).
python_function('src/tagi/planner/selector.py', 'select_safe_changes', 1, 8, 1).
python_function('src/tagi/planner/sorter.py', 'sort_by_complexity', 1, 1, 4).
python_function('src/tagi/planner/sorter.py', 'sort_by_tag_priority', 2, 2, 4).
python_function('src/tagi/planner/sorter.py', 'group_by_complexity', 2, 5, 5).
python_function('src/tagi/providers/detector.py', 'detect_provider', 1, 3, 3).
python_function('src/tagi/scanner/diff.py', 'get_diff', 2, 1, 1).
python_function('src/tagi/scanner/diff.py', 'get_staged_diff', 2, 1, 1).
python_function('src/tagi/scanner/files.py', 'count_lines_changed', 2, 7, 5).
python_function('src/tagi/scanner/status.py', 'scan_repo', 1, 7, 13).
python_function('src/tagi/scanner/status.py', 'parse_status', 1, 4, 0).
python_function('src/tagi/utils/logger.py', 'setup_logger', 4, 4, 10).
python_function('src/tagi/utils/logger.py', 'get_logger', 1, 1, 1).
python_function('tests/test_e2e.py', 'test_send_workflow_scan', 0, 4, 8).
python_function('tests/test_e2e.py', 'test_send_workflow_grouping', 0, 2, 8).
python_function('tests/test_e2e.py', 'test_send_workflow_commit_message', 0, 3, 8).
python_function('tests/test_e2e.py', 'test_send_workflow_tag_filtering', 0, 4, 8).
python_function('tests/test_e2e.py', 'test_publish_workflow_full', 0, 3, 8).
python_function('tests/test_github_provider.py', 'test_github_provider_initialization', 0, 2, 2).
python_function('tests/test_github_provider.py', 'test_github_provider_detect_remote', 0, 2, 4).
python_function('tests/test_github_provider.py', 'test_github_provider_detect_non_github_remote', 0, 2, 4).
python_function('tests/test_github_provider.py', 'test_github_provider_detect_no_remote', 0, 2, 4).
python_function('tests/test_github_provider.py', 'test_github_provider_get_auth_status', 0, 4, 5).
python_function('tests/test_github_provider.py', 'test_github_provider_is_authenticated', 0, 3, 5).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_initialization', 0, 2, 2).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_detect_remote', 0, 2, 4).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_detect_non_gitlab_remote', 0, 2, 4).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_detect_no_remote', 0, 2, 4).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_get_auth_status', 0, 4, 5).
python_function('tests/test_gitlab_provider.py', 'test_gitlab_provider_is_authenticated', 0, 3, 5).
python_function('tests/test_tagi.py', 'test_auto_prefix_with_hash', 0, 3, 1).
python_function('tests/test_tagi.py', 'test_auto_prefix_without_hash', 0, 4, 1).
python_function('tests/test_tagi.py', 'test_auto_prefix_empty_string', 0, 2, 1).
python_function('tests/test_tagi.py', 'test_tag_enum_creation_with_prefix', 0, 3, 1).
python_function('tests/test_tagi.py', 'test_tag_enum_creation_without_prefix', 0, 3, 1).
python_function('tests/test_tagi.py', 'test_tag_with_prefix_in_filter', 0, 4, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_case_sensitive', 0, 5, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_single_tag', 0, 6, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_multiple_tags_or', 0, 7, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_multiple_tags_and', 0, 7, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_no_match', 0, 4, 3).
python_function('tests/test_tagi.py', 'test_tag_filtering_all_tags_match', 0, 4, 3).
python_function('tests/test_tagi.py', 'test_send_help_uses_repo_path_option', 0, 5, 1).
python_function('tests/test_tagi.py', 'test_send_invalid_tag_exits_cleanly', 1, 3, 3).
python_function('tests/test_tagi.py', 'test_publish_invalid_tag_exits_cleanly', 1, 3, 3).
python_function('tests/test_tagi.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_tagi.py', 'test_import', 0, 1, 0).
python_function('tests/test_tagi.py', 'test_change_creation', 0, 4, 1).
python_function('tests/test_tagi.py', 'test_change_with_tags', 0, 4, 2).
python_function('tests/test_tagi.py', 'test_multiple_tags', 0, 5, 2).
python_function('tests/test_tagi.py', 'test_tag_values', 0, 11, 0).
python_function('tests/test_tagi.py', 'test_changetype_values', 0, 5, 0).
python_function('tests/test_tagi.py', 'test_change_with_metadata', 0, 5, 1).
python_function('tests/test_tagi.py', 'test_config_loading', 0, 4, 7).
python_function('tests/test_tagi.py', 'test_config_no_file', 0, 4, 5).
python_function('tests/test_tagi.py', 'test_planner_grouper', 0, 3, 5).
python_function('tests/test_tagi.py', 'test_planner_group_by_risk', 0, 5, 3).
python_function('tests/test_tagi.py', 'test_planner_selector_by_tags', 0, 3, 3).
python_function('tests/test_tagi.py', 'test_planner_select_safe', 0, 3, 3).
python_function('tests/test_tagi.py', 'test_composer_conventional', 0, 2, 3).
python_function('tests/test_tagi.py', 'test_composer_summary', 0, 3, 2).
python_function('tests/test_tagi.py', 'test_executor_git_executor', 0, 3, 4).
python_function('tests/test_tagi.py', 'test_executor_publish_executor', 0, 3, 2).
python_function('tests/test_tagi.py', 'test_executor_dry_run', 0, 6, 3).

% ── Python Classes ───────────────────────────────────────
python_class('src/tagi/analyzer/metrics.py', 'MetricsCollector').
python_method('MetricsCollector', '__init__', 0, 1, 0).
python_method('MetricsCollector', 'collect', 1, 12, 3).
python_method('MetricsCollector', 'to_json', 0, 1, 1).
python_method('MetricsCollector', 'save', 1, 2, 3).
python_class('src/tagi/config.py', 'Config').
python_method('Config', '__init__', 1, 1, 1).
python_method('Config', '_load_config', 0, 13, 6).
python_method('Config', 'get_tag_for_path', 1, 3, 2).
python_method('Config', 'get_custom_tags_for_pattern', 1, 1, 1).
python_method('Config', 'get_tag_color', 1, 1, 1).
python_method('Config', 'get_heuristics_for_path', 1, 3, 3).
python_method('Config', 'get_tag_description', 1, 1, 1).
python_method('Config', 'get_template', 1, 1, 1).
python_method('Config', 'should_ignore', 1, 3, 1).
python_class('src/tagi/executor/git.py', 'GitExecutor').
python_method('GitExecutor', '__init__', 1, 1, 0).
python_method('GitExecutor', 'add', 1, 3, 2).
python_method('GitExecutor', 'commit', 2, 3, 3).
python_method('GitExecutor', 'push', 3, 4, 3).
python_method('GitExecutor', 'status', 0, 1, 1).
python_method('GitExecutor', 'get_current_branch', 0, 2, 2).
python_method('GitExecutor', 'get_remote_url', 1, 2, 2).
python_method('GitExecutor', 'has_staged_changes', 0, 1, 3).
python_class('src/tagi/executor/publish.py', 'PublishExecutor').
python_method('PublishExecutor', '__init__', 1, 1, 1).
python_method('PublishExecutor', 'stage_and_commit', 3, 2, 2).
python_method('PublishExecutor', 'publish', 6, 3, 2).
python_method('PublishExecutor', 'dry_run', 2, 1, 1).
python_class('src/tagi/llm/llx_adapter.py', 'LlxAdapter').
python_method('LlxAdapter', '__init__', 2, 2, 1).
python_method('LlxAdapter', 'is_available', 0, 2, 0).
python_method('LlxAdapter', 'improve_message', 2, 4, 1).
python_method('LlxAdapter', 'improve_description', 2, 4, 1).
python_class('src/tagi/models/change.py', 'ChangeType').
python_class('src/tagi/models/change.py', 'Tag').
python_class('src/tagi/models/change.py', 'ChangeMetrics').
python_method('ChangeMetrics', 'to_vector', 0, 1, 0).
python_class('src/tagi/models/change.py', 'Change').
python_class('src/tagi/models/group.py', 'ChangeGroup').
python_class('src/tagi/models/plan.py', 'PlanStep').
python_class('src/tagi/models/plan.py', 'Plan').
python_class('src/tagi/providers/base.py', 'BaseProvider').
python_method('BaseProvider', '__init__', 1, 1, 0).
python_method('BaseProvider', 'is_authenticated', 0, 1, 0).
python_method('BaseProvider', 'get_auth_status', 0, 1, 0).
python_method('BaseProvider', 'create_pr', 6, 1, 0).
python_method('BaseProvider', 'detect_remote', 0, 1, 0).
python_method('BaseProvider', '_run_command', 1, 1, 1).
python_method('BaseProvider', '_get_git_remote_url', 0, 2, 2).
python_method('BaseProvider', '_check_git_remote_for_provider', 1, 2, 2).
python_class('src/tagi/providers/github.py', 'GitHubProvider').
python_method('GitHubProvider', 'is_authenticated', 0, 1, 1).
python_method('GitHubProvider', 'get_auth_status', 0, 2, 1).
python_method('GitHubProvider', 'get_token', 0, 2, 2).
python_method('GitHubProvider', 'create_pr', 6, 4, 4).
python_method('GitHubProvider', 'detect_remote', 0, 1, 1).
python_class('src/tagi/providers/gitlab.py', 'GitLabProvider').
python_method('GitLabProvider', 'is_authenticated', 0, 1, 1).
python_method('GitLabProvider', 'get_auth_status', 0, 2, 1).
python_method('GitLabProvider', 'get_configured_host', 0, 4, 3).
python_method('GitLabProvider', 'create_pr', 6, 4, 4).
python_method('GitLabProvider', 'detect_remote', 0, 1, 1).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').

