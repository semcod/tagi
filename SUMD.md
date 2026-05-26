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
- **version**: `0.47.0`
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
  version: 0.47.0;
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
  version: 0.47.0
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
# tagi | 46f 4051L | python:43,shell:2,less:1 | 2026-05-26
# stats: 130 func | 15 cls | 46 mod | CC̄=4.8 | critical:14 | cycles:0
# alerts[5]: CC send=27; CC filter=17; CC publish=17; CC inspect=15; CC summary=15
# hotspots[5]: inspect fan=20; summary fan=20; publish fan=20; send fan=19; stats fan=18
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[46]:
  app.doql.less,29
  project.sh,48
  src/tagi/__init__.py,48
  src/tagi/analyzer/dependency_graph.py,196
  src/tagi/analyzer/metrics.py,154
  src/tagi/cli.py,806
  src/tagi/composer/__init__.py,13
  src/tagi/composer/commit_message.py,184
  src/tagi/composer/summary.py,46
  src/tagi/config.py,130
  src/tagi/executor/__init__.py,10
  src/tagi/executor/git.py,115
  src/tagi/executor/publish.py,40
  src/tagi/heuristics/__init__.py,14
  src/tagi/heuristics/metrics.py,215
  src/tagi/heuristics/rules.py,22
  src/tagi/heuristics/scoring.py,32
  src/tagi/heuristics/tags.py,88
  src/tagi/hooks.py,126
  src/tagi/llm/__init__.py,8
  src/tagi/llm/llx_adapter.py,56
  src/tagi/models/__init__.py,15
  src/tagi/models/change.py,61
  src/tagi/models/group.py,17
  src/tagi/models/plan.py,24
  src/tagi/planner/__init__.py,19
  src/tagi/planner/branch_grouper.py,89
  src/tagi/planner/grouper.py,77
  src/tagi/planner/preview.py,42
  src/tagi/planner/selector.py,45
  src/tagi/planner/sorter.py,105
  src/tagi/providers/__init__.py,12
  src/tagi/providers/base.py,59
  src/tagi/providers/detector.py,16
  src/tagi/providers/github.py,48
  src/tagi/providers/gitlab.py,56
  src/tagi/scanner/__init__.py,14
  src/tagi/scanner/diff.py,32
  src/tagi/scanner/files.py,31
  src/tagi/scanner/status.py,68
  src/tagi/utils/logger.py,72
  tests/test_e2e.py,129
  tests/test_github_provider.py,78
  tests/test_gitlab_provider.py,77
  tests/test_tagi.py,483
  tree.sh,2
