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
- **version**: `0.47.0`
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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 44f 3875L | python:39,yaml:2,txt:1,shell:1,toml:1 | 2026-05-26
# generated in 0.02s
# CC̅=4.3 | critical:5/127 | dups:0 | cycles:0

HEALTH[5]:
  🟡 CC    inspect CC=15 (limit:15)
  🟡 CC    filter CC=17 (limit:15)
  🟡 CC    summary CC=15 (limit:15)
  🟡 CC    send CC=27 (limit:15)
  🟡 CC    publish CC=17 (limit:15)

REFACTOR[1]:
  1. split 5 high-CC methods  (CC>15)

PIPELINES[79]:
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
  [10] Src [preview_plan]: preview_plan
      PURITY: 100% pure
  [11] Src [preview_changes]: preview_changes
      PURITY: 100% pure
  [12] Src [select_by_tags]: select_by_tags
      PURITY: 100% pure
  [13] Src [select_safe_changes]: select_safe_changes
      PURITY: 100% pure
  [14] Src [_run_command]: _run_command
      PURITY: 100% pure
  [15] Src [_get_git_remote_url]: _get_git_remote_url
      PURITY: 100% pure
  [16] Src [_check_git_remote_for_provider]: _check_git_remote_for_provider
      PURITY: 100% pure
  [17] Src [is_authenticated]: is_authenticated
      PURITY: 100% pure
  [18] Src [get_auth_status]: get_auth_status
      PURITY: 100% pure
  [19] Src [get_configured_host]: get_configured_host
      PURITY: 100% pure
  [20] Src [create_pr]: create_pr
      PURITY: 100% pure
  [21] Src [detect_remote]: detect_remote
      PURITY: 100% pure
  [22] Src [is_authenticated]: is_authenticated
      PURITY: 100% pure
  [23] Src [get_auth_status]: get_auth_status
      PURITY: 100% pure
  [24] Src [get_token]: get_token
      PURITY: 100% pure
  [25] Src [create_pr]: create_pr
      PURITY: 100% pure
  [26] Src [detect_remote]: detect_remote
      PURITY: 100% pure
  [27] Src [get_staged_diff]: get_staged_diff
      PURITY: 100% pure
  [28] Src [__init__]: __init__
      PURITY: 100% pure
  [29] Src [improve_message]: improve_message
      PURITY: 100% pure
  [30] Src [improve_description]: improve_description
      PURITY: 100% pure
  [31] Src [generate_summary]: generate_summary
      PURITY: 100% pure
  [32] Src [generate_file_list]: generate_file_list
      PURITY: 100% pure
  [33] Src [add]: add
      PURITY: 100% pure
  [34] Src [commit]: commit
      PURITY: 100% pure
  [35] Src [push]: push
      PURITY: 100% pure
  [36] Src [status]: status
      PURITY: 100% pure
  [37] Src [get_current_branch]: get_current_branch
      PURITY: 100% pure
  [38] Src [get_remote_url]: get_remote_url
      PURITY: 100% pure
  [39] Src [has_staged_changes]: has_staged_changes
      PURITY: 100% pure
  [40] Src [__init__]: __init__
      PURITY: 100% pure
  [41] Src [stage_and_commit]: stage_and_commit
      PURITY: 100% pure
  [42] Src [publish]: publish
      PURITY: 100% pure
  [43] Src [dry_run]: dry_run
      PURITY: 100% pure
  [44] Src [setup_logging]: setup_logging → setup_logger
      PURITY: 100% pure
  [45] Src [scan]: scan → scan_repo → parse_status
      PURITY: 100% pure
  [46] Src [list_groups]: list_groups → _display_groups → _format_tags
      PURITY: 100% pure
  [47] Src [stats]: stats → scan_repo → parse_status
      PURITY: 100% pure
  [48] Src [inspect]: inspect → _display_changes → _format_tags
      PURITY: 100% pure
  [49] Src [filter]: filter → _display_changes → _format_tags
      PURITY: 100% pure
  [50] Src [file]: file → scan_repo → parse_status
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=4.3    ←in:0  →out:0
  │ !! cli                        805L  0C   19m  CC=27     ←0
  │ metrics                    214L  0C    9m  CC=5      ←1
  │ dependency_graph           195L  0C    5m  CC=10     ←0
  │ commit_message             183L  0C    7m  CC=14     ←1
  │ metrics                    153L  1C    6m  CC=12     ←0
  │ config                     129L  1C    9m  CC=13     ←0
  │ hooks                      125L  0C    5m  CC=5      ←0
  │ git                        114L  1C    8m  CC=4      ←0
  │ sorter                     104L  0C    3m  CC=5      ←1
  │ branch_grouper              88L  0C    2m  CC=8      ←0
  │ tags                        87L  0C    2m  CC=11     ←1
  │ grouper                     76L  0C    4m  CC=7      ←1
  │ logger                      71L  0C    2m  CC=4      ←1
  │ status                      67L  0C    2m  CC=7      ←1
  │ change                      60L  4C    1m  CC=1      ←0
  │ base                        58L  1C    8m  CC=2      ←0
  │ gitlab                      55L  1C    5m  CC=4      ←0
  │ llx_adapter                 55L  1C    4m  CC=4      ←0
  │ github                      47L  1C    5m  CC=4      ←0
  │ __init__                    47L  0C    0m  CC=0.0    ←0
  │ summary                     45L  0C    2m  CC=11     ←0
  │ selector                    44L  0C    5m  CC=8      ←1
  │ preview                     41L  0C    2m  CC=7      ←0
  │ publish                     39L  1C    4m  CC=3      ←0
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
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                    66L  0C    0m  CC=0.0    ←0
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
# redup/duplication | 7 groups | 39f 3166L | 2026-05-26

