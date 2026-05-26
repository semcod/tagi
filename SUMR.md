# tagi

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `tagi`
- **version**: `0.49.1`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(1), app.doql.less, goal.yaml, .env.example, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: tagi;
  version: 0.49.1;
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

## Call Graph

*66 nodes · 60 edges · 21 modules · CC̄=3.9*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `send` *(in src.tagi.cli)* | 23 ⚠ | 0 | 48 | **48** |
| `publish` *(in src.tagi.cli)* | 12 ⚠ | 0 | 45 | **45** |
| `filter` *(in src.tagi.cli)* | 11 ⚠ | 0 | 28 | **28** |
| `summary` *(in src.tagi.cli)* | 5 | 0 | 28 | **28** |
| `inspect` *(in src.tagi.cli)* | 11 ⚠ | 0 | 28 | **28** |
| `apply_tags` *(in src.tagi.heuristics.tags)* | 11 ⚠ | 10 | 16 | **26** |
| `scan_repo` *(in src.tagi.scanner.status)* | 7 | 10 | 15 | **25** |
| `draft` *(in src.tagi.cli)* | 10 ⚠ | 0 | 22 | **22** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/tagi
# generated in 0.03s
# nodes: 66 | edges: 60 | modules: 21
# CC̄=3.9

HUBS[20]:
  src.tagi.cli.send
    CC=23  in:0  out:48  total:48
  src.tagi.cli.publish
    CC=12  in:0  out:45  total:45
  src.tagi.cli.filter
    CC=11  in:0  out:28  total:28
  src.tagi.cli.summary
    CC=5  in:0  out:28  total:28
  src.tagi.cli.inspect
    CC=11  in:0  out:28  total:28
  src.tagi.heuristics.tags.apply_tags
    CC=11  in:10  out:16  total:26
  src.tagi.scanner.status.scan_repo
    CC=7  in:10  out:15  total:25
  src.tagi.cli.draft
    CC=10  in:0  out:22  total:22
  src.tagi.utils.logger.setup_logger
    CC=4  in:2  out:15  total:17
  src.tagi.composer.commit_message.generate_commit_message
    CC=15  in:3  out:13  total:16
  src.tagi.cli.scan
    CC=6  in:0  out:15  total:15
  src.tagi.composer.commit_message.generate_detailed_message
    CC=7  in:1  out:12  total:13
  src.tagi.cli._do_list_groups
    CC=4  in:2  out:11  total:13
  src.tagi.planner.grouper.group_changes
    CC=7  in:2  out:11  total:13
  src.tagi.cli._display_changes_grouped
    CC=5  in:1  out:12  total:13
  src.tagi.utils.inspect_helpers.display_statistics_table
    CC=1  in:1  out:11  total:12
  src.tagi.heuristics.metrics._calculate_complexity
    CC=5  in:1  out:10  total:11
  src.tagi.cli._display_changes
    CC=2  in:3  out:7  total:10
  src.tagi.cli._display_groups
    CC=2  in:1  out:8  total:9
  src.tagi.analyzer.dependency_graph.analyze_python_imports
    CC=8  in:1  out:8  total:9

