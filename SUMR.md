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
- **version**: `0.18.0`
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
  version: 0.18.0;
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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 36f 2787L | python:31,yaml:2,txt:1,shell:1,toml:1 | 2026-05-26
# generated in 0.01s
# CC̅=4.0 | critical:1/95 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    inspect CC=15 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[55]:
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
  [14] Src [get_staged_diff]: get_staged_diff
      PURITY: 100% pure
  [15] Src [get_custom_rules]: get_custom_rules
      PURITY: 100% pure
  [16] Src [get_custom_heuristics]: get_custom_heuristics
      PURITY: 100% pure
  [17] Src [__init__]: __init__
      PURITY: 100% pure
  [18] Src [improve_message]: improve_message
      PURITY: 100% pure
  [19] Src [improve_description]: improve_description
      PURITY: 100% pure
  [20] Src [generate_summary]: generate_summary
      PURITY: 100% pure
  [21] Src [generate_file_list]: generate_file_list
      PURITY: 100% pure
  [22] Src [add]: add
      PURITY: 100% pure
  [23] Src [commit]: commit
      PURITY: 100% pure
  [24] Src [push]: push
      PURITY: 100% pure
  [25] Src [status]: status
      PURITY: 100% pure
  [26] Src [get_current_branch]: get_current_branch
      PURITY: 100% pure
  [27] Src [get_remote_url]: get_remote_url
      PURITY: 100% pure
  [28] Src [has_staged_changes]: has_staged_changes
      PURITY: 100% pure
  [29] Src [__init__]: __init__
      PURITY: 100% pure
  [30] Src [stage_and_commit]: stage_and_commit
      PURITY: 100% pure
  [31] Src [publish]: publish
      PURITY: 100% pure
  [32] Src [dry_run]: dry_run
      PURITY: 100% pure
  [33] Src [scan]: scan → scan_repo → parse_status
      PURITY: 100% pure
  [34] Src [list_groups]: list_groups → _display_groups → _format_tags
      PURITY: 100% pure
  [35] Src [stats]: stats → scan_repo → parse_status
      PURITY: 100% pure
  [36] Src [inspect]: inspect → _display_changes → _format_tags
      PURITY: 100% pure
  [37] Src [filter]: filter → _display_changes → _format_tags
      PURITY: 100% pure
  [38] Src [file]: file → scan_repo → parse_status
      PURITY: 100% pure
  [39] Src [summary]: summary → scan_repo → parse_status
      PURITY: 100% pure
  [40] Src [draft]: draft → generate_commit_message → generate_conventional_message → _infer_scope
      PURITY: 100% pure
  [41] Src [send]: send → scan_repo → parse_status
      PURITY: 100% pure
  [42] Src [publish]: publish → scan_repo → parse_status
      PURITY: 100% pure
  [43] Src [_run_command]: _run_command
      PURITY: 100% pure
  [44] Src [_get_git_remote_url]: _get_git_remote_url
      PURITY: 100% pure
  [45] Src [_check_git_remote_for_provider]: _check_git_remote_for_provider
      PURITY: 100% pure
  [46] Src [is_authenticated]: is_authenticated
      PURITY: 100% pure
  [47] Src [get_auth_status]: get_auth_status
      PURITY: 100% pure
  [48] Src [get_configured_host]: get_configured_host
      PURITY: 100% pure
  [49] Src [create_pr]: create_pr
      PURITY: 100% pure
  [50] Src [detect_remote]: detect_remote
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=4.0    ←in:0  →out:0
  │ !! cli                        766L  0C   25m  CC=15     ←0
  │ commit_message             133L  0C    4m  CC=12     ←1
  │ config                     129L  1C    9m  CC=13     ←0
  │ git                        114L  1C    8m  CC=4      ←0
  │ tags                        83L  0C    2m  CC=11     ←1
  │ grouper                     75L  0C    4m  CC=7      ←1
  │ status                      67L  0C    2m  CC=7      ←1
  │ base                        58L  1C    8m  CC=2      ←0
  │ llx_adapter                 55L  1C    4m  CC=4      ←0
  │ gitlab                      55L  1C    5m  CC=4      ←0
  │ github                      47L  1C    5m  CC=4      ←0
  │ __init__                    47L  0C    0m  CC=0.0    ←0
  │ summary                     45L  0C    2m  CC=11     ←0
  │ selector                    44L  0C    5m  CC=8      ←0
  │ preview                     41L  0C    2m  CC=7      ←0
  │ publish                     39L  1C    4m  CC=3      ←0
  │ change                      37L  3C    0m  CC=0.0    ←0
  │ diff                        31L  0C    2m  CC=1      ←1
  │ scoring                     31L  0C    1m  CC=7      ←1
  │ files                       30L  0C    1m  CC=7      ←1
  │ plan                        23L  2C    0m  CC=0.0    ←0
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ group                       16L  1C    0m  CC=0.0    ←0
  │ rules                       15L  0C    2m  CC=1      ←0
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
# redup/duplication | 7 groups | 31f 2078L | 2026-05-26

