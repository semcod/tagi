# tagi

Orchestrator for Git change shipments

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `tagi`
- **version**: `0.17.0`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(1), app.doql.less, goal.yaml, .env.example, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: tagi;
  version: 0.17.0;
}

dependencies {
  runtime: "typer>=0.12.0, rich>=13.7.0, pydantic>=2.5.0, tomli>=2.0.0; python_version<'3.11'";
  dev: "pytest>=7.4.0, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="tagi"] {

}

deploy {
  target: pip;
}

environment[name="local"] {
  runtime: python;
  env_file: .env;
  python_version: >=3.10;
}
```

## Interfaces

### CLI Entry Points

- `tagi`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m tagi
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m tagi --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m tagi --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m tagi --help" 10000
ASSERT_EXIT_CODE 0
```

## Configuration

```yaml
project:
  name: tagi
  version: 0.17.0
  env: local
```

## Dependencies

### Runtime

```text markpact:deps python
typer>=0.12.0
rich>=13.7.0
pydantic>=2.5.0
tomli>=2.0.0; python_version<'3.11'
```

### Development

```text markpact:deps python scope=dev
pytest>=7.4.0
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Deployment

```bash markpact:run
pip install tagi

# development install
pip install -e .[dev]
```

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`tagi`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.13/site-packages/cryptography/__init__.py:__version__`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# tagi | 35f 2474L | python:32,shell:2,less:1 | 2026-05-26
# stats: 74 func | 13 cls | 35 mod | CC̄=5.0 | critical:10 | cycles:0
# alerts[5]: CC inspect=15; CC send=14; CC publish=13; CC stats=12; CC generate_conventional_message=12
# hotspots[5]: inspect fan=20; publish fan=20; summary fan=19; stats fan=18; send fan=17
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[35]:
  app.doql.less,29
  project.sh,48
  src/tagi/__init__.py,48
  src/tagi/cli.py,797
  src/tagi/composer/__init__.py,13
  src/tagi/composer/commit_message.py,134
  src/tagi/composer/summary.py,46
  src/tagi/config.py,130
  src/tagi/executor/__init__.py,10
  src/tagi/executor/git.py,115
  src/tagi/executor/publish.py,40
  src/tagi/heuristics/__init__.py,14
  src/tagi/heuristics/rules.py,16
  src/tagi/heuristics/scoring.py,32
  src/tagi/heuristics/tags.py,84
  src/tagi/llm/__init__.py,8
  src/tagi/llm/llx_adapter.py,56
  src/tagi/models/__init__.py,15
  src/tagi/models/change.py,38
  src/tagi/models/group.py,17
  src/tagi/models/plan.py,24
  src/tagi/planner/__init__.py,19
  src/tagi/planner/grouper.py,76
  src/tagi/planner/preview.py,42
  src/tagi/planner/selector.py,45
  src/tagi/providers/__init__.py,12
  src/tagi/providers/base.py,59
  src/tagi/providers/github.py,48
  src/tagi/providers/gitlab.py,56
  src/tagi/scanner/__init__.py,14
  src/tagi/scanner/diff.py,32
  src/tagi/scanner/files.py,31
  src/tagi/scanner/status.py,68
  tests/test_tagi.py,256
  tree.sh,2