MODULES:
  src.tagi.analyzer.dependency_graph  [2 funcs]
    analyze_python_imports  CC=8  out:8
    build_dependency_graph  CC=3  out:4
  src.tagi.cli  [20 funcs]
    _configure_command_logging  CC=2  out:2
    _display_changes  CC=2  out:7
    _display_changes_grouped  CC=5  out:12
    _display_groups  CC=2  out:8
    _do_list_groups  CC=4  out:11
    _ensure_tag_prefix  CC=2  out:1
    _format_tags  CC=5  out:4
    _is_known_tag  CC=2  out:2
    _resolve_send_target  CC=5  out:5
    detect_provider  CC=3  out:4
  src.tagi.composer.commit_message  [6 funcs]
    _infer_scope  CC=7  out:2
    generate_commit_message  CC=15  out:13
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
  src.tagi.providers.github  [3 funcs]
    create_pr  CC=1  out:3
    get_auth_status  CC=1  out:2
    is_authenticated  CC=1  out:2
  src.tagi.providers.gitlab  [3 funcs]
    create_pr  CC=1  out:3
    get_auth_status  CC=1  out:2
    is_authenticated  CC=1  out:2
  src.tagi.providers.utils.auth  [2 funcs]
    get_auth_status_from_result  CC=2  out:0
    is_authenticated_from_result  CC=1  out:0
  src.tagi.providers.utils.pr  [2 funcs]
    build_pr_command  CC=5  out:4
    execute_pr_command  CC=2  out:0
  src.tagi.scanner.files  [1 funcs]
    count_lines_changed  CC=7  out:7
  src.tagi.scanner.status  [2 funcs]
    parse_status  CC=4  out:0
    scan_repo  CC=7  out:15
  src.tagi.utils.inspect_helpers  [2 funcs]
    calculate_tag_statistics  CC=4  out:5
    display_statistics_table  CC=1  out:11
  src.tagi.utils.logger  [1 funcs]
    setup_logger  CC=4  out:15
  src.tagi.utils.publish_helpers  [2 funcs]
    detect_and_get_provider  CC=3  out:3
    filter_changes_by_tag  CC=3  out:1
  src.tagi.utils.send_helpers  [1 funcs]
    resolve_filtered_changes  CC=5  out:3
  src.tagi.utils.summary_helpers  [1 funcs]
    build_report_header  CC=1  out:7

EDGES:
  src.tagi.cli.setup_logging → src.tagi.utils.logger.setup_logger
  src.tagi.cli._configure_command_logging → src.tagi.utils.logger.setup_logger
  src.tagi.cli._is_known_tag → src.tagi.cli._ensure_tag_prefix
  src.tagi.cli._resolve_send_target → src.tagi.cli._is_known_tag
  src.tagi.cli.scan → src.tagi.scanner.status.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes_grouped
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.cli._do_list_groups
  src.tagi.cli.list_cmd → src.tagi.cli._do_list_groups
  src.tagi.cli._do_list_groups → src.tagi.cli._display_groups
  src.tagi.cli._do_list_groups → src.tagi.scanner.status.scan_repo
  src.tagi.cli._do_list_groups → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli._do_list_groups → src.tagi.planner.grouper.group_changes
  src.tagi.cli.inspect → src.tagi.utils.inspect_helpers.display_statistics_table
  src.tagi.cli.inspect → src.tagi.cli._display_changes
  src.tagi.cli.filter → src.tagi.cli._display_changes
  src.tagi.cli.filter → src.tagi.scanner.status.scan_repo
  src.tagi.cli.filter → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.summary → src.tagi.utils.summary_helpers.build_report_header
  src.tagi.cli.draft → src.tagi.composer.commit_message.generate_commit_message
  src.tagi.cli.send → src.tagi.cli._configure_command_logging
  src.tagi.cli.send → src.tagi.cli._resolve_send_target
  src.tagi.cli.publish → src.tagi.cli._configure_command_logging
  src.tagi.cli.publish → src.tagi.cli._ensure_tag_prefix
  src.tagi.cli.publish → src.tagi.utils.publish_helpers.filter_changes_by_tag
  src.tagi.cli._display_changes → src.tagi.cli._format_tags
  src.tagi.cli._display_groups → src.tagi.cli._format_tags
  src.tagi.analyzer.dependency_graph.build_dependency_graph → src.tagi.analyzer.dependency_graph.analyze_python_imports
  src.tagi.planner.sorter.group_by_complexity → src.tagi.planner.sorter.sort_by_complexity
  src.tagi.planner.grouper.group_changes → src.tagi.planner.grouper._get_primary_tag
  src.tagi.planner.grouper.group_by_tag → src.tagi.planner.selector.select_changes_by_tag
  src.tagi.providers.gitlab.GitLabProvider.is_authenticated → src.tagi.providers.utils.auth.is_authenticated_from_result
  src.tagi.providers.gitlab.GitLabProvider.get_auth_status → src.tagi.providers.utils.auth.get_auth_status_from_result
  src.tagi.providers.gitlab.GitLabProvider.create_pr → src.tagi.providers.utils.pr.build_pr_command
  src.tagi.providers.gitlab.GitLabProvider.create_pr → src.tagi.providers.utils.pr.execute_pr_command
  src.tagi.providers.github.GitHubProvider.is_authenticated → src.tagi.providers.utils.auth.is_authenticated_from_result
  src.tagi.providers.github.GitHubProvider.get_auth_status → src.tagi.providers.utils.auth.get_auth_status_from_result
  src.tagi.providers.github.GitHubProvider.create_pr → src.tagi.providers.utils.pr.build_pr_command
  src.tagi.providers.github.GitHubProvider.create_pr → src.tagi.providers.utils.pr.execute_pr_command
  src.tagi.scanner.status.scan_repo → src.tagi.scanner.status.parse_status
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_complexity
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_stability
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_test_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_dependency_depth
  src.tagi.heuristics.tags.apply_tags → src.tagi.scanner.files.count_lines_changed
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.metrics.calculate_metrics
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.scoring.calculate_risk_score
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.tags.apply_path_tags
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/tagi
# generated in 0.03s
# nodes: 66 | edges: 60 | modules: 21
# CC̄=3.9

