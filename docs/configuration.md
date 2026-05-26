# Configuration

## Overview

Tagi can be configured using a `tagi.toml` file in the root of your repository. This allows you to customize tagging rules, colors, heuristics, and tag definitions for your specific project.

## Getting Started

Generate an example configuration file:

```bash
tagi init /path/to/repo
```

This creates `tagi.toml.example`. Copy it to `tagi.toml` and customize:

```bash
cp tagi.toml.example tagi.toml
```

## Configuration Sections

### [rules]

Map file paths to tags. Files matching the pattern will be assigned the specified tag.

```toml
[rules]
"frontend/" = "frontend"
"backend/" = "backend"
"migration/" = "risky"
"tests/" = "tests"
"docs/" = "docs"
```

**Pattern Matching:**
- Prefix matching: `"api/"` matches `api/users.py`, `api/auth/`
- Exact matching: `"config.yaml"` matches only `config.yaml`
- Suffix matching: Not supported (use full path)

### [colors]

Customize display colors for tags using Rich color names.

```toml
[colors]
"frontend" = "blue"
"backend" = "green"
"risky" = "red"
"tests" = "magenta"
"docs" = "cyan"
```

**Available Colors:**
- Standard colors: `red`, `green`, `blue`, `yellow`, `magenta`, `cyan`, `white`, `black`
- Bright variants: `bright_red`, `bright_green`, etc.
- Styles: `bold`, `dim`, `italic`, `underline`

### [heuristics]

Map patterns to multiple tags. A file can have multiple tags assigned.

```toml
[heuristics]
"api/" = ["api", "backend"]
"cli/" = ["cli", "tool"]
"migration/" = ["risky", "database"]
```

**Use Cases:**
- API files get both `api` and `backend` tags
- CLI tools get both `cli` and `tool` tags
- Database migrations get both `risky` and `database` tags

### [tag_definitions]

Provide descriptions for tags that appear in command output.

```toml
[tag_definitions]
"small" = "Małe zmiany (< 10 linii)"
"large" = "Duże zmiany (> 100 linii)"
"risky" = "Wysokie ryzyko (auth, migrations, infra)"
"docs" = "Dokumentacja"
"tests" = "Testy"
"deps" = "Zależności"
```

## Complete Example

```toml
# tagi.toml - Configuration file for tagi

[rules]
# Map file paths to tags
"frontend/" = "frontend"
"backend/" = "backend"
"migration/" = "risky"
"tests/" = "tests"
"docs/" = "docs"
"config/" = "config"

[colors]
# Custom colors for tags (Rich color names)
"frontend" = "blue"
"backend" = "green"
"risky" = "red"
"tests" = "magenta"
"docs" = "cyan"
"config" = "yellow"

[heuristics]
# Custom heuristics - map patterns to multiple tags
"api/" = ["api", "backend"]
"cli/" = ["cli", "tool"]
"migration/" = ["risky", "database"]
"infra/" = ["risky", "infra"]

[tag_definitions]
# Tag descriptions
"small" = "Małe zmiany (< 10 linii)"
"large" = "Duże zmiany (> 100 linii)"
"risky" = "Wysokie ryzyko (auth, migrations, infra)"
"docs" = "Dokumentacja"
"tests" = "Testy"
"deps" = "Zależności"
"frontend" = "Frontend changes"
"backend" = "Backend changes"
"api" = "API changes"
```

## Tag Auto-Prefix

Tags in configuration do **not** need the `#` prefix. Tagi automatically adds the prefix when needed.

**Example:**
```toml
[rules]
"frontend/" = "frontend"  # Correct - will be treated as #frontend
"docs/" = "#docs"        # Also works but prefix is optional
```

## How Configuration is Loaded

1. Tagi looks for `tagi.toml` in the repository root
2. If not found, uses default heuristics and colors
3. Configuration is loaded on each command execution
4. Changes to `tagi.toml` take effect immediately

## Default Behavior

Without configuration, tagi uses built-in heuristics:

- **File type detection**: `.py`, `.js`, `.ts`, etc.
- **Path-based tagging**: `test/` → tests, `doc/` → docs
- **Size-based tagging**: < 10 lines → small, > 100 lines → large
- **Risk scoring**: Based on file type and changes

## Troubleshooting

### Configuration Not Applied

**Problem**: Custom rules not being used

**Solutions**:
1. Ensure file is named `tagi.toml` (not `tagi.toml.example`)
2. Check file is in repository root
3. Verify TOML syntax is valid
4. Check for typos in section names

### Invalid TOML Syntax

**Problem**: Configuration file causing errors

**Solutions**:
1. Use a TOML validator to check syntax
2. Ensure strings are quoted: `"value"` not `value`
3. Check for proper array syntax: `["a", "b"]` not `[a, b]`
4. Verify section headers: `[section]` not `[section]`

### Tags Not Showing Colors

**Problem**: Custom colors not appearing

**Solutions**:
1. Verify color names are valid Rich colors
2. Check terminal supports colors
3. Ensure tag names in `[colors]` match tags in `[rules]`
4. Try standard colors: `red`, `green`, `blue`, etc.
