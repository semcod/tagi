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
- **version**: `0.1.1`
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
  version: 0.1.1;
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

*17 nodes · 25 edges · 6 modules · CC̄=5.4*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `publish` *(in src.tagi.cli)* | 11 ⚠ | 0 | 34 | **34** |
| `apply_tags` *(in src.tagi.heuristics)* | 24 ⚠ | 6 | 27 | **33** |
| `send` *(in src.tagi.cli)* | 10 ⚠ | 0 | 32 | **32** |
| `generate_commit_message` *(in src.tagi.composer)* | 14 ⚠ | 3 | 18 | **21** |
| `scan_repo` *(in src.tagi.scanner)* | 3 | 6 | 7 | **13** |
| `draft` *(in src.tagi.cli)* | 4 | 0 | 12 | **12** |
| `group_changes` *(in src.tagi.planner)* | 7 | 4 | 8 | **12** |
| `scan` *(in src.tagi.cli)* | 3 | 0 | 11 | **11** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/tagi
# generated in 0.01s
# nodes: 17 | edges: 25 | modules: 6
# CC̄=5.4

HUBS[20]:
  src.tagi.cli.publish
    CC=11  in:0  out:34  total:34
  src.tagi.heuristics.apply_tags
    CC=24  in:6  out:27  total:33
  src.tagi.cli.send
    CC=10  in:0  out:32  total:32
  src.tagi.composer.generate_commit_message
    CC=14  in:3  out:18  total:21
  src.tagi.scanner.scan_repo
    CC=3  in:6  out:7  total:13
  src.tagi.cli.draft
    CC=4  in:0  out:12  total:12
  src.tagi.planner.group_changes
    CC=7  in:4  out:8  total:12
  src.tagi.cli.scan
    CC=3  in:0  out:11  total:11
  src.tagi.cli._display_groups
    CC=3  in:1  out:9  total:10
  src.tagi.cli._display_changes
    CC=3  in:2  out:7  total:9
  src.tagi.cli.inspect
    CC=4  in:0  out:9  total:9
  src.tagi.cli.list_groups
    CC=2  in:0  out:8  total:8
  src.tagi.heuristics._count_lines_changed
    CC=7  in:1  out:7  total:8
  src.tagi.heuristics._calculate_risk_score
    CC=7  in:1  out:2  total:3
  src.tagi.providers.detect_provider
    CC=3  in:1  out:1  total:2
  src.tagi.composer._build_title
    CC=1  in:1  out:1  total:2
  src.tagi.scanner._parse_status
    CC=4  in:1  out:0  total:1

MODULES:
  src.tagi.cli  [8 funcs]
    _display_changes  CC=3  out:7
    _display_groups  CC=3  out:9
    draft  CC=4  out:12
    inspect  CC=4  out:9
    list_groups  CC=2  out:8
    publish  CC=11  out:34
    scan  CC=3  out:11
    send  CC=10  out:32
  src.tagi.composer  [2 funcs]
    _build_title  CC=1  out:1
    generate_commit_message  CC=14  out:18
  src.tagi.heuristics  [3 funcs]
    _calculate_risk_score  CC=7  out:2
    _count_lines_changed  CC=7  out:7
    apply_tags  CC=24  out:27
  src.tagi.planner  [1 funcs]
    group_changes  CC=7  out:8
  src.tagi.providers  [1 funcs]
    detect_provider  CC=3  out:1
  src.tagi.scanner  [2 funcs]
    _parse_status  CC=4  out:0
    scan_repo  CC=3  out:7

EDGES:
  src.tagi.cli.scan → src.tagi.scanner.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.scanner.scan_repo
  src.tagi.cli.list_groups → src.tagi.heuristics.apply_tags
  src.tagi.cli.list_groups → src.tagi.planner.group_changes
  src.tagi.cli.list_groups → src.tagi.cli._display_groups
  src.tagi.cli.inspect → src.tagi.scanner.scan_repo
  src.tagi.cli.inspect → src.tagi.heuristics.apply_tags
  src.tagi.cli.inspect → src.tagi.cli._display_changes
  src.tagi.cli.draft → src.tagi.scanner.scan_repo
  src.tagi.cli.draft → src.tagi.heuristics.apply_tags
  src.tagi.cli.draft → src.tagi.planner.group_changes
  src.tagi.cli.draft → src.tagi.composer.generate_commit_message
  src.tagi.cli.send → src.tagi.scanner.scan_repo
  src.tagi.cli.send → src.tagi.heuristics.apply_tags
  src.tagi.cli.send → src.tagi.planner.group_changes
  src.tagi.cli.publish → src.tagi.scanner.scan_repo
  src.tagi.cli.publish → src.tagi.heuristics.apply_tags
  src.tagi.cli.publish → src.tagi.planner.group_changes
  src.tagi.cli.publish → src.tagi.providers.detect_provider
  src.tagi.composer.generate_commit_message → src.tagi.composer._build_title
  src.tagi.scanner.scan_repo → src.tagi.scanner._parse_status
  src.tagi.heuristics.apply_tags → src.tagi.heuristics._count_lines_changed
  src.tagi.heuristics.apply_tags → src.tagi.heuristics._calculate_risk_score
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
# nodes: 17 | edges: 25 | modules: 6
# CC̄=5.4