HUBS[20]:
  src.tagi.cli.send
    CC=23  in:0  out:48  total:48
  src.tagi.cli.publish
    CC=12  in:0  out:45  total:45
  src.tagi.cli.filter
    CC=11  in:0  out:28  total:28
  src.tagi.cli.summary
    CC=5  in:0  out:28  total:28
  src.tagi.cli.inspect
    CC=11  in:0  out:28  total:28
  src.tagi.heuristics.tags.apply_tags
    CC=11  in:10  out:16  total:26
  src.tagi.scanner.status.scan_repo
    CC=7  in:10  out:15  total:25
  src.tagi.cli.draft
    CC=10  in:0  out:22  total:22
  src.tagi.utils.logger.setup_logger
    CC=4  in:2  out:15  total:17
  src.tagi.composer.commit_message.generate_commit_message
    CC=15  in:3  out:13  total:16
  src.tagi.cli.scan
    CC=6  in:0  out:15  total:15
  src.tagi.composer.commit_message.generate_detailed_message
    CC=7  in:1  out:12  total:13
  src.tagi.cli._do_list_groups
    CC=4  in:2  out:11  total:13
  src.tagi.planner.grouper.group_changes
    CC=7  in:2  out:11  total:13
  src.tagi.cli._display_changes_grouped
    CC=5  in:1  out:12  total:13
  src.tagi.utils.inspect_helpers.display_statistics_table
    CC=1  in:1  out:11  total:12
  src.tagi.heuristics.metrics._calculate_complexity
    CC=5  in:1  out:10  total:11
  src.tagi.cli._display_changes
    CC=2  in:3  out:7  total:10
  src.tagi.cli._display_groups
    CC=2  in:1  out:8  total:9
  src.tagi.analyzer.dependency_graph.analyze_python_imports
    CC=8  in:1  out:8  total:9

MODULES:
  src.tagi.analyzer.dependency_graph  [2 funcs]
    analyze_python_imports  CC=8  out:8
    build_dependency_graph  CC=3  out:4
  src.tagi.cli  [20 funcs]
    _configure_command_logging  CC=2  out:2
    _display_changes  CC=2  out:7
    _display_changes_grouped  CC=5  out:12
    _display_groups  CC=2  out:8
    _do_list_groups  CC=4  out:11
    _ensure_tag_prefix  CC=2  out:1
    _format_tags  CC=5  out:4
    _is_known_tag  CC=2  out:2
    _resolve_send_target  CC=5  out:5
    detect_provider  CC=3  out:4
  src.tagi.composer.commit_message  [6 funcs]
    _infer_scope  CC=7  out:2
    generate_commit_message  CC=15  out:13
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
  src.tagi.providers.github  [3 funcs]
    create_pr  CC=1  out:3
    get_auth_status  CC=1  out:2
    is_authenticated  CC=1  out:2
  src.tagi.providers.gitlab  [3 funcs]
    create_pr  CC=1  out:3
    get_auth_status  CC=1  out:2
    is_authenticated  CC=1  out:2
  src.tagi.providers.utils.auth  [2 funcs]
    get_auth_status_from_result  CC=2  out:0
    is_authenticated_from_result  CC=1  out:0
  src.tagi.providers.utils.pr  [2 funcs]
    build_pr_command  CC=5  out:4
    execute_pr_command  CC=2  out:0
  src.tagi.scanner.files  [1 funcs]
    count_lines_changed  CC=7  out:7
  src.tagi.scanner.status  [2 funcs]
    parse_status  CC=4  out:0
    scan_repo  CC=7  out:15
  src.tagi.utils.inspect_helpers  [2 funcs]
    calculate_tag_statistics  CC=4  out:5
    display_statistics_table  CC=1  out:11
  src.tagi.utils.logger  [1 funcs]
    setup_logger  CC=4  out:15
  src.tagi.utils.publish_helpers  [2 funcs]
    detect_and_get_provider  CC=3  out:3
    filter_changes_by_tag  CC=3  out:1
  src.tagi.utils.send_helpers  [1 funcs]
    resolve_filtered_changes  CC=5  out:3
  src.tagi.utils.summary_helpers  [1 funcs]
    build_report_header  CC=1  out:7