SUMMARY:
  files_scanned: 39
  total_lines:   3166
  dup_groups:    7
  dup_fragments: 14
  saved_lines:   49
  scan_ms:       3355

HOTSPOTS[5] (files with most duplication):
  src/tagi/cli.py  dup=29L  groups=2  frags=3  (0.9%)
  src/tagi/providers/github.py  dup=27L  groups=4  frags=4  (0.9%)
  src/tagi/providers/gitlab.py  dup=27L  groups=4  frags=4  (0.9%)
  src/tagi/providers/detector.py  dup=9L  groups=1  frags=1  (0.3%)
  src/tagi/heuristics/rules.py  dup=6L  groups=1  frags=2  (0.2%)

DUPLICATES[7] (ranked by impact):
  [69c9d9a76f7c052c]   STRU  create_pr  L=12 N=2 saved=12 sim=1.00
      src/tagi/providers/github.py:32-43  (create_pr)
      src/tagi/providers/gitlab.py:40-51  (create_pr)
  [59cf75b9ca253237]   STRU  create_pr  L=10 N=2 saved=10 sim=1.00
      src/tagi/cli.py:780-789  (create_pr)
      src/tagi/cli.py:792-801  (create_mr)
  [0defbec6f6d556b3]   EXAC  detect_provider  L=9 N=2 saved=9 sim=1.00
      src/tagi/cli.py:769-777  (detect_provider)
      src/tagi/providers/detector.py:7-15  (detect_provider)
  [c70db8b1b5e736e6]   STRU  get_auth_status  L=8 N=2 saved=8 sim=1.00
      src/tagi/providers/github.py:16-23  (get_auth_status)
      src/tagi/providers/gitlab.py:16-23  (get_auth_status)
  [c1f4c1bd38f4f90b]   STRU  is_authenticated  L=4 N=2 saved=4 sim=1.00
      src/tagi/providers/github.py:11-14  (is_authenticated)
      src/tagi/providers/gitlab.py:11-14  (is_authenticated)
  [9e51ade4e046160f]   STRU  get_custom_rules  L=3 N=2 saved=3 sim=1.00
      src/tagi/heuristics/rules.py:14-16  (get_custom_rules)
      src/tagi/heuristics/rules.py:19-21  (get_custom_heuristics)
  [ead418deaec12c72]   STRU  detect_remote  L=3 N=2 saved=3 sim=1.00
      src/tagi/providers/github.py:45-47  (detect_remote)
      src/tagi/providers/gitlab.py:53-55  (detect_remote)

REFACTOR[7] (ranked by priority):
  [1] ○ extract_function   → src/tagi/providers/utils/create_pr.py
      WHY: 2 occurrences of 12-line block across 2 files — saves 12 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [2] ○ extract_function   → src/tagi/utils/create_pr.py
      WHY: 2 occurrences of 10-line block across 1 files — saves 10 lines
      FILES: src/tagi/cli.py
  [3] ○ extract_function   → src/tagi/utils/detect_provider.py
      WHY: 2 occurrences of 9-line block across 2 files — saves 9 lines
      FILES: src/tagi/cli.py, src/tagi/providers/detector.py
  [4] ○ extract_function   → src/tagi/providers/utils/get_auth_status.py
      WHY: 2 occurrences of 8-line block across 2 files — saves 8 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [5] ○ extract_function   → src/tagi/providers/utils/is_authenticated.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [6] ○ extract_function   → src/tagi/heuristics/utils/get_custom_rules.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/tagi/heuristics/rules.py
  [7] ○ extract_function   → src/tagi/providers/utils/detect_remote.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py

QUICK_WINS[4] (low risk, high savings — do first):
  [1] extract_function   saved=12L  → src/tagi/providers/utils/create_pr.py
      FILES: github.py, gitlab.py
  [2] extract_function   saved=10L  → src/tagi/utils/create_pr.py
      FILES: cli.py
  [3] extract_function   saved=9L  → src/tagi/utils/detect_provider.py
      FILES: cli.py, detector.py
  [4] extract_function   saved=8L  → src/tagi/providers/utils/get_auth_status.py
      FILES: github.py, gitlab.py

EFFORT_ESTIMATE (total ≈ 1.6h):
  easy   create_pr                           saved=12L  ~24min
  easy   create_pr                           saved=10L  ~20min
  easy   detect_provider                     saved=9L  ~18min
  easy   get_auth_status                     saved=8L  ~16min
  easy   is_authenticated                    saved=4L  ~8min
  easy   get_custom_rules                    saved=3L  ~6min
  easy   detect_remote                       saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  7 → 0
  saved_lines: 49 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 127 func | 28f | 2026-05-26
# generated in 0.00s

NEXT[7] (ranked by impact):
  [1] !! SPLIT           src/tagi/cli.py
      WHY: 805L, 0 classes, max CC=27
      EFFORT: ~4h  IMPACT: 21735

  [2] !! SPLIT-FUNC      send  CC=27  fan=19
      WHY: CC=27 exceeds 15
      EFFORT: ~1h  IMPACT: 513

  [3] !  SPLIT-FUNC      publish  CC=17  fan=20
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 340

  [4] !  SPLIT-FUNC      inspect  CC=15  fan=20
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 300

  [5] !  SPLIT-FUNC      summary  CC=15  fan=20
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 300

  [6] !  SPLIT-FUNC      filter  CC=17  fan=17
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 289

  [7] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/tagi/cli.py may break 19 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          4.3 → ≤3.0
  max-CC:      27 → ≤13
  god-modules: 2 → 0
  high-CC(≥15): 5 → ≤2
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
  prev CC̄=4.0 → now CC̄=4.3
```

## Intent

Orchestrator for Git change shipments