D:
  src/tagi/__init__.py:
  src/tagi/cli.py:
    e: scan,list_groups,stats,_find_change_by_tag,_calculate_tag_metrics,_display_tag_metrics,inspect,filter,file,_build_summary_header,_build_summary_statistics,_build_summary_by_type,_build_summary_tag_distribution,_build_summary_file_list,summary,draft,send,_parse_commit_message,_display_pr_preview,_create_pr_for_provider,publish,_display_changes,_format_tags,_display_groups,_display_changes_grouped,detect_provider,create_pr,create_mr
    scan(repo_path;grouped)
    list_groups(repo_path)
    stats(repo_path)
    _find_change_by_tag(changes;tag)
    _calculate_tag_metrics(filtered_changes)
    _display_tag_metrics(filtered_changes;tag)
    inspect(tag;repo_path;diff)
    filter(tags;repo_path;match_all)
    file(file_path;repo_path)
    _build_summary_header(repo_path;changes_count)
    _build_summary_statistics(changes)
    _build_summary_by_type(changes)
    _build_summary_tag_distribution(changes;config)
    _build_summary_file_list(changes)
    summary(repo_path;output)
    draft(tag;repo_path;template)
    send(tag;repo_path;dry_run;push;template)
    _parse_commit_message(message)
    _display_pr_preview(title;body;provider)
    _create_pr_for_provider(provider;title;body;repo_path)
    publish(tag;repo_path;dry_run;template)
    _display_changes(changes;config)
    _format_tags(tags;config)
    _display_groups(groups)
    _display_changes_grouped(changes)
    detect_provider(repo_path)
    create_pr(title;body;repo_path)
    create_mr(title;body;repo_path)
  src/tagi/composer/__init__.py:
  src/tagi/composer/commit_message.py:
    e: generate_commit_message,generate_conventional_message,generate_detailed_message,_infer_scope
    generate_commit_message(changes;template;repo_path;use_llm)
    generate_conventional_message(changes)
    generate_detailed_message(changes)
    _infer_scope(changes)
  src/tagi/composer/summary.py:
    e: generate_summary,generate_file_list
    generate_summary(changes)
    generate_file_list(changes;max_files)
  src/tagi/config.py:
    e: Config
    Config: __init__(1),_load_config(0),get_tag_for_path(1),get_custom_tags_for_pattern(1),get_tag_color(1),get_heuristics_for_path(1),get_tag_description(1),get_template(1),should_ignore(1)  # Configuration loaded from tagi.toml.
  src/tagi/executor/__init__.py:
  src/tagi/executor/git.py:
    e: GitExecutor
    GitExecutor: __init__(1),add(1),commit(2),push(3),status(0),get_current_branch(0),get_remote_url(1),has_staged_changes(0)  # Executor for git commands.
  src/tagi/executor/publish.py:
    e: PublishExecutor
    PublishExecutor: __init__(1),stage_and_commit(3),publish(6),dry_run(2)  # Executor for publishing changes.
  src/tagi/heuristics/__init__.py:
  src/tagi/heuristics/rules.py:
    e: get_custom_rules,get_custom_heuristics
    get_custom_rules(repo_path)
    get_custom_heuristics(repo_path)
  src/tagi/heuristics/scoring.py:
    e: calculate_risk_score
    calculate_risk_score(change;tags)
  src/tagi/heuristics/tags.py:
    e: apply_tags,apply_path_tags
    apply_tags(changes;repo_path)
    apply_path_tags(change;lines_changed)
  src/tagi/llm/__init__.py:
  src/tagi/llm/llx_adapter.py:
    e: LlxAdapter
    LlxAdapter: __init__(2),is_available(0),improve_message(2),improve_description(2)  # Adapter for LLX library for optional LLM integration.
  src/tagi/models/__init__.py:
  src/tagi/models/change.py:
    e: ChangeType,Tag,Change
    ChangeType:  # Type of git change.
    Tag:  # Hashtag categories for changes.
    Change:  # Represents a single file change.
  src/tagi/models/group.py:
    e: ChangeGroup
    ChangeGroup:  # Group of related changes.
  src/tagi/models/plan.py:
    e: PlanStep,Plan
    PlanStep:  # A single step in an execution plan.
    Plan:  # An execution plan for shipping changes.
  src/tagi/planner/__init__.py:
  src/tagi/planner/grouper.py:
    e: group_changes,group_by_tag,group_by_risk,_get_primary_tag
    group_changes(changes)
    group_by_tag(changes;tag)
    group_by_risk(changes;threshold)
    _get_primary_tag(tags)
  src/tagi/planner/preview.py:
    e: preview_plan,preview_changes
    preview_plan(changes;tag)
    preview_changes(group)
  src/tagi/planner/selector.py:
    e: select_changes_by_tag,select_low_risk_changes,select_small_changes,select_by_tags,select_safe_changes
    select_changes_by_tag(changes;tag)
    select_low_risk_changes(changes;threshold)
    select_small_changes(changes;max_lines)
    select_by_tags(changes;tags;require_all)
    select_safe_changes(changes)
  src/tagi/providers/__init__.py:
  src/tagi/providers/base.py:
    e: BaseProvider
    BaseProvider: __init__(1),is_authenticated(0),get_auth_status(0),create_pr(6),detect_remote(0),_run_command(1),_get_git_remote_url(0),_check_git_remote_for_provider(1)  # Base class for Git hosting providers.
  src/tagi/providers/github.py:
    e: GitHubProvider
    GitHubProvider: is_authenticated(0),get_auth_status(0),get_token(0),create_pr(6),detect_remote(0)  # GitHub provider using gh CLI.
  src/tagi/providers/gitlab.py:
    e: GitLabProvider
    GitLabProvider: is_authenticated(0),get_auth_status(0),get_configured_host(0),create_pr(6),detect_remote(0)  # GitLab provider using glab CLI.
  src/tagi/scanner/__init__.py:
  src/tagi/scanner/diff.py:
    e: get_diff,get_staged_diff
    get_diff(file_path;repo_path)
    get_staged_diff(file_path;repo_path)
  src/tagi/scanner/files.py:
    e: count_lines_changed
    count_lines_changed(file_path;repo_path)
  src/tagi/scanner/status.py:
    e: scan_repo,parse_status
    scan_repo(repo_path)
    parse_status(status)
  tests/test_tagi.py:
    e: test_placeholder,test_import,test_change_creation,test_change_with_tags,test_multiple_tags,test_tag_values,test_changetype_values,test_change_with_metadata,test_config_loading,test_config_no_file,test_planner_grouper,test_planner_group_by_risk,test_planner_selector_by_tags,test_planner_select_safe,test_composer_conventional,test_composer_summary,test_executor_git_executor,test_executor_publish_executor,test_executor_dry_run
    test_placeholder()
    test_import()
    test_change_creation()
    test_change_with_tags()
    test_multiple_tags()
    test_tag_values()
    test_changetype_values()
    test_change_with_metadata()
    test_config_loading()
    test_config_no_file()
    test_planner_grouper()
    test_planner_group_by_risk()
    test_planner_selector_by_tags()
    test_planner_select_safe()
    test_composer_conventional()
    test_composer_summary()
    test_executor_git_executor()
    test_executor_publish_executor()
    test_executor_dry_run()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('tagi', '0.17.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 29, 'less').
project_file('project.sh', 48, 'shell').
project_file('src/tagi/__init__.py', 48, 'python').
project_file('src/tagi/cli.py', 797, 'python').
project_file('src/tagi/composer/__init__.py', 13, 'python').
project_file('src/tagi/composer/commit_message.py', 134, 'python').
project_file('src/tagi/composer/summary.py', 46, 'python').
project_file('src/tagi/config.py', 130, 'python').
project_file('src/tagi/executor/__init__.py', 10, 'python').
project_file('src/tagi/executor/git.py', 115, 'python').
project_file('src/tagi/executor/publish.py', 40, 'python').
project_file('src/tagi/heuristics/__init__.py', 14, 'python').
project_file('src/tagi/heuristics/rules.py', 16, 'python').
project_file('src/tagi/heuristics/scoring.py', 32, 'python').
project_file('src/tagi/heuristics/tags.py', 84, 'python').
project_file('src/tagi/llm/__init__.py', 8, 'python').
project_file('src/tagi/llm/llx_adapter.py', 56, 'python').
project_file('src/tagi/models/__init__.py', 15, 'python').
project_file('src/tagi/models/change.py', 38, 'python').
project_file('src/tagi/models/group.py', 17, 'python').
project_file('src/tagi/models/plan.py', 24, 'python').
project_file('src/tagi/planner/__init__.py', 19, 'python').
project_file('src/tagi/planner/grouper.py', 76, 'python').
project_file('src/tagi/planner/preview.py', 42, 'python').
project_file('src/tagi/planner/selector.py', 45, 'python').
project_file('src/tagi/providers/__init__.py', 12, 'python').
project_file('src/tagi/providers/base.py', 59, 'python').
project_file('src/tagi/providers/github.py', 48, 'python').
project_file('src/tagi/providers/gitlab.py', 56, 'python').
project_file('src/tagi/scanner/__init__.py', 14, 'python').
project_file('src/tagi/scanner/diff.py', 32, 'python').
project_file('src/tagi/scanner/files.py', 31, 'python').
project_file('src/tagi/scanner/status.py', 68, 'python').
project_file('tests/test_tagi.py', 256, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('src/tagi/cli.py', 'scan', 2, 6, 9).
python_function('src/tagi/cli.py', 'list_groups', 1, 4, 9).
python_function('src/tagi/cli.py', 'stats', 1, 12, 18).
python_function('src/tagi/cli.py', '_find_change_by_tag', 2, 4, 2).
python_function('src/tagi/cli.py', '_calculate_tag_metrics', 1, 4, 2).
python_function('src/tagi/cli.py', '_display_tag_metrics', 2, 1, 7).
python_function('src/tagi/cli.py', 'inspect', 3, 15, 20).
python_function('src/tagi/cli.py', 'filter', 3, 6, 12).
python_function('src/tagi/cli.py', 'file', 2, 7, 14).
python_function('src/tagi/cli.py', '_build_summary_header', 2, 1, 0).
python_function('src/tagi/cli.py', '_build_summary_statistics', 1, 3, 3).
python_function('src/tagi/cli.py', '_build_summary_by_type', 1, 3, 4).
python_function('src/tagi/cli.py', '_build_summary_tag_distribution', 2, 5, 4).
python_function('src/tagi/cli.py', '_build_summary_file_list', 1, 3, 2).
python_function('src/tagi/cli.py', 'summary', 2, 5, 19).
python_function('src/tagi/cli.py', 'draft', 3, 10, 14).
python_function('src/tagi/cli.py', 'send', 5, 14, 17).
python_function('src/tagi/cli.py', '_parse_commit_message', 1, 2, 3).
python_function('src/tagi/cli.py', '_display_pr_preview', 3, 1, 1).
python_function('src/tagi/cli.py', '_create_pr_for_provider', 4, 3, 2).
python_function('src/tagi/cli.py', 'publish', 4, 13, 20).
python_function('src/tagi/cli.py', '_display_changes', 2, 2, 5).
python_function('src/tagi/cli.py', '_format_tags', 2, 5, 4).
python_function('src/tagi/cli.py', '_display_groups', 1, 2, 7).
python_function('src/tagi/cli.py', '_display_changes_grouped', 1, 5, 10).
python_function('src/tagi/cli.py', 'detect_provider', 1, 3, 3).
python_function('src/tagi/cli.py', 'create_pr', 3, 2, 5).
python_function('src/tagi/cli.py', 'create_mr', 3, 2, 5).
python_function('src/tagi/composer/commit_message.py', 'generate_commit_message', 4, 11, 9).
python_function('src/tagi/composer/commit_message.py', 'generate_conventional_message', 1, 12, 2).
python_function('src/tagi/composer/commit_message.py', 'generate_detailed_message', 1, 7, 5).
python_function('src/tagi/composer/commit_message.py', '_infer_scope', 1, 7, 2).
python_function('src/tagi/composer/summary.py', 'generate_summary', 1, 11, 4).
python_function('src/tagi/composer/summary.py', 'generate_file_list', 2, 5, 3).
python_function('src/tagi/heuristics/rules.py', 'get_custom_rules', 1, 1, 1).
python_function('src/tagi/heuristics/rules.py', 'get_custom_heuristics', 1, 1, 1).
python_function('src/tagi/heuristics/scoring.py', 'calculate_risk_score', 2, 7, 1).
python_function('src/tagi/heuristics/tags.py', 'apply_tags', 2, 11, 9).
python_function('src/tagi/heuristics/tags.py', 'apply_path_tags', 2, 4, 3).
python_function('src/tagi/planner/grouper.py', 'group_changes', 1, 7, 8).
python_function('src/tagi/planner/grouper.py', 'group_by_tag', 2, 3, 0).
python_function('src/tagi/planner/grouper.py', 'group_by_risk', 2, 5, 0).
python_function('src/tagi/planner/grouper.py', '_get_primary_tag', 1, 4, 0).
python_function('src/tagi/planner/preview.py', 'preview_plan', 2, 7, 4).
python_function('src/tagi/planner/preview.py', 'preview_changes', 1, 3, 3).
python_function('src/tagi/planner/selector.py', 'select_changes_by_tag', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_low_risk_changes', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_small_changes', 2, 3, 0).
python_function('src/tagi/planner/selector.py', 'select_by_tags', 3, 8, 2).
python_function('src/tagi/planner/selector.py', 'select_safe_changes', 1, 8, 1).
python_function('src/tagi/scanner/diff.py', 'get_diff', 2, 1, 1).
python_function('src/tagi/scanner/diff.py', 'get_staged_diff', 2, 1, 1).
python_function('src/tagi/scanner/files.py', 'count_lines_changed', 2, 7, 5).
python_function('src/tagi/scanner/status.py', 'scan_repo', 1, 7, 13).
python_function('src/tagi/scanner/status.py', 'parse_status', 1, 4, 0).
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
```

## Call Graph

*24 nodes · 27 edges · 7 modules · CC̄=4.0*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `publish` *(in src.tagi.cli)* | 13 ⚠ | 0 | 33 | **33** |
| `send` *(in src.tagi.cli)* | 14 ⚠ | 0 | 32 | **32** |
| `apply_tags` *(in src.tagi.heuristics.tags)* | 11 ⚠ | 10 | 15 | **25** |
| `scan_repo` *(in src.tagi.scanner.status)* | 7 | 10 | 15 | **25** |
| `draft` *(in src.tagi.cli)* | 10 ⚠ | 0 | 22 | **22** |
| `group_changes` *(in src.tagi.planner.grouper)* | 7 | 4 | 11 | **15** |
| `scan` *(in src.tagi.cli)* | 6 | 0 | 15 | **15** |
| `_display_changes_grouped` *(in src.tagi.cli)* | 5 | 1 | 12 | **13** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/tagi
# generated in 0.01s
# nodes: 24 | edges: 27 | modules: 7
# CC̄=4.0

HUBS[20]:
  src.tagi.cli.publish
    CC=13  in:0  out:33  total:33
  src.tagi.cli.send
    CC=14  in:0  out:32  total:32
  src.tagi.heuristics.tags.apply_tags
    CC=11  in:10  out:15  total:25
  src.tagi.scanner.status.scan_repo
    CC=7  in:10  out:15  total:25
  src.tagi.cli.draft
    CC=10  in:0  out:22  total:22
  src.tagi.planner.grouper.group_changes
    CC=7  in:4  out:11  total:15
  src.tagi.cli.scan
    CC=6  in:0  out:15  total:15
  src.tagi.cli._display_changes_grouped
    CC=5  in:1  out:12  total:13
  src.tagi.composer.commit_message.generate_detailed_message
    CC=7  in:1  out:12  total:13
  src.tagi.cli.list_groups
    CC=4  in:0  out:13  total:13
  src.tagi.composer.commit_message.generate_commit_message
    CC=11  in:3  out:9  total:12
  src.tagi.cli._display_changes
    CC=2  in:3  out:7  total:10
  src.tagi.cli._display_groups
    CC=2  in:1  out:8  total:9
  src.tagi.scanner.files.count_lines_changed
    CC=7  in:1  out:7  total:8
  src.tagi.cli._format_tags
    CC=5  in:4  out:4  total:8
  src.tagi.cli.create_pr
    CC=2  in:1  out:5  total:6
  src.tagi.cli.create_mr
    CC=2  in:1  out:5  total:6
  src.tagi.heuristics.tags.apply_path_tags
    CC=4  in:1  out:3  total:4
  src.tagi.cli._create_pr_for_provider
    CC=3  in:1  out:2  total:3
  src.tagi.heuristics.scoring.calculate_risk_score
    CC=7  in:1  out:2  total:3

MODULES:
  src.tagi.cli  [12 funcs]
    _create_pr_for_provider  CC=3  out:2
    _display_changes  CC=2  out:7
    _display_changes_grouped  CC=5  out:12
    _display_groups  CC=2  out:8
    _format_tags  CC=5  out:4
    create_mr  CC=2  out:5
    create_pr  CC=2  out:5
    draft  CC=10  out:22
    list_groups  CC=4  out:13
    publish  CC=13  out:33
  src.tagi.composer.commit_message  [4 funcs]
    _infer_scope  CC=7  out:2
    generate_commit_message  CC=11  out:9
    generate_conventional_message  CC=12  out:2
    generate_detailed_message  CC=7  out:12
  src.tagi.heuristics.scoring  [1 funcs]
    calculate_risk_score  CC=7  out:2
  src.tagi.heuristics.tags  [2 funcs]
    apply_path_tags  CC=4  out:3
    apply_tags  CC=11  out:15
  src.tagi.planner.grouper  [2 funcs]
    _get_primary_tag  CC=4  out:0
    group_changes  CC=7  out:11
  src.tagi.scanner.files  [1 funcs]
    count_lines_changed  CC=7  out:7
  src.tagi.scanner.status  [2 funcs]
    parse_status  CC=4  out:0
    scan_repo  CC=7  out:15

EDGES:
  src.tagi.planner.grouper.group_changes → src.tagi.planner.grouper._get_primary_tag
  src.tagi.scanner.status.scan_repo → src.tagi.scanner.status.parse_status
  src.tagi.cli.scan → src.tagi.scanner.status.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes_grouped
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.cli._display_groups
  src.tagi.cli.list_groups → src.tagi.scanner.status.scan_repo
  src.tagi.cli.list_groups → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.list_groups → src.tagi.planner.grouper.group_changes
  src.tagi.cli.draft → src.tagi.composer.commit_message.generate_commit_message
  src.tagi.cli.send → src.tagi.scanner.status.scan_repo
  src.tagi.cli.send → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.send → src.tagi.planner.grouper.group_changes
  src.tagi.cli._create_pr_for_provider → src.tagi.cli.create_pr
  src.tagi.cli._create_pr_for_provider → src.tagi.cli.create_mr
  src.tagi.cli.publish → src.tagi.scanner.status.scan_repo
  src.tagi.cli.publish → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.publish → src.tagi.planner.grouper.group_changes
  src.tagi.cli._display_changes → src.tagi.cli._format_tags
  src.tagi.cli._display_groups → src.tagi.cli._format_tags
  src.tagi.heuristics.tags.apply_tags → src.tagi.scanner.files.count_lines_changed
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.scoring.calculate_risk_score
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.tags.apply_path_tags
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_conventional_message
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_detailed_message
  src.tagi.composer.commit_message.generate_conventional_message → src.tagi.composer.commit_message._infer_scope
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Intent

Orchestrator for Git change shipments