D:
  src/tagi/__init__.py:
  src/tagi/analyzer/dependency_graph.py:
    e: analyze_python_imports,build_dependency_graph,find_dependency_order,detect_cycles,get_critical_path
    analyze_python_imports(file_path;repo_path)
    build_dependency_graph(changes;repo_path)
    find_dependency_order(graph)
    detect_cycles(graph)
    get_critical_path(graph)
  src/tagi/analyzer/metrics.py:
    e: generate_report,compare_metrics,MetricsCollector
    MetricsCollector: __init__(0),collect(1),to_json(0),save(1)  # Collect and analyze metrics about changes.
    generate_report(metrics)
    compare_metrics(metrics1;metrics2)
  src/tagi/cli.py:
    e: setup_logging,_ensure_tag_prefix,scan,list_groups,stats,inspect,filter,file,summary,draft,send,publish,_display_changes,_format_tags,_display_groups,_display_changes_grouped,detect_provider,create_pr,create_mr
    setup_logging(verbose)
    _ensure_tag_prefix(tag)
    scan(repo_path;grouped)
    list_groups(repo_path)
    stats(repo_path)
    inspect(tag;repo_path;diff)
    filter(tags;repo_path;match_all)
    file(file_path;repo_path)
    summary(repo_path;output)
    draft(tag;repo_path;template)
    send(tag;repo_path;auto_order;dry_run;push;template)
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
    e: generate_commit_message,generate_conventional_message,generate_detailed_message,generate_simple_message,generate_oneline_message,generate_files_message,_infer_scope
    generate_commit_message(changes;template;repo_path;use_llm)
    generate_conventional_message(changes)
    generate_detailed_message(changes)
    generate_simple_message(changes)
    generate_oneline_message(changes)
    generate_files_message(changes)
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
  src/tagi/heuristics/metrics.py:
    e: calculate_metrics,_calculate_complexity,_calculate_impact,_calculate_stability,_calculate_test_impact,_calculate_dependency_depth,filter_by_metrics,sort_by_metric,calculate_vector_distance
    calculate_metrics(change;repo_path)
    _calculate_complexity(change)
    _calculate_impact(change)
    _calculate_stability(change)
    _calculate_test_impact(change)
    _calculate_dependency_depth(change)
    filter_by_metrics(changes;min_risk;max_risk;min_complexity;max_complexity;min_impact;max_impact)
    sort_by_metric(changes;metric;ascending)
    calculate_vector_distance(change1;change2)
  src/tagi/heuristics/rules.py:
    e: _get_config_attr,get_custom_rules,get_custom_heuristics
    _get_config_attr(repo_path;attr_name)
    get_custom_rules(repo_path)
    get_custom_heuristics(repo_path)
  src/tagi/heuristics/scoring.py:
    e: calculate_risk_score
    calculate_risk_score(change;tags)
  src/tagi/heuristics/tags.py:
    e: apply_tags,apply_path_tags
    apply_tags(changes;repo_path)
    apply_path_tags(change;lines_changed)
  src/tagi/hooks.py:
    e: install_hooks,uninstall_hooks,check_hooks_installed,list_hooks,run_hook
    install_hooks(repo_path)
    uninstall_hooks(repo_path)
    check_hooks_installed(repo_path)
    list_hooks(repo_path)
    run_hook(hook_name;repo_path)
  src/tagi/llm/__init__.py:
  src/tagi/llm/llx_adapter.py:
    e: LlxAdapter
    LlxAdapter: __init__(2),is_available(0),improve_message(2),improve_description(2)  # Adapter for LLX library for optional LLM integration.
  src/tagi/models/__init__.py:
  src/tagi/models/change.py:
    e: ChangeType,Tag,ChangeMetrics,Change
    ChangeType:  # Type of git change.
    Tag:  # Hashtag categories for changes.
    ChangeMetrics: to_vector(0)  # Numerical metrics for change analysis.
    Change:  # Represents a single file change.
  src/tagi/models/group.py:
    e: ChangeGroup
    ChangeGroup:  # Group of related changes.
  src/tagi/models/plan.py:
    e: PlanStep,Plan
    PlanStep:  # A single step in an execution plan.
    Plan:  # An execution plan for shipping changes.
  src/tagi/planner/__init__.py:
  src/tagi/planner/branch_grouper.py:
    e: group_by_branch,get_branch_info
    group_by_branch(changes;repo_path)
    get_branch_info(repo_path)
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
  src/tagi/planner/sorter.py:
    e: sort_by_complexity,sort_by_tag_priority,group_by_complexity
    sort_by_complexity(changes)
    sort_by_tag_priority(changes;tag_order)
    group_by_complexity(changes;num_groups)
  src/tagi/providers/__init__.py:
  src/tagi/providers/base.py:
    e: BaseProvider
    BaseProvider: __init__(1),is_authenticated(0),get_auth_status(0),create_pr(6),detect_remote(0),_run_command(1),_get_git_remote_url(0),_check_git_remote_for_provider(1)  # Base class for Git hosting providers.
  src/tagi/providers/detector.py:
    e: detect_provider
    detect_provider(repo_path)
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
  src/tagi/utils/logger.py:
    e: setup_logger,get_logger
    setup_logger(name;level;log_file;verbose)
    get_logger(name)
  tests/test_e2e.py:
    e: test_send_workflow_scan,test_send_workflow_grouping,test_send_workflow_commit_message,test_send_workflow_tag_filtering,test_publish_workflow_full
    test_send_workflow_scan()
    test_send_workflow_grouping()
    test_send_workflow_commit_message()
    test_send_workflow_tag_filtering()
    test_publish_workflow_full()
  tests/test_github_provider.py:
    e: test_github_provider_initialization,test_github_provider_detect_remote,test_github_provider_detect_non_github_remote,test_github_provider_detect_no_remote,test_github_provider_get_auth_status,test_github_provider_is_authenticated
    test_github_provider_initialization()
    test_github_provider_detect_remote()
    test_github_provider_detect_non_github_remote()
    test_github_provider_detect_no_remote()
    test_github_provider_get_auth_status()
    test_github_provider_is_authenticated()
  tests/test_gitlab_provider.py:
    e: test_gitlab_provider_initialization,test_gitlab_provider_detect_remote,test_gitlab_provider_detect_non_gitlab_remote,test_gitlab_provider_detect_no_remote,test_gitlab_provider_get_auth_status,test_gitlab_provider_is_authenticated
    test_gitlab_provider_initialization()
    test_gitlab_provider_detect_remote()
    test_gitlab_provider_detect_non_gitlab_remote()
    test_gitlab_provider_detect_no_remote()
    test_gitlab_provider_get_auth_status()
    test_gitlab_provider_is_authenticated()
  tests/test_tagi.py:
    e: test_auto_prefix_with_hash,test_auto_prefix_without_hash,test_auto_prefix_empty_string,test_tag_enum_creation_with_prefix,test_tag_enum_creation_without_prefix,test_tag_with_prefix_in_filter,test_tag_filtering_case_sensitive,test_tag_filtering_single_tag,test_tag_filtering_multiple_tags_or,test_tag_filtering_multiple_tags_and,test_tag_filtering_no_match,test_tag_filtering_all_tags_match,test_send_help_uses_repo_path_option,test_send_invalid_tag_exits_cleanly,test_publish_invalid_tag_exits_cleanly,test_placeholder,test_import,test_change_creation,test_change_with_tags,test_multiple_tags,test_tag_values,test_changetype_values,test_change_with_metadata,test_config_loading,test_config_no_file,test_planner_grouper,test_planner_group_by_risk,test_planner_selector_by_tags,test_planner_select_safe,test_composer_conventional,test_composer_summary,test_executor_git_executor,test_executor_publish_executor,test_executor_dry_run
    test_auto_prefix_with_hash()
    test_auto_prefix_without_hash()
    test_auto_prefix_empty_string()
    test_tag_enum_creation_with_prefix()
    test_tag_enum_creation_without_prefix()
    test_tag_with_prefix_in_filter()
    test_tag_filtering_case_sensitive()
    test_tag_filtering_single_tag()
    test_tag_filtering_multiple_tags_or()
    test_tag_filtering_multiple_tags_and()
    test_tag_filtering_no_match()
    test_tag_filtering_all_tags_match()
    test_send_help_uses_repo_path_option()
    test_send_invalid_tag_exits_cleanly(monkeypatch)
    test_publish_invalid_tag_exits_cleanly(monkeypatch)
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
```

## Call Graph

*43 nodes · 39 edges · 13 modules · CC̄=4.3*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `send` *(in src.tagi.cli)* | 27 ⚠ | 0 | 47 | **47** |
| `publish` *(in src.tagi.cli)* | 17 ⚠ | 0 | 45 | **45** |
| `filter` *(in src.tagi.cli)* | 17 ⚠ | 0 | 28 | **28** |
| `apply_tags` *(in src.tagi.heuristics.tags)* | 11 ⚠ | 10 | 16 | **26** |
| `scan_repo` *(in src.tagi.scanner.status)* | 7 | 10 | 15 | **25** |
| `draft` *(in src.tagi.cli)* | 10 ⚠ | 0 | 22 | **22** |
| `setup_logger` *(in src.tagi.utils.logger)* | 4 | 1 | 15 | **16** |
| `generate_commit_message` *(in src.tagi.composer.commit_message)* | 14 ⚠ | 3 | 12 | **15** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/tagi
# generated in 0.04s
# nodes: 43 | edges: 39 | modules: 13
# CC̄=4.3

HUBS[20]:
  src.tagi.cli.send
    CC=27  in:0  out:47  total:47
  src.tagi.cli.publish
    CC=17  in:0  out:45  total:45
  src.tagi.cli.filter
    CC=17  in:0  out:28  total:28
  src.tagi.heuristics.tags.apply_tags
    CC=11  in:10  out:16  total:26
  src.tagi.scanner.status.scan_repo
    CC=7  in:10  out:15  total:25
  src.tagi.cli.draft
    CC=10  in:0  out:22  total:22
  src.tagi.utils.logger.setup_logger
    CC=4  in:1  out:15  total:16
  src.tagi.composer.commit_message.generate_commit_message
    CC=14  in:3  out:12  total:15
  src.tagi.cli.scan
    CC=6  in:0  out:15  total:15
  src.tagi.cli._display_changes_grouped
    CC=5  in:1  out:12  total:13
  src.tagi.cli.list_groups
    CC=4  in:0  out:13  total:13
  src.tagi.composer.commit_message.generate_detailed_message
    CC=7  in:1  out:12  total:13
  src.tagi.planner.grouper.group_changes
    CC=7  in:2  out:11  total:13
  src.tagi.heuristics.metrics._calculate_complexity
    CC=5  in:1  out:10  total:11
  src.tagi.cli._display_changes
    CC=2  in:3  out:7  total:10
  src.tagi.analyzer.dependency_graph.analyze_python_imports
    CC=8  in:1  out:8  total:9
  src.tagi.cli._display_groups
    CC=2  in:1  out:8  total:9
  src.tagi.cli._format_tags
    CC=5  in:4  out:4  total:8
  src.tagi.heuristics.metrics._calculate_impact
    CC=5  in:1  out:7  total:8
  src.tagi.scanner.files.count_lines_changed
    CC=7  in:1  out:7  total:8

MODULES:
  src.tagi.analyzer.dependency_graph  [2 funcs]
    analyze_python_imports  CC=8  out:8
    build_dependency_graph  CC=3  out:4
  src.tagi.cli  [13 funcs]
    _display_changes  CC=2  out:7
    _display_changes_grouped  CC=5  out:12
    _display_groups  CC=2  out:8
    _ensure_tag_prefix  CC=2  out:1
    _format_tags  CC=5  out:4
    detect_provider  CC=3  out:4
    draft  CC=10  out:22
    filter  CC=17  out:28
    list_groups  CC=4  out:13
    publish  CC=17  out:45
  src.tagi.composer.commit_message  [6 funcs]
    _infer_scope  CC=7  out:2
    generate_commit_message  CC=14  out:12
    generate_conventional_message  CC=12  out:2
    generate_detailed_message  CC=7  out:12
    generate_oneline_message  CC=6  out:2
    generate_simple_message  CC=7  out:4
  src.tagi.heuristics.metrics  [6 funcs]
    _calculate_complexity  CC=5  out:10
    _calculate_dependency_depth  CC=4  out:4
    _calculate_impact  CC=5  out:7
    _calculate_stability  CC=1  out:2
    _calculate_test_impact  CC=4  out:2
    calculate_metrics  CC=1  out:6
  src.tagi.heuristics.rules  [3 funcs]
    _get_config_attr  CC=1  out:2
    get_custom_heuristics  CC=1  out:1
    get_custom_rules  CC=1  out:1
  src.tagi.heuristics.scoring  [1 funcs]
    calculate_risk_score  CC=7  out:2
  src.tagi.heuristics.tags  [2 funcs]
    apply_path_tags  CC=4  out:3
    apply_tags  CC=11  out:16
  src.tagi.planner.grouper  [3 funcs]
    _get_primary_tag  CC=4  out:0
    group_by_tag  CC=1  out:1
    group_changes  CC=7  out:11
  src.tagi.planner.selector  [1 funcs]
    select_changes_by_tag  CC=3  out:0
  src.tagi.planner.sorter  [2 funcs]
    group_by_complexity  CC=5  out:7
    sort_by_complexity  CC=1  out:4
  src.tagi.scanner.files  [1 funcs]
    count_lines_changed  CC=7  out:7
  src.tagi.scanner.status  [2 funcs]
    parse_status  CC=4  out:0
    scan_repo  CC=7  out:15
  src.tagi.utils.logger  [1 funcs]
    setup_logger  CC=4  out:15

EDGES:
  src.tagi.scanner.status.scan_repo → src.tagi.scanner.status.parse_status
  src.tagi.cli.setup_logging → src.tagi.utils.logger.setup_logger
  src.tagi.cli.scan → src.tagi.scanner.status.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes_grouped
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.cli._display_groups
  src.tagi.cli.list_groups → src.tagi.scanner.status.scan_repo
  src.tagi.cli.list_groups → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.list_groups → src.tagi.planner.grouper.group_changes
  src.tagi.cli.filter → src.tagi.cli._display_changes
  src.tagi.cli.filter → src.tagi.scanner.status.scan_repo
  src.tagi.cli.filter → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.draft → src.tagi.composer.commit_message.generate_commit_message
  src.tagi.cli.send → src.tagi.composer.commit_message.generate_commit_message
  src.tagi.cli.publish → src.tagi.cli._ensure_tag_prefix
  src.tagi.cli.publish → src.tagi.cli.detect_provider
  src.tagi.cli._display_changes → src.tagi.cli._format_tags
  src.tagi.cli._display_groups → src.tagi.cli._format_tags
  src.tagi.analyzer.dependency_graph.build_dependency_graph → src.tagi.analyzer.dependency_graph.analyze_python_imports
  src.tagi.planner.sorter.group_by_complexity → src.tagi.planner.sorter.sort_by_complexity
  src.tagi.planner.grouper.group_changes → src.tagi.planner.grouper._get_primary_tag
  src.tagi.planner.grouper.group_by_tag → src.tagi.planner.selector.select_changes_by_tag
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_complexity
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_stability
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_test_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_dependency_depth
  src.tagi.heuristics.tags.apply_tags → src.tagi.scanner.files.count_lines_changed
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.metrics.calculate_metrics
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.scoring.calculate_risk_score
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.tags.apply_path_tags
  src.tagi.heuristics.rules.get_custom_rules → src.tagi.heuristics.rules._get_config_attr
  src.tagi.heuristics.rules.get_custom_heuristics → src.tagi.heuristics.rules._get_config_attr
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_conventional_message
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_detailed_message
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_simple_message
  src.tagi.composer.commit_message.generate_commit_message → src.tagi.composer.commit_message.generate_oneline_message
  src.tagi.composer.commit_message.generate_conventional_message → src.tagi.composer.commit_message._infer_scope
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Intent

Orchestrator for Git change shipments
