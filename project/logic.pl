% ── Project Metadata ─────────────────────────────────────
project_metadata('tagi', '0.1.1', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 29, 'less').
project_file('project.sh', 48, 'shell').
project_file('src/tagi/__init__.py', 2, 'python').
project_file('src/tagi/cli.py', 273, 'python').
project_file('src/tagi/composer.py', 59, 'python').
project_file('src/tagi/config.py', 64, 'python').
project_file('src/tagi/executor.py', 60, 'python').
project_file('src/tagi/heuristics.py', 123, 'python').
project_file('src/tagi/models.py', 48, 'python').
project_file('src/tagi/planner.py', 29, 'python').
project_file('src/tagi/providers.py', 70, 'python').
project_file('src/tagi/scanner.py', 47, 'python').
project_file('tests/test_tagi.py', 12, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('src/tagi/cli.py', 'scan', 1, 3, 9).
python_function('src/tagi/cli.py', 'list_groups', 1, 2, 7).
python_function('src/tagi/cli.py', 'inspect', 2, 4, 7).
python_function('src/tagi/cli.py', 'draft', 2, 4, 8).
python_function('src/tagi/cli.py', 'send', 4, 10, 15).
python_function('src/tagi/cli.py', 'publish', 3, 11, 17).
python_function('src/tagi/cli.py', '_display_changes', 1, 3, 5).
python_function('src/tagi/cli.py', '_display_groups', 1, 3, 7).
python_function('src/tagi/composer.py', 'generate_commit_message', 1, 14, 5).
python_function('src/tagi/composer.py', '_build_title', 2, 1, 1).
python_function('src/tagi/executor.py', 'stage_changes', 3, 5, 4).
python_function('src/tagi/executor.py', 'commit_changes', 3, 3, 2).
python_function('src/tagi/executor.py', 'push_changes', 2, 3, 2).
python_function('src/tagi/heuristics.py', 'apply_tags', 2, 24, 9).
python_function('src/tagi/heuristics.py', '_count_lines_changed', 2, 7, 5).
python_function('src/tagi/heuristics.py', '_calculate_risk_score', 2, 7, 1).
python_function('src/tagi/planner.py', 'group_changes', 1, 7, 6).
python_function('src/tagi/providers.py', 'create_pr', 4, 4, 2).
python_function('src/tagi/providers.py', 'create_mr', 4, 4, 2).
python_function('src/tagi/providers.py', 'detect_provider', 1, 3, 1).
python_function('src/tagi/scanner.py', 'scan_repo', 1, 3, 6).
python_function('src/tagi/scanner.py', '_parse_status', 1, 4, 0).
python_function('tests/test_tagi.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_tagi.py', 'test_import', 0, 1, 0).

% ── Python Classes ───────────────────────────────────────
python_class('src/tagi/config.py', 'Config').
python_method('Config', '__init__', 1, 1, 1).
python_method('Config', '_load_config', 0, 6, 5).
python_method('Config', 'get_tag_for_path', 1, 3, 2).
python_method('Config', 'get_custom_tags_for_pattern', 1, 1, 1).
python_class('src/tagi/models.py', 'ChangeType').
python_class('src/tagi/models.py', 'Tag').
python_class('src/tagi/models.py', 'Change').
python_class('src/tagi/models.py', 'ChangeGroup').

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