EDGES:
  src.tagi.cli.setup_logging → src.tagi.utils.logger.setup_logger
  src.tagi.cli._configure_command_logging → src.tagi.utils.logger.setup_logger
  src.tagi.cli._is_known_tag → src.tagi.cli._ensure_tag_prefix
  src.tagi.cli._resolve_send_target → src.tagi.cli._is_known_tag
  src.tagi.cli.scan → src.tagi.scanner.status.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes_grouped
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.cli._do_list_groups
  src.tagi.cli.list_cmd → src.tagi.cli._do_list_groups
  src.tagi.cli._do_list_groups → src.tagi.cli._display_groups
  src.tagi.cli._do_list_groups → src.tagi.scanner.status.scan_repo
  src.tagi.cli._do_list_groups → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli._do_list_groups → src.tagi.planner.grouper.group_changes
  src.tagi.cli.inspect → src.tagi.utils.inspect_helpers.display_statistics_table
  src.tagi.cli.inspect → src.tagi.cli._display_changes
  src.tagi.cli.filter → src.tagi.cli._display_changes
  src.tagi.cli.filter → src.tagi.scanner.status.scan_repo
  src.tagi.cli.filter → src.tagi.heuristics.tags.apply_tags
  src.tagi.cli.summary → src.tagi.utils.summary_helpers.build_report_header
  src.tagi.cli.draft → src.tagi.composer.commit_message.generate_commit_message
  src.tagi.cli.send → src.tagi.cli._configure_command_logging
  src.tagi.cli.send → src.tagi.cli._resolve_send_target
  src.tagi.cli.publish → src.tagi.cli._configure_command_logging
  src.tagi.cli.publish → src.tagi.cli._ensure_tag_prefix
  src.tagi.cli.publish → src.tagi.utils.publish_helpers.filter_changes_by_tag
  src.tagi.cli._display_changes → src.tagi.cli._format_tags
  src.tagi.cli._display_groups → src.tagi.cli._format_tags
  src.tagi.analyzer.dependency_graph.build_dependency_graph → src.tagi.analyzer.dependency_graph.analyze_python_imports
  src.tagi.planner.sorter.group_by_complexity → src.tagi.planner.sorter.sort_by_complexity
  src.tagi.planner.grouper.group_changes → src.tagi.planner.grouper._get_primary_tag
  src.tagi.planner.grouper.group_by_tag → src.tagi.planner.selector.select_changes_by_tag
  src.tagi.providers.gitlab.GitLabProvider.is_authenticated → src.tagi.providers.utils.auth.is_authenticated_from_result
  src.tagi.providers.gitlab.GitLabProvider.get_auth_status → src.tagi.providers.utils.auth.get_auth_status_from_result
  src.tagi.providers.gitlab.GitLabProvider.create_pr → src.tagi.providers.utils.pr.build_pr_command
  src.tagi.providers.gitlab.GitLabProvider.create_pr → src.tagi.providers.utils.pr.execute_pr_command
  src.tagi.providers.github.GitHubProvider.is_authenticated → src.tagi.providers.utils.auth.is_authenticated_from_result
  src.tagi.providers.github.GitHubProvider.get_auth_status → src.tagi.providers.utils.auth.get_auth_status_from_result
  src.tagi.providers.github.GitHubProvider.create_pr → src.tagi.providers.utils.pr.build_pr_command
  src.tagi.providers.github.GitHubProvider.create_pr → src.tagi.providers.utils.pr.execute_pr_command
  src.tagi.scanner.status.scan_repo → src.tagi.scanner.status.parse_status
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_complexity
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_stability
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_test_impact
  src.tagi.heuristics.metrics.calculate_metrics → src.tagi.heuristics.metrics._calculate_dependency_depth
  src.tagi.heuristics.tags.apply_tags → src.tagi.scanner.files.count_lines_changed
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.metrics.calculate_metrics
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.scoring.calculate_risk_score
  src.tagi.heuristics.tags.apply_tags → src.tagi.heuristics.tags.apply_path_tags
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 52f 4341L | python:47,yaml:2,toml:1,txt:1,shell:1 | 2026-05-26
# generated in 0.01s
# CC̅=3.9 | critical:2/152 | dups:0 | cycles:0