SUMMARY:
  files_scanned: 31
  total_lines:   2078
  dup_groups:    7
  dup_fragments: 14
  saved_lines:   44
  scan_ms:       3095

HOTSPOTS[6] (files with most duplication):
  src/tagi/providers/github.py  dup=27L  groups=4  frags=4  (1.3%)
  src/tagi/providers/gitlab.py  dup=27L  groups=4  frags=4  (1.3%)
  src/tagi/cli.py  dup=20L  groups=1  frags=2  (1.0%)
  src/tagi/heuristics/rules.py  dup=8L  groups=1  frags=2  (0.4%)
  src/tagi/planner/grouper.py  dup=3L  groups=1  frags=1  (0.1%)
  src/tagi/planner/selector.py  dup=3L  groups=1  frags=1  (0.1%)

DUPLICATES[7] (ranked by impact):
  [69c9d9a76f7c052c]   STRU  create_pr  L=12 N=2 saved=12 sim=1.00
      src/tagi/providers/github.py:32-43  (create_pr)
      src/tagi/providers/gitlab.py:40-51  (create_pr)
  [59cf75b9ca253237]   STRU  create_pr  L=10 N=2 saved=10 sim=1.00
      src/tagi/cli.py:741-750  (create_pr)
      src/tagi/cli.py:753-762  (create_mr)
  [c70db8b1b5e736e6]   STRU  get_auth_status  L=8 N=2 saved=8 sim=1.00
      src/tagi/providers/github.py:16-23  (get_auth_status)
      src/tagi/providers/gitlab.py:16-23  (get_auth_status)
  [bd7df8cd1b30b067]   STRU  get_custom_rules  L=4 N=2 saved=4 sim=1.00
      src/tagi/heuristics/rules.py:6-9  (get_custom_rules)
      src/tagi/heuristics/rules.py:12-15  (get_custom_heuristics)
  [c1f4c1bd38f4f90b]   STRU  is_authenticated  L=4 N=2 saved=4 sim=1.00
      src/tagi/providers/github.py:11-14  (is_authenticated)
      src/tagi/providers/gitlab.py:11-14  (is_authenticated)
  [bce305937123af75]   STRU  group_by_tag  L=3 N=2 saved=3 sim=1.00
      src/tagi/planner/grouper.py:39-41  (group_by_tag)
      src/tagi/planner/selector.py:8-10  (select_changes_by_tag)
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
  [3] ○ extract_function   → src/tagi/providers/utils/get_auth_status.py
      WHY: 2 occurrences of 8-line block across 2 files — saves 8 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [4] ○ extract_function   → src/tagi/heuristics/utils/get_custom_rules.py
      WHY: 2 occurrences of 4-line block across 1 files — saves 4 lines
      FILES: src/tagi/heuristics/rules.py
  [5] ○ extract_function   → src/tagi/providers/utils/is_authenticated.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py
  [6] ○ extract_function   → src/tagi/planner/utils/group_by_tag.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: src/tagi/planner/grouper.py, src/tagi/planner/selector.py
  [7] ○ extract_function   → src/tagi/providers/utils/detect_remote.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: src/tagi/providers/github.py, src/tagi/providers/gitlab.py

QUICK_WINS[3] (low risk, high savings — do first):
  [1] extract_function   saved=12L  → src/tagi/providers/utils/create_pr.py
      FILES: github.py, gitlab.py
  [2] extract_function   saved=10L  → src/tagi/utils/create_pr.py
      FILES: cli.py
  [3] extract_function   saved=8L  → src/tagi/providers/utils/get_auth_status.py
      FILES: github.py, gitlab.py

EFFORT_ESTIMATE (total ≈ 1.5h):
  easy   create_pr                           saved=12L  ~24min
  easy   create_pr                           saved=10L  ~20min
  easy   get_auth_status                     saved=8L  ~16min
  easy   get_custom_rules                    saved=4L  ~8min
  easy   is_authenticated                    saved=4L  ~8min
  easy   group_by_tag                        saved=3L  ~6min
  easy   detect_remote                       saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  7 → 0
  saved_lines: 44 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 95 func | 19f | 2026-05-26
# generated in 0.00s

NEXT[3] (ranked by impact):
  [1] !! SPLIT           src/tagi/cli.py
      WHY: 766L, 0 classes, max CC=15
      EFFORT: ~4h  IMPACT: 11490

  [2] !  SPLIT-FUNC      inspect  CC=15  fan=20
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 300

  [3] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/tagi/cli.py may break 25 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          4.0 → ≤2.8
  max-CC:      15 → ≤7
  god-modules: 2 → 0
  high-CC(≥15): 1 → ≤0
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
  prev CC̄=5.0 → now CC̄=4.0
```

## Intent

Orchestrator for Git change shipments
