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
- **version**: `0.1.1`
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
  version: 0.1.1
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
- **version files**: `pyproject.toml:version`, `venv/lib/python3.13/site-packages/pip/__init__.py:__version__`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# tagi | 14f 866L | python:11,shell:2,less:1 | 2026-05-26
# stats: 24 func | 5 cls | 14 mod | CC̄=5.5 | critical:4 | cycles:0
# alerts[5]: CC apply_tags=24; CC generate_commit_message=14; CC publish=11; CC send=10; CC _count_lines_changed=7
# hotspots[5]: publish fan=17; send fan=15; scan fan=9; apply_tags fan=9; draft fan=8
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[14]:
  app.doql.less,29
  project.sh,48
  src/tagi/__init__.py,2
  src/tagi/cli.py,273
  src/tagi/composer.py,59
  src/tagi/config.py,64
  src/tagi/executor.py,60
  src/tagi/heuristics.py,123
  src/tagi/models.py,48
  src/tagi/planner.py,29
  src/tagi/providers.py,70
  src/tagi/scanner.py,47
  tests/test_tagi.py,12
  tree.sh,2
D:
  src/tagi/__init__.py:
  src/tagi/cli.py:
    e: scan,list_groups,inspect,draft,send,publish,_display_changes,_display_groups
    scan(repo_path)
    list_groups(repo_path)
    inspect(tag;repo_path)
    draft(tag;repo_path)
    send(tag;repo_path;dry_run;push)
    publish(tag;repo_path;dry_run)
    _display_changes(changes)
    _display_groups(groups)
  src/tagi/composer.py:
    e: generate_commit_message,_build_title
    generate_commit_message(group)
    _build_title(tag;count)
  src/tagi/config.py:
    e: Config
    Config: __init__(1),_load_config(0),get_tag_for_path(1),get_custom_tags_for_pattern(1)  # Configuration loaded from tagi.toml.
  src/tagi/executor.py:
    e: stage_changes,commit_changes,push_changes
    stage_changes(changes;repo_path;dry_run)
    commit_changes(message;repo_path;dry_run)
    push_changes(repo_path;dry_run)
  src/tagi/heuristics.py:
    e: apply_tags,_count_lines_changed,_calculate_risk_score
    apply_tags(changes;repo_path)
    _count_lines_changed(file_path;repo_path)
    _calculate_risk_score(change;tags)
  src/tagi/models.py:
    e: ChangeType,Tag,Change,ChangeGroup
    ChangeType:  # Type of git change.
    Tag:  # Hashtag categories for changes.
    Change:  # Represents a single file change.
    ChangeGroup:  # Group of related changes.
  src/tagi/planner.py:
    e: group_changes
    group_changes(changes)
  src/tagi/providers.py:
    e: create_pr,create_mr,detect_provider
    create_pr(title;body;repo_path;dry_run)
    create_mr(title;body;repo_path;dry_run)
    detect_provider(repo_path)
  src/tagi/scanner.py:
    e: scan_repo,_parse_status
    scan_repo(repo_path)
    _parse_status(status)
  tests/test_tagi.py:
    e: test_placeholder,test_import
    test_placeholder()
    test_import()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
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

## Intent

Orchestrator for Git change shipments