HEALTH[2]:
  🟡 CC    send CC=23 (limit:15)
  🟡 CC    generate_commit_message CC=15 (limit:15)

REFACTOR[1]:
  1. split 2 high-CC methods  (CC>15)

PIPELINES[85]:
  [1] Src [__init__]: __init__
      PURITY: 100% pure
  [2] Src [_load_config]: _load_config
      PURITY: 100% pure
  [3] Src [get_tag_for_path]: get_tag_for_path
      PURITY: 100% pure
  [4] Src [get_custom_tags_for_pattern]: get_custom_tags_for_pattern
      PURITY: 100% pure
  [5] Src [get_tag_color]: get_tag_color
      PURITY: 100% pure
  [6] Src [get_heuristics_for_path]: get_heuristics_for_path
      PURITY: 100% pure
  [7] Src [get_tag_description]: get_tag_description
      PURITY: 100% pure
  [8] Src [get_template]: get_template
      PURITY: 100% pure
  [9] Src [should_ignore]: should_ignore
      PURITY: 100% pure
  [10] Src [setup_logging]: setup_logging → setup_logger
      PURITY: 100% pure
  [11] Src [scan]: scan → scan_repo → parse_status
      PURITY: 100% pure
  [12] Src [list_groups]: list_groups → _do_list_groups → _display_groups → _format_tags
      PURITY: 100% pure
  [13] Src [list_cmd]: list_cmd → _do_list_groups → _display_groups → _format_tags
      PURITY: 100% pure
  [14] Src [stats]: stats → scan_repo → parse_status
      PURITY: 100% pure
  [15] Src [inspect]: inspect → display_statistics_table → calculate_tag_statistics
      PURITY: 100% pure
  [16] Src [filter]: filter → _display_changes → _format_tags
      PURITY: 100% pure
  [17] Src [file]: file → scan_repo → parse_status
      PURITY: 100% pure
  [18] Src [summary]: summary → build_report_header
      PURITY: 100% pure
  [19] Src [draft]: draft → generate_commit_message → generate_conventional_message → _infer_scope
      PURITY: 100% pure
  [20] Src [send]: send → _configure_command_logging → setup_logger
      PURITY: 100% pure
  [21] Src [publish]: publish → _configure_command_logging → setup_logger
      PURITY: 100% pure
  [22] Src [install_hooks]: install_hooks
      PURITY: 100% pure
  [23] Src [uninstall_hooks]: uninstall_hooks
      PURITY: 100% pure
  [24] Src [check_hooks_installed]: check_hooks_installed
      PURITY: 100% pure
  [25] Src [list_hooks]: list_hooks
      PURITY: 100% pure
  [26] Src [run_hook]: run_hook
      PURITY: 100% pure
  [27] Src [build_dependency_graph]: build_dependency_graph → analyze_python_imports
      PURITY: 100% pure
  [28] Src [find_dependency_order]: find_dependency_order
      PURITY: 100% pure
  [29] Src [detect_cycles]: detect_cycles
      PURITY: 100% pure
  [30] Src [get_critical_path]: get_critical_path
      PURITY: 100% pure
  [31] Src [collect]: collect
      PURITY: 100% pure
  [32] Src [to_json]: to_json
      PURITY: 100% pure
  [33] Src [save]: save
      PURITY: 100% pure
  [34] Src [generate_report]: generate_report
      PURITY: 100% pure
  [35] Src [sort_by_tag_priority]: sort_by_tag_priority
      PURITY: 100% pure
  [36] Src [group_by_complexity]: group_by_complexity → sort_by_complexity
      PURITY: 100% pure
  [37] Src [group_by_tag]: group_by_tag → select_changes_by_tag
      PURITY: 100% pure
  [38] Src [preview_plan]: preview_plan
      PURITY: 100% pure
  [39] Src [preview_changes]: preview_changes
      PURITY: 100% pure
  [40] Src [group_by_branch]: group_by_branch
      PURITY: 100% pure
  [41] Src [get_branch_info]: get_branch_info
      PURITY: 100% pure
  [42] Src [select_by_tags]: select_by_tags
      PURITY: 100% pure
  [43] Src [select_safe_changes]: select_safe_changes
      PURITY: 100% pure
  [44] Src [_run_command]: _run_command
      PURITY: 100% pure
  [45] Src [_get_git_remote_url]: _get_git_remote_url
      PURITY: 100% pure
  [46] Src [_check_git_remote_for_provider]: _check_git_remote_for_provider
      PURITY: 100% pure
  [47] Src [detect_provider]: detect_provider
      PURITY: 100% pure
  [48] Src [is_authenticated]: is_authenticated → is_authenticated_from_result
      PURITY: 100% pure
  [49] Src [get_auth_status]: get_auth_status → get_auth_status_from_result
      PURITY: 100% pure
  [50] Src [get_configured_host]: get_configured_host
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.9    ←in:0  →out:0
  │ !! cli                        797L  0C   24m  CC=23     ←2
  │ metrics                    214L  0C    9m  CC=5      ←1
  │ dependency_graph           195L  0C    5m  CC=10     ←0
  │ !! commit_message             185L  0C    7m  CC=15     ←1
  │ metrics                    153L  1C    6m  CC=12     ←0
  │ config                     129L  1C    9m  CC=13     ←0
  │ hooks                      125L  0C    5m  CC=5      ←0
  │ git                        114L  1C    8m  CC=4      ←0
  │ summary_helpers            113L  0C    5m  CC=5      ←1
  │ sorter                     104L  0C    3m  CC=5      ←1
  │ inspect_helpers             98L  0C    5m  CC=7      ←1
  │ branch_grouper              88L  0C    2m  CC=8      ←0
  │ tags                        87L  0C    2m  CC=11     ←1
  │ grouper                     76L  0C    4m  CC=7      ←1
  │ logger                      71L  0C    2m  CC=4      ←1
  │ send_helpers                70L  0C    2m  CC=5      ←0
  │ status                      67L  0C    2m  CC=7      ←1
  │ publish_helpers             62L  0C    3m  CC=4      ←1
  │ change                      60L  4C    1m  CC=1      ←0
  │ base                        58L  1C    8m  CC=2      ←0
  │ pr                          58L  0C    2m  CC=5      ←2
  │ llx_adapter                 55L  1C    4m  CC=4      ←0
  │ __init__                    47L  0C    0m  CC=0.0    ←0
  │ gitlab                      45L  1C    5m  CC=4      ←0
  │ summary                     45L  0C    2m  CC=11     ←0
  │ selector                    44L  0C    5m  CC=8      ←1
  │ preview                     41L  0C    2m  CC=7      ←0
  │ github                      39L  1C    5m  CC=2      ←0
  │ publish                     39L  1C    4m  CC=3      ←0
  │ detect_provider             33L  0C    1m  CC=4      ←0
  │ auth                        32L  0C    2m  CC=2      ←2
  │ diff                        31L  0C    2m  CC=1      ←1
  │ scoring                     31L  0C    1m  CC=7      ←1
  │ files                       30L  0C    1m  CC=7      ←1
  │ plan                        23L  2C    0m  CC=0.0    ←0
  │ rules                       21L  0C    3m  CC=1      ←0
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ group                       16L  1C    0m  CC=0.0    ←0
  │ detector                    15L  0C    1m  CC=3      ←0
  │ __init__                    14L  0C    0m  CC=0.0    ←0
  │ __init__                    13L  0C    0m  CC=0.0    ←0
  │ __init__                    13L  0C    0m  CC=0.0    ←0
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ __init__                    11L  0C    0m  CC=0.0    ←0
  │ __init__                     9L  0C    0m  CC=0.0    ←0
  │ __init__                     7L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                    89L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              64L  0C    0m  CC=0.0    ←0
  │ project.sh                  48L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │

COUPLING: no cross-package imports detected

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 10 groups | 47f 3609L | 2026-05-26

SUMMARY:
  files_scanned: 47
  total_lines:   3609
  dup_groups:    10
  dup_fragments: 20
  saved_lines:   77
  scan_ms:       2213

HOTSPOTS[7] (files with most duplication):
  src/tagi/utils/inspect_helpers.py  dup=54L  groups=2  frags=3  (1.5%)
  src/tagi/cli.py  dup=39L  groups=3  frags=5  (1.1%)
  src/tagi/providers/github.py  dup=17L  groups=4  frags=4  (0.5%)
  src/tagi/providers/gitlab.py  dup=17L  groups=4  frags=4  (0.5%)
  src/tagi/utils/publish_helpers.py  dup=12L  groups=1  frags=1  (0.3%)
  src/tagi/providers/detector.py  dup=9L  groups=1  frags=1  (0.2%)
  src/tagi/heuristics/rules.py  dup=6L  groups=1  frags=2  (0.2%)

DUPLICATES[10] (ranked by impact):
  [69031414365d89a7]   STRU  filter_changes_by_tags_any  L=21 N=2 saved=21 sim=1.00
      src/tagi/utils/inspect_helpers.py:23-43  (filter_changes_by_tags_any)
      src/tagi/utils/inspect_helpers.py:46-66  (filter_changes_by_tags_all)
  [34f34aac7a5602b7]   STRU  filter_changes_by_tag  L=12 N=2 saved=12 sim=1.00
      src/tagi/utils/inspect_helpers.py:9-20  (filter_changes_by_tag)
      src/tagi/utils/publish_helpers.py:28-39  (filter_changes_by_tag)
  [59cf75b9ca253237]   STRU  create_pr  L=10 N=2 saved=10 sim=1.00
      src/tagi/cli.py:772-781  (create_pr)
      src/tagi/cli.py:784-793  (create_mr)
  [0defbec6f6d556b3]   EXAC  detect_provider  L=9 N=2 saved=9 sim=1.00
      src/tagi/cli.py:761-769  (detect_provider)
      src/tagi/providers/detector.py:7-15  (detect_provider)
  [2f1566a469905cc9]   STRU  create_pr  L=6 N=2 saved=6 sim=1.00
      src/tagi/providers/github.py:30-35  (create_pr)
      src/tagi/providers/gitlab.py:36-41  (create_pr)
  [54c9428ffca26dbc]   STRU  list_groups  L=5 N=2 saved=5 sim=1.00
      src/tagi/cli.py:117-121  (list_groups)
      src/tagi/cli.py:125-129  (list_cmd)
  [9aaebb2fb961d57d]   STRU  is_authenticated  L=4 N=2 saved=4 sim=1.00
      src/tagi/providers/github.py:13-16  (is_authenticated)
      src/tagi/providers/gitlab.py:11-14  (is_authenticated)
  [180c7709efe6a452]   STRU  get_auth_status  L=4 N=2 saved=4 sim=1.00
      src/tagi/providers/github.py:18-21  (get_auth_status)
      src/tagi/providers/gitlab.py:16-19  (get_auth_status)
  [9e51ade4e046160f]   STRU  get_custom_rules  L=3 N=2 saved=3 sim=1.00
      src/tagi/heuristics/rules.py:14-16  (get_custom_rules)
      src/tagi/heuristics/rules.py:19-21  (get_custom_heuristics)
  [ead418deaec12c72]   STRU  detect_remote  L=3 N=2 saved=3 sim=1.00
      src/tagi/providers/github.py:37-39  (detect_remote)
      src/tagi/providers/gitlab.py:43-45  (detect_remote)