HUBS[20]:
  src.tagi.cli.publish
    CC=11  in:0  out:34  total:34
  src.tagi.heuristics.apply_tags
    CC=24  in:6  out:27  total:33
  src.tagi.cli.send
    CC=10  in:0  out:32  total:32
  src.tagi.composer.generate_commit_message
    CC=14  in:3  out:18  total:21
  src.tagi.scanner.scan_repo
    CC=3  in:6  out:7  total:13
  src.tagi.cli.draft
    CC=4  in:0  out:12  total:12
  src.tagi.planner.group_changes
    CC=7  in:4  out:8  total:12
  src.tagi.cli.scan
    CC=3  in:0  out:11  total:11
  src.tagi.cli._display_groups
    CC=3  in:1  out:9  total:10
  src.tagi.cli._display_changes
    CC=3  in:2  out:7  total:9
  src.tagi.cli.inspect
    CC=4  in:0  out:9  total:9
  src.tagi.cli.list_groups
    CC=2  in:0  out:8  total:8
  src.tagi.heuristics._count_lines_changed
    CC=7  in:1  out:7  total:8
  src.tagi.heuristics._calculate_risk_score
    CC=7  in:1  out:2  total:3
  src.tagi.providers.detect_provider
    CC=3  in:1  out:1  total:2
  src.tagi.composer._build_title
    CC=1  in:1  out:1  total:2
  src.tagi.scanner._parse_status
    CC=4  in:1  out:0  total:1

MODULES:
  src.tagi.cli  [8 funcs]
    _display_changes  CC=3  out:7
    _display_groups  CC=3  out:9
    draft  CC=4  out:12
    inspect  CC=4  out:9
    list_groups  CC=2  out:8
    publish  CC=11  out:34
    scan  CC=3  out:11
    send  CC=10  out:32
  src.tagi.composer  [2 funcs]
    _build_title  CC=1  out:1
    generate_commit_message  CC=14  out:18
  src.tagi.heuristics  [3 funcs]
    _calculate_risk_score  CC=7  out:2
    _count_lines_changed  CC=7  out:7
    apply_tags  CC=24  out:27
  src.tagi.planner  [1 funcs]
    group_changes  CC=7  out:8
  src.tagi.providers  [1 funcs]
    detect_provider  CC=3  out:1
  src.tagi.scanner  [2 funcs]
    _parse_status  CC=4  out:0
    scan_repo  CC=3  out:7

EDGES:
  src.tagi.cli.scan → src.tagi.scanner.scan_repo
  src.tagi.cli.scan → src.tagi.heuristics.apply_tags
  src.tagi.cli.scan → src.tagi.cli._display_changes
  src.tagi.cli.list_groups → src.tagi.scanner.scan_repo
  src.tagi.cli.list_groups → src.tagi.heuristics.apply_tags
  src.tagi.cli.list_groups → src.tagi.planner.group_changes
  src.tagi.cli.list_groups → src.tagi.cli._display_groups
  src.tagi.cli.inspect → src.tagi.scanner.scan_repo
  src.tagi.cli.inspect → src.tagi.heuristics.apply_tags
  src.tagi.cli.inspect → src.tagi.cli._display_changes
  src.tagi.cli.draft → src.tagi.scanner.scan_repo
  src.tagi.cli.draft → src.tagi.heuristics.apply_tags
  src.tagi.cli.draft → src.tagi.planner.group_changes
  src.tagi.cli.draft → src.tagi.composer.generate_commit_message
  src.tagi.cli.send → src.tagi.scanner.scan_repo
  src.tagi.cli.send → src.tagi.heuristics.apply_tags
  src.tagi.cli.send → src.tagi.planner.group_changes
  src.tagi.cli.publish → src.tagi.scanner.scan_repo
  src.tagi.cli.publish → src.tagi.heuristics.apply_tags
  src.tagi.cli.publish → src.tagi.planner.group_changes
  src.tagi.cli.publish → src.tagi.providers.detect_provider
  src.tagi.composer.generate_commit_message → src.tagi.composer._build_title
  src.tagi.scanner.scan_repo → src.tagi.scanner._parse_status
  src.tagi.heuristics.apply_tags → src.tagi.heuristics._count_lines_changed
  src.tagi.heuristics.apply_tags → src.tagi.heuristics._calculate_risk_score
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 14f 1388L | python:10,shell:2,yaml:1,toml:1 | 2026-05-26
# generated in 0.00s
# CC̅=5.4 | critical:1/26 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    apply_tags CC=24 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[10]:
  [1] Src [__init__]: __init__
      PURITY: 100% pure
  [2] Src [_load_config]: _load_config
      PURITY: 100% pure
  [3] Src [get_tag_for_path]: get_tag_for_path
      PURITY: 100% pure
  [4] Src [get_custom_tags_for_pattern]: get_custom_tags_for_pattern
      PURITY: 100% pure
  [5] Src [scan]: scan → scan_repo → _parse_status
      PURITY: 100% pure
  [6] Src [list_groups]: list_groups → scan_repo → _parse_status
      PURITY: 100% pure
  [7] Src [inspect]: inspect → scan_repo → _parse_status
      PURITY: 100% pure
  [8] Src [draft]: draft → scan_repo → _parse_status
      PURITY: 100% pure
  [9] Src [send]: send → scan_repo → _parse_status
      PURITY: 100% pure
  [10] Src [publish]: publish → scan_repo → _parse_status
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=5.4    ←in:0  →out:0
  │ cli                        272L  0C    8m  CC=11     ←0
  │ !! heuristics                 122L  0C    3m  CC=24     ←1
  │ providers                   69L  0C    3m  CC=4      ←1
  │ config                      63L  1C    4m  CC=6      ←0
  │ executor                    59L  0C    3m  CC=5      ←1
  │ composer                    58L  0C    2m  CC=14     ←1
  │ models                      47L  4C    0m  CC=0.0    ←0
  │ scanner                     46L  0C    2m  CC=4      ←1
  │ planner                     28L  0C    1m  CC=7      ←1
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  510L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              64L  0C    0m  CC=0.0    ←0
  │ project.sh                  48L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │

COUPLING: no cross-package imports detected

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 1 groups | 10f 765L | 2026-05-26

SUMMARY:
  files_scanned: 10
  total_lines:   765
  dup_groups:    1
  dup_fragments: 2
  saved_lines:   21
  scan_ms:       2108

HOTSPOTS[1] (files with most duplication):
  src/tagi/providers.py  dup=42L  groups=1  frags=2  (5.5%)

DUPLICATES[1] (ranked by impact):
  [e67f77bbdc4b5d22]   STRU  create_pr  L=21 N=2 saved=21 sim=1.00
      src/tagi/providers.py:7-27  (create_pr)
      src/tagi/providers.py:30-50  (create_mr)

REFACTOR[1] (ranked by priority):
  [1] ○ extract_function   → src/tagi/utils/create_pr.py
      WHY: 2 occurrences of 21-line block across 1 files — saves 21 lines
      FILES: src/tagi/providers.py

QUICK_WINS[1] (low risk, high savings — do first):
  [1] extract_function   saved=21L  → src/tagi/utils/create_pr.py
      FILES: providers.py

EFFORT_ESTIMATE (total ≈ 0.7h):
  medium create_pr                           saved=21L  ~42min

METRICS-TARGET:
  dup_groups:  1 → 0
  saved_lines: 21 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 26 func | 8f | 2026-05-26
# generated in 0.00s

NEXT[2] (ranked by impact):
  [1] !  SPLIT-FUNC      apply_tags  CC=24  fan=9
      WHY: CC=24 exceeds 15
      EFFORT: ~1h  IMPACT: 216

  [2] !! SPLIT           goal.yaml
      WHY: 510L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          5.4 → ≤3.8
  max-CC:      24 → ≤12
  god-modules: 1 → 0
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
  (first run — no previous data)
```

## Intent

Orchestrator for Git change shipments