REFACTOR[10] (ranked by priority):
  [1] ○ extract_function   → src/tagi/utils/utils/filter_changes_by_tags_any.py
      WHY: 2 occurrences of 21-line block across 1 files — saves 21 lines
      FILES: src/tagi/utils/inspect_helpers.py
  [2] ○ extract_function   → src/tagi/utils/utils/filter_changes_by_tag.py
      WHY: 2 occurrences of 12-line block across 2 files — saves 12 lines
      FILES: src/tagi/utils/inspect_helpers.py, src/tagi/utils/publish_helpers.py
  [3] ○ extract_function   → src/tagi/utils/create_pr.py
      WHY: 2 occurrences of 10-line block across 1 files — saves 10 lines
      FILES: src/tagi/cli.py
  [4] ○ extract_function   → src/tagi/utils/detect_provider.py
      WHY: 2 occurrences of 9-line block across 2 files — saves 9 lines
      FILES: src/tagi/cli.py, src/tagi/providers/detector.py
  [5] ○ extract_function   → src/tagi/providers/utils/create_pr.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [6] ○ extract_function   → src/tagi/utils/list_groups.py
      WHY: 2 occurrences of 5-line block across 1 files — saves 5 lines
      FILES: src/tagi/cli.py
  [7] ○ extract_function   → src/tagi/providers/utils/is_authenticated.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [8] ○ extract_function   → src/tagi/providers/utils/get_auth_status.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [9] ○ extract_function   → src/tagi/heuristics/utils/get_custom_rules.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/tagi/heuristics/rules.py
  [10] ○ extract_function   → src/tagi/providers/utils/detect_remote.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py

QUICK_WINS[5] (low risk, high savings — do first):
  [1] extract_function   saved=21L  → src/tagi/utils/utils/filter_changes_by_tags_any.py
      FILES: inspect_helpers.py
  [2] extract_function   saved=12L  → src/tagi/utils/utils/filter_changes_by_tag.py
      FILES: inspect_helpers.py, publish_helpers.py
  [3] extract_function   saved=10L  → src/tagi/utils/create_pr.py
      FILES: cli.py
  [4] extract_function   saved=9L  → src/tagi/utils/detect_provider.py
      FILES: cli.py, detector.py
  [5] extract_function   saved=6L  → src/tagi/providers/utils/create_pr.py
      FILES: github.py, gitlab.py

EFFORT_ESTIMATE (total ≈ 2.6h):
  medium filter_changes_by_tags_any          saved=21L  ~42min
  easy   filter_changes_by_tag               saved=12L  ~24min
  easy   create_pr                           saved=10L  ~20min
  easy   detect_provider                     saved=9L  ~18min
  easy   create_pr                           saved=6L  ~12min
  easy   list_groups                         saved=5L  ~10min
  easy   is_authenticated                    saved=4L  ~8min
  easy   get_auth_status                     saved=4L  ~8min
  easy   get_custom_rules                    saved=3L  ~6min
  easy   detect_remote                       saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  10 → 0
  saved_lines: 77 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 152 func | 35f | 2026-05-26
# generated in 0.00s

NEXT[4] (ranked by impact):
  [1] !! SPLIT           src/tagi/cli.py
      WHY: 797L, 0 classes, max CC=23
      EFFORT: ~4h  IMPACT: 18331

  [2] !  SPLIT-FUNC      send  CC=23  fan=20
      WHY: CC=23 exceeds 15
      EFFORT: ~1h  IMPACT: 460

  [3] !  SPLIT-FUNC      generate_commit_message  CC=15  fan=12
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 180

  [4] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/tagi/cli.py may break 24 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.9 → ≤2.7
  max-CC:      23 → ≤11
  god-modules: 2 → 0
  high-CC(≥15): 2 → ≤1
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.9 → now CC̄=3.9
```

## Intent

Orchestrator for Git change shipments
